import sys
import os

# Add src to path if running directly
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from engine import PlacementEngine
from models import PlacementParams

from utils.generators import create_systolic_array

def main():
    print("--- AutoPlacer: AI/ML Accelerator Grid Example ---")
    netlist = create_systolic_array(10, 10)
    
    params = PlacementParams(
        chip_w=2000,
        chip_h=2000,
        num_partitions=5,
        anneal_iters=20000,
        rng_seed=42,
        visualize=False
    )
    
    engine = PlacementEngine(params)
    engine.load_netlist(netlist)
    
    metrics = engine.run()
    
    print("\nAI Accelerator Metrics:")
    print(f"  Total Cells: {len(netlist['cells'])}")
    print(f"  Total Nets: {len(netlist['nets'])}")
    print(f"  Final Wirelength: {metrics['wirelength_total']:.2f}")
    print(f"  Density Overflow: {metrics['density_overflow_sum']:.2f}")

if __name__ == "__main__":
    main()
