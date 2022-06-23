'''
Reader beware: this script is ugly, but it gets the job done!
It loads flat JEC files and parses them into a dictionary as:
{JEC name:
    {(eta_low, eta_high):
       {pT: correction_low, correction_high} # note the correctiosn are symmetric so I'm assuming low is first
    }
}.
The script then uses `jes_to_combine` to find all corrections which it should add in quadrature.
Finanlly, it creates a new set of files (with `Quad` in the name instead of `RegroupedV2`) 
and writes out the new corrections.


import numpy as np
from topcoffea.modules.paths import topcoffea_path

files = ['data/JEC/RegroupedV2_Summer19UL16APV_V7_MC_UncertaintySources_AK4PFchs.junc.txt', 'data/JEC/RegroupedV2_Summer19UL16_V7_MC_UncertaintySources_AK4PFchs.junc.txt', 'data/JEC/RegroupedV2_Summer19UL17_V5_MC_UncertaintySources_AK4PFchs.junc.txt', 'data/JEC/RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.junc.txt']
header='{1 JetEta 1 JetPt "" Correction JECSource}\n'
for file in files:
    with open(topcoffea_path(file), 'r') as f:
        fin = f.readlines()
    jecs = {}
    jes_to_combine = ['FlavorQCD', 'BBEC1', 'Absolute', 'RelativeBal', 'RelativeSample']
    for line in fin:
        line = line.strip()
        if line[0] == '[':
            jec = line[1:-1]
            continue
        if line[0] == '{': continue
        else:
            line = line.split(' ')
            eta_low = line[0]
            eta_high = line[1]
            bins = line[2]
            line = line[3:]
            corr = [line[i:i+3] for i in range(0, len(line), 3)]
            for name, up, down in corr:
                up = float(up)
                down = float(down)
                if jec in jecs:
                    if (eta_low, eta_high) in jecs[jec]:
                        jecs[jec][(eta_low, eta_high)].update({name: [up,down]})
                    else:
                        jecs[jec].update({(eta_low, eta_high): {name: [up,down]}})
                else:
                    jecs[jec] = {(eta_low, eta_high): {name: [up,down]}}
    '''
    for jec in jecs:
        for name,corr in jecs[jec].items():
            if(corr[0] != corr[1]):
                print(name,corr)
    
    # Use FlavorQCD as template (all have same nubmer of corrections)
    jes_array = np.zeros(shape=(len(jecs.keys()), len(jecs['FlavorQCD'].keys()), 2))
    for i,jec in enumerate(jecs.values()):
        for j,corr in enumerate(jec.values()):
            jes_array[i][j] = corr
    
    for jes in jes_to_combine:
        collapse = [n for n,jec in enumerate(jecs) if jes in jec]
        print(collapse)
        print([jes_array.T[:,0:,].T[n-1] for n in collapse])
    '''
    
    '''
    for jes in jes_to_combine:
        # Use FlavorQCD as template (all have same nubmer of corrections)
        combined = np.zeros(len(jecs['FlavorQCD']))
        for jec in jecs:
            if jes in jec:
                print(jecs[jec])
    '''
    jecs_final = {}
    for jes in jes_to_combine:
        collapse = [(n,jec) for n,jec in enumerate(jecs) if jes in jec]
        if len(collapse)>0:
            jecs_final[jes] = {}
            for _,jec in collapse:
                for eta in jecs[jec]:
                    for pt in jecs[jec][eta]:
                        if eta in jecs_final[jes] and pt in jecs_final[jes][eta]:
                            sign = np.nan_to_num(jecs_final[jes][eta][pt] / np.abs(jecs_final[jes][eta][pt]), 1)
                            jecs_final[jes][eta][pt] = sign*np.sqrt(np.square(jecs_final[jes][eta][pt]) + np.square(jecs[jec][eta][pt]))
                        elif eta in jecs_final[jes]:
                            jecs_final[jes][eta].update({pt: np.array(jecs[jec][eta][pt])})
                        else:
                            jecs_final[jes].update({eta: {pt: np.array(jecs[jec][eta][pt])}})
    with open(topcoffea_path(file.replace('RegroupedV2', 'Quad')), 'w') as fout:
        for jec in jecs_final:
            fout.write(f'[{jec}]\n')
            fout.write(header)
            for eta in jecs_final[jec]:
                fout.write(' '.join(eta) + ' ' + str(3*(len(jecs_final[jec][eta].keys()))))
                for pt in jecs_final[jec][eta]:
                    corr = list(jecs_final[jec][eta][pt])
                    corr = [str(round(c, 4)) for c in corr]
                    fout.write(' ' + pt + ' ' + ' '.join(corr))
                fout.write('\n')
