from customer import Customer
import numpy as np
from csvToPoints import getCustomersFromCSV

class AntColonyOptimization:
    def __init__(self,
                 n_ants: int = 20,
                 n_generations: int = 50,
                 population_size: int = 40,
                 alpha: float = 1.0,  # pheromone importance
                 beta: float = 2.0,   # heuristic importance
                 evaporation_rate: float = 0.1,
                 mutation_rate: float = 0.1):
        self.n_ants = n_ants
        self.n_generations = n_generations
        self.population_size = population_size
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.mutation_rate = mutation_rate

        self.depot, self.customers = getCustomersFromCSV('data/r1type_vc200/R101.csv')
        
        n_nodes = len(self.customers) + 1  # including depot
        self.pheromone = np.ones((n_nodes, n_nodes))
        self.distance_matrix = self._create_distance_matrix()

        # Initialize heuristic information (1/distance)
        self.heuristic = 1 / (self.distance_matrix + np.eye(n_nodes))
        print(self.heuristic)
        
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

    def update_pheromone(self):
        pass

if __name__ == '__main__':
    aco = AntColonyOptimization()
    