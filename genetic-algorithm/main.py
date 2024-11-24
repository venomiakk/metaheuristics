import experiments



def interface():
    print("i")


def set_run_all_experiments():
    # szansa na krzyzowanie
    experiments.experiment1(0.1)
    experiments.experiment1(0.5)
    experiments.experiment1(1)

    #szansa na mutacje
    experiments.experiment2(0.1)
    experiments.experiment2(0.5)
    experiments.experiment2(1)

    #wielkosc populacji
    experiments.experiment3(10)
    experiments.experiment3(20)
    experiments.experiment3(30)

    #metody selekcji
    experiments.experiment4(0)
    experiments.experiment4(1)

    #metody krzyzowania
    experiments.experiment5(0)
    experiments.experiment5(1)

    #TODO czy jeszcze szansa na krzyzowanie z druga metoda?


if __name__ == '__main__':
    experiments.experiment3(10)
    experiments.experiment3(20)
    experiments.experiment3(30)

# Maximum value: 13692887
# Maximum weight: 6397822
# Expected chromosome: [0,0,0,0,1,1,0,1,0,0,1,1,0,1,0,1,0,0,0,0,1,1,0,1,0,1]

# TODO co zrobic gdy mamy wiele osobnikow z fitness = 0
# * rodzic moze byc rodzicem wiecej niz raz
# ? czy podczas selekcji powinien moc byc wybrany wiecej niz raz?
# * dodać selekcje rankingową jako druga metoda
