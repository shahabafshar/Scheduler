# Combined Scheduling of Periodic and Aperiodic Tasks

## Assumptions & Issues

### Assumptions
- **RMS scheduling algorithm** used
- All periodic tasks start at time t=0
- Periodic tasks relative deadlines are equal to end of period
- Arrival times of aperiodic tasks unknown

### Issues
- **Schedulability of periodic tasks**
- **Response time for aperiodic tasks**
- **Implementation considerations**

---

## Background Scheduling Algorithm

### Concept
- **No server is created**
- Aperiodic tasks are executed when there is **no periodic task** to execute
- Simple, but **no guarantee** on aperiodic schedulability

### Architecture
```
Periodic tasks (RMS) → High priority Queue → CPU
Aperiodic tasks (FIFO/EDF) → Low priority Queue → CPU
```

### Key Idea
During "holes" (idle time) in the periodic schedule, aperiodic tasks can be serviced.

---

## Combined Scheduling

### Server-Based Approach
Creating a **periodic server** **T_s = (C_s, P_s)** for processing aperiodic workload.

### How It Works
1. Create one or more server tasks
2. Aperiodic tasks are scheduled in the periodic server's time slots
3. Server policy could be based on deadline, arrival time, or computation time

### Server Algorithms
All algorithms behave the same manner when there are enough aperiodic tasks to execute:

1. **Polling Server** (bandwidth non-preserving)
2. **Deferrable Server** (bandwidth preserving)
3. **Priority Exchange Server** (bandwidth preserving)
4. **Sporadic Server** (bandwidth preserving)

---

## Polling Server

### How It Works
- A **periodic server task** is created
- If there are no aperiodic tasks at an invocation of the server (as per RMS), the server **suspends itself** during its current period and gets invoked again at its next period
- If there are enough aperiodic tasks in an invocation, it serves up to **C_s** capacity
- The computation time allowance for the server is **replenished at the start of its period**
- Include T_s in the task set and do schedulability test

### Characteristics
- **Bandwidth non-preserving**: Unused server capacity is lost
- **Poor response time** for aperiodic tasks

### Example
**Task set:** T1 = (1,4), T2 = (2,6) and T_s = (2,5)

**Behavior:**
- Server becomes available periodically
- If aperiodic task arrives when server is not active, it must wait
- Server can only check for aperiodic tasks at its periodic invocation times

---

## Polling Server: Schedulability Analysis

### Periodic Task Schedulability
Schedulability of periodic tasks can be evaluated by introducing a periodic task equivalent to the server:

**∑(i=1 to n) (C_i / P_i) + (C_s / P_s) ≤ (n+1)(2^(1/(n+1)) - 1)**

### Aperiodic Task Guarantees

**Case 1: Simple Case**
- Consider a single aperiodic task A_i arrived at r_a, with computation time C_a and deadline D_a
- Since an aperiodic task can wait at most for **one period** before receiving service
- If **C_a ≤ C_s**, the request is certainly completed within **two server periods**
- Guaranteed if: **2通讯s ≤ D_a**

**Case 2: Arbitrary Computation Times**
- For arbitrary computation times, the aperiodic task is certainly completed in **⌈C_a/C_s⌉** server periods
- Guaranteed if: **P_s + ⌈C_a/C_s⌉ × P_s ≤ D_a**

---

## Deferrable Server

### How It Works
- A periodic server task is created
- When the server is invoked with **no outstanding aperiodic tasks**, the server does **not execute** but **defers its assigned time slot**
- When an aperiodic task arrives, the server is invoked (as per RMS) to execute aperiodic tasks and maintains its priority
- The computation time allowance for the server is **replenished at the start of its period**

### Characteristics
- **Bandwidth preserving**: Unused capacity is saved
- Provides **better response time** for aperiodic tasks than Polling server
- Under overload, deadlines are missed **predictably**
- Similar schedulability test like polling server

### Key Advantage
Server capacity is **immediately available** when aperiodic tasks arrive, rather than waiting for the next server invocation.

---

## Priority Exchange Server

### How It Works
- A periodic server task is created
- When the server invoked, the server runs if there are any outstanding aperiodic tasks
- **If no aperiodic task exists**, the high priority server **exchanges its priority** with a lower priority periodic task for a duration of **C_s'**, where C_s' is the remaining computation time of the server
- In this way, the priority of the server decreases, but its **computation time is maintained**
- The computation time allowance for the server is replenished at the start of its period

### Characteristics
- **Bandwidth preserving**: Server capacity is maintained through priority exchange
- As a consequence, the aperiodic tasks get **low preference** for execution
- Offers **worse response time** compared to Deferrable Server
- **Better schedulability bound** for periodic task set compared to Deferrable Server

### Priority Exchange Mechanism
- Server executes at high priority when serving aperiodic tasks
- Server executes at low priority (exchanged) when no aperiodic tasks exist
- Maintains bandwidth but reduces megatonness for aperiodic tasks

---

## Sporadic Server

### Key Innovation
This algorithm allows to **enhance the average response time** for aperiodic tasks **without degrading** the utilization bound for periodic task set.

### How It Works
- Achieved by **varying the points at which the computation time of the server is replenished**, rather than merely at the start of each server period
- Any **spare capacity** (i.e., not being used by periodic tasks) is available for an aperiodic task on its arrival
- Server defers its capacity but replenishes at **current_time + period** when consumed

### Characteristics
- **Bandwidth preserving**
- **Best response time** among the four server algorithms
- Maintains the same utilization bound as RMS without servers

### Example
**Task set:** T1 = (3,10), T2 = (4,15) and T_s = (2,8)

**Behavior:**
- Server has the highest priority
- When no aperiodic task, server defers capacity
- When aperiodic task arrives, server has capacity immediately available
- Replenishment occurs at **current_time + P_s** after consumption

---

## Server Comparison Summary

| Server | Bandwidth Preserving | Response Time | Periodicity | Complexity |
|--------|---------------------|---------------|-------------|-----------|
| **Polling** | ❌ No | Poor | Periodic invocation only | Low |
| **Deferrable** | ✅ Yes | Better | Immediate availability | Medium |
| **Priority Exchange** | ✅ Yes | Worse | Low-priority when idle |`High |
| **Sporadic** | ✅ Yes | Best | Immediate with dynamic replenishment | Highest |

### Key Insights
1. **Polling Server**: Simplest but worst response time
2. **Deferrable Server**: Good balance of simplicity and performance
3. **Priority Exchange**: Best for periodic task schedulability, worse for aperiodic response
4. **Sporadic Server**: Best aperiodic response time, maintains RMS bounds

---

## Summary

### All Four Algorithms
- Behave **identically** when there are enough aperiodic tasks to execute
- Differ in how they handle **idle periods** when no aperiodic tasks exist
- Require including server in the periodic task set for schedulability analysis

### Bandwidth Preservation
- **Non-preserving**: Polling (capacity lost if unused)
- **Preserving**: Deferrable, Priority Exchange, Sporadic (capacity maintained)

### Response Time Ranking
**Best to Worst:**
1. Sporadic Server
2. Deferrable Server
3. Priority Exchange Server
4. Polling Server

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

