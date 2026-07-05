# Vision & Philosophy

## Why Phoenix Exists

Modern GPU research can be highly complex, making it difficult for students, researchers, and engineers to experiment with new paradigms without getting bogged down in proprietary or overly complex toolchains.

The primary goal of Phoenix-XM is to serve as an **open-source educational and experimental platform for GPU architecture**.

## Problems in GPU Scaling

Modern GPU architectures face several scaling limitations that we aim to explore and address educationally:
* **Yield**: Building single monolithic silicon dies (reticle-limit) is incredibly expensive and prone to defects.
* **The Memory Wall**: Compute power scales at a different rate than memory bandwidth. Data movement is a primary bottleneck in both power and performance.
* **Interconnect Bottlenecks**: As GPUs transition to chiplets, moving data between separate silicon dies incurs latency and power overheads over electrical signaling.

## Core Philosophy

* **Modular**: Every stage, from the decoder to the warp scheduler, is designed to be easily swapped, tested, and upgraded.
* **Research-Friendly**: Written in standard, synthesizable SystemVerilog.
* **Open**: Fully open-source and free from proprietary NDAs or un-simulate-able black-box IPs.
* **Modern**: It embraces the reality of chiplet (tile-based) design from day one, rather than pretending the GPU is a single physical chip.

## Long-Term Vision

The ultimate trajectory of Phoenix-XM is the **Virtual Monolithic GPU** backed by an **Optical Fabric**. 

As electrical SerDes links reach their physical limits, optical interconnects (Photonic NoCs) will become necessary to link multiple chiplets together with low enough latency and high enough bandwidth that software cannot tell it is running on a multi-die system. Phoenix-XM aims to be the standard open-source RTL platform for simulating and testing these future topologies.
