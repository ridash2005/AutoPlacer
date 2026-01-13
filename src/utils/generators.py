from .samples import CHIP_W, CHIP_H

def create_systolic_array(rows=10, cols=10):
    """Generates a 2D mesh netlist typical of AI accelerators."""
    cells = {}
    nets = []
    
    # Create PEs
    for r in range(rows):
        for c in range(cols):
            name = f"PE_{r}_{c}"
            cells[name] = {"w": 40, "h": 40}
            
            # Local mesh connections
            if r > 0:
                nets.append({"pins": [f"PE_{r-1}_{c}", name]})
            if c > 0:
                nets.append({"pins": [f"PE_{r}_{c-1}", name]})
                
    # Add Weight Memory interfaces (Fixed at bottom)
    for c in range(cols):
        name = f"W_MEM_{c}"
        cells[name] = {"w": 40, "h": 100, "fixed": True, "x": c * 150 + 400, "y": 50}
        nets.append({"pins": [name, f"PE_0_{c}"]})
        
    return {"cells": cells, "nets": nets}

def create_modern_soc():
    """Generates a multi-core SoC architecture with peripheral hub."""
    cells = {
        # 4 CPU Cores
        "CORE_0": {"w": 250, "h": 250}, "CORE_1": {"w": 250, "h": 250},
        "CORE_2": {"w": 250, "h": 250}, "CORE_3": {"w": 250, "h": 250},
        
        # Shared Resources
        "L3_CACHE_0": {"w": 400, "h": 200}, "L3_CACHE_1": {"w": 400, "h": 200},
        "NOC_ROUTER": {"w": 150, "h": 150},
        
        # Peripherals
        "DDR_CTRL": {"w": 200, "h": 100}, "PCIE_PHY": {"w": 150, "h": 120},
        "USB_HUB": {"w": 100, "h": 80}, "ETHERNET_PHY": {"w": 120, "h": 100},
        
        # Fixed IO / Macros
        "IO_PAD_TOP": {"w": CHIP_W, "h": 50, "fixed": True, "x": 0, "y": CHIP_H-50},
        "IO_PAD_BOT": {"w": CHIP_W, "h": 50, "fixed": True, "x": 0, "y": 0}
    }
    
    nets = [
        {"pins": ["CORE_0", "NOC_ROUTER"]}, {"pins": ["CORE_1", "NOC_ROUTER"]},
        {"pins": ["CORE_2", "NOC_ROUTER"]}, {"pins": ["CORE_3", "NOC_ROUTER"]},
        {"pins": ["NOC_ROUTER", "L3_CACHE_0", "L3_CACHE_1"]},
        {"pins": ["NOC_ROUTER", "DDR_CTRL", "PCIE_PHY"]},
        {"pins": ["PCIE_PHY", "IO_PAD_TOP"]}, {"pins": ["DDR_CTRL", "IO_PAD_BOT"]},
        {"pins": ["NOC_ROUTER", "USB_HUB", "ETHERNET_PHY"]}
    ]
    
    return {"cells": cells, "nets": nets}
