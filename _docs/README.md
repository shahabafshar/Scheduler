# Real-Time Scheduling Documentation

This directory contains comprehensive documentation on real-time scheduling concepts and algorithms extracted from the PDF resources.

## Directory Structure

### 01-Fundamentals/
- **01-Concepts-of-Real-Time-Systems.md**: Basic concepts and characteristics of real-time systems
- **02-Basics-of-Real-Time-Systems.md**: Fundamental terminology and task models

### 02-Task-Scheduling/
- **01-Basic-Task-Scheduling.md**: Fundamental scheduling algorithms (RMS, DMS, EDF)
- **02-Advanced-Task-Scheduling.md**: Response time analysis and schedulability tests
- **03-Blocking-Time-Calculation.md**: Blocking time analysis and priority inversion

### 03-Resource-Protocols/
- **01-Resource-Access-Control-Protocols.md**: PIP, PCP, SRP and blocking analysis

### 04-Overload-Handling/
- **01-Imprecise-Computation-and-mk-Firm-Tasks.md**: Mandatory/optional decomposition and (m,k) firm model
- **02-Feedback-Control-Based-Scheduling.md**: Control-theoretic approaches
- **03-Best-Effort-Scheduling.md**: Utility-based scheduling

### 05-Advanced-Scheduling/
- **01-Combined-Scheduling.md**: Server-based approaches for mixed task sets
- **02-Scheduling-Precedence-Tasks.md**: Scheduling with dependency constraints

### 06-Real-Time-Networking/
- **01-CANbus.md**: CANbus protocol and priority-based arbitration
- **02-Packet-Scheduling.md**: Packet scheduling in wide area networks
- **03-QoS-Routing.md**: Quality of Service routing algorithms

### 07-Fault-Tolerance/
- **01-Dependability-Concepts.md**: Reliability, availability, safety concepts
- **02-Fault-Tolerant-Design-Techniques.md**: Redundancy and fault tolerance techniques
- **03-Failure-Case-Studies.md**: Real-world failure analysis

### 08-Practical-Implementations/
- **01-FreeRTOS-Tutorial.md**: FreeRTOS kernel overview and usage

## Key Topics Covered

### Scheduling Algorithms
- Rate Monotonic Scheduling (RMS)
- Deadline Monotonic Scheduling (DMS)
- Earliest Deadline First (EDF)
- Combined scheduling approaches

### Analysis Techniques
- Response time analysis
- Utilization-based tests
- Blocking time calculation
- Schedulability verification

### System Design
- Resource access protocols
- Overload handling
- Precedence constraints
- Real-time networking

### Reliability
- Fault tolerance techniques
- Dependability concepts
- Safety and integrity

### Implementation
- FreeRTOS usage
- Practical considerations
- Best practices

## How to Use This Documentation

1. Start with **Fundamentals** to understand basic concepts
2. Study **Task Scheduling** for core algorithms and analysis
3. Explore **Advanced Topics** for specific scenarios
4. Review **Fault Tolerance** for safety-critical considerations
5. Refer to **Practical Implementations** for hands-on guidance

## Sources

All documentation is derived from PDF files in the `resources` directory:
- Concepts of Real-Time Systems
- Real-Time Task Scheduling lectures
- Resource Access Control Protocols
- Overload handling techniques
- Combined Scheduling
- Scheduling with Precedence Tasks
- Real-Time LAN/WAN networking
- Dependability and Fault-Tolerant Design
- FreeRTOS Tutorial
- Failure Case Studies

## Additional Resources

For deeper understanding, refer to the original PDF sources and academic textbooks on real-time systems, scheduling theory, and fault-tolerant computing.
