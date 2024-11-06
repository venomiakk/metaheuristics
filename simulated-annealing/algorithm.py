import math
import numpy as np
from random import randint, uniform
from datetime import datetime

# maksimum funkcji o ekstremach bardzo oddalonych od siebie
# [-15, 15]×[-15, 15]
# maks lokalne f(-12, -12)=8.015598, f(-12, 12)=9.000000, f(12, -12)=10.007806
# maks globalne f(12, 12)=11.015598.
def funkcja3(x, y):
    return 8 * np.exp(-(x+12)**2 - (y+12)**2) + \
           9/(1+(x+12)**2 + (y-12)**2) + \
           20/(np.cosh(x-12)**2 + np.cosh(y+12)**2) + \
           176/((np.exp(x-12)+2+np.exp(-x+12)) * (np.exp(y-12)+2+np.exp(-y+12)))


# maksimum funkcji o ekstremach bliskich siebie
# [-3, 12]×[4.1, 5.8].
# f(11.625545, 5.7250444) = 38.850294
def funkcja4(x, y):
    return 21.5 + (x * np.sin(4 * np.pi * x)) + (y * np.sin(20 * np.pi * y))


class simulatedAnnealing:
    def __init__(self, minX, maxX, minY, maxY, func, Temp, Temp_alpha,
                  k_iter, wsp_k_boltz, result_accuracy=0.1, results_stored=10,
                    max_epochs=-1, k_iter_bonus=1, wsp_c=1, filename=''):
        """
        @brief Konstruktor klasy simulatedAnnealing.

        @param minX Poczatek przedzialu X
        @param maxX Koniec przedzialu X
        @param minY Poczatek przedzialu Y
        @param maxY Koniec przedzialu Y
        @param func Funkcja, ktorej maksimum szukamy
        @param Temp Poczatkowa temperatura
        @param Temp_alpha Wspolczynnik schladzania
        @param k_iter Liczba iteracji dla kazdej epoki
        @param wsp_k_boltz Stala Boltzmanna dla prawdopodobienstaw przyjecia gorszego rozwiazania
        @param result_accuracy Zmiana rozwiazania (warunek stopu), domyslnie 0.1
        @param results_stored Liczba ostatnich wynikow brana pod uwage przy obliczaniu zmiany rozwiazan, domyslnie 10
        @param max_epochs Liczba epok, po ktorej algorytm ma zakonczyc obliczenia, jezeli -1, drugi warunek stopu, domyslnie -1
        @param k_iter_bonus Inkrementacja iteracji w kazdej epoce, domyslnie 1
        @param wsp_c Wspolczynnik zawezajacy przedzial podczas losowania nowego rozwiazania, domyslnie 1
        @param filename Nazwa pliku do zapisania wynikow, domyslnie '', wtedy wyniki nie sa zapisywane
        """
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.x = uniform(self.minX, self.maxX)
        self.y = uniform(self.minY, self.maxY)
        self.func = func
        self.last_result = self.func(self.x, self.y)

        self.temp = Temp
        self.t_alpha = Temp_alpha
        self.k_iter = k_iter
        self.wsp_k = wsp_k_boltz

        self.result_accuracy = result_accuracy
        self.results_stored = results_stored
        self.max_epochs = max_epochs
        self.k_iter_bonus = k_iter_bonus
        self.wsp_c = wsp_c

        self.epochs = 0
        self.results_tab = []

        self.filename = filename
    
    def generate(self, value, min, max ):
        while True:
            wynik = uniform(value - (self.wsp_c * self.temp), value + (self.wsp_c * self.temp))
            if (wynik > min and  wynik < max):
                break
        return wynik

    def run(self):
        points = []
        if self.filename != '':
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file = open(self.filename, 'a')
                file.write(
                    f'{current_time}, params:minX={self.minX}, maxX={self.maxX}, minY={self.minY}, maxY={self.maxY}, '
                    f'func={self.func}, Temp={self.temp}, Temp_alpha={self.t_alpha}, k_iter={self.k_iter}, '
                    f'wsp_k_boltz={self.wsp_k}, result_accuracy={self.result_accuracy}, results_stored={self.results_stored}, '
                    f'max_epochs={self.max_epochs}, k_iter_bonus={self.k_iter_bonus}, wsp_c={self.wsp_c}, filename={self.filename}\n'
                )
                file.close()
        while True:
            self.epochs += 1
            for _ in range(self.k_iter):
                newx = self.generate(self.x, self.minX, self.maxX)
                newy = self.generate(self.y, self.minY, self.maxY)

                if self.func(newx, newy) >= self.func(self.x, self.y):
                    self.x = newx
                    self.y = newy
                else:
                    check = uniform(0, 1)
                    if math.exp(-(self.func(self.x,self.y) - self.func(newx,newy)) / (self.wsp_k * self.temp)) > check:
                        self.x = newx
                        self.y = newy
            
            tmp = [self.x, self.y]
            points.append(tmp)

            current_result = self.func(self.x, self.y)
            self.results_tab.append(current_result)
            if len(self.results_tab) > self.results_stored:
                self.results_tab.pop(0)

            if (self.max_epochs != -1 and self.epochs >= self.max_epochs):
                self.last_result = current_result
                break
            
            if (self.max_epochs == -1 and len(self.results_tab) >= self.results_stored):
                avg_diff = np.mean(np.abs(np.diff(self.results_tab)))
                if avg_diff <= self.result_accuracy:
                    self.last_result = current_result
                    break
            
            self.last_result = current_result
            print(f'{self.epochs}: x={self.x}, y={self.y}, f(x,y)={self.last_result}')
            if self.filename != '':
                file = open(self.filename, 'a')
                file.write(f'{self.epochs}: x={self.x}, y={self.y}, f(x,y)={self.last_result}\n')
                file.close()
            
            self.temp *= self.t_alpha
            self.k_iter += self.k_iter_bonus
        
        print(f'Result: {self.epochs}: x={self.x}, y={self.y}, f(x,y)={self.last_result}')
        if self.filename != '':
                file = open(self.filename, 'a')
                file.write(f'Result: {self.epochs}: x={self.x}, y={self.y}, f(x,y)={self.last_result}\n')
                file.close()

        return points
    