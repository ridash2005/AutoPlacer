from typing import Dict, List
from models import Cell

def write_def(cells: Dict[str, Cell], chip_w: float, chip_h: float, file_path: str, design_name: str = "top"):
    """
    Writes placement results to a standardized .def file.
    """
    with open(file_path, 'w') as f:
        f.write(f"VERSION 5.8 ;\n")
        f.write(f"DIVIDERCHAR \"/\" ;\n")
        f.write(f"BUSBITCHARS \"[]\" ;\n")
        f.write(f"DESIGN {design_name} ;\n")
        f.write(f"UNITS DISTANCE MICRONS 1000 ;\n\n")
        
        f.write(f"DIEAREA ( 0 0 ) ( {int(chip_w)} {int(chip_h)} ) ;\n\n")
        
        # Components section
        num_movable = sum(1 for c in cells.values() if not c.fixed)
        f.write(f"COMPONENTS {num_movable} ;\n")
        for name, cell in cells.items():
            if not cell.fixed:
                # Format: - inst_name mod_name + PLACED ( x y ) N ;
                # Since we don't track original mod_name in Cell, we use "CELL" as placeholder
                f.write(f"    - {name} CELL + PLACED ( {int(cell.x)} {int(cell.y)} ) N ;\n")
        f.write(f"END COMPONENTS\n\n")
        
        f.write(f"END DESIGN\n")
