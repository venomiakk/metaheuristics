from customer import Customer
import numpy as np
from csvToPoints import getCustomersFromCSV
from copy import deepcopy
from vehicle import Vehicle
from ant import Ant

class AntColonyOptimization:
    def __init__(self,
                 n_ants: int = 20,
                 n_generations: int = 50,
                 alpha: float = 1.0,  # pheromone importance
                 beta: float = 2.0,   # heuristic importance
                 evaporation_rate: float = 0.1,):
        self.n_ants = n_ants
        self.n_generations = n_generations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate

        self.depot, self.customers = getCustomersFromCSV('data/r1type_vc200/R101.csv')
        self.max_time = self.depot.duedate
        self.max_capacity = 200

        n_nodes = len(self.customers) + 1  # including depot
        self.pheromones = np.ones((n_nodes, n_nodes))
        self.distance_matrix = self._create_distance_matrix()

    
    def test(self):
        ant = Ant()
        routes = self.build_routes(ant)
        print(routes)
        # for route in routes:
        #     for customer in route:
        #         print(customer.custno)
        
    def run(self):
        best_solution = None
        best_distance = float('inf')
        for _ in range(self.n_generations):
            ants = [Ant() for _ in range(self.n_ants)]
            for ant in ants:
                # ? Unvisited here or what???
                routes = self.build_routes(ant)
                ant.routes = routes
            
            best_ant_routes = self.select_best_route(ants)
            best_ant_len = sum([sum([customer.calculateDst(route[i + 1]) for i, customer in enumerate(route[:-1])]) for route in best_ant_routes])

            if best_ant_len < best_distance:
                best_solution = best_ant_routes
                best_distance = best_ant_len

            self.update_pheromones(ants)
        
        print(best_distance, best_solution)
        return best_solution, best_distance
    
    def build_routes(self, ant, unvisited=None):
        if unvisited is None:
            unvisited = deepcopy(self.customers)
        else:
            unvisited = deepcopy(unvisited)
        iters = 0
        ant.reset()
        # ant = Ant()

        current_location = self.depot
        new_vehicle = Vehicle(self.max_capacity, self.depot)
        new_vehicle.route.append(current_location)

        min_ready_time = min([customer.readytime for customer in unvisited])
        new_vehicle.current_time = min_ready_time
        
        ant.vehicle = new_vehicle
        
        visited = []
        # TODO Stop this loop when there is no more possible customers to visit
        # ? Should unvisited be all customers or just the ones that can be visited?
        while unvisited:
            iters += 1
            # print(len(unvisited))
            probablities = []
            for customer in unvisited:
                # ? if none can visit due to ready time - add this time to the current time
                if ant.vehicle.canVisit(customer):
                    # print(iters, customer.custno)
                    pheromone = (self.pheromones[current_location.custno - 1, customer.custno - 1]) ** self.alpha
                    distance = ant.vehicle.calculateDistance(customer)
                    heuristic = (1 / (distance + 1e-10)) ** self.beta
                    probablities.append((customer, pheromone * heuristic))

            # Normalize probabilities
            total_prob = sum([p[1] for p in probablities])
            probablities = [(p[0], p[1] / total_prob) for p in probablities]
            # print(iters, probablities)
            # Choose next customer (roulette wheel selection)
            if probablities:
                next_customer = np.random.choice([p[0] for p in probablities], p=[p[1] for p in probablities])
                ant.vehicle.visit(next_customer)
                unvisited.remove(next_customer)
                current_location = next_customer
            else:
                curr_time = ant.vehicle.current_time
                min_ready_time = min([customer.readytime for customer in unvisited if customer.readytime > curr_time])
                ant.vehicle.current_time = min_ready_time
                # print(min_ready_time, ant.vehicle.current_time, ant.vehicle.current_load)
                # print(len(unvisited))
                if not ant.vehicle.canVisitAnyOf(unvisited):
                    # print('No more customers can be visited')
                    ant.vehicle.current_time = curr_time
                    ant.vehicle.visit(self.depot)
                    ant.add_route(ant.vehicle.route)
                    # TODO Maybe possible to go back to depot and set of again after unloading
                    break
                # No more customers can be visited
                # TODO Check if this is right
                # ant.vehicle.visit(self.depot)
                # ant.add_route(ant.vehicle.route)
                # ? Maybe should wait for next min ready time
                # break
            
        # if ant.vehicle.route:
        #     ant.add_route(ant.vehicle.route)
        
        # print(iters)
        # print(ant.calculateDistanceSum())
        # TODO i guess it should return also visited customers
        # !
        # TODO Should every route in routes be a pair of points?????
        # !
        # And final route is a list of routes
        # print(ant.vehicle.current_time, ant.vehicle.current_load)
        return ant.routes

    def _create_distance_matrix(self) -> np.ndarray:
        n_nodes = len(self.customers) + 1
        matrix = np.zeros((n_nodes, n_nodes))
        all_nodes = [self.depot] + self.customers
        
        for i, node1 in enumerate(all_nodes):
            for j, node2 in enumerate(all_nodes):
                if i != j:
                    matrix[i,j] = node1.calculateDst(node2)
        return matrix
    
    def calculate_probabilities(self, current):
        probabilities = []

    def update_pheromones(self, ants):
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones[i])):
                self.pheromones[i,j] *= (1 - self.evaporation_rate)
        
        for ant in ants:
            for route in ant.routes:
                for i in range(len(route) - 1):
                    self.pheromones[route[i].custno - 1, route[i + 1].custno - 1] += 1 / ant.calculateDistanceSum()

    def select_best_route(self, ants):
        best_ant = min(ants, key=lambda ant: ant.calculateDistanceSum())
        return best_ant.routes

if __name__ == '__main__':
    aco = AntColonyOptimization()
    aco.run()
    