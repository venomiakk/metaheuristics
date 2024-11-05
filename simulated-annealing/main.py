import algorithm
import numpy as np
import plots
import sys

if __name__ == '__main__':
    dir = 'output'
    f_sa1_1 = f'{dir}/sa1_1_1_1.txt'
    f_sa1_2 = f'{dir}/sa1_2.txt'
    f_sa2_1 = f'{dir}/sa2_1.txt'
    f_sa2_2 = f'{dir}/sa2_2.txt'
    file = 'outputs.txt'

    c_file = sys.argv[1]
    func = sys.argv[2]
    
    if func == 'f3':
        sa1_2 = algorithm.simulatedAnnealing(-15, 15, -15, 15, algorithm.funkcja3, 90, 0.999, 200, 0.5,
                                          filename=c_file, result_accuracy=0.0001, wsp_c=1, k_iter_bonus=0)
        points = sa1_2.run()

    if func == 'f4':
        sa2_1 = algorithm.simulatedAnnealing(-3, 12, 4.1, 5.8, algorithm.funkcja4, 100, 0.999, 100, 0.5, 
                                         filename=c_file, k_iter_bonus=0, result_accuracy=0.001, wsp_c=1)
        pts = sa2_1.run()

    sa2_1 = algorithm.simulatedAnnealing(-3, 12, 4.1, 5.8, algorithm.funkcja4, 100, 0.999, 100, 0.5, 
                                         filename=c_file, k_iter_bonus=0, result_accuracy=0.001, wsp_c=1)
    pts = sa2_1.run()