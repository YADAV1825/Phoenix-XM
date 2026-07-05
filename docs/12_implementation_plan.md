# Implementation Plan & Tracking

This document tracks the detailed engineering roadmap and phase execution of Phoenix-XM.

## Phase 1: Foundation (Completed)
- [x] Write `phoenix_pkg.sv` (Constants, ISA definitions).
- [x] Create Python Assembler (`phoenix_asm.py`).
- [x] Implement the RV32IM Decoder (`phoenix_decode.sv`).

## Phase 2: Pipeline (Completed)
- [x] Implement 4-lane SIMD ALU (`phoenix_alu.sv`).
- [x] Implement Banked Register File (`phoenix_regfile.sv`).
- [x] Implement 6-stage SM Pipeline (`phoenix_sm.sv`).

## Phase 3: Scheduler (Completed)
- [x] Implement 8-Warp Scheduler (`phoenix_warp_scheduler.sv`).
- [x] Implement Block Dispatcher (`phoenix_dispatcher.sv`).

## Phase 4: Memory & Caches (Completed)
- [x] Implement Non-Blocking LSU (`phoenix_lsu.sv`).
- [x] Implement Shared Memory Scratchpad (`phoenix_shared_mem.sv`).
- [x] Implement L1 and L2 Caches (`phoenix_l1_dcache.sv`, `phoenix_l2_cache.sv`).

## Phase 5: Scaling Out (Completed)
- [x] Implement the Compute Tile (`phoenix_tile.sv`).
- [x] Implement the Top-Level GPU (`phoenix_gpu.sv`).
- [x] Implement Global Scheduler (`phoenix_global_scheduler.sv`).

## Phase 6: Validation (Current)
- [x] Create Cocotb Runtime (`phoenix_runtime.py`).
- [x] Write Vector Addition Test (`test_vecadd.py`).
- [ ] Run RTL Simulation (Waiting on Simulator Installation).

## Phase 7: Future Exploration
- [ ] Implement advanced optical routing in `phoenix_fabric.sv`.
- [ ] Expand Tensor Core to support FP16.
