import numpy as np
from particle import Particle
from functions import ackley, himmelblaus
from plots import plot_himmelblaus, plot_ackley


class ParticleSwarmAlgorithm:
    def __init__(self, number_of_particles=100, choosen_function=0, particle_inertia=0.5, particle_social=0.5,
                 particle_cognition=0.5, stop_condition=0, stop_value=75):
        self.number_of_particles = number_of_particles
        self.choosen_function = choosen_function
        self.particle_inertia = particle_inertia
        self.particle_social = particle_social
        self.particle_cognition = particle_cognition

        self.stop_condition = stop_condition
        self.stop_value = stop_value
        self.last_values = []
        self.number_of_last_values = 10

        self.function = ackley
        if self.choosen_function != 0:
            self.function = himmelblaus

        self.swarm = []
        # best particle
        self.best_particle = None
        self.best_particle_fitness = float('inf')

        # functions limits
        self.min_fvalue = -5
        self.max_fvalue = 5

    def run(self):
        iterations = 0
        self.__generate_swarm()
        self.__calculate_swarm_fitness()
        while True:
            # update position
            self.__update_swarm(function_borders=True)
            # calculate fitness for every particle
            self.__calculate_swarm_fitness()

            # stop condition
            iterations += 1
            if self.stop_condition == 0 and iterations >= self.stop_value:
                break
            elif self.stop_condition != 0:
                self.last_values.append(self.best_particle_fitness)
                if len(self.last_values) > self.number_of_last_values:
                    self.last_values.pop(0)
                    diff = np.mean(np.abs(np.diff(self.last_values)))
                    if diff < 0.01:
                        return iterations, self.best_particle

        return iterations, self.best_particle

    def __generate_swarm(self):
        x = np.random.uniform(self.min_fvalue, self.max_fvalue, self.number_of_particles)
        y = np.random.uniform(self.min_fvalue, self.max_fvalue, self.number_of_particles)

        for i in range(self.number_of_particles):
            self.swarm.append(Particle(x=x[i], y=y[i], inertia=self.particle_inertia, cognition=self.particle_cognition,
                                       social=self.particle_social))

    def __calculate_swarm_fitness(self):
        for particle in self.swarm:
            particle.calculate_fitnes(self.function)
            # get best particle
            if particle.fitness < self.best_particle_fitness:
                self.best_particle = particle
                self.best_particle_fitness = particle.fitness

    def __update_swarm(self, function_borders=True):
        for particle in self.swarm:
            particle.update_position2(best_particle=self.best_particle, function_borders=function_borders)

    def plot_particles(self, particles, best_particle):
        if self.choosen_function == 0:
            plot_ackley(particles, best_particle)
        else:
            plot_himmelblaus(particles, best_particle)
