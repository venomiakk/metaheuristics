from algorithm import geneticAlgorithm
from data import items

if __name__ == '__main__':
    ga = geneticAlgorithm(items, 5)
    ga.run()


# TODO co zrobic gdy mamy wiele osobnikow z fitness = 0
# * rodzic moze byc rodzicem wiecej niz raz
# ? czy podczas selekcji powinien moc byc wybrany wiecej niz raz?
# * dodać selekcje rankingową jako druga metoda
