#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_normalized_vector_lengths.py

Functions to plot normalized vector lengths of actigraphy data against one
another.

@author: jon.clucas
"""
from annotate_range import annotation_line
from chart_data import write_csv
from config import organized_dir, placement_dir
from datetime import datetime
from organize_wearable_data import datetimedt, datetimeint
import json, numpy as np, os, pandas as pd, matplotlib.pyplot as plt

with open(os.path.join('./line_charts/device_colors.json')) as fp:
    color_key = json.load(fp)
facecolors = {'left':'lightblue', 'right':'pink'}

def define_plot_data():
    """
    Define a list of (label, person, devices, start, stop) tuples to plot.
    
    Parameters
    ----------
    None
    
    Returns
    plot_data_tuples : list of 4-tuples (string, string, list of strings,
                       datetime, datetime)
        list of tuples to plot. Each tuple is a list of plot title, devices, 
        start time, and stop time
    """
    plot_data_tuples = [("GENEActiv and ActiGraph on same dominant wrist", 
                       "Arno", ["GENEActiv_pink", "Actigraph"], datetime(2017,
                       4, 6, 15, 45), datetime(2017, 4, 7, 14, 8)), (
                       "GENEActiv and Wavelet on same non-dominant wrist",
                       "Jon", ["GENEActive_black", "Wavelet"], datetime(2017,
                       4, 3, 18), datetime(2017, 4, 4, 17)), (
                       "GENEActiv and E4 on same non-dominant wrist", "Jon",
                       ["GENEActiv_black", "E4"], datetime(2017, 4, 4, 17),
                       datetime(2017, 4, 5, 13)), (
                       "ActiGraph and Wavelet on same non-dominant wrist",
                       "Jon", ["Actigraph", "Wavelet"], datetime(2017, 4, 5,
                       12), datetime(2017, 4, 6, 15)), (
                       "GENEActiv and ActiGraph on same dominant wrist, zoomed"
                       , "Arno", ["GENEActiv_pink", "Actigraph"], datetime(
                       2017, 4, 7, 9, 45), datetime(2017, 4, 7, 10, 15)), (
                       "GENEActiv and Wavelet on same non-dominant wrist, zoom\
                       ed", "Jon", ["GENEActive_black", "Wavelet"], datetime(
                       2017, 4, 4, 9, 45), datetime(2017, 4, 4, 10, 15)), (
                       "GENEActiv and E4 on same non-dominant wrist, zoomed",
                       "Jon", ["GENEActiv_black", "E4"], datetime(2017, 4, 5,
                       9, 45), datetime(2017, 4, 5, 10, 15)), (
                       "ActiGraph and Wavelet on same non-dominant wrist, zoom\
                       ed", "Jon", ["Actigraph", "Wavelet"], datetime(2017, 4,
                       6, 9, 45), datetime(2017, 4, 6, 10, 15))]
    return(plot_data_tuples)

def main():
    for plot_data_tuple in define_plot_data():
        plot_label = plot_data_tuple[0]
        plot_person = plot_data_tuple[1]
        plot_devices = plot_data_tuple[2]
        plot_start = plot_data_tuple[3]
        plot_stop = plot_data_tuple[4]
        build_plot(plot_label, plot_person, plot_devices, plot_start, plot_stop
                   )
        
def baseshift_and_renormalize(data):
    """
    Function to shift base to 0 and max value to 1
    
    Parameters
    ----------
    data : pandas dataframe
        dataframe to baseshift and renormalize
        
    Returns
    -------
    data : pandas dataframe
        baseshifted, renormalized dataframe
    """
    baseline = np.median(data['normalized_vector_length'])
    data['normalized_vector_length'] = data['normalized_vector_length'].map(
                                       lambda x: max(x - baseline, 0) if x <=
                                       baseline else x)
    datamax = max(data['normalized_vector_length'])
    data['normalized_vector_length'] = data['normalized_vector_length'] /     \
                                       datamax
    return(data)
        
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
    csv_df = pd.DataFrame(columns=['device', 'Timestamp',
             'normalized_vector_length'])
    shifted_df = pd.DataFrame(columns=['device', 'Timestamp',
             'normalized_vector_length'])
    for device in plot_devices:
        person_device_dfs = []
        person_device_shifteds = []
        acc_path = os.path.join(organized_dir, 'accelerometer', '.'.join([
                   '_'.join([device, 'normalized', 'unit']), 'csv']))
        if os.path.exists(acc_path):
            device_df = pd.read_csv(acc_path)
            device_df.sort_values(by='Timestamp', inplace=True)
            try:
                device_df[['Timestamp']] = device_df.Timestamp.map(lambda x:
                                           datetimedt(datetimeint(str(x),
                                           '%Y-%m-%d %H:%M:%S.%f')))
            except:
                device_df[['Timestamp']] = device_df.Timestamp.map(lambda x:
                                           datetimedt(datetimeint(str(x))))
            person_device_df = device_df.loc[(device_df['Timestamp'] >=
                               plot_start) & (device_df['Timestamp'] <= 
                               plot_stop)].copy()
            person_device_shifted = person_device_df.copy()
            del device_df
            for pddf in [person_device_df, person_device_shifted]:
                pddf['device'] = device
                pddf = pddf[['device', "Timestamp", "normalized_vector_length"]
                       ]
            person_device_dfs.append(person_device_df)
            baseshift_and_renormalize(person_device_df)
            person_device_shifteds.append(person_device_shifted)
        person_device_csv_df = pd.DataFrame(columns=['device', 'Timestamp',
                               'normalized_vector_length'])
        person_device_shifted_df = pd.DataFrame(columns=['device', 'Timestamp',
                               'normalized_vector_length'])
        for person_device_df in person_device_dfs:
            person_device_csv_df = pd.concat([person_device_csv_df,
                                   person_device_df])
        for person_device_shifted in person_device_shifteds:
            person_device_shifted_df = pd.concat([person_device_shifted_df,
                                   person_device_shifted])
        csv_df = pd.concat([csv_df, person_device_csv_df])
        shifted_df = pd.concat([shifted_df, person_device_shifted_df])
    if len(csv_df) > 0:
        csv_df.reset_index(inplace=True)
        person_df_to_csv = csv_df.pivot(index="Timestamp", columns="device")
        person_df_to_csv.sortlevel(inplace=True)
        shifted_df_to_csv = shifted_df.pivot(index="Timestamp", columns=
                            "device")
        linechart(person_df_to_csv, plot_label, plot_person)
        linechart(shifted_df_to_csv, ' '.join([plot_label, 'baseline adjusted'
                  ]), plot_person)
        write_csv(person_df_to_csv, plot_label, 'accelerometer', normal=
                  "normalized_vector_length")
        write_csv(shifted_df_to_csv, ' '.join([plot_label, 'baseline adjusted'
                  ]), 'accelerometer', normal="normalized_vector_length")

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
    svg_out = os.path.join(organized_dir, 'accelerometer', "_".join([
              'normalized_vector_length', '.'.join(['_'.join(plot_label.split(
              ' ')), 'svg'])]))
    png_out = ''.join([svg_out.strip('svg'), 'png'])
    fig = plt.figure(figsize=(10, 8), dpi=75)
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
    plot_df = df.xs('normalized_vector_length', level=0, axis=1)
    for device in list(plot_df.columns):
        plot_line = plot_df[[device]].dropna()
        if "GENEActiv" in device:
            label = "GENEActiv"
        elif device == "Actigraph":
            label = "ActiGraph"
        else:
            label = device
        ax.plot_date(x=plot_line.index, y=plot_line, color=color_key[device],
                     alpha=0.5, label=label, marker="", linestyle="solid")
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

# ============================================================================
if __name__ == '__main__':
    main()