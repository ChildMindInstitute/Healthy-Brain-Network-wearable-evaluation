#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chart_data.py

Functions to organize data into charts from which we can comare our devices.

Created on Mon Apr 10 17:25:39 2017

@author: jon.clucas
"""
from config import devices, organized_dir, placement_dir
import numpy as np, os, pandas as pd

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
    print(person)
    print(pd.unique(person_df.device))
    for device in pd.unique(person_df.device):
        acc_path = os.path.join(organized_dir, 'accelerometer', '.'.join([
                   device, 'csv']))
        if os.path.exists(acc_path):
            print(acc_path)
    
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
        elif(type(v)) == int:
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
    return(pd.DataFrame(people, columns=["person_wrist", "device", "start",
           "stop"]))
    
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
    person_start_stop : 3-tuple (string, int, int)
        person-wrist, overall start time, overall stop time (times in Linux
        time format, as integers)
    """
    starts = []
    stops = []
    for i, item in enumerate(df.person_wrist):
        if item == person:
            starts.append(df.loc[i, 'start'])
            stops.append(df.loc[i, 'stop'])
    return(person, min(starts), max(stops))

# ============================================================================
if __name__ == '__main__':
    main()