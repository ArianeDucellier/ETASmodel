"""
Script to generate event histories using the parameters
of the fitted ETAS model for each LFE family
"""

import numpy as np
import pandas as pd

from math import floor
from scipy.io import loadmat

from simulate_ETAS_model import generate_history_marked

np.random.seed(0)

duration = 852
M0 = 0.0
N = 100

data = loadmat('../data/Chestler_2017/LFEsAll.mat')
LFEs = data['LFEs']
NLFE = len(LFEs)

df = pd.read_csv('models_Chestler_2017.txt', sep=' ')

for i in range(0, NLFE):
    filename = LFEs[i]['name'][0][0].replace(' ', '')
    
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
        output_file = 'models_Chestler_2017/' + filename + '/catalog_' + str(j + 1) + '.txt'
        catalog.to_csv(output_file, sep=' ', index=False)
