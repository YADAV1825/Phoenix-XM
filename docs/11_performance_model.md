# Performance Model

This document outlines the theoretical, mathematically grounded performance expectations of the Phoenix-XM architecture.

*All calculations assume synthesis targeting a 1.5 GHz clock frequency.*

## Current Prototype Configuration
* 2 Compute Tiles
* 4 SMs per Tile (8 SMs total)
* 4 ALUs (Lanes) per SM
* 1 Tensor Core (4x4) per SM

### Peak INT32 Compute (Standard Math)
* 8 SMs × 4 Lanes/SM = 32 ALUs.
* 32 ALUs × 1 instruction/cycle × 1.5 GHz = **48 GOPS** (Giga-Operations Per Second).

### Peak Tensor Compute (INT8 AI Math)
* 8 SMs × 1 Tensor Core (4x4).
* A 4x4 array completes 16 MACs per cycle (after pipeline fill).
* 1 MAC = 2 Operations (Multiply + Add).
* 8 SMs × 16 MACs/cycle × 2 Ops/MAC × 1.5 GHz = **384 GOPS**.

### Memory Bandwidth
* **L1 Cache / Shared Memory**: 
  * 4 Banks × 32 bits = 128 bits/cycle per SM.
  * 128 bits × 1.5 GHz = 24 GB/s per SM.
  * System L1 Bandwidth: 8 SMs × 24 GB/s = **192 GB/s**.

---

## Scaled Configuration (The Virtual Monolith)
*If parameters were scaled to represent a modern datacenter accelerator (e.g., 64 Tiles, 4096 SMs):*

### Peak Compute
* **INT32**: 4096 SMs × 32 Lanes/SM × 1.5 GHz = **~196 TOPS** (Tera-Operations Per Second).
* **Tensor (INT8)**: 4096 SMs × 256 MACs/cycle × 2 Ops/MAC × 1.5 GHz = **~3.1 POPS** (Peta-Operations Per Second).

### Latency and Occupancy
Because the Warp Scheduler executes a 0-cycle context switch, memory latency is mathematically masked entirely as long as:
`Active Warps > (Memory Latency in Cycles / Instructions per Warp)`

For a 100-cycle L2 cache miss, maintaining 10 active warps per SM guarantees 100% pipeline utilization (occupancy).
