# Fault-Tolerant Design Techniques

## Fault Tolerant Strategies

Fault tolerance in computer system is achieved through **redundancy** in hardware, software, information, and/or computations. Such redundancy can be implemented in **static, dynamic, or hybrid** configurations.

### Two Main Approaches

**Fault Masking:** Any process that prevents faults in a system from introducing errors.
- Example: Error correcting memories and majority voting

**Reconfiguration:** The process of eliminating faulty component from a system and restoring the system to some operational state.

---

## Reconfiguration Approach

### Steps in Reconfiguration

**1. Fault Detection**
- The process of **recognizing that a fault has occurred**
- Required before any recovery procedure can be initiated

**2. Fault Location**
- The process of **determining where a fault has occurred**
- Enables appropriate recovery to be initiated

**3. Fault Containment**
- The process of **isolating a fault**
- Prevents effects of that fault from propagating throughout the system

**4. Fault Recovery**
- The process of **remaining operational** or regaining operational status via reconfiguration even in the presence of faults

---

## The Concept of Redundancy

### Definition

Redundancy is simply the addition of **information, resources, or time** beyond what is needed for normal system operation.

### Types of Redundancy

**1. Hardware Redundancy**
- Addition of extra hardware
- Purpose: detecting or tolerating faults

**2. Software Redundancy**
- Addition of extra software beyond what is needed to perform a given function
- Purpose: detect and possibly tolerate faults

**3. Information Redundancy**
- Addition of extra information beyond light required to implement a given function
- Example: Error detection codes

**4. Time Redundancy**
- Uses additional time to perform the functions of a system
- Purpose: fault detection and often fault tolerance
- **Tolerates transient faults**

### Cost of Redundancy

Redundancy can have very important impact on:
- **Performance**
- **Size**
- **Weight**
- **Power consumption**
- **Reliability**

---

## Hardware Redundancy

### Passive Techniques

**Concept:** Use fault **masking**. Designed to achieve fault tolerance **without requiring any action** on the part of the system.

**Mechanism:** Relies on voting mechanisms.

**Example:** Triple Modular Redundancy (TMR)

### Active Techniques

**Concept:** Achieve fault tolerance by **detecting existence of faults** and performing some action to **remove faulty hardware** from the system.

**Process:**
- Fault detection
- Fault location
- Fault recovery

**Approach:** Remove and replace faulty components with spares.

### Hybrid Techniques

**Concept:** Combine attractive features of both passive and active approaches.

**Features:**
- **Fault masking** used to prevent erroneous results from being generated
- **Fault detection, location, and recovery** used to improve fault tolerance by removing faulty hardware and replacing with spares

---

## Hardware Redundancy - A Taxonomy

### Passive Techniques
- **Triple Modular Redundancy (TMR)**
- **N-Modular Redundancy (NMR)**
- **Duplication with Comparison**

### Active Techniques (Standby Sparing)
- **Hot standby** (Ready to take over immediately)
- **Cold standby** (Must be initialized before use)
- **Pair-and-a-Spare** (Two active components + spare)
- **Watchdog timer** (Detects processor failures)

### Hybrid Techniques
- **NMR with Spares** (Combine voting with spares)
- **Self-Purging Redundancy**
- **Sift-Out Redundancy**
- **Triple-Duplex Architecture**

---

## Triple Modular Redundancy (TMR)

### Architecture

```
Input 1 → MODULE 1 ┐
Input 2 → MODULE 2 ├→ VOTER → Output
Input 3 → MODULE 3 ┘
```

### How It Works

1. **Three identical modules** process the same input
2. **Voter** compares the three outputs
3. **Majority wins:** If any module fails, the other two provide correct output
4. **Mask fault** without system action

### Characteristics

- **Passive technique**: No fault detection/recovery needed
- **Fault masking**: Automatically masks single fault
- **Reliability:** System fails only if 2 or more modules fail simultaneously
- **Cost:** 3x hardware

### Limitation

- **Cannot tolerate multiple faults** (two modules failing simultaneously)

---

## Software Redundancy - To Detect Software Faults

### Two Popular Approaches

**1. N-Version Programming (NVP)**
- **Forward recovery scheme** - it masks faults
- Multiple versions of the same task executed **concurrently**
- Relies on **voting**

**2. Recovery Blocks (RB)**
- **Backward error recovery scheme**
- Versions of a task executed **serially**
- Uses acceptance tests

### Comparison

| Aspect | N-Version Programming | Recovery Blocks |
|--------|---------------------|----------------|
| **Execution** | Parallel | Sequential |
| **Recovery** | Forward (masking) | Backward |
| **Mechanism** | Voting | Acceptance test |
| **Performance** | Faster (parallel) | Slower (serial) |
| **Resource usage** | Higher | Lower |

---

## Hardware Redundancy Techniques Details

### Duplication with Comparison

**Architecture:**
- Two identical modules
- Compare outputs
- If outputs differ → fault detected

**Uses:**
- Fault detection (not tolerance)
- Checker circuits
- Less expensive than TMR

### Hot Standby

**Characteristics:**
- **Backup unit runs synchronously** with primary
- Ready to take over **immediately**
- No initialization needed

**Application:** Where fast recovery is critical

**Cost:** Continuous power for backup unit

### Cold Standby

**Characteristics:**
- Backup unit is **off or idle**
- Must be **initialized before use**
- Longer recovery time than hot standby

**Application:** Where recovery time is less critical

**Cost:** Lower power consumption

### Pair-and-a-Spare

**Architecture:**
- Two active components + one spare
- Spare replaces failed component
- Continue operation with remaining pair

**Benefit:** Tolerates two sequential failures

---

## Hybrid Redundancy Techniques

### NMR with Spares

**Concept:** Combine N-Modular Redundancy with spares

**How It Works:**
1. Initial N modules with voting
2. When module fails, spare replaces it
3. Continue with N-module voting

**Advantage:** Can tolerate multiple sequential failures

### Self-Purging Redundancy

**Concept:** Active voting combined with removal of failed units

**Process:**
1. All modules vote on results
2. Failed modules excluded from system
3. Continue with remaining good modules

### Sift-Out Redundancy

**Concept:** Sift out unreliable modules

**Process:**
1. Test all modules
2. Identify and remove unreliable ones
3. Use remaining high-reliability modules

### Triple-Duplex Architecture

**Concept:** Combination of triplication and duplication

**Architecture:**
- Three pairs of modules
- Each pair votes internally
- Three pair outputs vote together

---

## Fault Detection and Recovery Mechanisms

### Watchdog Timer

**Purpose:** Detect processor failures

**How It Works:**
- Processor must reset timer periodically
- If processor fails, timer expires
- Timer triggers recovery action

**Application:** Microcontrollers, embedded systems

### Checkpoint/Restart

**Concept:** Save system state periodically

**Recovery:**
- Restore to last checkpoint
- Re-execute from checkpoint
- Requires non-volatile storage

### Roll-Back Recovery

**Concept:** Maintain multiple checkpoints

**Recovery:**
- Roll back to earlier checkpoint if recovery fails
- Progressive roll-back until successful

---

## Design Considerations

### Cost vs. Reliability Trade-offs

**More redundancy = Higher reliability BUT:**
- Increased cost
- Increased complexity
- Increased power consumption
- Decreased performance

### Choosing the Right Technique

Consider:
- **Application requirements** (safety-critical level)
- **Cost constraints**
- **Size/weight limitations**
- **Power budget**
- **Recovery time requirements**
- **Environment** (harsh vs. benign)

### Fault Hypothesis

Define:
- **Maximum number of faults** to tolerate
- **Fault types** (permanent, transient, intermittent)
- **Fault locations** (which components can fail)

---

## Summary

### Key Strategies

1. **Fault Masking**: Prevent faults from causing errors (passive)
2. **Reconfiguration**: Detect, locate, contain, and recover from faults (active)
3. **Hybrid Approaches**: Combine both for optimal fault tolerance

### Redundancy Types

- **Hardware**: Extra components (TMR, standby systems)
- **Software**: N-version programming, recovery blocks
- **Information**: Error detection/correction codes
- **Time**: Retry with re-execution

### Common Techniques

- **Passive**: TMR, NMR, duplication with comparison
- **Active**: Hot/cold standby, pair-and-a-spare, watchdog timers
- **Hybrid**: NMR with spares, self-purging redundancy

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

