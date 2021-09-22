import argparse
from coffea import hist, processor
from topcoffea.modules.YieldTools import YieldTools
from topcoffea.modules.GetValuesFromJsons import get_lumi, get_cut
import cloudpickle
from collections import defaultdict 
import re, gzip

class DataDrivenProducer: 
    def __init__(self, inputHist, outputName, doDDFakes=True, doDDFlips=False):
        yt=YieldTools()
        if type(inputHist) == str and inputHist.endswith('.pkl.gz'): # we are plugging a pickle file
            self.inhist=yt.get_hist_from_pkl(inputHist)
        else: # we already have the histogram
            self.inhist=inputHist
        self.outputName=outputName
        if doDDFlips: 
            raise RuntimeError("Data driven flips not yet implemented")
        self.doDDFlips=doDDFlips
        self.doDDFakes=doDDFakes
        self.dataName='data'
        self.chargeFlipName='chargeFip' # place holder, to implement in the future
        self.outHist=None
        self.promptSubtractionSamples=get_cut('prompt_subtraction_samples')
        self.DDFakes()

    def DDFakes(self):
        if self.outHist!=None:  # already some processing has been done, so using what is available
            self.inhist=self.outHist
            
        self.outHist={}
        if 'SumOfEFTweights' in self.inhist:
            self.outHist['SumOfEFTweights']=self.inhist['SumOfEFTweights']
            SumOfEFTweights=self.inhist['SumOfEFTweights']
            SumOfEFTweights.set_sm()
            self.smsow = {proc: SumOfEFTweights.integrate('sample', proc).values()[()][0] for proc in SumOfEFTweights.identifiers('sample') if SumOfEFTweights.integrate('sample', proc)._nwc} # get only samples with EFT stuff

        for key,histo in self.inhist.items():
            if key == 'SumOfEFTweights': 
                # we have already dealt with the sum of weights
                continue 

            if not len(histo.values()): # histo is empty, so we just integrate over appl and keep an empty histo
                print(f'[W]: Histogram {key} is empty, returning an empty histo')
                self.outHist[key]=histo.integrate('appl')
                continue

            if not self.doDDFakes:
                # if we are not gonna use the data-driven, then we don't care about the application region, so we get rid of it, and the associated dimension
                srs=[ histo.integrate('appl',ident) for ident in histo.identifiers('appl') if 'SR' in ident.name]
                if not len(srs):
                    raise RuntimeError(f"Histogram {key} does not have any signal region")
                newhist=srs[0]
                for h in srs[1:]:
                    newhist = newhist + h # sum doesnt work for some reason...
            else:

                # First we are gonna scale all MC processes in  by the luminosity
                name_regex='(?P<sample>.*)UL(?P<year>.*)'
                pattern=re.compile(name_regex)

                scale_dict={}
                for sample in histo.identifiers('sample'):
                    match = pattern.search(sample.name)
                    sampleName=match.group('sample')
                    year=match.group('year')
                    if not match: 
                        raise RuntimeError(f"Sample {sample} does not match the naming convention")
                    if year not in ['16','17','18']:
                        raise RuntimeError(f"Sample {sample} does not match the naming convention")

                    if self.dataName == sampleName or self.chargeFlipName == sampleName:
                        continue # We do not scale data or data-driven at all 
                    smweight = self.smsow[sample] if sample in self.smsow else 1 # dont reweight samples not in smsow
                    scale_dict[(sample, )] = 1000*get_lumi('20'+year)/smweight

                prescale=histo.values().copy()
                histo.scale( scale_dict, axis=('sample',))
                postscale=histo.values()

                # now for each year we actually perform the subtraction and integrate out the application regions
                newhist=None
                for ident in histo.identifiers('appl'):
                    hAR=histo.integrate('appl', ident)

                    if 'isAR' not in ident.name:
                        # if we are in the signal region, we just take the 
                        # whole histogram integrating out the application region axis
                        if newhist==None:
                            newhist=hAR
                        else:
                            newhist=newhist+hAR
                    else:
                        # if we are in the application region, we also integrate the application region axis
                        # and construct the new sample 'nonprompt'

                        # we look at data only, and rename it to fakes
                        newNameDictData=defaultdict(list); newNameDictNoData=defaultdict(list)
                        addedNonPrompts=[]
                        for sample in hAR.identifiers('sample'):
                            match = pattern.search(sample.name)
                            sampleName=match.group('sample')
                            year=match.group('year')
                            nonPromptName='nonpromptUL%s'%year
                            if self.dataName==sampleName:
                                newNameDictData[nonPromptName].append(sample.name)
                                addedNonPrompts.append( (nonPromptName, year)) # keep it to rescale later
                            elif sampleName in self.promptSubtractionSamples: 
                                newNameDictNoData[nonPromptName].append(sample.name)
                            else:
                                print(f"We won't consider {sampleName} for the prompt subtraction in the appl. region")
                        
                        hFakes=hAR.group('sample',  hist.Cat('sample','sample'), newNameDictData)
                    
                        # now we take all the stuff that is not data in the AR to make the prompt subtraction and assign them to nonprompt.
                        hPromptSub=hAR.group('sample', hist.Cat('sample','sample'), newNameDictNoData )
                        
                        # now we actually make the subtraction
                        hPromptSub.scale(-1)
                        hFakes=hFakes+hPromptSub

                        

                        # now adding them to the list of processes: 
                        if newhist==None:
                            newhist=hFakes
                        else:
                            newhist=newhist+hFakes

                # scale back by 1/lumi all processes but data so they can be used transparently downtream
                # mind that we scaled all mcs already above
                scaleDict={}
                for sample in newhist.identifiers('sample'):
                    match = pattern.search(sample.name)
                    sampleName=match.group('sample')
                    if self.dataName == sampleName or self.chargeFlipName == sampleName:
                        continue
                    year=match.group('year')
                    scaleDict[sample]=1/(1000*get_lumi('20'+year))
                print(scaleDict)
                newhist.scale( scaleDict, axis='sample')
            

            self.outHist[key]=newhist

    def dumpToPickle(self):
        with gzip.open(self.outputName + ".pkl.gz", "wb") as fout:
            cloudpickle.dump(self.outHist, fout)


    def getDataDrivenHistogram(self):
        return self.outHist


if __name__ == "__main__":

    yt = YieldTools()

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--pkl-file-path", default="histos/plotsTopEFT.pkl.gz", help = "The path to the pkl file")
    parser.add_argument("-y", "--year", default="2017", help = "The year of the sample")
    args = parser.parse_args()


    DataDrivenProducer(args.pkl_file_path, '',args.year)
