import os
import warnings
import argparse
import numpy as np
import pandas as pd
import matplotlib

from prepper import Prepper


# -- command line inputs

parser = argparse.ArgumentParser(description='prepper!')
parser.add_argument('--dataset', help='filename.ext of the dataset')
parser.add_argument('--lowercase', type=bool, default=False, help='make columns lowercase?')
args = parser.parse_args()

# -- arguments

dataset = args.dataset
lowercase = args.lowercase

# -- prepper

pp = Prepper
data = pp.set_data(dataset, lowercase=lowercase)
data_variables = pp.set_variables(data)

# -- 


#!/bin/usr/env python3
#
# MY, 2022
# OCUMET

import numpy as np
import pandas as pd
from tabulate import tabulate

"""
Nov 17 2022

1 data cleaning for 'ocumet-1102-raw.csv'

"""

df = pd.read_csv("../data/ocumet-1102-raw.csv")

class cleaningteam:

    def __init__(self, df):
        print("df initialized")
        self.df = df

    def to_drop(self, arg):
        ''' drops columns by arg provided. arg can be a string or a list '''
        data = self.df
        if not type(arg) == list:
            arg = [arg]
        for substring in arg:
            data = data[data.columns.drop(list(data.filter(regex=substring)))]
        self.df = data
    
    def to_create(self, arg):
        ''' creates new columns based on the values for arg '''
        data = self.df
        for k,v in arg.items():
            if len(v)==2:
                data[k] = data[v[0]].astype(str) + '_' + data[v[1]].astype(str)
            elif len(v)==3:
                data[k] = data[v[0]].astype(str) + '_' + data[v[1]].astype(str) + '_' + data[v[2]].astype(str)
        self.df = data
    
    def to_replace(self, arg):
        ''' replaces all instances of key in df with value. arg should be a dictionary '''
        data = self.df
        data = data.replace(arg)
        self.df = data

    def to_filter(self, arg):
        pass
    




ct = cleanteam(df)
df = ct.to_drop(['RimProf', 'Subject ID'])



# drop variables
df = df[df.columns.drop(list(df.filter(regex='RimProf')))]  # drop columns with RimProf_

# create variables

# filter by variables

df = df.dropna(subset=['Subject ID'])
df['ID'] = df['Subject ID'].astype(int).astype(str) + '.' + df['Eye']  # get id for each eye
df['Bilateral'].fillna('', inplace=True)
df['Group'] = df['Diagnosis'] + '_' + df['Bilateral']
df['Group'] = df['Group'].str.replace("_", "")

# clean up diagnosis
df = df.replace({"Not control": "Not Control", "Not controlN": "Not Control", "not control": "Not Control", "NAIONY": "NAION Bilateral", "NAIONN": "NAION Unilateral"})

df = df[df['Group'].isin(
    ['Control', 'NAION Unilateral', 'NAION Bilateral', 'ODD'])]

df.rename(columns={'Visit_no':'Visit'}, inplace=True)
df.to_csv("../data/ocumet-1102-clean.csv", index=False)

for j in ['FPF', 'OCT']:
    
    dvars_tmp = [col for col in df.columns if col.startswith(j)]  
    data = df[ ivars + dvars_tmp ].copy()
    dvars = [dvar.split("_")[1] + "_" + dvar.split("_")[-1] for dvar in dvars_tmp]
    data.rename(columns=dict(zip(dvars_tmp, dvars)), inplace=True)
    data = foo().fill_nans(data, dvars, ivar='Diag')
    data.to_csv('../data/ocumet-1102-clean-{}.csv'.format(j))

    print(tabulate(data.iloc[:5,:8].head()))
