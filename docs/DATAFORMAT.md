# AutoPlacer: Data Format Specification

This document describes the netlist and chip constraint formats used by AutoPlacer.

## 1. Netlist Dictionary Format

The core input is a Python dictionary containing `cells` and `nets`.

### Cells
Defined as a mapping of unique names to their attributes.
```python
"cells": {
    "cell_name": {
        "w": 100,           # Width (float)
        "h": 80,            # Height (float)
        "fixed": False,     # Optional: True for IO/Pads (bool)
        "x": 0.0,           # Optional: Initial/Fixed X (float)
        "y": 0.0            # Optional: Initial/Fixed Y (float)
    }
}
```

### Nets
Defined as a list of pin connections. Each pin must correspond to a key in the `cells` dictionary.
```python
"nets": [
    {"pins": ["cell_a", "cell_b", "cell_c"]}
]
```

---

## 2. Chip Constraints

### Blockages
Blockages are rectangular regions where cells are penalized or prohibited from dwelling. They are defined for each instance by an (x0, y0, x1, y1) bounding box.
- Core logic in `utils/samples.py` automatically generates CPU-like blockage patterns (pad rings, cache regions, crosses).

### Chip Dimensions
Configured via `CHIP_W` and `CHIP_H` in the `PlacementParams` object.

---

### Complex Architecture Patterns
The `examples/` directory demonstrates how to model advanced architectures:
- **Systolic Arrays**: Programmatic generation of large PE grids with mesh connectivity (`ai_accelerator_grid.py`).
- **Hub-and-Spoke SoC**: Modeling central NoC routers connected to diverse peripherals and large memory macros (`soc_peripheral_hub.py`).

## 3. Output Metrics

AutoPlacer calculates the following metrics after each run:
- **Wirelength (HPWL)**: Sum of half-perimeters of all net bounding boxes.
- **Density Overflow**: Measure of area where local cell density exceeds 70%.
- **Congestion**: A 2D heatmap indicating predicted routing hotspots.
