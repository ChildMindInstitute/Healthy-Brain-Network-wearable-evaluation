#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
organize_wearable_data.py

Functions to organize data from wearable devices with Linux time-series index
columns and additional value columns

Created on Fri Apr  7 17:27:05 2017

@author: jon.clucas
"""
from config import e4_dir
import numpy as np, os, pandas as pd

def e4_acc(dirpath):
    """
    Function to take all e4 accelerometry data from a directory and format that
    data with Linux time-series index columns and x, y, z value columns
    """
    acc_data = pd.DataFrame
    for acc in os.listdir(dirpath):
        if "ACC" in acc and acc.endswith("csv"):
            if pd.DataFrame.empty:
                acc_data = e4_acc_timestamp(pd.read_csv(os.path.join(dirpath,
                                 acc), names=['x', 'y', 'z'], index_col=False))
            else:
                acc_data.append(e4_acc_timestamp(pd.read_csv(os.path.join(
                                dirpath, acc), names=['x', 'y', 'z'], index_col
                                =False)))
    print(acc_data)
    
def e4_acc_timestamp(df):
    """
    Function to move the timestamp data from its own rows to an index column
    for E4 accelerometry data
    """
    start_time = int(df.iloc[0,0])
    sample_rate = int(df.iloc[1,0])
    new_df = df[2:].copy()
    new_index = np.arange(start_time, len(new_df)*sample_rate+start_time,
                sample_rate)
    new_df['Timestamp'] = new_index
    new_df.set_index('Timestamp', inplace=True)
    return(new_df)

def main():
    e4_acc(e4_dir)

# ============================================================================
if __name__ == '__main__':
    main()