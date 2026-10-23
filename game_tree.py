import math

# --------------------------------------------------
# Fixed Game Tree (Depth = 3)
# ROOT = MAX
# Level 1 = MIN
# Level 2 = MAX
# Level 3 = LEAVES
# --------------------------------------------------
tree = {
    "A": {
        "A1": [6, 9],
        "A2": [1, 4]
    },
    "B": {
        "B1": [17, 7],
        "B2": [-9, -3]
    }
}

pruned_nodes = set()
results = {}

# --------------------------------------------------
# Print FULL TREE (Before Pruning)
# --------------------------------------------------
def print_full_tree():
    print("\nFULL GAME TREE (Before Pruning)\n")
    print("ROOT (MAX)")
    for min_node in tree:
        print(f" ├── {min_node} (MIN)")
        for max_node in tree[min_node]:
            print(f" │   ├── {max_node} (MAX)")
            for leaf in tree[min_node][max_node]:
                print(f" │   │   └── Leaf → {leaf}")
    print()

# --------------------------------------------------
# Alpha–Beta for MAX node (leaf evaluation)
# --------------------------------------------------
def minimax_alpha_beta(leaves, alpha, beta, parent):
    value = -math.inf

    for leaf in leaves:
        value = max(value, leaf)
        alpha = max(alpha, value)

        # PRUNING CONDITION
        if alpha >= beta:
            for l in leaves:
                if l != leaf:
                    pruned_nodes.add(f"{parent}→{l}")
            break

    return value

# --------------------------------------------------
# Run Alpha–Beta Pruning
# --------------------------------------------------
def run_alpha_beta():
    print("\nRunning Alpha–Beta Pruning...\n")
    alpha = -math.inf

    for min_node in tree:
        beta = math.inf
        values = []

        print(f"Evaluating {min_node} (MIN)")
        for max_node in tree[min_node]:
            score = minimax_alpha_beta(
                tree[min_node][max_node],
                alpha,
                beta,
                max_node
            )

            print(f"  {max_node} returns {score}")
            values.append(score)
            beta = min(beta, score)

            if beta <= alpha:
                pruned_nodes.add(f"{min_node}→{max_node}")
                print(f"  PRUNED remaining children of {min_node}")
                break

        results[min_node] = min(values)
        alpha = max(alpha, results[min_node])

    best_move = max(results, key=results.get)
    return best_move

# --------------------------------------------------
# Print TREE AFTER PRUNING
# --------------------------------------------------
def print_pruned_tree(best_move):
    print("\nGAME TREE AFTER ALPHA–BETA PRUNING\n")
    print("ROOT (MAX)")

    for min_node in tree:
        tag = " <-- SELECTED" if min_node == best_move else ""
        print(f" ├── {min_node} (MIN){tag}")

        for max_node in tree[min_node]:
            if f"{min_node}→{max_node}" in pruned_nodes:
                print(f" │   ├── {max_node} (PRUNED)")
                continue

            print(f" │   ├── {max_node} (MAX)")
            for leaf in tree[min_node][max_node]:
                if f"{max_node}→{leaf}" in pruned_nodes:
                    print(f" │   │   └── {leaf} (PRUNED)")
                else:
                    print(f" │   │   └── Leaf → {leaf}")

# --------------------------------------------------
# MAIN
# --------------------------------------------------
print_full_tree()
best = run_alpha_beta()
print_pruned_tree(best)

print("\nBest Move for MAX:", best)
print("Minimax Values:", results)