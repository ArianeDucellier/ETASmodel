"""
Function to simulate an ETAS process with thinning algorithm
"""

import numpy as np

from math import log

def compute_gif(t, mu, A, c, p, times):
    """
    type t: float
    t: Time at which we compute gif
    type times: numpy array of floats
    times: Event history
    """
    if len(times) > 0:
        ti = times[times < t]
        history = np.power(1 + (t - ti) / c, - p)
        gif = mu + A * np.sum(history)
    else:
        gif = mu
    return gif

def compute_gif_marked(t, mu, A, c, p, alpha, M0, times, M):
    """
    """
    if len(times) > 0:
        ti = times[times < t]
        Mi = M[times < t]
        history = np.exp(alpha * (Mi - M0)) * np.power(1 + (t - ti) / c, - p)
        gif = mu + A * np.sum(history)
    else:
        gif = mu
    return gif

def generate_history(duration, mu, A, c, p):
    """
    """
    tau = 0
    times = []
    while tau < duration:
        lambda_max = compute_gif(tau, mu, A, c, p, np.array(times))
        ksi = np.random.exponential(scale=1.0 / lambda_max, size=1)
        lambda_g = compute_gif(tau + ksi[0], mu, A, c, p, np.array(times))
        U = np.random.uniform(0, 1, 1)
        # An event is generated
        if U <= lambda_g / lambda_max:
            times.append(tau + ksi[0])
        tau = tau + ksi[0]
    return np.array(times)

def generate_history_marked(duration, mu, A, c, p, alpha, M0, beta):
    """
    """
    tau = 0
    times = []
    M = []
    while (tau < duration) and (len(times) < 2000):
        lambda_max = compute_gif_marked(tau, mu, A, c, p, alpha, M0, np.array(times), np.array(M))
        ksi = np.random.exponential(scale=1.0 / lambda_max, size=1)
        lambda_g = compute_gif_marked(tau + ksi[0], mu, A, c, p, alpha, M0, np.array(times), np.array(M))
        U = np.random.uniform(0, 1, 1)
        # An event is generated
        if U <= lambda_g / lambda_max:
            times.append(tau + ksi[0])
            M.append(M0 + np.random.exponential(scale=1.0 / beta, size=1)[0])
        tau = tau + ksi[0]
        if len(times) % 100 == 0:
            print('Generated {:d} earthquakes'.format(len(times)))
    return (np.array(times), np.array(M))

def variable_mu(t, duration):
    """
    """
    N = int(duration / 100)
    mu = 0.01
    for n in range(0, N):
        if (t > n * 100) and (t < n * 100 + 10):
            mu = 1
    return mu

def generate_history_varmu_marked(duration, A, c, p, alpha, M0, beta):
    """
    """
    tau = 0
    times = []
    M = []
    while tau < duration:
        scale = 1.0 / ((beta - 1) * log(10) * 1.5)
        mu = variable_mu(tau, duration)
        lambda_max = compute_gif_marked(tau, mu, A, c, p, alpha, M0, np.array(times), np.array(M))
        delta = - log(0.3) / lambda_max
        mu = variable_mu(tau + delta, duration)
        lambda_alt = compute_gif_marked(tau + delta, mu, A, c, p, alpha, M0, np.array(times), np.array(M))
        if lambda_alt > lambda_max:
            lambda_max = lambda_alt
        ksi = np.random.exponential(scale=1.0 / lambda_max, size=1)[0]
        mu = variable_mu(tau + ksi, duration)
        lambda_g = compute_gif_marked(tau + ksi, mu, A, c, p, alpha, M0, np.array(times), np.array(M))
        U = np.random.uniform(0, 1, 1)
        # An event is generated
        if U <= lambda_g / lambda_max:
            times.append(tau + ksi)
            M.append(M0 + np.random.exponential(scale=scale, size=1)[0])
            print(times[-1], M[-1])
        tau = tau + ksi
    return (np.array(times), np.array(M))
