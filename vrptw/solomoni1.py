from utils import euclidean_distance
from utils import time_feasible, capacity_feasible

def find_seed(customers, depot):
    # Seed selection: farthest from depot and earliest due date
    seed = max(customers, key=lambda c: (-euclidean_distance(c, depot), c.due_date))
    return seed


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