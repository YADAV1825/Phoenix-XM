# Runtime and Launch

The `phoenix_runtime.py` acts as the simulated PCIe Host Driver for the GPU.

## The Principle of Data Locality

In a distributed chiplet architecture, moving data is extremely expensive. Phoenix-XM operates on the principle of **Move Compute, Not Data**.

Rather than transferring terabytes of matrix data across the inter-tile fabric to a specific SM, the Runtime and Global Scheduler allocate the data into physical memory banks located on a specific Tile. The Global Scheduler then guarantees that the compute blocks assigned to operate on that data are launched *on the same Tile*.

## Kernel Launch Sequence

1. **Compilation**: The Python Assembler compiles the RISC-V assembly into machine code.
2. **Memory Allocation**: The Runtime writes the machine code into the GPU's Instruction Memory via the simulated host pins (`host_imem_wr_en`).
3. **Data Transfer**: The Runtime writes initial vectors/matrices into the GPU's Data Memory via (`host_dmem_wr_en`).
4. **Launch**: The Runtime pulses `host_kernel_valid` and passes the Program Counter, Block Count, and Threads Per Block.
5. **Wait**: The host waits until the hardware asserts `host_kernel_done`.
6. **Retrieval**: The Runtime reads the final computed results back out of GPU memory.
