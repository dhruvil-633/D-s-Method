import numpy as np

def directional_accuracy(pred, real):
    return np.mean(np.sign(pred) == np.sign(real))

def information_coefficient(pred, real):
    return np.corrcoef(pred, real)[0, 1]

def rmse(pred, real):
    return np.sqrt(np.mean((pred - real)**2))
