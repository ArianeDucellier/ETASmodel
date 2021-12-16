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
data = np.loadtxt('models_Chestler_2017/simulated_d_PtProcess.txt')
data_minus = np.loadtxt('models_Chestler_2017/simulated_dminus_PtProcess.txt')

# Open file of families
families = pd.read_csv('models_Chestler_2017/families.txt', header=None)

# Map
longitude = np.zeros(nt)
latitude = np.zeros(nt)
d = np.zeros(nt)
dminus = np.zeros(nt)

# Loop on templates
for n in range(0, nt):
    filename = LFEs[n]['name'][0][0].replace(' ', '')

    # Get index
    index = families.index[families[0]==filename].tolist()[0]

    # Get the location of the LFE families
    longitude[n] = LFEs[n]['lon'][0][0][0]
    latitude[n] = LFEs[n]['lat'][0][0][0]

    d[n] = np.nanmean(data[:, index])
    dminus[n] = np.nanmean(data_minus[:, index])
    # If there are values, plot
    if np.isnan(d[n]) == False:
        params = {'legend.fontsize': 24, \
                  'xtick.labelsize':24, \
                  'ytick.labelsize':24}
        pylab.rcParams.update(params)
        plt.figure(1, figsize=(20, 8))
        ax1 = plt.subplot2grid((1, 2), (0, 0))
        plt.hist(data[:, index], bins=[0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])
        plt.xlabel('Fractional differencing parameter', fontsize=24)
        plt.title('Family ' + filename, fontsize=24)
        ax2 = plt.subplot2grid((1, 2), (0, 1))
        plt.hist(data_minus[:, index], bins=[-0.2, -0.15, -0.1, -0.05, 0.0, 0.05, 0.1, 0.15, 0.2])
        plt.xlabel('Lower limit of 95% confidence interval', fontsize=24)
        plt.title('Family ' + filename, fontsize=24)
        plt.tight_layout()
        plt.savefig('models_Chestler_2017/PtProcess/' + filename + '.eps', format='eps')
        plt.close(1)

# Plot all families
params = {'legend.fontsize': 24, \
          'xtick.labelsize':24, \
          'ytick.labelsize':24}
pylab.rcParams.update(params)
plt.figure(1, figsize=(20, 8))
ax1 = plt.subplot2grid((1, 2), (0, 0))
plt.hist(data.flatten(), bins=[0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4])
plt.xlabel('Fractional differencing parameter', fontsize=24)
plt.title('All Families', fontsize=24)
ax2 = plt.subplot2grid((1, 2), (0, 1))
plt.hist(data_minus.flatten(), bins=[-0.2, -0.15, -0.1, -0.05, 0.0, 0.05, 0.1, 0.15, 0.2])
plt.xlabel('Lower limit of 95% confidence interval', fontsize=24)
plt.title('All families', fontsize=24)
plt.tight_layout()
plt.savefig('models_Chestler_2017/simulated_d_PtProcess.eps', format='eps')
plt.close(1)

# Create dataframe
output = pd.DataFrame(data={'longitude': longitude, 'latitude': latitude, 'd':d})
tfile = open('models_Chestler_2017/PtProcess.txt', 'w')
tfile.write(output.to_string(index=False, header=False))
tfile.close()
