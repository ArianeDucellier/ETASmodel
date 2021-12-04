"""
Python script to read the gif and residuals files
and plot them along with the LFE catalog
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

tbegin = 0
tend = 852

# Loop on templates
for n in range(0, nt):
    filename = LFEs[n]['name'][0][0].replace(' ', '')

    # Get the catalog
    df = pd.read_csv('../data/Chestler_2017/catalogs/' + filename + '.txt', sep='\s+')
    X = np.zeros(tend - tbegin)
    # Loop on LFES
    for j in range(0, len(df)):
        t = df['time'].iloc[j]
        index = int(t - tbegin)
        X[index] = X[index] + 1

    # Get the GIF
    gif = np.loadtxt('models_Chestler_2017/' + filename + '/gif.txt')

    # Get the residuals
    res = np.loadtxt('models_Chestler_2017/' + filename + '/res.txt')

    # Start figure
    fig = plt.figure(1, figsize=(16, 8))
    params = {'xtick.labelsize':20,
              'ytick.labelsize':20}
    pylab.rcParams.update(params)

    # Plot catalog
    ax1 = plt.subplot2grid((1, 2), (0, 0))
    plt.stem(0.5 + np.arange(tbegin, tend), X, 'k-', markerfmt=' ', basefmt=' ')
    plt.xlim([0, len(X)])
    plt.xlabel('Time (days)', fontsize=24)
    ax1.set_ylabel('Number of LFEs', color = 'black', fontsize=24)

    # Plot GIF
    ax2 = ax1.twinx()
    plt.plot(np.arange(tbegin, tend + 1), gif, 'r-')
    ax2.set_ylabel('GIF', color = 'red', fontsize=24)
    plt.title('Family {} ({:d} LFEs)'.format(filename, int(np.sum(X))), fontsize=24)

    # Plot residuals
    ax3 = plt.subplot2grid((1, 2), (0, 1))
    plt.axhline(0, color='black')
    plt.plot(np.arange(1, len(res) + 1), res - np.arange(1, len(res) + 1), 'ko')
    plt.xlabel('Index of LFE', fontsize=24)
    plt.ylabel('Residual - Index', fontsize=24)
    plt.title('Goodness of fit', fontsize=24)

    # End figure
    plt.tight_layout()
    plt.savefig('models_Chestler_2017/' + filename + '/gif_residuals_PtProcess.eps', format='eps')
    plt.close(1)
