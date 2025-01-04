class Particle:
    def __init__(self, x, y, inertia, cognition, social):
        self.x = x
        self.y = y
        self.inertia = inertia
        self.cognition = cognition
        self.social = social

        self.best_x = self.x
        self.best_y = self.y

        self.velocity = 0
        self.fitness = float('inf')
        self.best_fitness = self.fitness
