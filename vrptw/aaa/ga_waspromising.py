from typing import List, Tuple
from customer import Customer
from v2.vehicle import Vehicle
from copy import deepcopy
import random

class GeneticVRPTW:
    def __init__(self, 
                 customers: List[Customer],
                 depot: Customer,
                 vehicle_capacity: float,
                 population_size: int = 100,
                 generations: int = 1000,
                 mutation_rate: float = 0.1,
                 elite_size: int = 10,
                 vehicle_weight: float = 10000,  
                 distance_weight: float = 1):
        self.customers = customers
        self.depot = depot
        self.vehicle_capacity = vehicle_capacity
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elite_size = elite_size
        self.vehicle_weight = vehicle_weight
        self.distance_weight = distance_weight
    
    def create_initial_population(self, initial_solution: List[Vehicle]) -> List[List[Vehicle]]:
        population = [deepcopy(initial_solution)]
        attempts = 0
        max_attempts = self.population_size * 10

        while len(population) < self.population_size and attempts < max_attempts:
            # warjacje obecnego rozwiązania
            new_solution = self.create_random_variation(deepcopy(initial_solution), max_operations=1)
            if self.is_feasible_solution(new_solution):
                population.append(new_solution)
            attempts += 1

        # if cannot create feasible solution, just duplicate initial solution
        while len(population) < self.population_size:
            population.append(deepcopy(initial_solution))

        return population

    def create_random_variation(self, solution: List[Vehicle], max_operations=1) -> List[Vehicle]:
        """Create a random variation while maintaining depot constraints"""
        for _ in range(random.randint(1, max_operations)):
            operation = random.choice(['swap', 'move'])
            
            if operation == 'swap':
                if len(solution) >= 2:
                    route1, route2 = random.sample(solution, 2)
                    if len(route1.route) > 0 and len(route2.route) > 0:
                        pos1 = random.randint(0, len(route1.route)-1)
                        pos2 = random.randint(0, len(route2.route)-1)
                        # Swap customers while maintaining route structure
                        route1.route[pos1], route2.route[pos2] = route2.route[pos2], route1.route[pos1]
            
            elif operation == 'move':
                if len(solution) >= 2:
                    route1, route2 = random.sample(solution, 2)
                    if len(route1.route) > 0:
                        pos1 = random.randint(0, len(route1.route)-1)
                        customer = route1.route.pop(pos1)
                        
                        # Insert maintaining depot -> customers -> depot structure
                        insert_pos = random.randint(0, len(route2.route))
                        route2.route.insert(insert_pos, customer)
        
        return solution

    def repair_route_structure(self, solution: List[Vehicle]) -> List[Vehicle]:
        """Ensure all routes properly start and end at depot"""
        for vehicle in solution:
            if not vehicle.route:
                continue
                
            # Reset the route timing from depot
            current_time = 0
            prev_point = self.depot
            
            # Recalculate times with proper depot start
            new_route = []
            for customer in vehicle.route:
                distance = self.calculate_distance(prev_point, customer)
                travel_time = distance / vehicle.speed
                arrival_time = max(current_time + travel_time, customer.readytime)
                
                if arrival_time <= customer.duedate:
                    new_route.append(customer)
                    current_time = arrival_time + customer.servicetime
                    prev_point = customer
            
            vehicle.route = new_route
            
        return solution

    def repair_solution(self, solution: List[Vehicle]) -> List[Vehicle]:
        """Try to repair an infeasible solution"""
        # Collect all customers
        all_customers = []
        for vehicle in solution:
            all_customers.extend(vehicle.route)
            vehicle.route = []
        
        # Sort by ready time
        all_customers.sort(key=lambda x: x.readytime)
        
        # Reassign customers to vehicles
        for customer in all_customers:
            assigned = False
            for vehicle in solution:
                # Try to insert customer in the best position
                best_pos = 0
                min_increase = float('inf')
                
                for i in range(len(vehicle.route) + 1):
                    test_route = vehicle.route[:i] + [customer] + vehicle.route[i:]
                    
                    # Check if this insertion is feasible
                    current_load = sum(c.demand for c in test_route)
                    if current_load > vehicle.capacity:
                        continue
                    
                    # Calculate time feasibility
                    current_time = 0
                    prev_point = self.depot
                    feasible = True
                    
                    for c in test_route:
                        distance = self.calculate_distance(prev_point, c)
                        travel_time = distance / vehicle.speed
                        current_time = max(current_time + travel_time, c.readytime)
                        
                        if current_time > c.duedate:
                            feasible = False
                            break
                        
                        current_time += c.servicetime
                        prev_point = c
                    
                    if feasible:
                        min_increase = current_time
                        best_pos = i
                        assigned = True
                        break
                
                if assigned:
                    vehicle.route.insert(best_pos, customer)
                    break
        
        return solution


    def calculate_fitness(self, solution: List[Vehicle]) -> Tuple[float, dict]:
        """Calculate fitness score with stronger emphasis on vehicle reduction"""
        if not self.is_feasible_solution(solution):
            return float('inf'), {}
        
        total_distance = 0
        total_time_window_violations = 0
        active_vehicles = 0
        empty_vehicles = 0
        
        for vehicle in solution:
            if not vehicle.route:
                empty_vehicles += 1
                continue
                
            active_vehicles += 1
            prev_point = self.depot
            current_time = 0
            
            for customer in vehicle.route:
                distance = self.calculate_distance(prev_point, customer)
                total_distance += distance
                
                travel_time = distance / vehicle.speed
                current_time = max(current_time + travel_time, customer.readytime)
                
                if current_time > customer.duedate:
                    total_time_window_violations += current_time - customer.duedate
                
                current_time += customer.servicetime
                prev_point = customer
            
            total_distance += self.calculate_distance(prev_point, self.depot)
        
        metrics = {
            'distance': total_distance,
            'vehicles': active_vehicles,
            'time_violations': total_time_window_violations,
            'empty_vehicles': empty_vehicles
        }
        
        # Much stronger penalty for number of vehicles
        fitness = (
            self.distance_weight * total_distance +
            self.vehicle_weight * (active_vehicles ** 2) +  # Quadratic penalty for vehicles
            1000 * total_time_window_violations
        )
        
        return fitness, metrics

    def calculate_distance(self, point1: Customer, point2: Customer) -> float:
        #* change?
        return point1.calculateDst(point2)

    def is_feasible_solution(self, solution: List[Vehicle]) -> bool:
        """Check if solution meets all constraints including depot start/end"""
        visited_customers = set()
        
        for vehicle in solution:
            current_load = 0
            current_time = 0
            
            # Skip empty routes
            if not vehicle.route:
                continue
                
            # Check if route starts and ends at depot
            if len(vehicle.route) == 0:
                continue  # Empty route is fine
                
            prev_point = self.depot  # Always start from depot
            
            for customer in vehicle.route:
                # Check capacity constraint
                current_load += customer.demand
                if current_load > vehicle.capacity:
                    return False
                
                # Check for duplicate customers
                if customer.custno in visited_customers:
                    return False
                
                # Check time windows
                distance = self.calculate_distance(prev_point, customer)
                travel_time = distance / vehicle.speed
                current_time = max(current_time + travel_time, customer.readytime)
                
                if current_time > customer.duedate:
                    return False
                    
                current_time += customer.servicetime
                prev_point = customer
                
                if customer.custno != 1:
                    visited_customers.add(customer.custno)
            
            # Check return to depot
            final_distance = self.calculate_distance(prev_point, self.depot)
            final_time = current_time + (final_distance / vehicle.speed)
            if final_time > vehicle.max_time:
                return False
        
        # Check if all customers are visited
        # print('Feasible solution')
        return len(visited_customers) == len(self.customers)
    
    def crossover(self, parent1: List[Vehicle], parent2: List[Vehicle]) -> List[Vehicle]:
        child = deepcopy(parent1)
        
        # Select random route from parent2
        if parent2:
            donor_route = random.choice(parent2)
            if donor_route.route:
                # Select random segment from donor route
                start = random.randint(0, len(donor_route.route)-1)
                length = random.randint(1, min(5, len(donor_route.route)-start))
                segment = donor_route.route[start:start+length]
                
                # Remove these customers from child
                customer_nos = {c.custno for c in segment}
                for vehicle in child:
                    vehicle.route = [c for c in vehicle.route 
                                   if c.custno not in customer_nos]
                
                # Insert segment into random position in child
                if child:
                    target_vehicle = random.choice(child)
                    insert_pos = random.randint(0, len(target_vehicle.route))
                    target_vehicle.route[insert_pos:insert_pos] = segment
        
        return child

    def try_eliminate_vehicle(self, solution: List[Vehicle]) -> List[Vehicle]:
        """Attempts to eliminate one vehicle by redistributing its customers"""
        # Only try if we have more than one vehicle
        if len(solution) <= 1:
            return solution
        
        # Make a copy to avoid modifying original
        new_solution = deepcopy(solution)
        
        # Try to eliminate each vehicle one by one
        for vehicle_idx in range(len(new_solution)):
            if not new_solution[vehicle_idx].route:
                continue
                
            test_solution = deepcopy(new_solution)
            target_vehicle = test_solution.pop(vehicle_idx)
            customers_to_redistribute = target_vehicle.route
            
            # Try to insert each customer into other routes
            success = True
            for customer in customers_to_redistribute:
                inserted = False
                
                # Try each remaining vehicle
                for other_vehicle in test_solution:
                    # Try each position in the route
                    for insert_pos in range(len(other_vehicle.route) + 1):
                        # Try inserting customer
                        other_vehicle.route.insert(insert_pos, customer)
                        
                        # Check if solution is still feasible
                        if self.is_feasible_solution(test_solution):
                            inserted = True
                            break
                        else:
                            # Remove if infeasible
                            other_vehicle.route.pop(insert_pos)
                    
                    if inserted:
                        break
                
                if not inserted:
                    success = False
                    break
            
            if success:
                return test_solution
        
        return new_solution

    def mutate(self, solution: List[Vehicle]) -> List[Vehicle]:
        """Apply mutation operators to a solution with vehicle elimination attempt"""
        if random.random() < self.mutation_rate:
            solution = self.create_random_variation(solution)
            
        # Try to eliminate a vehicle with some probability
        if random.random() < 0.2:  # 20% chance to try vehicle elimination
            improved_solution = self.try_eliminate_vehicle(solution)
            if self.is_feasible_solution(improved_solution):
                solution = improved_solution
        
        return solution

    def evolve(self, initial_solution: List[Vehicle]) -> Tuple[List[Vehicle], List[dict]]:
        """Main genetic algorithm loop with progress tracking"""
        # Initialize population
        if not self.is_feasible_solution(initial_solution):
            print("Warning: Initial solution is not feasible!")
        else:
            print("Initial solution is feasible")
            
        population = self.create_initial_population(initial_solution)
        best_solution = None
        best_fitness = float('inf')
        progress_history = []
        generations_without_improvement = 0
        
        for generation in range(self.generations):
            print(f"Generation {generation}... out of {self.generations}")
            # Evaluate fitness for all solutions
            fitness_scores = [(solution, *self.calculate_fitness(solution)) 
                            for solution in population]
            fitness_scores.sort(key=lambda x: x[1])  # Sort by fitness value
            
            # Update best solution
            current_best_fitness = fitness_scores[0][1]
            if current_best_fitness < best_fitness:
                best_solution = deepcopy(fitness_scores[0][0])
                print('Best solution updated')
                print(best_solution)
                best_fitness = current_best_fitness
                best_metrics = fitness_scores[0][2]
                generations_without_improvement = 0
                
                print(f"Generation {generation}:")
                print(f"  Vehicles: {best_metrics['vehicles']}")
                print(f"  Total Distance: {best_metrics['distance']:.2f}")
                print(f"  Time Window Violations: {best_metrics['time_violations']:.2f}")
                
                progress_history.append(best_metrics)
            else:
                generations_without_improvement += 1
                
            # Early stopping if no improvement for many generations
            if generations_without_improvement > 100:
                print(f"Stopping early - no improvement for {generations_without_improvement} generations")
                break
                
            # Select elite solutions
            elite_solutions = [solution for solution, _, _ in fitness_scores[:self.elite_size]]
            
            # Create new population
            new_population = elite_solutions.copy()  # Keep elite solutions
            
            # Fill rest of population with children
            while len(new_population) < self.population_size:
                # Tournament selection
                tournament_size = 5
                parent1 = None
                parent2 = None
                
                # Select first parent
                tournament = random.sample(fitness_scores, tournament_size)
                tournament.sort(key=lambda x: x[1])  # Sort by fitness
                parent1 = tournament[0][0]  # Take the best
                
                # Select second parent
                tournament = random.sample(fitness_scores, tournament_size)
                tournament.sort(key=lambda x: x[1])
                parent2 = tournament[0][0]
                
                # Create and mutate child
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)

                child = self.repair_route_structure(child)
                
                # # Try to repair if infeasible
                # if not self.is_feasible_solution(child):
                #     child = self.repair_solution(child)
                
                # Add child if feasible
                if self.is_feasible_solution(child):
                    new_population.append(child)
                else:
                    # If child is not feasible, add a random elite solution
                    new_population.append(deepcopy(random.choice(elite_solutions)))
            
            # Replace old population
            population = new_population
            
            # Optional: Add some random fresh solutions occasionally to maintain diversity
            if generation % 20 == 0:
                num_random = self.population_size // 10  # 10% random solutions
                for _ in range(num_random):
                    random_solution = self.create_random_variation(deepcopy(initial_solution), max_operations=1)
                    if self.is_feasible_solution(random_solution):
                        # Replace a random non-elite solution
                        idx = random.randint(self.elite_size, len(population)-1)
                        population[idx] = random_solution
        
        if best_solution is None:
            print("Warning: No feasible solution found!")
            return initial_solution, progress_history
        
        return best_solution, progress_history

def optimize_vrptw(customers: List[Customer], 
                  depot: Customer,
                  initial_solution: List[Vehicle],
                  vehicle_capacity: float,
                  vehicle_weight: float = 10000,   # Weight for vehicle minimization
                  distance_weight: float = 1) -> Tuple[List[Vehicle], List[dict]]:
    """Wrapper function to run the genetic algorithm with configurable weights"""
    ga = GeneticVRPTW(
        customers=customers,
        depot=depot,
        vehicle_capacity=vehicle_capacity,
        population_size=100,
        generations=100,
        mutation_rate=0.2,
        elite_size=20,
        vehicle_weight=vehicle_weight,
        distance_weight=distance_weight
    )
    # print(ga.is_feasible_solution(initial_solution))
    # return None, None
    optimized_solution, progress_history = ga.evolve(initial_solution)
    return optimized_solution, progress_history