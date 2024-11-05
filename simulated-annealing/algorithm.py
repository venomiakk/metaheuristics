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
    def __init__(self, minX, maxX, minY, maxY, func, Temp, Temp_alpha,
                  k_iter, wsp_k_boltz, result_accuracy=0.1, results_stored=10,
                    max_epochs=-1, k_iter_bonus=1, wsp_c=1):
        """
        @brief Constructor for the simulatedAnnealing class.

        @param minX Minimum value for the x-coordinate.
        @param maxX Maximum value for the x-coordinate.
        @param minY Minimum value for the y-coordinate.
        @param maxY Maximum value for the y-coordinate.
        @param func Function to find the maximum.
        @param Temp Initial temperature for the annealing process.
        @param Temp_alpha Cooling rate for the temperature.
        @param k_iter Number of iterations per temperature step.
        @param wsp_k_boltz Boltzmann constant for the acceptance probability.
        @param result_accuracy Desired accuracy for the result. Default is 0.1
        @param results_stored Number of results to calculate for checking result_accuracy. Default is 10 
        @param max_epochs Maximum number of epochs to run the algorithm, If -1, other stop condition. Default is -1
        @param k_iter_bonus Increment for the number of iterations per temperature step. Default is 1
        @param wsp_c Coefficient for the generation of new candidate solutions. Default is 1
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
    
    def generate(self, value, min, max ):
        while True:
            wynik = uniform(value - (self.wsp_c * self.temp), value + (self.wsp_c * self.temp))
            if (wynik > min and  wynik < max):
                break
        return wynik

    def run(self):
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

            self.last_result = self.func(self.x, self.y)
            print(self.x, self.y, self.last_result, self.epochs)
            self.temp *= self.t_alpha
            self.k_iter += self.k_iter_bonus
        
        print(self.x, self.y, self.last_result, self.epochs)


    
    def calc(self,  gen, func, wsp_alpha, wsp_k):
        epochs = 0
        while(self.temp>0.1):
            epochs += 1
            for _ in range(self.k):
                newx = gen(self.x, 0.5, self.minX, self.maxX)
                newy = gen(self.y, 0.5, self.minY, self.maxY)

                if func(self.x, self.y) - func(newx, self.y) < 0:
                    self.x = newx
                else:
                    check = uniform(0, 1)
                    if math.exp(-(func(self.x,self.y) - func(newx,self.y)) / (wsp_k * self.temp)) > check:
                        self.x = newx
                if func(self.x, self.y) - func(self.x, newy) < 0:
                    self.y = newy
                else:
                    check = uniform(0, 1)
                    if math.exp(-(func(self.x,self.y) - func(self.x,newy)) / (wsp_k * self.temp)) > check:
                        self.y = newy

            print(self.x, self.y, func(self.x, self.y), epochs)
            self.temp *= wsp_alpha
            #self.k += 3

        return self.x, self.y, func(self.x, self.y)
    
    def calc2(self,  gen, fun, wsp_alpha, wsp_k):
        epochs = 0
        while(self.temp>0.1):
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
                    if math.exp(-(fun(self.x,self.y) - fun(newx,newy)) / (wsp_k * self.temp)) > check:
                        self.x = newx
                        self.y = newy

            print(self.x, self.y, fun(self.x, self.y), epochs)
            self.temp *= wsp_alpha
            # self.k += 3

        return self.x, self.y, fun(self.x, self.y)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    nwm = simulatedAnnealing(-3, 12, 4.1, 5.8, funkcja4, 100, 0.999, 7000, 0.2) #K = M
    nwm.run()
    # print(nwm.calc(nwm.generate, funkcja4, 0.999, 0.2)) #wsp1= k wsp = alfa(T)   
    #print(nwm.calc2(nwm.generate, funkcja4, 0.999, 0.2)) #6905 epochs

    # sa2 = simulatedAnnealing(-15, 15, -15, 15, 90)
    # print(sa2.calc2(sa2.generate, funkcja3, 0.999, 0.5))
    # print(funkcja3(-12,-12))
    # print(funkcja3(-12,12))
    # print(funkcja3(12,-12))
    # print(funkcja3(12,12))
    # print(funkcja4(11.625545, 5.7250444))