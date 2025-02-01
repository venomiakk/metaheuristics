import math
import random
import csv
import copy
from datetime import datetime, timedelta

# Data Parsing
class Customer:
    def __init__(self, id, x, y, demand, ready_time, due_date, service_time):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time

def load_data(file_path):
    customers = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            id = int(row[0])
            x = float(row[1])
            y = float(row[2])
            demand = float(row[3])
            ready_time = float(row[4])
            due_date = float(row[5])
            service_time = float(row[6])
            customers.append(Customer(id, x, y, demand, ready_time, due_date, service_time))
    depot = customers[0]
    customers = customers[1:]
    return depot, customers

# Distance Calculation (Euclidean)
def euclidean_distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

# Solomon's I1 Insertion Heuristic
def find_seed(customers, depot):
    # Seed selection: farthest from depot and earliest due date
    seed = max(customers, key=lambda c: (-euclidean_distance(c, depot), c.due_date))
    return seed

def time_feasible(route, customer, position, depot, distance_matrix):
    # Check time window feasibility after inserting customer at position
    current_time = 0
    current_load = 0
    prev = depot
    for i in range(len(route) + 1):
        if i == position:
            arrival = current_time + distance_matrix[prev.id][customer.id]
            arrival = max(arrival, customer.ready_time)
            departure = arrival + customer.service_time
            if arrival > customer.due_date:
                return False
            current_time = departure
            prev = customer
        if i < len(route):
            next_c = route[i]
            arrival = current_time + distance_matrix[prev.id][next_c.id]
            arrival = max(arrival, next_c.ready_time)
            if arrival > next_c.due_date:
                return False
            departure = arrival + next_c.service_time
            current_time = departure
            prev = next_c
    return True

def capacity_feasible(route, customer, vehicle_capacity):
    total_demand = sum(c.demand for c in route) + customer.demand
    return total_demand <= vehicle_capacity

def find_best_insertion(route, customer, depot, distance_matrix, vehicle_capacity):
    best_cost = float('inf')
    best_position = -1
    for i in range(len(route) + 1):
        if capacity_feasible(route, customer, vehicle_capacity) and time_feasible(route, customer, i, depot, distance_matrix):
            # Calculate insertion cost (increase in distance)
            if len(route) == 0:
                cost = distance_matrix[depot.id][customer.id] + distance_matrix[customer.id][depot.id]
            else:
                if i == 0:
                    prev = depot
                    next_c = route[0]
                elif i == len(route):
                    prev = route[-1]
                    next_c = depot
                else:
                    prev = route[i-1]
                    next_c = route[i]
                cost = distance_matrix[prev.id][customer.id] + distance_matrix[customer.id][next_c.id] - distance_matrix[prev.id][next_c.id]
            if cost < best_cost:
                best_cost = cost
                best_position = i
    return best_position, best_cost

def solomon_i1(depot, customers, distance_matrix, vehicle_capacity):
    routes = []
    unserved = customers.copy()
    
    while unserved:
        # Find seed customer
        seed = find_seed(unserved, depot)
        route = [seed]
        unserved.remove(seed)
        
        while True:
            best_customer = None
            best_position = -1
            best_cost = float('inf')
            
            for customer in unserved:
                pos, cost = find_best_insertion(route, customer, depot, distance_matrix, vehicle_capacity)
                if pos != -1 and cost < best_cost:
                    best_customer = customer
                    best_position = pos
                    best_cost = cost
            
            if best_customer:
                route.insert(best_position, best_customer)
                unserved.remove(best_customer)
            else:
                break
        
        routes.append(route)
    
    return routes

# Simulated Annealing
def calculate_route_distance(route, depot, distance_matrix):
    if not route:
        return 0
    total = distance_matrix[depot.id][route[0].id]
    for i in range(len(route)-1):
        total += distance_matrix[route[i].id][route[i+1].id]
    total += distance_matrix[route[-1].id][depot.id]
    return total

def calculate_objective(routes, depot, distance_matrix):
    num_vehicles = len(routes)
    total_distance = sum(calculate_route_distance(route, depot, distance_matrix) for route in routes)
    return num_vehicles * 1e6 + total_distance  # Prioritize fewer vehicles

def intra_relocate(route, depot, distance_matrix):
    if len(route) < 2:
        return route
    i = random.randint(0, len(route)-1)
    customer = route.pop(i)
    best_pos = -1
    best_cost = float('inf')
    for j in range(len(route)+1):
        new_route = route[:j] + [customer] + route[j:]
        if time_feasible(new_route, customer, j, depot, distance_matrix):
            cost = calculate_route_distance(new_route, depot, distance_matrix)
            if cost < best_cost:
                best_cost = cost
                best_pos = j
    if best_pos != -1:
        return route[:best_pos] + [customer] + route[best_pos:]
    else:
        route.insert(i, customer)  # Revert if no feasible position
        return route

def inter_relocate(routes, depot, distance_matrix, vehicle_capacity):
    if len(routes) < 2:
        return routes
    src_route_idx = random.randint(0, len(routes)-1)
    src_route = routes[src_route_idx]
    if len(src_route) == 0:
        return routes
    customer = src_route.pop(random.randint(0, len(src_route)-1))
    
    best_dest_idx = -1
    best_pos = -1
    best_cost = float('inf')
    for dest_route_idx in range(len(routes)):
        if dest_route_idx == src_route_idx:
            continue
        dest_route = routes[dest_route_idx]
        for j in range(len(dest_route)+1):
            new_route = dest_route[:j] + [customer] + dest_route[j:]
            if capacity_feasible(new_route, customer, vehicle_capacity) and time_feasible(new_route, customer, j, depot, distance_matrix):
                cost = calculate_route_distance(new_route, depot, distance_matrix)
                if cost < best_cost:
                    best_cost = cost
                    best_dest_idx = dest_route_idx
                    best_pos = j
    if best_dest_idx != -1:
        routes[best_dest_idx] = routes[best_dest_idx][:best_pos] + [customer] + routes[best_dest_idx][best_pos:]
        if len(src_route) == 0:
            routes.pop(src_route_idx)
        return routes
    else:
        src_route.append(customer)
        return routes

def simulated_annealing(initial_routes, depot, distance_matrix, vehicle_capacity, initial_temp=1000, cooling_rate=0.995, iterations=1000):
    current_solution = copy.deepcopy(initial_routes)
    best_solution = copy.deepcopy(current_solution)
    current_cost = calculate_objective(current_solution, depot, distance_matrix)
    best_cost = current_cost
    temp = initial_temp
    
    for _ in range(iterations):
        # Generate neighbor solution (escape move)
        neighbor = copy.deepcopy(current_solution)
        move_type = random.choice(['intra', 'inter'])
        if move_type == 'intra' and neighbor:
            route_idx = random.randint(0, len(neighbor)-1)
            neighbor[route_idx] = intra_relocate(neighbor[route_idx], depot, distance_matrix)
        elif move_type == 'inter':
            neighbor = inter_relocate(neighbor, depot, distance_matrix, vehicle_capacity)
        
        neighbor_cost = calculate_objective(neighbor, depot, distance_matrix)
        
        # Metropolis acceptance criterion
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost) / temp):
            current_solution = neighbor
            current_cost = neighbor_cost
            if neighbor_cost < best_cost:
                best_solution = copy.deepcopy(neighbor)
                best_cost = neighbor_cost
        
        # Cool down
        temp *= cooling_rate
    
    return best_solution

# Main Execution
# (Previous code remains the same until the Main Execution section)

# Modified Main Execution with depot display and SA tuning
if __name__ == "__main__":
    depot, customers = load_data('data/r1type_vc200/R101.csv')
    vehicle_capacity = 200
    
    # Precompute distance matrix
    all_nodes = [depot] + customers
    distance_matrix = {}
    for i in all_nodes:
        distance_matrix[i.id] = {}
        for j in all_nodes:
            distance_matrix[i.id][j.id] = euclidean_distance(i, j)
    
    # Generate initial solution
    initial_routes = solomon_i1(depot, customers, distance_matrix, vehicle_capacity)
    
    # Display initial routes with depot
    print("Initial Solution:")
    for i, route in enumerate(initial_routes):
        route_ids = [depot.id] + [c.id for c in route] + [depot.id]
        distance = calculate_route_distance(route, depot, distance_matrix)
        print(f"Route {i+1}: {route_ids}, Distance: {distance:.2f}")

    total_distance = sum(calculate_route_distance(route, depot, distance_matrix) for route in initial_routes)
    print(f"\nTotal Vehicles: {len(initial_routes)}, Total Distance: {total_distance:.2f}")
    
    # Apply Simulated Annealing with adjusted parameters
    optimized_routes = simulated_annealing(
        initial_routes, 
        depot, 
        distance_matrix, 
        vehicle_capacity,
        initial_temp=10000,  # Increased temperature
        cooling_rate=0.995,
        iterations=5000      # More iterations
    )
    
    # Display optimized routes with depot
    print("\nOptimized Solution:")
    for i, route in enumerate(optimized_routes):
        route_ids = [depot.id] + [c.id for c in route] + [depot.id]
        distance = calculate_route_distance(route, depot, distance_matrix)
        print(f"Route {i+1}: {route_ids}, Distance: {distance:.2f}")
    
    total_distance = sum(calculate_route_distance(route, depot, distance_matrix) for route in optimized_routes)
    print(f"\nTotal Vehicles: {len(optimized_routes)}, Total Distance: {total_distance:.2f}")