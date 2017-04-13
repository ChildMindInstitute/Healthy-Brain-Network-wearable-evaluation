#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
organize_wearable_data.py

Functions to organize data from wearable devices with Linux time-series index
columns and additional value columns. Unless otherwise specified, timestamps
are stored as datetime.

Created on Fri Apr 7 17:27:05 2017

@author: jon.clucas
"""
from config import actigraph_dir, e4_dir, geneactiv_dir, organized_dir, \
                   wavelet_dir
from datetime import datetime
import numpy as np, os, pandas as pd, time

axes = ['x', 'y', 'z']

"""
--------------------------------
Actigraph wGT3X-BT with Polar H7
--------------------------------
"""
def actigraph_acc(dirpath):
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
    acc_data = pd.DataFrame
    for acc in os.listdir(dirpath):
        if acc.endswith("1sec.csv"):
            if acc_data.empty:
                with open(os.path.join(dirpath, acc), 'r') as acc_f:
                    acc_data = actigraph_acc_data(acc_f)
            else:
                with open(os.path.join(dirpath, acc), 'r') as acc_f:
                    acc_data = pd.concat([acc_data, actigraph_acc_data(acc_f)])
            print(' : '.join(['Actigraph accelorometer data, adding', acc, str(
                  acc_data.shape)]))
    save_df(acc_data, 'accelerometer', 'Actigraph')
    
def actigraph_acc_data(open_csv):
    """
    Function to collect Actigraph data and return dataframe with Linux time-
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
    
    df = drop_non_csv(open_csv, 10, True)
    df['timestamp'] = df['timestamp'].map(actigraph_datetimeint)
    new_df = pd.DataFrame()
    new_df[['Timestamp', 'x', 'y', 'z']] = df[['timestamp', 'axis1', 'axis2',
                                           'axis3']]
    new_df.set_index('Timestamp', inplace=True)
    # convert from 1/128g to g
    for axis in axes:
        new_df[axis] = new_df[axis].map(lambda x: float(x)/128)
    return(new_df)

def actigraph_datetimeint(x):
    """
    Function to pass dt_format parameter to datetimeint(x, dt_format) for
    Actigraph data
    
    Parameters
    ----------
    x : string
        timestamp data from Actigraph
        
    Returns
    -------
    timestamp : int
        Linux timestamp (from datetimeformat)
    """
    dt_format='%Y-%m-%d %H:%M:%S'
    return(datetimeint(x, dt_format))

"""
-----------
Empatica E4
-----------
"""
def e4_acc(dirpath):
    """
    Function to take all e4 accelerometry data from a directory and format
    those data with Linux time-series index columns and x, y, z value columns
    
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
    E4.csv : csv file (via save_df() function)
        comma-separated-values file with Linux time-series index column and x,
        y, z accelerometer value columns
    """    
    acc_data = pd.DataFrame()
    for acc in os.listdir(dirpath):
        if "ACC" in acc and acc.endswith("csv"):
            if acc_data.empty:
                acc_data = e4_timestamp(pd.read_csv(os.path.join(dirpath, acc),
                           names=axes, index_col=False))
                print(' : '.join([acc, str(acc_data.shape)]))
            else:
                acc_data = pd.concat([acc_data, e4_timestamp(pd.read_csv(
                           os.path.join(dirpath, acc), names=axes,
                           index_col=False))])
            print(' : '.join(['E4 accelorometer data, adding',  acc, str(
                      acc_data.shape)]))
    # convert from 1/64g to g
    for axis in axes:
        acc_data[axis] = acc_data[axis].map(lambda x: float(x)/64)
    save_df(acc_data, 'accelerometer', 'E4')
    
def e4_timestamp(df):
    """
    Function to move the timestamp data from its own rows to an index column
    for E4 accelerometry data
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe for which to organize timestamps
        
    Returns
    -------
    new_df : pandas dataframe
        dataframe with Linux time-series index column and sensor-specific value
        columns
    """
    start_time = int(df.iloc[0,0])
    sample_rate = int(df.iloc[1,0])
    new_df = df[2:].copy()
    new_index = np.arange(start_time, len(new_df)*sample_rate+start_time,
                sample_rate)
    new_df['Timestamp'] = pd.Series(new_index).apply(lambda x:
                          datetime.fromtimestamp(int(x)).strftime(
                          "%Y-%m-%d %H:%M:%S.%f"))
    new_df.set_index('Timestamp', inplace=True)
    return(new_df)

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
def geneactiv_acc(dirpath):
    """
    Function to take all GENEActiv accelerometry data from a directory and
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
    GENEActiv_`color`.csv : csv file (via save_df() function)
        comma-separated-values file with Linux time-series index column and x,
        y, z accelerometer value columns
    """    
    acc_data_black = pd.DataFrame()
    acc_data_pink = pd.DataFrame()
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
                    acc_data_pink = pd.concat([acc_data_black, 
                                     geneactiv_acc_data(acc_f)])
            print(' : '.join(['Pink GENEActiv accelorometer data, adding',
                  acc, str(acc_data_pink.shape)]))
    save_df(acc_data_black, 'accelerometer', 'GENEActiv_black')
    save_df(acc_data_black, 'accelerometer', 'GENEActiv_pink')
    
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
    # convert from 1/64g to g
    for axis in axes:
        acc_data_returns[axis] = acc_data_returns[axis].map(lambda x: float(x)/
                                 64)
    save_df(acc_data_returns, 'accelerometer', 'Wavelet')
    

"""
-----------------
general functions
-----------------
"""
def datetimedt(x):
    """
    Function to turn a datetime in format "%Y-%m-%d %H:%M:%S.%f" (e.g., outputs
    from datetimeint()) into a datetime object
    
    Parameter
    ---------
    x : string
        datetime string in format "%Y-%m-%d %H:%M:%S.%f"
        
    Returns
    -------
    timestamp : datetime
        Linux timestamp
    """
    return(datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"))

def datetimeint(x, dt_format='%Y-%m-%d %H:%M:%S:%f'):
    """
    Function to turn a datetime string into an datetime formatted as
    "%Y-%m-%d %H:%M:%S.%f"
    
    Parameters
    ----------
    x : string
       datetime string
       
    dt_format : string
       datetime format (default='%Y-%m-%d %H:%M:%S:%f')
       
    Returns
    -------
    timestamp : string
        Linux timestamp as string formatted as "%Y-%m-%d %H:%M:%S.%f"
    """
    return(datetime.strptime(x, dt_format).strftime("%Y-%m-%d %H:%M:%S.%f"))

def drop_non_csv(open_csv_file, drop_rows, header_row=False):
    """
    Function to read a csv file into a pandas dataframe dropping a specified
    number of rows first.
    
    Parameters
    ----------
    open_csv_file : open csv file
        an open csv file
        
    drop_rows : int
        number of rows to drop
        
    header_row : boolean
        Does csv contain a header after dropped rows? (default=False)
        
    Returns
    -------
    df : pandas dataframe
        a pandas dataframe without the dropped top rows
    """
    header = None
    for x in range(0, drop_rows):
        open_csv_file.readline()
    if header_row:
        header = open_csv_file.readline().split(',')
    lines = open_csv_file.readlines()
    df = pd.DataFrame([sub.split(',') for sub in lines], columns=header)
    return(df)

def main():
    e4_acc(e4_dir)
    geneactiv_acc(geneactiv_dir)
    actigraph_acc(actigraph_dir)
    wavelet_acc(wavelet_dir)

def save_df(df, sensor, device):
    """
    Function to save formatted dataframe to csv in organized_dir (defined in
    config.py).
    
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
    out_dir = os.path.join(organized_dir, sensor)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    print(''.join(['Saving formatted ', sensor, ' data from ', device]))
    df.to_csv(os.path.join(out_dir, '.'.join([device, 'csv'])))
    return(df)

# ============================================================================
if __name__ == '__main__':
    main()