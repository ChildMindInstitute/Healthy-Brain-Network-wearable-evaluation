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
short_dir = os.path.abspath('/Users/jon.clucas/wearables/quicktest')

sensor_dictionary = {'Actigraph':['accelerometer', 'ecg', 'light'],
                    'Embrace':['accelerometer', 'gyro', 'eda', 'temp'],
                    'E4':['accelerometer', 'ppg', 'eda', 'temp'],
                    'Wavelet':['accelerometer', 'gyro', 'ppg'],
                    'GENEActiv':['accelerometer', 'light', 'temp']}
   
def test_urls(): 
    urls = {}
    urls['A_acc_quicktest'] = 'https://osf.io/h3aem/?action=download&version=1'
    urls['G1_acc_quicktest'] = ('https://osf.io/j5rcu/?action=download&version'
                               '=1')
    urls['G2_acc_quicktest'] = ('https://osf.io/yxgzt/?action=download&version'
                               '=1')
    
    urls['ActiGraph_acc'] = ('https://osf.io/aqj9g/?action=download&version'
                            '=2')
    urls['E4_acc'] = ('https://osf.io/asfn5/?action=download&version'
                     '=3')
    urls['GENEActiv_black_acc'] = ('https://osf.io/r64e2/?action=download&version'
                                  '=1')
    urls['GENEActiv_pink_acc'] = ('https://osf.io/7kdv3/?action=download&version'
                                  '=1')
    urls['Wavelet_acc'] = ('https://osf.io/b5gm4/?action=download&version'
                         '=1')
    
    urls['ActiGraph_hr'] = ('https://osf.io/cde76/?action=download&version'
                           '=1')
    urls['E4_hr'] = ('https://osf.io/be2p8/?action=download&version'
                    '=2')
    
    urls['E4_ppg'] = 'https://osf.io/v3ad6/?action=download&version=3'
    urls['Wavelet_ppg'] = 'https://osf.io/c5b9z/?action=download&version=1'
    
    return(urls)
    
cmi_colors = ["#0067a0", "#919d9d", "#00c1d5", "#b5bd00", "#a31c3f", "#ea234b",
              "#eeae30", "#f2cd32", "#4db789", "#90d9b9", "#404341", "#e4e4e4",
              "#090e3c", "#242a6a", "#97e2ef", "#f9e28a", "#d3da5f"]