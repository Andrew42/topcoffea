import os
import datetime
import argparse
import matplotlib.pyplot as plt
from cycler import cycler

from coffea import hist
from topcoffea.modules.HistEFT import HistEFT

from topcoffea.modules.YieldTools import YieldTools
from topcoffea.modules.GetValuesFromJsons import get_lumi
from topcoffea.plotter.make_html import make_html

# Some options for plotting the data and MC
DATA_ERR_OPS = {'linestyle':'none', 'marker': '.', 'markersize': 10., 'color':'k', 'elinewidth': 1,}
MC_ERROR_OPS = {'label': 'Stat. Unc.', 'hatch': '////', 'facecolor': 'none', 'edgecolor': (0,0,0,.5), 'linewidth': 0}
FILL_OPS = {}

# The channels that define the CR categories
CR_CHAN_DICT = {
    "cr_2los_Z" : [
        "2los_ee_CRZ_0j",
        "2los_mm_CRZ_0j",
    ],
    "cr_2los_tt" : [
        "2los_em_CRtt_2j",
    ],
    "cr_2lss" : [
        "2lss_ee_CR_1j",
        "2lss_em_CR_1j",
        "2lss_mm_CR_1j",
        "2lss_ee_CR_2j",
        "2lss_em_CR_2j",
        "2lss_mm_CR_2j",
    ],

    "cr_3l" : [
        "3l_eee_CR_1j",
        "3l_eem_CR_1j",
        "3l_emm_CR_1j",
        "3l_mmm_CR_1j",
    ],
}

# The channels that define the CR categories nor the njets hist (where we do not keep track of jets in the sparse axis)
CR_CHAN_DICT_NO_J = {
    "cr_2los_Z" : [
        "2los_ee_CRZ",
        "2los_mm_CRZ",
    ],
    "cr_2los_tt" : [
        "2los_em_CRtt",
    ],
    "cr_2lss" : [
        "2lss_ee_CR",
        "2lss_em_CR",
        "2lss_mm_CR",
    ],
    "cr_3l" : [
        "3l_eee_CR",
        "3l_eem_CR",
        "3l_emm_CR",
        "3l_mmm_CR",
    ],
}

CR_GRP_MAP = {
    "DY" : [],
    "Ttbar" : [],
    "Diboson" : [],
    "Triboson" : [],
    "Single top" : [],
    "Singleboson" : [],
    "data" : [],
}


yt = YieldTools()

# Get a subset of the elements from a list of strings given a whitelist and/or blacklist of substrings
def filter_lst_of_strs(in_lst,substr_whitelist=[],substr_blacklist=[]):

    # Check all elements are strings
    if not (all(isinstance(x,str) for x in in_lst) and all(isinstance(x,str) for x in substr_whitelist) and all(isinstance(x,str) for x in substr_blacklist)):
        raise Exception("Error: This function only filters lists of strings, one of the elements in one of the input lists is not a str.")
    for elem in substr_whitelist:
        if elem in substr_blacklist:
            raise Exception(f"Error: Cannot whitelist and blacklist the same element (\"{elem}\").")

    # Append to the return list
    out_lst = []
    for element in in_lst:
        blacklisted = False
        whitelisted = True
        for substr in substr_blacklist:
            if substr in element:
                # If any of the substrings are in the element, blacklist it
                blacklisted = True
        for substr in substr_whitelist:
            if substr not in element:
                # If any of the substrings are NOT in the element, do not whitelist it
                whitelisted = False
        if whitelisted and not blacklisted:
            out_lst.append(element)

    return out_lst


# Figures out which year a sample is from, retruns the lumi for that year
def get_lumi_for_sample(sample_name):
    if "UL17" in sample_name:
        lumi = 1000.0*get_lumi("2017")
    elif "UL18" in sample_name:
        lumi = 1000.0*get_lumi("2018")
    else:
        raise Exception("Note yet sure how to handle UL16 vas UL16APV, so just crash for now")
    return lumi

# Group bins in a hist, returns a new hist
def group_bins(histo,bin_map):

    # Construct the map of bins to remap
    bins_to_remap_lst = []
    for grp_name,bins_in_grp in bin_map.items():
        bins_to_remap_lst.extend(bins_in_grp)
    for bin_name in yt.get_cat_lables(histo,"sample"):
        if bin_name not in bins_to_remap_lst:
            bin_map[bin_name] = bin_name

    # Remap the bins
    old_ax = histo.axis("sample")
    new_ax = hist.Cat(old_ax.name,old_ax.label)
    new_histo = histo.group(old_ax,new_ax,bin_map)

    return new_histo


# Takes two histograms and makes a plot (with only one sparse axis, whihc should be "sample"), one hist should be mc and one should be data
def make_cr_fig(h_mc,h_data,unit_norm_bool):

    colors = ['#e31a1c','#fb9a99','#a6cee3','#1f78b4','#b2df8a','#33a02c']

    # Create the figure
    fig, (ax, rax) = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(7,7),
        gridspec_kw={"height_ratios": (3, 1)},
        sharex=True
    )
    fig.subplots_adjust(hspace=.07)

    # Set up the colors
    ax.set_prop_cycle(cycler(color=colors))

    # Normalize if we want to dod that
    if unit_norm_bool:
        sum_mc = 0
        sum_data = 0
        for sample in h_mc.values():
            sum_mc = sum_mc + sum(h_mc.values()[sample])
        for sample in h_data.values():
            sum_data = sum_data + sum(h_data.values()[sample])
        h_mc.scale(1.0/sum_mc)
        h_data.scale(1.0/sum_data)

    # Plot the MC
    hist.plot1d(
        h_mc,
        #overlay="sample",
        ax=ax,
        stack=True,
        line_opts=None,
        fill_opts=FILL_OPS,
        error_opts=MC_ERROR_OPS,
        clear=False,
    )

    # Plot the data
    hist.plot1d(
        h_data,
        ax=ax,
        error_opts = DATA_ERR_OPS,
        stack=False,
        clear=False,
    )

    # Make the ratio plot
    hist.plotratio(
        num=h_mc.sum("sample"),
        denom=h_data.sum("sample"),
        ax=rax,
        error_opts=DATA_ERR_OPS,
        denom_fill_opts={},
        guide_opts={},
        unc='num',
        clear=False,
    )

    # Scale the y axis and labels
    ax.autoscale(axis='y')
    ax.set_xlabel(None)
    rax.set_ylabel('Ratio')
    rax.set_ylim(0.5,1.5)

    return fig


# Wrapper function to loop over all CR categories and make plots for all variables
# The input hist should include both the data and MC
def make_all_cr_plots(dict_of_hists,year,unit_norm_bool,save_dir_path):

    # Construct list of MC samples
    mc_wl = []
    mc_bl = ["data"]
    data_wl = ["data"]
    data_bl = []
    if year is None:
        pass # Don't think we actually need to do anything here?
    elif year == "2017":
        mc_wl.append("UL17")
        data_wl.append("UL17")
    elif year == "2018":
        mc_wl.append("UL18")
        data_wl.append("UL18")
    else: raise Exception # Not sure what to do about 2016 vs UL16 yet

    all_samples = yt.get_cat_lables(dict_of_hists,"sample")
    mc_sample_lst = filter_lst_of_strs(all_samples,substr_whitelist=mc_wl,substr_blacklist=mc_bl)
    data_sample_lst = filter_lst_of_strs(all_samples,substr_whitelist=data_wl,substr_blacklist=data_bl)
    print("\nAll samples:",all_samples)
    print("\nMC samples:",mc_sample_lst)
    print("\nData samples:",data_sample_lst)

    # Fill group map (should we just fully hard code this?)
    for proc_name in mc_sample_lst:
        if "data" in proc_name:
            CR_GRP_MAP["Data"].append(proc_name)
        elif "ST" in proc_name or "tW" in proc_name or "tbarW" in proc_name:
            CR_GRP_MAP["Single top"].append(proc_name)
        elif "DY" in proc_name:
            CR_GRP_MAP["DY"].append(proc_name)
        elif "TT" in proc_name:
            CR_GRP_MAP["Ttbar"].append(proc_name)
        elif "WWW" in proc_name or "WWZ" in proc_name or "WZZ" in proc_name or "ZZZ" in proc_name:
            CR_GRP_MAP["Triboson"].append(proc_name)
        elif "WWTo2L2Nu" in proc_name or "ZZTo4L" in proc_name or "WZTo3LNu" in proc_name:
            CR_GRP_MAP["Diboson"].append(proc_name)
        elif "WJets" in proc_name:
            CR_GRP_MAP["Singleboson"].append(proc_name)
        else:
            raise Exception(f"Error: Process name \"{proc_name}\" is not known.")

    # Loop over hists and make plots
    skip_lst = ["SumOfEFTweights"] # Skip this hist
    for idx,var_name in enumerate(dict_of_hists.keys()):
        if (var_name in skip_lst): continue
        if (var_name == "njets"):
            cr_cat_dict = CR_CHAN_DICT_NO_J
        else:  cr_cat_dict= CR_CHAN_DICT
        print("\nVar name:",var_name)

        # Extract the MC and data hists
        hist_mc = dict_of_hists[var_name].remove(data_sample_lst,"sample")
        hist_data = dict_of_hists[var_name].remove(mc_sample_lst,"sample")

        # Normalize the MC hists
        sample_lumi_dict = {}
        for sample_name in mc_sample_lst:
            sample_lumi_dict[sample_name] = get_lumi_for_sample(sample_name)
        hist_mc.scale(sample_lumi_dict,axis="sample")

        # Group the samples by process type
        hist_mc = group_bins(hist_mc,CR_GRP_MAP)

        # Loop over the CR categories
        for hist_cat in cr_cat_dict.keys():
            if (hist_cat == "cr_2los_Z" and "j0" in var_name): continue # The 2los Z category does not require jets
            print("\n\tCategory:",hist_cat)

            # Make a sub dir for this category
            save_dir_path_tmp = os.path.join(save_dir_path,hist_cat)
            if not os.path.exists(save_dir_path_tmp):
                os.mkdir(save_dir_path_tmp)

            # Integrate to get the categories we want
            # NOTE: Once we merge PR #98, integrating the appl axis should not be necessary
            axes_to_integrate_dict = {}
            axes_to_integrate_dict["systematic"] = "nominal"
            axes_to_integrate_dict["channel"] = cr_cat_dict[hist_cat]
            if "2l" in hist_cat:
                axes_to_integrate_dict["appl"] = "isSR_2l"
            elif "3l" in hist_cat:
                axes_to_integrate_dict["appl"] = "isSR_3l"
            else:
                raise Exception
            hist_mc_integrated = yt.integrate_out_cats(hist_mc,axes_to_integrate_dict)
            hist_data_integrated = yt.integrate_out_cats(hist_data,axes_to_integrate_dict)

            # Create and save the figure
            fig = make_cr_fig(hist_mc_integrated,hist_data_integrated,unit_norm_bool)
            title = hist_cat+"_"+var_name
            if unit_norm_bool: title = title + "_unitnorm"
            fig.savefig(os.path.join(save_dir_path_tmp,title))

            # Make an index.html file if saving to web area
            if "www" in save_dir_path_tmp: make_html(save_dir_path_tmp)


def main():

    # Set up the command line parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--pkl-file-path", default="histos/plotsTopEFT.pkl.gz", help = "The path to the pkl file")
    parser.add_argument("-o", "--output-path", default=".", help = "The path the output files should be saved to")
    parser.add_argument("-y", "--year", default=None, help = "The year of the sample")
    parser.add_argument("-u", "--unit-norm", action="store_true", help = "Unit normalize the plots")
    args = parser.parse_args()

    # Whether or not to unit norm the plots
    unit_norm_bool = args.unit_norm

    # Make a tmp output directory in curren dir a different dir is not specified
    timestamp_tag = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    save_dir_path = args.output_path
    outdir_name = "cr_plots_"+timestamp_tag
    save_dir_path = os.path.join(save_dir_path,outdir_name)
    os.mkdir(save_dir_path)

    # Get the histograms
    hin_dict = yt.get_hist_from_pkl(args.pkl_file_path)

    # Print info about histos
    #yt.print_hist_info(args.pkl_file_path,"nbtagsl")
    #exit()

    make_all_cr_plots(hin_dict,args.year,unit_norm_bool,save_dir_path)

if __name__ == "__main__":
    main()
