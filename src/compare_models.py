"""
Script to compare the parameters of the models
for both packages
"""

import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Families with too big values for bayesianETAS
# mu: 39
# A: 39
# c: 31
# p: 31, 39

# Families with too big values for PtProcess
# A: 5, 30, 32, 64
# c: 5, 30, 32, 64
# p: 32

# Families with too small values for PtProcess
# alpha: 22, 56

# Read models with two packages
model1 = pd.read_csv('models_Chestler_2017_bayesianETAS.txt', sep=' ')
model2 = pd.read_csv('models_Chestler_2017_PtProcess.txt', sep=' ')

# Drop rows with outliers
model1.drop(index=[5, 22, 30, 31, 32, 39, 56, 64], inplace=True)
model2.drop(index=[5, 22, 30, 31, 32, 39, 56, 64], inplace=True)

model1.reset_index(inplace=True)
model2.reset_index(inplace=True)

# Take the logarithm for alpha
model1['alpha'] = np.log(model1['alpha'])
model2['alpha'] = np.log(model2['alpha'])

model1.rename(columns={'alpha':'log(alpha)'}, inplace=True)
model2.rename(columns={'alpha':'log(alpha)'}, inplace=True)

parameters = ['mu', 'A', 'log(alpha)', 'c', 'p']

# Start figure

params = {'legend.fontsize': 24, \
          'xtick.labelsize':24, \
          'ytick.labelsize':24}
pylab.rcParams.update(params)
plt.figure(1, figsize=(25, 15))

for i in range(0, len(parameters)):
    ax = plt.subplot2grid((3, len(parameters)), (0, i))
    plt.plot(model1[parameters[i]], model2[parameters[i]], 'ko')
    plt.xlabel(parameters[i] + ' from bayesianETAS', fontsize=24)
    plt.ylabel(parameters[i] + ' from PtProcess', fontsize=24)
    plt.title('Comparison', fontsize=24)

    ax = plt.subplot2grid((3, len(parameters)), (1, i))
    plt.hist(model1[parameters[i]])
    plt.xlabel(parameters[i], fontsize=24)
    plt.title('bayesianETAS', fontsize=24)

    ax = plt.subplot2grid((3, len(parameters)), (2, i))
    plt.hist(model2[parameters[i]])
    plt.xlabel(parameters[i], fontsize=24)
    plt.title('PtProcess', fontsize=24)

plt.tight_layout()
plt.savefig('compare_models.eps', format='eps')
plt.close(1)
