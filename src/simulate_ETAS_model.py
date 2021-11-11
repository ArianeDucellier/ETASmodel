"""
Function to simulate an ETAS process with thinning algorithm
"""

import numpy as np

def compute_gif(times, t, mu, A, c, p):
    """
    """
    N = len(times)
    gif = np.zeros(N)
    for i in range(0, N):
        ti = t[t < times[i]]
        history = np.power(1 + (times[i] - ti) / c, - p)
        gif[i] = mu[i] + A * np.sum(history)
    return gif

def compute_gif_marked(times, t, mu, A, c, p, M, alpha, M0):
    """
    """
    N = len(times)
    gif = np.zeros(N)
    for i in range(0, N):
        ti = t[t < times[i]]
        Mi = M[t < times[i]]
        history = np.exp(alpha * (Mi - M0)) * np.power(1 + (times[i] - ti) / c, - p)
        gif[i] = mu[i] + A * np.sum(history)
    return gif

def generate_history(duration, delta, mu, A, c, p, alpha, M0):
    """
    """
    
    