#!/usr/bin/env python3
"""
data/osf.py

Functions for fetching data from OSF.

Authors:
    - Jon Clucas, 2017  <jon.clucas@childmind.org>

Copyright ©2017, Apache v2.0 License
"""

import os
import sys

hwa = (os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
if hwa not in sys.path:
    sys.path.append(hwa)

from config import config
from utilities import fetch_data

data = dict()
urls = config.raw_urls()
for sensor, device in urls.items():
    for device, url in device.items():
        data[sensor] = {device:None}
        data[sensor][device] = fetch_data.fetch_data(url)