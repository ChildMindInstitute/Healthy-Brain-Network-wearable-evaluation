#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_normalized_ppgs.py

Functions to plot normalized photoplethysmography data against one another.

Created on Thu Apr 20 12:45:28 2017

@author: jon.clucas
"""
from annotate_range import annotation_line
from chart_data import write_csv
from config import organized_dir, placement_dir
from datetime import datetime
from plot_normalized_vector_lengths import cross_correlate
import numpy as np, os, pandas as pd, matplotlib.pyplot as plt, sys

column_dict = {'nW':'E4 combined red and green', 'infrared':'Wavelet infrared',
               'red':'Wavelet red'}
color_key = {'nW':'green', 'infrared':'black', 'red':'red'}

def define_plot_data():
    """
    Define a list of (label, person, devices, start, stop) tuples to plot.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    plot_data_tuples : list of 4-tuples (string, string, list of strings,
                       datetime, datetime)
        list of tuples to plot. Each tuple is a list of plot title, devices, 
        start time, and stop time
    """
    plot_data_tuples = [("E4 and Wavelet on same non-dominant wrist", "Arno", [
                       "E4", "Wavelet"], datetime(2017, 4, 7, 18, 30),
                       datetime(2017, 4, 8, 18, 30)), (
                       "E4 and Wavelet on same non-dominant wrist, zoomed",
                       "Arno", ["E4", "Wavelet"], datetime(2017, 4, 7, 19, 00),
                       datetime(2017, 4, 7, 19, 30))]
    return(plot_data_tuples)

def main():
    for plot_data_tuple in define_plot_data():
        plot_label = plot_data_tuple[0]
        plot_person = plot_data_tuple[1]
        plot_devices = plot_data_tuple[2]
        plot_start = plot_data_tuple[3]
        plot_stop = plot_data_tuple[4]
        # try:
        build_plot(plot_label, plot_person, plot_devices, plot_start,
                   plot_stop)
        #except:
        #    e = sys.exc_info()[0]
        #    print(" ".join([plot_label, "failed: ", str(e)]))
            
            
def build_plot(plot_label, plot_person, plot_devices, plot_start, plot_stop):
    """
    Function to build specified lineplot.
    
    Parameters
    ----------
    plot_label : string
        plot title
        
    plot_person : string
        person being plotted
        
    plot_devices : list of strings
        list of devices to plot
        
    plot_start : datetime
        plot start time
    
    plot_stop : datetime
        plot stop time
        
    Returns
    -------
    None
    
    Outputs
    -------
    png
       PNG image file (via linechart())
    
    svg
       SVG image file (via linechart())
    """
    csv_df = pd.DataFrame()
    for device in plot_devices:
        ppg_path = os.path.join(organized_dir, 'photoplethysmograph', '.'.join(
                   [device, 'csv']))
        if os.path.exists(ppg_path):
            print(" ".join(["Loading", ppg_path]))
            device_df = pd.read_csv(ppg_path, parse_dates=['Timestamp'],
                        infer_datetime_format=True, low_memory=False)
            device_df.sort_values(by='Timestamp', inplace=True)
            device_df.dropna(inplace=True)
            person_device_df = device_df.loc[(device_df['Timestamp'] >= 
                               plot_start) & (device_df['Timestamp'] <=
                               plot_stop)].copy()
            del device_df
            write_csv(person_device_df, plot_person, 'photoplethysmograph',
                      device)
            if csv_df.empty:
                csv_df = person_device_df.copy()
            else:
                csv_df = pd.merge(csv_df, person_device_df, how='outer', on=[
                         'Timestamp'])
    if len(csv_df) > 0:
        print(str(list(csv_df.columns)))
        person_df_to_csv = csv_df.set_index("Timestamp")
        person_df_to_csv.dropna(axis=[0, 1], how='all', inplace=True)
        print(str(list(person_df_to_csv.columns)))
        linechart(person_df_to_csv, plot_label, plot_person)
        
def demean(s):
    """
    Function to demean a series.
    
    Paramaters
    ----------
    s : pandas series
        series to demean
        
    Returns
    -------
    ds : pandas series
        series recentered on 0
    """
    s.apply(lambda x: pd.to_numeric(x))
    s.dropna(inplace=True)
    nonzero = s.iloc[s.nonzero()[0]]
    print(nonzero)
    return(nonzero - nonzero.mean())

def normalize(s):
    """
    Function to normalize a demeaned series from [-1:1]
    
    Parameters
    ----------
    s : pandas series
        series to normalize
        
    Returns
    -------
    ns : pandas series
        series with new minimum -1 and new maximum +1
    """
    print(s)
    absmax = max(max(s), abs(min(s)))
    return(s/absmax)

def linechart(df, plot_label, plot_person):
    """
    Function to build a linechart and export a PNG and an SVG of the image.
    
    Parameters
    ----------
    df : pandas dataframe
        dataframe to plot
        
    plot_label : string
        plot title
        
    plot_person : string
        wearer (for annotations)
        
    Returns
    -------
    None
    
    Outputs
    -------
    png file
        png of lineplot
    
    svg file
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
    print(plot_label)
    svg_out = os.path.join(organized_dir, 'photoplethysmograph', "_".join([
              'normalized', '.'.join(['_'.join(plot_label.split(
              ' ')), 'svg'])]))
    png_out = ''.join([svg_out.strip('svg'), 'png'])
    fig = plt.figure(figsize=(10, 8), dpi=75)
    plt.rcParams['agg.path.chunksize'] = 10000
    ax = fig.add_subplot(111)
    ax.set_ylabel('unit cube normalized vector length')
    annotations_a = {}
    annotations_b = {}
    annotation_y = 0.04
    plot_log = w_log.loc[(w_log['wearer'] == plot_person) & (w_log['start'] >= 
                         start) & (w_log['stop'] <= stop)].copy()
    for row in plot_log.itertuples():
        if row[4] not in annotations_a:
            annotations_a[row[4]] = row[1]
            annotations_b[row[4]] = row[2]
    esses = []
    for light in list(df.columns):
        if light == "nW":
            plot_line = normalize(df.loc[:, light].dropna())
            ax.plot_date(x=plot_line.index, y=plot_line, color=color_key[
                         light], alpha=0.5, label=column_dict[light], marker=
                         "", linestyle="solid")
        else:
            plot_line = normalize(demean(df.loc[:, light].dropna()))
            ax.plot_date(x=plot_line.index, y=plot_line, color=color_key[
                         light], alpha=0.5, label=column_dict[light], marker=
                         "o", linestyle="None")
        esses.append(pd.Series(plot_line, name=light, index=
                     plot_line.index))
    ax.legend(loc='best', fancybox=True, framealpha=0.5)
    for annotation in annotations_a:
        annotation_line(ax, annotations_a[annotation], annotations_b[
                        annotation], annotation, annotation_y)
        annotation_y += 0.08
    ax.set_ylim([0, 1])
    plt.suptitle(plot_label)
    plt.xticks(rotation=65)
    for image in [svg_out, png_out]:
        print("".join(["Saving ", image]))
        fig.savefig(image)
        print("Saved.")
    plt.close()
    while len(esses) > 2:
        for i, s in enumerate(esses):
            if i < len(esses):
                cross_correlate(s, esses[-1], os.path.join(organized_dir,
                                'photoplethysmograph',"_".join([s.name, esses[
                                -1].name, 'correlation.csv'])))
        del esses[-1]
    cross_correlate(esses[0], esses[1], os.path.join(organized_dir,
                    'photoplethysmograph',"_".join([esses[0].name, esses[1
                    ].name, 'correlation.csv'])))

# ============================================================================
if __name__ == '__main__':
    main()