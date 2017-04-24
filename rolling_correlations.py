#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rolling_correlation.py

Functions to calculate and plot rolling correlation values pairwise between
wearable device data streams.

Created on Fri Apr 21 16:28:13 2017

@author: jon.clucas
"""
from config import organized_dir
from datetime import datetime
import os, pandas as pd, sys
precision_dict = {'year':-6, 'month':-5, 'week': -4, 'day': -3, 'hour':-2,
                  'minute':-1, 'second':0, 'decisecond':1, 'centisecond':2,
                  'millisecond':3, 'microsecond':4, 'nanosecond':5,
                  'picosecond':6}

def only_matching_ts_points(s0, s1, precision='second'):
    """
    Function to match time-series data streams point for point to the lowest
    resolution.
    
    Parameters
    ----------
    s0 : pandas dataframe
        time-series data stream
        
    s1 : pandas dataframe
        time-series data stream
        
    precision : int or string
        if int, the number of decimal places of a fractional second; if string,
        the time unit of resolution to match to.
        
    Returns
    -------
    m0: pandas dataframe
        time-series data with precision matching m2
    
    m1 : pandas dataframe
        time-series data with precision matching m1
    """
    if isinstance(precision, str):
        precision = int(precision_dict[precision])
    if precision < 0:
        sys.exit("Matching precision less than second is not yet implemented")
    m0 = combine_extra_precision(s0, precision)
    m1 = combine_extra_precision(s1, precision)
    return(m0, m1)
    
def combine_extra_precision(df, decimals):
    """
    Function to combine precision beyond the comparable limit.
    
    Parameters
    ----------
    df : pandas dataframe
        time series data
        
    decimals : int
        the number of decimal places of a fractional second to include
        
    Returns
    -------
    df : pandas dataframe
        time series data with resolution reduced to specified level of
        precision
    """
    if(decimals == 0):
        df[['Timestamp']] = df.Timestamp.apply(lambda x: datetime(x.year,
                            x.month, x.day, x.hour, x.minute, x.second))
    else:
        df[['Timestamp']] = df.Timestamp.apply(lambda x: datetime(x.year,
                            x.month, x.day, x.hour, x.minute, x.second,
                            x.microseconds.round(decimals)))
    df = pd.DataFrame(df.groupby(by='Timestamp')[list(df.columns)[1]].mean())
    return(df)

def r_corr(devices, sensor, start, stop):
    """
    Function to calculate rolling correlations between two sensor data streams.
    
    Parameters
    ----------
    devices : list of strings (len 2)
        each string is the name of one of the two devices to compare
        
    sensor : string
        the sensor to compare
        
    start : datetime
        beginning of time to compare
        
    stop : datetime
        end of time to compare
        
    Returns
    -------
    ?
    """
    if sensor == 'accelerometer':
        suffix = '_normalized_unit.csv'
    else:
        suffix = '.csv'
    s0 = pd.read_csv(os.path.join(organized_dir, sensor, ''.join([devices[0],
         suffix])), usecols=['Timestamp', 'normalized_vector_length'],
         parse_dates=['Timestamp'], infer_datetime_format=True)
    s0 = s0.loc[(s0['Timestamp'] >= start) & (s0['Timestamp'] <= stop)].copy()
    s1 = pd.read_csv(os.path.join(organized_dir, sensor, ''.join([devices[1],
         suffix])), usecols=['Timestamp', 'normalized_vector_length'],
         parse_dates=['Timestamp'], infer_datetime_format=True)
    s1 = s1.loc[(s1['Timestamp'] >= start) & (s1['Timestamp'] <= stop)].copy()
    m0, m1 = only_matching_ts_points(s0, s1, 'second')
    df = m0.merge(m1, left_index=True, right_index=True, suffixes=(''.join([
         '_', devices[0]]), ''.join(['_', devices[1]])))
    correls = df.rolling(window=2, center=True).corr()
    print(correls.loc[:, list(df.columns)[0], list(df.columns)[1]])
    # df.rolling(window=5, center=True).corr().sum().plot()
    # df.rolling(window=2, center=True).corr().sum().plot()
    
r_corr(['GENEActiv_pink', 'Actigraph'], 'accelerometer',  datetime(2017, 4, 6,
       15, 45), datetime(2017, 4, 7, 14, 8))