#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chart_data.py

Functions to organize data into charts from which we can comare our devices.

Created on Mon Apr 10 17:25:39 2017

@author: jon.clucas
"""
from config import placement_dir
import os, pandas as pd

def main():
    location = pd.read_csv(os.path.join(placement_dir, 'location.csv'))
    person = pd.read_csv(os.path.join(placement_dir, 'person.csv'))
    wrist = pd.read_csv(os.path.join(placement_dir, 'wrist.csv'))
    print(pd.merge(person, wrist, how="outer", on="﻿Timestamp"))

# ============================================================================
if __name__ == '__main__':
    main()