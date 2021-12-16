"""
Script to compare the results from the package bayesianETAS
with maximum likelihood and bahesian framework
"""

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from math import log
from scipy.io import loadmat

data = loadmat('../data/Chestler_2017/LFEsAll.mat')
LFEs = data['LFEs']
NLFE = len(LFEs)

df = pd.read_csv('models_Chestler_2017_bayesianETAS.txt', sep=' ')

mu_MLE = np.zeros(NLFE)
A_MLE = np.zeros(NLFE)
c_MLE = np.zeros(NLFE)
p_MLE = np.zeros(NLFE)
alpha_MLE = np.zeros(NLFE)

mu_bayes = np.zeros(NLFE)
A_bayes = np.zeros(NLFE)
c_bayes = np.zeros(NLFE)
p_bayes = np.zeros(NLFE)
alpha_bayes = np.zeros(NLFE)

for i in range(0, NLFE):
    filename = LFEs[i]['name'][0][0].replace(' ', '')

    # Maximum likelihood
    df0 = df.loc[df['family']==filename]
    df0.reset_index(inplace=True, drop=True)
    mu_MLE[i] = df0['mu'].iloc[0]
    A_MLE[i] = df0['A'].iloc[0]
    c_MLE[i] = df0['c'].iloc[0]
    p_MLE[i] = df0['p'].iloc[0]
    alpha_MLE[i] = df0['alpha'].iloc[0]

    # Mean of posterior
    posterior = np.loadtxt('models_Chestler_2017/' + filename + '/posterior.txt')
    mu_bayes[i] = np.mean(posterior[:, 0])
    K = np.mean(posterior[:, 1])
    alpha_bayes[i] = np.mean(posterior[:, 2])
    c_bayes[i] = np.mean(posterior[:, 3])
    p_bayes[i] = np.mean(posterior[:, 4])
    A_bayes[i] = K * (p_bayes[i] - 1) / c_bayes[i]

params = {'xtick.labelsize':24,
          'ytick.labelsize':24}
pylab.rcParams.update(params)

# Plot mu
fig = plt.figure(1, figsize=(10, 10))
plt.plot([log(np.min(mu_bayes)), log(np.max(mu_bayes))], [log(np.min(mu_bayes)), log(np.max(mu_bayes))], 'r-')
plt.plot(np.log(mu_MLE), np.log(mu_bayes), 'ko')
plt.xlabel('Maximum likelihood', fontsize=24)
plt.ylabel('Sample mean of posterior', fontsize=24)
plt.title('Log(mu)', fontsize=24)
plt.tight_layout()
plt.savefig('models_Chestler_2017/comparison_mu.eps', format='eps')
plt.close(1)

# Plot A
fig = plt.figure(1, figsize=(10, 10))
plt.plot([log(np.min(A_bayes)), log(np.max(A_bayes))], [log(np.min(A_bayes)), log(np.max(A_bayes))], 'r-')
plt.plot(np.log(A_MLE), np.log(A_bayes), 'ko')
plt.xlabel('Maximum likelihood', fontsize=24)
plt.ylabel('Sample mean of posterior', fontsize=24)
plt.title('Log(A)', fontsize=24)
plt.tight_layout()
plt.savefig('models_Chestler_2017/comparison_A.eps', format='eps')
plt.close(1)

# Plot alpha
fig = plt.figure(1, figsize=(10, 10))
plt.plot([log(np.min(alpha_bayes)), log(np.max(alpha_bayes))], [log(np.min(alpha_bayes)), log(np.max(alpha_bayes))], 'r-')
plt.plot(np.log(alpha_MLE), np.log(alpha_bayes), 'ko')
plt.xlabel('Maximum likelihood', fontsize=24)
plt.ylabel('Sample mean of posterior', fontsize=24)
plt.title('Log(alpha)', fontsize=24)
plt.tight_layout()
plt.savefig('models_Chestler_2017/comparison_alpha.eps', format='eps')
plt.close(1)

# Plot c
fig = plt.figure(1, figsize=(10, 10))
plt.plot([np.min(c_bayes), np.max(c_bayes)], [np.min(c_bayes), np.max(c_bayes)], 'r-')
plt.plot(c_MLE[c_MLE < 1], c_bayes[c_MLE < 1], 'ko')
plt.xlabel('Maximum likelihood', fontsize=24)
plt.ylabel('Sample mean of posterior', fontsize=24)
plt.title('c', fontsize=24)
plt.tight_layout()
plt.savefig('models_Chestler_2017/comparison_c.eps', format='eps')
plt.close(1)

# Plot p
fig = plt.figure(1, figsize=(10, 10))
plt.plot([np.min(p_bayes), np.max(p_bayes)], [np.min(p_bayes), np.max(p_bayes)], 'r-')
plt.plot(p_MLE[p_MLE < 40], p_bayes[p_MLE < 40], 'ko')
plt.xlabel('Maximum likelihood', fontsize=24)
plt.ylabel('Sample mean of posterior', fontsize=24)
plt.title('p', fontsize=24)
plt.tight_layout()
plt.savefig('models_Chestler_2017/comparison_p.eps', format='eps')
plt.close(1)
