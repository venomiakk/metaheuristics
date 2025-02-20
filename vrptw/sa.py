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
    return num_vehicles * 1e6 + total_distance

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
        route.insert(i, customer)
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

    route1_idx, route2_idx = random.sample(range(len(routes)), 2)
    route1 = routes[route1_idx].copy()
    route2 = routes[route2_idx].copy()

    if not route1 or not route2:
        return routes

    customer1 = random.choice(route1)
    customer2 = random.choice(route2)

    new_route1 = [customer2 if c == customer1 else c for c in route1]
    new_route2 = [customer1 if c == customer2 else c for c in route2]

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

def cross_exchange(routes, depot, distance_matrix, vehicle_capacity):

    if len(routes) < 2:
        return routes
    
    route_a_idx, route_b_idx = random.sample(range(len(routes)), 2)
    route_a = routes[route_a_idx].copy()
    route_b = routes[route_b_idx].copy()
    
    if len(route_a) < 2 or len(route_b) < 2:
        return routes
    
    a_start, a_end = sorted(random.sample(range(len(route_a)), 2))
    b_start, b_end = sorted(random.sample(range(len(route_b)), 2))
    
    segment_a = route_a[a_start:a_end]
    segment_b = route_b[b_start:b_end]
    
    new_route_a = route_a[:a_start] + segment_b + route_a[a_end:]
    new_route_b = route_b[:b_start] + segment_a + route_b[b_end:]
    
    feasible = (
        route_capacity_feasible(new_route_a, vehicle_capacity) and
        route_capacity_feasible(new_route_b, vehicle_capacity) and
        time_feasible_route(new_route_a, depot, distance_matrix) and
        time_feasible_route(new_route_b, depot, distance_matrix)
    )
    
    if feasible:
        routes[route_a_idx] = new_route_a
        routes[route_b_idx] = new_route_b
    
    return routes

def route_merge(routes, depot, distance_matrix, vehicle_capacity):

    if len(routes) < 2:
        return routes
    
    route1_idx, route2_idx = random.sample(range(len(routes)), 2)
    route1 = routes[route1_idx].copy()
    route2 = routes[route2_idx].copy()
    
    merged_route = route1 + route2
    
    feasible = (
        route_capacity_feasible(merged_route, vehicle_capacity) and
        time_feasible_route(merged_route, depot, distance_matrix)
    )
    
    if feasible:
        routes = [route for idx, route in enumerate(routes) if idx not in (route1_idx, route2_idx)]
        routes.append(merged_route)
    
    return routes


def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    return 1 if val > 0 else 2


def on_segment(p, q, r):
    return (min(p.x, q.x) <= r.x <= max(p.x, q.x)) and (min(p.y, q.y) <= r.y <= max(p.y, q.y))

def segments_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(p1, q1, p2):
        return True
    if o2 == 0 and on_segment(p1, q1, q2):
        return True
    if o3 == 0 and on_segment(p2, q2, p1):
        return True
    if o4 == 0 and on_segment(p2, q2, q1):
        return True

    return False

def intra_two_opt(route, depot, distance_matrix):
    if len(route) < 4:
        return route

    for i in range(len(route) - 1):
        for j in range(i + 2, len(route) - 1):
            p1, q1 = route[i], route[i+1]
            p2, q2 = route[j], route[j+1]

            if segments_intersect(p1, q1, p2, q2):
                new_route = route[:i+1] + route[i+1:j+1][::-1] + route[j+1:]
                new_cost = calculate_route_distance(new_route, depot, distance_matrix)
                original_cost = calculate_route_distance(route, depot, distance_matrix)
                if new_cost < original_cost and time_feasible_route(new_route, depot, distance_matrix):
                    return new_route
    
    i, j = sorted(random.sample(range(len(route)), 2))
    new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
    new_cost = calculate_route_distance(new_route, depot, distance_matrix)
    original_cost = calculate_route_distance(route, depot, distance_matrix)
    if new_cost < original_cost and time_feasible_route(new_route, depot, distance_matrix):
        return new_route
    else:
        return route

def escape_move(current_solution, depot, distance_matrix, vehicle_capacity):
    neighbor = copy.deepcopy(current_solution)
    move_type = random.choices([
        'intra_relocate', 
        'inter_relocate', 
        'inter_exchange', 
        'cross_exchange', 
        'route_merge' 
    ],  weights=[1, 1, 1, 2, 3],
        k=1
    )[0]
    if move_type == 'intra_relocate' and neighbor:
        route_idx = random.randint(0, len(neighbor)-1)
        neighbor[route_idx] = intra_relocate(neighbor[route_idx], depot, distance_matrix)
    elif move_type == 'inter_relocate':
        neighbor = inter_relocate(neighbor, depot, distance_matrix, vehicle_capacity)
    elif move_type == 'inter_exchange':
        neighbor = inter_exchange(neighbor, depot, distance_matrix, vehicle_capacity)
    elif move_type == 'cross_exchange':
        neighbor = cross_exchange(neighbor, depot, distance_matrix, vehicle_capacity)
    elif move_type == 'route_merge':
        neighbor = route_merge(neighbor, depot, distance_matrix, vehicle_capacity)

    return neighbor

def local_search(solution, depot, distance_matrix, vehicle_capacity):
    improved = True
    best_solution = copy.deepcopy(solution)
    best_cost = calculate_objective(best_solution, depot, distance_matrix)
    while improved:
        improved = False
        for i in range(len(best_solution)):
            new_route = intra_two_opt(best_solution[i], depot, distance_matrix)
            if calculate_route_distance(new_route, depot, distance_matrix) < calculate_route_distance(best_solution[i], depot, distance_matrix):
                best_solution[i] = new_route
                improved = True

    return best_solution

def simulated_annealing(initial_routes, depot, distance_matrix, vehicle_capacity, initial_temp=1000, cooling_rate=0.995, iterations=1000):
    current_solution = copy.deepcopy(initial_routes)
    best_solution = copy.deepcopy(current_solution)
    current_cost = calculate_objective(current_solution, depot, distance_matrix)
    best_cost = current_cost
    temp = initial_temp
    
    for i in range(iterations):
        print(f'\rIteration {i+1}/{iterations}', end='', flush=True)

        neighbor = escape_move(current_solution, depot, distance_matrix, vehicle_capacity)
        neighbor = local_search(neighbor, depot, distance_matrix, vehicle_capacity)

        neighbor = [route for route in neighbor if len(route) > 0]
        neighbor_cost = calculate_objective(neighbor, depot, distance_matrix)
        
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost) / temp):
            current_solution = neighbor
            current_cost = neighbor_cost
            if neighbor_cost < best_cost:
                best_solution = copy.deepcopy(neighbor)
                best_cost = neighbor_cost
        
        temp *= cooling_rate
    
    return best_solution

def run_sa(filepath='data/rc1type_vc200/RC101.csv', vehicle_capacity=200, initial_temp=10, cooling_rate=0.995, iterations=10000):
    depot, customers = load_data(filepath)
    
    all_nodes = [depot] + customers
    distance_matrix = {}
    for i in all_nodes:
        distance_matrix[i.id] = {}
        for j in all_nodes:
            distance_matrix[i.id][j.id] = euclidean_distance(i, j)
    
    initial_routes = solomon_i1(depot, customers, distance_matrix, vehicle_capacity)
    
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

