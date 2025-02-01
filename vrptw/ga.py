from vehicle import Vehicle
from customer import Customer
from utils import getCustomersFromCSV, csvToPoints, plotPlainData, plotRoutes, greedy, calculateSolutionDistance

class GA_VRPTW:
    def __init__(self, depot, customers, vehicle_capacity, 
                 population_size=100, generations=200, 
                 mutation_rate=0.3, elite_size=10):
        self.depot = depot
        self.customers = customers
        self.vehicle_capacity = vehicle_capacity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.best_fitness_history = []

    def run(self):
        population = self.initializePopulation()
        for i in population:
            print(calculateSolutionDistance(i))

    def initializePopulation(self):
        pop = []
        for _ in range(self.population_size):
            solution = greedy(self.depot, self.customers, self.vehicle_capacity)
            # self.evaluateFitness(vehicles)
            pop.append(solution)
        return pop
    
    def evaluateFitness(self, solution):
        for vehicle in solution:
            if not vehicle.isRouteCorrect():
                vehicle.fitness = float('inf')
            else:
                vehicle.fitness = vehicle.calculateRouteDistance()
        return solution

if __name__ == '__main__':
    file = 'data/c1type_vc200/C101.csv'
    capacity = 200
    allpoints = csvToPoints(file)
    depot, customers = allpoints[0], allpoints[1:]
    ga = GA_VRPTW(depot, customers, capacity)
    ga.run()