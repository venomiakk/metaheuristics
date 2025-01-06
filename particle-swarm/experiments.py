from algorithm import ParticleSwarmAlgorithm
from plots import plot_ackley, plot_himmelblaus, heatmap, histogram_ackley, histogram_himmelblaus

glb_iterations = 50
glb_no_particles = 100
glb_inertia = 0.1
glb_social = 0.5
glb_cognitive = 0.5
no_runs = 6


def experiment_iters(param, function):
    xs, ys, vs = [], [], []
    for i in range(no_runs):
        obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=function,
                                     particle_inertia=glb_inertia,
                                     particle_social=glb_social,
                                     particle_cognition=glb_cognitive, stop_condition=0, stop_value=param)
        iters, best_particle = obj.run()
        xs.append(best_particle.x)
        ys.append(best_particle.y)
        vs.append(best_particle.fitness)
        if function == 0:
            plot_ackley(particles=obj.swarm, best_particle=best_particle, iteration=param, inertia=glb_inertia,
                        social=glb_social,
                        cognition=glb_cognitive, no_particles=glb_no_particles)
            histogram_ackley(obj.swarm)
        else:
            plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=param,
                             inertia=glb_inertia,
                             social=glb_social,
                             cognition=glb_cognitive, no_particles=glb_no_particles)
            histogram_himmelblaus(obj.swarm)

    print('Results:')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')


def experiment_no_particles(param, function):
    xs, ys, vs = [], [], []
    for i in range(no_runs):
        obj = ParticleSwarmAlgorithm(number_of_particles=param, choosen_function=function, particle_inertia=glb_inertia,
                                     particle_social=glb_social,
                                     particle_cognition=glb_cognitive, stop_condition=0, stop_value=glb_iterations)
        iters, best_particle = obj.run()
        xs.append(best_particle.x)
        ys.append(best_particle.y)
        vs.append(best_particle.fitness)
        if function == 0:
            plot_ackley(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations, inertia=glb_inertia,
                        social=glb_social,
                        cognition=glb_cognitive, no_particles=param)
            histogram_ackley(obj.swarm)
        else:
            plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations,
                             inertia=glb_inertia,
                             social=glb_social,
                             cognition=glb_cognitive, no_particles=param)
            histogram_himmelblaus(obj.swarm)

    print('Results:')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')


def experiment_inertia(param, function):
    xs, ys, vs = [], [], []
    for i in range(no_runs):
        obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=function,
                                     particle_inertia=param,
                                     particle_social=glb_social,
                                     particle_cognition=glb_cognitive, stop_condition=1, stop_value=glb_iterations)
        iters, best_particle = obj.run()
        xs.append(best_particle.x)
        ys.append(best_particle.y)
        vs.append(best_particle.fitness)
        if function == 0:
            plot_ackley(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations, inertia=param,
                        social=glb_social,
                        cognition=glb_cognitive, no_particles=glb_no_particles)
            histogram_ackley(obj.swarm)
        else:
            plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=param,
                             inertia=glb_inertia,
                             social=glb_social,
                             cognition=glb_cognitive, no_particles=glb_no_particles)
            histogram_himmelblaus(obj.swarm)

    print('Results:')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')


def experiment_cognitive(param, function):
    xs, ys, vs = [], [], []
    for i in range(no_runs):
        obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=function,
                                     particle_inertia=glb_inertia,
                                     particle_social=glb_social,
                                     particle_cognition=param, stop_condition=1, stop_value=glb_iterations)
        iters, best_particle = obj.run()
        xs.append(best_particle.x)
        ys.append(best_particle.y)
        vs.append(best_particle.fitness)
        if function == 0:
            plot_ackley(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations, inertia=glb_inertia,
                        social=glb_social,
                        cognition=param, no_particles=glb_no_particles)
            histogram_ackley(obj.swarm)
        else:
            plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations,
                             inertia=glb_inertia,
                             social=glb_social,
                             cognition=param, no_particles=glb_no_particles)
            histogram_himmelblaus(obj.swarm)

    print('Results:')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')


def experiment_social(param, function):
    xs, ys, vs = [], [], []
    for i in range(no_runs):
        obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=function,
                                     particle_inertia=glb_inertia,
                                     particle_social=param,
                                     particle_cognition=glb_cognitive, stop_condition=1, stop_value=glb_iterations)
        iters, best_particle = obj.run()
        xs.append(best_particle.x)
        ys.append(best_particle.y)
        vs.append(best_particle.fitness)
        if function == 0:
            plot_ackley(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations, inertia=glb_inertia,
                        social=param,
                        cognition=glb_cognitive, no_particles=glb_no_particles)
            histogram_ackley(obj.swarm)
        else:
            plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations,
                             inertia=glb_inertia,
                             social=param,
                             cognition=glb_cognitive, no_particles=glb_no_particles)
            histogram_himmelblaus(obj.swarm)

    print('Results:')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')


def test_ackley():
    obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=0, particle_inertia=glb_inertia,
                                 particle_social=glb_social,
                                 particle_cognition=glb_cognitive, stop_condition=0, stop_value=glb_iterations)
    iters, best_particle = obj.run()
    plot_ackley(particles=obj.swarm, best_particle=best_particle, iteration=iters, inertia=glb_inertia,
                social=glb_social,
                cognition=glb_cognitive, no_particles=glb_no_particles)
    print(best_particle.x, best_particle.y, best_particle.fitness, obj.best_particle_fitness)
    print(obj.best_particle.x, obj.best_particle.y, obj.best_particle.fitness)
    heatmap(obj.all_particles)
    histogram_ackley(obj.swarm)


def test_himmelblaus():
    obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=1, particle_inertia=glb_inertia,
                                 particle_social=glb_social,
                                 particle_cognition=glb_cognitive, stop_condition=0, stop_value=glb_iterations)
    iters, best_particle = obj.run()
    plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=iters, inertia=glb_inertia,
                     social=glb_social,
                     cognition=glb_cognitive, no_particles=glb_no_particles)
    print(best_particle.x, best_particle.y, best_particle.fitness, obj.best_particle_fitness)
    print(obj.best_particle.x, obj.best_particle.y, obj.best_particle.fitness)
    heatmap(obj.all_particles)
    histogram_himmelblaus(obj.swarm)


if __name__ == '__main__':
    test_himmelblaus()
    test_ackley()
