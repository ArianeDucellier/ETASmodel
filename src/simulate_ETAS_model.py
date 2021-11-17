"""
Function to simulate an ETAS process with thinning algorithm
"""

import numpy as np

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
    while tau < duration:
        lambda_max = compute_gif_marked(tau, mu, A, c, p, alpha, M0, np.array(times), np.array(M))
        ksi = np.random.exponential(scale=1.0 / lambda_max, size=1)
        lambda_g = compute_gif_marked(tau + ksi[0], mu, A, c, p, alpha, M0, np.array(times), np.array(M))
        U = np.random.uniform(0, 1, 1)
        # An event is generated
        if U <= lambda_g / lambda_max:
            times.append(tau + ksi[0])
            M.append(M0 + np.random.exponential(scale=1.0 / beta, size=1))
        tau = tau + ksi[0]
    return (np.array(times), np.array(M))
