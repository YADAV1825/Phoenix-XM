# Memory Hierarchy

Phoenix-XM employs a multi-tiered memory hierarchy to balance latency, capacity, and bandwidth.

## Hierarchy Flow

```text
Registers (Local to Thread)
       ↓
Shared Memory (Local to Block/SM)
       ↓
L1 Cache (Local to SM)
       ↓
L2 Cache (Local to Tile)
       ↓
HBM / Global Memory (Device-wide)
```

## Layers Explained

### Registers
* **Latency**: 1 cycle.
* **Scope**: Thread-private.
* **Architecture**: Highly banked. Each thread has 32 independent 32-bit registers.

### Shared Memory
* **Latency**: 1-2 cycles.
* **Scope**: Shared among all threads in a CTA (Block) running on the same SM.
* **Architecture**: 4KB of heavily banked (4 interleaved banks) SRAM. Requires explicit software management (`lw`, `sw`). Essential for avoiding global memory trips during matrix operations.

### L1 Cache (Instruction & Data)
* **Latency**: ~3 cycles.
* **Scope**: Local to the SM.
* **Architecture**: Write-through Data cache, Read-only Instruction cache. Misses generate a request on the Tile Crossbar.

### L2 Cache
* **Latency**: ~10 cycles.
* **Scope**: Shared by all SMs within a specific Tile.
* **Architecture**: Backed by the Tile Crossbar. Filters redundant requests from different SMs before they hit the global interconnect.

### Global Memory (HBM)
* **Latency**: ~100-300 cycles.
* **Scope**: Globally accessible across all Tiles.
* **Architecture**: High Bandwidth Memory controllers. Accessed via the Inter-Tile Fabric.
