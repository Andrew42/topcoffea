import argparse

from topcoffea.modules.datacard_tools import *
from topcoffea.modules.utils import regex_match

def main():
    parser = argparse.ArgumentParser(description="You can select which file to run over")
    parser.add_argument("pkl_file",nargs="?",help="Pickle file with histograms to run over")
    parser.add_argument("--lumi-json","-l",default="json/lumi.json",help="Lumi json file, path relative to topcoffea_path()")
    parser.add_argument("--rate-syst-json","-s",default="json/rate_systs.json",help="Rate related systematics json file, path relative to topcoffea_path()")
    parser.add_argument("--miss-parton-file","-m",default="data/missing_parton/missing_parton.root",help="File for missing parton systematic, path relative to topcoffea_path()")
    parser.add_argument("--out-dir","-d",default=".",help="Output directory to write root and text datacard files to")
    parser.add_argument("--var-lst",default=[],action="extend",nargs="+",help="Specify a list of variables to make cards for.")
    parser.add_argument("--ch-lst","-c",default=[],action="extend",nargs="+",help="Specify a list of channels to process.")
    parser.add_argument("--POI",default=[],help="List of WCs (comma separated)")
    parser.add_argument("--year","-y",default="",help="Run over single year")
    parser.add_argument("--do-nuisance",action="store_true",help="Include nuisance parameters")
    parser.add_argument("--unblind",action="store_true",help="If set, use real data, otherwise use asimov data")
    parser.add_argument("--verbose","-v",action="store_true",help="Set to verbose output")

    args = parser.parse_args()
    pkl_file  = args.pkl_file
    lumi_json = args.lumi_json
    rs_json   = args.rate_syst_json
    mp_file   = args.miss_parton_file
    out_dir   = args.out_dir
    # year      = args.year     # NOT IMPLEMENTED YET
    var_lst   = args.var_lst
    ch_lst    = args.ch_lst
    wcs       = args.POI
    do_nuis   = args.do_nuisance
    unblind   = args.unblind
    verbose   = args.verbose

    if isinstance(wcs,str):
        wcs = wcs.split(",")

    kwargs = {
        "wcs": wcs,
        "lumi_json_path": lumi_json,
        "rate_syst_path": rs_json,
        "missing_parton_path": mp_file,
        "out_dir": out_dir,
        "var_lst": var_lst,
        "do_nuisance": do_nuis,
        "unblind": unblind,
        "verbose": verbose,
    }

    tic = time.time()
    dc = DatacardMaker(pkl_file,**kwargs)

    dists = var_lst if len(var_lst) else dc.hists.keys()
    for km_dist in dists:
        selected_wcs = dc.get_selected_wcs(km_dist)
        all_chs = dc.channels(km_dist)
        matched_chs = regex_match(all_chs,ch_lst)
        if ch_lst:
            print(f"Channels to process: {matched_chs}")
        for ch in matched_chs:
            r = dc.analyze(km_dist,ch,selected_wcs)
    dt = time.time() - tic
    print(f"Total Time: {dt:.2f} s")
    print("Finished!")

main()
