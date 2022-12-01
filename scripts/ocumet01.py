
#!usr/bin/env python3
#
# MY, 23 Nov 2022
# mmy@stanford.edu

'''
Ocumet Data Analysis
	comparisons of controls with 1) NAION and 2) ODD patients
    looking at FPF and OCT measurements (expected to negatively correlate)
    NAION group split into unilateral and bilaterally affected subgroups
'''

import os
import glob
import warnings
import argparse
import numpy as np
import pandas as pd
from tabulate import tabulate

import palettable
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from sklearn.preprocessing import StandardScaler

# these modules can be found at: https://github.com/miaomiaoyu/toolbox
from prepper import Prepper as pp
from summarizer import Summarizer
from shoebox import *
from visualizer import *
from wrangler import *


def is_data(data_type, accepted=('fpf', 'oct')):
    ''' checks that the data is of the right type '''
    return data_type in accepted

def parse_args():
    parser = argparse.ArgumentParser(description='Ocumet FPF analysis')
    parser.add_argument('--dataset', help='filename.ext of the main dataset')
    parser.add_argument('--datatype', help='fpf or oct')
    parser.add_argument('--lowercase', help='lowercase columns')
    args = parser.parse_args()
    assert (is_data(args.datatype)), \
        'data_type has to be `fpf` or `oct`.'
    return args


def split_data(args, datatype):
    ''' splits ocumet dataset into 'oct' and 'fpf' sets '''

    dataset = args.dataset
    lowercase = args.lowercase
    data = pp.get_data(dataset, lowercase=lowercase)
    ivars = ['id', 'visit_no', 'diagnosistmp']
    dvars = [col for col in data.columns if col.startswith(datatype)]  # FPF
    dvars.append('hvf_mean_deviation')
    subset = data[ ivars + dvars ].copy()
    dvars.remove('hvf_mean_deviation')
    dvars_tmp = [dvar.split("_")[1] + "_" + dvar.split("_")[-1] for dvar in dvars]  # remove the dvar_type
    subset.rename(columns=dict(zip(dvars, dvars_tmp)), inplace=True)
    dvars = rank_list(lst=dvars_tmp, order=['rnfl', 'gh', 'gcc', 'cq'])
    subset = set_nans(data=subset, dvars=dvars_tmp, ivars='diagnosistmp')
    subset.to_csv('../data/ocumet-1102-clean-%s.csv' % datatype, index=False)
    print(tabulate(subset.head(3)))
    print('%s dataframe saved' % datatype)


def get_clustermap(dataset, dvars, ivars, scale_to, cmap):    
    ''' grpvar is the one to separate groups '''

    data = dataset.copy()
    data = set_nans(data, dvars=dvars, ivars='diagnosistmp', how='mean')
    scaler = StandardScaler()

    match scale_to:
        case 'none':
            pass
        case 'all':
            data[dvars] = scaler.fit_transform(data[dvars])
        case 'control':
            control_data = data[data[ivars]=='Control']
            scaler.fit(control_data[dvars])
            data[dvars] = scaler.transform(data[dvars])

    dx_palette = get_palette('cartacube')
    dx_levels = data[ivars].unique().tolist()
    dx_lut = dict(zip(dx_levels, dx_palette))
    dx_colors = data[ivars].map(dx_lut)

    g = sns.clustermap(
        data[dvars].T, 
        cmap=cmap,
        center=0, 
        figsize=(25,4), 
        col_colors=dx_colors,
        dendrogram_ratio=(.05,.2), 
        cbar_kws=dict(orientation='horizontal'),
        linewidth=.5)

    axes_object = g.ax_heatmap
    format_xticklabels(axes_object)
    format_yticklabels(axes_object)
    g.tick_params(axis='both', labelbottom=False)

    set_font('h', 14)
    set_colorlegend(dx_lut, 'Diagnosis', ncol=3, bbox_to_anchor=(0.4, 0.2))
    ''' left_pos, bottom_pos, cbar_width, cba_height'''

    title = 'Standardized'
    spinecolor = 'k'
    spinewidth = 1
    g.ax_cbar.set_position((.92,.8,.05,.05))
    g.ax_cbar.set_title(title)
    g.ax_cbar.set_xticks([0,5])
    g.ax_cbar.set_xticklabels([0,5])

    for spine in g.ax_cbar.spines:
        g.ax_cbar.spines[spine].set_color(spinecolor)
        g.ax_cbar.spines[spine].set_linewidth(spinewidth)

    return g

# -- arguments

def main(args):

    import os
    from prepper import Prepper as pp
    
    datatype = args.datatype
    filepath = '../data/ocumet-1102-clean-%s.csv' % datatype
    
    if ~os.path.exists(filepath):
        split_data(args, datatype)

    dataset = pp.get_data(filepath)
    print(filepath)
    print(dataset.columns)
    idvars = ['id', 'visit_no']
    ivars = 'diagnosistmp'
    
    dvars = [col for col in dataset.columns if (
        not col in idvars) and (not col in ivars) and (not col.startswith('hvf'))]
    
    cmap = get_palette('redblue1')
    g = get_clustermap(dataset, dvars, ivars, scale_to='control', cmap=cmap)

    g.savefig('../output/clustermap_01.pdf')

if __name__ == "__main__":
    args = parse_args()
    main(args)
