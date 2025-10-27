# Dependability Concepts

## Dependable System

A system is **dependable** when it is trustworthy enough that reliance can be placed on the service that it delivers.

### For a system to be dependable, it must be:

- **Available** - e.g., ready for use when we need it.
- **Reliable** - e.g., able to provide continuity of service while we are using it.
- **Safe** - e.g., does not have a catastrophic consequence on the environment.
- **Secure** - e.g., able to preserve confidentiality.

---

## Why Dependability?

With a greater reliance on computers in a variety of safety-critical applications, the consequences of failure and down time have become more severe.

### Safety-Critical Applications

- **Flight control** systems
- **Medical life support** systems
- **Process control** systems
- **공munication switching** systems
- **On-line transaction processing** systems

**Failure of computing resources can cost lives and/or money.**

---

## Examples of Dependable Systems

### Reliability Goals

- **Commercial aircraft** computer systems: **less than 10⁻⁹ failures per hour**
- **Modern telephone switching** systems: down time of **at most one hour in 40 years**
- **Medical life support** systems
- **Command and control** systems
- **Process control** applications

---

## Attributes of Dependability

### Categories

**FAULTS** → **IMPAIRMENTS** → **ERRORS** → **FAILURES**

**MEANS TO ACHIEVE DEPENDABILITY:**
- **Fault Avoidance** (Procurement)
- **Fault Tolerance** (Procurement)
- **Fault Removal** (Validation)
- **Fault Forecasting** (Validation)

**MEASURES:**
- **Quantitative**: Reliability, Availability
- **Qualitative**: Fail-Safe, Fail-Operational, No Single Point of Failure, Consistency

---

## Approaches to Achieving Dependability

### 1. Fault Avoidance
How to **prevent**, by construction, asymmet faults occurrence or introduction.

**Techniques:**
- Design methodologies
- Verification and validation methodologies
- Modeling
- Code inspections and walk-throughs

**Principle:** A fault avoided is one that does not have to be dealt with at a later time.

### 2. Fault Removal
How to **minimize**, by verification, the presence of faults.

**Techniques:**
- Unit testing
- Integration testing

**Note:** It is generally **much more expensive to remove a fault than to avoid a fault**.

### 3. Fault Tolerance
How to **provide**, by redundancy, a service complying with the specification **in spite of faults**.

**Capabilities Required:**
- Detect
- Diagnose
- Confine
- Mask
- Compensate
- Recover from faults

**Definition:** Fault-tolerance is informally defined as the **ability of a system to deliver the expected service even in the presence of faults**.

### 4. Fault Forecasting
How to **estimate**, by evaluation, the presence, the creation, and the consequence of faults.

**Application:** Observing system behavior to take action to compensate for faults **before they occur**.

**Example:** When a system deviates from normal behavior, reconfigure to reduce stress on a component with high failure potential.

---

## Dependability Categories

### Procurement (How to Provide)

- **Fault avoidance** and **Fault tolerance** constitute dependability **procurement**

**Purpose:** How to provide the system with the ability to deliver the specified service

### Validation (How to Reach Confidence)

- **Fault removal** and **Fault forecasting** constitute dependability **validation**

**Purpose:** How to reach confidence in the system's ability to deliver the specified service

---

## Fault, Error, and Failure

### Definitions

**Fault:** A deviation in a hardware or software component from its intended function

**Error:** A manifestation of a fault in a system, in which the logical state of an element differs from its intended value

**Failure:** A transition from proper to improper service

### Latency Concepts

**Fault Latency:** The time between fault occurrence and the first appearance of an error

**Error Latency:** The time between occurrence of an error and its detection

### Recovery Process

When fault-tolerance mechanisms **detect** an error, they may initiate several actions:
- Handle the fault
- Contain its errors

**Recovery occurs** if these actions are successful; otherwise, the system eventually **malfunctions and a failure occurs**.

---

## Example of Fault, Error, and Failure

**Fault:** s-a-0 (stuck-at-0) fault occurs in a bit with value 0

**Error:** Reads s-a-0 value 1 instead of the correct value 1

**Recovery or Failure:** Proper service continues or is disrupted

```
Fault → (fault latency) → Error → (error latency) → Detection of Error → (latency of fault tolerance mechanism) → Recovery or Failure
```

---

## Fault Characteristics

### Occurrence Throughout System Life

Faults can arise during **all stages** in a computer system's evolution:
- Specification
- Design
- Development
- Manufacturing
- Assembly
- Installation
- Throughout operational life

### Pre-Deployment vs. Field

- **Most faults** that occur before full system deployment are **discovered through testing** and eliminated
- **Faults not removed** can reduce a system's dependability when it is in the field

### Classification

A fault can be classified by:
- Duration
- Nature of output
- Correlation to other faults

---

## Fault Types - Based on Duration

### Permanent Faults

- Caused by **irreversible device failures** within a component
- Causes: damage, fatigue, or improper manufacturing
- **Restoration:** Replacement or repair

### Transient Faults

- Triggered by **environmental disturbances**
- Examples: voltage fluctuations, electromagnetic interference, radiation
- **Characteristic:** Short duration, returning affected circuitry to normal operating state
- **No lasting damage**

### Intermittent Faults

- **Oscillate** between periods of erroneous activity and dormancy
- Often attributed to **design errors** resulting in marginal or unstable hardware
- **Example:** Fault due to a loose wire

---

## Fault Types - Based on Nature of Output

### Malicious Faults (Byzantine Failure)

- Fault can cause a unit to **behave arbitrarily**
- **Examples:**
  - Sensor sending conflicting outputs to different processors
  - Output line that stays afloat rather than stuck-at to 0 or 1
- **Detecting malicious faults:** Much harder than non-malicious faults

### Non-Malicious Faults

- **Example:** Stuck-at faults
- Easier to detect than malicious faults

---

## Fail-Stop and Fail-Safe Units

### Fail-Stop Unit

A unit is said to be **fail-stop** if it responds to up to a certain maximum number of faults by **simply stopping** rather than producing incorrect output.

**Typical Implementation:**
- Many processors running the same tasks
- Comparing the outputs
- If outputs don't agree, **whole unit turns itself off**

### Fail-Safe System

A system is said to be **fail-safe** if one or more safe states can be identified that can be accessed in case of a system failure to avoid catastrophe.

**Example:** Railway signaling systems

---

## Fault Types - Based on Correlation

### Independent Faults

- **Fault does not directly or indirectly cause another fault**
- Components fail independently

### Correlated Faults

- Faults are **related**
- Can be correlated due to:
  - **Physical coupling** of components
  - **Electrical coupling** of components

**Types:**
- **Common-mode** faults: Failures affecting multiple components simultaneously
- **Similar errors/failures**: Related failure patterns

---

## Load and Fault Hypothesis

### Assumptions

Any system has a **finite processing power**. To guarantee by design that certain performance requirements can be met, we must postulate a set of assumptions about the behavior of the environment.

### Load Hypothesis

Defines the **peak load** that is assumed to be generated by the environment.

### Fault Hypothesis

Defines the **types and frequency** of faults that a system must be capable of handling.

### Critical Scenario

The worst scenario that a fault-tolerant system must be capable of handling is at **peak load with the maximum number of faults**.

---

## Graceful Degradation

### Definition

If a specified fault scenario develops, the system must still provide a specified level of service. If more faults are generated than what is specified in the fault hypothesis, the performance of the system must **degrade gracefully**.

### Characteristics

- System must **not suddenly collapse** as the size of the faults increases
- Should **continue to execute part of the workload**
- Maintain core functionality while losing non-critical features

### Assumption Coverage

The concept of **assumption coverage** defines the probability that the load and fault hypotheses - and all other assumptions made about the behavior of the environment - are in agreement with the reality.

---

## Dependability Measures - Quantitative

### Service States

A life of a system is perceived by its users as an alternation between two states of the delivered service:
- **Proper service**
- **Improper service**

A failure is thus a **transition from proper to improper service**.

### Measures

Quantifying the alternation of proper-improper service leads to the two main measures of dependability: **reliability** and **availability**.

---

## Reliability

### Definition

Reliability is a measure of **continuous delivery of proper service** - or, equivalently, of the **time to failure**.

**Characteristics:**
- Measures how long a system operates without failure
- Important for applications requiring uninterrupted service
- Expressed as probability or Mean Time Between Failures (MTBF)

---

## Availability

### Definition

Availability is a measure of the **delivery of correct service with respect to the alternation of proper and improper service**.

**Characteristics:**
- Measures the percentage of time system is operational
- Includes time for repair/maintenance
- Formula: **Availability = (Total Time - Down Time) / Total Time**

**Example:** System with 99.9% availability is down approximately 8.76 hours per year.

---

## Dependability Measures - Qualitative

### No Single Point of Failure

Design the system so that the **failure of any single component will not cause the system to fail**.

**Implementation:**
- Redundancy in critical components
- Distributed architectures
- Backup systems

### Consistency

Design the system so that **all information delivered by the system is equivalent** to the information that would be delivered by an instance of a non-faulty system.

**Principles:**
- Data integrity
- Transaction consistency
- Agreement protocols

---

## Summary

### Key Concepts

1. **Dependability** = Availability + Reliability + Safety + Security
2. **Four Means**: Fault Avoidance, Fault Tolerance, Fault Removal, Fault Forecasting
3. **Fault Chain**: Faults → Errors → Failures
4. **Redundancy**: Key to fault tolerance (hardware, software, information, time)
5. **Graceful Degradation**: Degrade performance rather than fail completely

### Applications

- Safety-critical systems (aviation, medical, industrial control)
- High-availability systems (telecommunication, banking)
- Mission-critical applications (space exploration, defense systems)

**Sources:** 
- CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)
- CprE 545: Dependable Computing (Iowa State University)

