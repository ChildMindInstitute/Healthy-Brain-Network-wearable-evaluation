#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chart_data.py

Functions to organize data into charts from which we can compare
our devices.

Created on Mon Apr 10 17:25:39 2017

@author: jon.clucas
"""
# from utilities.analysis_2 import *
from astropy.stats import median_absolute_deviation as mad
from config import config
from datetime import datetime, timedelta
from utilities.fetch_data import fetch_check_data, fetch_data, fetch_hash
from utilities.normalize_acc_data import normalize as norm
import json, numpy as np, os, pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
from plotly.graph_objs import *
init_notebook_mode()
import holoviews as hv
hv.extension('bokeh')
with open(os.path.join('./config/device_colors.json')) as fp:
    color_key = json.load(fp)


def bland_altman_plot(data1, data2, *args, **kwargs):
    """
    Function to build a Bland-Altman plot.
    
    Parameters
    ----------
    data1, data2 : pandas dataframes
        dataframes to compare
        
    *args, **kwargs : various types
        additional arguments for plotting
    """
    data1     = np.asarray(data1)
    data2     = np.asarray(data2)
    mean      = np.mean([data1, data2], axis=0)
    diff      = data1 - data2            # Difference between data1 and data2
    md        = np.mean(diff)            # Mean of the difference
    sd        = np.std(diff, axis=0)     # Standard deviation of the difference

    plt.scatter(mean, diff, *args, **kwargs)
    plt.axhline(md,           color='gray', linestyle='--')
    plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
        
def df_devices_qt(devices, sensor, start, stop, acc_hashes={}):
    """
    Function to calculate rolling correlations between two sensor data streams.
    
    Parameters
    ----------
    devices : list of (subdirectory, device) tuples (len 2)
        each string is the name of one of the two devices to compare
        
    sensor : string
        the sensor to compare
        
    start : datetime
        beginning of time to compare
        
    stop : datetime
        end of time to compare
        
    acc_hashes : dictionary
        dictionary of cached datafile hashes
        
    Returns
    -------
    df : pandas dataframe
        merged dataframe with a column per device
    """
    suffix = '.csv'
    s = []
    for i, device in enumerate(devices):
        s.append(pd.read_csv(fetch_data(config.rawurls[
                 sensor][device[1]]),
                 parse_dates=['Timestamp'], infer_datetime_format=True))
        s[i] = s[i].loc[(s[i]['Timestamp'] >= start) & (s[i]['Timestamp'] <=
               stop)].copy()
        s[i] = norm(s[i])
        if device[1] == 'ActiGraph wGT3X-BT':
            s[i][['Timestamp']] = s[i].Timestamp.apply(lambda x: x - 
                                  timedelta(microseconds=1000))
        s[i].set_index('Timestamp', inplace=True)
    df = s[0].merge(s[1], left_index=True, right_index=True, suffixes=(''.join(
         ['_', devices[0][1]]), ''.join(['_', devices[1][1]])))
    for i in range(2, len(s), 1):
        df = df.merge(s[i], left_index=True, right_index=True, suffixes=('', ''.join(['_', devices[i][1]])))
    return(df)


def hvplot(device_data, device_names):
    """
    Function to build a plotly line plot from device data from one or more
    devices.
    
    Parameters
    ----------
    device_data: pandas dataframe
        only including colemns 'Timestamp' and data to plot
    
    device_names: list
        ordered list of names, one per dataframe
    """
    data = list()
    for i, path in enumerate(device_data):
        for column in list(path.columns):
            if not column == 'Timestamp':
                data.append(hv.Scatter(path, kdims=['Timestamp'], vdims=[column
                            ]))
    layout = hv.Layout(data).cols(1)
    return(layout)
    

def linechart(df, plot_label, line=True, full=False):
    """
    Function to build a linechart and export a PNG and an SVG of the image.
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe to plot
        
    plot_label : string
        plot title
        
    line : boolean
        True for lineplot, False for scatterplot
        
    full : boolean
        True for ylim=[0, 1], False for ylim=[0, 3×max(mad)
        
    Returns
    -------
    plotted : boolean
        True if data plotted, False otherwise
    
    Outputs
    -------
    inline plot
    """
    try:
        start = min(df.index.values)
    except:
        print("End of data.")
        return False
    stop = max(df.index.values)
    print("Plotting...")
    print(plot_label)
    fig = plt.figure(figsize=(10, 8), dpi=75)
    plt.rcParams['agg.path.chunksize'] = 10000
    ax = fig.add_subplot(111)
    ax.set_ylabel('unit cube normalized vector length')
    mad_values = []
    for i, device in enumerate(list(df.columns)):
        if device.startswith('normalized'):
            d2 = device[25:]
        else:
            d2 = device
        plot_line = df[[device]].dropna()
        mp = mad(plot_line)
        if mp > 0:
            print(mp)
            mad_values.append(mp)
        else:
            mp = plot_line.std()[0]
            if mp > 0:
                print(mp)
                mad_values.append(mp)
            else:
                print(max(plot_line[[device]]))
                mad_values.append(max(plot_line[[device]]))
        label = d2
        for c in color_key:
            if c in d2 or d2 in c:
                cmap = color_key[c]
            else:
                cmap = "#000000"
        if line:
            ax.plot_date(x=plot_line.index, y=plot_line, alpha=0.5,
                         label=label, marker="", linestyle="solid",
                         color=cmap)
        else:
            ax.plot_date(x=plot_line.index, y=plot_line, alpha=0.5,
                         label=label, marker="o", linestyle="None",
                         color=cmap)
        ax.legend(loc='best', fancybox=True, framealpha=0.5)
    try:
        ylim = max(mad_values)
    except:
        ylim = 0
    if full or ylim == 0:
        ax.set_ylim([0, 1])
    else:
        try:
            ax.set_ylim([0, 3 * ylim])
        except:
            ax.set_ylim([0, 1])
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    plt.suptitle(plot_label)
    plt.xticks(rotation=65)
    plt.show()
    return True


def plplot(device_data, device_names):
    """
    Function to build a plotly line plot from device data from one or more
    devices.
    
    Parameters
    ----------
    device_data: list of pandas dataframes
        only including columns 'Timestamp' and data to plot
    
    device_names: list
        ordered list of names, one per dataframe
    """
    data = list()
    for i, path in enumerate(device_data):
        for column in list(path.columns):
            if not column == 'Timestamp':
                data.append(Scatter(x=path['Timestamp'], y=path[column], name=
                            ': '.join([device_names[i], column])))
    return(data)


def rolling_window(a, window):
    # http://wichita.ogs.ou.edu/documents/python/xcor.py
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)  


def xcorr(x,y):
    """
    c=xcor(x,y)
    Fast implementation to compute the normalized cross correlation where x and
    y are 1D numpy arrays
    x is the timeseries
    y is the template time series
    returns a numpy 1D array of correlation coefficients, c"
  
    The standard deviation algorithm in numpy is the biggest slow down in this
    method.  
    The issue has been identified hopefully they make improvements.

    http://wichita.ogs.ou.edu/documents/python/xcor.py
    """
    N = len(x)
    M = len(y)
    meany = np.nanmean(y)
    stdy = np.nanstd(np.asarray(y))
    tmp = rolling_window(x,M)
    c = np.nansum((y-meany)*(tmp-np.reshape(np.nanmean(tmp,-1),(N-M+1,1))),-1
        )/(M*np.nanstd(tmp,-1)*stdy)
    return(c)

# ============================================================================
if __name__ == '__main__':
    pass