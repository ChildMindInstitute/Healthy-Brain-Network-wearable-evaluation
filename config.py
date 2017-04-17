#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py

Configuration for organize_wearable_data.py

Created on Fri Apr  7 17:35:28 2017

@author: jon.clucas
"""
import os

actigraph_dir = os.path.abspath('./ActiLife/Downloads')
e4_dir = os.path.abspath('./E4')
geneactiv_dir = os.path.abspath('./GENEActiv/Data/')
wavelet_dir = os.path.abspath('./Wavelet/RawData/')

devices = ['Actigraph', 'E4', 'Embrace', 'GENEActiv_black', 'GENEActiv_pink',
          'Wavelet']

organized_dir = os.path.abspath('./organized')
placement_dir = os.path.join(organized_dir, 'device_placement')

sensor_dictionary = {'Actigraph':['accelerometer', 'ecg', 'light'],
                    'Embrace':['accelerometer', 'gyro', 'eda', 'temp'],
                    'E4':['accelerometer', 'ppg', 'eda', 'temp'],
                    'Wavelet':['accelerometer', 'gyro', 'ppg'],
                    'GENEActiv':['accelerometer', 'light', 'temp']}