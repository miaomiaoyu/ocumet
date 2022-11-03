#!/usr/bin/env python3

# test python script
# MY, 10-31-2022
# mmy@stanford.edu



import sys
import pandas as pd
from ocumet import Ocumet

ocumet = Ocumet()

filepath = '../data/20221102_ocumet_data.xlsx'

df = ocumet.read_data(filepath)