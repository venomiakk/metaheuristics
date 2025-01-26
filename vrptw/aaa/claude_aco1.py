import math
import random
import numpy as np

class Customer:
    def __init__(self, id, x, y, demand, ready_time, due_date, service_time):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time

class VRPTW_ACO:
    def __init__(self, customers, num_ants, alpha=1, beta=2, evaporation_rate=0.5, Q=100, vehicle_capacity=200):
        self.customers = customers
        self.depot = customers[0]
        self.num_customers = len(customers)
        self.num_ants = num_ants
        self.alpha = alpha  # pheromone importance
        self.beta = beta    # heuristic importance
        self.evaporation_rate = evaporation_rate
        self.Q = Q  # pheromone deposit factor
        self.vehicle_capacity = vehicle_capacity
        
        # Calculate distance matrix
        self.distance_matrix = self._calculate_distance_matrix()
        
        # Initialize pheromone matrix
        self.pheromone_matrix = np.ones((self.num_customers, self.num_customers))
    
    def _calculate_distance(self, customer1, customer2):
        return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)
    
    def _calculate_distance_matrix(self):
        matrix = np.zeros((self.num_customers, self.num_customers))
        for i in range(self.num_customers):
            for j in range(self.num_customers):
                matrix[i][j] = self._calculate_distance(self.customers[i], self.customers[j])
        return matrix
    
    def _is_feasible_route(self, route):
        current_time = 0
        current_load = 0
        
        for i in range(len(route)):
            customer = self.customers[route[i]]
            
            # Check vehicle capacity
            if current_load + customer.demand > self.vehicle_capacity:
                return False
            
            # Update current load
            current_load += customer.demand
            
            # Check time window constraints
            current_time = max(current_time, customer.ready_time)
            current_time += customer.service_time
            
            if current_time > customer.due_date:
                return False
        
        return True
    
    def _calculate_route_cost(self, route):
        total_distance = 0
        current_time = 0
        
        # Start from depot
        current_customer = self.depot
        
        for i in route:
            next_customer = self.customers[i]
            
            # Calculate travel distance and time
            distance = self.distance_matrix[current_customer.id-1][next_customer.id-1]
            total_distance += distance
            
            # Update time considering time windows
            current_time = max(current_time + distance, next_customer.ready_time)
            current_time += next_customer.service_time
            
            current_customer = next_customer
        
        # Return to depot
        total_distance += self.distance_matrix[current_customer.id-1][self.depot.id-1]
        
        return total_distance
    
    def solve(self, max_iterations=100):
        best_route = None
        best_cost = float('inf')
        
        for _ in range(max_iterations):
            # Generate routes for each ant
            routes = self._construct_routes()
            
            # Evaluate routes
            for route in routes:
                if self._is_feasible_route(route):
                    route_cost = self._calculate_route_cost(route)
                    if route_cost < best_cost:
                        best_route = route
                        best_cost = route_cost
            
            # Update pheromones
            self._update_pheromones(routes)
        
        return best_route, best_cost
    
    def _construct_routes(self):
        routes = []
        
        for _ in range(self.num_ants):
            route = []
            unvisited = set(range(1, self.num_customers))  # exclude depot
            
            while unvisited:
                # Probabilistic selection based on pheromones and distance
                probabilities = self._calculate_transition_probabilities(route, unvisited)
                selected_customer = self._select_next_customer(probabilities)
                
                route.append(selected_customer)
                unvisited.remove(selected_customer)
            
            routes.append(route)
        
        return routes
    
    def _calculate_transition_probabilities(self, current_route, unvisited):
        probabilities = {}
        
        for customer in unvisited:
            # Calculate transition probability
            pheromone = self.pheromone_matrix[current_route[-1] if current_route else 0][customer] ** self.alpha
            heuristic = (1 / self.distance_matrix[current_route[-1] if current_route else 0][customer]) ** self.beta
            probabilities[customer] = pheromone * heuristic
        
        # Normalize probabilities
        total = sum(probabilities.values())
        return {k: v/total for k, v in probabilities.items()}
    
    def _select_next_customer(self, probabilities):
        r = random.random()
        cumulative = 0
        
        for customer, prob in probabilities.items():
            cumulative += prob
            if r <= cumulative:
                return customer
    
    def _update_pheromones(self, routes):
        # Evaporation
        self.pheromone_matrix *= (1 - self.evaporation_rate)
        
        # Deposit pheromones
        for route in routes:
            route_cost = self._calculate_route_cost(route)
            for i in range(len(route) - 1):
                self.pheromone_matrix[route[i]][route[i+1]] += self.Q / route_cost

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

# Parse customer data
customers = csvToPoints('data/r1type_vc200/R106.csv')

# Create and solve VRPTW problem
vrptw_solver = VRPTW_ACO(customers, num_ants=10)
best_route, best_cost = vrptw_solver.solve()

print("Best Route:", best_route)
print("Best Cost:", best_cost)