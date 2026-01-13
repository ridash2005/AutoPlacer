import random
from typing import Dict, List, Tuple, Optional
from models import Cell, Net

def recursive_bipartition_place(
    cells_dict: Dict[str, Cell], nets: List[Net], 
    w: float, h: float, num_levels: int, 
    tol: float, rng: random.Random
):
    cells = list(cells_dict.values())
    _bipartition(cells, 0, 0, w, h, num_levels, tol, rng)

def _bipartition(cells: List[Cell], x: float, y: float, w: float, h: float, level: int, tol: float, rng: random.Random):
    if level <= 0 or not cells:
        for c in cells:
            if not c.fixed:
                c.x = max(x, min(x + w - c.w, c.x))
                c.y = max(y, min(y + h - c.h, c.y))
        return

    movable = [c for c in cells if not c.fixed]
    if not movable: return

    horiz = w > h
    if horiz:
        movable.sort(key=lambda c: c.x)
        mid = x + w / 2
        w1, w2 = w / 2, w / 2
        h1, h2 = h, h
        x1, x2 = x, x + w / 2
        y1, y2 = y, y
    else:
        movable.sort(key=lambda c: c.y)
        mid = y + h / 2
        w1, w2 = w, w
        h1, h2 = h / 2, h / 2
        x1, x2 = x, x
        y1, y2 = y, y + h / 2

    split_idx = len(movable) // 2
    c1 = movable[:split_idx] + [c for c in cells if c.fixed and (c.x < mid if horiz else c.y < mid)]
    c2 = movable[split_idx:] + [c for c in cells if c.fixed and (c.x >= mid if horiz else c.y >= mid)]

    _bipartition(c1, x1, y1, w1, h1, level - 1, tol, rng)
    _bipartition(c2, x2, y2, w2, h2, level - 1, tol, rng)
