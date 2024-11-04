import math
import numpy as np
from random import randint, uniform

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
    return 21.5 + x * np.sin(4 * np.pi * x) + y * np.sin(20 * np.pi * y)


class simulatedAnnealing:
    def __init__(self, minX, maxX, minY, maxY, T, K):
        self.x = uniform(minX, maxX)
        self.y = uniform(minY, maxY)
        self.t = T
        self.k = K
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        print(self.x, self.y)

    def generate(self, x, c, min, max ):
        while True:
            wynik = uniform(x - c * self.t, x + c * self.t)
            if (wynik > min and  wynik < max):
                break
        return wynik

    
    def calc(self,  gen, fun, wsp_alpha, wsp_k):
        epochs = 0
        while(self.t>0.1):
            epochs += 1
            for _ in range(self.k):
                newx = gen(self.x, 0.5, self.minX, self.maxX)
                newy = gen(self.y, 0.5, self.minY, self.maxY)

                if fun(self.x, self.y) - fun(newx, self.y) < 0:
                    self.x = newx
                else:
                    check = uniform(0, 1)
                    if math.exp(-(fun(self.x,self.y) - fun(newx,self.y)) / (wsp_k * self.t)) > check:
                        self.x = newx
                if fun(self.x, self.y) - fun(self.x, newy) < 0:
                    self.y = newy
                else:
                    check = uniform(0, 1)
                    if math.exp(-(fun(self.x,self.y) - fun(self.x,newy)) / (wsp_k * self.t)) > check:
                        self.y = newy

            print(self.x, self.y, fun(self.x, self.y), epochs)
            self.t *= wsp_alpha
            #self.k += 3

        return self.x, self.y, fun(self.x, self.y)
    
    def calc2(self,  gen, fun, wsp_alpha, wsp_k):
        epochs = 0
        while(self.t>0.1):
            epochs += 1
            for _ in range(self.k):
                newx = gen(self.x, 0.5, self.minX, self.maxX)
                newy = gen(self.y, 0.5, self.minY, self.maxY)

                # if fun(self.x, self.y) - fun(newx, newy) < 0:
                if fun(newx, newy) >= fun(self.x, self.y):
                    self.x = newx
                    self.y = newy
                else:
                    check = uniform(0, 1)
                    if math.exp(-(fun(self.x,self.y) - fun(newx,newy)) / (wsp_k * self.t)) > check:
                        self.x = newx
                        self.y = newy

            print(self.x, self.y, fun(self.x, self.y), epochs)
            self.t *= wsp_alpha
            # self.k += 3

        return self.x, self.y, fun(self.x, self.y)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    nwm = simulatedAnnealing(-3, 12, 4.1, 5.8, 100, 7000) #K = M
    # print(nwm.calc(nwm.generate, funkcja4, 0.999, 0.2)) #wsp1= k wsp = alfa(T)   
    print(nwm.calc2(nwm.generate, funkcja4, 0.999, 0.2)) #6905 epochs

    # sa2 = simulatedAnnealing(-15, 15, -15, 15, 90)
    # print(sa2.calc2(sa2.generate, funkcja3, 0.999, 0.5))
    # print(funkcja3(-12,-12))
    # print(funkcja3(-12,12))
    # print(funkcja3(12,-12))
    # print(funkcja3(12,12))
    # print(funkcja4(11.625545, 5.7250444))