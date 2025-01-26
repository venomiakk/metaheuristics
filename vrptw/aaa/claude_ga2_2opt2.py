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

    def _line_intersection(self, line1, line2):
        # Check if two line segments intersect
        def ccw(A, B, C):
            return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
        
        A, B = line1
        C, D = line2
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    def _two_opt(self, route: List[Customer]) -> List[Customer]:
        best_route = route.copy()
        improved = True
        
        while improved:
            improved = False
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route) - 1):
                    # Check if swapping these edges reduces total distance
                    new_route = route.copy()
                    new_route[i:j] = route[j-1:i-1:-1]
                    
                    # Check route feasibility
                    if self._is_route_feasible(new_route):
                        # Check for path crossings
                        crossing = False
                        for k in range(len(new_route) - 1):
                            for l in range(k + 2, len(new_route) - 1):
                                if self._line_intersection(
                                    (new_route[k], new_route[k+1]), 
                                    (new_route[l], new_route[l+1])
                                ):
                                    crossing = True
                                    break
                            if crossing:
                                break
                        
                        # If no crossings and better total distance, update route
                        if not crossing:
                            best_route = new_route
                            improved = True
                            route = new_route
                            break
                if improved:
                    break
        
        return best_route

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

    def _fitness(self, route: List[Customer]) -> Tuple[float, float]:
        # Apply 2-opt local search to improve route
        route = self._two_opt(route)
        
        # Split route into feasible vehicle routes
        routes = self._split_routes(route)
        
        # Check if all routes are feasible
        if not all(self._is_route_feasible(r) for r in routes):
            return (float('inf'), float('inf'))
        
        # Compute number of vehicles (routes)
        num_vehicles = len(routes)
        
        # Total route distance
        total_distance = sum(
            sum(self.distances[self.depot.id][route[0].id] +
                sum(self.distances[route[i].id][route[i+1].id] for i in range(len(route)-1)) +
                self.distances[route[-1].id][self.depot.id]
                for route in routes)
        )
        
        # Multi-objective fitness: primary is number of vehicles, secondary is total distance
        return (num_vehicles, total_distance)

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

    class RouteWithFitness:
        def __init__(self, route: List[Customer], fitness: float):
            self.route = route
            self.fitness = fitness
        
        def __lt__(self, other):
            return self.fitness < other.fitness

    def solve(self):
        # Initialize population
        population = self._create_initial_population()
        
        for generation in range(self.generations):
            # Calculate fitness and create RouteWithFitness objects
            route_with_fitness = []
            for route in population:
                fitness = self._fitness(route)
                route_with_fitness.append(self.RouteWithFitness(route, fitness))
            
            # Sort population by fitness
            route_with_fitness.sort()
            
            # Extract sorted routes
            sorted_population = [rwf.route for rwf in route_with_fitness]
            
            # Select best routes
            elite = sorted_population[:self.population_size // 10]
            
            # Create new population
            new_population = elite.copy()
            
            while len(new_population) < self.population_size:
                parent1 = random.choice(elite)
                parent2 = random.choice(elite)
                child = self._crossover(parent1, parent2)
                if random.random() < self.mutation_rate:
                    child = self._mutate(child)
                new_population.append(child)
                
            population = new_population
        
        # Return best solution
        best_fitness = float('inf')
        best_solution = None
        for route in population:
            fitness = self._fitness(route)
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = route
                
        return self._split_routes(best_solution)

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
    customers = csvToPoints('data/r1type_vc200/R101.csv')
    
    vrptw = VRPTWGenetic(customers, 
                         vehicle_capacity=50, 
                         population_size=200, 
                         generations=300, 
                         mutation_rate=0.15)
    
    routes = vrptw.solve()
    
    # Print routes
    for i, route in enumerate(routes):
        print(f"Route {i+1}: {[c.id for c in route]}")
    
    # Visualize routes
    vrptw.plot_routes(routes)

if __name__ == "__main__":
    main()