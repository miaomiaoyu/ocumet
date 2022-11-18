#!/bin/usr/env python3
#
# MY, 2022
# ocumet_clean

import numpy as np
import pandas as pd
from tabulate import tabulate

"""
Nov 17 2022
1 data cleaning for 'ocumet-1102-raw.csv'
"""

df = pd.read_csv("../data/ocumet-1102-raw.csv")

df = df[df.columns.drop(list(df.filter(regex='RimProf')))]  # drop columns with RimProf_
df = df.dropna(subset=['Subject ID'])
df['ID'] = df['Subject ID'].astype(int).astype(str) + '.' + df['Eye']  # get id for each eye
df['Bilateral'].fillna('', inplace=True)
df['DiagnosisTmp'] = df['Diagnosis'] + '_' + df['Bilateral']
df['DiagnosisTmp'] = df['DiagnosisTmp'].str.replace("_", "")

# Clean up Diagnosis
df = df.replace({
    "Not control": "Not Control", 
    "Not controlN": "Not Control",
    "not control": "Not Control",
    "NAIONY": "NAION Bilateral",
    "NAIONN": "NAION Unilateral"})

df = df[df['DiagnosisTmp'].isin(
    ['Control', 'NAION Unilateral', 'NAION Bilateral', 'ODD'])]

print(tabulate(df.iloc[:5,:15].head()))

df.to_csv("../data/ocumet-1102-clean-01.csv", index=False)