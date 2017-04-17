#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chart_data.py

Functions to organize photoplethysmograph data into charts from which we can
compare our devices.

Created on Mon Apr 10 17:25:39 2017

@author: jon.clucas
"""
from config import organized_dir
from chart_data import getpeople, get_startstop, split_datetimes, write_csv
from organize_wearable_data import datetimedt, datetimeint
import os, pandas as pd, matplotlib.pyplot as plt

color_key = {'Wavelet red':'red', 'Wavelet infrared':'black',
             'E4 PPG (amplified ×1,000)':'green', 'Wavelet infrared filtered':
             'grey', 'Wavelet red filtered': 'pink'}
facecolors = {'left':'lightblue', 'right':'pink'}

def main():
    people_df = getpeople()
    people_w = pd.unique(people_df.person_wrist)
    for pw in people_w:
        buildperson(people_df, pw)
    
def buildperson(df, pw):
    """
    Function to build plottable csv file for each available person-wrist-device
    
    Paramters
    ---------
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
    person, start, stop = get_startstop(df, pw)
    person_df = df.loc[df['person_wrist'] == pw].copy()
    person_df.reset_index(drop=True, inplace=True)
    devices = pd.unique(person_df.device)
    print(person, end=": ")
    print(devices)
    csv_df = pd.DataFrame()
    for device in devices:
        ppg_path = os.path.join(organized_dir, 'photoplethysmograph', '.'.join(
                   [device, 'csv']))
        if os.path.exists(ppg_path):
            device_df = pd.read_csv(ppg_path)
            device_df.sort_values(by='Timestamp', inplace=True)
            try:
                device_df[['Timestamp']] = device_df.Timestamp.map(lambda x:
                                       datetimeint(str(x)))
            except:
                pass
            person_device_df = device_df.loc[(device_df['Timestamp'] >= start)
                               & (device_df['Timestamp'] <= stop)].copy()
            del device_df
            # write_csv(person_device_df, person, 'photoplethysmograph', device)
            person_device_df[['Timestamp']] = person_device_df.Timestamp.map(
                                              lambda x: datetimedt(x))
            if csv_df.empty:
                csv_df = person_device_df.copy()
            else:
                csv_df = pd.merge(csv_df, person_device_df, how='outer', on=[
                         'Timestamp'])
    if len(csv_df) > 0:
        csv_df = split_datetimes(csv_df)
        csv_df.sort_values(by=["Datestamp", "Timestamp"], inplace=True)
        for d in csv_df.Datestamp.unique():
            df_to_csv = csv_df.loc[(csv_df['Datestamp'] == d)]
            person_df_to_csv = df_to_csv.set_index("Timestamp")
            person_df_to_csv.dropna(axis=[0, 1], how='all', inplace=True)
            del person_df_to_csv['Datestamp']
            linechart(person_df_to_csv, pw, d)
            write_csv(person_df_to_csv, person, 'photoplethysmograph', d=d)
        
def linechart(df, pw, d=None):
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
    for filtered in ['red_filtered', 'infrared_filtered']:
        df = df.drop(filtered, axis=1, errors='ignore')
    if 'nW' in list(df.columns):
        df['nW'] = df['nW'].map(lambda x: x * 1000)
    sensors = ['photoplethysmograph']
    for sensor in sensors:
        print("Plotting...")
        print(pw, end=" ")
        if d:
            print(d, end=" ")
            svg_out = os.path.join(organized_dir, sensor, "_".join([
                      d.isoformat(), pw[0], '.'.join([pw[1], 'svg'])]))
        else:
            svg_out = os.path.join(organized_dir, sensor, "_".join([pw[0], 
                  '.'.join([pw[1], 'svg'])]))   
        fig = plt.figure(figsize=(10, 8), dpi=75)
        ax = fig.add_subplot(111)
        ax.set_ylabel('nW')
        for light in list(df.columns):
            if light == "nW":
                label = "E4 PPG (amplified ×1,000)"
            else:
                label = " ".join(["Wavelet", ' '.join(light.split('_'))])
            plot_line = df[[light]].dropna()
            ax.plot_date(x=plot_line.index, y=plot_line, color=color_key[
                         label], alpha=0.5, label=label, marker="", linestyle=
                         "solid")
        ax.legend(loc='best', fancybox=True, framealpha=0.5)
        if d:
            plt.suptitle(''.join([d.isoformat(), ' ', pw[0], ', ', pw[1],
                         ' wrist']), fontweight='bold')
        else:
            plt.suptitle(''.join([pw[0], ', ', pw[1], ' wrist']), fontweight=
                         'bold')
        plt.xticks(rotation=65)
        print("".join(["Saving ", svg_out]))
        fig.savefig(svg_out, facecolor=facecolors[pw[1]])
        plt.close()

# ============================================================================
if __name__ == '__main__':
    main()