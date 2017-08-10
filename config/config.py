#!/usr/bin/env python3
"""
config/config.py

Configurations for HBN Wearable Analysis.

Authors:
    - Jon Clucas, 2017  <jon.clucas@childmind.org>

Copyright ©2017, Apache v2.0 License
"""

# dictionary of rawurls by device by sensor
rawurls = {'accelerometer': {'ActiGraph wGT3X-BT':
                             'https://osf.io/rjhv6/?action=download&version=3',
                             'Empatica E4':
                             'https://osf.io/kc2xz/?action=download&version=5',
                             'Wavelet Wristband':
                             'https://osf.io/8zpkn/?action=download&version=2',
                             'GENEActiv Original (black)':
                             'https://osf.io/df7zq/?action=download&version=2',
                             'GENEActiv Original (pink)':
                            'https://osf.io/yjc7s/?action=download&version=2'},
           'photoplethysmograph': {'Empatica E4':
                             'https://osf.io/v3ad6/?action=download&version=3',
                                   'Wavelet Wristband':
                            'https://osf.io/c5b9z/?action=download&version=1'},
           'electrodermal activity': {'Empatica E4':
                            'https://osf.io/53vwz/?action=download&version=2'},
           'gyroscopy': {},
           'electrocardiography': {'ActiGraph wGT3X-BT':
                             'https://osf.io/cde76/?action=download&version=1',
                                   'Empatica E4':
                            'https://osf.io/be2p8/?action=download&version=2'},
           'light': {'ActiGraph wGT3X-BT':
                             'https://osf.io/b2xtm/?action=download&version=1',
                     'GENEActiv Original (black)':
                             'https://osf.io/c5by9/?action=download&version=1',
                     'GENEActiv Original (pink)':
                            'https://osf.io/b75g8/?action=download&version=1'},
           'temperature': {'Empatica E4':
                             'https://osf.io/38pyj/?action=download&version=3',
                           'GENEActiv Original (black)':
                             'https://osf.io/hync2/?action=download&version=1',
                           'GENEActiv Original (pink)':
                            'https://osf.io/vhd8w/?action=download&version=1'},
           'raw_accelerometer': {'ActiGraph wGT3X-BT':
                             'https://osf.io/va9kc/?action=download&version=1',
                                 'GENEActiv Original (black)':
                             'https://osf.io/y5cz7/?action=download&version=1',
                                 'GENEActiv Original (pink)':
                            'https://osf.io/q4bwx/?action=download&version=1'},
          'accelerometer quicktest': {'ActiGraph wGT3X-BT':
                             'https://osf.io/h3aem/?action=download&version=1',
                             'GENEActiv Original (black)':
                             'https://osf.io/j5rcu/?action=download&version=1',
                             'GENEActiv Original (pink)':
                            'https://osf.io/yxgzt/?action=download&version=1'}}


def raw_urls(sensors=None):
    """
    Return the URLs for raw data for a given sensor or list of sensors.

    Parameter
    ---------
    sensors : string or list or None, default None
        The sensor(s) to supply URLs for. If None, return all sensors.

    Returns
    -------
    urls: dictionary
        A dictionary with sensor keys and device / sensor key / value values.
    """
    if not sensors:
        return(rawurls)
    urls = dict()
    if isinstance(sensors, str):
        if sensors in rawurls:
            return({sensors: rawurls[sensors]})
    else:
        try:
            for sensor in sensors:
                urls = {**urls, **raw_urls(sensor)}
        except:
            print(" ".join(["Error loading raw", str(sensors), "data"]))
    return(urls)

def sensorlist():
    """
    Return a list of sensors.

    Parameters
    ----------
        None

    Returns
    -------
    sensors: list
        A list of strings representing sensors.
    """
    return(['accelerometer', 'photoplethysmograph', 'electrodermal activity',
           'gyroscopy', 'electrocardiography', 'light', 'temperature'])
