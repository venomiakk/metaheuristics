import numpy as np
from openpyxl import load_workbook
from algorithm import ParticleSwarmAlgorithm
from plots import plot_ackley, plot_himmelblaus, heatmap, histogram_ackley, histogram_himmelblaus
from datetime import datetime

glb_iterations = 50
glb_no_particles = 50
glb_inertia = 0.5
glb_social = 0.5
glb_cognitive = 0.5
no_runs = 5


def format_for_xlsx(title, xs, ys, vs, details):
    data = [[title[0]],
            [title[1]],
            ['', 'x', 'y', 'f(x, y)']]
    for i in range(no_runs):
        new_row = ['', xs[i], ys[i], vs[i]]
        data.append(new_row)
    data.append([])
    data.append(['', 'worst v', 'best v', 'avg v'])
    details.insert(0, '')
    data.append(details)
    return data


def save_to_xlsx(data):
    file_path = "res.xlsx"
    workbook = load_workbook(file_path)
    sheet = workbook.active

    new_data = data
    new_data.insert(0, [datetime.now()])

    last_row = sheet.max_row

    additional_rows = 3
    start_row = last_row + additional_rows + 1

    for i, row in enumerate(new_data, start=start_row):
        for j, value in enumerate(row, start=1):
            sheet.cell(row=i, column=j, value=value)

    workbook.save(file_path)


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

    worst_v = max(vs)
    best_v = min(vs)
    avg_v = np.average(vs)
    xs = [round(num, 6) for num in xs]
    ys = [round(num, 6) for num in ys]
    vs = [round(num, 6) for num in vs]
    print(f'Results - function: {function}, iters: {param}')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')
    print(f'best v: {best_v}, avg v: {avg_v}, worst v: {worst_v}')

    func = f'function: {function}'
    param_s = f'iters: {param}'
    title = [func, param_s]
    details = [worst_v, best_v, avg_v]
    data = format_for_xlsx(title, xs, ys, vs, details)
    save_to_xlsx(data)


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

    worst_v = max(vs)
    best_v = min(vs)
    avg_v = np.average(vs)
    xs = [round(num, 6) for num in xs]
    ys = [round(num, 6) for num in ys]
    vs = [round(num, 6) for num in vs]
    print(f'Results - function: {function}, particles: {param}')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')
    print(f'best v: {best_v}, avg v: {avg_v}, worst v: {worst_v}')

    func = f'function: {function}'
    param_s = f'particles: {param}'
    title = [func, param_s]
    details = [worst_v, best_v, avg_v]
    data = format_for_xlsx(title, xs, ys, vs, details)
    save_to_xlsx(data)


def experiment_inertia(param, function):
    xs, ys, vs = [], [], []
    for i in range(no_runs):
        obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=function,
                                     particle_inertia=param,
                                     particle_social=glb_social,
                                     particle_cognition=glb_cognitive, stop_condition=0, stop_value=glb_iterations)
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

    worst_v = max(vs)
    best_v = min(vs)
    avg_v = np.average(vs)
    xs = [round(num, 6) for num in xs]
    ys = [round(num, 6) for num in ys]
    vs = [round(num, 6) for num in vs]
    print(f'Results - function: {function}, inertia: {param}')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')
    print(f'best v: {best_v}, avg v: {avg_v}, worst v: {worst_v}')

    func = f'function: {function}'
    param_s = f'inertia: {param}'
    title = [func, param_s]
    details = [worst_v, best_v, avg_v]
    data = format_for_xlsx(title, xs, ys, vs, details)
    save_to_xlsx(data)


def experiment_cognitive(param, function):
    xs, ys, vs = [], [], []
    for i in range(no_runs):
        obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=function,
                                     particle_inertia=glb_inertia,
                                     particle_social=glb_social,
                                     particle_cognition=param, stop_condition=0, stop_value=glb_iterations)
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

    worst_v = max(vs)
    best_v = min(vs)
    avg_v = np.average(vs)
    xs = [round(num, 6) for num in xs]
    ys = [round(num, 6) for num in ys]
    vs = [round(num, 6) for num in vs]
    print(f'Results - function: {function}, cognitive: {param}')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')
    print(f'best v: {best_v}, avg v: {avg_v}, worst v: {worst_v}')

    func = f'function: {function}'
    param_s = f'cognitive: {param}'
    title = [func, param_s]
    details = [worst_v, best_v, avg_v]
    data = format_for_xlsx(title, xs, ys, vs, details)
    save_to_xlsx(data)


def experiment_social(param, function):
    xs, ys, vs = [], [], []
    for i in range(no_runs):
        obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=function,
                                     particle_inertia=glb_inertia,
                                     particle_social=param,
                                     particle_cognition=glb_cognitive, stop_condition=0, stop_value=glb_iterations)
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

    worst_v = max(vs)
    best_v = min(vs)
    avg_v = np.average(vs)
    xs = [round(num, 6) for num in xs]
    ys = [round(num, 6) for num in ys]
    vs = [round(num, 6) for num in vs]
    print(f'Results - function: {function}, social: {param}')
    print(f'x: {xs}')
    print(f'y: {ys}')
    print(f'v: {vs}')
    print(f'best v: {best_v}, avg v: {avg_v}, worst v: {worst_v}')

    func = f'function: {function}'
    param_s = f'social: {param}'
    title = [func, param_s]
    details = [worst_v, best_v, avg_v]
    data = format_for_xlsx(title, xs, ys, vs, details)
    save_to_xlsx(data)


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


def run_all_experiments():
    experiment_iters(25, 0)
    experiment_iters(50, 0)
    experiment_iters(100, 0)

    experiment_iters(25, 1)
    experiment_iters(50, 1)
    experiment_iters(100, 1)


if __name__ == '__main__':
    experiment_iters(25, 0)
    experiment_iters(50, 0)
    experiment_iters(100, 0)

    experiment_iters(25, 1)
    experiment_iters(50, 1)
    experiment_iters(100, 1)

    #TODO save plots to files
