# AutoPlacer: API Reference

This document provides a detailed reference for the public classes and methods in the `autoplacer` package.

## `PlacementEngine`
The main orchestrator class for the placement flow.

### `__init__(self, params: Optional[PlacementParams] = None)`
Initializes the engine. If `params` is not provided, uses default `PlacementParams`.

### `load_netlist(self, netlist: Dict)`
Parses a netlist dictionary and initializes the cell and net internal structures.
- **Arguments**: `netlist` (Dict) - See [DATAFORMAT.md](DATAFORMAT.md).

### `run(self, init_coords: Optional[Dict[str, Tuple[float, float]]] = None) -> Dict[str, Any]`
Executes all stages of the placement flow (QGP, RB, SA).
- **Returns**: A dictionary containing `wirelength_total`, `density_overflow_sum`, `congestion_heatmap`, and `anneal_accept_ratio`.

### `src/utils/gui.py`
Provides graphical interfaces for user interaction.
- `get_user_params(default_w, default_h)`: Launches the advanced configuration window and returns a dictionary of settings.

### `src/utils/visualize.py`
(self, metrics: Dict[str, Any])`
Generates Matplotlib plots for the final placement and congestion map.

---

## `PlacementParams`
Dataclass containing optimization and chip parameters.

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `chip_w` | float | - | Total width of the chip area. |
| `chip_h` | float | - | Total height of the chip area. |
| `num_partitions`| int | 4 | Number of recursive bipartitioning levels. |
| `anneal_iters` | int | 10000 | Number of simulated annealing moves. |
| `rng_seed` | int | 42 | Seed for reproducible random generation. |
| `visualize` | bool | True | Whether to enable plotting. |

---

## Utilities

### `utils.parser.parse_netlist`
Internal helper used by the engine to convert raw dictionaries into `Cell` and `Net` objects.

### `utils.samples.create_cpu_like_blockages`
Generates synthetic blockage regions typical of modern CPU layouts.
