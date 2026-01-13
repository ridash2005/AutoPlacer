import re
from typing import Dict, List, Tuple
from models import Cell, Net

def parse_verilog_netlist(file_path: str) -> Tuple[Dict[str, Cell], List[Net]]:
    """
    Primitive structural Verilog/SystemVerilog parser.
    Extracts instances as cells and wires as nets.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Remove comments
    content = re.sub(r'//.*', '', content)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    cells = {}
    nets_dict = {} # wire_name -> list of cell_names

    # 1. Look for instances: module_name instance_name (.pin(wire), ...)
    # This regex is a simplification but often works for structural netlists
    instance_pattern = r'(\w+)\s+(\w+)\s*\((.*?)\);'
    instances = re.findall(instance_pattern, content, re.DOTALL)

    for mod_name, inst_name, ports_str in instances:
        # Ignore common keywords that might match this pattern if not careful
        if mod_name in ['module', 'endmodule', 'wire', 'reg', 'input', 'output']:
            continue
            
        # Default size if not known
        cells[inst_name] = Cell(name=inst_name, w=50, h=50)

        # Parse ports: .pin(wire)
        port_matches = re.findall(r'\.\w+\s*\(\s*(\w+)\s*\)', ports_str)
        for wire in port_matches:
            if wire not in nets_dict:
                nets_dict[wire] = []
            nets_dict[wire].append(inst_name)

    # 2. Look for inputs/outputs as fixed pads
    port_pattern = r'(input|output)\s+(?:wire\s+|reg\s+)?(\w+)'
    ports = re.findall(port_pattern, content)
    
    for p_type, p_name in ports:
        # Create a fixed "pad" cell for each top-level port
        pad_name = f"PAD_{p_name}"
        cells[pad_name] = Cell(name=pad_name, w=30, h=30, fixed=True)
        
        # Connect to the wire of the same name
        if p_name not in nets_dict:
            nets_dict[p_name] = []
        nets_dict[p_name].append(pad_name)

    # Convert nets_dict to List[Net]
    nets = []
    for wire_name, connected_cells in nets_dict.items():
        if len(connected_cells) > 1:
            nets.append(Net(name=wire_name, pins=list(set(connected_cells))))

    return cells, nets
