# giftproblem
## Approach
My solution for the Gift Problem consists of two steps:
1. Estimating item volumes by minimizing error 
2. Solving deterministic knapsack model with estimated item volumes

### Estimating Item Volumes
There is no information about outlier in the measured total package volumes,
therefore I propose to estimate the package volumes by two methods. One of the methods is less prone to be influenced by outliers.

### Method 1: Least Square

#### Formulation
Let $M \in \mathbb{N}$ be the amount of packages, $N \in \mathbb{N}$ the amount of items. Furthermore, let $A \in \{0, 1\}^{M \times N}$ a binary matrix with $a_{ij} = 1$ iff. package $i$ contains item $j$ for entries $a_{ij} \in \{0, 1\}$ of $A$. Furthermore, let $b \in \mathbb{Q}_{\geq 0}^M$ the measured total volume of all packages.

For each item $j$ the Least Square Problem contains a variable $x_j$ that indicates the volume of the item $j$ that is to be estimated. 

For each package $i$, the sum of the variables corresponding to the items of a package is equal to $b_i+\varepsilon_i$, whereas $\varepsilon_i$ depicts the error occured when the package $i$ was measured.

The Least Square Problem consists of finding an assignment of all $x_j$ variables such that $\sum_{i \in [M]} \varepsilon_i^2$ is minimized. This leads to the following non-linear objective:
$\min (Ax - b)^2$. A solution and therefore volume estimation of each item of the Least Square Problem minimizes this objective. 

A solution gives a reasonably well volume estimation under the assumption that the error follows a normal distribution, has a constant variance and there are not too many outliers. The former applies, the latter is unknown. 

#### Technicalities

I use qpsolver to solve the Least Square Problem as a QP. 

### Method 2: Least Absolute Deviation

## Used tools
### qpsolver
qpsolver acts as a generic interface for quadratic programming solvers. It offers an abstraction that solves Least Square by transforming the LS problem into a QP. It then calls an underlying QP solver.

### Gurobi / gurobipy
I use Gurobi and gurobipy ...
1. for solving the knapsack model 
2. as the underlying QP solver for qpsolver's LS solver
3. for solving Least Absolute Deviation as an LP 



