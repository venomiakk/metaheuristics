import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt

class Customer:
    def __init__(self, id: int, x: float, y: float, demand: float, 
                 ready_time: float, due_time: float, service_time: float):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.ready_time = ready_time
        self.due_time = due_time
        self.service_time = service_time

class Vehicle:
    def __init__(self, capacity: float):
        self.capacity = capacity
        self.route = []

def load_data(filename: str) -> List[Customer]:
    customers = []
    df = pd.read_csv(filename, names=[
        'id', 'x', 'y', 'demand', 
        'ready_time', 'due_time', 'service_time'
    ])
    
    for _, row in df.iterrows():
        customers.append(Customer(
            id=row['id'],
            x=row['x'],
            y=row['y'], 
            demand=row['demand'],
            ready_time=row['ready_time'],
            due_time=row['due_time'],
            service_time=row['service_time']
        ))
    return customers

def kmeans_clustering(customers: List[Customer], num_clusters: int) -> Dict[int, List[Customer]]:
    coords = np.array([[c.x, c.y] for c in customers[1:]])
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=0, n_init=10)
    clusters = kmeans.fit_predict(coords)
    
    depot = customers[0]
    clustered_customers = {i: [depot] for i in range(num_clusters)}
    
    for i, cluster in enumerate(clusters):
        clustered_customers[cluster].append(customers[i+1])
    
    return clustered_customers

def calculate_distance(c1: Customer, c2: Customer) -> float:
    return euclidean([c1.x, c1.y], [c2.x, c2.y])

def calculate_route_distance(route: List[Customer]) -> float:
    dist = 0.0
    for i in range(len(route) - 1):
        dist += calculate_distance(route[i], route[i+1])
    return dist

def optimize_cluster(customers: List[Customer], 
                    num_ants: int = 20, 
                    num_iterations: int = 100,
                    alpha: float = 1.0,
                    beta: float = 2.0,
                    evaporation: float = 0.1) -> Tuple[List[List[Customer]], float]:
    
    depot = customers[0]
    customers_list = customers[1:]
    points = {c.id: np.array([c.x, c.y]) for c in customers}
    num_customers = len(customers_list)
    pheromones = np.ones((len(customers), len(customers)))
    best_routes = []
    best_total_distance = float('inf')
    
    for iteration in range(num_iterations):
        ant_routes = []
        ant_distances = []
        
        for _ in range(num_ants):
            current_load = 0
            current_time = 0
            current = depot
            route = [depot]
            unvisited = set(customers_list)
            
            while unvisited and current_load < 200:
                feasible = []
                
                for customer in unvisited:
                    travel_time = calculate_distance(current, customer)
                    arrival_time = current_time + travel_time
                    
                    if (arrival_time <= customer.due_time and 
                        current_load + customer.demand <= 200):
                        feasible.append(customer)
                
                if not feasible:
                    break
                    
                probs = []
                for next_customer in feasible:
                    distance = calculate_distance(current, next_customer)
                    pheromone = pheromones[customers.index(current)][customers.index(next_customer)]
                    prob = (pheromone ** alpha) * ((1.0 / distance) ** beta)
                    probs.append(prob)
                
                probs = np.array(probs) / sum(probs)
                next_customer = np.random.choice(feasible, p=probs)
                
                route.append(next_customer)
                unvisited.remove(next_customer)
                current = next_customer
                current_load += next_customer.demand
                current_time = max(arrival_time, next_customer.ready_time) + next_customer.service_time
            
            route.append(depot)
            distance = sum(calculate_distance(route[i], route[i+1]) 
                         for i in range(len(route)-1))
            
            ant_routes.append(route)
            ant_distances.append(distance)
        
        min_idx = np.argmin(ant_distances)
        if ant_distances[min_idx] < best_total_distance:
            best_routes = [ant_routes[min_idx]]
            best_total_distance = ant_distances[min_idx]
        
        pheromones *= (1 - evaporation)
        for route in best_routes:
            for i in range(len(route) - 1):
                pheromones[customers.index(route[i])][customers.index(route[i+1])] += 1.0 / best_total_distance
    
    return best_routes, best_total_distance

def calculate_solution_cost(routes: List[List[Customer]], vehicle_capacity: float) -> float:
    total_distance = 0
    vehicle_count = len(routes)
    for route in routes:
        load = sum(c.demand for c in route)
        if load > vehicle_capacity:
            return float('inf')  # Infeasible
        for i in range(len(route)-1):
            total_distance += calculate_distance(route[i], route[i+1])
    # Heavily penalize vehicle count
    cost = total_distance + (vehicle_count * 5000)
    return cost

def split_into_vehicles(customers: List[Customer], capacity: float) -> List[List[Customer]]:
    routes = []
    current_route = []
    current_load = 0
    for cust in customers:
        if current_load + cust.demand <= capacity:
            current_route.append(cust)
            current_load += cust.demand
        else:
            routes.append(current_route)
            current_route = [cust]
            current_load = cust.demand
    if current_route:
        routes.append(current_route)
    return routes

def merge_routes(routes: List[List[Customer]], capacity: float) -> List[List[Customer]]:
    merged = True
    while merged:
        merged = False
        for i in range(len(routes)):
            for j in range(i + 1, len(routes)):
                if sum(c.demand for c in routes[i] + routes[j]) <= capacity:
                    routes[i] += routes[j]
                    del routes[j]
                    merged = True
                    break
            if merged:
                break
    return routes

def plot_routes(final_routes):
    plt.figure(figsize=(8, 8))
    colors = plt.cm.get_cmap('tab20', len(final_routes))
    for idx, route in enumerate(final_routes):
        x_coords = [cust.x for cust in route]
        y_coords = [cust.y for cust in route]
        plt.plot(x_coords, y_coords, color=colors(idx), marker='o', label=f'Route {idx+1}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('VRPTW Routes')
    plt.legend()
    plt.show()

def main():
    customers = load_data('data/r1type_vc200/R101.csv')
    # Vehicle capacity
    vehicle_capacity = 200
    
    # Reduce number of clusters
    num_clusters = 10
    
    kmeans_data = kmeans_clustering(customers, num_clusters)
    
    final_routes = []
    for cluster_id, cluster_customers in kmeans_data.items():
        routes, distance = optimize_cluster(cluster_customers)  # ACO solution
        # Now split any route that exceeds capacity
        feasible_routes = []
        for r in routes:
            splitted = split_into_vehicles(r, vehicle_capacity)
            feasible_routes.extend(splitted)
        final_routes.extend(feasible_routes)

    # After splitting, attempt to merge feasible routes
    final_routes = merge_routes(final_routes, vehicle_capacity)
    cost = calculate_solution_cost(final_routes, vehicle_capacity)
    print(f"Total vehicles: {len(final_routes)}")
    print(f"Solution cost (distance + vehicle penalty): {cost}")
    plot_routes(final_routes)

if __name__ == "__main__":
    main()