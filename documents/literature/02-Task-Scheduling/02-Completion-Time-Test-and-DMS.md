# Completion Time Test and Deadline Monotonic Scheduling

## Exact Analysis (Necessary & Sufficient)

### Critical Zone Theorem

For a set of independent periodic tasks, if a task Ti meets its first deadline di ≤ pi when all other higher priority tasks are started (i.e., ready) at the same time, then it meets all its future deadlines with any other task start times.

This theorem provides the basis for exact schedulability analysis beyond the utilization-based test.

---

## Completion Time Test

### Workload Function

Let there be n tasks ordered in decreasing priority. Consider any task Ti. The workload over [0,t] (for arbitrary t > 0) due to all tasks of equal or higher priority than Ti is given by:

**W_i(t) = ∑(j=1 to i) [⌈t/P_j⌉ × C_j]**

The term **⌈t/P_j⌉** represents the number of times task T_j arrives in time t, and therefore represents its computational demand in time t.

### Completion Time Test Procedure

1. Suppose that task Ti completes its execution exactly at time t
2. This means that the total cumulative demand from the i tasks up to time t, W_i(t), is exactly equal to t, that is, **W_i(t) = t**
3. A method for finding the completion time of task Ti, that is, the time at which W_i(t) = t, is known as **completion time test**

### Schedulability Condition

A task Ti is schedulable if **W_i ≤ d_i**, where W_i(t) = t.

An entire task set is schedulable if this condition holds for all tasks in the set.

### Iterative Computation

The completion time test is computed iteratively:

```
t_0 = ∑(j=1 to i) C_j  (initial estimate)
t_k+1 = W_i(t_k)        (refine estimate)
Continue until t_k+1 = t_k (convergence)
```

### Completion Time Test — Example

**Task set:**
- Task T1: c₁ = 20; p₁ = 100; d₁ = 100
- Task T2: c₂ = 30; p₂ = 145; d₂ = 145
- Task T3: c₃ = 68; p₃ = 150; d₃ = 150

This task set **fails** the utilization-based schedulability test for RMS.

**Perform completion time test for T3:**

**Step 1:** Initial estimate
```
t₀ = c₁ + c₂ + c₃ = 20 + 30 + 68 = 118
```

**Step 2:** First iteration
```
t₁ = W₃(t₀) = 2×c₁ + c₂ + c₃ = 2×20 + 30 + 68 = 40 + 30 + 68 = 138
```
(Number of T1 arrivals in time 138 = ⌈138/100⌉ = 2)

**Step 3:** Check convergence
```
W₃(t₁) = 2×20 + 30 + 68 = 138 = t₁  ✓
```

**Result:** Task T3 is schedulable (W₃ = 138 ≤ d₃ = 150)

Since T3 (lowest priority) is schedulable, Tasks T1 and T2 are also schedulable.

---

## Deadline Monotonic Scheduling (DMS)

### Task Model
- Task Ti: (ci, pi, di)
- Relative deadline di ≤ pi
- **Note:** "di" in DMS is a **fixed parameter** (static priority), whereas the "absolute deadline" used in EDF is a **dynamic parameter**

### Priority Assignment
- **Smaller deadline = Higher priority**
- Assigns priority based on di; smaller the di, higher the priority

### Schedulability Test

**Utilization-based (sufficient but not necessary):**
**∑(i=1 to n) (C_i / d_i) ≤ n(2^(1/n) - 1)**

- Similar to RMS, except **C_i/d_i** is used instead of **C_i/p_i**
- Uses deadline instead of period in the calculation

### Exact Analysis
- Similar to RMS exact analysis
- Exception: the ordering of tasks is based on **di** instead of **pi**

### Example

**Task set:** (ci, pi, di)
- T1: (3, 20, 7)
- T2: (2, 5, 4)
- T3: (2, 10, 9)

**Priority order (by deadline):** T2 > T3 > T1

**Utilization check:**
```
C₁/d₁ + C₂/d₂ + C₃/d₃ = 3/7 + 2/4 + 2/9 = 0.43 + 0.5 + 0.22 = 1.15
```

**Sum(C_i/d_i) = 1.15 > 1**, but this task set **is schedulable** under DMS.

This demonstrates that the utilization test is not necessary - the task set can still be schedulable even when utilization exceeds the bound.

### Optimality
- DMS is an **optimal fixed-priority scheduling algorithm**
- It is a **generalization of RMS** (when di = pi for all tasks, DMS reduces to RMS)

---

## RMS/DMS Schedulability Test Flow

For a given task set:

```
1. Is the task set Harmonic?
   - NO → Go to step 2
   - YES → Check if ∑U_i ≤ 1
     - YES → Schedulable ✓
     - NO → NOT Schedulable ✗

2. Utilization-based test: Check ∑U_i ≤ n(2^(1/n) - 1)
   - YES → Schedulable ✓
   - NO → Go to step 3

3. Exact Analysis (Completion Time Test)
   - For RMS: Use ordering by period
   - For DMS: Use ordering by deadline
   - Compute W_i(t) for each task
   - Check if W_i ≤ d_i for all tasks
     - YES → Schedulable ✓
     - NO → NOT Schedulable ✗
```

### Harmonic Task Sets

A task set is **harmonic** if for every pair of periods (P_i, P_j) with P_i < P_j, P_j is an integer multiple of P_i.

Example: Task periods {4, 8, 16, 32} form a harmonic set.

For harmonic task sets, the schedulability bound increases to 100% utilization (∑U_i ≤ 1).

---

## Summary

### RMS/DMS Comparison

| Aspect | RMS | DMS |
|--------|-----|-----|
| **Task Model** | (ci, pi) | (ci, pi, di) |
| **Deadline** | di = pi | di ≤ pi |
| **Priority Assignment** | By period (smaller = higher) | By deadline (smaller = higher) |
| **Utilization Test** | ∑(C_i/P_i) ≤ n(2^(1/n) - 1) | ∑(C_i/d_i) ≤ n(2^(1/n) - 1) |
| **Exact Analysis** | Order by period | Order by deadline |

### When to Use

- **Use RMS** when deadlines equal periods (di = pi)
- **Use DMS** when deadlines are less than or equal to periods (di ≤ pi)
- **Use Completion Time Test** when utilization test fails but you want to verify schedulability

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

