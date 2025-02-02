import random
import math
import csv
import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass
import random
import math


@dataclass
class Customer:
    id: int
    x: float
    y: float
    demand: float
    ready_time: float  # Earliest service time
    due_time: float    # Latest service time
    service_time: float

class Route:
    def __init__(self, depot: Customer, capacity: float):
        self.path = [depot]  # Start and end with depot
        self.capacity = capacity
        self.current_load = 0
        self.current_time = 0
        
    def is_feasible(self, customer: Customer, position: int) -> bool:
        """Check if inserting customer at position is feasible regarding capacity and time windows"""
        # First check capacity
        if self.current_load + customer.demand > self.capacity:
            return False
            
        # Then check time windows
        temp_route = self.path.copy()
        temp_route.insert(position, customer)
        current_time = 0
        temp_load = 0
        
        for i in range(len(temp_route) - 1):
            current = temp_route[i]
            next_customer = temp_route[i + 1]
            
            # Update load
            if i > 0:  # Don't count depot
                temp_load += current.demand
                if temp_load > self.capacity:
                    return False
            
            # TODO
            # Add travel time (using Euclidean distance)
            travel_time = np.sqrt((current.x - next_customer.x)**2 + 
                                (current.y - next_customer.y)**2)
            current_time = max(current_time + travel_time, next_customer.ready_time)
            
            if current_time > next_customer.due_time:
                return False
                
            current_time += next_customer.service_time
            
        return True

    def add_customer(self, customer: Customer, position: int) -> bool:
        """Add customer to route if feasible and update current load"""
        if self.is_feasible(customer, position):
            self.path.insert(position, customer)
            self.current_load += customer.demand
            return True
        return False

    def remove_customer(self, position: int) -> Customer:
        """Remove customer from route and update current load"""
        customer = self.path.pop(position)
        if position > 0 and position < len(self.path):  # Don't count depot
            self.current_load -= customer.demand
        return customer

    def calculate_total_distance(self) -> float:
        """Calculate total distance of route"""
        total = 0
        for i in range(len(self.path) - 1):
            current = self.path[i]
            next_customer = self.path[i + 1]
            total += np.sqrt((current.x - next_customer.x)**2 + 
                           (current.y - next_customer.y)**2)
        return total

class Solution:
    def __init__(self, routes: List[Route]):
        self.routes = routes
    
    def objective_value(self) -> float:
        """Calculate total distance + vehicle penalty"""
        total_distance = sum(route.calculate_total_distance() for route in self.routes)
        vehicle_penalty = len(self.routes) * 1000  # Penalize number of vehicles
        return total_distance + vehicle_penalty
    
    def __str__(self):
        r_str = ''
        for idx, route in enumerate(self.routes):
            r_str += f'Route {idx + 1}: '
            for customer in route.path:
                r_str += str(customer.id) + ' '
            r_str += '\n'
        return r_str

def readData(file):
    customers = []
    with open(file) as f:
        for line in f:
            line = line.strip().split(',')
            customers.append(Customer(int(line[0])-1, float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6])))
    return customers

def plotRoutes(routes, depot, title='VRPTW Routes'):
    plt.figure(figsize=(8, 8))
    for idx, route in enumerate(routes):
        x = [cust['x'] for cust in route]
        y = [cust['y'] for cust in route]
        plt.plot(x, y, marker='o', label=f'Route {idx+1}')
    plt.scatter(depot['x'], depot['y'], color='red', zorder=10, label='Depot')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.legend()
    plt.show()

def create_initial_solution(customers: List[Customer], depot: Customer, vehicle_capacity: float) -> Solution:
    """Create initial solution ensuring valid routes"""
    routes = []
    unassigned = customers.copy()
    
    while unassigned:
        route = Route(depot, vehicle_capacity)
        route.add_customer(depot, 0)  # Start with depot
        
        # Try to add customers while feasible
        i = 0
        while i < len(unassigned):
            customer = unassigned[i]
            if route.is_feasible(customer, len(route.path)-1):
                if route.add_customer(customer, len(route.path)-1):  # Add before final depot
                    unassigned.remove(customer)
                    continue
            i += 1
            
        route.add_customer(depot, len(route.path))  # End with depot
        if len(route.path) > 2:  # Only add routes with at least one customer
            routes.append(route)
    
    return Solution(routes)

def escape(solution: Solution) -> Solution:
    """Generate neighboring solution using operators from the paper"""
    new_solution = Solution([Route(route.path[0], route.capacity) for route in solution.routes])
    for i, route in enumerate(new_solution.routes):
        route.path = solution.routes[i].path.copy()
        route.current_load = solution.routes[i].current_load
    
    operator = random.choice(['intra_relocate', 'inter_relocate', 'inter_exchange'])
    
    if operator == 'intra_relocate' and len(new_solution.routes) > 0:
        route = random.choice(new_solution.routes)
        if len(route.path) > 3:
            pos1 = random.randint(1, len(route.path) - 2)
            pos2 = random.randint(1, len(route.path) - 2)
            customer = route.remove_customer(pos1)
            if not route.add_customer(customer, pos2):
                route.add_customer(customer, pos1)  # Revert if infeasible
            
    elif operator == 'inter_relocate' and len(new_solution.routes) > 1:
        route1, route2 = random.sample(new_solution.routes, 2)
        # Add length check for both routes
        if len(route1.path) > 3 and len(route2.path) > 2:
            pos1 = random.randint(1, len(route1.path) - 2)
            pos2 = random.randint(1, len(route2.path) - 1)
            customer = route1.remove_customer(pos1)
            if not route2.add_customer(customer, pos2):
                route1.add_customer(customer, pos1)  # Revert if infeasible
                
    elif operator == 'inter_exchange' and len(new_solution.routes) > 1:
        route1, route2 = random.sample(new_solution.routes, 2)
        if len(route1.path) > 3 and len(route2.path) > 3:
            pos1 = random.randint(1, len(route1.path) - 2)
            pos2 = random.randint(1, len(route2.path) - 2)
            
            # Store original loads
            load1 = route1.current_load
            load2 = route2.current_load
            
            # Try exchange
            customer1 = route1.remove_customer(pos1)
            customer2 = route2.remove_customer(pos2)
            
            feasible = (route1.add_customer(customer2, pos1) and 
                       route2.add_customer(customer1, pos2))
            
            if not feasible:
                # Revert if infeasible
                route1.path = []
                route2.path = []
                route1.current_load = load1
                route2.current_load = load2
                route1.add_customer(customer1, pos1)
                route2.add_customer(customer2, pos2)
    
    return new_solution

def simulated_annealing(customers: List[Customer], depot: Customer,
                       vehicle_capacity: float,
                       initial_temp: float = 100, cooling_rate: float = 0.95,
                       min_temp: float = 0.1, max_iterations: int = 100) -> Solution:
    """Main Simulated Annealing algorithm"""
    
    current = create_initial_solution(customers, depot, vehicle_capacity)
    
    # Initialize best solution
    best = Solution([Route(depot, vehicle_capacity) for _ in current.routes])
    for i, route in enumerate(best.routes):
        route.path = [depot] + current.routes[i].path[1:-1] + [depot]  # Ensure depot at start/end
        route.current_load = current.routes[i].current_load
    
    temperature = initial_temp
    
    while temperature > min_temp and max_iterations > 0:
        neighbor = escape(current)
        delta = neighbor.objective_value() - current.objective_value()
        
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current = neighbor
            
            if current.objective_value() < best.objective_value():
                best = Solution([Route(depot, vehicle_capacity) for _ in current.routes])
                for i, route in enumerate(best.routes):
                    route.path = [depot] + current.routes[i].path[1:-1] + [depot]  # Ensure depot at start/end
                    route.current_load = current.routes[i].current_load
        
        temperature *= cooling_rate
        max_iterations -= 1
    
    return best


def main():
    file = 'data/c1type_vc200/C101.csv'
    VCAPACITY = 200
    allpoint = readData(file)
    DEPOT = allpoint[0]
    CUSTOMERS = allpoint[1:]
    # display(DEPOT)
    # display(CUSTOMERS)
    # initial_solution = create_initial_solution(CUSTOMERS, DEPOT, VCAPACITY)
    # print(initial_solution)
    best_solution = simulated_annealing(CUSTOMERS, DEPOT, VCAPACITY)
        
    # Print results
    for i, route in enumerate(best_solution.routes):
        print(f"Route {i + 1}:")
        print(f"Path: {[c.id for c in route.path]}")
        print(f"Load: {route.current_load}/{route.capacity}")
        print(f"Distance: {route.calculate_total_distance():.2f}")
        print("---")

if __name__ == "__main__":
    main()