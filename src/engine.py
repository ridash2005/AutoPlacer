import random
from typing import Dict, Tuple, List, Optional, Any
import numpy as np

from utils.samples import create_cpu_like_blockages, example_netlist_dict, CHIP_W, CHIP_H
from models import Cell, Net, PlacementParams
from utils.parser import parse_netlist, init_placement
from utils.verilog_parser import parse_verilog_netlist
from utils.def_writer import write_def
from algorithms.cost import total_wirelength, density_overflow, congestion_estimate
from algorithms.global_placer import quadratic_global_placement
from algorithms.partitioning import recursive_bipartition_place
from algorithms.annealing import anneal
from utils.visualize import plot_cells_and_nets, plot_congestion
import json
import os

class PlacementEngine:
    """
    Core engine for the AutoPlacer VLSI placement flow.
    """
    def __init__(self, params: Optional[PlacementParams] = None):
        self.params = params or PlacementParams(chip_w=CHIP_W, chip_h=CHIP_H)
        self.cells: Dict[str, Cell] = {}
        self.nets: List[Net] = []
        self.rng = random.Random(self.params.rng_seed)

    def load_netlist(self, netlist: Dict):
        self.cells, self.nets = parse_netlist(netlist)
        if not self.params.blockages:
            self.params.blockages = create_cpu_like_blockages(self.cells, rng_seed=self.params.rng_seed)

    def load_verilog(self, file_path: str):
        """Loads a Verilog or SystemVerilog netlist."""
        self.cells, self.nets = parse_verilog_netlist(file_path)
        if not self.params.blockages:
            self.params.blockages = create_cpu_like_blockages(self.cells, rng_seed=self.params.rng_seed)

    def run(self, init_coords: Optional[Dict[str, Tuple[float, float]]] = None) -> Dict[str, Any]:
        """Runs the full placement flow."""
        init_placement(self.cells, self.params.chip_w, self.params.chip_h, init_coords, self.rng)

        print("Starting placement flow...")
        print("1. Quadratic global placement...")
        quadratic_global_placement(self.cells, self.nets, self.params.chip_w, self.params.chip_h, self.rng)

        print("2. Recursive bisection partitioning...")
        recursive_bipartition_place(self.cells, self.nets, self.params.chip_w, self.params.chip_h, 
                                   self.params.num_partitions, self.params.balance_tolerance, self.rng)

        print("3. Simulated annealing refinement...")
        final_cost, acc_ratio = anneal(self.nets, self.cells, self.params, self.rng)

        print("\nPlacement complete. Calculating metrics...")
        wl = total_wirelength(self.nets, self.cells)
        dens_over, util = density_overflow(self.cells, self.params.chip_w, self.params.chip_h)
        cong = congestion_estimate(self.nets, self.cells, self.params.chip_w, self.params.chip_h)

        metrics = {
            "wirelength_total": wl,
            "density_overflow_sum": dens_over,
            "avg_utilization": float(np.mean(util)),
            "congestion_heatmap": cong,
            "anneal_accept_ratio": acc_ratio,
            "final_cost": final_cost,
        }

        return metrics

    def visualize(self, metrics: Dict[str, Any], save_dir: Optional[str] = None):
        """Generates plots for the placement and congestion."""
        p_path = os.path.join(save_dir, "placement.png") if save_dir else None
        c_path = os.path.join(save_dir, "congestion.png") if save_dir else None
        
        plot_cells_and_nets(self.cells, self.nets, self.params, "Final Placement", save_path=p_path)
        plot_congestion(metrics["congestion_heatmap"], self.params, "Final Congestion", save_path=c_path)

    def save_results(self, folder_path: str, design_name: str = "top"):
        """Saves placement results in .def and .json formats."""
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        # 1. Save DEF
        def_path = os.path.join(folder_path, f"{design_name}.def")
        write_def(self.cells, self.params.chip_w, self.params.chip_h, def_path, design_name)
        
        # 2. Save JSON coordinates
        json_path = os.path.join(folder_path, f"{design_name}_placement.json")
        coords = {name: {"x": c.x, "y": c.y} for name, c in self.cells.items()}
        with open(json_path, 'w') as f:
            json.dump(coords, f, indent=4)
            
        print(f"Results saved to folder: {folder_path}")
