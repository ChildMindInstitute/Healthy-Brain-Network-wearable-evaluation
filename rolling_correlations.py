#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rolling_correlation.py

Functions to calculate and plot rolling correlation values pairwise between
wearable device data streams.

Created on Fri Apr 21 16:28:13 2017

@author: jon.clucas

TODO: clip dfs and try again
"""
from config import organized_dir
import os, pandas as pd

def r_corr(devices, sensor):
    if sensor == 'accelerometer':
        suffix = '_normalized_unit.csv'
    else:
        suffix = '.csv'
    s0 = pd.read_csv(os.path.join(organized_dir, sensor, ''.join([devices[0],
         suffix])), usecols=['Timestamp', 'normalized_vector_length'],
         parse_dates=['Timestamp'], infer_datetime_format=True)
    s1 = pd.read_csv(os.path.join(organized_dir, sensor, ''.join([devices[1],
         suffix])), usecols=['Timestamp', 'normalized_vector_length'],
         parse_dates=['Timestamp'], infer_datetime_format=True)
    print(pd.rolling_corr(s0, s1, 12)) 
    
r_corr(['E4', 'Actigraph'], 'accelerometer')