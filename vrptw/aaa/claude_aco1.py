import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import math
import random
from copy import deepcopy

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

class VRPTW_ACO:
    def __init__(self, customers: List[Customer], vehicle_capacity: float = 200, 
                 num_ants: int = 30, alpha: float = 1.0, beta: float = 2.0, 
                 evaporation_rate: float = 0.5, Q: float = 100):
        self.customers = customers
        self.depot = customers[0]
        self.vehicle_capacity = vehicle_capacity
        self.num_ants = num_ants
        self.alpha = alpha  # pheromone importance
        self.beta = beta    # heuristic importance
        self.evaporation_rate = evaporation_rate
        self.Q = Q          # pheromone deposit factor
        
        # Precompute distances
        self.distances = self._compute_distances()
        
        # Initialize pheromone trails
        self.pheromones = np.ones((len(customers), len(customers)))

    def _compute_distances(self) -> np.ndarray:
        num_customers = len(self.customers) + 1  # Include depot
        distances = np.zeros((num_customers, num_customers))
        
        all_nodes = [self.depot] + self.customers
        
        for i in range(num_customers):
            for j in range(num_customers):
                ci, cj = all_nodes[i], all_nodes[j]
                distances[i][j] = math.sqrt((ci.x - cj.x)**2 + (ci.y - cj.y)**2)
        
        return distances

    def _is_feasible_route(self, route: List[Customer]) -> bool:
        current_time = 0
        current_load = 0
        prev_customer = route[0]  # Start at depot
        
        for customer in route[1:]:  # Skip depot
            # Travel time to next customer
            travel_time = self.distances[prev_customer.id][customer.id]
            
            # Arrival time at customer
            arrival_time = current_time + travel_time
            
            # Wait if arrived before ready time
            current_time = max(arrival_time, customer.ready_time)
            
            # Check time window constraint
            if current_time > customer.due_date:
                return False
                
            # Check capacity constraint    
            current_load += customer.demand
            if current_load > self.vehicle_capacity:
                return False
                
            # Service time
            current_time += customer.service_time
            prev_customer = customer
        
        # Check return to depot
        final_time = current_time + self.distances[prev_customer.id][self.depot.id]
        return final_time <= self.depot.due_date

    def solve(self, max_iterations: int = 100) -> List[List[Customer]]:
        best_solution = None
        best_cost = float('inf')
        
        for _ in range(max_iterations):
            ant_solutions = []
            
            for _ in range(self.num_ants):
                route = self._construct_route()
                if route:
                    ant_solutions.append(route)
            
            # Evaluate solutions
            for solution in ant_solutions:
                cost = self._calculate_solution_cost(solution)
                if cost < best_cost:
                    best_solution = solution
                    best_cost = cost
            
            # Update pheromones
            self._update_pheromones(ant_solutions)
        
        return self._split_routes(best_solution)

    def _construct_route(self) -> List[Customer]:
        unvisited = set(self.customers[1:])  # Exclude depot
        current = self.depot
        route = []
        
        while unvisited:
            next_customer = self._select_next_customer(current, unvisited)
            if next_customer is None:
                break
            route.append(next_customer)
            unvisited.remove(next_customer)
            current = next_customer
        
        # Add return to depot if route is feasible
        route.append(self.depot)
        
        return route if self._is_feasible_route(route) else None

    def _select_next_customer(self, current: Customer, unvisited: List[Customer]) -> Customer:
        EPSILON = 1e-10  # Small constant to prevent division by zero
        
        probabilities = []
        for customer in unvisited:
            pheromone = self.pheromones[current.id-1][customer.id-1]
            distance = max(self.distances[current.id-1][customer.id-1], EPSILON)
            prob = (pheromone ** self.alpha) * ((1.0 / distance) ** self.beta)
            probabilities.append((customer, prob))
        
        total = sum(p for _, p in probabilities) 
        if total == 0:
            return random.choice(unvisited)
            
        probabilities = [(c, p/total) for c, p in probabilities]
        customer = random.choices(
            population=[c for c, _ in probabilities],
            weights=[p for _, p in probabilities],
            k=1
        )[0]
        
        return customer

    def _update_pheromones(self, solutions: List[List[Customer]]):
        # Evaporation
        self.pheromones *= (1 - self.evaporation_rate)
        
        # Deposit pheromones
        for solution in solutions:
            route_cost = self._calculate_solution_cost(solution)
            for i in range(len(solution) - 1):
                self.pheromones[solution[i].id][solution[i+1].id] += self.Q / route_cost

    def _calculate_solution_cost(self, route: List[Customer]) -> float:
        # Total route length
        total_distance = sum(
            self.distances[route[i].id][route[i+1].id] 
            for i in range(len(route)-1)
        )
        return total_distance

    def _split_routes(self, solution: List[Customer]) -> List[List[Customer]]:
        # Create deep copy of solution excluding first and last depot
        solution_copy = [self.depot] + [deepcopy(c) for c in solution[1:-1]] + [self.depot]
        
        routes = []
        current_route = [self.depot]
        current_load = 0
        current_time = 0
        
        for customer in solution_copy[1:-1]:  # Exclude depot at start and end
            # Check if adding customer violates constraints
            if (current_load + customer.demand > self.vehicle_capacity or 
                current_time + self.distances[current_route[-1].id][customer.id] > customer.due_date):
                # Start a new route
                current_route.append(self.depot)
                routes.append(current_route)
                current_route = [self.depot]
                current_load = 0
                current_time = 0
            
            current_route.append(customer)
        
        # Add final depot to last route
        current_route.append(self.depot)
        routes.append(current_route)
        
        return routes

    def plot_routes(self, routes: List[List[Customer]]):
        plt.figure(figsize=(10, 10))
        plt.title('VRPTW Routes')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        
        # Plot depot
        plt.scatter(self.depot.x, self.depot.y, color='red', s=200, label='Depot')
        
        # Plot routes with different colors
        for i, route in enumerate(routes):
            x_coords = [c.x for c in route]
            y_coords = [c.y for c in route]
            plt.plot(x_coords, y_coords, marker='o', label=f'Route {i+1}')
        
        plt.legend()
        plt.grid(True)
        plt.show()

# Parse input data
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

# Example usage
def main():
    customers = csvToPoints('data/r1type_vc200/R101.csv')
    
    vrptw = VRPTW_ACO(customers, 
                      vehicle_capacity=200, 
                      num_ants=30)
    
    routes = vrptw.solve()
    
    # Print routes
    for i, route in enumerate(routes):
        print(f"Route {i+1}: {[c.id for c in route]}")
    
    # Visualize routes
    vrptw.plot_routes(routes)

if __name__ == "__main__":
    main()