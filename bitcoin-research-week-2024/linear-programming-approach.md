---
title: Linear Programming Approach
date: 2024-11-21
---

We consider the following linear programming formulation for transaction selection:

### Variables and Objective

- Let $f_i$ represent the fee rate of transaction $i$ and $s_i$ represent its size.

- Define decision variables $x_i$, where $x_i = 1$ if transaction $i$ is selected, and $x_i = 0$ otherwise.

The objective is to **maximize the total fee rate**:

$$
\text{Maximize: } \sum f_i x_i
$$

### Constraints

1. **Size Constraint**: The sum of the sizes of selected transactions must equal the block size (normalized to 1 for simplicity):

$$
\sum s_i x_i = 1
$$

2. **Non-Negativity**: Decision variables must be non-negative:

$$
x_i \geq 0 \quad \forall i
$$

3. **Ordering Constraints (Optional)**: To respect descendant dependencies, enforce:

$$
x_i \geq x_j \quad \text{if transaction } j \text{ depends on transaction } i
$$

### Approximate Solutions

We solve this linear program approximately, allowing for a small tolerance $\epsilon$. Efficient algorithms exist with a complexity of $O((m + n)^3)$, where $m$ is the number of constraints and $n$ is the number of variables. For practical cases, such as 64 variables and 100 constraints, solutions can be computed in under 1 millisecond using modern solvers.

An open-source library called **HiGHS** (available under a compatible license) can efficiently solve this formulation.

### Handling Dynamic Updates

To adapt to new transactions:

- If a new transaction $t_{\text{new}}$ arrives with fee rate $f_{\text{new}}$ and size $s_{\text{new}}$, we include $x_{\text{new}}$ as a variable in the linear program.

- The updated solution respects the same constraints and does not alter the theoretical understanding of the problem.

- By incorporating $\epsilon$-tolerance, the solution can adjust slightly to accommodate optimality trade-offs.

This approach seamlessly handles dynamic updates without the need for significant recomputation, making it highly applicable to real-time mempool management.

### Advantages Over Current Rules

1. **Simplifies RBF Rules**: Replaces the need for extensive rules like the "125% RBF" rule, which is complex and makes mempool behavior difficult to predict.

2. **Black-Box Mempool**: Treats the mempool as a simplified optimization problem, avoiding the need for exhaustive rule-based testing (e.g., testmempool).

3. **Generalizability**: Linear programming is already a proven method for solving knapsack-style problems, making this approach well-suited for transaction selection.

### Resources

For further reading on linear programming techniques and theoretical foundations:

- **SpringerLink**: [Understanding Linear Programming](https://link.springer.com/book/10.1007/978-3-540-24777-7)
