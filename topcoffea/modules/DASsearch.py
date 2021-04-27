# Usage:
# python CheckDatasets.py datasets/mc2018.txt
# python CheckDatasets.py /TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM
# python CheckDatasets.py /TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM -o files
# python CheckDatasets.py /TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv6-Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/NANOAODSIM -o nevents
#
# To get a dict with all the needed info to run:
#  Get full dataset, all files: GetDatasetFromDAS(dataset, withRedirector='root://cms-xrd-global.cern.ch/')    
#  Get full dataset, n files  : GetDatasetFromDAS(dataset, nFiles, withRedirector='root://cms-xrd-global.cern.ch/')    
#  Get info for just n files  : GetDatasetFromDAS(dataset, nFiles, options='file', withRedirector='root://cms-xrd-global.cern.ch/') 
#

import os, sys, subprocess

# Check and load voms certificate
def HasVomsProxy():
  return True
  #process = subprocess.Popen('voms-proxy-info', stdout=subprocess.PIPE)
  #output, error = process.communicate()
  #output=str(output)
  #l = [int(x) for x in output[output.find('timeleft'):].split('\n')[0].replace(' ', '').replace('\\n', '').replace("'", "").split(':')[1:]]
  #return (not l == [0]*len(l))

if not HasVomsProxy():
  print('[DASsearch] Please, load your voms proxy...')
  os.system('voms-proxy-init -voms cms')
if not HasVomsProxy():
  print('[DASsearch] Error loading voms proxy...')
  exit()

# Check if dasgoclient is available
if not os.path.isfile('/cvmfs/cms.cern.ch/common/dasgoclient'):
  print('[DASsearch] Hmmm... dasgoclient seems not to be available in "/cvmfs/cms.cern.ch/common/dasgoclient"...')
  exit()

def GetDasGoClientCommand(opt=''):
  ''' Get dasgoclient command '''
  command = '/cvmfs/cms.cern.ch/common/dasgoclient --query="%s dataset =%s" %s'
  mode='dataset' if not 'file' in opt.lower() else 'file'
  extropt = '' if not 'json' in opt.lower() else ' -json'
  command = command%(mode, '%s', extropt)
  return command

def ReadDatasetsFromFile(fname):
  ''' Read datasets from a file with dataset names '''
  datasets = []
  if os.path.isfile(fname):
    f = open(fname)
    print('Opening file: %s'%fname)
    for l in f.readlines():
      if l.startswith('#'): continue
      if '#' in l: l = l.split('#')[0]
      l = l.replace(' ', '').replace('\n', '')
      if l == '': continue
      datasets.append(l)
  else: datasets = [fname]
  return datasets

def GetEvDic(l):
  ''' Search for some values when using the -json options in dasgoclient '''
  for d2 in l:
    for d in d2['dataset']:
      if 'nevents' in d.keys():
        return d
  return {}


def CheckDatasets(datasets):
  ''' Check that a dataset exist and is accesible '''
  command = GetDasGoClientCommand('')
  for d in datasets:
    match = os.popen(command%d).read()
    match = match.replace('\n', '')
    warn = '\033[0;32mOK       \033[0m' if match == d else '\033[0;31mNOT FOUND\033[0m'
    print('[%s] %s'%(warn, d))

def GetFilesFromDatasets(datasets, nFiles=None, withRedirector='', verbose=False):
  ''' Get all the rootfiles associated to a dataset '''
  if isinstance(datasets, list) and len(datasets) == 1: datasets = datasets[0]
  if isinstance(datasets, list):
    files = {}
    for d in datasets: files[d] = GetFilesFromDatasets(d)
    return files
  else:
    command = GetDasGoClientCommand('file')
    match = os.popen(command%datasets).read()
    if match.endswith('\n'): match=match[:-1]
    match = match.replace(' ', '').split('\n')
    if withRedirector != '':
      #redirect = 'root://cms-xrd-global.cern.ch/' 
      match = [withRedirector+s for s in match]
    if verbose:
      for d in match: print(d)
    if not nFiles is None: return match[:nFiles]
    return match

def GetDatasetNumbers(dataset, options='', verbose=0):
  ''' Get some info of a full dataset using dasgoclient -json '''
  dic = {'events' : 0, 'nfiles' : 0, 'size' : 0}
  if not isinstance(dataset, list): dataset=[dataset]
  for d in dataset:
    command = GetDasGoClientCommand('json')
    match = os.popen(command%d).read()
    match = match.replace('\n', '').replace('null', '""')
    l = eval(match)
    fdic = GetEvDic(l)
    if fdic == {}:
      print('\nWARNING: not found categories of dataset ', d)
      return dic
    dic['events'] += fdic['nevents']
    dic['nfiles'] += fdic['nfiles']
    dic['size'  ] += fdic['size']
    size    = fdic['size']/1e6
  if   options.lower() in ['events', 'evt', 'event', 'nevents', 'nevent']:
    if verbose: print('Events = ', dic['events'])
    return dic['events']
  elif options.lower() in ['nfiles']:
    if verbose: print('Number of files = ', dic['nfiles'])
    return dic['nfiles']
  elif options.lower() in ['size', 'store', 'storage']:
    if verbose: print('Size = ', dic['size'])
    return dic['size']
  else:
    if verbose: print('nevets = %i, nfiles = %i, size = %1.2f MB'%(dic['events'], dic['nfiles'], dic['size']))
    return dic

def GetFilesInDataset(dataset, nFiles=1, withRedirector='', verbose=0):
  ''' Get some info of nFiles in a dataset using dasgoclient -json '''
  dic = {'events' : 0, 'nfiles' : 0, 'size' : 0, 'files' : []}
  if not isinstance(dataset, list): dataset=[dataset]
  for d in dataset:
    command = GetDasGoClientCommand('filejson')
    match = os.popen(command%d).read()
    #match = match.replace('\n', '').replace('null', '""')
    match = match.replace('\n', '').replace('null', '""')
    l = eval(match)
    nf = 0
    for f in l:
      nf += 1
      fdic = f['file'][0]
      dic['events'] += fdic['nevents']
      dic['files']  += [(withRedirector) + fdic['name']]
      dic['size'  ] += fdic['size']
      if nf == nFiles: break
    dic['nfiles'] = len(dic['files'])
    return dic

def GetDatasetFromDAS(dataset, nFiles=None, options='', withRedirector='', verbose=0):
  ''' Get full dataset, all files: GetDatasetFromDAS(dataset, withRedirector='root://cms-xrd-global.cern.ch/')    
      Get full dataset, n files  : GetDatasetFromDAS(dataset, nFiles, withRedirector='root://cms-xrd-global.cern.ch/')    
      Get info for just n files  : GetDatasetFromDAS(dataset, nFiles, options='file', withRedirector='root://cms-xrd-global.cern.ch/') '''
  if not 'file' in options.lower():
    # Check event numbers for nFiles
    dic = GetDatasetNumbers(dataset, withRedirector=withRedirector, verbose=verbose)
    files = GetFilesFromDatasets(dataset, nFiles, withRedirector=withRedirector, verbose=verbose)
    dic['files'] = files
  else:
    # Check event numbers for the full dataset
    dic = GetFilesInDataset(dataset, nFiles, withRedirector, verbose)
  return dic



def main():
  ''' Executing from terminal, obtain info for some datasets '''
  import argparse
  parser = argparse.ArgumentParser(description='Look for datasets using dasgoclient')
  parser.add_argument('--verbose','-v'    , default=0, help = 'Activate the verbosing')
  parser.add_argument('--pretend','-p'    , action='store_true'  , help = 'Do pretend')
  parser.add_argument('--test','-t'       , action='store_true'  , help = 'Do test')
  parser.add_argument('--options','-o'    , default=''           , help = 'Options to pass to your producer')
  parser.add_argument('dataset'           , default=''           , nargs='?', help = 'txt file with datasets or dataset name')

  args = parser.parse_args()

  verbose     = args.verbose
  doPretend   = args.pretend
  dotest      = args.test
  dataset     = args.dataset
  options     = args.options

  datasets = ReadDatasetsFromFile(dataset)
  if   options == '': CheckDatasets(datasets)
  elif options in ['file', 'files']: GetFilesFromDatasets(datasets, verbose=True)
  else : GetDatasetNumbers(datasets, options, verbose=True)

if __name__ == '__main__':
  main()
