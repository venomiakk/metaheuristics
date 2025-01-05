import numpy as np


class Particle:
    def __init__(self, x=0, y=0, inertia=0.5, cognition=0.5, social=0.5, function_borders=(-5, 5)):
        self.x = x
        self.y = y
        self.inertia = inertia
        ##
        self.inertia_x = inertia
        self.inertia_y = inertia
        ##
        self.cognition = cognition
        self.social = social

        self.function_borders = function_borders

        self.best_x = self.x
        self.best_y = self.y

        self.velocity = 0
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
        self.inertia = self.inertia * self.velocity
        # social component
        social_distance = np.sqrt((best_particle.x - self.x) ** 2 + (best_particle.y - self.best_y) ** 2)
        social_component = self.social * social_distance

        # cognitive component
        cognitive_component = self.cognition * (np.sqrt((self.best_x - self.x) ** 2 + (self.best_y - self.y) ** 2))

        self.velocity = self.inertia + social_component + cognitive_component
        new_x = self.x + self.velocity
        new_y = self.y + self.velocity
        if function_borders:
            if (self.function_borders[0] <= new_x <= self.function_borders[1] and
                    self.function_borders[0] <= new_y <= self.function_borders[1]):
                self.x = new_x
                self.y = new_y
        else:
            self.x = new_x
            self.y = new_y

    def update_position2(self, best_particle, function_borders=True):
        # inetrtia
        self.inertia_x = self.inertia_x * self.velocity_x
        self.inertia_y = self.inertia_y * self.velocity_y

        # social component
        social_distance = np.sqrt((best_particle.x - self.x) ** 2 + (best_particle.y - self.best_y) ** 2)
        social_x = (best_particle.x - self.x) / (social_distance + 1e-10)
        social_y = (best_particle.y - self.best_y) / (social_distance + 1e-10)

        # cognitive component
        cognitive_distance = np.sqrt((self.best_x - self.x) ** 2 + (self.best_y - self.y) ** 2)
        cognitive_x = (self.best_x - self.x) / (cognitive_distance + 1e-10)
        cognitive_y = (self.best_y - self.y) / (cognitive_distance + 1e-10)

        self.velocity_x = self.inertia_x + social_x + cognitive_x
        self.velocity_y = self.inertia_y + social_y + cognitive_y

        v_max = 5
        self.velocity_x = np.clip(self.velocity_x, -v_max, v_max)
        self.velocity_y = np.clip(self.velocity_y, -v_max, v_max)

        new_x = self.x + self.velocity_x
        new_y = self.y + self.velocity_y
        if function_borders:
            if (self.function_borders[0] <= new_x <= self.function_borders[1] and
                    self.function_borders[0] <= new_y <= self.function_borders[1]):
                self.x = new_x
                self.y = new_y
        else:
            self.x = new_x
            self.y = new_y
