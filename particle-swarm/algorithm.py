import numpy as np


class ParticleSwarmAlgorithm:
    def __init__(self, number_of_particles):
        self.number_of_particles = number_of_particles

        self.swarm = []

    def __generate_swarm(self):
        x = np.random.uniform(-5, 5, self.number_of_particles)
        y = np.random.uniform(-5, 5, self.number_of_particles)
        pass
