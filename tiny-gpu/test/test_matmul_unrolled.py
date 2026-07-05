import cocotb
from cocotb.triggers import RisingEdge
from .helpers.setup import setup
from .helpers.memory import Memory
from .helpers.format import format_cycle
from .helpers.logger import logger

@cocotb.test()
async def test_matmul_unrolled(dut):
    # Program Memory
    # Unrolled 2x2 MatMul — same algorithm as Phoenix-XM's unrolled version.
    # No loops, no branches. Each thread computes its own C[i] element.
    # k-loop (N=2) is fully unrolled: body duplicated for k=0 and k=1.
    #
    # Original looped body (13 instrs with CMP+BRn) becomes:
    #   k=0 body (11 instrs, including k++) + k=1 body (10 instrs, no k++)
    # = 21 instructions for the compute, vs 13*2+2 = 28 dynamic in looped version.
    program_memory = Memory(dut=dut, addr_bits=8, data_bits=16, channels=1, name="program")
    program = [
        # Setup: compute thread index, row, col (same as looped version)
        0b0101000011011110, # MUL R0, %blockIdx, %blockDim
        0b0011000000001111, # ADD R0, R0, %threadIdx         ; i = blockIdx * blockDim + threadIdx
        0b1001000100000001, # CONST R1, #1                   ; increment
        0b1001001000000010, # CONST R2, #2                   ; N (matrix inner dimension)
        0b1001001100000000, # CONST R3, #0                   ; baseA (matrix A base address)
        0b1001010000000100, # CONST R4, #4                   ; baseB (matrix B base address)
        0b1001010100001000, # CONST R5, #8                   ; baseC (matrix C base address)
        0b0110011000000010, # DIV R6, R0, R2                 ; row = i // N
        0b0101011101100010, # MUL R7, R6, R2
        0b0100011100000111, # SUB R7, R0, R7                 ; col = i % N
        0b1001100000000000, # CONST R8, #0                   ; acc = 0
        0b1001100100000000, # CONST R9, #0                   ; k = 0

        # ---- k=0 iteration (unrolled) ----
        0b0101101001100010, #   MUL R10, R6, R2              ; row * N
        0b0011101010101001, #   ADD R10, R10, R9             ; + k
        0b0011101010100011, #   ADD R10, R10, R3             ; + baseA -> addr(A[row*N+k])
        0b0111101010100000, #   LDR R10, R10                 ; load A[row][k]
        0b0101101110010010, #   MUL R11, R9, R2              ; k * N
        0b0011101110110111, #   ADD R11, R11, R7             ; + col
        0b0011101110110100, #   ADD R11, R11, R4             ; + baseB -> addr(B[k*N+col])
        0b0111101110110000, #   LDR R11, R11                 ; load B[k][col]
        0b0101110010101011, #   MUL R12, R10, R11            ; A * B
        0b0011100010001100, #   ADD R8, R8, R12              ; acc += A*B
        0b0011100110010001, #   ADD R9, R9, R1               ; k++ (k=1 now)

        # ---- k=1 iteration (unrolled, no increment needed) ----
        0b0101101001100010, #   MUL R10, R6, R2              ; row * N
        0b0011101010101001, #   ADD R10, R10, R9             ; + k
        0b0011101010100011, #   ADD R10, R10, R3             ; + baseA
        0b0111101010100000, #   LDR R10, R10                 ; load A[row][k]
        0b0101101110010010, #   MUL R11, R9, R2              ; k * N
        0b0011101110110111, #   ADD R11, R11, R7             ; + col
        0b0011101110110100, #   ADD R11, R11, R4             ; + baseB
        0b0111101110110000, #   LDR R11, R11                 ; load B[k][col]
        0b0101110010101011, #   MUL R12, R10, R11            ; A * B
        0b0011100010001100, #   ADD R8, R8, R12              ; acc += A*B

        # Store result and return
        0b0011100101010000, # ADD R9, R5, R0                 ; addr(C[i]) = baseC + i
        0b1000000010011000, # STR R9, R8                     ; store C[i] in global memory
        0b1111000000000000  # RET                            ; end of kernel
    ]

    # Data Memory (same as looped test)
    data_memory = Memory(dut=dut, addr_bits=8, data_bits=8, channels=4, name="data")
    data = [
        1, 2, 3, 4, # Matrix A (2 x 2)
        1, 2, 3, 4, # Matrix B (2 x 2)
    ]

    # Device Control
    threads = 4

    await setup(
        dut=dut,
        program_memory=program_memory,
        program=program,
        data_memory=data_memory,
        data=data,
        threads=threads
    )

    data_memory.display(12)

    cycles = 0
    while dut.done.value != 1:
        data_memory.run()
        program_memory.run()

        await cocotb.triggers.ReadOnly()
        format_cycle(dut, cycles, thread_id=1)

        await RisingEdge(dut.clk)
        cycles += 1

    logger.info(f"Completed in {cycles} cycles")
    data_memory.display(12)

    # Verify (same expected results as looped version)
    matrix_a = [data[0:2], data[2:4]]
    matrix_b = [data[4:6], data[6:8]]
    expected_results = [
        matrix_a[0][0] * matrix_b[0][0] + matrix_a[0][1] * matrix_b[1][0],  # C[0,0] = 7
        matrix_a[0][0] * matrix_b[0][1] + matrix_a[0][1] * matrix_b[1][1],  # C[0,1] = 10
        matrix_a[1][0] * matrix_b[0][0] + matrix_a[1][1] * matrix_b[1][0],  # C[1,0] = 15
        matrix_a[1][0] * matrix_b[0][1] + matrix_a[1][1] * matrix_b[1][1],  # C[1,1] = 22
    ]
    for i, expected in enumerate(expected_results):
        result = data_memory.memory[i + 8]
        assert result == expected, f"Result mismatch at index {i}: expected {expected}, got {result}"
