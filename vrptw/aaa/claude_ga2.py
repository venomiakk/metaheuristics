import numpy as np
import matplotlib.pyplot as plt
import random
from typing import List, Tuple

class Customer:
    def __init__(self, id: int, x: float, y: float, demand: float, 
                 ready_time: float, due_date: float, service_time: float):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time

class VRPTWGenetic:
    def __init__(self, customers: List[Customer], 
                 vehicle_capacity: float = 200, 
                 population_size: int = 200, 
                 generations: int = 300, 
                 mutation_rate: float = 0.15):
        self.customers = customers
        self.depot = customers[0]
        self.vehicle_capacity = vehicle_capacity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        
        # Precompute distances
        self.distances = self._compute_distances()

    def _compute_distances(self) -> np.ndarray:
        num_customers = len(self.customers)
        distances = np.zeros((num_customers, num_customers))
        
        for i in range(num_customers):
            for j in range(num_customers):
                ci, cj = self.customers[i], self.customers[j]
                distances[i][j] = np.sqrt((ci.x - cj.x)**2 + (ci.y - cj.y)**2)
        
        return distances

    def _create_initial_population(self) -> List[List[Customer]]:
        population = []
        customers_copy = self.customers[1:]  # Exclude depot
        
        for _ in range(self.population_size):
            route = customers_copy.copy()
            random.shuffle(route)
            population.append(route)
        
        return population

    def _split_routes(self, solution: List[Customer]) -> List[List[Customer]]:
        routes = []
        current_route = []
        current_load = 0
        
        for customer in solution:
            # Check if adding customer violates capacity
            if not current_route or current_load + customer.demand <= self.vehicle_capacity:
                current_route.append(customer)
                current_load += customer.demand
            else:
                # Start a new route
                routes.append(current_route)
                current_route = [customer]
                current_load = customer.demand
        
        if current_route:
            routes.append(current_route)
        
        return routes

    def _is_route_feasible(self, route: List[Customer]) -> bool:
        current_time = 0
        current_load = 0
        current = self.depot
        
        for customer in route:
            # Travel time and distance
            travel_time = self.distances[current.id-1][customer.id-1]
            current_time += travel_time
            
            # Time window check
            current_time = max(current_time, customer.ready_time)
            if current_time > customer.due_date:
                return False
            
            # Capacity check
            current_load += customer.demand
            if current_load > self.vehicle_capacity:
                return False
            
            current_time += customer.service_time
            current = customer
        
        return True

    def _fitness(self, route: List[Customer]) -> float:
        if not self._is_route_feasible(route):
            return float('inf')
            
        total_distance = 0
        current = self.depot
        
        for customer in route:
            total_distance += self.distances[current.id-1][customer.id-1]
            current = customer
        
        # Add return to depot
        total_distance += self.distances[current.id-1][self.depot.id-1]
        return total_distance

    def _crossover(self, parent1: List[Customer], parent2: List[Customer]) -> List[Customer]:
        # Order crossover
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        
        child = [None] * size
        child[start:end] = parent1[start:end]
        
        remaining = [c for c in parent2 if c not in child[start:end]]
        
        for i in range(size):
            if child[i] is None:
                child[i] = remaining.pop(0)
        
        return child

    def _mutate(self, route: List[Customer]) -> List[Customer]:
        if random.random() < self.mutation_rate:
            # Swap mutation
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]
        return route

    def solve(self) -> List[List[Customer]]:
        # Initialize population
        population = self._create_initial_population()
        
        for generation in range(self.generations):
            # Calculate fitness for each route
            fitness_scores = [self._fitness(route) for route in population]
            
            # Create (fitness, route) pairs and sort
            population_with_fitness = list(zip(fitness_scores, population))
            population_with_fitness.sort(key=lambda x: x[0])  # Sort by fitness score
            
            # Extract sorted population
            sorted_population = [route for _, route in population_with_fitness]
            
            # Rest of solve method...
            new_population = []
            for _ in range(self.population_size):
                # Tournament selection
                tournament = random.sample(list(zip(sorted_population, fitness_scores)), 3)
                winner = min(tournament, key=lambda x: x[1])[0]
                new_population.append(winner)
            
            # Crossover
            offspring = []
            for i in range(0, len(new_population), 2):
                if i+1 < len(new_population):
                    child1 = self._crossover(new_population[i], new_population[i+1])
                    child2 = self._crossover(new_population[i+1], new_population[i])
                    offspring.extend([child1, child2])
            
            # Mutation
            population = [self._mutate(route) for route in offspring]
        
        # Return best solution (minimizing vehicles)
        best_solutions = sorted(population, key=self._fitness)
        return self._split_routes(best_solutions[0])

    def plot_routes(self, routes: List[List[Customer]]):
        plt.figure(figsize=(10, 10))
        plt.title(f'VRPTW Routes (Vehicles: {len(routes)})')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        
        # Plot depot
        plt.scatter(self.depot.x, self.depot.y, color='red', s=200, label='Depot')
        
        # Plot routes with different colors
        for i, route in enumerate(routes):
            x_coords = [self.depot.x] + [c.x for c in route] + [self.depot.x]
            y_coords = [self.depot.y] + [c.y for c in route] + [self.depot.y]
            plt.plot(x_coords, y_coords, marker='o', label=f'Route {i+1}')
        
        plt.legend()
        plt.grid(True)
        plt.show()

    def calculate_total_distance(self, routes):
        total = 0
        for route in routes:
            current = self.depot
            route_distance = 0
            
            for customer in route:
                route_distance += self.distances[current.id-1][customer.id-1]
                current = customer
                
            # Return to depot
            route_distance += self.distances[current.id-1][self.depot.id-1]
            total += route_distance
        return total

# (Parsing function remains the same as in previous implementation)
def csvToPoints(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            fields = line.split(',')
            custno = int(fields[0])
            xcord = float(fields[1])
            ycord = float(fields[2])
            demand = float(fields[3])
            readytime = float(fields[4])
            duedate = float(fields[5])
            servicetime = float(fields[6])
            point = Customer(custno, xcord, ycord, demand, readytime, duedate, servicetime)
            points.append(point)
    return points

def main():
    customers = csvToPoints('data/C1type_vc200/C101.csv')
    
    vrptw = VRPTWGenetic(customers, 
                         vehicle_capacity=200, 
                         population_size=50, 
                         generations=100, 
                         mutation_rate=0.15)
    
    routes = vrptw.solve()
    
    # Print routes and distances
    total_distance = 0
    for i, route in enumerate(routes):
        route_distance = vrptw.calculate_total_distance([route])
        print(f"Route {i+1}: {[c.id for c in route]} - Distance: {route_distance:.2f}")
        total_distance += route_distance
    
    print(f"\nTotal Distance: {total_distance:.2f}")
    
    # Visualize routes
    vrptw.plot_routes(routes)

if __name__ == "__main__":
    main()