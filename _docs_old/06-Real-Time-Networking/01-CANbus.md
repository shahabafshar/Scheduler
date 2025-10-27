# Real-Time LAN: CANbus

## Overview
Controller Area Network (CANbus) is a robust, distributed real-time communication protocol designed for embedded systems in automotive and industrial applications.

## CAN Protocol Fundamentals

### Purpose
- Serial communication protocol
- Multi-master bus
- Message-based communication
- Priority-based arbitration
- Fault-tolerant design

### Applications
- Automotive systems
- Industrial automation
- Medical devices
- Aircraft systems

## CAN Bus Topology

### Physical Layer
- **Bus structure**: Linear bus topology
- **Media**: Twisted pair cable
- **Termination**: 120Ω resistors at both ends
- **Nodes**: Connected via CAN transceiver

### Electrical Characteristics
- **Dominant bit**: 0 (driven to GND)
- **Recessive bit**: 1 (pulled high)
- **Bitwise arbitration**: Dominant wins
- **Differential signaling**: Noise immunity

## CAN Message Frame

### Frame Types

#### Standard Frame (11-bit identifier)
```
[SOF][11-bit ID][RTR][IDE][r0][DLC][DATA][CRC][ACK][EOF][IFS]
```

#### Extended Frame (29-bit identifier)
```
[SOF][11-bit ID][SRR][IDE][18-bit ID][RTR][r0][DLC][DATA][CRC][ACK][EOF][IFS]
```

### Frame Fields

#### Start of Frame (SOF)
- 1 bit
- Marks beginning of frame

#### Identifier Field
- 11 bits (standard) or 29 bits (extended)
- **Used for arbitration and priority**
- Lower value = higher priority
- Also used as message ID

#### Remote Transmission Request (RTR)
- 1 bit
- 0 = data frame
- 1 = remote frame (request data)

#### Identifier Extension (IDE)
- 1 bit
- 0 = standard frame (11-bit ID)
- 1 = extended frame (29-bit ID)

#### Data Length Code (DLC)
- 4 bits
- Indicates data field length (0-8 bytes)

#### Data Field
- 0-8 bytes
- Actual message payload

#### CRC Field
- 15 bits
- Cyclic Redundancy Check for error detection

#### ACK Slot
- 1 bit
- Acknowledgment bit
- Sent by receivers

#### End of Frame (EOF)
- 7 bits
- Marks end of frame

#### Inter-Frame Space (IFS)
- 3 bits
- Minimum separation between frames

## Priority-Based Arbitration

### CSMA/CA Protocol
- **Carrier Sense**: Nodes listen before transmitting
- **Multiple Access**: Multiple nodes can access bus
- **Collision Avoidance**: Non-destructive arbitration

### Arbitration Mechanism
1. All nodes start transmitting simultaneously
2. Each bit transmitted bit-by-bit
3. Recessive bits overridden by dominant bits
4. Losing nodes detect conflict and stop transmitting
5. Winner continues to completion

### Arbitration Example
```
Node A: 0 1 0 1 1 0 1 0 1 0 1  (ID = 0x55A)
Node B: 0 1 0 1 1 0 1 1 0 0 1  (ID = 0x56C)
        ^ ^ ^ ^ ^ ^ ^
       all match until bit 7...
       Node A transmits 0 (dominant)
       Node B transmits 1 (recessive)
       Node B loses and stops
       Node A continues
```

### Properties
- Non-destructive arbitration
- Deterministic priority ordering
- Lower ID = higher priority
- Predictable worst-case latency

## Real-Time Characteristics

### Message Latency

#### Components
1. **Arbitration time**: Log(ID) bits
2. **Frame transmission**: Data frame size
3. **Propagation delay**: Bus physical delay
4. **Queuing delay**: Waiting in transmit buffer

### Worst-Case Response Time

#### Busy Period Analysis
```
Busy period = time during which higher priority messages being transmitted
```

#### Response Time Calculation
```
Rᵢ = Jᵢ + Cᵢ + Bᵢ + Σⱼ∈hp(i) (⌈(Rᵢ + Jⱼ)/Tⱼ⌉ × Cⱼ)
```

Where:
- **Jᵢ**: Jitter (release time variation)
- **Cᵢ**: Transmission time
- **Bᵢ**: Blocking by lower priority messages
- **hp(i)**: Higher priority messages

### Transmission Time
```
C = (55 + 10d + 3)/bit_rate
```

Where:
- 55: Fixed overhead bits
- 10d: Data bits (d = DLC × 8)
- 3: Inter-frame space
- bit_rate: CAN bit rate (e.g., 1Mbps)

### Example Calculation
```
Message with 8 bytes @ 1Mbps:
C = (55 + 10×64 + 3)/1000000
C = 698/1000000 = 0.698 ms
```

## Error Handling

### Error Detection

#### CRC Error
- Mismatch in received CRC
- Frame retransmitted

#### Bit Error
- Stuff bit error detected
- Retransmission triggered

#### ACK Error
- No acknowledgment received
- Transmission retransmitted

#### Form Error
- Invalid bit patterns
- Frame considered invalid

### Error States
1. **Error Active**: Normal operation, can transmit
2. **Error Passive**: Limited transmission, no error flags
3. **Bus Off**: No transmission, requires recovery

### Error Recovery
- Automatic retransmission
- Error counter management
- Bus-off recovery procedure

## Scheduling Analysis

### Schedulability Test

#### Utilization Test
```
U = Σ(Cᵢ/Tᵢ) ≤ U_bound
```

#### Response Time Test
Compute worst-case response time and verify Rᵢ ≤ Dᵢ.

### Blocking Time
A message can be blocked by at most one lower priority message currently on bus.

```
Bᵢ = max{Cⱼ | Pⱼ < Pᵢ AND τⱼ can be on bus when τᵢ released}
```

### Priority Assignment
Lower CAN identifier = higher priority

```
Priority(τᵢ) = -CAN_IDᵢ
```

## CAN Variants

### Classical CAN
- Standard CAN protocol
- Up to 1 Mbps
- 11 or 29-bit identifiers

### CAN FD (Flexible Data-Rate)
- Extended data field (up to 64 bytes)
- Higher bit rates in data phase
- Backward compatible with Classical CAN

### CAN XL
- Extended payload capacity
- Up to 2048 bytes
- Non-backward compatible

## Design Considerations

### Message ID Assignment
- Based on priority requirements
- Lower ID for higher priority messages
- Grouping by criticality

### Bit Timing
- Bit rate configuration
- Propagation segment
- Phase segments
- Sample point optimization

### Network Topology
- Linear bus for simplicity
- Star topology with gateways
- Ring topology (rarer)

### Bandwidth Utilization
- Keep utilization < 70% for safety margin
- Account for error recovery overhead
- Consider burst arrivals

## Sources
- Real-Time LAN -- CANbus.pdf
- Introoduction to CAN BUS_(TI ).pdf
