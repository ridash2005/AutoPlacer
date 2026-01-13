import sys
import os

# Add src to path if running directly
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from engine import PlacementEngine
from models import PlacementParams
from utils.samples import CHIP_W, CHIP_H

from utils.generators import create_modern_soc

def main():
    print("--- AutoPlacer: Modern SoC Peripheral Hub Example ---")
    netlist = create_modern_soc()
    
    params = PlacementParams(
        chip_w=CHIP_W,
        chip_h=CHIP_H,
        num_partitions=4,
        anneal_iters=30000,
        rng_seed=123,
        visualize=True
    )
    
    engine = PlacementEngine(params)
    engine.load_netlist(netlist)
    
    metrics = engine.run()
    
    # Save results
    results_dir = os.path.join("results", "soc_peripheral_hub_placed")
    engine.save_results(results_dir, "soc_peripheral_hub")
    engine.visualize(metrics, save_dir=results_dir)
    
    print("\nModern SoC Metrics:")
    print(f"  Total Cells: {len(netlist['cells'])}")
    print(f"  Total Nets: {len(netlist['nets'])}")
    print(f"  Final Wirelength: {metrics['wirelength_total']:.2f}")
    print(f"  Results saved to: {results_dir}")

if __name__ == "__main__":
    main()
