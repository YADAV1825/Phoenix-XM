# Scheduler Hierarchy

Efficient execution requires keeping the execution units fed. Phoenix-XM relies on a nested hierarchy of schedulers.

## Hierarchy Flow

```text
Kernel Scheduler (Host CPU / Driver)
       ↓
Global Tile Scheduler (GPU Top-Level)
       ↓
CTA Dispatcher (Per Tile)
       ↓
Warp Scheduler (Per SM)
```

## Scheduler Roles

### 1. Kernel Scheduler
Lives in the Host Runtime. It is responsible for compiling the kernel, tracking total available GPU memory, allocating buffers, and issuing the initial grid dimensions (total blocks, threads per block) over the PCIe bus.

### 2. Global Tile Scheduler
Lives in `phoenix_global_scheduler.sv`. When a kernel is launched, this hardware block evaluates the physical location of the data the kernel will operate on. It distributes the blocks to specific Tiles aiming to maximize data locality (preventing excessive traffic over the Inter-Tile Fabric).

### 3. CTA Dispatcher (Block Dispatcher)
Lives in `phoenix_dispatcher.sv` on every Tile. It maintains a queue of blocks assigned to its Tile. It constantly polls the 4 local SMs for their warp occupancy. When an SM finishes a block and clears its warp slots, the Dispatcher immediately pushes a new block to that SM.

### 4. Warp Scheduler
Lives in `phoenix_warp_scheduler.sv` on every SM. It tracks the Program Counter, Active Mask, and Stall Status of 8 independent warps. Every clock cycle, it evaluates the ready status of all 8 warps and selects one to issue to the instruction fetch unit. This round-robin switching is what allows the SM to completely hide memory latencies without halting the hardware.
