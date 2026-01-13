import argparse
import sys
import os
import json
import tkinter as tk
from tkinter import filedialog
from engine import PlacementEngine
from models import PlacementParams
from utils.samples import example_netlist_dict, CHIP_W, CHIP_H
from utils.generators import create_systolic_array, create_modern_soc
from utils.gui import get_user_params

def select_file():
    root = tk.Tk()
    root.withdraw() # Hide the main window
    file_path = filedialog.askopenfilename(
        title="AutoPlacer: Select Input Netlist",
        filetypes=[("Hardware Description", "*.v *.sv"), ("JSON Netlist", "*.json")]
    )
    root.destroy()
    return file_path

def main():
    parser = argparse.ArgumentParser(description="AutoPlacer: Automated VLSI Placement Engine")
    parser.add_argument("--input", type=str, help="Path to input netlist (.v, .sv, or .json)")
    parser.add_argument("--example", type=str, choices=['systolic', 'soc'], help="Run an industry-standard example")
    parser.add_argument("--iters", type=int, default=10000, help="Simulated annealing iterations")
    parser.add_argument("--partitions", type=int, default=4, help="Number of recursive bisection levels")
    parser.add_argument("--no-vis", action="store_true", help="Disable visualization")
    parser.add_argument("--no-gui", action="store_true", help="Disable GUI pop-up for file selection")

    args = parser.parse_args()

    # 1. Determine Input
    input_path = args.input
    netlist_data = None
    is_verilog = False

    if not args.example and not args.input and not args.no_gui:
        print("Launching file selection pop-up...")
        input_path = select_file()

    if args.example:
        print(f"Loading industry example: {args.example}")
        if args.example == 'systolic':
            netlist_data = create_systolic_array(10, 10)
        elif args.example == 'soc':
            netlist_data = create_modern_soc()
    elif input_path:
        if input_path.endswith(('.v', '.sv')):
            is_verilog = True
        elif input_path.endswith('.json'):
            with open(input_path, 'r') as f:
                netlist_data = json.load(f)
        else:
            print(f"Error: Unsupported file format for {input_path}")
            sys.exit(1)
    else:
        print("No input provided. Using default sample netlist.")
        netlist_data = example_netlist_dict

    # 2. Get Advanced Parameters via GUI
    user_params = None
    if not args.no_gui:
        print("Opening advanced configuration GUI...")
        user_params = get_user_params(CHIP_W, CHIP_H)
        if not user_params:
            print("Configuration cancelled by user.")
            sys.exit(0)

    # 3. Initialize Engine
    params = PlacementParams(
        chip_w=user_params["chip_w"] if user_params else CHIP_W,
        chip_h=user_params["chip_h"] if user_params else CHIP_H,
        num_partitions=user_params["num_partitions"] if user_params else args.partitions,
        anneal_iters=user_params["anneal_iters"] if user_params else args.iters,
        blockages=user_params["blockages"] if user_params else [],
        rng_seed=42,
        visualize=not args.no_vis
    )
    
    engine = PlacementEngine(params)
    
    if is_verilog:
        print(f"Parsing Hardware Description: {input_path}")
        engine.load_verilog(input_path)
    else:
        engine.load_netlist(netlist_data)
    
    # 3. Execution
    metrics = engine.run()
    
    # 4. Results Bundling
    design_name = os.path.splitext(os.path.basename(input_path))[0] if input_path else args.example if args.example else "autoplacer_result"
    results_dir = os.path.join("results", f"{design_name}_placed")
    print(f"\nFinalizing results in '{results_dir}' folder...")
    
    engine.save_results(results_dir, design_name)
    
    if not args.no_vis:
        engine.visualize(metrics, save_dir=results_dir)
    
    print("\n--- Placement Complete ---")
    print(f"  Final Wirelength: {metrics['wirelength_total']:.2f}")
    if is_verilog:
        print(f"  Coordinates exported to: {results_dir}/{design_name}.def")

if __name__ == "__main__":
    main()
