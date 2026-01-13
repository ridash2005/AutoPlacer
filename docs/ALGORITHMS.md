# AutoPlacer: Optimization Algorithms

AutoPlacer uses a multi-stage approach to VLSI cell placement, combining analytical and stochastic optimization techniques.

## 1. Quadratic Global Placement (QGP)

The goal of QGP is to find an initial configuration that minimizes the total squared wirelength.

### Theory
The problem is formulated by representing the connectivity as a cost function:
$$ \Phi(x, y) = \sum_{i,j \in Nets} w_{i,j} [(x_i - x_j)^2 + (y_i - y_j)^2] $$
where $w_{i,j}$ is the weight of the connection between pins $i$ and $j$.

### Implementation
We translate this into a system of linear equations:
$$ A \mathbf{x} = \mathbf{b}_x, \quad A \mathbf{y} = \mathbf{b}_y $$
- $A$: Connectivity matrix (Laplacian).
- $\mathbf{b}$: Vector representing connections to fixed (IO/Pad) cells.

We use `scipy.sparse.linalg.spsolve` to efficiently find the global minimum.

---

## 2. Recursive Bipartitioning (RB)

RB is used for **legalization**—ensuring cells do not overlap and adhere to area density constraints.

### Process
1. **Divide**: The chip area is split either horizontally or vertically (based on the larger dimension).
2. **Assign**: Cells are sorted by their current coordinates (from QGP) and split into two groups based on area balancing.
3. **Constrain**: The process repeats recursively until a target granularity (number of partitions) is reached.

This stage resolves the "clumping" often seen in pure quadratic placement results.

---

## 3. Simulated Annealing (SA)

SA performs local refinement to minimize the Half-Perimeter Wirelength (HPWL) and eliminate remaining overlaps.

### Algorithm
1. **Move**: A random cell is selected and shifted by a distance controlled by the current "Temperature" ($T$).
2. **Evaluate**: The change in cost ($\Delta C$) is calculated.
3. **Acceptance**: 
   - If $\Delta C < 0$ (improvement), the move is always accepted.
   - If $\Delta C > 0$, the move is accepted with probability $P = e^{-\Delta C / T}$.

### Cooling Schedule
We use a geometric cooling schedule: $T_{new} = T_{old} \times \alpha$ (typically $\alpha = 0.995$). As $T$ decreases, the engine becomes less likely to accept "bad" moves, converging on a local optimum.
