# This file is essentially a wrapper for createJSON.py:
#   - It runs createJSON.py for each sample that you include in a dictionary, and moves the resulting json file to the directory you specify
#   - If the private NAOD has to be remade, the version numbers should be updated in the dictionaries here, then just rerun the script to remake the jsons

import subprocess
import os
from topcoffea.modules.paths import topcoffea_path


########### Private UL signal samples ###########

private_UL17_dict = {

    "UL17_ttHJet_b1"   : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch1/naodOnly_step/v2/nAOD_step_ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttHJet_privateUL17",
        "xsecName": "ttHnobb",
    },
    "UL17_ttHJet_b2"   : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch2/naodOnly_step/v2/nAOD_step_ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttHJet_privateUL17",
        "xsecName": "ttHnobb",
    },
    "UL17_ttHJet_b3"   : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch3/naodOnly_step/v3/nAOD_step_ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttHJet_privateUL17",
        "xsecName": "ttHnobb",
    },

    "UL17_ttlnuJet_b1" : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch1/naodOnly_step/v2/nAOD_step_ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttlnuJet_privateUL17",
        "xsecName": "TTWJetsToLNu",
    },
    "UL17_ttlnuJet_b2" : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch2/naodOnly_step/v2/nAOD_step_ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttlnuJet_privateUL17",
        "xsecName": "TTWJetsToLNu",
    },
    "UL17_ttlnuJet_b3" : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch3/naodOnly_step/v3/nAOD_step_ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttlnuJet_privateUL17",
        "xsecName": "TTWJetsToLNu",
    },

    "UL17_ttllJet_b1"  : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch1/naodOnly_step/v2/nAOD_step_ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttllJet_privateUL17",
        "xsecName": "TTZToLLNuNu_M_10",
    },
    "UL17_ttllJet_b2"  : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch2/naodOnly_step/v2/nAOD_step_ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttllJet_privateUL17",
        "xsecName": "TTZToLLNuNu_M_10",
    },
    "UL17_ttllJet_b3"  : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch3/naodOnly_step/v3/nAOD_step_ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttllJet_privateUL17",
        "xsecName": "TTZToLLNuNu_M_10",
    },

    "UL17_tllq_b1"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch1/naodOnly_step/v2/nAOD_step_tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0",
        "histAxisName" : "tllq_privateUL17",
        "xsecName": "tZq",
    },
    "UL17_tllq_b2"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch2/naodOnly_step/v2/nAOD_step_tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0",
        "histAxisName": "tllq_privateUL17",
        "xsecName": "tZq",
    },
    "UL17_tllq_b3"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch3/naodOnly_step/v3/nAOD_step_tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0",
        "histAxisName": "tllq_privateUL17",
        "xsecName": "tZq",
    },

    "UL17_tHq_b1"      : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch1/naodOnly_step/v2/nAOD_step_tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "tHq_privateUL17",
        "xsecName": "tHq",
    },
    "UL17_tHq_b2"      : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch2/naodOnly_step/v2/nAOD_step_tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "tHq_privateUL17",
        "xsecName": "tHq",
    },
    "UL17_tHq_b3"      : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch3/naodOnly_step/v3/nAOD_step_tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "tHq_privateUL17",
        "xsecName": "tHq",
    },

    "UL17_tttt_b4"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL17/Round1/Batch4/naodOnly_step/v1/nAOD_step_tttt_FourtopsMay3v1_run0",
        "histAxisName": "tttt_privateUL17",
        "xsecName": "tttt",
    },
}

private_UL18_dict = {

    "UL18_ttHJet_b1"   : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch1/naodOnly_step/v4/nAOD_step_ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttHJet_privateUL18",
        "xsecName": "ttHnobb",
    },
    "UL18_ttHJet_b2"   : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch2/naodOnly_step/v1/nAOD_step_ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttHJet_privateUL18",
        "xsecName": "ttHnobb",
    },
    "UL18_ttHJet_b3"   : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch3/naodOnly_step/v1/nAOD_step_ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttHJet_privateUL18",
        "xsecName": "ttHnobb",
    },

    "UL18_ttlnuJet_b1" : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch1/naodOnly_step/v4/nAOD_step_ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttlnuJet_privateUL18",
        "xsecName": "TTWJetsToLNu",
    },
    "UL18_ttlnuJet_b2" : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch2/naodOnly_step/v1/nAOD_step_ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttlnuJet_privateUL18",
        "xsecName": "TTWJetsToLNu",
    },
    "UL18_ttlnuJet_b3" : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch3/naodOnly_step/v1/nAOD_step_ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttlnuJet_privateUL18",
        "xsecName": "TTWJetsToLNu",
    },

    "UL18_ttllJet_b1"  : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch1/naodOnly_step/v4/nAOD_step_ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttllJet_privateUL18",
        "xsecName": "TTZToLLNuNu_M_10",
    },
    "UL18_ttllJet_b2"  : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch2/naodOnly_step/v1/nAOD_step_ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttllJet_privateUL18",
        "xsecName": "TTZToLLNuNu_M_10",
    },
    "UL18_ttllJet_b3"  : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch3/naodOnly_step/v1/nAOD_step_ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttllJet_privateUL18",
        "xsecName": "TTZToLLNuNu_M_10",
    },

    "UL18_tllq_b1"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch1/naodOnly_step/v4/nAOD_step_tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0",
        "histAxisName": "tllq_privateUL18",
        "xsecName": "tZq",
    },
    "UL18_tllq_b2"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch2/naodOnly_step/v1/nAOD_step_tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0",
        "histAxisName": "tllq_privateUL18",
        "xsecName": "tZq",
    },
    "UL18_tllq_b3"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch3/naodOnly_step/v1/nAOD_step_tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0",
        "histAxisName": "tllq_privateUL18",
        "xsecName": "tZq",
    },

    "UL18_tHq_b1"      : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch1/naodOnly_step/v4/nAOD_step_tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "tHq_privateUL18",
        "xsecName": "tHq",
    },
    "UL18_tHq_b2"      : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch2/naodOnly_step/v1/nAOD_step_tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "tHq_privateUL18",
        "xsecName": "tHq",
    },
    "UL18_tHq_b3"      : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch3/naodOnly_step/v1/nAOD_step_tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "tHq_privateUL18",
        "xsecName": "tHq",
    },

    "UL18_tttt_b4"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL18/Round1/Batch4/naodOnly_step/v1/nAOD_step_tttt_FourtopsMay3v1_run0",
        "histAxisName": "tttt_privateUL18",
        "xsecName": "tttt",
    },
}

private_UL16_dict = {

    "UL16_ttHJet_b1"   : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16/Round1/Batch1/naodOnly_step/v1/nAOD_step_ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttHJet_privateUL16",
        "xsecName": "ttHnobb",
    },
    "UL16_ttlnuJet_b1" : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16/Round1/Batch1/naodOnly_step/v1/nAOD_step_ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttlnuJet_privateUL16",
        "xsecName": "TTWJetsToLNu",
    },
    "UL16_ttllJet_b1"  : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16/Round1/Batch1/naodOnly_step/v1/nAOD_step_ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttllJet_privateUL16",
        "xsecName": "TTZToLLNuNu_M_10",
    },
    "UL16_tllq_b1"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16/Round1/Batch1/naodOnly_step/v1/nAOD_step_tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0",
        "histAxisName": "tllq_privateUL16",
        "xsecName": "tZq",
    },
    "UL16_tHq_b1"      : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16/Round1/Batch1/naodOnly_step/v1/nAOD_step_tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "tHq_privateUL16",
        "xsecName": "tHq",
    },
    "UL16_tttt_b1"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16/Round1/Batch1/naodOnly_step/v1/nAOD_step_tttt_FourtopsMay3v1_run0",
        "histAxisName": "tttt_privateUL16",
        "xsecName": "tttt",
    },
}

private_UL16APV_dict = {

    "UL16APV_ttHJet_b1"   : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16APV/Round1/Batch1/naodOnly_step/v1/nAOD_step_ttHJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttHJet_privateUL16APV",
        "xsecName": "ttHnobb",
    },
    "UL16APV_ttlnuJet_b1" : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16APV/Round1/Batch1/naodOnly_step/v1/nAOD_step_ttlnuJet_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttlnuJet_privateUL16APV",
        "xsecName": "TTWJetsToLNu",
    },
    "UL16APV_ttllJet_b1"  : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16APV/Round1/Batch1/naodOnly_step/v1/nAOD_step_ttllNuNuJetNoHiggs_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "ttllJet_privateUL16APV",
        "xsecName": "TTZToLLNuNu_M_10",
    },
    "UL16APV_tllq_b1"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16APV/Round1/Batch1/naodOnly_step/v1/nAOD_step_tllq4fNoSchanWNoHiggs0p_all22WCsStartPtCheckV2dim6TopMay20GST_run0",
        "histAxisName": "tllq_privateUL16APV",
        "xsecName": "tZq",
    },
    "UL16APV_tHq_b1"      : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16APV/Round1/Batch1/naodOnly_step/v1/nAOD_step_tHq4f_all22WCsStartPtCheckdim6TopMay20GST_run0",
        "histAxisName": "tHq_privateUL16APV",
        "xsecName": "tHq",
    },
    "UL16APV_tttt_b1"     : {
        "path" : "/store/user/kmohrman/FullProduction/FullR2/UL16APV/Round1/Batch1/naodOnly_step/v1/nAOD_step_tttt_FourtopsMay3v1_run0",
        "histAxisName": "tttt_privateUL16APV",
        "xsecName": "tttt",
    },
}


########### TOP-19-001 samples (locally at ND on /scratch365) ###########

private_2017_dict = {
    "2017_ttHJet" : {
        "path" : "/scratch365/kmohrman/mc_files/TOP-19-001/ttH/",
        "histAxisName": "ttH_private2017",
        "xsecName": "ttHnobb",
    },
    "2017_ttlnuJet" : {
        "path" : "/scratch365/kmohrman/mc_files/TOP-19-001/ttlnu/",
        "histAxisName": "ttlnu_private2017",
        "xsecName": "TTWJetsToLNu",
    },
    "2017_ttllJet" : {
        "path" : "/scratch365/kmohrman/mc_files/TOP-19-001/ttll/",
        "histAxisName": "ttll_private2017",
        "xsecName": "TTZToLLNuNu_M_10",
    },
    "2017_tllqJet" : {
        "path" : "/scratch365/kmohrman/mc_files/TOP-19-001/tllq/",
        "histAxisName": "tllq_private2017",
        "xsecName": "tZq",
    },
    "2017_tHqJet" : {
        "path" : "/scratch365/kmohrman/mc_files/TOP-19-001/tHq/",
        "histAxisName": "tHq_private2017",
        "xsecName": "tHq",
    },
}



########### Central signal samples ###########

sync_dict = {
    "ttHJetToNonbb_sync" : {
        "path" : "/store/mc/RunIIFall17NanoAODv7/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/NANOAODSIM/PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/110000/BB506088-A858-A24D-B27C-0D31058D3125.root",
        "histAxisName": "ttHJetToNonbb_sync",
        "xsecName": "ttHnobb",
    },
}

central_2017_correctnPartonsInBorn_dict = {
    "2017_TTZToLLNuNu_M_10_correctnPartonsInBorn" : {
        "path" : "/TTZToLLNuNu_M-10_TuneCP5_PSweights_correctnPartonsInBorn_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "ttZ_central2017_correctnPartonsInBorn",
        "xsecName" : "tZq",
    }
}

central_2017_dict = {
    "2017_ttHnobb" : {
        "path" : "/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "ttH_central2017",
        "xsecName": "ttHnobb",
    },
    "2017_TTWJetsToLNu" : {
        "path" : "/TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "ttW_central2017",
        "xsecName": "TTWJetsToLNu",
    },
    "2017_TTZToLLNuNu_M_10" : {
        "path" : "/TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "ttZ_central2017",
        "xsecName": "TTZToLLNuNu_M_10",
    },
    "2017_tZq" : {
        "path" : "/tZq_ll_4f_ckm_NLO_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM",
        "histAxisName": "tZq_central2017",
        "xsecName": "tZq",
    },
    "2017_THQ" : {
        "path" : "/THQ_ctcvcp_4f_Hincl_13TeV_madgraph_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "tHq_central2017",
        "xsecName": "tHq",
    },
    "2017_TTTT" : {
        "path" : "/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "tttt_central2017",
        "xsecName": "tttt",
    },
}

central_UL17_dict = {
    "UL17_ttHnobb" : {
        "path" : "/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "ttH_centralUL17",
        "xsecName": "ttHnobb",
    },
    "UL17_TTWJetsToLNu" : {
        "path" : "/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "ttW_centralUL17",
        "xsecName": "TTWJetsToLNu",
    },
    "UL17_TTZToLLNuNu_M_10" : {
        "path" : "/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "ttZ_centralUL17",
        "xsecName": "TTZToLLNuNu_M_10",
    },
    "UL17_tZq" : {
        "path" : "/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "tZq_centralUL17",
        "xsecName": "tZq",
    },
}

central_UL17_bkg_dict = {
    "UL17_DY10to50" : {
        "path" : "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "DYJetsToLL_centralUL17",
        "xsecName": "DYJetsToLL_M_10to50_MLM",
    },

    "UL17_DY50" : {
        "path" : "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "DYJetsToLL_centralUL17",
        "xsecName": "DYJetsToLL_M_50_MLM",
    },

    "UL17_singleTop" : {
        "path" : "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "singleTop_centralUL17",
        "xsecName": "ST",
    },

    "UL17_t" : {
        "path" : "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "t_centralUL17",
        "xsecName": "t",
    },

    "UL17_tbar" : {
        "path" : "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "tbar_centralUL17",
        "xsecName": "tbar",
    },

    "UL17_tbarW" : {
        "path" : "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "tbarW_noFullHad_centralUL17",
        "xsecName": "tbarW_noFullHad",
    },

    "UL17_tW" : {
        "path" : "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "tW_noFullHad_centralUL17",
        "xsecName": "tW_noFullHad",
    },

    "UL17_TTGJets" : {
        "path" : "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "TTGJets_centralUL17",
        "xsecName": "TTGJets",
    },

    "UL17_TTJets" : {
        "path" : "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "TTJets_centralUL17",
        "xsecName": "TT",
    },

    "UL17_TTWJetsToLNu" : {
        "path" : "/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "TTWJetsToLNu_centralUL17",
        "xsecName": "TTWJetsToLNu",
    },

    "UL17_TTZToLLNuNu" : {
        "path" : "/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "TTZToLLNuNu_centralUL17",
        "xsecName": "TTZToLLNuNu_M_10",
    },

    "UL17_WJetsToLNu" : {
        "path" : "/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "WJetsToLNu_centralUL17",
        "xsecName": "WJetsToLNu",
    },

    "UL17_WWTo2L2Nu" : {
        "path" : "/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "WWTo2L2Nu_centralUL17",
        "xsecName": "WWTo2L2Nu",
    },

    "UL17_WWW_4F" : {
        "path" : "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "WWW_centralUL17",
        "xsecName": "WWW",
    },

    "UL17_WWW_4F_ext" : {
        "path" : "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8_ext1-v1/NANOAODSIM",
        "histAxisName": "WWW_centralUL17",
        "xsecName": "WWW",
    },

    "UL17_WWZ_4F" : {
        "path" : "/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "WWZ_centralUL17",
        "xsecName": "WWZ",
    },

    "UL17_WZTo3LNu" : {
        "path" : "/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "WZTo3LNu_centralUL17",
        "xsecName": "WZTo3LNu",
    },

    "UL17_WZZ" : {
        "path" : "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "WZZ_centralUL17",
        "xsecName": "WZZ",
    },

    "UL17_WZZ_ext" : {
        "path" : "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8_ext1-v1/NANOAODSIM",
        "histAxisName": "WZZ_centralUL17",
        "xsecName": "WZZ",
    },

    "UL17_ZZ" : {
        "path" : "/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "ZZTo4L_centralUL17",
        "xsecName": "ZZTo4L",
    },

    "UL17_ZZZ" : {
        "path" : "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM",
        "histAxisName": "ZZZ_centralUL17",
        "xsecName": "ZZZ",
    },

    "UL17_ZZZ" : {
        "path" : "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv2-106X_mc2017_realistic_v8_ext1-v1/NANOAODSIM",
        "histAxisName": "ZZZ_centralUL17",
        "xsecName": "ZZZ",
    },
}

central_UL18_dict = {
    "UL18_ttHnobb" : {
        "path" : "/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "ttH_centralUL18",
        "xsecName": "ttHnobb",
    },
    "UL18_TTWJetsToLNu" : {
        "path" : "/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "ttW_centralUL18",
        "xsecName": "TTWJetsToLNu",
    },
    "UL18_TTZToLLNuNu_M_10" : {
        "path" : "/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "ttZ_centralUL18",
        "xsecName": "TTZToLLNuNu_M_10",
    },
    "UL18_tZq" : {
        "path" : "/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "tZq_centralUL18",
        "xsecName": "tZq",
    },
}

central_UL18_bkg_dict = {
    "UL18_DY10to50" : {
        "path" : "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "DY10to50_centralUL18",
        "xsecName": "DY10to50",
    },
    "UL18_DY50" : {
        "path" : "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "DY50_centralUL18",
        "xsecName": "DY50",
    },
    "UL18_singleTop" : {
        "path" : "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "singleTop_centralUL18",
        "xsecName": "singleTop",
    },
    "UL18_t" : {
        "path" : "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "t_centralUL18",
        "xsecName": "t",
    },
    "UL18_tbar" : {
        "path" : "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "tbar_centralUL18",
        "xsecName": "tbar",
    },
    "UL18_tbarW" : {
        "path" : "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "tbarW_centralUL18",
        "xsecName": "tbarW",
    },
    "UL18_tW" : {
        "path" : "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "tW_centralUL18",
        "xsecName": "tW",
    },
    "UL18_TTGJets" : {
        "path" : "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "TTGJets_centralUL18",
        "xsecName": "TTGJets",
    },
    "UL18_TTJets" : {
        "path" : "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "TTJets_centralUL18",
        "xsecName": "TTJets",
    },
    "UL18_TTWJetsToLNu" : {
        "path" : "/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "TTWJetsToLNu_centralUL18",
        "xsecName": "TTWJetsToLNu",
    },
    "UL18_TTZToLLNuNu" : {
        "path" : "/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "TTZToLLNuNu_centralUL18",
        "xsecName": "TTZToLLNuNu",
    },
    "UL18_WJetsToLNu" : {
        "path" : "/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "WJetsToLNu_centralUL18",
        "xsecName": "WJetsToLNu",
    },
    "UL18_WWTo2L2Nu" : {
        "path" : "/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "WWTo2L2Nu_centralUL18",
        "xsecName": "WWTo2L2Nu",
    },
    "UL18_WWW_4F" : {
        "path" : "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "WWW_4F_centralUL18",
        "xsecName": "WWW",
    },
    "UL18_WWZ_4F" : {
        "path" : "/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "WWZ_4F_centralUL18",
        "xsecName": "WWZ",
    },
    "UL18_WZTo3Lnu" : {
        "path" : "/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "WZTo3Lnu_centralUL18",
        "xsecName": "WZTo3Lnu",
    },
    "UL18_WZZ" : {
        "path" : "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "WZZ_centralUL18",
        "xsecName": "WZZ",
    },
    "UL18_WZZ_ext" : {
        "path" : "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM",
        "histAxisName": "WZZ_ext_centralUL18",
        "xsecName": "WZZ_ext",
    },
    "UL18_ZZ" : {
        "path" : "/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM",
        "histAxisName": "ZZ_centralUL18",
        "xsecName": "ZZ",
    },
    "UL18_ZZZ" : {
        "path" : "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
        "histAxisName": "ZZZ_centralUL18",
        "xsecName": "ZZZ",
    },
}

central_UL16_bkg_dict = {
    "UL16_DY10to50" : {
        "path" : "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM",
        "histAxisName": "DY10to50_centralUL16",
        "xsecName": "DY10to50",
    },
    "UL16_DY50" : {
        "path" : "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM",
        "histAxisName": "DY50_centralUL16",
        "xsecName": "DY50",
    },
    "UL16_ST" : {
        "path" : "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM",
        "histAxisName": "ST_centralUL16",
        "xsecName": "ST",
    },
    "UL16_ST_tW_antitop_5f_inclusiveDecays" : {
        "path" : "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM",
        "histAxisName": "ST_tW_antitop_5f_inclusiveDecays_centralUL16",
        "xsecName": "ST_tW_antitop_5f_inclusiveDecays",
    },
    "UL16_ST_tW_top_5f_inclusiveDecays" : {
        "path" : "/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM",
        "histAxisName": "ST_tW_top_5f_inclusiveDecays_centralUL16",
        "xsecName": "ST_tW_top_5f_inclusiveDecays",
    },
    "UL16_TTGJets" : {
        "path" : "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
        "histAxisName": "TTGJets_centralUL16",
        "xsecName": "TTGJets",
    },
    "UL16_TTJets" : {
        "path" : "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM",
        "histAxisName": "TTJets_centralUL16",
        "xsecName": "TTJets",
    },
    "UL16_WJetsToLNu" : {
        "path" : "/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
        "histAxisName": "WJetsToLNu_centralUL16",
        "xsecName": "WJetsToLNu",
    },
    "UL16_WWW_4F" : {
        "path" : "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
        "histAxisName": "WWW_4F_centralUL16",
        "xsecName": "WWW",
    },
    "UL16_WWW_4F_ext" : {
        "path" : "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17_ext1-v1/NANOAODSIM",
        "histAxisName": "WWW_4F_centralUL16",
        "xsecName": "WWW",
    },
    "UL16_WWZ_4F" : {
        "path" : "/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
        "histAxisName": "WWZ_4F_centralUL16",
        "xsecName": "WWZ",
    },
    "UL16_WWZ_ext" : {
        "path" : "/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17_ext1-v1/NANOAODSIM",
        "histAxisName": "WWZ_4F_centralUL16",
        "xsecName": "WWZ",
    },
    "UL16_WZTo3LNu" : {
        "path" : "/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
        "histAxisName": "WZTo3LNu_centralUL16",
        "xsecName": "WZTo3LNu",
    },
    "UL16_WZZ" : {
        "path" : "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
        "histAxisName": "WZZ_centralUL16",
        "xsecName": "WZZ",
    },
    "UL16_WZZ_ext" : {
        "path" : "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17_ext1-v1/NANOAODSIM",
        "histAxisName": "WZZ_centralUL16",
        "xsecName": "WZZ",
    },
    "UL16_ZZZ" : {
        "path" : "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
        "histAxisName": "ZZZ_centralUL16",
        "xsecName": "ZZZ",
    },
    "UL16_ZZZ_ext" : {
        "path" : "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17_ext1-v1/NANOAODSIM",
        "histAxisName": "ZZZ_centralUL16",
        "xsecName": "ZZZ",
    },
    "UL16_ttHJetToNonbb_M125" : {
        "path" : "/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM",
        "histAxisName": "ttHJetToNonbb_M125_centralUL16",
        "xsecName": "ttHJetToNonbb_M125",
    },
}

central_UL16APV_bkg_dict = {
    "UL16_DY10to50_APV" : {
        "path" : "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv2-106X_mcRun2_asymptotic_preVFP_v9-v1/NANOAODSIM",
        "histAxisName": "DY10to50_APV_centralUL16",
        "xsecName": "DY10to50_APV",
    },
    "UL16_DY50_APV" : {
        "path" : "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
        "histAxisName": "DY50_APV_centralUL16",
        "xsecName": "DY50_APV",
    },
    "UL16_ST_APV" : {
        "path" : "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
        "histAxisName": "ST_APV_centralUL16",
        "xsecName": "ST_APV",
    },
    "UL16_ST_tW_antitop_5f_inclusiveDecays_APV" : {
        "path" : "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
        "histAxisName": "ST_tW_antitop_5f_inclusiveDecays_APV_centralUL16",
        "xsecName": "ST_tW_antitop_5f_inclusiveDecays_APV",
    },
    "UL16_ST_tW_top_5f_inclusiveDecays_APV" : {
        "path" : "/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
        "histAxisName": "ST_tW_top_5f_inclusiveDecays_APV_centralUL16",
        "xsecName": "ST_tW_top_5f_inclusiveDecays_APV",
    },
    "UL16_TTJets_APV" : {
        "path" : "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv2-106X_mcRun2_asymptotic_preVFP_v9-v1/NANOAODSIM",
        "histAxisName": "TTJets_APV_centralUL16",
        "xsecName": "TTJets_APV",
    },
    "UL16_WJetsToLNu_APV" : {
        "path" : "/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer19UL16NanoAODAPVv2-106X_mcRun2_asymptotic_preVFP_v9-v1/NANOAODSIM",
        "histAxisName": "WJetsToLNu_APV_centralUL16",
        "xsecName": "WJetsToLNu_APV",
    },
    "UL16_WWW_4F_APV" : {
        "path" : "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
        "histAxisName": "WWW_APV_centralUL16",
        "xsecName": "WWW",
    },
    "UL16_WWW_APV_ext" : {
        "path" : "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11_ext1-v1/NANOAODSIM",
        "histAxisName": "WWW_APV_centralUL16",
        "xsecName": "WWW",
    },
    "UL16_WZZ_APV" : {
        "path" : "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
        "histAxisName": "WZZ_APV_centralUL16",
        "xsecName": "WZZ_APV",
    },
    "UL16_WZZ_APV_ext" : {
        "path" : "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11_ext1-v1/NANOAODSIM",
        "histAxisName": "WZZ_APV_centralUL16",
        "xsecName": "WZZ_APV",
    },
    "UL16_ZZZ_APV" : {
        "path" : "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",
        "histAxisName": "ZZZ_APV_centralUL16",
        "xsecName": "ZZZ_APV",
    },
    "UL16_ZZZ_APV_ext" : {
        "path" : "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11_ext1-v1/NANOAODSIM",
        "histAxisName": "ZZZ_APV_centralUL16",
        "xsecName": "ZZZ_APV",
    },
    "UL16_ttHJetToNonbb_M125_APV" : {
        "path" : "/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer20UL16NanoAODAPVv2-106X_mcRun2_asymptotic_preVFP_v9-v1/NANOAODSIM",
        "histAxisName": "ttHJetToNonbb_M125_APV_centralUL16",
        "xsecName": "ttHJetToNonbb_M125_APV",
    },
}

########### TESTING ########### 

test_dict = {
    "test_dy_sample" : {
        "path" : "/store/user/jrgonzal/nanoAODcrab/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/mc2017_28apr2021_DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/210427_231758/0000/",
        "histAxisName": "central_DY",
        "xsecName" : "DYJetsToLL_M_50_MLM", # Not sure if this is actually the right xsec, I just picked one of the DY ones
    }
}

########### Functions for makign the jsons ###########

# Wrapper for createJSON.py
def make_json(sample_dir,sample_name,prefix,sample_yr,xsec_name,hist_axis_name,on_das=False):

    # If the sample is on DAS, inclue the DAS flag in the createJSON.py arguments
    das_flag = ""
    if on_das: das_flag = "--DAS"

    # Run createJSON.py
    subprocess.run([
        "python",
        "../../topcoffea/modules/createJSON.py",
        sample_dir,
        das_flag,
        "--sampleName"   , sample_name,
        "--prefix"       , prefix,
        "--xsec"         , "../../topcoffea/cfg/xsec.cfg",
        "--xsecName"     , xsec_name,
        "--year"         , sample_yr,
        "--histAxisName" , hist_axis_name,
    ])


# Convenience function for running make_json() on all entries in a dictionary of samples, and moving the results to out_dir
def make_jsons_for_dict_of_samples(samples_dict,prefix,year,out_dir,on_das=False):
    for sample_name,sample_info in samples_dict.items():
        path = sample_info["path"]
        hist_axis_name = sample_info["histAxisName"]
        xsec_name = sample_info["xsecName"]
        make_json(
            sample_dir = path,
            sample_name = sample_name,
            prefix = prefix,
            sample_yr = year,
            xsec_name = xsec_name,
            hist_axis_name = hist_axis_name,
            on_das = on_das,
        )
        out_name = sample_name+".json"
        subprocess.run(["mv",out_name,out_dir]) 
        print("sample name:",sample_name)
        print("\tpath:",path,"\n\thistAxisName:",hist_axis_name,"\n\txsecName",xsec_name,"\n\tout name:",out_name,"\n\tout dir:",out_dir)


# Uncomment the make_jsons_for_dict_of_samples() lines for the jsons you want to make/remake
def main():

    # Specify some output dirs
    out_dir_private_UL     = os.path.join(topcoffea_path("json"),"signal_samples/private_UL/")
    out_dir_top19001_local = os.path.join(topcoffea_path("json"),"signal_samples/private_top19001_local")
    out_dir_central_UL     = os.path.join(topcoffea_path("json"),"signal_samples/central_UL/")
    out_dir_central_bkg_UL     = os.path.join(topcoffea_path("json"),"background_samples/central_UL/")
    out_dir_central_2017   = os.path.join(topcoffea_path("json"),"signal_samples/central_2017/")

    # Private UL
    #make_jsons_for_dict_of_samples(private_UL17_dict,"/hadoop","2017",out_dir_private_UL)
    #make_jsons_for_dict_of_samples(private_UL18_dict,"/hadoop","2018",out_dir_private_UL)
    #make_jsons_for_dict_of_samples(private_UL16_dict,"/hadoop","2016",out_dir_private_UL)
    #make_jsons_for_dict_of_samples(private_UL16APV_dict,"/hadoop","2016APV",out_dir_private_UL) # Not sure what we need here for the year, can remake the JSONs later to update when we have SFs etc set up for 2016 stuff (right now I think it's mostly just 18)

    # TOP-19-001 ttll
    #make_jsons_for_dict_of_samples(private_2017_dict,"","2017",out_dir_top19001_local)

    # Central
    #make_jsons_for_dict_of_samples(central_2016_dict,"root://ndcms.crc.nd.edu/","2016",out_dir_central_2016,on_das=True)
    #make_jsons_for_dict_of_samples(central_UL16_dict,"root://ndcms.crc.nd.edu/","2016",out_dir_central_UL,on_das=True)
    make_jsons_for_dict_of_samples(central_UL16_bkg_dict,"root://ndcms.crc.nd.edu/","2016",out_dir_central_bkg_UL,on_das=True)
    #make_jsons_for_dict_of_samples(central_2016APV_dict,"root://ndcms.crc.nd.edu/","2016APV",out_dir_central_2016APV,on_das=True)
    #make_jsons_for_dict_of_samples(central_UL16APV_dict,"root://ndcms.crc.nd.edu/","2016APV",out_dir_central_UL,on_das=True)
    make_jsons_for_dict_of_samples(central_UL16APV_bkg_dict,"root://ndcms.crc.nd.edu/","2016APV",out_dir_central_bkg_UL,on_das=True)
    #make_jsons_for_dict_of_samples(central_2017_correctnPartonsInBorn_dict,"root://ndcms.crc.nd.edu/","2017",out_dir_central_2017,on_das=True)
    #make_jsons_for_dict_of_samples(central_2017_dict,"root://ndcms.crc.nd.edu/","2017",out_dir_central_2017,on_das=True)
    #make_jsons_for_dict_of_samples(central_UL17_dict,"root://ndcms.crc.nd.edu/","2017",out_dir_central_UL,on_das=True)
    make_jsons_for_dict_of_samples(central_UL17_bkg_dict,"root://ndcms.crc.nd.edu/","2017",out_dir_central_bkg_UL,on_das=True)
    #make_jsons_for_dict_of_samples(central_UL18_dict,"root://ndcms.crc.nd.edu/","2018",out_dir_central_UL,on_das=True)
    make_jsons_for_dict_of_samples(central_UL18_bkg_dict,"root://ndcms.crc.nd.edu/","2018",out_dir_central_bkg_UL,on_das=True)

    # Testing finding list of files with xrdfs ls
    #make_jsons_for_dict_of_samples(test_dict,"root://xrootd-local.unl.edu/","2017",".")


main()
