# Import the data
from data import items

def knapsack(items, capacity):
    n = len(items)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if items[i - 1]["weight"] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - items[i - 1]["weight"]] + items[i - 1]["value"])
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack to find the items included in the optimal solution
    w = capacity
    selected_items = []
    total_weight = 0
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(items[i - 1])
            total_weight += items[i - 1]["weight"]
            w -= items[i - 1]["weight"]

    return dp[n][capacity], total_weight, selected_items

# Define the backpack capacity
backpack_capacity = 6404180

# Solve the knapsack problem
max_value, total_weight, selected_items = knapsack(items, backpack_capacity)

print(f"Maximum value: {max_value}")
print(f"Total weight: {total_weight}")
print("Selected items:")
for item in selected_items:
    print(item)