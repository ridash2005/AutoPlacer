from engine import PlacementEngine
from models import PlacementParams

def main():
    # 1. Customize parameters
    params = PlacementParams(
        chip_w=1000, 
        chip_h=1000, 
        num_partitions=2, 
        anneal_iters=5000
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
    
    # 4. Access results
    print(f"Final Wirelength: {metrics['wirelength_total']}")
    
    # 5. Optional visualization
    # engine.visualize(metrics)

if __name__ == "__main__":
    main()
