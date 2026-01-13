import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Dict, Any, Optional

class ConfigGUI:
    """
    Advanced configuration window for AutoPlacer parameters.
    Allows users to set chip dimensions, manage blockages, and tune algorithm parameters.
    """
    def __init__(self, default_w: float = 1000.0, default_h: float = 1000.0):
        self.root = tk.Tk()
        self.root.title("AutoPlacer: Advanced Configuration")
        self.root.geometry("500x700")
        
        # Results to be returned
        self.results: Dict[str, Any] = {
            "chip_w": default_w,
            "chip_h": default_h,
            "blockages": [],
            "anneal_iters": 10000,
            "num_partitions": 4
        }
        self.confirmed = False

        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Chip Dimensions Section
        geo_lf = ttk.LabelFrame(main_frame, text="Chip Geometry", padding="10")
        geo_lf.pack(fill=tk.X, pady=10)

        ttk.Label(geo_lf, text="Width (um):").grid(row=0, column=0, sticky=tk.W)
        self.w_entry = ttk.Entry(geo_lf)
        self.w_entry.insert(0, str(self.results["chip_w"]))
        self.w_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(geo_lf, text="Height (um):").grid(row=1, column=0, sticky=tk.W)
        self.h_entry = ttk.Entry(geo_lf)
        self.h_entry.insert(0, str(self.results["chip_h"]))
        self.h_entry.grid(row=1, column=1, padx=5, pady=2)

        # 2. Blockage Manager Section
        block_lf = ttk.LabelFrame(main_frame, text="Obstacle Manager (Blockages)", padding="10")
        block_lf.pack(fill=tk.BOTH, expand=True, pady=10)

        # Listbox for current blockages
        self.blockage_list = tk.Listbox(block_lf, height=5)
        self.blockage_list.pack(fill=tk.BOTH, expand=True, pady=5)

        btn_frame = ttk.Frame(block_lf)
        btn_frame.pack(fill=tk.X)

        self.add_btn = ttk.Button(btn_frame, text="Add Block", command=self._add_blockage_popup)
        self.add_btn.pack(side=tk.LEFT, padx=2)

        self.rem_btn = ttk.Button(btn_frame, text="Remove Selected", command=self._remove_blockage)
        self.rem_btn.pack(side=tk.LEFT, padx=2)

        # 3. Algorithm Settings Section
        algo_lf = ttk.LabelFrame(main_frame, text="Algorithm Tuning", padding="10")
        algo_lf.pack(fill=tk.X, pady=10)

        ttk.Label(algo_lf, text="SA Iterations:").grid(row=0, column=0, sticky=tk.W)
        self.iters_entry = ttk.Entry(algo_lf)
        self.iters_entry.insert(0, "10000")
        self.iters_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(algo_lf, text="(Recommended: 10k-50k)", font=("", 8, "italic")).grid(row=0, column=2)

        ttk.Label(algo_lf, text="Bisection Depth:").grid(row=1, column=0, sticky=tk.W)
        self.depth_entry = ttk.Entry(algo_lf)
        self.depth_entry.insert(0, "4")
        self.depth_entry.grid(row=1, column=1, padx=5, pady=2)
        ttk.Label(algo_lf, text="(Recommended: 3-5)", font=("", 8, "italic")).grid(row=1, column=2)

        # 4. Recommendation Panel
        tips_lf = ttk.LabelFrame(main_frame, text="AutoPlacer Tips", padding="10")
        tips_lf.pack(fill=tk.X, pady=10)
        tips_text = (
            "- Use more SA iterations for complex designs (>50 cells).\n"
            "- Higher Bisection Depth helps with very large chips.\n"
            "- Ensure blockages don't cover the entire chip area!"
        )
        ttk.Label(tips_lf, text=tips_text, wraplength=400, justify=tk.LEFT).pack()

        # Final Actions
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=20)
        
        self.start_btn = ttk.Button(action_frame, text="💾 Save & Run Placement", command=self._on_start)
        self.start_btn.pack(side=tk.RIGHT, padx=5)

    def _add_blockage_popup(self):
        # Local pop-up for entering blockage coordinates
        popup = tk.Toplevel(self.root)
        popup.title("New Blockage")
        popup.geometry("250x200")
        
        frame = ttk.Frame(popup, padding=10)
        frame.pack()

        entries = {}
        for i, label in enumerate(["X0", "Y0", "X1", "Y1"]):
            ttk.Label(frame, text=f"{label}:").grid(row=i, column=0)
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1)
            entries[label] = entry

        def save():
            try:
                vals = [float(entries[l].get()) for l in ["X0", "Y0", "X1", "Y1"]]
                self.results["blockages"].append(tuple(vals))
                self.blockage_list.insert(tk.END, f"Block: ({vals[0]}, {vals[1]}) to ({vals[2]}, {vals[3]})")
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")

        ttk.Button(frame, text="Add", command=save).grid(row=4, columnspan=2, pady=10)

    def _remove_blockage(self):
        selection = self.blockage_list.curselection()
        if selection:
            idx = selection[0]
            self.blockage_list.delete(idx)
            self.results["blockages"].pop(idx)

    def _on_start(self):
        try:
            self.results["chip_w"] = float(self.w_entry.get())
            self.results["chip_h"] = float(self.h_entry.get())
            self.results["anneal_iters"] = int(self.iters_entry.get())
            self.results["num_partitions"] = int(self.depth_entry.get())
            
            # Basic Validation
            if self.results["chip_w"] <= 0 or self.results["chip_h"] <= 0:
                raise ValueError("Dimensions must be positive.")
                
            self.confirmed = True
            self.root.destroy()
        except ValueError as e:
            messagebox.showerror("Validation Error", f"Invalid input: {e}")

    def run(self) -> Optional[Dict[str, Any]]:
        self.root.mainloop()
        return self.results if self.confirmed else None

def get_user_params(default_w=1000.0, default_h=1000.0):
    gui = ConfigGUI(default_w, default_h)
    return gui.run()
