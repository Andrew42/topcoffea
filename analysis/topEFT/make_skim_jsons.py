import os
import argparse
import json

from topcoffea.modules.paths import topcoffea_path
from topcoffea.modules.utils import regex_match, load_sample_json_file, update_json, get_files

pjoin = os.path.join

# Attempts to match a hadoop dataset to a json dataset based on the file name
def find_json_match(hadoop_skim_dir,json_fpaths):
    hadoop_dataset_name = os.path.split(hadoop_skim_dir)[1]
    for json_fpath in json_fpaths:
        json_dataset_name = os.path.split(json_fpath)[1].replace(".json","")
        # This is a result of the fact that lobster doesnt allow workflows to contain hyphens in the name
        json_dataset_name = json_dataset_name.replace("-","_")
        if hadoop_dataset_name == json_dataset_name:
            return json_fpath
    return None

def main():
    parser = argparse.ArgumentParser(description='You want options? We got options!')
    parser.add_argument('src_dirs',       nargs='+', metavar='SRC_DIR', help='Path(s) to toplevel directory that contains the lobster skims we want to match to')
    parser.add_argument('--json-dir',     nargs='?', default=topcoffea_path("json"), metavar='DIR', help='Path to the directory with JSON files you want to update. Will recurse down into all sub-directories looking for any .json files along the way')
    parser.add_argument('--ignore-dirs',  nargs='*', default=[], metavar='DIR')
    parser.add_argument('--match-files',  nargs='*', default=[], metavar='FILE')
    parser.add_argument('--ignore-files', nargs='*', default=[], metavar='FILE')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Run the script, but do not actually modify the JSON files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()
    src_dirs     = args.src_dirs
    json_dir     = args.json_dir
    ignore_dirs  = args.ignore_dirs
    match_files  = args.match_files
    ignore_files = args.ignore_files
    dry_run      = args.dry_run
    verbose      = args.verbose

    # These sub-directories have duplicated JSON names with those from private_UL
    ignore_dirs.extend(['subsets_of_private_UL_.*','private_UL_backup'])
    # Make sure to always only find .json files
    match_files.extend(['.*\\.json'])
    # These are not sample json files, so skip them
    ignore_files.extend(['lumi.json','params.json'])
    # These are json files for already produced skims, so skip them as well
    ignore_files.extend([".*_atPSI\\.json",".*_NDSkim\\.json"])
    template_json_fpaths = get_files(json_dir,
        ignore_dirs  = ignore_dirs,
        match_files  = match_files,
        ignore_files = ignore_files,
        recursive = True,
        verbose = verbose
    )
    missing_templates = []
    hadoop_dataset_dirs = []
    for src_dir in src_dirs:
        for d in os.listdir(src_dir):
            dir_fpath = pjoin(src_dir,d)
            if not os.path.isdir(dir_fpath): continue
            hadoop_dataset_dirs.append(dir_fpath)
    hadoop_dataset_dirs = ["/hadoop/store/user/awightma/skims/NanoAOD_ULv8/v1/SingleMuon_C_UL2017"]
    for hdir in hadoop_dataset_dirs:
        dataset = os.path.split(hdir)[1]
        matched_json_fp = find_json_match(hdir,template_json_fpaths)
        print(f"Match: {matched_json_fp}")
        if not matched_json_fp:
            missing_templates.append(hdir)
            continue
        template_json_dir = os.path.split(matched_json_fp)[0]
        updates = {
            "files": [x.replace("/hadoop","") for x in get_files(hdir,match_files=[".*\\.root"])]
        }
        outname = os.path.split(matched_json_fp)[1].replace(".json","_NDSkim.json")
        outname = pjoin(template_json_dir,outname)
        update_json(matched_json_fp,dry_run=dry_run,outname=outname,verbose=verbose,**updates)
        template_json_fpaths.remove(matched_json_fp)
    # These are lobster skims for which we couldn't find a matching json template
    if missing_templates:
        print(f"No matching json template found:")
        for x in missing_templates:
            print(f"\t{x}")
    else:
        print(f"No matching json template found: {missing_templates}")
    # These are json templates for which we couldn't find a lobster skim
    if template_json_fpaths:
        print(f"No matching skim found:")
        for x in template_json_fpaths:
            print(f"\t{x}")
    else:
        print(f"No matching skim found: {template_json_fpaths}")


if __name__ == "__main__":
    main()

