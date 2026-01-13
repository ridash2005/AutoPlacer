import random
from typing import Dict, List, Tuple, Optional
from models import Cell, Net

def parse_netlist(netlist_dict: Dict) -> Tuple[Dict[str, Cell], List[Net]]:
    cells = {}
    for name, attr in netlist_dict["cells"].items():
        cells[name] = Cell(name=name, w=attr["w"], h=attr["h"], 
                          fixed=attr.get("fixed", False),
                          x=attr.get("x", 0.0), y=attr.get("y", 0.0))
    
    nets = []
    for i, n_attr in enumerate(netlist_dict["nets"]):
        nets.append(Net(name=f"net_{i}", pins=n_attr["pins"]))
    
    return cells, nets

def init_placement(cells: Dict[str, Cell], chip_w: float, chip_h: float, 
                  init_coords: Optional[Dict[str, Tuple[float, float]]], rng: random.Random):
    for name, cell in cells.items():
        if cell.fixed:
            continue
        if init_coords and name in init_coords:
            cell.x, cell.y = init_coords[name]
        else:
            cell.x = rng.uniform(0, chip_w - cell.w)
            cell.y = rng.uniform(0, chip_h - cell.h)
