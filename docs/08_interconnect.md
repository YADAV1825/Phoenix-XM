# Interconnect Fabric

The Interconnect Fabric is the primary research contribution of the Phoenix-XM architecture. It represents the shift away from monolithic dies towards scalable chiplet systems.

## Current Implementation (Electrical/Simulated)

```text
Tile 0
   ↓
Fabric Router 0
   ↓
Inter-Tile Fabric (Simulated crossbar)
   ↓
Fabric Router 1
   ↓
Tile 1
```

In the current RTL, the fabric is modeled as a configurable-latency bus. When an L2 Cache misses, the request hits the Fabric Router. If the physical memory address belongs to a remote tile, the router packages the request and sends it over the fabric. 

## Future Implementation (Optical Fabric)

```text
Tile 0 (Electrical-to-Optical Ring Modulator)
   ↓
Photonic Waveguide (NoC)
   ↓
Tile 1 (Optical-to-Electrical Photodetector)
```

As electrical SerDes reaches its physical limits regarding power and edge density, optical interconnects will become necessary. Phoenix-XM aims to simulate Photonic Network-on-Chip (NoC) topologies. 

Future revisions of the `phoenix_fabric.sv` module will model specific optical routing protocols, wavelength-division multiplexing (WDM) collisions, and laser power constraints, providing a cycle-accurate testbed for optical GPU research.
