"""
This script looks at the catalog from Sweet (2014) and
transform the LFE detections for each template into a list of times and magnitudes
"""

import numpy as np
import pickle
import pandas as pd

from datetime import datetime
from scipy.io import loadmat

from date import matlab2ymdhms

def write_catalog_Sweet(n, tbegin):
    """
    Function to write the LFE catalog into a file suitable
    to be read and analyzed with the R package PtProcess

    Input:
        type n = int
        n = Index of the LFE template
        type tbegin = tuple of 6 integers
        tbegin = Beginning time of the catalog
                 (year, month, day, hour, minute, second)
    Output:
        type df = pandas dataframe
        df = Time and magnitude of LFEs
    """
    # Get the time of LFE detections
    data = loadmat('../data/Sweet_2014/catalogs/LFE' + str(n) + 'catalog.mat')
    if (n <= 4):
        LFEtime = data['peakTimes'][0]
    else:
        LFEtime = data['peakTimes']
    time = np.zeros(np.shape(LFEtime)[0])
    magnitude = np.zeros(np.shape(LFEtime)[0])
    # Loop on LFEs
    for i in range(0, np.shape(LFEtime)[0]):
        if (n <= 4):
            (myYear, myMonth, myDay, myHour, myMinute, mySecond, \
                 myMicrosecond) = matlab2ymdhms(LFEtime[i], False)
        else:
            (myYear, myMonth, myDay, myHour, myMinute, mySecond, \
                 myMicrosecond) = matlab2ymdhms(LFEtime[i][0], False)
        t = datetime(myYear, myMonth, myDay, myHour, myMinute, mySecond, \
            myMicrosecond)
        dt = t - tbegin
        time[i] = dt.days + (dt.seconds + dt.microseconds * 0.000001) / 86400.0
    df = pd.DataFrame(data={'time':time, 'magnitude':magnitude})
    return df

if __name__ == '__main__':

    # Number of LFE families
    nf = 9

    # Beginning of the period we are looking at
    tbegin = datetime(2006, 10, 1, 0, 0, 0)

    # Loop on templates
    for n in range(0, nf):
        df = write_catalog_Sweet(n + 1, tbegin)
        filename = 'LFE' + str(n + 1)
        output = '../data/Sweet_2014/catalogs/{}.txt'.format(filename)
        tfile = open(output, 'w')
        tfile.write(df.to_string())
        tfile.close()
