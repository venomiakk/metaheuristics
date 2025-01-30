from typing import List, Tuple
from customer import Customer
from vehicle import Vehicle
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

        while len(population) < self.population_size:
            # warjacje obecnego rozwiązania
            new_solution = self.create_random_variation(deepcopy(initial_solution))
            if self.is_feasible_solution(new_solution):
                #TODO: never happens
                print('Feasible solution')
                population.append(new_solution)

        return population

    def create_random_variation(self, solution: List[Vehicle]) -> List[Vehicle]:
        
        for _ in range(random.randint(1, 3)):
            operation = random.choice(['swap','move','reverse'])

            if operation == 'swap':
                # zamiana dwóch losowych klientów między trasami
                if len(solution) >= 2:
                    route1, route2 = random.sample(solution, 2)
                    if len(route1.route) > 0 and len(route2.route) > 0:
                        pos1 = random.randint(0, len(route1.route) - 1)
                        pos2 = random.randint(0, len(route2.route) - 1)
                        route1.route[pos1], route2.route[pos2] = route2.route[pos2], route1.route[pos1]
            elif operation == 'move':
                # przeniesienie losowego klienta z jednej trasy na inną
                if len(solution) >= 2:
                    route1, route2 = random.sample(solution, 2)
                    if len(route1.route) > 0:
                        pos1 = random.randint(0, len(route1.route) - 1)
                        customer = route1.route.pop(pos1)
                        insert_pos = random.randint(0, len(route2.route))
                        route2.route.insert(insert_pos, customer)
            else: # reverse
                # odwrócenie kolejności klientów na losowej trasie
                if solution:
                    route = random.choice(solution)
                    if len(route.route) >= 2:
                        start = random.randint(0, len(route.route) - 2)
                        end = random.randint(start + 1, len(route.route))
                        route.route[start:end] = reversed(route.route[start:end])
        
        return solution

    def calculate_fitness(self, solution: List[Vehicle]) -> float:
        # mniej = lepiej
        if not self.is_feasible_solution(solution):
            return float('inf'), {}
        
        total_distance = 0
        total_time_window_violations = 0
        total_vehicles = len(solution)

        for vehicle in solution:
            if not vehicle.route:
                continue

            #* calculate route distance
            # * -----------------------
            active_vehicles += 1
            prev_point = self.depot
            current_time = 0
            for customer in vehicle.route:
                # distance calculation
                distance = self.calculate_distance(prev_point, customer)
                total_distance += distance

                #! time calcultaions
                travel_time = distance / vehicle.speed
                current_time = max(current_time + travel_time, customer.readytime)

                # time window violation
                if current_time > customer.duedate:
                    total_time_window_violations += current_time - customer.duedate

                current_time += customer.servicetime
                prev_point = customer

            #* return to depot
            # * --------------
            total_distance += self.calculate_distance(prev_point, self.depot)

        metrics = {
            'distance': total_distance,
            'vehicles': active_vehicles,
            'time_violations': total_time_window_violations
        }
        
        # TODO
        #! fitness - weights from class 
        fitness = (
            self.distance_weight * total_distance +
            self.vehicle_weight * active_vehicles +
            1000 * total_time_window_violations  # Heavy penalty for time window violations
        )
        
        return fitness, metrics

    def calculate_distance(self, point1: Customer, point2: Customer) -> float:
        #* change?
        return point1.calculateDst(point2)

    def is_feasible_solution(self, solution: List[Vehicle]) -> bool:
        visited_customers = set()

        for vehicle in solution:
            # print('is_feasible_solution 1st loop')
            current_load = 0
            current_time = 0
            prev_point = self.depot

            for customer in vehicle.route:
                # capacity check
                current_load += customer.demand
                if current_load > vehicle.capacity:
                    # print('Capacity failed')
                    return False
                
                # check for duplicate customers
                if customer.custno in visited_customers:
                    # print('Duplicate customer')
                    return False
                
                #! allows time window violations....
                visited_customers.add(customer.custno)

                # time window check
                distance = self.calculate_distance(prev_point, customer)
                travel_time = distance / vehicle.speed
                current_time = max(current_time + travel_time, customer.readytime)

                if current_time > customer.duedate:
                    # print('Due date failed')
                    return False
                
                #TODO:
                #? what about ready time?
                #? should it wait here?
                #? or should it return False?

                # visited_customers.add(customer.custno)
    
                current_time += customer.servicetime
                prev_point = customer

            # Check return to depot
            final_distance = self.calculate_distance(prev_point, self.depot)
            final_time = current_time + (final_distance / vehicle.speed)
            if final_time > vehicle.max_time:
                # print('Max time failed')
                return False
            
        #TODO:
        #? is this correct???
        #? what should be returned here?
        # Check if all customers are visited
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

    def mutate(self, solution: List[Vehicle]) -> List[Vehicle]:
        if random.random() < self.mutation_rate:
            solution = self.create_random_variation(solution)
        return solution

    def evolve(self, initial_solution: List[Vehicle]) -> List[Vehicle]:
        #* main GA loop
        population = self.create_initial_population(initial_solution)
        best_solution = None
        best_fitness = float('inf')
        progress_history = []

        for generation in range(self.generations):
            #* calculate fitness
            fitness_scores = [(solution, *self.calculate_fitness(solution))
                                for solution in population]
            fitness_scores.sort(key=lambda x: x[1])

            # upadate best solution
            if fitness_scores[0][1] < best_fitness:
                best_solution = deepcopy(fitness_scores[0][0])
                best_fitness = fitness_scores[0][1]
                best_metrics = fitness_scores[0][2]
                print(f"Generation: {generation}, new best fitness: {best_fitness}")

                print(f"Generation {generation}:")
                print(f"  Vehicles: {best_metrics['vehicles']}")
                print(f"  Total Distance: {best_metrics['distance']:.2f}")
                print(f"  Time Window Violations: {best_metrics['time_violations']:.2f}")

                progress_history.append(best_metrics)

            # select elite solution
            new_population = [solution for solution, _ in fitness_scores[:self.elite_size]]

            # create rest of new population
            while len(new_population) < self.population_size:
                # tournament selection
                parent1, _ = random.choice(fitness_scores[:len(fitness_scores)//2])
                parent2, _ = random.choice(fitness_scores[:len(fitness_scores)//2])

                # crossover and mutation
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)

                if self.is_feasible_solution(child):
                    new_population.append(child)

            population = new_population

        return best_solution

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
        generations=1000,
        mutation_rate=0.1,
        elite_size=10,
        vehicle_weight=vehicle_weight,
        distance_weight=distance_weight
    )
    
    optimized_solution, progress_history = ga.evolve(initial_solution)
    return optimized_solution, progress_history
    