import sys
import os

# Add src to path if running directly
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from engine import PlacementEngine
from models import PlacementParams

def main():
    print("--- AutoPlacer: Basic Logic Cluster Example ---")
    # 1. Customize parameters
    params = PlacementParams(
        chip_w=1000, 
        chip_h=1000, 
        num_partitions=2, 
        anneal_iters=5000,
        visualize=True
    )

    # 2. Define a simple netlist
    custom_netlist = {
        "cells": {
            "reg1": {"w": 50, "h": 50},
            "reg2": {"w": 50, "h": 50},
            "io1": {"w": 40, "h": 40, "fixed": True, "x": 10, "y": 10}
        },
        "nets": [
            {"pins": ["reg1", "reg2", "io1"]}
        ]
    }

    # 3. Running the engine
    engine = PlacementEngine(params)
    engine.load_netlist(custom_netlist)
    
    metrics = engine.run()
    
    # 4. Save results
    results_dir = os.path.join("results", "logic_array_basic_placed")
    engine.save_results(results_dir, "logic_array_basic")
    engine.visualize(metrics, save_dir=results_dir)
    
    print(f"\nFinal Wirelength: {metrics['wirelength_total']:.2f}")
    print(f"Results saved to: {results_dir}")

if __name__ == "__main__":
    main()
