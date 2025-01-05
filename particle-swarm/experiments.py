from algorithm import ParticleSwarmAlgorithm
from plots import plot_ackley, plot_himmelblaus

glb_iterations = 50
glb_no_particles = 100
glb_inertia = 0.5
glb_social = 0.5
glb_cognitive = 0.5
no_runs = 6


def experiment_iters(param, function):
    xs, ys, vs = [], [], []
    for i in range(no_runs):
        obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=function,
                                     particle_inertia=glb_inertia,
                                     particle_social=glb_social,
                                     particle_cognition=glb_cognitive, stop_condition=1, stop_value=param)
        iters, best_particle = obj.run()
        xs.append(best_particle.x)
        ys.append(best_particle.y)
        vs.append(best_particle.fitness)
        if function == 0:
            plot_ackley(particles=obj.swarm, best_particle=best_particle, iteration=param, inertia=glb_inertia,
                        social=glb_social,
                        cognition=glb_cognitive, no_particles=glb_no_particles)
        else:
            plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=param,
                             inertia=glb_inertia,
                             social=glb_social,
                             cognition=glb_cognitive, no_particles=glb_no_particles)
    print('Results:')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')


def experiment_no_particles(param, function):
    xs, ys, vs = [], [], []
    for i in range(no_runs):
        obj = ParticleSwarmAlgorithm(number_of_particles=param, choosen_function=function, particle_inertia=glb_inertia,
                                     particle_social=glb_social,
                                     particle_cognition=glb_cognitive, stop_condition=1, stop_value=glb_iterations)
        iters, best_particle = obj.run()
        xs.append(best_particle.x)
        ys.append(best_particle.y)
        vs.append(best_particle.fitness)
        if function == 0:
            plot_ackley(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations, inertia=glb_inertia,
                        social=glb_social,
                        cognition=glb_cognitive, no_particles=param)
        else:
            plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations,
                             inertia=glb_inertia,
                             social=glb_social,
                             cognition=glb_cognitive, no_particles=param)
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
        else:
            plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=param,
                             inertia=glb_inertia,
                             social=glb_social,
                             cognition=glb_cognitive, no_particles=glb_no_particles)
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
        else:
            plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations,
                             inertia=glb_inertia,
                             social=glb_social,
                             cognition=param, no_particles=glb_no_particles)
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
        else:
            plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations,
                             inertia=glb_inertia,
                             social=param,
                             cognition=glb_cognitive, no_particles=glb_no_particles)
    print('Results:')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')


def test():
    # arr = []
    # for i in range(30):
    #     obj = ParticleSwarmAlgorithm(number_of_particles=100, choosen_function=0, particle_inertia=0.5,
    #                                  particle_social=0.5,
    #                                  particle_cognition=0.5, stop_condition=0, stop_value=100)
    #     res = obj.run()
    #     arr.append(res)
    #
    # print(f'min: {min(arr)}, avg: {np.average(arr)}')

    obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=0, particle_inertia=glb_inertia,
                                 particle_social=glb_social,
                                 particle_cognition=glb_cognitive, stop_condition=1, stop_value=glb_iterations)
    iters, best_particle = obj.run()
    plot_ackley(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations, inertia=glb_inertia,
                social=glb_social,
                cognition=glb_cognitive, no_particles=glb_no_particles)

    obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=1, particle_inertia=glb_inertia,
                                 particle_social=glb_social,
                                 particle_cognition=glb_cognitive, stop_condition=1, stop_value=glb_iterations)
    iters, best_particle = obj.run()
    plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=glb_iterations, inertia=glb_inertia,
                     social=glb_social,
                     cognition=glb_cognitive, no_particles=glb_no_particles)


if __name__ == '__main__':
    experiment_inertia(0.3, 0)
