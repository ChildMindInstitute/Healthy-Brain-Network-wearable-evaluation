#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_acc_data.py

Functions to normalize accelerometery data to a single number from wearable
devices with Linux time-series index columns and additional value columns.
Unless otherwise specified, timestamps are stored as datetime.
Actigraphy values calculated as √((x/√((max(x))² + (max(y))² + (max(z))²))² +
(y/√((max(x))² + (max(y))² + (max(z))²))² + (z/√((max(x))² + (max(y))² + (max(z
))²))²), i.e. vector length normalized to a unit cube.

@author: jon.clucas
"""
from config import actigraph_dir, e4_dir, geneactiv_dir, organized_dir,       \
                   wavelet_dir
from organize_wearable_data import actigraph_datetimeint, datetimeint,        \
                                   drop_non_csv, e4_timestamp
from datetime import datetime
from math import sqrt
import numpy as np, os, pandas as pd

axes = ['x', 'y', 'z']

"""
--------------------------------
Actigraph wGT3X-BT with Polar H7
--------------------------------
"""
def actigraph_acc(dirpath, outpath=None):
    """
    Function to take all Actigraph accelerometry data from a directory and
    format those data with Linux time-series index columns and x, y, z value
    columns
    
    Parameters
    ----------
    dirpath : string
        path to E4 outputs
        
    Returns
    -------
    acc_data : pandas dataframe
        dataframe with Linux time-series index column and x, y, z value columns
    
    Outputs
    -------
    Actigraph.csv : csv file (via save_df() function)
        comma-separated-values file with Linux time-series index column and x,
        y, z accelerometer value columns
    """    
    acc_data = pd.DataFrame()
    for acc in os.listdir(dirpath):
        if acc.endswith("RAW.csv"):
            acc_path = os.path.join(dirpath, acc)
            if acc_data.empty:
                acc_data = pd.read_csv(acc_path, skiprows=10, header=0,
                           parse_dates=['Timestamp'], infer_datetime_format=
                           True)
            else:
                acc_data = pd.concat([acc_data, pd.read_csv(acc_path, skiprows=
                           10, header=0, parse_dates=['Timestamp'],
                           infer_datetime_format=True)])
            print(' : '.join(['Actigraph accelorometer data, adding', acc, str(
                  acc_data.shape)]))
    acc_data_new = pd.DataFrame({'Timestamp': [], 'x': [], 'y': [], 'z': []})
    acc_data_new[['Timestamp', 'x', 'y', 'z']] = acc_data[['Timestamp',
                                                 'Accelerometer X',
                                                 'Accelerometer Y',
                                                 'Accelerometer Z']]
    acc_data_new.set_index('Timestamp', inplace=True)
    for column in list(acc_data_new.columns):
        print(column, end=": ")
        print(max(acc_data_new[column]))
    acc_data_new = normalize(acc_data_new, 1024)
    if outpath:
        save_df(acc_data_new, 'accelerometer', 'Actigraph', outpath)
    else:
        save_df(acc_data_new, 'accelerometer', 'Actigraph')

"""
-----------
Empatica E4
-----------
"""
def e4_acc(dirpath):
    """
    Function to take all e4 accelerometry data from a directory and format
    those data with Linux time-series index column and x, y, z value columns
    
    Parameters
    ----------
    dirpath : string
        path to E4 outputs
        
    Returns
    -------
    None
    
    Outputs
    -------
    E4_normalized_unit.csv : csv file (via save_df() function)
        comma-separated-values file with Linux time-series index column and x,
        y, z, normalized_vector_length accelerometer value columns
    """    
    acc_data = pd.DataFrame()
    for acc in os.listdir(dirpath):
        if "E4" in acc and acc.endswith("csv"):
            if acc_data.empty:
                acc_data = e4_timestamp(pd.read_csv(os.path.join(dirpath, acc),
                           header=0, parse_dates=['Timestamp'],
                           infer_datetime_format=True, index_col=0,
                           dtype='float'))
                print(' : '.join([acc, str(acc_data.shape)]))
            else:
                acc_data = pd.concat([acc_data, e4_timestamp(pd.read_csv(
                           os.path.join(dirpath, acc), header=0,
                           parse_dates=['Timestamp'], infer_datetime_format=
                           True, index_col=0, dtype='float'))])
            print(' : '.join(['E4 accelorometer data, adding',  acc, str(
                  acc_data.shape)]))
    acc_data = normalize(acc_data, 128)
    save_df(acc_data, 'accelerometer', 'E4')

"""
----------------
Empatica Embrace
----------------
"""

"""
------------
Fitbit Blaze
------------
"""

"""
------------------
GENEActiv Original
------------------
"""
def geneactiv_acc(dirpath, outpath=None):
    """
    Function to take all GENEActiv accelerometry data from a directory and
    format those data with Linux time-series index column and x, y, z value
    columns
    
    Parameters
    ----------
    dirpath : string
        path to E4 outputs
        
    Returns
    -------
    acc_data : pandas dataframe
        dataframe with Linux time-series index column and x, y, z value columns
    
    Outputs
    -------
    GENEActiv_`color`.csv : csv file (via save_df() function)
        comma-separated-values file with Linux time-series index column and x,
        y, z accelerometer value columns
    """    
    acc_data_black = pd.DataFrame()
    acc_data_pink = pd.DataFrame()
    acc_data = pd.DataFrame()
    for acc in os.listdir(dirpath):
        if "Jon" in acc and acc.endswith("csv"):
            if acc_data_black.empty:
                with open(os.path.join(dirpath, acc), 'r') as acc_f:
                    acc_data_black = geneactiv_acc_data(acc_f)
            else:
                with open(os.path.join(dirpath, acc), 'r') as acc_f:
                    acc_data_black = pd.concat([acc_data_black, 
                                     geneactiv_acc_data(acc_f)])
            print(' : '.join(['Black GENEActiv accelorometer data, adding',
                  acc, str(acc_data_black.shape)]))
        elif (("Curt" in acc or "Arno" in acc) and acc.endswith("csv")):
            if acc_data_pink.empty:
                with open(os.path.join(dirpath, acc), 'r') as acc_f:
                    acc_data_pink = geneactiv_acc_data(acc_f)
            else:
                with open(os.path.join(dirpath, acc), 'r') as acc_f:
                    acc_data_pink = pd.concat([acc_data_pink, 
                                     geneactiv_acc_data(acc_f)])
            print(' : '.join(['Pink GENEActiv accelorometer data, adding',
                  acc, str(acc_data_pink.shape)]))
        elif acc.endswith("csv"):
            if acc_data.empty:
                with open(os.path.join(dirpath, acc), 'r') as acc_f:
                    acc_data = geneactiv_acc_data(acc_f)
            else:
                with open(os.path.join(dirpath, acc), 'r') as acc_f:
                    acc_data = pd.concat([acc_data_pink, 
                                     geneactiv_acc_data(acc_f)])
            print(' : '.join(['GENEActiv accelorometer data, adding',
                  acc, str(acc_data.shape)]))
    for acc_data_f in [acc_data_black, acc_data_pink, acc_data]:
        if(not acc_data_f.empty):
            acc_data_f = normalize(acc_data, 8)
    if outpath:
        if len(acc_data_black > 0):
            save_df(acc_data_black, 'accelerometer', 'GENEActiv_black', outpath)
        if len(acc_data_pink > 0):
            save_df(acc_data_pink, 'accelerometer', 'GENEActiv_pink', outpath)
        if len(acc_data > 0):
            save_df(acc_data, 'accelerometer', 'GENEActiv', outpath)
    else:
        if len(acc_data_black > 0):
            save_df(acc_data_black, 'accelerometer', 'GENEActiv_black')
        if len(acc_data_pink > 0):
            save_df(acc_data_pink, 'accelerometer', 'GENEActiv_pink')
        if len(acc_data > 0):
            save_df(acc_data, 'accelerometer', 'GENEActiv')
    
def geneactiv_acc_data(open_csv):
    """
    Function to collect GENEActiv data and return dataframe with Linux time-
    series index column and x, y, z value columns
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe for which to organize data
        
    Returns
    -------
    new_df : pandas dataframe
        dataframe with Linux time-series index column and accelerometer value
        columns
    """
    df = drop_non_csv(open_csv, 100)
    df[0] = df[0].map(datetimeint)
    new_df = pd.DataFrame()
    new_df[['Timestamp', 'x', 'y', 'z']] = df[[0,1,2,3]]
    new_df.set_index('Timestamp', inplace=True)
    return(new_df)

"""
----------------
Wavelet Biostrap
----------------
"""
def wavelet_acc(dirpath):
    """
    Function to take all Wavelet accelerometry data from a directory and format
    those data with Linux time-series index columns and x, y, z value columns
    
    Parameters
    ----------
    dirpath : string
        path to Wavelet outputs
        
    Returns
    -------
    acc_data_returns : pandas dataframe
        dataframe with Linux time-series index column and x, y, z value columns
    
    Outputs
    -------
    Wavelet.csv : csv file (via save_df() function)
        comma-separated-values file with Linux time-series index column and x,
        y, z accelerometer value columns
    """    
    csv_path = os.path.join(dirpath, 'CSV')
    acc_data = pd.DataFrame()
    for acc in os.listdir(csv_path):
        if acc.endswith("csv"):
            if acc_data.empty:
                acc_data = pd.read_csv(os.path.join(csv_path, acc),
                           header=0, skip_blank_lines=True, comment="C")
                print(' : '.join([acc, str(acc_data.shape)]))
            else:
                acc_data = pd.concat([acc_data, pd.read_csv(os.path.join(
                           csv_path, acc), header=0, skip_blank_lines=True,
                           comment="C")])
            print(' : '.join(['Wavelet accelorometer data, adding',  acc, str(
                      acc_data.shape)]))
    acc_data['timestamp'] = acc_data['timestamp'].map(lambda x:
                            datetime.fromtimestamp(int(x)/1000).strftime(
                            "%Y-%m-%d %H:%M:%S.%f"), na_action='ignore')
    acc_data_returns = pd.DataFrame()
    acc_data_returns[['Timestamp', 'x', 'y', 'z']] = acc_data[['timestamp',
                                                     ' accel.X', ' accel.Y',
                                                     ' accel.Z']]
    acc_data_returns.set_index('Timestamp', inplace=True)
    acc_data_returns = normalize(acc_data_returns, 128)
    save_df(acc_data_returns, 'accelerometer', 'Wavelet')

def main():
    # accelerometry
    acc_dir = os.path.join(organized_dir, 'accelerometer')
    # unit: normalized vector length (/1)
    e4_acc(acc_dir)
    # geneactiv_acc(acc_dir)
    # actigraph_acc(acc_dir)
    # wavelet_acc(acc_dir)
    
def normalize(df, scale):
    """
    function to calculate vector length normalized to a unit cube (i.e., √((x/√
    ((max(x))² + (max(y))² + (max(z))²))² + (y/√((max(x))² + (max(y))² + (max(z
    ))²))² + (z/√((max(x))² + (max(y))² + (max(z))²))²))
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe with ['x', 'y', 'z'] columns to normalize
    
    scale : numeric
        maximum possible absolute value of dataframe's current scale
        
    Returns
    -------
    df : pandas dataframe
        dataframe with ['normalized_vector_length'] column added
    """
    unit = np.float64(sqrt(3*(scale**2)))
    for column in list(df.columns):
        df[column] = df[column].map(np.float64)
    df['normalized_vector_length'] = np.sqrt((df['x'] / unit) ** 2 + (df['y'] /
                                     unit) ** 2 + (df['z'] / unit) ** 2)
    return(df)

def save_df(df, sensor, device, organized_dir_out=organized_dir):
    """
    Function to save formatted dataframe to csv in organized_dir (defined in
    config.py) or to specified dir.
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe to save
        
    sensor : string
        sensor for which dataframe holds data
    
    device : string
        device data is from
        
    Outputs
    -------
    csv file
        comma-separated-values file with Linux time-series index column and
        sensor-specific value columns, stored in `organized_dir`/`sensor`/
        `device`.csv
    
    Returns
    -------
    df : pandas dataframe
        unmodified dataframe
    """
    out_dir = os.path.join(organized_dir_out, sensor)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    print(''.join(['Saving formatted ', sensor, ' data from ', device]))
    df.to_csv(os.path.join(out_dir, '.'.join(['_'.join([device, 'normalized',
              'unit']), 'csv'])))
    print("Saved.")
    return(df)

# ============================================================================
if __name__ == '__main__':
    main()