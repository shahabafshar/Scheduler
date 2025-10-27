# Basics of Real-Time Systems

## Introduction
This document covers the fundamental concepts and terminologies used in real-time systems design and analysis.

## Real-Time System Definition

A **Real-Time System** (RTS) is a computing system that must respond to external events within strict time constraints. The correctness of the system depends on both:
1. **Logical correctness**: Producing correct results
2. **Temporal correctness**: Producing results at the right time

## Types of Real-Time Systems

### Hard Real-Time Systems
- **Critical**: Missing a deadline can cause catastrophic failure
- **Examples**: Aircraft control, medical life support, nuclear power plants
- **Requirements**: Absolute guarantees on meeting deadlines

### Soft Real-Time Systems
- **Non-Critical**: Missing deadlines degrades quality but doesn't cause failure
- **Examples**: Video streaming, games, multimedia applications
- **Requirements**: Best-effort to meet deadlines, statistical guarantees

### Firm Real-Time Systems
- **Value-based**: Missing a deadline results in zero value
- **Examples**: Stock trading systems, sensor data processing
- **Requirements**: High probability of meeting deadlines

## Real-Time Task Model

### Task Parameters
```
τ = (r, e, d, p, J, D)
```
Where:
- **r**: Release time (ready time)
- **e**: Execution time (computation time)
- **d**: Deadline
- **p**: Period (for periodic tasks)
- **J**: Jitter (maximum variation in release time)
- **D**: Task duration (relative deadline)

### Task Types

#### Periodic Tasks
- Executed at regular intervals
- Fully characterized by: period (T) and execution time (C)
- Example: Control loop that runs every 10ms

#### Aperiodic Tasks
- Triggered by external events
- No fixed period
- Example: Alarm handling, user input processing

#### Sporadic Tasks
- Similar to aperiodic tasks
- Has minimum inter-arrival time (MIT)
- Helps in predictability

## Scheduling Concepts

### Scheduling Policy
The algorithm that determines which task executes at any given time.

### Scheduling Attributes

1. **Priority**: Numerical value indicating importance
2. **Preemption**: Can a running task be interrupted?
3. **Criticality**: Impact of missing deadline
4. **Resource requirements**: CPU, memory, I/O

### Preemption

#### Preemptive Scheduling
- Higher priority tasks can interrupt lower priority tasks
- Better responsiveness for high-priority tasks
- Overhead due to context switching
- Example: Rate Monotonic Scheduling (RMS)

#### Non-Preemptive Scheduling
- Tasks run to completion once started
- No context switching overhead
- May cause priority inversion
- Example: Cyclic Executive

### Jitter
- Variation in task release times
- Can affect system predictability
- Bounded jitter is often required

## System Components

### Real-Time Tasks
- **Independent Tasks**: No precedence constraints
- **Precedence Tasks**: Dependencies between tasks
- **Synchronous Tasks**: Released at specific times
- **Asynchronous Tasks**: Released by events

### Resources
- **Shared Resources**: Accessed by multiple tasks
- **Mutually Exclusive**: Only one task at a time
- **Preemptable**: Can be taken away
- **Non-Preemptable**: Must be held until release

### Scheduling Algorithms

#### Static Priority Algorithms
- Priorities assigned offline
- Example: Rate Monotonic, Deadline Monotonic

#### Dynamic Priority Algorithms
- Priorities assigned at runtime
- Example: Earliest Deadline First (EDF), Least Laxity First

## Performance Metrics

### Timing Metrics
1. **Worst-Case Execution Time (WCET)**: Maximum time to complete
2. **Best-Case Execution Time (BCET)**: Minimum time to complete
3. **Average Execution Time**: Expected execution time
4. **Response Time**: Time from release to completion
5. **Latency**: Delay in responding to events

### Utilization Metrics
1. **Processor Utilization**: Percentage of time CPU is busy
2. **Resource Utilization**: Usage of shared resources
3. **Communication Utilization**: Network bandwidth usage

## Design Considerations

### Predictability
- Deterministic behavior
- Bounded response times
- Known worst-case scenarios

### Safety
- Error detection mechanisms
- Fault tolerance
- Backup systems

### Timeliness
- Meeting deadlines consistently
- Minimum jitter
- Bounded latency

## Scheduling Paradigms

### Time-Triggered
- Tasks scheduled at regardless of events
- Predictable timing behavior
- Used in safety-critical systems

### Event-Triggered
- Tasks scheduled in response to events
- More flexible and efficient
- Less predictable timing

### Hybrid
- Combination of both approaches
- Best of both worlds
- More complex to design

## Sources
- Lecture 2 - Basics of Real-Time Systems, Part 1-2.pdf
