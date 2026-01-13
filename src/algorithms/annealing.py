import math
import random
from typing import List, Tuple, Dict
from models import Cell, Net, PlacementParams
from algorithms.cost import total_wirelength, density_overflow, blockage_penalty

def anneal(nets: List[Net], cells_dict: Dict[str, Cell], params: PlacementParams, rng: random.Random):
    cells = [c for c in cells_dict.values() if not c.fixed]
    if not cells: return 0.0, 0.0
    
    current_wl = total_wirelength(nets, cells_dict)
    current_dens = density_overflow(cells_dict, params.chip_w, params.chip_h)[0]
    current_blk = blockage_penalty(cells_dict, params.blockages)
    current_cost = current_wl + current_dens * 1000 + current_blk
    
    T = 100.0
    alpha = 0.995
    accepted = 0
    
    for i in range(params.anneal_iters):
        c = rng.choice(cells)
        old_x, old_y = c.x, c.y
        
        dx = rng.uniform(-50, 50) * (T / 100.0)
        dy = rng.uniform(-50, 50) * (T / 100.0)
        
        c.x = max(0, min(params.chip_w - c.w, c.x + dx))
        c.y = max(0, min(params.chip_h - c.h, c.y + dy))
        
        new_wl = total_wirelength(nets, cells_dict)
        new_dens = density_overflow(cells_dict, params.chip_w, params.chip_h)[0]
        new_blk = blockage_penalty(cells_dict, params.blockages)
        new_cost = new_wl + new_dens * 1000 + new_blk
        
        delta = new_cost - current_cost
        if delta < 0 or (T > 0 and rng.random() < math.exp(-delta / T)):
            current_cost = new_cost
            accepted += 1
        else:
            c.x, c.y = old_x, old_y
            
        T *= alpha
        if T < 0.01: T = 0.01
        
    return current_cost, accepted / max(1, params.anneal_iters)
