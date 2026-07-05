# ISA Reference

Phoenix-XM natively supports a subset of the standard RV32IM RISC-V instruction set, augmented with custom GPGPU extensions.

## Standard RV32IM Supported

### R-Type (Register-Register)
* `ADD`, `SUB`, `SLL`, `SLT`, `SLTU`, `XOR`, `SRL`, `SRA`, `OR`, `AND`
* `MUL`, `DIV`, `REM`

### I-Type (Register-Immediate)
* `ADDI`, `SLTI`, `SLTIU`, `XORI`, `ORI`, `ANDI`, `SLLI`, `SRLI`, `SRAI`

### B-Type (Branching)
* `BEQ`, `BNE`, `BLT`, `BGE`, `BLTU`, `BGEU`

### U/J-Type (Jumps and Upper Immediates)
* `LUI`, `AUIPC`, `JAL`, `JALR`

### Load/Store
* `LW`, `LH`, `LB`, `LHU`, `LBU`
* `SW`, `SH`, `SB`

---

## Phoenix-XM Custom GPGPU Extensions

*Currently under active development in the `phoenix_sfu.sv` module.*

### `RET` (Kernel Return)
* **Opcode**: `0x0B`
* **Semantics**: Signals that the warp has completed execution. When all warps in a block execute `RET`, the SM signals the Dispatcher that the block is complete.

### `TMC` (Thread Mask Control)
* **Semantics**: Dynamically updates the active thread mask for the warp, allowing certain lanes to be disabled during branch divergence.

### `WSPAWN` (Warp Spawn)
* **Semantics**: Allows a running block to dynamically request the Warp Scheduler to initialize and start a new warp at a specific PC.

### `SPLIT` / `JOIN`
* **Semantics**: Hardware-accelerated stack operations for the IPDOM (Immediate Post-Dominator) divergence stack. Ensures threads within a warp reconverge after `if/else` branching.

### `BAR` (Barrier)
* **Semantics**: Block-level synchronization. Warps executing this instruction are forcibly stalled by the SFU until all other active warps in the block reach the same barrier.

### `TMMA` (Tensor Matrix Multiply-Accumulate)
* **Semantics**: Triggers the 4x4 integer systolic array to multiply two matrices loaded from shared memory/registers and accumulate the result into a third matrix.
