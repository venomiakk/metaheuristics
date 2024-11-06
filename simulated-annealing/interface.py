import plots
import algorithm

def main_int():
    func = int(input("Wybierz funkcje (1 lub 2): "))
    choose = int(input("    1. Podaj parametry\n    2. Parametry z artykulu\n       "))
    if choose != 1:
        if func == 1:
            sa = algorithm.simulatedAnnealing(-15, 15, -15, 15, algorithm.funkcja3, 90, 0.999, 200, 0.5, 
                                                k_iter_bonus=0, result_accuracy=0.001, wsp_c=0.1)
            pts = sa.run()
            plots.plot_f3([pts[-1]])
            return
        else:
            sa4 = algorithm.simulatedAnnealing(-3, 12, 4.1, 5.8, algorithm.funkcja4, 100, 0.999, 7000, 0.2, 
                                                k_iter_bonus=0, result_accuracy=0.001, wsp_c=0.1)
            pts = sa4.run()
            plots.plot_f4([pts[-1]])
            return
    else:
        print("Podaj parametry: ")
        stop_cond = int(input("Warunek stopu\n  1. Liczba epok\n  2. Srednia roznica ostatnich rozwiazan\n   "))
        stop_value = float(input("Wartosc warunku stopu: "))
        temp = float(input("Temperatura: "))
        temp_alpha = float(input("Wspolczynnik schladzania: "))
        k_iter = int(input("Liczba iteracji w epoce: "))
        k_boltz = float(input("Stala Boltzmana: "))
        c = float(input("Modyfikator przedzialu losowanych rozwiazan: "))

        if func == 1:
            if stop_cond != 1:
                sa = algorithm.simulatedAnnealing(-15, 15, -15, 15, algorithm.funkcja3, temp, temp_alpha, k_iter, k_boltz, 
                                                    k_iter_bonus=0, result_accuracy=stop_value, wsp_c=c)
                pts = sa.run()
                plots.plot_f3([pts[-1]])
                return
            else:
                sa = algorithm.simulatedAnnealing(-15, 15, -15, 15, algorithm.funkcja3, temp, temp_alpha, k_iter, k_boltz, 
                                                    k_iter_bonus=0, max_epochs=stop_value, wsp_c=c)
                pts = sa.run()
                plots.plot_f3([pts[-1]])
                return
        else:
            if stop_cond != 1:
                sa4 = algorithm.simulatedAnnealing(-3, 12, 4.1, 5.8, algorithm.funkcja4, temp, temp_alpha, k_iter, k_boltz, 
                                                    k_iter_bonus=0, result_accuracy=stop_value, wsp_c=c)
                pts = sa4.run()
                plots.plot_f4([pts[-1]])
                return
            else:
                sa4 = algorithm.simulatedAnnealing(-3, 12, 4.1, 5.8, algorithm.funkcja4, temp, temp_alpha, k_iter, k_boltz, 
                                                    k_iter_bonus=0, max_epochs=stop_value, wsp_c=c)
                pts = sa4.run()
                plots.plot_f4([pts[-1]])
                return


if __name__ == '__main__':
    main_int()