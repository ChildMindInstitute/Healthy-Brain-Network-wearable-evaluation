#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chart_data.py

Functions to organize data into charts from which we can compare
our devices.

Created on Mon Apr 10 17:25:39 2017

@author: jon.clucas
"""
from annotate_range import annotation_line
from astropy.stats import median_absolute_deviation as mad
from config import devices, organized_dir, placement_dir, test_urls
from datetime import datetime, timedelta
from matplotlib.dates import DateFormatter
from organize_wearable_data import datetimedt, datetimeint
from plot_normalized_vector_lengths import baseshift_and_renormalize
from utilities.fetch_data import fetch_check_data, fetch_data, fetch_hash
import json, numpy as np, os, pandas as pd, matplotlib.pyplot as plt

with open(os.path.join('./line_charts/device_colors.json')) as fp:
    color_key = json.load(fp)
facecolors = {'left':'lightblue', 'right':'pink'}

def main():
    people_df = getpeople()
    people_w = pd.unique(people_df.person_wrist)
    for pw in people_w:
        buildperson(people_df, pw)

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
    diff      = data1 - data2                   # Difference between data1 and data2
    md        = np.mean(diff)                   # Mean of the difference
    sd        = np.std(diff, axis=0)            # Standard deviation of the difference

    plt.scatter(mean, diff, *args, **kwargs)
    plt.axhline(md,           color='gray', linestyle='--')
    plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
        
def buildperson(df, pw):
    """
    Function to build plottable csv file for each available person-wrist-device
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe with columns ["person_wrist", "device", "start", "stop"]
        detailing which device was worn by whom when
        
    pw : 2-tuple (person_name : string, wrist : string)
        indentifier for csv to build
        
    Returns
    -------
    None
    
    Outputs
    -------
    person_wrist.csv : csv file
        csv file formatted for plotting
    """
    person, starts, stops = get_startstop(df, pw)
    person_df = df.loc[df['person_wrist'] == pw].copy()
    person_df.reset_index(drop=True, inplace=True)
    devices = pd.unique(person_df.device)
    print(person, end=": ")
    print(devices)
    csv_df = pd.DataFrame(columns=['device', 'Timestamp', 'x', 'y', 'z'])
    for device in devices:
        person_device_dfs = []
        for sti, start in enumerate(starts):
            stop = stops[sti]
            acc_path = os.path.join(organized_dir, 'accelerometer', '.'.join([
                       device, 'csv']))
            if os.path.exists(acc_path):
                device_df = pd.read_csv(acc_path)
                device_df.sort_values(by='Timestamp', inplace=True)
                try:
                    device_df[['Timestamp']] = device_df.Timestamp.map(lambda
                                               x: datetimeint(str(x)))
                except:
                    pass
                person_device_df = device_df.loc[(device_df['Timestamp'] >=
                                   start) & (device_df['Timestamp'] <= stop)
                                   ].copy()
                del device_df
                person_device_df[['Timestamp'
                                  ]] = person_device_df.Timestamp.map(lambda x:
                                       datetimedt(x))
                print(device, end=" ranges: x=(")
                print(min(person_device_df.x), end=", ")
                print(max(person_device_df.x), end="), y=(")
                print(min(person_device_df.y), end=", ")
                print(max(person_device_df.y), end="), z=(")
                print(min(person_device_df.z), end=", ")
                print(max(person_device_df.z), end=")\n")
                person_device_df['device'] = device
                person_device_df = person_device_df[['device', "Timestamp",
                                   "x", "y", "z"]]
                person_device_dfs.append(person_device_df)
        person_device_csv_df = pd.DataFrame(columns=['device', 'Timestamp',
                               'x', 'y', 'z'])
        for person_device_df in person_device_dfs:
            person_device_csv_df = pd.concat([person_device_csv_df,
                                   person_device_df])
        csv_df = pd.concat([csv_df, person_device_csv_df])
        write_csv(person_device_csv_df, person, 'accelerometer', device)
    if len(csv_df) > 0:
        csv_dfs = split_datetimes(csv_df)
        for df_to_csv in csv_dfs:
            df_to_csv.reset_index(inplace=True)
            try:
                d = df_to_csv.Timestamp[0].to_datetime().date()
            except:
                d = df_to_csv.Timestamp[0].date()
            person_df_to_csv = df_to_csv.pivot(index="Timestamp", columns=
                               "device")
            person_df_to_csv.sortlevel(inplace=True)
            linechart_pw(person_df_to_csv, pw, d)
            write_csv(person_df_to_csv, person, 'accelerometer', d=d)
            
def df_devices(devices, sensor, start, stop, hashes={}):
    """
    Function to calculate rolling correlations between two sensor data streams.
    
    Parameters
    ----------
    devices : list of (subdirectory, device) 2-tuples or list of strings
        each string is the name of one of the two devices to compare
        
    sensor : string
        the sensor to compare
        
    start : datetime
        beginning of time to compare
        
    stop : datetime
        end of time to compare
        
    hashes : dictionary
        dictionary of cached datafile hashes
        
    Returns
    -------
    df : pandas dataframe
        merged dataframe with a column per device
    """
    suffix = '.csv'
    s = []
    df = pd.DataFrame()
    sub = ''
    for i, device in enumerate(devices):
        if sensor.startswith('acc'):
            sub = 'normalized_vector_length'
            acc_sub = '_'.join([device, 'acc'])
            if not acc_sub in hashes:
                try:
                    fetch_check_data(acc_sub, test_urls()[acc_sub], hashes,
                                     cache_directory='./sample_data',
                                     append='.csv', verbose=True)
                except:
                    hashes[acc_sub] = fetch_hash(fetch_data(test_urls()[acc_sub],
                                      os.path.join('./sample_data', acc_sub), '.csv'))
            s.append(pd.read_csv(fetch_check_data(acc_sub, test_urls()[acc_sub], hashes,
                     cache_directory='./sample_data', append='.csv', verbose=True),
                     usecols=['Timestamp', 'normalized_vector_length'],
                     parse_dates=['Timestamp'], infer_datetime_format=True, index_col=0,
                     dtype='float'))
            if device[1] == 'ActiGraph':
                s[i].index = pd.Series(s[i].index).apply(lambda x: x - timedelta(microseconds=1000))
        elif sensor == 'ppg':
            ppg = '_'.join([device, sensor])
            if not ppg in hashes:
                try:
                    fetch_check_data(device, test_urls()[ppg], hashes, cache_directory='sample_data', append='.csv',
                                     verbose=True)
                except:
                    hashes[ppg] = fetch_hash(fetch_data(test_urls()[ppg], os.path.join('./sample_data', ppg), '.csv'))
            if "Wavelet" in ppg:
                s.append(pd.read_csv(fetch_check_data(ppg, test_urls()[ppg], hashes,
                         cache_directory='sample_data', append='.csv', verbose=True), parse_dates=['Timestamp'],
                         infer_datetime_format=True, low_memory=False, na_values=[0, '0']))
            else:
                s.append(pd.read_csv(fetch_check_data(ppg, test_urls()[ppg], hashes,
                         cache_directory='sample_data', append='.csv', verbose=True), parse_dates=['Timestamp'],
                         infer_datetime_format=True, low_memory=False))
            s[i].set_index('Timestamp', inplace=True)
            s[i] = s[i][(s[i] != 0).all(1)]
            sub = list(s[i].columns)[0]
        s[i] = s[i].loc[(s[i].index >= start) & (s[i].index <= stop)].copy()
    if len(s) > 1:
        df = s[0].merge(s[1], how='outer', left_index=True, right_index=True,
             suffixes=(''.join(['_', devices[0]]), ''.join(['_', devices[1]])))
        for i in range(2, len(s), 1):
            df = df.merge(s[i], how='outer', left_index=True, right_index=True,
                 suffixes=('', ''.join(['_', devices[i]])))
    df = df.apply(pd.to_numeric, errors='coerce')
    return(df)

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
        acc_sub = '_'.join([device[0], 'acc', 'quicktest'])
        if not acc_sub in acc_hashes:
            try:
                fetch_check_data(acc_sub, test_urls()[acc_sub], acc_hashes, cache_directory='./sample_data',
                                 append='.csv', verbose=True)
            except:
                acc_hashes[acc_sub] = fetch_hash(fetch_data(test_urls()[acc_sub], os.path.join('./sample_data',
                                      acc_sub), '.csv'))
        s.append(pd.read_csv(fetch_check_data(acc_sub, test_urls()[acc_sub], acc_hashes,
                 cache_directory='./sample_data', append='.csv', verbose=True),
                 usecols=['Timestamp', 'normalized_vector_length'],
                 parse_dates=['Timestamp'], infer_datetime_format=True))
        s[i] = s[i].loc[(s[i]['Timestamp'] >= start) & (s[i]['Timestamp'] <= stop)].copy()
        s[i] = baseshift_and_renormalize(s[i])
        if device[1] == 'ActiGraph':
            s[i][['Timestamp']] = s[i].Timestamp.apply(lambda x: x - timedelta(microseconds
                        =1000))
        s[i].set_index('Timestamp', inplace=True)
    df = s[0].merge(s[1], left_index=True, right_index=True, suffixes=(''.join([
         '_', devices[0][1]]), ''.join(['_', devices[1][1]])))
    for i in range(2, len(s), 1):
        df = df.merge(s[i], left_index=True, right_index=True, suffixes=('', ''.join(['_', devices[i][1]])))
    return(df)

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
    annotations_a = {}
    annotations_b = {}
    annotation_y = 0.04
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
        if "GENEActiv" in device:
            label = "GENEActiv"
        elif device == "Actigraph":
            label = "ActiGraph"
        else:
            label = d2
        """
        if device == "Wavelet":
            ax.plot_date(x=plot_line.index, y=plot_line, color=color_key[
                         device], alpha=0.5, label=label, marker="o",
                         linestyle="None")
        else:
        """
        if line:
            ax.plot_date(x=plot_line.index, y=plot_line, alpha=0.5, label=label, marker="", linestyle=
                             "solid")
        else:
            ax.plot_date(x=plot_line.index, y=plot_line, alpha=0.5, label=label, marker="o", linestyle=
                             "None")
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
            
def linechart_pw(df, pw, d=None):
    """
    Function to build a linechart of the given (person, wrist) and export an
    SVG of the image.
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe to plot
    
    pw : 2-tuple (person_name : string, wrist : string)
        identifiers for plot
        
    d : date or None
        date
        
    Returns
    -------
    None
    
    Outputs
    -------
    person_wrist.svg : svg file
        svg of lineplot
    """
    start = min(df.index.values)
    stop = max(df.index.values)
    w_log = pd.read_csv(os.path.join(placement_dir, 'wearable_log.csv'),
            parse_dates={'start':['start date', 'start time'], 'stop':[
            'end date', 'end time']})
    w_log.dropna(inplace=True)
    w_log['start'] = pd.to_datetime(w_log.start, errors="coerce")
    w_log['stop'] = pd.to_datetime(w_log.stop, errors="coerce")
    print("Plotting...")
    print(pw, end=" ")
    if d:
        print(d)
        svg_out = os.path.join(organized_dir, 'accelerometer', "_".join([
                  d.isoformat(), pw[0], '.'.join([pw[1], 'svg'])]))
    else:
        print('\n')
        svg_out = os.path.join(organized_dir, 'accelerometer', "_".join([pw[0], 
              '.'.join([pw[1], 'svg'])]))
    png_out = ''.join([svg_out.strip('svg'), 'png'])
    fig, axes = plt.subplots(figsize=(10, 8), dpi=75, nrows=3, ncols=1,
                sharex=True)
    i = 0
    annotations_a = {}
    annotations_b = {}
    annotation_y = -2
    pw_log = w_log.loc[(w_log['wearer'] == pw[0]) & (w_log['start'] >= start) &
             (w_log['stop'] <= stop)].copy()
    for row in pw_log.itertuples():
        if row[4] not in annotations_a:
            annotations_a[row[4]] = row[1]
            annotations_b[row[4]] = row[2]
    for axis in ['x', 'y', 'z']:
        plot_df = df.xs(axis, level=0, axis=1)
        for device in list(plot_df.columns):
            plot_line = plot_df[[device]].dropna()
            if "GENEActiv" in device:
                label = "GENEActiv"
            else:
                label = device
            axes[i].plot_date(x=plot_line.index, y=plot_line, color=
                              color_key[device], alpha=0.5, label=label,
                              marker="", linestyle="solid")
        if i == 0:
            axes[i].legend(loc='best', fancybox=True, framealpha=0.5)
        if i == 2:
            for annotation in annotations_a:
                annotation_line(axes[2], annotations_a[annotation],
                                annotations_b[annotation], annotation,
                                annotation_y)
                annotation_y += 0.75
        i = i + 1
    if d:
        plt.suptitle(''.join(['–'.join([d.isoformat(), (d + timedelta(days=
                     1)).isoformat()]), ' ', pw[0], ', ', pw[1], ' wrist'])
                     )
    else:
        plt.suptitle(''.join([pw[0], ', ', pw[1], ' wrist']))
    plt.xticks(rotation=65)
    for image in [svg_out, png_out]:
        print("".join(["Saving ", image]))
        fig.savefig(image, facecolor=facecolors[pw[1]])
        print("Saved.")
    plt.close()
    
def getpeople():
    """
    Function to organize timestamps by people and wrists.
    
    Parameters
    ----------
    None

    Returns
    -------
    people_df : pandas dataframe
        dataframe with columns ["person_wrist", "device", "start", "stop"]
        detailing which device was worn by whom when
    """
    # location = pd.read_csv(os.path.join(placement_dir, 'location.csv'))
    person = pd.read_csv(os.path.join(placement_dir, 'person.csv'))
    wrist = pd.read_csv(os.path.join(placement_dir, 'wrist.csv'))
    person_wrist = pd.DataFrame()
    pw0 = pd.merge(person, wrist, how="outer", on="﻿Timestamp", suffixes=(
          '_person', '_wrist'))
    person_wrist[['Timestamp']] = pw0[["﻿Timestamp"]]
    person_wrist['Actigraph'] = tuple(zip(pw0.Actigraph_person,
                                pw0.Actigraph_wrist))
    person_wrist['E4'] = tuple(zip(pw0.E4_person, pw0.E4_wrist))
    person_wrist['Embrace'] = tuple(zip(pw0.Embrace_person, pw0.Embrace_wrist))
    person_wrist['GENEActiv_black'] = tuple(zip(pw0.ix[:,
                                      'GeneActiv (black)_person'], pw0.ix[:,
                                      'GeneActiv (black)_wrist']))
    person_wrist['GENEActiv_pink'] = tuple(zip(pw0.ix[:,
                                      'GeneActiv (pink)_person'], pw0.ix[:,
                                      'GeneActiv (pink)_wrist']))
    person_wrist['Wavelet'] = tuple(zip(pw0.Biostrap_person, pw0.Biostrap_wrist
                              ))
    del pw0
    chart_wrists = []
    times = []
    for v in list(pd.unique(person_wrist.values.ravel())):
        if(type(v)) == tuple and v != (np.nan, np.nan):
            chart_wrists.append(v)
        elif(type(v) == int):
            times.append(v)
    chart_wrists.sort()
    times.sort()
    start_stop = {}
    for i, t in enumerate(times):
        if i < len(times) - 1:
            start_stop[t] = times[i + 1]
    people = []
    for pw in chart_wrists:
        for device in devices:
            for i, item in enumerate(person_wrist.ix[:, device]):
                if item == pw:
                    people.append([pw, device, person_wrist.loc[i, 'Timestamp'
                                  ],  start_stop[person_wrist.loc[i,
                                  'Timestamp']]])
    people_df = pd.DataFrame(people, columns=["person_wrist", "device",
                "start", "stop"])
    people_df[['start']] = people_df.start.map(lambda x:
                           datetime.fromtimestamp(int(x)))
    people_df[['stop']] = people_df.stop.map(lambda x:
                          datetime.fromtimestamp(int(x)))
    return(people_df)
    
def get_startstop(df, person):
    """
    Function to get overall start and stop times for each person-wrist.
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe of at least ["person_wrist", "start", "stop"]
        
    person : string
        person-wrist to get start and stop for

    Returns
    -------
    person_start_stop : 3-tuple (string, list of datetimes, list of datetimes)
        person-wrist, start times, stop times (times in Linux time format)
    """
    starts = []
    stops = []
    ssdt = "%Y-%m-%d %H:%M:%S"
    for i, item in enumerate(df.person_wrist):
        if item == person:
            starts.append(datetimeint(df.loc[i, 'start'].strftime(ssdt), ssdt))
            stops.append(datetimeint(df.loc[i, 'stop'].strftime(ssdt), ssdt))
    return(person, starts, stops)

def rolling_window(a, window):
    # http://wichita.ogs.ou.edu/documents/python/xcor.py
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def split_datetimes(df):
    """
    Function to split datetimes into dates and times.
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe with "Timestamp" column
        
    Returns
    -------
    dtdfs : list of pandas dataframes
        dataframes of 1 day or less "Timestamp" columns
    """
    dtdf = df.copy()
    dtdf.reset_index(inplace=True)
    start = min(dtdf.Timestamp)
    final = max(dtdf.Timestamp)
    stop = min(start + timedelta(hours=24), final)
    if stop >= final:
        return([dtdf])
    else:
        dtdfs = []
        while(stop < final):
            print(' : '.join([str(start), str(stop), str(final)]))
            dtdfs.append(dtdf.loc[(dtdf.Timestamp >= start) & (
                         dtdf.Timestamp <= stop)].copy())
            start = stop
            stop = min(start + timedelta(hours=24), final)
        print(' : '.join([str(start), str(stop), str(final)]))
        dtdfs.append(dtdf.loc[(dtdf.Timestamp >= start) & (dtdf.Timestamp <=
                     stop)].copy())
    return(dtdfs)

def write_csv(df, person, sensor, device=None, d=None, normal=None):
    """
    Function to write a csv for a person-wrist for a particular sensor.
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe to write to csv
        
    person : 2-tuple (string, string)
        person_name, wrist
        
    sensor : string
        type of sensor data included in df
    
    device : string or None
        device name
        
    d : datetime.date or None
        date  
    
    Returns
    -------
    df : pandas dataframe
        unchanged dataframe
        
    Output
    ------
    csv : csv file
        csv copy of dataframe stored in
        organized_dir/`sensor`/`person_name`_`wrist`_`sensor`.csv
    """
    if normal:
        csv_out = os.path.join(organized_dir, sensor, '.'.join(['_'.join([
                  normal, '_'.join(person.split(' '))]), 'csv']))
    elif device:
        if d:
            csv_out = os.path.join(organized_dir, sensor, "_".join([
                      d.isoformat(), person[0], person[1], '.'.join([device,
                      'csv'])]))
        else:
            csv_out = os.path.join(organized_dir, sensor, "_".join([person[0],
                      person[1], '.'.join([device, 'csv'])]))
    else:
        if d:
            csv_out = os.path.join(organized_dir, sensor, "_".join([
                      d.isoformat(), person[0], '.'.join([person[1], 'csv'])]))
        else:
            csv_out = os.path.join(organized_dir, sensor, "_".join([person[0],
                      '.'.join([person[1], 'csv'])]))
    if not os.path.exists(os.path.dirname(csv_out)):
        os.makedirs(os.path.dirname(csv_out))
    print(''.join(["Saving ", csv_out]))
    df.to_csv(csv_out, index=False)
    return(df)

def xcorr(x,y):
  """
  c=xcor(x,y)
  Fast implementation to compute the normalized cross correlation where x and y are 1D numpy arrays
  x is the timeseries
  y is the template time series
  returns a numpy 1D array of correlation coefficients, c"
  
  The standard deviation algorithm in numpy is the biggest slow down in this method.  
  The issue has been identified hopefully they make improvements.

  http://wichita.ogs.ou.edu/documents/python/xcor.py
  """
  N=len(x)
  M=len(y)
  meany=np.nanmean(y)
  stdy=np.nanstd(np.asarray(y))
  tmp=rolling_window(x,M)
  c=np.nansum((y-meany)*(tmp-np.reshape(np.nanmean(tmp,-1),(N-M+1,1))),-1)/(M*np.nanstd(tmp,-1)*stdy)

  return c

# ============================================================================
if __name__ == '__main__':
    main()