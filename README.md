# giftproblem
## Run
To run this software, please install Python 3.12, [`gurobipy`](https://pypi.org/project/gurobipy/) and [`qpsolvers`](https://pypi.org/project/qpsolvers/),
and then run [`choose_gifts.py`](choose_gifts.py). By default, this solves the
problem and prints the chosen items, estimated total backpack volume and the
total cost.

## Approach
My solution for the Gift Problem consists of two steps:
1. Estimating item volumes by minimizing error
2. Solving deterministic knapsack model with estimated item volumes and multiple 

### 1. Estimating Item Volumes
There is no information about outlier in the measured total package volumes,
therefore I propose to estimate the package volumes by two methods. One of the
methods is less prone to be influenced by outliers.

### Method 1: Least Square
#### Formulation
Let $M \in \mathbb{N}$ be the amount of packages, $N \in \mathbb{N}$ the amount of items. Furthermore, let $A \in \{0, 1\}^{M \times N}$ a binary matrix with $a_{ij} = 1$ iff. package $i$ contains item $j$ for entries $a_{ij} \in \{0, 1\}$ of $A$. Furthermore, let $b \in \mathbb{Q}_{\geq 0}^M$ the measured total volume of all packages.

For each item $j$ the Least Square Problem contains a variable $x_j$ that indicates the volume of the item $j$ that is to be estimated. 

For each package $i$, the sum of the variables corresponding to the items of a package is equal to $b_i+\varepsilon_i$, whereas $\varepsilon_i$ depicts the error occured when the package $i$ was measured.

The Least Square Problem consists of finding an assignment of all $x_j$ variables such that $\sum_{i \in [M]} \varepsilon_i^2=(Ax-b)^2$ is minimized. This leads to the following non-linear objective:
$\min (Ax - b)^2$. A solution and therefore volume estimation of each item of the Least Square Problem minimizes this objective. 

A solution gives a reasonably well volume estimation under the assumption that the error follows a normal distribution, has a constant variance and there are not too many outliers. The former applies, the latter is unknown. 
On a theoretical note, this works because maximum likelihood estimation of a normal distributed error is the least square estimation.

#### Technicalities
I use `qpsolvers` to model the Least Square Problem as a QP and solve it with a QP solver. 
For source code, see [`regression/ls.py`](regression/ls.py).

### Method 2: Least Absolute Deviation
#### Formulation
Most of the formulation of the Least Square method applies to Least Absolute
Deviation Problem. Instead of minimizing the squared deviation, we instead minimize the
absolute deviation: $\min_{\text{item } j} |\varepsilon_i| = \min_{\text{item} |Ax - b|}.

#### Model
I express the formulation of the Least Absolute Deviation Problem as a linear program.
We introduce continuous variables $x_j \in \mathbb{R}$ for every item $j$. I linearize the formulated objective function by introducing non-negative continuous error slack variables $e_i^{+} \in \mathbb{R}_{\geq 0}$ and $e_i^{-} \in \mathbb{R}_{\geq 0}$ such that the value of the expression $e_i^{+} - e_i^{-}$ precisely captures the occured error when the volume of package $i$ was measured as $b_i$. For this, I introduce a linear constraint for each package $i$ that expresses exactly this. Given the set $\mathcal{J}_i$ of items of a package $i$, the following constraint is added to the model: $\sum_{j \in \mathcal{J}_{i}} x_j + e_i^{+} - e_i^{-} = b_i$. 
Then, a linear objective function that minimizes the cumulated absolute deviations corresponds to $\min \sum_{\text{package } i} e_i^{+} + e_i^{-}$. 

This yields an LP that can be solved by any off-the-shelf LP solver

#### Technicalities
I use Gurobi and `gurobipy` to solve the construced LP and therefore to solve the Least Absolute Deviation Problem.
For source code, see [`regression/lad.py`](regression/lad.py).

### 2. Solving Knapsack with Estimated Item Volumes
#### Assumption
We assume that each item has unlimited quantity available. Furthermore, we assume that Ahmad can pick an item more than once.

#### Model
Given estimated item volumes $w_j$ for each item $j$. Furthermore, let $W=40$
denote the backpack size and let $c_j$ denote the price of an item $j$. 

We introduce a non-negative integer variable $y_j \in \mathbb{\geq 0}$ that indicates how many pieces of item $j$ are packed into Ahmad's backpack.
It should hold that the backpack's volume is not exceeded with very high probability. Therefore we introduce the knapsack constraint that models this given the estimated item volumes $w_j$: $\sum_{\text{item } j} w_j \cdot y_j \leq W$. 
The objective of the model maximizes the price of all packed items. Therefore, the objective is $\max \sum_{\text{item } j} c_j \cdot y_j$

In total, this model is a Mixed-Integer Linear Program and is solved with B&C. 

#### Technicalities
I use `gurobipy` and Gurobi for solving this MILP. For source code, see [`knapsack.py`](knapsack.py).

## Used tools
### `qpsolvers`
`qpsolvers` acts as a generic interface for quadratic programming solvers. It offers an abstraction that solves Least Square by transforming the LS problem into a QP. It then calls an underlying QP solver.

### Gurobi / `gurobipy`
I use Gurobi and `gurobipy` ...
1. for solving the knapsack model 
2. as the underlying QP solver for `qpsolver`'s LS solver
3. for solving Least Absolute Deviation as an LP 


