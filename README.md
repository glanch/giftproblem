# My Solution of The Gift Problem
The description of the Gift Problem does not state whether Ahmad can pack a
single item multiple times into his backpack. I assume that this is allowed,
but still give solution for both cases.
## My solution
### Estimated item volumes
I estimated the item volumes with least square method.
<details>
  <summary>Volume Estimations with Least Square Method</summary>
  A1: 22.021118524229237; A2: 14.45781057459718; A3: 8.454916764907193; A4: 23.950558756832113; A5: 16.608708443894614; A6: 0.37567656740091904; A7: 8.83333202950414; A8: 3.5461802660479966; A9: 0.9593400482423037; A10: 14.540566462507497; A11: 22.77823394134002; A12: 14.964040774318565; A13: 21.54299887703683; A14: 29.669818032304043; A15: 11.036597705506871; A16: 15.957820495491042; A17: 6.864389014170886; A18: 8.352695353244146; A19: 15.184085730433905; A20: 22.104818560228278; A21: 26.435365285293734; A22: 25.803030807701752; A23: 7.27123906961052; A24: 25.775826640735204; A25: 9.482042023006557; A26: 20.583395403232; A27: 7.515408134789879; A28: 6.832125304629022; A29: 20.850502769938625; A30: 19.326638574705974; A31: 6.875682589926919; A32: 0.9218247852384645; A33: 5.946422038616392; A34: 13.246743951714274; A35: 4.975683341427916; A36: 25.11605272089536; A37: 12.500112589023555; A38: 9.898305182537658; A39: 1.5554143168213463; A40: 10.532179324218948; A41: 23.033278454756104; A42: 11.566374135419498; A43: 5.005751745097541; A44: 4.8114853019376795; A45: 22.43858887689611; A46: 17.58217751885109; A47: 26.037340206750926; A48: 7.212602587589086; A49: 11.176684062545817; A50: 11.384898741525287; A51: 26.99512694944281; A52: 23.010644144875265; A53: 5.623208376885822; A54: 11.655422808835144; A55: 16.508915373108138; A56: 10.441519525942489; A57: 18.70332938563313; A58: 25.492607324517877; A59: 16.193789972373573; A60: 12.35544498375213
</details>

### Items cannot be packed more than once:
Ahmad should pack items A6, A8, A9, A23, A32, A35, A38, A44, A48. This yields a total price of 757.0 and a total estimated volume of 39.9723.

### Items can be packed more than once
Ahmad should pack item A6 106 times. This yields a total price of 11554.0 and a total estimated volume of 39.8217.

## Run
To run this software, please install Python 3.12, [`gurobipy`](https://pypi.org/project/gurobipy/) and [`qpsolvers`](https://pypi.org/project/qpsolvers/),
and then run [`choose_gifts.py`](choose_gifts.py). By default, this solves the
problem and prints the chosen items, estimated total backpack volume and the
total cost.

## Approach
My solution for the Gift Problem consists of two steps:
1. Estimating item volumes by minimizing error / deviation
2. Solving deterministic knapsack model with estimated item volumes and potentially with multiple packing of single item allowed.

### 1. Estimating Item Volumes
There is no information about outlier in the measured total package volumes,
therefore I propose to estimate the package volumes by two methods. One of the
methods is less prone to be influenced by outliers.

### Method 1: Least Square
#### Formulation
Let $M \in \mathbb{N}$ be the amount of packages, $N \in \mathbb{N}$ the amount of items. Furthermore, let $A \in \{0, 1\}^{M \times N}$ a binary matrix with $a_{ij} = 1$ iff. package $i$ contains item $j$ for entries $a_{ij} \in \{0, 1\}$ of $A$. Furthermore, let $b \in \mathbb{Q}_{\geq 0}^M$ the measured total volume of all packages.

For each item $j$, the Least Square Problem contains a variable $x_j$ that indicates the volume of the item $j$ that is to be estimated. 

For each package $i$, the sum of the variables corresponding to the items of a package is equal to $b_i+\varepsilon_i$, whereas $\varepsilon_i$ depicts the error occured when the package $i$ was measured.

The Least Square Problem consists of finding an assignment of all $x_j$ variables such that the squared deviation, i.e. $\sum_{i \in [M]} \varepsilon_i^2=(Ax-b)^2$, is minimized. This leads to the following non-linear objective:
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
absolute deviation: $\min_{\text{item } j} |\varepsilon_i| = \min_{\text{item}} |Ax - b|$.

#### Model
I express the formulation of the Least Absolute Deviation Problem as a linear program.
We introduce continuous variables $x_j \in \mathbb{R}$ for every item $j$. I linearize the formulated objective function by introducing non-negative continuous error slack variables $e_i^{+} \in \mathbb{R}_{\geq 0}$ and $e_i^{-} \in \mathbb{R}_{\geq 0}$ such that the value of the expression $e_i^{+} - e_i^{-}$ precisely captures the occured error $\varepsilon_i$ when the volume of package $i$ was measured as $b_i$. For this, I introduce a linear constraint for each package $i$ that expresses exactly this. Given the set $\mathcal{J}_i$ of items of a package $i$, the following constraint is added to the model: $\sum_{i \in \mathcal{J}_{i}} x_j + e_i^{+} - e_i^{-} = b_i$. 
Then, a linear objective function that minimizes the cumulated absolute deviations corresponds to $\min \sum_{\text{package } i} e_i^{+} + e_i^{-}$. 

This yields an LP that can be solved by any off-the-shelf LP solver

#### Technicalities
I use Gurobi and `gurobipy` to solve the construced LP and therefore to solve the Least Absolute Deviation Problem.
For source code, see [`regression/lad.py`](regression/lad.py).

### 2. Solving Knapsack with Estimated Item Volumes
Optimally packing Ahmad's backpack without exceeding the capacity and maximizing profit / item cost is a Knapsack problem. 

#### Model
Given estimated item volumes $w_j$ for each item $j$. Furthermore, let $W=40$
denote the backpack size and let $c_j$ denote the price of an item $j$. 

We introduce a non-negative integer variable $y_j \in \mathbb{Z}_{\geq 0}$ that indicates how many pieces of item $j$ are packed into Ahmad's backpack. If 
Ahmad cannot pick an item more than once, $y_j$ is limited to a boolean value $\{0, 1\}$-
It should hold that the backpack's volume is not exceeded with very high probability. Therefore we introduce the linear knapsack constraint that models this given the estimated item volumes $w_j$: $\sum_{\text{item } j} w_j \cdot y_j \leq W$. 
The objective of the model maximizes the price of all packed items. Therefore, the linear objective is $\max \sum_{\text{item } j} c_j \cdot y_j$

In total, this model is a Mixed-Integer Linear Program and is solved with B&C. 

#### Technicalities
I use `gurobipy` and Gurobi for expressing and solving this MILP. For source code, see [`knapsack.py`](knapsack.py).

## Used tools
### `qpsolvers`
`qpsolvers` acts as a generic interface for quadratic programming solvers. It offers an abstraction that solves Least Square by transforming the LS problem into a QP. It then calls an underlying QP solver.

### Gurobi / `gurobipy`
I use Gurobi and `gurobipy` ...
1. for solving the knapsack model 
2. as the underlying QP solver for `qpsolvers`' LS solver
3. for solving Least Absolute Deviation as an LP