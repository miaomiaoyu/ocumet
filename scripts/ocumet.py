#!/usr/bin/env python3
#
# ocumet: ocumet.py
#
# MY, 11-02-2022
# mmy@stanford.edu


import pandas as pd
import numpy as np



def fill_nans_with_means(df, columns, group):
    
    """
    Fills NaN values of columns (specified by columns) with the mean of the group (specified by group) within dataframe.

    Parameters:
        df
        columns
        group
    
    Returns:
        transformed_df

    """

    fillers = df.groupby([group])[columns].mean().reset_index()
    
    transformed_dfs = []

    for this_group in df[group].unique():
        group_df = df[df[group]==this_group].copy()

        for col in columns:
            filler = fillers[fillers[group]==this_group][col].values[0]
            group_df.loc[:,col].fillna(filler, inplace=True)
        
        transformed_dfs.append(group_df)
    
    return pd.concat(transformed_dfs)



class Ocumet:

    def __init__(self):

        pass


    def read_data(self, filepath):
        
        df = pd.read_excel(filepath, header=1)
        
        return df


    
    
