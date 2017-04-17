#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_all_sensors.py

Functions to plot all sensor outputs from each device.

Created on Mon Apr 17 11:00:32 2017

@author: jon.clucas
"""
from config import devices, organized_dir, sensor_dictionary
from datetime import datetime
from organize_wearable_data import datetimeint
import json, matplotlib.dates as mdates, os, pandas as pd, matplotlib.pyplot \
       as plt

with open(os.path.join('./line_charts/device_colors.json')) as fp:
    color_key = json.load(fp)

"""
-------------
Accelerometer
-------------
"""

def plot_acc(device):
    fp = os.path.join(organized_dir, 'accelerometer', '.'.join([device, 'csv'])
         )
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        df.sort_values(by='Timestamp', inplace=True)
        try:
            df[['Timestamp']] = df.Timestamp.map(lambda x: datetimeint(str(x)))
        except:
            pass
        plot_nd(df, fp, device, 'accelerometer')

"""
---------
Gyroscope
---------
"""
def plot_gyro(device):
    pass

"""
-------------------
Photoplethysmograph
-------------------
"""
def plot_ppg(device):
    fp = os.path.join(organized_dir, 'photoplethysmograph', '.'.join([device,
         'csv']))
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        df.sort_values(by='Timestamp', inplace=True)
        try:
            df[['Timestamp']] = df.Timestamp.map(lambda x: datetimeint(str(x)))
        except:
            pass
        if device == 'E4':
            plot_2d(df, fp, device, 'photoplethysmograph')
        else:
            plot_nd(df, fp, device, 'photoplethysmograph')

"""
------------------
Electrocardiograph
------------------
"""
def plot_ecg(device):
    pass

"""
----------------------
Electrodermal Activity
----------------------
"""
def plot_eda(device):
    pass

"""
-----
Light
-----
"""
def plot_light(device):
    pass

"""
-----------
Temperature
-----------
"""
def plot_temperature(device):
    pass

def main():
    # assign functions to sensors
    plot_fxn = {'accelerometer':plot_acc, 'gyro':plot_gyro, 'ppg':plot_ppg,
                'ecg':plot_ecg, 'eda':plot_eda, 'light':plot_light, 'temp':
                plot_temperature}
    
    for device in devices:
        print(device, end=": ")
        if 'GENEActiv' in device:
            for sensor in sensor_dictionary['GENEActiv']:
                plot_fxn[sensor](device)
        else:
            for sensor in sensor_dictionary[device]:
                plot_fxn[sensor](device)
                
def plot_2d(df, fp, device, sensor):
    """
    Function to create a lineplot and save svg and png versions of said plot.
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe to plot
        
    fp : string
        path to source file
        
    device : string
        device name
        
    sensor : string
        sensor type
        
    Returns
    -------
    None
    
    Outputs
    -------
    fp.svg : SVG
        scalable vector graphics file
        
    fp.png : PNG
        portable network graphics file
    """
    print("Plotting...")
    print(' '.join([device, sensor]))
    start = datetimeint(str(datetime(2017, 4, 3, 12)), '%Y-%m-%d %H:%M:%S')
    stop = datetimeint(str(datetime(2017, 4, 11)), '%Y-%m-%d %H:%M:%S')
    plot_df = df.loc[(df['Timestamp'] >= start) & (df['Timestamp'] <= stop)
              ].copy()
    fig = plt.figure(figsize=(10, 8), dpi=75)
    ax = fig.add_subplot(111)
    y = plot_df[[list(plot_df.columns)[1]]]
    ax.plot_date(x=plot_df.Timestamp, y=y, color=color_key[device], marker="",
                 linestyle="solid")
    plt.suptitle(' '.join([device, sensor]))
    fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.xticks(rotation=65)
    for image in ['svg', 'png']:
        fpout = ''.join([fp.strip('csv'), image])
        print("".join(["Saving ", fpout]))
        fig.savefig(fpout)
        print("Saved.")
    plt.close()

def plot_nd(df, fp, device, sensor):
    """
    Function to create a lineplot and save svg and png versions of said plot.
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe to plot
        
    fp : string
        path to source file
        
    device : string
        device name
        
    sensor : string
        sensor type
        
    Returns
    -------
    None
    
    Outputs
    -------
    fp.svg : SVG
        scalable vector graphics file
        
    fp.png : PNG
        portable network graphics file
    """
    print("Plotting...")
    print(' '.join([device, sensor]))
    start = datetimeint(str(datetime(2017, 4, 3, 12)), '%Y-%m-%d %H:%M:%S')
    stop = datetimeint(str(datetime(2017, 4, 11)), '%Y-%m-%d %H:%M:%S')
    plot_df = df.loc[(df['Timestamp'] >= start) & (df['Timestamp'] <= stop)
              ].copy()
    fig, axes = plt.subplots(figsize=(10, 8), dpi=75, nrows=len(list(
                plot_df.columns)[1:]), ncols=1, sharex=True)
    for i, axis in enumerate(list(plot_df.columns)[1:]):
        y = plot_df[[axis]]
        axes[i].plot_date(x=plot_df.Timestamp, y=y, color=color_key[device],
                          marker="", linestyle="solid")
        if len(axis) == 1:
            axes[i].set_ylabel(' '.join([axis, 'axis']))
        else:
            axes[i].set_ylabel(axis)
    plt.suptitle(' '.join([device, sensor]))
    fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.xticks(rotation=65)
    for image in ['svg', 'png']:
        fpout = ''.join([fp.strip('csv'), image])
        print("".join(["Saving ", fpout]))
        fig.savefig(fpout)
        print("Saved.")
    plt.close()

# ============================================================================
if __name__ == '__main__':
    main()