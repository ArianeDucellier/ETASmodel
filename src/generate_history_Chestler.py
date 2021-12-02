"""
Script to generate event histories using the parameters
of the fitted ETAS model for each LFE family
"""

import numpy as np
import os
import pandas as pd

from math import floor
from scipy.io import loadmat

from simulate_ETAS_model import generate_history_marked

np.random.seed(0)

duration = 852
M0 = 0.0
N = 100

package = 'PrProcess'

data = loadmat('../data/Chestler_2017/LFEsAll.mat')
LFEs = data['LFEs']
NLFE = len(LFEs)

if package == 'bayesianETAS':
    df = pd.read_csv('models_Chestler_2017_bayesianETAS.txt', sep=' ')
else:
    df = pd.read_csv('models_Chestler_2017_PtProcess.txt', sep=' ')

for i in range(12, 13): #, NLFE):
    filename = LFEs[i]['name'][0][0].replace(' ', '')

    if package == 'bayesianETAS':

        # Get value of beta
        df0 = df.loc[df['family']==filename]
        df0.reset_index(inplace=True, drop=True)
        beta = df0['beta'].iloc[0]

        # Generate random values for ETAS parameters
        posterior = np.loadtxt('models_Chestler_2017/' + filename + '/posterior.txt')
        NS = np.shape(posterior)[0]
        indices = NS * np.random.uniform(0, 1, N)

        # Loop on synthetic event catalogs
        for j in range(0, N):
            index = int(floor(indices[j]))
            mu = posterior[index, 0]
            K = posterior[index, 1]
            alpha = posterior[index, 2]
            c = posterior[index, 3]
            p = posterior[index, 4]
            A = K * (p - 1) / c
            (times, magnitudes) = generate_history_marked(duration, mu, A, c, p, alpha, M0, beta)
            catalog = pd.DataFrame(data={'times': times, 'magnitudes': magnitudes})

            # Create drectory and save
            directory = 'models_Chestler_2017/' + filename + '/bayesianETAS/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            output_file = directory + '/catalog_' + str(j + 1) + '.txt'
            catalog.to_csv(output_file, sep=' ', index=False)


    else:

        df0 = df.loc[df['family']==filename]
        df0.reset_index(inplace=True, drop=True)

        # Get value of beta
        df_catalog = pd.read_csv('../data/Chestler_2017/catalogs/' + \
            filename + '.txt', sep='\s+')
        beta = 1.0 / df_catalog['magnitude'].mean()

        mu = df0['mu'].iloc[0]
        A = df0['A'].iloc[0]
        c = df0['c'].iloc[0]
        p = df0['p'].iloc[0]
        alpha = df0['alpha'].iloc[0]

        # Loop on synthetic event catalogs
        for j in range(0, N):
            (times, magnitudes) = generate_history_marked(duration, mu, A, c, p, alpha, M0, beta)
            catalog = pd.DataFrame(data={'times': times, 'magnitudes': magnitudes})

            # Create drectory and save
            directory = 'models_Chestler_2017/' + filename + '/PtProcess/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            output_file = directory + '/catalog_' + str(j + 1) + '.txt'
            catalog.to_csv(output_file, sep=' ', index=False)
