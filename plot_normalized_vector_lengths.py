#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_normalized_vector_lengths.py

Functions to plot normalized vector lengths of actigraphy data against one
another.

@author: jon.clucas
"""
from annotate_range import annotation_line
from config import organized_dir, placement_dir
from datetime import datetime
from matplotlib.dates import DateFormatter
import json, numpy as np, os, pandas as pd, matplotlib.pyplot as plt

with open(os.path.join('./line_charts/device_colors.json')) as fp:
    color_key = json.load(fp)

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

    plot_data_tuples = [(
                       "GENEActiv and Wavelet on same dominant wrist",
                       "Arno", ["GENEActiv_pink", "Wavelet"], datetime(2017,
                       4, 6, 15, 45), datetime(2017, 4, 7, 14, 8)), (
                       "ActiGraph and Wavelet on same dominant wrist",
                       "Arno", ["Actigraph", "Wavelet"], datetime(2017, 4, 6,
                       15, 53), datetime(2017, 4, 7, 15)), (
                       "ActiGraph and Wavelet on same dominant wrist, zoomed",
                       "Arno", ["Actigraph", "Wavelet"], datetime(2017,
                       4, 6, 15, 53), datetime(2017, 4, 7, 15)),
                       ("ActiGraph and Wavelet on same dominant wrist, zoom"
                       "ed", "Arno", ["Actigraph", "Wavelet"], datetime(2017,
                       4, 6, 15, 53), datetime(2017, 4, 7, 15)),
                       (("E4 and Wavelet on same dominant wrist, zoomed"),
                       "Arno", ["E4", "Wavelet"], datetime(2017, 4, 9, 7),
                       datetime(2017, 4, 9, 9, 45)), (
                       "GENEActiv and Wavelet on same dominant wrist",
                       "Arno", ["GENEActiv_pink", "Wavelet"], datetime(2017,
                       4, 6, 15, 45), datetime(2017, 4, 7, 14, 8)), (
                       "GENEActiv and Wavelet on same dominant wrist, zoomed",
                       "Arno", ["GENEActiv_pink", "Wavelet"], datetime(2017,
                       4, 6, 15, 53), datetime(2017, 4, 7, 15)),
                       ("GENEActiv, ActiGraph and Wavelet on same dominant wr"
                       "ist", "Arno", ["GENEActiv_pink", "Actigraph", "Wavelet"
                       ], datetime(2017, 4, 6, 15, 45), datetime(2017, 4, 7,
                       14, 8)), ("GENEActiv, ActiGr"
                       "aph and Wavelet on same dominant wrist, zoomed",
                       "Arno", ["GENEActiv_pink", "Actigraph", "Wavelet"],
                       datetime(2017, 4, 7, 7, 15), datetime(2017, 4, 7, 7, 45)
                       )]
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
        """
        except:
            e = sys.exc_info()
            print(" ".join([plot_label, "failed: ", str(e)]))
        """

def baseshift_and_renormalize(data, sub='normalized_vector_length'):
    """
    Function to shift base to 0 and max value to 1
    
    Parameters
    ----------
    data : pandas dataframe
        dataframe to baseshift and renormalize
        
    sub : string
        name of column to normalize
        
    Returns
    -------
    data : pandas dataframe
        baseshifted, renormalized dataframe
    """
    baseline = np.nanmedian(data[sub])
    data[sub] = data[sub].map(
                                       lambda x: max(x - baseline, 0))
    datamax = max(data[sub])
    data[sub] = data[sub] / datamax
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
            print(" ".join(["Loading ", acc_path]))
            device_df = pd.read_csv(acc_path, parse_dates=['Timestamp'],
                        infer_datetime_format=True)
            device_df.sort_values(by='Timestamp', inplace=True)
            device_df.dropna(inplace=True)
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
            person_device_shifted = baseshift_and_renormalize(
                                    person_device_shifted)
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
        shifted_df.reset_index(inplace=True)
        person_df_to_csv = csv_df.pivot(index="Timestamp", columns="device")
        person_df_to_csv.sortlevel(inplace=True)
        shifted_df_to_csv = shifted_df.pivot(index="Timestamp", columns=
                            "device")
        shifted_df_to_csv.sortlevel(inplace=True)
        linechart(person_df_to_csv, plot_label, plot_person)
        linechart(shifted_df_to_csv, ' '.join([plot_label, 'baseline adjusted'
                  ]), plot_person)
        write_csv(person_df_to_csv, plot_label, 'accelerometer', normal=
                  "normalized_vector_length")
        write_csv(shifted_df_to_csv, ' '.join([plot_label, 'baseline adjusted'
                  ]), 'accelerometer', normal="normalized_vector_length")
                    
def cross_correlate(s1, s2, filepath):
    """
    Function to calculate and save pairwise correlations.
    
    Parameters
    ----------
    s1, s2 : pandas series
        series to correlate
        
    filepath : string
        where to save result
    """
    corr = np.correlate(s1, s2)
    print(' '.join(['Saving', str(corr), 'to', filepath]))
    np.savetxt(filepath, corr, delimiter=',')

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
            annotations_a[row[4]] = row[1] if row[1] >= start else start
            annotations_b[row[4]] = row[2] if row[2] <= stop else stop
    plot_df = df.xs('normalized_vector_length', level=0, axis=1)
    print(plot_df.head())
    esses = []
    for device in list(plot_df.columns):
        plot_line = plot_df[[device]].dropna()
        esses.append(pd.Series(plot_line.iloc[:,0], name=device, index=
                     plot_line.index))
        if "GENEActiv" in device:
            label = "GENEActiv"
        elif device == "Actigraph":
            label = "ActiGraph"
        else:
            label = device
        """
        if device == "Wavelet":
            ax.plot_date(x=plot_line.index, y=plot_line, color=color_key[
                         device], alpha=0.5, label=label, marker="o",
                         linestyle="None")
        else:
        """
        ax.plot_date(x=plot_line.index, y=plot_line, color=color_key[
                         device], alpha=0.5, label=label, marker="", linestyle=
                         "solid")
        ax.legend(loc='best', fancybox=True, framealpha=0.5)
    for annotation in annotations_a:
        try:
            annotation_line(ax, annotations_a[annotation], annotations_b[
                            annotation], annotation, annotation_y)
            annotation_y += 0.08
        except:
            print(annotation)
    ax.set_ylim([0, 1])
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    plt.suptitle(plot_label)
    plt.xticks(rotation=65)
    for image in [svg_out, png_out]:
        print("".join(["Saving ", image]))
        fig.savefig(image)
        print("Saved.")
    plt.close()
    mads = []
    for s in esses:
        mads.append(np.nanmedian(abs(s - np.nanmedian(s))))
    while len(esses) > 2:
        for i, s in enumerate(esses):
            if i < len(esses):
                cross_correlate(s, esses[-1], os.path.join(organized_dir,
                                'accelerometer',"_".join([s.name, esses[-1
                                ].name, 'correlation.csv'])))
        del esses[-1]
    cross_correlate(esses[0], esses[1], os.path.join(organized_dir,
                    'accelerometer',"_".join([esses[0].name, esses[1].name,
                    'correlation.csv'])))
    m = max(mads)
    fig = plt.figure(figsize=(10, 8), dpi=75)
    plt.rcParams['agg.path.chunksize'] = 10000
    ax = fig.add_subplot(111)
    plot_labelc = ''.join([plot_label, ', clipped to 3 MADs'])
    svg_outc = os.path.join(organized_dir, 'accelerometer', "_".join([
              'normalized_vector_length', '.'.join(['_'.join(plot_labelc.split(
              ' ')), 'svg'])]))
    png_outc = ''.join([svg_out.strip('svg'), 'png'])
    for device in list(plot_df.columns):
        plot_line = plot_df[[device]].dropna()
        if "GENEActiv" in device:
            label = "GENEActiv"
        elif device == "Actigraph":
            label = "ActiGraph"
        else:
            label = device
        """
        if device == "Wavelet":
            ax.plot_date(x=plot_line.index, y=plot_line, color=color_key[
                         device], alpha=0.5, label=label, marker="o",
                         linestyle="None")
        else:
        """
        ax.plot_date(x=plot_line.index, y=plot_line, color=color_key[
                         device], alpha=0.5, label=label, marker="", linestyle=
                         "solid")
        ax.legend(loc='best', fancybox=True, framealpha=0.5)
    for annotation in annotations_a:
        try:
            annotation_line(ax, annotations_a[annotation], annotations_b[
                            annotation], annotation, annotation_y)
            annotation_y += 0.08
        except:
            print(annotation)
    ax.set_ylim([0, 3 * m])
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d %H:%M'))
    plt.suptitle(plot_labelc)
    plt.xticks(rotation=65)
    for image in [svg_outc, png_outc]:
        print("".join(["Saving ", image]))
        fig.savefig(image)
        print("Saved.")
    plt.close()
    
def demean_and_normalize(data):
    """
    Function to shift base to 0 and max absolute value to 1
    
    Parameters
    ----------
    data : pandas dataframe
        dataframe to demean and renormalize
        
    Returns
    -------
    data : pandas dataframe
        baseshifted, renormalized dataframe
    """
    for column in list(data.columns):
        data[column] = data[column].astype('float', errors='ignore')
        baseline = np.nanmean(data[column])
        data[column] = data[column].map(
                       lambda x: x - baseline)
        datamax = np.nanmax(abs(data[column]))
        data[column] = data[column] / datamax
    return(data)

# ============================================================================
if __name__ == '__main__':
    main()