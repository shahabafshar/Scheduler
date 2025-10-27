# Controller Area Network (CAN Bus)

## Introduction

Controller Area Network (CAN) is a fast serial bus designed to provide an efficient and reliable link between sensors and actuators.

### Key Advantages
- **Low cost**
- **Handles high sensor data volumes** with minimal latency
- **Supports integration** of advanced control systems, sensors, actuators, etc.
- **Real-time deterministic** communication

---

## Technical Specifications

### Physical Layer
- Uses a **twisted pair cable** (dual-wire: CAN High and CAN Low)
- Communicate at speeds **up to 8Mbit/s** (max)
- **Up to 255 devices** on a single network
- Supports **multiple data rates** – high data rate bus, low data rate bus

### Standard
- **CAN Layered ISO 11898 Standard** (conforming to OSI model)
- Developed by **BOSCH**
- Multi-master, message broadcast system
- Maximum signaling rate: **1 megabit per second** (bps) typically

---

## CAN Features

1. **Any node can access the bus** when the bus is quiet

2. **Non-destructive bit-wise arbitration** to allow 100% use of the bandwidth without loss of data

3. **Variable message priority** based on 11-bit / 29-bit packet identifier

4. **Peer-to-peer and multi-cast reception**

5. **Automatic error detection, signaling and retries**

6. **Data packets**: 4 or 8 bytes long

7. **#
ynchronous communication** (Event Triggered)

---

## CAN Message Structure

### Standard CAN Frame
- **11-bit identifier**

### Extended CAN Frame
- **29-bit identifier**

### Message Types/Frames

1. **Data Frame**: Contains actual data
2. **Remote Frame**: Used to request data from another node
3. **Error Frame**: Special message that violates formatting rules
4. **Overload Frame**: Used to request a delay between frames

---

## Arbitration Mechanism

### How It Works

**Bit-Wise Non-Destructive Arbitration:**
- If two messages are simultaneously sent over the CAN bus, the bus takes the **"logical AND"** of all of them
- Message identifiers with the **lowest binary number** get the **highest priority**
- Every device listens on the channel and **backs off** when it notices a mismatch between the bus's bit and its identifier's bit

### Key Characteristics

**Priority Allocation:**
- The **lower the binary message identifier number**, the **higher its priority**
- An identifier consisting entirely of zeros is the **highest priority message** on a network
- **Dominant bit** (logic-low) always overwrites **recessive bit** (logic-high)

**Collision Resolution:**
- Node sending a last identifier bit as a zero (dominant) while other nodes send a one (recessive) **retains control** of the CAN bus
- Goes on to complete its message without destruction or corruption

---

## Inverted Logic

### CAN Bus Logic

A fundamental CAN characteristic is the **opposite logic state** between the bus, and the driver input and receiver output:

- Normally, logic-high is associated with a "1"
- Logic-low is associated with a "0"
- **But not so on a CAN bus!**

### Physical Implementation

- **Logic-low = dominant** (transmitted)
- **Logic-high = recessive** (default state)
- CAN transceivers have driver input and receiver output pins passively pulled high internally
- In the absence of any input, the device automatically defaults to a **recessive bus state**

---

## Communication Protocol

### CSMA/CD+AMP

CAN uses a **carrier-sense, multiple-access protocol with collision detection and arbitration on message priority** (CSMA/CD+AMP):

- **CSMA**: Each node on a bus must wait for a prescribed period of inactivity before attempting to send a message
- **CD+AMP**: Collisions are resolved through **bit-wise arbitration**, based on a preprogrammed priority of each message in the identifier field

### Arbitration Process

Since every node on a bus takes part in writing every bit "as it is being written," an arbitrating node knows if it placed the logic-high bit on the bus.

**Non-destructive**: The node winning arbitration just continues on with the message, without the message being destroyed or corrupted by another node.

---

## Error Handling

### Error Frame

- Special message that **violates the formatting rules** of a CAN message
- Transmitted when a node detects an error in a message
- Causes **all other nodes** in the network to send an error frame as well
- The original transmitter then **automatically retransmits** the message

### Error Counters

- Elaborate system of error counters in the CAN controller
- Ensures that a node **cannot tie up a bus** by repeatedly transmitting error frames

---

## Applications

### Intra-Vehicular Communication

CAN bus is widely used in automotive systems for connecting various ECUs (Electronic Control Units):
- Engine Control ECU
- Transmission Control ECU
- Brake Control ECU
- Airbag Control ECU
- Steering ECU
- Body Control ECU
- Lighting Control ECU

### Industrial Applications

- **Concrete State Monitor & Control System**
- **MRI Cooling System**
- **Tram Energy Recycle System**
- **Industrial automation**

### Real-Time Characteristics

- **Deterministic message delivery**
- **Predictable worst-case response times**
- **Priority-based message ordering**
- Essential for safety-critical applications

---

## Bus Topology vs Point-to-Point

### Trade-off

By introducing a **single bus** as the only means of communication (as opposed to point-to-point network):
- ✅ **Circuit simplicity**
- ❌ **Channel access complexity**

### MAC Protocol

Since two devices might want to transmit simultaneously, we need a **MAC (Medium Access Control) protocol** to handle the situation.

**CAN Solution:** Uses a unique identifier for each outgoing message, where **the identifier of a message represents its priority**.

---

## Implementation Example

### Hardware Components

- **Raspberry Pi 3 Model B+**: Higher-level processing node
- **Arduino UNO**: Sensor/actuator control node
- **MCP2515 CANbus Transceiver Board**: Converts CAN messages to SPI signals (and vice versa)
- **10kΩ Potentiometer Sensor**: Sensor input

### Software Components

- **Raspbian OS** (Linux & Python based) for RPi
- **Arduino UNO IDE** (Code written in C)
- **SocketCAN** Linux CANbus Driver Package
- **Python Library** – canutils, cantools, PyQt5

### Implementation Architecture

```
┌─────────────┐
│  Arduino    │
│   UNO       │─── MCP2515 ───┐
│  (Node A)   │                │
└─────────────┘                │
                               ├── CAN Bus (CAN_H, CAN_L)
┌─────────────┐                │
│ Raspberry   │                │
│     Pi      │─── MCP2515 ───┘
│  (Node B)   │
└─────────────┘
```

**Features:**
- Two-wire circuit comprising of CAN High and CAN Low
- MCP2515 board converts CAN messages into SPI signals
- Arduino programmed using C
- Raspberry Pi programmed using Python (acts as HMI)

---

## Real-World Performance Characteristics

### Advantages

✅ **Robust noise immunity** and fault tolerance
✅ **Deterministic real-time communication**
✅ **Priority-based arbitration** ensures critical messages are delivered first
✅ **Built-in error detection** and automatic retransmission

### Limitations

❌ **Lacks data security and privacy** (unencrypted)
❌ **Limited payload size** (4-8 bytes per message)
❌ **Bus length limitations** based on data rate

---

## Summary

CAN bus is an ideal solution for **real-time distributed control systems** where:
- Deterministic communication is required
- Multiple nodes need to share information
- Priority-based message ordering is important
- Cost-effective networking is needed

The **non-destructive bit-wise arbitration** mechanism ensures that the highest priority messages always get through while maintaining 100% bandwidth utilization without data loss.

**Source:** CprE 4580/5580: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

