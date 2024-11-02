import math
from random import randint, uniform


class zad1:
    def __init__(self):
        self.x = randint(-10, 10)
        self.T = uniform(0.8,2)
        self.K = 1
    def generuj(self):
        return uniform(self.x - 2 * self.T, self.x + 2 * self.T)

    def funkcja(self, x):
        return x**2 + 5*x + 10

    def calc(self,  gen, fun, wsp):
        while(self.K<100):
            for n in range(self.K):
                j = gen()
                if(fun(j) <= fun(self.x)):
                    self.x = j
                else:
                    if math.exp(-(fun(j) - fun(self.x)) / self.T)>randint(0, 1):
                        self.x = j
            self.K += 1
            self.T *= wsp
        return self.x



if __name__ == '__main__':
    nwm = zad1()
    print(nwm.calc(nwm.generuj, nwm.funkcja, 0.95))
