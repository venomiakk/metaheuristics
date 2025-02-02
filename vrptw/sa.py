import random
import copy
import math
from utils import time_feasible, capacity_feasible, route_capacity_feasible, time_feasible_route, euclidean_distance, load_data
from solomoni1 import solomon_i1


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

def inter_exchange(routes, depot, distance_matrix, vehicle_capacity):
    if len(routes) < 2:
        return routes

    # Select two distinct routes
    route1_idx, route2_idx = random.sample(range(len(routes)), 2)
    route1 = routes[route1_idx].copy()
    route2 = routes[route2_idx].copy()

    if not route1 or not route2:
        return routes

    # Randomly select customers to swap
    customer1 = random.choice(route1)
    customer2 = random.choice(route2)

    # Swap customers
    new_route1 = [customer2 if c == customer1 else c for c in route1]
    new_route2 = [customer1 if c == customer2 else c for c in route2]

    # Check feasibility after swap
    feasible = (
        route_capacity_feasible(new_route1, vehicle_capacity) and
        route_capacity_feasible(new_route2, vehicle_capacity) and
        time_feasible_route(new_route1, depot, distance_matrix) and
        time_feasible_route(new_route2, depot, distance_matrix)
    )

    if feasible:
        routes[route1_idx] = new_route1
        routes[route2_idx] = new_route2

    return routes

def simulated_annealing(initial_routes, depot, distance_matrix, vehicle_capacity, initial_temp=1000, cooling_rate=0.995, iterations=1000):
    current_solution = copy.deepcopy(initial_routes)
    best_solution = copy.deepcopy(current_solution)
    current_cost = calculate_objective(current_solution, depot, distance_matrix)
    best_cost = current_cost
    temp = initial_temp
    
    for i in range(iterations):
        print(f'\rIteration {i+1}/{iterations}', end='', flush=True)
        # Generate neighbor solution (escape move)
        neighbor = copy.deepcopy(current_solution)
        move_type = random.choice(['intra_relocate', 'inter_relocate', 'inter_exchange'])
        if move_type == 'intra_relocate' and neighbor:
            route_idx = random.randint(0, len(neighbor)-1)
            neighbor[route_idx] = intra_relocate(neighbor[route_idx], depot, distance_matrix)
        elif move_type == 'inter_relocate':
            neighbor = inter_relocate(neighbor, depot, distance_matrix, vehicle_capacity)
        elif move_type == 'inter_exchange':
            neighbor = inter_exchange(neighbor, depot, distance_matrix, vehicle_capacity)
        
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

def run_sa(filepath='data/rc1type_vc200/RC101.csv', vehicle_capacity=200, initial_temp=10, cooling_rate=0.995, iterations=10000):
    depot, customers = load_data(filepath)
    
    # Precompute distance matrix
    all_nodes = [depot] + customers
    distance_matrix = {}
    for i in all_nodes:
        distance_matrix[i.id] = {}
        for j in all_nodes:
            distance_matrix[i.id][j.id] = euclidean_distance(i, j)
    
    # Generate initial solution
    initial_routes = solomon_i1(depot, customers, distance_matrix, vehicle_capacity)
    
    
    # Apply Simulated Annealing
    optimized_routes = simulated_annealing(
        initial_routes, 
        depot, 
        distance_matrix, 
        vehicle_capacity,
        initial_temp=initial_temp,  
        cooling_rate=cooling_rate,
        iterations=iterations
    )
    
    return initial_routes, optimized_routes, depot, distance_matrix

