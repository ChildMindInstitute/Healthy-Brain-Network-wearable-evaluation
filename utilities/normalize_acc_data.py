#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_acc_data.py

Functions to normalize accelerometery data to a single number from wearable
devices with Linux time-series index columns and additional value columns.
Unless otherwise specified, timestamps are stored as datetime.
Actigraphy values calculated as √((x/√((max(x))² + (max(y))² + (max(z))²))² +
(y/√((max(x))² + (max(y))² + (max(z))²))² + (z/√((max(x))² + (max(y))² + (max(z
))²))²), i.e. vector length normalized to a unit cube.

@author: jon.clucas
"""

from datetime import datetime
from dateutil import parser
from math import sqrt
import numpy as np, os, pandas as pd

axes = ['x', 'y', 'z']

def main():
    pass

def normalize(df, scale=None):
    """
    function to calculate vector length normalized to a unit cube (i.e., √((x/√
    ((max(x))² + (max(y))² + (max(z))²))² + (y/√((max(x))² + (max(y))² + (max(z
    ))²))² + (z/√((max(x))² + (max(y))² + (max(z))²))²))

    Parameters
    ----------
    df : pandas dataframe
        dataframe with ['x', 'y', 'z'] columns to normalize

    scale : numeric or None
        maximum possible absolute value of dataframe's current scale
        if None, calculated from data

    Returns
    -------
    df : pandas dataframe
        dataframe with ['normalized_vector_length'] column added
    """
    cols = ['x', 'y', 'z']
    if not scale:
        scale = max([max(df[ax].max(), abs(df[ax].min())) for ax in cols])        
    unit = np.float64(sqrt(3*(scale**2)))
    try:
        df['Timestamp'] = df['Timestamp'].map(parser.parse, 'ignore')
    except:
        pass
    df['normalized_vector_length'] = np.sqrt((df['x'] / unit) ** 2 + (df['y'] /
                                     unit) ** 2 + (df['z'] / unit) ** 2)
    return(df)

# ============================================================================
if __name__ == '__main__':
    main()