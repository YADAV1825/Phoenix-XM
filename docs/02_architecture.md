# Architecture Overview

Phoenix-XM is fundamentally a hierarchical system designed to distribute workloads from a central host out to a sea of identical compute tiles.

## The Hardware Hierarchy

```text
Host CPU (PCIe)
       ↓
GPU Runtime Driver
       ↓
Global Scheduler
       ↓
Compute Tiles
       ↓
Streaming Multiprocessors (SM)
       ↓
Execution Units
```

## Functional Layers

1. **Host & Runtime**: The CPU compiles the kernel (using the Phoenix assembler), allocates data in the GPU's memory space, and issues a kernel launch command containing grid dimensions (blocks and threads).
2. **Global Scheduler**: The entry point into the GPU hardware. It receives the kernel launch and determines which physical Compute Tile should receive which blocks of work.
3. **Compute Tiles**: The physically distinct chiplets. A tile contains a cluster of SMs (typically 4), a local block dispatcher, and a shared L2 Cache. 
4. **SM (Streaming Multiprocessor)**: The primary core. Responsible for fetching, decoding, scheduling, and executing instructions.
5. **Execution Units**: The lowest level hardware blocks inside the SM (ALUs, Load-Store Units, Tensor Cores) that perform the actual mathematical and memory operations.
