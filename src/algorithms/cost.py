import numpy as np
from typing import Dict, List, Tuple
from models import Cell, Net

def total_wirelength(nets: List[Net], cells: Dict[str, Cell]) -> float:
    wl = 0.0
    for net in nets:
        xs = [cells[p].x + cells[p].w / 2 for p in net.pins if p in cells]
        ys = [cells[p].y + cells[p].h / 2 for p in net.pins if p in cells]
        if xs:
            wl += (max(xs) - min(xs)) + (max(ys) - min(ys))
    return wl

def density_overflow(cells: Dict[str, Cell], chip_w: float, chip_h: float, grid_size: int = 20) -> Tuple[float, np.ndarray]:
    util = np.zeros((grid_size, grid_size))
    gx, gy = chip_w / grid_size, chip_h / grid_size
    target_util = 0.7
    for c in cells.values():
        ix0, iy0 = int(c.x / gx), int(c.y / gy)
        ix1, iy1 = int((c.x + c.w) / gx), int((c.y + c.h) / gy)
        for i in range(max(0, ix0), min(grid_size, ix1 + 1)):
            for j in range(max(0, iy0), min(grid_size, iy1 + 1)):
                util[j, i] += (c.w * c.h) / (gx * gy)
    overflow = np.sum(np.maximum(0, util - target_util))
    return float(overflow), util

def blockage_penalty(cells: Dict[str, Cell], blockages: List[Tuple[float, float, float, float]]) -> float:
    penalty = 0.0
    for c in cells.values():
        if c.fixed: continue
        cx, cy = c.x + c.w/2, c.y + c.h/2
        for bx0, by0, bx1, by1 in blockages:
            if bx0 < cx < bx1 and by0 < cy < by1:
                penalty += 1000.0
    return penalty

def congestion_estimate(nets: List[Net], cells: Dict[str, Cell], chip_w: float, chip_h: float, grid_size: int = 25) -> np.ndarray:
    heat = np.zeros((grid_size, grid_size))
    gx, gy = chip_w / grid_size, chip_h / grid_size
    for net in nets:
        pts = [(cells[p].x + cells[p].w/2, cells[p].y + cells[p].h/2) for p in net.pins if p in cells]
        if not pts: continue
        xs, ys = zip(*pts)
        ix0, ix1 = int(min(xs)/gx), int(max(xs)/gx)
        iy0, iy1 = int(min(ys)/gy), int(max(ys)/gy)
        for i in range(max(0, ix0), min(grid_size, ix1 + 1)):
            for j in range(max(0, iy0), min(grid_size, iy1 + 1)):
                heat[j, i] += 1.0
    return heat
