# Tensor Core

The Tensor Core (`phoenix_tensor_core.sv`) accelerates dense matrix operations commonly found in AI and ML workloads.

## Execution Flow

```text
TMMA Instruction Issued
       ↓
Load Matrix A (from Shared Mem/Regs)
Load Matrix B (from Shared Mem/Regs)
       ↓
Systolic Multiply (4 cycles)
       ↓
Accumulate (Matrix C)
       ↓
Writeback (to Regs/Shared Mem)
```

## Architecture

The Tensor Core is implemented as a 4x4 integer systolic array. 
Rather than a traditional ALU that executes one instruction per lane, a single `TMMA` instruction triggers a state machine inside the Tensor Core that manages data flow through the 16 Multiply-Accumulate (MAC) units over multiple clock cycles.

By keeping the data localized in the systolic array, register file reads and writes are heavily reduced compared to performing the same operations via standard SIMD ALUs.

## Supported Datatypes

* **Current**: INT8 (32-bit accumulation).
* **Future Implementation**: FP16, BF16, and FP32.
