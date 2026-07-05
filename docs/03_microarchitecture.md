# SM Microarchitecture

The Streaming Multiprocessor (SM) is the core computational engine of Phoenix-XM.

## Component Layout

```text
Streaming Multiprocessor (SM)

      Warp Scheduler
            ↓
    Instruction Fetch
            ↓
   Instruction Decode
            ↓
  Issue / Pipeline Reg
            ↓
 ┌──────────┼──────────┐
 │          │          │
ALU        LSU    Tensor Core
 │          │          │
 └──────────┼──────────┘
            ↓
      Register File
```

## Key Components

### Warp Scheduler
Maintains the architectural state (Program Counter and Active Thread Mask) for multiple concurrent warps (default 8). It performs zero-cycle context switching to hide memory latency.

### Registers
A highly banked static RAM structure. Each thread possesses 32 independent 32-bit registers. The register file provides multi-port access to feed the execution units without stalling.

### ALU (Arithmetic Logic Unit)
A SIMD (Single Instruction, Multiple Data) engine. A single instruction decoded by the SM drives multiple parallel ALUs (lanes) simultaneously, executing standard integer math, shifts, and comparisons.

### LSU (Load-Store Unit)
Handles memory traffic. Features a Miss Status Holding Register (MSHR) to track outstanding memory requests. It operates asynchronously from the main pipeline, signaling the Warp Scheduler to stall/unstall specific warps based on data availability.

### Tensor Core
A specialized dense-math execution unit utilizing an integer systolic array. It handles matrix multiplications natively in hardware.

### Shared Memory
A highly banked, software-managed scratchpad memory that resides inside the SM, bypassing the L1/L2 cache hierarchy entirely for ultra-low latency thread-to-thread communication.
