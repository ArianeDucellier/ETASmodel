"""
This script looks at the catalog from Frank (2014) and
transform the LFE detections for each template into a list of times and magnitudes
"""

import numpy as np
import pickle
import pandas as pd

from datetime import datetime
from math import floor

def write_catalog_Shelly(LFEtime, filename, tbegin):
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
        myHour = data['hr'].iloc[j]
        myMinute = data['min'].iloc[j]
        mySecond = int(floor(data['sec'].iloc[j]))
        myMicrosecond = int(1000000.0 * (data['sec'].iloc[j] - mySecond))
        t = datetime(myYear, myMonth, myDay, myHour, myMinute, mySecond, \
            myMicrosecond)
        dt = t - tbegin
        time[j] = dt.days + (dt.seconds + dt.microseconds * 0.000001) / 86400.0
    df = pd.DataFrame(data={'time':time, 'magnitude':magnitude})
    return df

if __name__ == '__main__':

    # Read the LFE file
    LFEtime = pd.read_csv('../data/Shelly_2017/jgrb52060-sup-0002-datas1.txt', \
        delim_whitespace=True, header=None, skiprows=2)
    LFEtime.columns = ['year', 'month', 'day', 's_of_day', 'hr', 'min', \
        'sec', 'ccsum', 'meancc', 'med_cc', 'seqday', 'ID', 'latitude', \
        'longitude', 'depth', 'n_chan']
    LFEtime['ID'] = LFEtime.ID.astype('category')
    families = LFEtime['ID'].cat.categories.tolist()

    # Beginning of the period we are looking at
    tbegin = datetime(2001, 4, 6, 0, 0, 0)

    # Loop on LFE families
    for i in range(0, len(families)):
        df = write_catalog_Shelly(LFEtime, families[i], tbegin)
        output = '../data/Shelly_2017/catalogs/{}.txt'.format(str(families[i]))
        tfile = open(output, 'w')
        tfile.write(df.to_string())
        tfile.close()
