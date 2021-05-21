'''
  createJSON.py

  This script looks for samples an create a json with paths and metadata
  You can use the json file to run on a dataset, providing a prefix (rxd redirector, local path...)

  You can execute this script in different modes:
  1) Rootfiles locally or through xrootd with the format:
       Directory: [Prefix]/path/to/files/
       Names:     sampleName1_0.root sampleName1_1.root ... sampleName2_0.root sampleName2_1.root ...
     (a single dir containing files for multiple datasets.. you can pass a list of sample names)
  2) Rootfiles in a local dir or accesible through xrootd with the format:
       [Prefix]/path/to/files/
       subdir1/ subdir2/...
       tree_0.root tree_1.root...
     (similar to the output from crab, where you have a structure of folders and want to collect all the rootfiles inside a parent folder)
  3) Dataset published in DAS
     
  Inputs:
  - Is data?
  - year
  - cross section (or file to read the cross section + name in file)

  - tree name ('Events' by default)

  Usage:
    1) and 2)
    MC:
    >> python createJSON.py [path] --prefix "root:/REDIRECTOR/" --sampleName "ttllnunu0, ttllnunu1" --xsec topcoffea/cfg/xsec.cfg --xsecName TTTo2L2Nu  --year 2018
    Data:
    >> python createJSON.py [path] --prefix "root:/REDIRECTOR/" --sampleName MuonEG_2018 --isData --year 2018

    3)
    MC:
    >> python createJSON.py [DAS_dataset] --DAS --sampleName TTTo2L2Nu --xsec topcoffea/cfg/xsec.cfg
    Data:
    >> python createJSON.py [DAS_dataset] --DAS --sampleName DoubleMuon_2017 --isData --year 2017

  Note: the "--xsecName TTTo2L2Nu" argument is only needed if sampleName does not exist in topcoffea/cfg/xsec.cfg


'''

import os, sys
from coffea.util import save
from topcoffea.modules.DASsearch import GetDatasetFromDAS
from topcoffea.modules.paths import topcoffea_path
from topcoffea.modules.fileReader import GetFiles, GetAllInfoFromFile, GetListOfWCs
from topcoffea.modules.samples import loadxsecdic
basepath = topcoffea_path("") # Just want path to topcoffea/topcoffea, not any particular file within it, so just pass "" to the function

def main():
  import argparse
  parser = argparse.ArgumentParser(description='Create json file with list of samples and metadata')
  parser.add_argument('path'              , default=''           , help = 'Path to directory or DAS dataset')
  parser.add_argument('--prefix','-p'     , default=''           , help = 'Prefix to add to the path (e.g. redirector)')
  parser.add_argument('--sampleName','-s' , default=''           , help = 'Sample name, used to find files and/or output name')
  parser.add_argument('--xsec','-x'       , default=1            , help = 'Cross section (number or file to read)')
  parser.add_argument('--xsecName'        , default=''           , help = 'Name in cross section .cfg (only if different from sampleName)')
  parser.add_argument('--year','-y'       , default=-1           , help = 'Year')
  parser.add_argument('--treename'        , default='Events'     , help = 'Name of the tree')

  parser.add_argument('--DAS'             , action='store_true'  , help = 'Search files from DAS dataset')
  parser.add_argument('--nFiles'          , default=None         , help = 'Number of max files (for the moment, only applies for DAS)')

  parser.add_argument('--outname','-o'    , default=''           , help = 'Out name of the json file')
  parser.add_argument('--options'         , default=''           , help = 'Sample-dependent options to pass to your analysis')
  parser.add_argument('--verbose','-v'    , action='store_true'  , help = 'Activate the verbosing')

  args, unknown = parser.parse_known_args()
  #cfgfile     = args.cfgfile
  path        = args.path
  prefix      = args.prefix
  sample      = args.sampleName
  xsec        = args.xsec
  xsecName    = args.xsecName
  year        = args.year
  options     = args.options
  treeName    = args.treename
  outname     = args.outname
  isDAS       = args.DAS
  nFiles      = int(args.nFiles) if not args.nFiles is None else None
  verbose     = args.verbose

  # Get the xsec for the dataset
  if xsecName == '': xsecName = sample
  try:
    xsec = float(xsec)
  except:
    xsecdic = loadxsecdic(xsec, verbose)
    if xsecName in xsecdic.keys():
      xsec = xsecdic[xsecName]
    else:
      print('Setting xsec=1 for dataset %s'%xsecName)

  sampdic = {}
  sampdic['xsec']       = xsec
  sampdic['year']       = year
  sampdic['treeName']   = treeName
  sampdic['options']    = options

  # 1) Search files with name 'sample' or 'sample1, sample2...' in path
  if not isDAS:
    filesWithPrefix = GetFiles(prefix+path, sample)

  # 2) Get all rootfiles in a dir and all the sub dirs
    if filesWithPrefix == []:
      filesWithPrefix = GetFiles(prefix+path, '')

    files = [(f[len(prefix):]) for f in filesWithPrefix]

  # 3) Search files in DAS dataset
  else:
    dataset = path
    dicfiles = GetDatasetFromDAS(dataset, nFiles, options='file', withRedirector=prefix)
    files = [f[len(prefix):] for f in dicFiles['files']]
    filesWithPrefix = dicFiles['files']

  nEvents, nGenEvents, nSumOfWeights, isData = GetAllInfoFromFile(filesWithPrefix, treeName)

  sampdic['WCnames'] = GetListOfWCs(filesWithPrefix[0])
  sampdic['files']         = files
  sampdic['nEvents']       = nEvents
  sampdic['nGenEvents']    = nGenEvents
  sampdic['nSumOfWeights'] = nSumOfWeights
  sampdic['isData']        = isData

  import json
  if outname == '':
    outname = sample
    if   isinstance(outname, list): outname = outname[0]
    elif ',' in outname:outname = sample.replace(' ', '').split(',')[0]
  if not outname.endswith('.json'): outname += '.json'
  with open(outname, 'w') as outfile:
    json.dump(sampdic, outfile)
    print('>> New json file: %s'%outname)

if __name__ == '__main__':
  main()

'''
  samplefiles = {}
  fileopt = {}
  xsecdic = {}
  sampdic = {}

  if not os.path.isfile(cfgfile) and os.path.isfile(cfgfile+'.cfg'): cfgfile+='.cfg'
  f = open(cfgfile)
  lines = f.readlines()
  for l in lines:
    l = l.replace(' ', '')
    l = l.replace('\n', '')
    if l.startswith('#'): continue
    if '#' in l: l = l.split('#')[0]
    if l == '': continue
    if l.endswith(':'): l = l[:-1]
    if not ':' in l:
      if l in ['path', 'verbose', 'pretend', 'test', 'options', 'xsec', 'year', 'treeName']: continue
      else: samplefiles[l]=l
    else:
      lst = l.split(':')
      key = lst[0]
      val = lst[1] if lst[1] != '' else lst[0]
      if   key == 'pretend'   : pretend   = 1
      elif key == 'verbose'   : verbose   = int(val) if val.isdigit() else 1
      elif key == 'test'      : dotest    = 1
      elif key == 'path'      :
        path      = val
        if len(lst) > 2: 
          for v in lst[2:]: path += ':'+v
      elif key == 'options'   : options   = val
      elif key == 'xsec'      : xsec      = val
      elif key == 'year'      : year      = int(val)
      elif key == 'treeName'  : treeName  = val
      else:
        fileopt[key] = ''#options
        if len(lst) >= 3: fileopt[key] += lst[2]
        samplefiles[key] = val

  # Re-assign arguments...
  aarg = sys.argv
  if '--pretend' in aarg or '-p' in aarg : pretend     = args.pretend
  if '--test'    in aarg or '-t' in aarg : dotest      = args.test
  if args.path       != ''       : path        = args.path
  if args.options    != ''       : options     = args.options
  if args.xsec       != 'xsec'   : xsec        = args.xsec
  if args.year       != -1       : year        = args.year
  if args.treename   != 'Events' : treeName    = args.treename
  if args.verbose    != 0        : verbose     = int(args.verbose)
  xsecdic = loadxsecdic(xsec, verbose)

  for sname in samplefiles.keys():
    sampdic[sname] = {}
    sampdic[sname]['xsec']       = xsecdic[sname] if sname in xsecdic.keys() else 1
    sampdic[sname]['year']       = year
    sampdic[sname]['treeName']   = treeName
    if 'DAS' in options:
      dataset = samplefiles[sname]
      nFiles = int(fileopt[sname]) if fileopt[sname]!='' else None
      #dicFiles = GetDatasetFromDAS(dataset, nFiles, options='file', withRedirector='root://cms-xrd-global.cern.ch/')
      dicFiles = GetDatasetFromDAS(dataset, nFiles, options='file', withRedirector=path)
      nEvents, nGenEvents, nSumOfWeights, isData = GetAllInfoFromFile(dicFiles['files'], sampdic[sname]['treeName'])
      files          = dicFiles['files']
      nEvents        = dicFiles['events']
      fileOptions = ''
    else:
      files = GetFiles(path, samplefiles[sname])
      nEvents, nGenEvents, nSumOfWeights, isData = GetAllInfoFromFile(files, sampdic[sname]['treeName'])
      fileOptions = fileopt[sname]
    sampdic[sname]['options']    = fileOptions
    sampdic[sname]['files']      = files
    sampdic[sname]['nEvents']       = nEvents
    sampdic[sname]['nGenEvents']    = nGenEvents
    sampdic[sname]['nSumOfWeights'] = nSumOfWeights
    sampdic[sname]['isData']        = isData
'''

