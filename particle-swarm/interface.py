from algorithm import ParticleSwarmAlgorithm
from plots import plot_himmelblaus, plot_ackley, histogram_himmelblaus, histogram_ackley


def console_interface():
    glb_no_particles = 100
    glb_inertia = 0.5
    glb_social = 0.5
    glb_cognitive = 0.5
    glb_function = 0
    glb_stop = 75
    glb_stop_cond = 0

    glb_function = int(input("Wybierz funkcje:\n 0. Ackley\n 1. Himmelblau\n: "))
    glb_stop_cond = int(input("Wybierz warunek stopu:\n 0. Iteracje\n 1. Stagnacja\n: "))
    if glb_stop_cond == 0:
        glb_stop = int(input("  Podaj ilosc iteracji: "))
    glb_no_particles = int(input("Podaj ilosc czasteczek: "))
    glb_inertia = float(input("Podaj wartosc inercji: "))
    glb_cognitive = float(input("Podaj wartosc wspolczynnika poznawczego: "))
    glb_social = float(input("Podaj wartość wspolczynnika spolecznego: "))

    obj = ParticleSwarmAlgorithm(number_of_particles=glb_no_particles, choosen_function=glb_function,
                                 particle_inertia=glb_inertia,
                                 particle_social=glb_social,
                                 particle_cognition=glb_cognitive, stop_condition=glb_stop_cond, stop_value=glb_stop)
    iters, best_particle = obj.run()
    print(f'\nWynik:\n'
          f'x = {best_particle.x}\n'
          f'y =  {best_particle.y}\n'
          f'f(x,y) = {best_particle.fitness}')
    if glb_function == 0:
        plot_ackley(particles=obj.swarm, best_particle=best_particle, iteration=iters, inertia=glb_inertia,
                    social=glb_social,
                    cognition=glb_cognitive, no_particles=glb_no_particles)
        histogram_ackley(obj.swarm)
    else:
        plot_himmelblaus(particles=obj.swarm, best_particle=best_particle, iteration=iters,
                         inertia=glb_inertia,
                         social=glb_social,
                         cognition=glb_cognitive, no_particles=glb_no_particles)
        histogram_himmelblaus(obj.swarm)


if __name__ == '__main__':
    console_interface()
