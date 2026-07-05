# The Execution Pipeline

Phoenix-XM utilizes a classic 6-stage execution pipeline designed to maximize throughput and minimize stalls.

## Pipeline Stages

```text
Schedule
   ↓
Fetch
   ↓
Decode
   ↓
Issue
   ↓
Execute
   ↓
Commit (Writeback)
```

1. **Schedule**: The Warp Scheduler selects one "Ready" warp and emits its Program Counter (PC) and Active Thread Mask.
2. **Fetch**: The PC is used to index into the L1 Instruction Cache. The 32-bit instruction is returned.
3. **Decode**: The 32-bit RV32IM machine code is combinationally expanded into a wide internal control bundle (`decoded_instr_t`), mapping opcodes to specific execution units.
4. **Issue**: The decoded bundle and the read operands from the Register File are latched into the pipeline registers.
5. **Execute**: The appropriate functional unit (ALU, LSU, Tensor Core, or SFU) performs the operation. The ALU completes in 1 cycle; the LSU and Tensor Cores may take multiple cycles.
6. **Commit**: Results are written back to the Register File.

## Pipeline Hazards

### Data Hazards (Read-After-Write)
Currently, data hazards are resolved implicitly through the Warp Scheduler's round-robin nature. If the number of active warps is greater than the pipeline depth, back-to-back dependencies within the same warp naturally resolve before that warp is scheduled again. 
*(Future implementation: Scoreboarding will be added to strictly enforce data dependencies when warp counts drop below pipeline depth).*

### Structural Hazards
Structural hazards (e.g., two execution units attempting to write to the Register File on the same cycle) are handled by a priority multiplexer in the writeback stage. The LSU's delayed memory return is given highest priority, potentially forcing the ALU to stall if a collision occurs.

### Control Hazards (Branches)
Resolved via an IPDOM (Immediate Post-Dominator) stack managed by the Special Function Unit (SFU). When a branch divergence occurs, the warp is split: one path is pushed to the stack, and the other is executed. When the executed path reaches a Reconvergence Barrier, the stack is popped.
