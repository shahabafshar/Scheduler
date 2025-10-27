# Real-Time WAN: Packet Scheduling

## Overview
Packet scheduling algorithms manage the transmission order of packets in wide area networks to meet real-time constraints and QoS requirements.

## Network Scheduling Challenges

### Characteristics
- **Variable latency**: Network propagation delays
- **Packet loss**: Network congestion and errors
- **Jitter**: Variable end-to-end delay
- **Bandwidth limits**: Link capacity constraints

### Requirements
- Meet packet deadlines
- Manage bandwidth allocation
- Handle packet bursts
- Provide QoS guarantees

## Traffic Models

### Periodic Traffic
- Regular packet arrivals
- Fixed inter-arrival time
- Predictable pattern

### Bursty Traffic
- Variable packet taxonomy
- Bursts of packets
- Statistical characteristics

### Leaky Bucket Immodel
```
Parameters:
- ρ: Average rate
- σ: Burst size
- Maximum rate: ρ + σ/B
```

Where B is time window.

### Token Bucket Model
- Tokens accumulated at rate ρ
- Each token allows one packet transmission
- Maximum burst: σ tokens

## Packet Scheduling Algorithms

### 1. First-Come-First-Served (FCFS)
- Simple FIFO queuing
- No priority differentiation
- May starve low-rate flows

### 2. Priority Queuing (PQ)
- Multiple priority queues
- Higher priority always served first
- May starve lower priority

### 3. Weighted Fair Queuing (WFQ)
- Service rate proportional to weights
- Virtual time for fair allocation
- Bandwidth guarantees

### 4. Earliest Deadline First (EDF) for Packets
- Packets scheduled by earliest deadline
- Optimal for meeting deadlines
- Requires deadline information

## Sources
- Real-Time WAN -- Packet Scheduling, Part 1.pdf
- Real-Time WAN -- Packet Scheduling, Part 2.pdf
- Real-Time WAN -- Traffic Models.pdf
- Real-Time WAN -- Traffic Shaping_Policing.pdf
