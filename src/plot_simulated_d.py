"""
Script to plot distribution of fractional parameter
for simulated time series with the bayesianETAS parameters
"""

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.io import loadmat

# Get the names of the template detection files
data = loadmat('../data/Chestler_2017/LFEsAll.mat')
LFEs = data['LFEs']
nt = len(LFEs)

# Open file of simulated d
data = np.loadtxt('models_Chestler_2017/simulated_d.txt')

# Loop on templates
for n in range(0, nt):
    filename = LFEs[n]['name'][0][0].replace(' ', '')

    params = {'legend.fontsize': 24, \
              'xtick.labelsize':24, \
              'ytick.labelsize':24}
    pylab.rcParams.update(params)
    plt.figure(1, figsize=(10, 8))
    plt.hist(data[:, n], bins=[0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])
    plt.xlabel('Fractional differencing parameter', fontsize=24)
    plt.title('Family ' + filename, fontsize=24)
    plt.tight_layout()
    plt.savefig('models_Chestler_2017/bayesianETAS/' + filename + '.eps', format='eps')
    plt.close(1)

# Map
longitude = np.zeros(nt)
latitude = np.zeros(nt)
d = np.zeros(nt)

# Get the location of the LFE families
for n in range(0, nt):
    longitude[n] = LFEs[n]['lon'][0][0][0]
    latitude[n] = LFEs[n]['lat'][0][0][0]
    d[n] = np.mean(data[:, n])

# Create dataframe
output = pd.DataFrame(data={'longitude': longitude, 'latitude': latitude, 'd':d})
tfile = open('models_Chestler_2017/bayesianETAS.txt', 'w')
tfile.write(output.to_string(index=False, header=False))
tfile.close()
