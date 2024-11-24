import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter


def format_with_commas(x, pos):
    return f'{int(x): }'


def bar_plot_weights(best_weights, avg_weights, worst_weights):
    max_capacity = 6404180.0
    expected_weight = 6397822.0 / max_capacity
    best_weights = [i / max_capacity for i in best_weights]
    avg_weights = [i / max_capacity for i in avg_weights]
    worst_weights = [i / max_capacity for i in worst_weights]
    categories = [str(i) for i in range(1, len(best_weights) + 1)]


    worst_weights = [max(v, 0.01) for v in worst_weights]
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.ylim(0, 1)
    plt.bar(categories, best_weights, color='mediumslateblue', edgecolor='black', label='Najlepsza waga')
    plt.bar(categories, avg_weights, color='rebeccapurple', edgecolor='black', label='Średnia waga')
    plt.bar(categories, worst_weights, color='indigo', edgecolor='black', label='Najgorsza waga')

    plt.axhline(y=expected_weight, color='red', linestyle='--', linewidth=1,
                label=f'Oczekiwany wynik')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.title('Wyniki dla badanych parametrów', fontsize=9)
    plt.xlabel('Uruchomienia', fontsize=9)
    plt.ylabel('Procent wypełnienia plecaka', fontsize=9)
    plt.legend(bbox_to_anchor=(0., -0.2, 1., .102), loc='lower left',
               ncols=2, mode="expand", borderaxespad=0., frameon=False)
    plt.tight_layout()

    plt.show()


def bar_plot_values(best_values, avg_values, worst_values):
    categories = [str(i) for i in range(1, len(best_values) + 1)]

    expected_value = 13692887

    worst_values = [max(v, 100000) for v in worst_values]

    plt.bar(categories, best_values, color='mediumslateblue', edgecolor='black', label='Najlepsza wartość')
    plt.bar(categories, avg_values, color='rebeccapurple', edgecolor='black', label='Średnia wartość')
    plt.bar(categories, worst_values, color='indigo', edgecolor='black', label='Najgorsza wartość')

    plt.axhline(y=expected_value, color='red', linestyle='--', linewidth=1,
                label=f'Oczekiwany wynik')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.ylim(0, expected_value + 1000000)
    plt.title('Wyniki dla badanych parametrów', fontsize=9)
    plt.xlabel('Uruchomienia', fontsize=9)
    plt.ylabel('Wartości', fontsize=9)
    plt.legend(bbox_to_anchor=(0., -0.2, 1., .102), loc='lower left',
               ncols=2, mode="expand", borderaxespad=0., frameon=False)
    plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    print('plots')
