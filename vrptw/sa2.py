import math
import random
import csv
import copy
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

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

def time_feasible_route(route, depot, distance_matrix):
    current_time = 0
    prev = depot
    for customer in route:
        # Travel time to customer
        arrival = current_time + distance_matrix[prev.id][customer.id]
        arrival = max(arrival, customer.ready_time)
        if arrival > customer.due_date:
            return False
        # Service time
        departure = arrival + customer.service_time
        current_time = departure
        prev = customer
    return True

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

def route_capacity_feasible(route, vehicle_capacity):
    total_demand = sum(c.demand for c in route)
    return total_demand <= vehicle_capacity

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
        route_capacity_feasible(new_route1, vehicle_capacity) and  # Use new helper
        route_capacity_feasible(new_route2, vehicle_capacity) and
        time_feasible_route(new_route1, depot, distance_matrix) and  # NEW: See Step 3
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

# Main Execution
# (Previous code remains the same until the Main Execution section)

# ====================== NEW FUNCTIONS ====================== #
def plot_routes(routes, depot, filename="routes.png"):
    plt.figure(figsize=(10, 10))
    
    # Plot depot
    plt.scatter(depot.x, depot.y, c='red', s=100, marker='s', edgecolors='black', label='Depot', zorder=10)
    
    # Plot customers and routes
    colors = plt.cm.tab20.colors  # 20 distinct colors
    for i, route in enumerate(routes):
        if not route:
            continue
        
        # Generate route coordinates (including depot at start/end)
        x = [depot.x] + [c.x for c in route] + [depot.x]
        y = [depot.y] + [c.y for c in route] + [depot.y]
        
        # Plot customers
        plt.scatter(
            [c.x for c in route], 
            [c.y for c in route], 
            color=colors[i % 20],
            s=50,
            label=f'Route {i+1}' if i < 20 else None
        )
        
        # Plot route path
        plt.plot(x, y, linestyle='-', linewidth=1, color=colors[i % 20])
    
    plt.title("Vehicle Routes")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Create output directory if not exists
    os.makedirs("output", exist_ok=True)
    plt.savefig(f"output/{filename}")
    plt.close()

def save_results(routes, depot, distance_matrix, filename="results.txt"):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{filename}", "w") as f:
        total_distance = 0
        total_vehicles = len(routes)
        
        f.write("Route Details:\n")
        f.write("="*50 + "\n")
        
        for i, route in enumerate(routes):
            route_distance = calculate_route_distance(route, depot, distance_matrix)
            total_distance += route_distance
            
            # Format route with depot at start/end
            route_ids = [depot.id] + [c.id for c in route] + [depot.id]
            
            f.write(f"Route {i+1}:\n")
            f.write(f"  Customers: {len(route)}\n")
            f.write(f"  Sequence: {route_ids}\n")
            f.write(f"  Distance: {route_distance:.2f}\n")
            f.write("-"*50 + "\n")
        
        f.write("\nSummary:\n")
        f.write("="*50 + "\n")
        f.write(f"Total Vehicles: {total_vehicles}\n")
        f.write(f"Total Distance: {total_distance:.2f}\n")

# ====================== UPDATED MAIN ====================== #
def main():
    depot, customers = load_data('data/rc1type_vc200/RC101.csv')
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
    
    # Save and plot initial solution
    save_results(initial_routes, depot, distance_matrix, "initial_results.txt")
    plot_routes(initial_routes, depot, "initial_routes.png")
    
    # Apply Simulated Annealing
    optimized_routes = simulated_annealing(
        initial_routes, 
        depot, 
        distance_matrix, 
        vehicle_capacity,
        initial_temp=1,  
        cooling_rate=0.995,
        iterations=100000
    )
    
    # Save and plot optimized solution
    save_results(optimized_routes, depot, distance_matrix, "optimized_results.txt")
    plot_routes(optimized_routes, depot, "optimized_routes.png")
    
    # Terminal output
    print("\nResults saved to:")
    print("- output/initial_results.txt")
    print("- output/initial_routes.png")
    print("- output/optimized_results.txt")
    print("- output/optimized_routes.png")

if __name__ == "__main__":
    main()