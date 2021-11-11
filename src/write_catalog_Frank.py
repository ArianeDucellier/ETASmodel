"""
This script looks at the catalog from Frank (2014) and
transform the LFE detections for each template into a list of times and magnitudes
"""

import numpy as np
import pickle
import pandas as pd

from datetime import datetime
from math import floor

def write_catalog_Frank(LFEtime, filename, tbegin):
    """
    Function to write the LFE catalog into a file suitable
    to be read and analyzed with the R package PtProcess

    Input:
        type LFEtime = panda DataFrame
        LFEtime = Times of LFE detections
        type filename = int
        filename = Name of the LFE family
        type tbegin = tuple of 6 integers
        tbegin = Beginning time of the catalog
                 (year, month, day, hour, minute, second)
    Output:
        type df = pandas dataframe
        df = Time and magnitude of LFEs
    """
    # Get the data for the family
    data = LFEtime.loc[LFEtime['ID'] == filename]
    time = np.zeros(data.shape[0])
    magnitude = np.zeros(data.shape[0])
    # Loop on LFEs
    for j in range(0, data.shape[0]):
        myYear = data['year'].iloc[j]
        myMonth = data['month'].iloc[j]
        myDay = data['day'].iloc[j]
        myHour = data['hour'].iloc[j]
        myMinute = data['minute'].iloc[j]
        mySecond = int(floor(data['second'].iloc[j]))
        myMicrosecond = int(1000000.0 * (data['second'].iloc[j] - mySecond))
        t = datetime(myYear, myMonth, myDay, myHour, myMinute, mySecond, \
            myMicrosecond)
        dt = t - tbegin
        time[j] = dt.days + (dt.seconds + dt.microseconds * 0.000001) / 86400.0
    df = pd.DataFrame(data={'time':time, 'magnitude':magnitude})
    return df

if __name__ == '__main__':

    # Read the LFE file
    LFEtime = pd.read_csv('../data/Frank_2014/frank_jgr_2014_lfe_catalog.txt', \
        delim_whitespace=True, header=None, skiprows=0)
    LFEtime.columns = ['year', 'month', 'day', 'hour', 'minute', 'second', \
        'ID', 'latitude', 'longitude', 'depth']
    LFEtime['ID'] = LFEtime.ID.astype('category')
    families = LFEtime['ID'].cat.categories.tolist()

    # Beginning of the period we are looking at
    tbegin = datetime(2005, 1, 15, 0, 0, 0)

    # Loop on LFE families
    for i in range(0, len(families)):
        df = write_catalog_Frank(LFEtime, families[i], tbegin)
        output = '../data/Frank_2014/catalogs/{}.txt'.format(str(families[i]))
        tfile = open(output, 'w')
        tfile.write(df.to_string())
        tfile.close()
