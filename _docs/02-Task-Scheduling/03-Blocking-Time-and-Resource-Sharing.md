# Blocking Time and Resource Sharing

## Overview

When tasks share resources, they can experience **blocking** - delays caused by other tasks holding required resources. This document explains priority inversion, resource access control protocols, and how to calculate blocking time.

---

## Priority Inversion Problem

### Definition

Priority inversion is an undesirable situation in which a **higher priority task gets blocked** (waits for CPU) **for more time than it is supposed to**, by lower priority tasks.

### Example Scenario

- Let **T1, T2, and T3** be three periodic tasks with **decreasing order of priorities** (T1 > T2 > T3)
- Let **T1 and T3** share a resource "**S**"

### Timeline of Events

1. **T3** obtains a lock on the semaphore **S** and enters its critical section
2. **T1** becomes ready to run and preempts T3
3. **T1** tries to enter its critical section by locking **S**
4. But **S** is already locked by T3 → **T1 gets blocked**
5. **T2** becomes ready to run
6. Since only T2 and T3 are ready to run, **T2 preempts T3** while T3 is in its critical section

### The Problem

**Ideal behavior:** T1 should be blocked no longer than the time for T3 to complete its critical section

**Actual behavior:** The duration of blocking is **unpredictable** because task **T2 got executed in between**

### Total Blocking Time

**Total blocking time for task T1 = (K1 + K2 + K3) + L1**

Where:
- **K1, K2, K3**: Time spent executing higher priority task T2
- **L1**: Critical section duration of T3

---

## Resource Access Control -- Example

### Task Set extends Attributes

**Task Model with Resource Sharing:**

| Task | cᵢᵢ | pᵢ | cᵢˣ | cᵢʸ | cᵢᶻ |
|------|-----|----|-----|-----|-----|
| T1 | 2 | 8 | 2 | 0 | 0 |
| T2 | 4 | 12 | 0 | 4 | 0 |
| T3 | 2 | 6 | 1 | 1 | 0 |

Where:
- **cᵢˣ**: Task duration before entering the critical section
- **cᵢʸ**: Critical section duration
- **cᵢᶻ**: Task duration after the critical section
- **cᵢ = cᵢˣ + cᵢʸ + cᵢᶻ**

**Priority order (by RMS):** T3 > T1 > T2

**T2 and T3 have access to a shared resource R**

---

## Priority Inheritance Protocol (PIP)

### How It Works

Priority inheritance protocol solves the problem of priority inversion.

**Under this protocol:**
- If a higher priority task **T_H** is blocked by a lower priority task **T_L**, because **T_L** is currently executing critical section needed by **T_H**
- Then **T_L temporarily inherits the priority of T_H**
- When blocking ceases (i.e., **T_L** exits the critical section), **T_L** resumes its original priority

### Limitation

**Unfortunately, priority inheritance may lead to deadlock.**

---

## Priority Ceiling Protocol (PCP)

### How It Works

Priority ceiling protocol solves the priority inversion problem **without getting into deadlock**.

### Priority Ceiling Definition

For each semaphore, a **priority ceiling** is defined, whose value is the **highest priority of all the tasks that may lock it**.

### Protocol Rules

**Rule 1:**
- When a task **Ti** attempts to execute one of its critical sections, it will be **suspended unless** its priority is higher than the **priority ceiling of all semaphores currently locked by tasks other than Ti**.

**Rule 2:**
- If task **Ti** is unable to enter its critical section for this reason, the task that holds the lock on the semaphore with the highest priority ceiling is said to be **blocking Ti** and hence **inherits the priority of Ti**.

**Rule 3:**
- As long as a task **Ti** is not attempting to enter one of its critical sections, it will preempt every task that has a lower priority.

### Properties

- This protocol is the same as the priority inheritance protocol, **except** that a task **Ti** can also be blocked from entering a critical section if any other task is currently holding a semaphore whose priority ceiling is greater than or equal to the priority of task **Ti**.
- **Prevents mutual deadlock** among tasks
- A task can be blocked by lower priority tasks **at most once**

### Example

For a previous example, the priority ceiling for both **CS₁** and **CS₂** is the priority of **T₂**.

- From time **t₀** to **t₂**, the operations are the same as before
- At time **t₃**, **T₂** attempts to lock **CS₁**, but is blocked since **CS₂** (which has been locked by **T₁**) has a priority ceiling equal to the priority of **T₂**
- Thus **T₁** inherits the priority of **T₂** and proceeds to completion, thereby **preventing deadlock situation**

---

## Priority Ceiling Emulation

### How It Works

- **Once a task locks a semaphore**, its priority is **immediately raised to the level of the priority ceiling** of the semaphore
- **Deadlock avoidance** and block at-most-once result of priority ceiling protocol still holds
- **Restriction:** A task **cannot suspend its execution** within the critical section

---

## Real-World Example: Mars Pathfinder

### Mission

**Mars Pathfinder mission** (July 4, 1997)

### System

- **VxWorks** (real-time OS)
- **Preemptive priority scheduling** of threads (e.g., RMS)

### The Problem

**Priority inversion** involving three threads:
- Information bus task (**T₁**)
- Meteorological data gathering task (**T₃**)
- Communication task (**T₂**)

**Priority order:** T1 > T2 > T3

**Shared resource:** Information bus (used mutex)

### What Happened

Same situation as described in the previous example had occurred

### Findings

**Priority ceiling protocol was found to be disabled initially**, then it was **enabled online** and the problem was corrected

---

## Modeling Blocking Time and Earlier Deadline

### Blocking Time Modeling

Blocking time (**Bᵢ**) encountered by task **Ti** by lower priority tasks can be modeled by **increasing Ti's utilization by Bᵢ/Pᵢ**.

### Earlier Deadline Modeling

Earlier deadline (**Dᵢ < Pᵢ**) can also be modeled as blocking time for **Eᵢ = Pᵢ - Dᵢ**.

### Net Increase in Utilization

**Net increase in task Ti's utilization is: (Bᵢ + Eᵢ) / Pᵢ**

---

## Schedulability Check with Blocking Time

### Utilization Test (Sufficient, but not necessary)

For sorted order **T1 > T2 > ... > Tn**:

**∑(i=1 to n) [(Cᵢ + Bᵢ + Eᵢ) / Pᵢ] ≤ n(2^(1/n) - 1)**

Where:
- **Cᵢ**: Computation time
- **Bᵢ**: Blocking time
- **Eᵢ**: Earlier deadline extra time = Pᵢ - Dᵢ (if Dᵢ < Pᵢ)

### Completion Time Test (Exact Analysis)

**Earlier deadline (di < pi) case:**
- Same as DMS exact analysis

**Blocking time (Bᵢ) case:**
- Let **Cᵢ' = Cᵢ + Bᵢ**
- While calculating **Wᵢ(t)** for task **Ti**, use **Cᵢ'** for task **Ti** and for all other higher priority tasks **Tj** simply use **Cj**

---

## Summary

### Key Concepts

1. **Priority Inversion:** Higher priority task blocked by lower priority tasks unpredictably
2. **Priority Inheritance:** Lower priority task inherits priority when blocking higher priority task
3. **Priority Ceiling:** Assign ceiling priority to resources to prevent deadlock
4. **Blocking Time:** Can be modeled as increased utilization

### Protocols Comparison

| Aspect | No Protocol | PIP | PCP |
|--------|------------|-----|-----|
| **Priority Inversion** | Yes | Reduced | Eliminated |
| **Deadlock** | No | Possible | Prevented |
| **Max Blocking** | Unbounded | Once per resource | Once total |
| **Implementation** | Simple | Moderate | Complex |

### Modeling Approaches

- **Bᵢ**: Blocking time → Increases task utilization by **Bᵢ/Pᵢ**
- **Eᵢ**: Earlier deadline extra time → Increases task utilization by **Eᵢ/Pᵢ**
- **Combined:** (Bᵢ + Eᵢ) / Pᵢ added to utilization test

**Note:** Blocking Time calculation details will be learned through homework; reading notes will be provided.

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

