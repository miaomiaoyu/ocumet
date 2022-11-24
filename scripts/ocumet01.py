
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

# these modules can be found at: https://github.com/miaomiaoyu/toolbox
from prepper import Prepper
from summarizer import Summarizer
from shoebox import *
from visualizer import *
from wrangler import *


# -- command line inputs

parser = argparse.ArgumentParser(description='prepper!')
parser.add_argument('--dataset', help='filename.ext of the dataset')
parser.add_argument('--lowercase', type=bool, default=False, help='make columns lowercase?')
args = parser.parse_args()


# -- arguments

dataset = args.dataset
lowercase = args.lowercase


# -- run prepper

pp = Prepper
data = pp.set_data(dataset, lowercase=lowercase)
data_variables = pp.set_variables(data)

