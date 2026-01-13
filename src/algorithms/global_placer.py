import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from typing import Dict, List, Tuple
import random
from models import Cell, Net

def quadratic_global_placement(cells: Dict[str, Cell], nets: List[Net], chip_w: float, chip_h: float, rng: random.Random):
    movable = [c for c in cells.values() if not c.fixed]
    fixed = [c for c in cells.values() if c.fixed]
    if not movable: return

    m_idx = {c.name: i for i, c in enumerate(movable)}
    n = len(movable)
    A = sparse.lil_matrix((n, n))
    bx, by = np.zeros(n), np.zeros(n)

    for net in nets:
        weight = 1.0 / max(1, len(net.pins) - 1)
        for i in range(len(net.pins)):
            for j in range(i + 1, len(net.pins)):
                p1, p2 = net.pins[i], net.pins[j]
                if p1 in m_idx and p2 in m_idx:
                    u, v = m_idx[p1], m_idx[p2]
                    A[u, u] += weight; A[v, v] += weight
                    A[u, v] -= weight; A[v, u] -= weight
                elif p1 in m_idx and p2 in cells and cells[p2].fixed:
                    u = m_idx[p1]
                    A[u, u] += weight
                    bx[u] += weight * cells[p2].x
                    by[u] += weight * cells[p2].y
                elif p2 in m_idx and p1 in cells and cells[p1].fixed:
                    u = m_idx[p2]
                    A[u, u] += weight
                    bx[u] += weight * cells[p1].x
                    by[u] += weight * cells[p1].y

    A = A.tocsr()
    try:
        sol_x = spsolve(A, bx)
        sol_y = spsolve(A, by)
        for i, c in enumerate(movable):
            c.x = max(0, min(chip_w - c.w, sol_x[i]))
            c.y = max(0, min(chip_h - c.h, sol_y[i]))
    except:
        pass
