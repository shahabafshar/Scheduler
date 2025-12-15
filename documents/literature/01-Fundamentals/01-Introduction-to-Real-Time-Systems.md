# Introduction to Real-Time Systems

## Definition

**Real-time systems** are defined as those systems in which the correctness of the system depends not only on the **logical result** of computation, but also on the **time** at which the results are produced.

### Key Characteristics

- The performance of real-time systems must be **predictable**
- Real-time systems often operate in a **constrained environment** – workload variations, fault conditions, resource constraints

## Types of Real-Time Systems

### Hard Real-Time Systems
- Missing a deadline can lead to **catastrophic consequences**
- Examples: Avionics, Command & Control Systems
- Penalty due to missing deadline is a **higher order of magnitude** than the reward in meeting the deadline

### Firm Real-Time Systems
- Missing deadlines results in **no value** (as if the task never executed)
- Examples: Radar tracking, manufacturing assembly line
- Penalty and reward are in the **same order of magnitude**

### Soft Real-Time Systems
- Missing deadlines **degrades system performance** but doesn't cause failure
- Examples: Video conferencing, multimedia applications
- Penalty often **lesser magnitude** than reward

## Real-Time Tasks (Workload)

### Periodic Tasks
- **Time-driven**. Characteristics are known *a priori*
- Task *Ti* is characterized by (*ci, pi*)
  - *ci*: worst-case execution time
  - *pi*: task period
- **Example:** Task monitoring temperature of a patient in an ICU

### Aperiodic Tasks
- **Event-driven**. Characteristics are **not** known *a priori*
- Task *Ti* is characterized by (*ai, ri, ci, di*)
  - *ai*: arrival time
  - *ri*: ready time
  - *ci*: computation time
  - *di*: deadline
- **Example:** Task activated upon detecting change in patient's condition

### Sporadic Tasks
- Known **minimum inter-arrival time** among successive instances of a (periodic) task, rather strictly being periodic
- Has a minimum inter-arrival time constraint

## Task Constraints

### 1. Deadline Constraint
- Latest time by which a task must complete

### 2. Resource Constraints
- **Shared access** (read-read): multiple tasks can read simultaneously
- **Exclusive access** (write-x, where x: read or write): only one task can access

### 3. Precedence Constraints
- Task T1 precedes T2 denoted as **T1 → T2**
- Task T2 can start its execution only after T1 finishes
- Precedence relations among tasks are denoted in the form of a graph, known as **precedence graph**

### 4. Fault-tolerant Requirements
- **Redundancy** in task execution to achieve higher reliability

## The Notion of Predictability

The most common denominator expected from a real-time system is **predictability**.

### Definition
**The behavior of the real-time system must be predictable** which means that with certain assumptions about workload and failures, it should be possible to show at **"design time"** that all the timing constraints of the application will be met.

### Static Systems
- 100% guarantees can be given at design time

### Dynamic Systems
- 100% guarantee **cannot be given** since the characteristics of tasks are not known a priori
- Predictability means that once a task is **admitted into the system** (based on online admission test), its guarantee should **never be violated** as long as the assumptions under which the task was admitted hold

## Computing System Architectures

- **Uniprocessor**: Single CPU system
- **Multiprocessor** (multicore systems): Multiple CPUs
- **Distributed system**: Multiple nodes communicating over network
- **Networked control systems**: Real-time control over network

## Common Misconceptions

❌ **Real-time computing is equivalent to fast computing**

❌ **Real-time programming is assembly coding, priority interrupt programming, and writing device drivers**

❌ **Real-time systems operate in a static environment**

❌ **The problems in real-time system design have all been solved in other areas of computer science**

## Source
CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

