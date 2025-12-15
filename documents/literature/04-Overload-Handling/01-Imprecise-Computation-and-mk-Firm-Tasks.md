# Imprecise Computation and (m,k)-Firm Tasks

## How Overloads Occur

### Sources of Overload

1. **Dynamic workload beyond anticipated**
   - Aperiodic tasks
   - Dynamically arriving periodic tasks

2. **Unanticipated faults**
   - Frequency and duration of the faults

---

## Imprecise Computational Model

### Overview

A way to avoid timing faults during transient overloads and a way to introduce fault-tolerance by **graceful degradation** is the use of **Imprecise Computation (IC)** technique.

### Key Concept

The IC model provides scheduling flexibility by **trading off result quality to meet task deadlines**.

### Task Structure

A task is divided into two parts:
- **Mandatory part**: Must be completed before the task's deadline for an acceptable quality of result
- **Optional part**: Can be skipped to conserve system resources; refines the result

### Results

- **Precise result**: Task has executed its mandatory as well as optional parts before its deadline
- **Imprecise result** (i.e., approximate): Task executes the mandatory part alone

---

## Types of Imprecise Tasks

### Monotone Tasks

- A task is **monotone** if the quality of its intermediate result does **not decrease** as it executes longer
- Results improve over time

### 0/1 Constraint Tasks

- An imprecise task with **0/1 constraint** requires the optional part to be either **fully executed** or **not at all**
- No partial execution of optional part

---

## Applications of Imprecise Computations

### General Principle

Applications where one may prefer **timely imprecise results to late precise results**.

### Examples

1. **Image processing**
   - Better to have frames of fuzzy images in time than perfect images late

2. **Radar tracking**
   - Better to have estimates of target locations in time than accurate location data too late

3. **Tracking and control systems**
   - A transient fault may cause tracking computation to terminate prematurely and produce an approximate result
   - No recovery action is needed if the result still allows the system to maintain a track of its targets
   - As long as the approximate result is sufficiently accurate for the controlled system to remain stable, the fault can be tolerated

---

## Error Function & Objective Functions

### Task Model

**Monotone task, Ti**: (mi, oi, di)
- **mi**: Mandatory computation time
- **oi**: Optional computation time
- **di**: Deadline

### Error Function

**Error ei = F(oi, ki) = oi - ki**

Where:
- **ei**: Error incurred by task Ti
- **ki**: Optional portion completed

### Objective Functions

1. **Minimize the total error**
2. **Minimize the number of optional tasks discarded**
   - Shortest processing time first strategy
3. **Minimize the number of tardy tasks**

---

## Algorithm F (Minimize Total Error)

**For monotone task, identical weights, optimal, O(n log n)**

### Steps

1. Treat all mandatory tasks as optional
2. Use **ED policy** (Earliest Deadline) to schedule all the tasks (St)
3. If a feasible schedule is found, precise schedule is obtained → **stop**
4. Else use **ED to schedule mandatory tasks** (Sm)
5. If feasible schedule is not found, infeasible schedule → **stop**
6. Else use Sm as a template, transform St into an optimal schedule that is feasible and minimizes the total error

---

## Scheduling with 0/1 Constraints

### Problem Complexity

The general problem of optimal scheduling of IC tasks with 0/1 constraints is **NP-complete**.

### Optimal Schedule Definition

A schedule in which the **number of discarded optional tasks is minimum**.

### Algorithms

**Special case: Optional tasks have equal computation time**

#### LDF Algorithm (Latest Deadline First)
- **Same ready time**
- **O(n log n)** complexity

#### DFS Algorithm (Density-based First)
- **Arbitrary ready time**
- **O(n²)** complexity

---

## Scheduling Periodic Tasks

### Error-Cumulative
- Tracking and control applications
- Errors accumulate over time

### Error-Non-Cumulative
- Image enhancement and speech processing applications
- Each result is independent

---

## (m,k)-Firm Real-Time Tasks

### Definition

A periodic task is said to have an **(m,k)-firm guarantee** if it is adequate to meet the deadlines of **m out of k consecutive instances** of the task, where **m ≤ k**.

### Task Model

**Periodic task**: (pi, ci, mi, ki)

Where:
- **ci**: Computation time
- **pi**: Period
- **mi**: Number of mandatory instances (out of k)
- **ki**: Window size (consecutive instances)

### Properties

- A **flexible method** for expressing timing requirements
- Allows **"graceful degradation"** during overloads
- Choose values for m and k such that desired **m/k ratio** is obtained

### Key Points

- **(1,1)-firm** → hard real-time task (all instances must meet deadline)
- Female applications: Radar tracking, Automobile control

### (m,k) vs. Imprecise Computation

| Aspect | (m,k)-Firm | Imprecise Computation |
|--------|-----------|----------------------|
| **Model** | Instance-level | Task-level |
| **What can drop** | Entire instances | Portions of instances |
| **Granularity** | Coarser | Finer |
| **Application** | Periodic tasks only | Both periodic and aperiodic |

---

## Adaptive QoS Management Problem

### Goal

1. **Admit** tasks to satisfy at least the (m,k) guarantee
2. **Maximize** the QoS of admitted tasks beyond the (m,k) property at run-time
3. **Without violating** (m,k) property of any of the admitted tasks

### Dynamic Failure

**Dynamic failure (Timing failure)** is said to occur when (m,k) property is violated for one or more tasks.

---

## MK-RMS Schedulability Check

### Utilization-Based Test

**MK Load = ∑(i=1 to n) (c_i × m_i) / (p_i × k_i)**

**Check:** MK Load ≤ n(2^(1/n) - 1)

- Sufficient, but **not necessary**

### Classification of Mandatory and Optional Instances

**Instances of task Ti activated at times api is mandatory if:**

**a = ⌊(a × m_i) / k_i⌋** where a = 0, 1, 2, ...

### Priority Assignment

- **Optional instance**: Assigned the **lowest priority**
- **Mandatory instances**: Assigned priority **as per RMS**

### State Diagram Model

State diagram model is used to keep track of temporal history of task execution:
- **M**: Meeting deadline
- **m**: Missing deadline

---

## References

1. J.W.S. Liu, K.J. Lin, W.K. Shih, A.C. Yu, J.Y.Chung, and W. Zhao, "Algorithms for scheduling imprecise computations," *IEEE Computer*, vol.24, no.5, pp.58-68, May 1991.

2. P. Ramanathan, "Graceful degradation in real-time control applications using (m,k)-firm guarantee," In Proc. of Fault-Tolerant Computing Symposium, pp.132-141, 1997.

---

## Summary

| Technique | Task Type | Granularity | Graceful Degradation |
|-----------|-----------|-------------|---------------------|
| **Imprecise Computation** | Periodic, Aperiodic | Portion of task | Yes (partial execution) |
| **(m,k)-Firm** | Periodic only | Entire instances | Yes (instance dropping) |
| **Best Effort** | All | Full task | No (task dropped) |

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

