import numpy as np


def ackley(x, y):
    # -5 <= x,y <= 5
    # min: f(0,0) = 0

    term1 = -20.0 * np.exp(-0.2 * (np.sqrt(0.5 * (x ** 2 + y ** 2))))
    term2 = -np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
    return term1 + term2 + np.e + 20


def himmelblaus(x, y):
    # -5 <= x,y <= 5
    # min:
    # f(3.0, 2.0) = 0
    # f(-2.805118, 3.131312) = 0
    # f(-3.779310, -3.283186) = 0
    # f(3.584428, -1.848126) = 0

    term1 = (x ** 2 + y - 11) ** 2
    term2 = (x + y ** 2 - 7) ** 2
    return term1 + term2
