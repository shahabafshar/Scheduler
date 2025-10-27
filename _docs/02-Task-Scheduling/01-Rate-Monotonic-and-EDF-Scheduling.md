# Rate Monotonic and EDF Scheduling

## Priority-Driven Preemptive Scheduling

### Assumptions
- Periodic tasks (known a priori)
- Deadline equals period (Di = Pi)
- No resource constraints
- Tasks are preemptable
- Independent tasks (no precedence constraints)

### Laxity Definition
The **laxity** of a task Ti is defined as:
**L_i = d_i - (t + c_i')**
where:
- **d_i**: deadline
- **t**: current time
- **c_i'**: remaining computation time

---

## Rate Monotonic Scheduling (RMS)

### Priority Assignment
- **Smaller period = Higher priority**
- Task with the smallest period is assigned the highest priority
- At any time, the highest priority task is executed

### Schedulability Test (Utilization-Based)

A set of **n** tasks is schedulable on a uniprocessor by the RMS algorithm if the processor utilization:

**∑(i=1 to n) (C_i / P_i) ≤ n(2^(1/n) - 1)**

**Properties:**
- This condition is **sufficient but not necessary**
- The term **n(2^(1/n) - 1)** approaches **ln 2 (≈ 0.69)** as n → ∞
- For n = 1: bound = 1.0
- For n = 2: bound = 0.828
- For n = 3: bound = 0.78
- For n = ∞: bound = 0.693

**Optimality:**
- RMS is an **optimal preemptive scheduling algorithm with fixed priorities**
- Static/fixed priority algorithm assigns the same priority to all jobs (instances) in each task

### Example 1: RMS Schedulable

**Task set:** T1 = (2, 4) and T2 = (1, 8)

**Schedulability check:**
```
C1/P1 + C2/P2 = 2/4 + 1/8 = 0.5 + 0.125 = 0.625 ≤ 2(√2 - 1) = 0.82
```

**Result:** **Schedulable**

### Example 2: RMS Utilization Test Failed (but may still be schedulable)

**Task set:** T1 = (2, 4) and T2 = (4, 8)

**Schedulability check:**
```
C1/P1 + C2/P2 = 2/4 + 4/8 = 0.5 + 0.5 = 1.0 > 2(√2 - 1) = 0.82
```

**Result:** Fails utilization test, but may still be schedulable → Need exact analysis

---

## Earliest Deadline First (EDF)

### Priority Assignment
- **Smaller deadline = Higher priority**
- Task with the smallest deadline is assigned the highest priority
- At any time, the highest priority task is executed

### Schedulability Test

A set of **n** tasks is schedulable on a uniprocessor by the EDF algorithm if the processor utilization:

**∑(i=1 to n) (C_i / P_i) ≤ 1**

**Properties:**
- This condition is **both necessary and sufficient**
- EDF is an **optimal preemptive scheduling algorithm with dynamic priorities**
- Dynamic priority algorithm assigns **different priorities to individual jobs** (instances) in each task

### Least Laxity First (LLF)
- **LLF has the same schedulability check as EDF**
- Priority assignment: Smaller laxity = Higher priority

### EDF Example

**Task set:** T1 = (1, 3, 3) and T2 = (4, 6, 6)

**Schedulability check:**
```
C1/P1 + C2/P2 = 1/3 + 4/6 = 0.33 + 0.67 = 1.0 ≤ 1
```

**Result:** **Schedulable**

**Note:** Unlike RMS, only those task sets which pass the schedulability test are schedulable under EDF.

---

## RMS vs EDF/LLF

| Aspect | RMS | EDF/LLF |
|--------|-----|---------|
| **Priority Type** | Fixed/Static | Dynamic |
| **Priority Assignment** | Based on period (smaller = higher) | Based on deadline/laxity (smaller = higher) |
| **Optimality** | Optimal fixed-priority preemptive | Optimal dynamic-priority preemptive |
| **Schedulability Bound** | n(2^(1/n) - 1) ≈ 0.69 (for large n) | 1.0 (100% utilization) |
| **Implementation** | Easier to implement | More difficult to implement |
| **Complex Scenarios** | Rich theory exists | Limited theory |
| **Practical Use** | Widely used in practice | Less commonly used |

**Summary:**
- RMS offers **lower schedulability** (≈69% utilization) but is **easier to implement and analyze**
- EDF/LLF offers **higher schedulability** (100% utilization) but is **more difficult to implement**
- RMS schedulability properties can be analyzed for complex scenarios; rich theory exists and it is widely used in practice

---

## EDF Schedulability Test Revisited

### When di ≥ pi (Deadline equals or exceeds period)
- Test: **∑(C_i / P_i) ≤ 1**
- Sufficient but **NOT necessary**

### When di < pi (Deadline less than period)
- Test: **∑(C_i / d_i) ≤ 1**
- Necessary **and sufficient**

### Alternative Approach
- **Processor demand-based test** (not covered in detail here)

---

## Periodic Task Scheduling Summary

| Condition | Algorithm | Priority Type | Test |
|-----------|-----------|---------------|------|
| Di = Pi | RMS | Static/Fixed | Utilization test OR Exact Analysis |
| Di ≤ Pi | DMS | Static/Fixed | Utilization test OR Exact Analysis |
| Di ≥ Pi | EDF | Dynamic | Utilization test (sufficient) |
| Di < Pi | EDF | Dynamic | Processor demand test (necessary & sufficient) |

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

