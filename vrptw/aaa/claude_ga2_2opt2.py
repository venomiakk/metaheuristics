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

class FitnessTracker:
    def __init__(self, distance: float, num_vehicles: int, feasible: bool):
        self.distance = distance
        self.num_vehicles = num_vehicles
        self.feasible = feasible
        # Prioritize vehicles over distance 
        self.score = (num_vehicles * 10000) + distance  # Much higher vehicle penalty
        self.utilization = 0  # Will track vehicle capacity usage
    
    def __lt__(self, other):
        if self.feasible and not other.feasible:
            return True
        if not self.feasible and other.feasible:
            return False
        # Compare vehicles first, then distance
        if self.num_vehicles != other.num_vehicles:
            return self.num_vehicles < other.num_vehicles
        return self.distance < other.distance

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
        for _ in range(self.population_size):
            # Create route using nearest neighbor for 50% of population
            if random.random() < 0.5:
                route = self._create_nearest_neighbor_route()
            else:
                route = random.sample(self.customers[1:], len(self.customers)-1)
            population.append(route)
        return population

    def _create_nearest_neighbor_route(self) -> List[Customer]:
        unvisited = self.customers[1:].copy()  # Exclude depot
        current = random.choice(unvisited)
        route = [current]
        unvisited.remove(current)
        
        while unvisited:
            next_customer = min(unvisited, 
                key=lambda x: self.distances[current.id-1][x.id-1])
            route.append(next_customer)
            current = next_customer
            unvisited.remove(current)
        
        return route

    def _split_routes(self, solution: List[Customer]) -> List[List[Customer]]:
        routes = []
        current_route = []
        current_load = 0
        
        # Sort by demand to pack vehicles better
        sorted_customers = sorted(solution, key=lambda x: x.demand, reverse=True)
        
        for customer in sorted_customers:
            if current_load + customer.demand <= self.vehicle_capacity:
                current_route.append(customer)
                current_load += customer.demand
            else:
                if current_route:
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
        # Edge recombination crossover
        edges = {}
        
        # Build edge map
        for p in [parent1, parent2]:
            for i in range(len(p)):
                if p[i] not in edges:
                    edges[p[i]] = set()
                edges[p[i]].add(p[i-1])
                edges[p[i]].add(p[(i+1) % len(p)])
        
        # Create child
        current = random.choice(parent1)
        child = [current]
        
        while len(child) < len(parent1):
            if current in edges:
                neighbors = edges[current]
                # Choose next city with fewest remaining neighbors
                next_city = min(neighbors, key=lambda x: len(edges.get(x, set())) if x not in child else float('inf'))
                if next_city in child:
                    next_city = random.choice([c for c in parent1 if c not in child])
            else:
                next_city = random.choice([c for c in parent1 if c not in child])
            
            child.append(next_city)
            current = next_city
            
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

    def _calculate_route_distance(self, route: List[Customer]) -> float:
        total_distance = 0
        current = self.depot
        
        for customer in route:
            total_distance += self.distances[current.id-1][customer.id-1]
            current = customer
            
        # Return to depot
        total_distance += self.distances[current.id-1][self.depot.id-1]
        return total_distance

    def _check_route_crossings(self, route):
        crossings = 0
        for i in range(len(route)-1):
            for j in range(i+2, len(route)-1):
                if self._line_intersection(
                    (route[i], route[i+1]),
                    (route[j], route[j+1])
                ):
                    crossings += 1
        return crossings

    def _calculate_fitness(self, route: List[Customer]) -> FitnessTracker:
        routes = self._split_routes(route)
        if not routes:
            return FitnessTracker(float('inf'), float('inf'), False)
            
        total_distance = 0
        total_utilization = 0
        
        for r in routes:
            total_distance += self._calculate_route_distance(r)
            route_load = sum(c.demand for c in r)
            total_utilization += route_load / self.vehicle_capacity
        
        avg_utilization = total_utilization / len(routes)
        penalty = 0 if self._is_feasible(routes) else 1000000
        
        fitness = FitnessTracker(
            distance=total_distance,
            num_vehicles=len(routes),
            feasible=penalty == 0
        )
        fitness.utilization = avg_utilization
        
        return fitness

    def _calculate_constraints_violations(self, route: List[Customer]) -> Tuple[int, int]:
        time_violations = 0
        capacity_violations = 0
        current_time = 0
        current_load = 0
        current = self.depot
        
        for customer in route:
            travel_time = self.distances[current.id-1][customer.id-1]
            arrival = current_time + travel_time
            
            if arrival > customer.due_date:
                time_violations += arrival - customer.due_date
                
            current_load += customer.demand
            if current_load > self.vehicle_capacity:
                capacity_violations += 1
                
            current_time = max(arrival, customer.ready_time) + customer.service_time
            current = customer
            
        return time_violations, capacity_violations

    def _optimize_route(self, route: List[Customer]) -> List[Customer]:
        improved = True
        while improved:
            improved = False
            for i in range(1, len(route)-2):
                for j in range(i+1, len(route)-1):
                    if self._line_intersection(
                        (route[i], route[i+1]),
                        (route[j], route[j+1])
                    ):
                        # Try 2-opt swap
                        new_route = route[:i+1] + route[i+1:j+1][::-1] + route[j+1:]
                        if (self._is_route_feasible(new_route) and 
                            self._calculate_route_distance(new_route) < self._calculate_route_distance(route)):
                            route = new_route
                            improved = True
                            break
                if improved:
                    break
        return route

    def _try_merge_routes(self, routes: List[List[Customer]]) -> List[List[Customer]]:
        improved = True
        while improved:
            improved = False
            for i in range(len(routes)):
                for j in range(i + 1, len(routes)):
                    # Try combining routes
                    merged_route = routes[i] + routes[j]
                    if (self._is_route_feasible(merged_route) and 
                        sum(c.demand for c in merged_route) <= self.vehicle_capacity):
                        # Merge successful
                        routes[i] = merged_route
                        routes.pop(j)
                        improved = True
                        break
                if improved:
                    break
        return routes

    def _is_feasible(self, routes: List[List[Customer]]) -> bool:
        return all(self._is_route_feasible(route) for route in routes)

    def _calculate_route_utilization(self, route: List[Customer]) -> float:
        total_demand = sum(c.demand for c in route)
        return total_demand / self.vehicle_capacity

    def solve(self):
        population = self._create_initial_population()
        best_solution = None
        best_fitness = FitnessTracker(float('inf'), float('inf'), False)
        
        for generation in range(self.generations):
            # Optimize each route in population
            population = [self._optimize_route(route) for route in population]
            
            fitness_scores = [self._calculate_fitness(route) for route in population]
            population = [x for _, x in sorted(zip(fitness_scores, population))]
            
            if fitness_scores[0] < best_fitness:
                best_fitness = fitness_scores[0]
                best_solution = population[0]
            
            # Elitism
            elite = population[:int(self.population_size * 0.2)]
            new_population = elite.copy()
            
            # Crossover and mutation
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(elite, 2)
                child = self._crossover(parent1, parent2)
                if random.random() < self.mutation_rate:
                    child = self._mutate(child)
                new_population.append(child)
                
            population = new_population
        
        final_routes = self._split_routes(best_solution)
        optimized_routes = [self._optimize_route(route) for route in final_routes]
        
        # Try to merge routes after optimization
        merged_routes = self._try_merge_routes(optimized_routes)
        
        return merged_routes

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
    customers = csvToPoints('data/c1type_vc200/C101.csv')
    
    vrptw = VRPTWGenetic(customers, 
                         vehicle_capacity=200,
                         population_size=300,
                         generations=500,
                         mutation_rate=0.2)
    
    routes = vrptw.solve()
    
    total_distance = 0
    print("\nRoute Details:")
    for i, route in enumerate(routes):
        distance = vrptw._calculate_route_distance(route)
        total_distance += distance
        print(f"Route {i+1}: Customers={len(route)}, Distance={distance:.2f}")
        print(f"Sequence: {[c.id for c in route]}\n")
    
    print(f"Total Routes: {len(routes)}")
    print(f"Total Distance: {total_distance:.2f}")

    vrptw.plot_routes(routes)

if __name__ == "__main__":
    main()