"""
This script looks at the catalog from Frank (2014) and
transform the LFE detections for each template into a list of times and magnitudes
"""

import numpy as np
import pickle
import pandas as pd

from datetime import datetime
from math import floor

def write_catalog_Ducellier(filename, threshold, tbegin):
    """
    Function to write the LFE catalog into a file suitable
    to be read and analyzed with the R package PtProcess

    Input:
        type filename = string
        filename = Name of the LFE family
        type threshold = Pandas dataframe
        threshold = Cut-off cross-correlation to clean the catalog
        type tbegin = tuple of 6 integers
        tbegin = Beginning time of the catalog
                 (year, month, day, hour, minute, second)
    Output:
        type df = pandas dataframe
        df = Time and magnitude of LFEs
    """
    # Open LFE catalog
    namedir = '../data/Ducellier_2022/catalogs/' + filename
    namefile = namedir + '/catalog_2004_2011.pkl'
    df = pickle.load(open(namefile, 'rb'))

    # Filter LFEs
    df = df.loc[df['cc'] * df['nchannel'] >= threshold['threshold_perm'].iloc[i]]

    time = np.zeros(len(df))
    magnitude = np.zeros(len(df))

    # Loop on LFEs
    for j in range(0, len(df)):
        myYear = df['year'].iloc[j]
        myMonth = df['month'].iloc[j]
        myDay = df['day'].iloc[j]
        myHour = df['hour'].iloc[j]
        myMinute = df['minute'].iloc[j]
        mySecond = int(floor(df['second'].iloc[j]))
        myMicrosecond = int(1000000.0 * (df['second'].iloc[j] - mySecond))
        t = datetime(myYear, myMonth, myDay, myHour, myMinute, mySecond, \
            myMicrosecond)
        dt = t - tbegin
        time[j] = dt.days + (dt.seconds + dt.microseconds * 0.000001) / 86400.0
    df = pd.DataFrame(data={'time':time, 'magnitude':magnitude})
    return df

if __name__ == '__main__':

    # List of LFE families
    templates = np.loadtxt('../data/Plourde_2015/templates_list.txt', \
        dtype={'names': ('name', 'family', 'lat', 'lon', 'depth', 'eH', \
        'eZ', 'nb'), \
             'formats': ('S13', 'S3', np.float, np.float, np.float, \
        np.float, np.float, np.int)}, \
        skiprows=1)

    # Threshold for filtering the catalog
    threshold = pd.read_csv('../data/Ducellier_2022/threshold_cc.txt', sep=r'\s{1,}', header=None, engine='python')
    threshold.columns = ['family', 'threshold_FAME', 'threshold_perm']

    # Beginning of the period we are looking at
    tbegin = datetime(2004, 1, 1, 0, 0, 0)
   
    # Loop on LFE families
    for i in range(0, np.shape(templates)[0]):
        filename = templates[i][0].astype(str)
        df = write_catalog_Ducellier(filename, threshold, tbegin)
        output = '../data/Ducellier_2022/catalogs/{}.txt'.format(filename)
        tfile = open(output, 'w')
        tfile.write(df.to_string())
        tfile.close()
