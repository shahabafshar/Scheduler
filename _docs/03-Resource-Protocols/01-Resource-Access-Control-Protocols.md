# Resource Access Control Protocols

## Assumptions

- Periodic tasks
- Tasks can have resource access (critical sections)
- Semaphore is used for mutual exclusion
- RMS scheduling used

---

## Background: Task State Diagram

### Task States

- **Ready State**: Waiting in ready queue
- **Running State**: CPU executing the task
- **Blocked**: Waiting in the semaphore queue until the shared resource is free

### Semaphore Types

- **Mutex** (binary semaphore)
- **Counting semaphore**

### State Transitions

```
READY → (scheduled) → RUN
RUN → (preemption) → READY
RUN → (wait on busy resource) → WAITING
WAITING → (signal on free resource) → READY
RUN → (termination) → Terminated
```

---

## Priority Inversion Problem

### Definition

Priority inversion is an **undesirable situation** in which a higher priority task gets blocked (waits for CPU) for more time than that it is supposed to, by lower priority tasks.

### Scenario

Consider three periodic tasks with decreasing order of priorities:
- T1: Highest priority
- T2: Medium priority
- T3: Lowest priority

T1 and T3 share a resource **S**.

### Problem Sequence

1. T3 obtains a lock on semaphore S and enters its critical section
2. T1 becomes ready to run and preempts T3
3. T1 tries to enter its critical section by locking S, but S is already locked by T3
4. T1 gets blocked
5. T2 becomes ready to run
6. Since only T2 and T3 are ready to run, T2 preempts T3 while T3 is in its critical section

**Problem**: The highest priority task (T1) is blocked for longer than just the time for T3 to complete its critical section. The duration of blocking is **unpredictable** because T2 got executed in between.

### Total Blocking Time

In the worst case, T1's total blocking time = (K1 + K2 + K3) + (L1)

Where:
- K1, K2, K3 are the durations when T3 is waiting for higher priority tasks
- L1 is the direct blocking time in the critical section

---

## Priority Inheritance Protocol (PIP)

### How It Works

Priority inheritance protocol solves the problem of priority inversion.

**Key Mechanism:**
- If a higher priority task T_H is blocked by a lower priority task T_L (because T_L is currently executing a critical section needed by T_H), T_L **temporarily inherits the priority of T_H**
- When blocking ceases (i.e., T_L exits the critical section), T_L **resumes its original priority**

### Limitations

Unfortunately, priority inheritance **may lead to deadlock**.

### Example: Deadlock Scenario

Assume T2 > T1 (T2 has higher priority):

1. T1 locks CS1
2. T2 tries to lock CS2 and is blocked by T1 holding CS1
3. T1 inherits T2's priority
4. T1 tries to lock CS2 but cannot because T2 is waiting
5. **Deadlock occurs**

---

## Priority Ceiling Protocol (PCP)

### Overview

Priority ceiling protocol solves the priority inversion problem **without getting into deadlock**.

### How It Works

**Priority Ceiling Definition:**
- For each semaphore, a **priority ceiling** is defined
- The value is the **highest priority** of all the tasks that may lock it

**Entry Rule:**
- When a task Ti attempts to execute one of its critical sections, it will be **suspended** unless its priority is **higher than the priority ceiling** of all semaphores currently locked by tasks other than Ti

**Blocking:**
- If task Ti is unable to enter its critical section for this reason, the task that holds the lock on the semaphore with the highest priority ceiling is said to be blocking Ti
- That task **inherits the priority of Ti**

**Normal Operation:**
- As long as a task Ti is not attempting to enter one of its critical sections, it will preempt every task that has a lower priority

### Properties

1. This protocol is the same as priority inheritance protocol, **except** that a task Ti can also be blocked from entering a critical section if any other task is currently holding a semaphore whose priority ceiling is **greater than or equal to** the priority of task Ti

2. **Prevents mutual deadlock** among tasks

3. A task can be blocked by lower priority tasks **at most once**

### Example

For the deadlock scenario:

1. Priority ceiling for both CS1 and CS2 is the priority of T2
2. From time t0 to t2, operations are the same as before
3. At time t3, T2 attempts to lock CS1, but is blocked since CS2 (which has been locked by T1) has a priority ceiling equal to the priority of T2
4. T1 inherits the priority of T2 and proceeds to completion, thereby **preventing deadlock** situation

---

## Priority Ceiling Emulation

**How It Works:**
- Once a task locks a semaphore, its priority is **immediately raised** to the level of the priority ceiling of the semaphore

**Benefits:**
- Deadlock avoidance and block at-most-once result of priority ceiling protocol still holds

**Restriction:**
- A task **cannot suspend its execution** within the critical section

---

## Real-World Example: Mars Pathfinder

### The Problem

**Mission:** Mars Pathfinder (July 4, 1997)

**System:** VxWorks (real-time OS), preemptive priority scheduling of threads (e.g., RMS)

**Issue:** Priority inversion involving three threads:
- **T1**: Information bus task (highest priority)
- **T2**: Communication task (medium priority)
- **T3**: Meteorological data gathering task (lowest priority)

Priority order: T1 > T2 > T3

**Shared Resource:** Information bus (used mutex)

### What Happened

The same priority inversion situation as described in the example occurred:
1. T3 locked the information bus
2. T1 tried to access it and was blocked
3. T2 preempted T3, causing unpredictable blocking for T1

### Resolution

- Priority ceiling protocol was found to be **disabled initially**
- It was **enabled online** and the problem was corrected

This real-world example demonstrates the critical importance of proper resource access control protocols in safety-critical systems.

---

## Modeling Blocking Time and Earlier Deadline

### Blocking Time Modeling

- **Blocking time (Bi)** encountered by task Ti by lower priority tasks can be modeled by increasing Ti's utilization by **Bi/Pi**

### Earlier Deadline Modeling

- **Earlier deadline (Di < Pi)** can also be modeled as blocking time for **Ei = Pi - Di**
- Net increase in task Ti's utilization is **(Bi + Ei) / Pi**

### Schedulability Check (Utilization-Based)

For tasks in sorted order T1 > T2 > … > Tn (sufficient, but not necessary):

**∑(i=1 to j) (C_i/P_i) + (C_j + B_j + E_j)/P_j ≤ j(2^(1/j) - 1)** for j = 1 to n

### Completion Time Test (Exact Analysis)

**Earlier deadline case (di < pi):**
- Same as DMS exact analysis

**Blocking time case (Bi):**
- Let **C_i' = C_i + B_i**
- While calculating W_i(t) for task Ti, use **C_i'** for task Ti
- For all other higher priority tasks Tj, use **C_j**

**Note:** Blocking Time calculation is typically learned through homework and detailed notes are provided separately.

---

## Summary

| Protocol | Solves Priority Inversion | Prevents Deadlock | Max Blocking Times |
|----------|--------------------------|-------------------|-------------------|
| **No Protocol** | ❌ | ❌ | Unbounded |
| **Priority Inheritance** | ✅ | ❌ | Bounded but > 1 |
| **Priority Ceiling** | ✅ | ✅ | Once (at most) |
| **Priority Ceiling Emulation** | ✅ | ✅ | Once (at most) |

### Key Takeaways

1. Priority inversion can cause unpredictable blocking times in real-time systems
2. Priority Inheritance Protocol solves inversion but may cause deadlock
3. Priority Ceiling Protocol solves both inversion and deadlock
4. A task can be blocked by lower priority tasks at most once under PCP
5. Proper resource access control is critical in safety-critical systems (Mars Pathfinder example)

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

