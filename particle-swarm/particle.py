import numpy as np


class Particle:
    def __init__(self, x=0, y=0, inertia=0.5, cognition=0.5, social=0.5, function_borders=(-5, 5)):
        self.x = x
        self.y = y
        self.inertia = inertia
        self.cognition = cognition
        self.social = social

        self.function_borders = function_borders

        self.best_x = self.x
        self.best_y = self.y

        self.fitness = float('inf')
        self.best_fitness = self.fitness

        self.velocity_x = 0
        self.velocity_y = 0

    def calculate_fitnes(self, function):
        self.fitness = function(self.x, self.y)

        if self.fitness < self.best_fitness:
            self.best_fitness = self.fitness
            self.best_x = self.x
            self.best_y = self.y

    def update_position(self, best_particle, function_borders=True):
        social_rand = np.random.rand()
        cognitive_rand = np.random.rand()

        # inertia
        inertia_x = self.inertia * self.velocity_x
        inertia_y = self.inertia * self.velocity_y

        # social component
        social_distance = np.sqrt((best_particle.x - self.x) ** 2 + (best_particle.y - self.best_y) ** 2)
        social_x = (best_particle.x - self.x) / (social_distance + 1e-10)
        social_y = (best_particle.y - self.best_y) / (social_distance + 1e-10)
        social_component_x = self.social * social_rand * social_x
        social_component_y = self.social * social_rand * social_y

        # cognitive component
        cognitive_distance = np.sqrt((self.best_x - self.x) ** 2 + (self.best_y - self.y) ** 2)
        cognitive_x = (self.best_x - self.x) / (cognitive_distance + 1e-10)
        cognitive_y = (self.best_y - self.y) / (cognitive_distance + 1e-10)
        cognitive_component_x = self.cognition * cognitive_rand * cognitive_x
        cognitive_component_y = self.cognition * cognitive_rand * cognitive_y

        self.velocity_x = inertia_x + social_component_x + cognitive_component_x
        self.velocity_y = inertia_y + social_component_y + cognitive_component_y

        v_max = 5
        self.velocity_x = np.clip(self.velocity_x, -v_max, v_max)
        self.velocity_y = np.clip(self.velocity_y, -v_max, v_max)

        new_x = self.x + self.velocity_x
        new_y = self.y + self.velocity_y
        if function_borders:
            self.x = np.clip(new_x, self.function_borders[0], self.function_borders[1])
            self.y = np.clip(new_y, self.function_borders[0], self.function_borders[1])
        else:
            self.x = new_x
            self.y = new_y
