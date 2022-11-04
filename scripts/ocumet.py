#!/usr/bin/env python3
#
# ocumet: ocumet.py
#
# MY, 11-02-2022
# mmy@stanford.edu


import pandas as pd
import numpy as np


class Ocumet:

    def __init__(self):

        pass


    def read_data(self, filepath):
        
        df = pd.read_excel(filepath, header=1)
        
        return df


    
    
