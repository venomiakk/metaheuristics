import algorithm
import numpy as np

if __name__ == '__main__':
    tab = [1.23, 2.34, 5.1, 2.02]
    print(np.mean(np.abs(np.diff(tab))))
    print(max(tab)-min(tab))