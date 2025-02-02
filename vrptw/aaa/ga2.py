from copy import deepcopy
import random
import numpy as np
from v2.vehicle import Vehicle

class VRPTW_Genetic:
    def __init__(self, depot, customers, vehicle_capacity, 
                 population_size=100, generations=200, 
                 mutation_rate=0.3, elite_size=10):
        self.depot = depot
        self.customers = customers
        self.vehicle_capacity = vehicle_capacity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.best_fitness_history = []

    def create_initial_population(self):
        population = []
        # Create diverse initial population using different methods
        for i in range(self.population_size):
            if i < self.population_size // 3:
                # Pure random solutions
                unvisited = deepcopy(self.customers)
                random.shuffle(unvisited)
                solution = self.create_solution(unvisited)
            elif i < self.population_size * 2 // 3:
                # Nearest neighbor with randomization
                solution = self.create_nearest_neighbor_solution(randomization=0.3)
            else:
                # Clustered solutions
                solution = self.create_clustered_solution()
            population.append(solution)
        return population

    def create_nearest_neighbor_solution(self, randomization=0.3):
        vehicles = []
        unvisited = self.customers.copy()
        
        while unvisited:
            vehicle = Vehicle(self.vehicle_capacity, self.depot)
            vehicle.route.append(self.depot)
            
            while unvisited:
                current = vehicle.route[-1]
                # Sort customers by distance
                feasible = [(c, current.calculateDst(c)) for c in unvisited 
                           if vehicle.canFit(c) and vehicle.canMakeBackToDepotFromCustomer(c)]
                
                if not feasible:
                    break
                    
                # Sort by distance
                feasible.sort(key=lambda x: x[1])
                
                # Select customer with some randomization
                max_idx = min(len(feasible), max(3, int(len(feasible) * randomization)))
                chosen = random.choice(feasible[:max_idx])[0]
                
                if vehicle.canVisitInReadyTime(chosen):
                    vehicle.visit(chosen)
                else:
                    vehicle.waitForCustomer(chosen)
                    vehicle.visit(chosen)
                unvisited.remove(chosen)
            
            vehicle.route.append(self.depot)
            vehicles.append(vehicle)
        
        return vehicles

    def create_clustered_solution(self):
        # Simple clustering based on polar coordinates from depot
        customers = self.customers.copy()
        
        # Calculate angles and distances from depot
        customer_angles = []
        for c in customers:
            dx = c.xcord - self.depot.xcord
            dy = c.ycord - self.depot.ycord
            angle = np.arctan2(dy, dx)
            customer_angles.append((c, angle))
        
        # Sort by angle
        customer_angles.sort(key=lambda x: x[1])
        sorted_customers = [c[0] for c in customer_angles]
        
        # Create solution with sorted customers
        return self.create_solution(sorted_customers)

    def create_solution(self, customers):
        vehicles = []
        unvisited = customers.copy()
        
        while unvisited:
            vehicle = Vehicle(self.vehicle_capacity, self.depot)
            vehicle.route.append(self.depot)
            
            while unvisited:
                feasible_customers = [c for c in unvisited[:10] 
                                   if vehicle.canFit(c) and 
                                   vehicle.canMakeBackToDepotFromCustomer(c) and
                                   vehicle.canVisitBeforeDueDate(c)]
                
                if not feasible_customers:
                    break
                
                chosen = random.choice(feasible_customers)
                if vehicle.canVisitInReadyTime(chosen):
                    vehicle.visit(chosen)
                else:
                    vehicle.waitForCustomer(chosen)
                    vehicle.visit(chosen)
                unvisited.remove(chosen)
            
            vehicle.route.append(self.depot)
            vehicles.append(vehicle)
        
        return vehicles

    def fitness(self, solution):
        # More sophisticated fitness function
        total_distance = sum(v.calculateRouteDistance() for v in solution)
        num_vehicles = len(solution)
        
        # Penalties
        vehicle_penalty = num_vehicles * 1000  # Base vehicle penalty
        
        # Additional penalties for nearly empty routes
        utilization_penalty = 0
        for vehicle in solution:
            capacity_utilization = vehicle.current_load / vehicle.capacity
            if capacity_utilization < 0.5:  # Penalize routes using less than 50% capacity
                utilization_penalty += (0.5 - capacity_utilization) * 500
        
        return -(total_distance + vehicle_penalty + utilization_penalty)

    def select_parents(self, population):
        # Sort population by fitness
        population.sort(key=lambda x: self.fitness(x), reverse=True)
        
        # Keep elite solutions
        selected = deepcopy(population[:self.elite_size])
        
        # Create index-based selection
        population_size = len(population)
        ranks = list(range(1, population_size + 1))
        rank_sum = sum(ranks)
        probabilities = [r/rank_sum for r in reversed(ranks)]
        
        while len(selected) < self.population_size:
            # Select index based on probability
            idx = np.random.choice(population_size, p=probabilities)
            selected.append(deepcopy(population[idx]))
        
        return selected

    def crossover(self, parent1, parent2):
        # Enhanced route-based crossover
        child_routes = []
        
        # Randomly select complete routes from both parents
        all_routes = parent1 + parent2
        random.shuffle(all_routes)
        
        # Track included customers
        included_customers = set()
        
        # Add routes while maintaining feasibility
        for route in all_routes:
            route_customers = {c.custno for c in route.route[1:-1]}
            if not route_customers & included_customers:  # No overlap
                child_routes.append(deepcopy(route))
                included_customers.update(route_customers)
        
        # Handle missing customers
        missing_customers = []
        for customer in self.customers:
            if customer.custno not in included_customers:
                missing_customers.append(customer)
        
        if missing_customers:
            # Use nearest neighbor for missing customers
            additional_routes = self.create_nearest_neighbor_solution()
            child_routes.extend(additional_routes)
        
        return child_routes

    def mutate(self, solution):
        if random.random() < self.mutation_rate:
            # Apply multiple mutations with decreasing probability
            mutations = ['swap', 'insert', 'reverse', 'redistribute']
            for mutation in mutations:
                if random.random() < self.mutation_rate:
                    self._apply_mutation(solution, mutation)
    
    def _apply_mutation(self, solution, mutation_type):
        if mutation_type == 'redistribute':
            # Take a random route and redistribute its customers
            if len(solution) > 1:
                route_idx = random.randint(0, len(solution) - 1)
                customers = solution[route_idx].route[1:-1]  # Exclude depot
                solution.pop(route_idx)
                
                # Redistribute customers to nearest feasible routes
                for customer in customers:
                    min_dist = float('inf')
                    best_route = None
                    best_pos = None
                    
                    for route in solution:
                        if route.canFit(customer):
                            for i in range(1, len(route.route)):
                                # Check feasibility of insertion
                                route.route.insert(i, customer)
                                if (route.canMakeBackToDepotFromCustomer(customer) and 
                                    route.canVisitBeforeDueDate(customer)):
                                    dist = (route.route[i-1].calculateDst(customer) + 
                                          customer.calculateDst(route.route[i+1]))
                                    if dist < min_dist:
                                        min_dist = dist
                                        best_route = route
                                        best_pos = i
                                route.route.pop(i)
                    
                    if best_route is not None:
                        best_route.route.insert(best_pos, customer)
        
        elif mutation_type == 'swap':
            if len(solution) >= 2:
                route1, route2 = random.sample(solution, 2)
                if len(route1.route) > 2 and len(route2.route) > 2:
                    idx1 = random.randint(1, len(route1.route)-2)
                    idx2 = random.randint(1, len(route2.route)-2)
                    route1.route[idx1], route2.route[idx2] = route2.route[idx2], route1.route[idx1]
        
        elif mutation_type == 'insert':
            if solution:
                route = random.choice(solution)
                if len(route.route) > 3:
                    idx1 = random.randint(1, len(route.route)-2)
                    idx2 = random.randint(1, len(route.route)-2)
                    customer = route.route.pop(idx1)
                    route.route.insert(idx2, customer)
        
        elif mutation_type == 'reverse':
            if solution:
                route = random.choice(solution)
                if len(route.route) > 4:
                    idx1 = random.randint(1, len(route.route)-3)
                    idx2 = random.randint(idx1+1, len(route.route)-2)
                    route.route[idx1:idx2+1] = reversed(route.route[idx1:idx2+1])

    def optimize(self):
        population = self.create_initial_population()
        best_solution = None
        best_fitness = float('-inf')
        generations_without_improvement = 0
        
        for generation in range(self.generations):
            # Select parents
            parents = self.select_parents(population)
            
            # Create new population
            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(parents, 2)
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)
            
            # Add some fresh blood if stuck
            if generations_without_improvement > 20:
                num_new = self.population_size // 10
                new_population[-num_new:] = self.create_initial_population()[:num_new]
                generations_without_improvement = 0
            
            # Update population
            population = new_population
            
            # Track best solution
            current_best = max(population, key=lambda x: self.fitness(x))
            current_fitness = self.fitness(current_best)
            self.best_fitness_history.append(current_fitness)
            
            if current_fitness > best_fitness:
                best_fitness = current_fitness
                best_solution = deepcopy(current_best)
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1
            
            if generation % 10 == 0:
                print(f"Generation {generation}: Best fitness = {best_fitness}")
        
        return best_solution, best_fitness