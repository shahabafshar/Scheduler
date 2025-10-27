# Scheduling Tasks with Precedence Relations

## Overview

When tasks have precedence constraints (dependencies), we need to modify task parameters before applying standard scheduling algorithms like RMS, DMS, or EDF.

### Goal
Modify task parameters (ready times, deadlines) in order to respect precedence constraints so that standard schedulers can be used.

---

## Modifying Task Parameters for RMS

### Rule for Ready Time

For a precedence relationship: **T_i → T_j** (T_i precedes T_j)

**R_j* ≥ Max(R_j, R_i*)**

Where R_i* is the modified ready time of task T_i

### Priority Requirement

**Priority(T_i) > Priority(T_j)** (strictly greater)

### Procedure

1. Process tasks in **topological order** (respecting precedence graph)
2. For each task, modify its ready time based on all its predecessors
3. Assign priorities to ensure precedence relationships are respected

---

## RMS: Modifying Ready Times - Example

### Initial Task Parameters

**Precedence Graph:**
```
T1 → T2, T3
T3, T4 → T5
```

**Initial Parameters:**

| Task | R_i | C_i | D_i |
|---------|-----|-----|-----|
| T1 | 0 | 1 | 5 |
| T2 | 5 | 2 | 7 |
| T3 | 0 | 2 | 5 |
| T4 | 0 | 1 | 10 |
| T5 | 0 | 3 | 12 |

### Modification Steps

**Step 1: T1 (no predecessors)**
- R₁* = R₁ = 0

**Step 2: T2 (predecessor: T1)**
- R₂* = Max(R₂, R₁*) = Max(5, 0) = 5

**Step 3: T3 (predecessor: T1)**
- R₃* = Max(R₃, R₁*) = Max(0, 0) = 0

**Step 4: T4 (no predecessors)**
- R₄* = R₄ = 0

**Step 5: T5 (predecessors: T3狠, T4)**
- R₅* = Max(R₅, R₃*, R₄*) = Max(0, 0, 0) = 0

### Modified Task Parameters

| Task | R_i* | C_i | D_i | Priority |
|------|------|-----|-----|----------|
| T1 | 0 | 1 | 5 | 3 |
| T2 | 5 | 2 | 7 | 4 |
| T3 | 0 | 2 | 5 | 2 |
| T4 | 5 | 1 | 10 | 1 |
| T5 | 5 | 3 | 12 | 0 |

### Priority Assignment

If all tasks in a connected component have the same period, they will have a **tie in priority** under RMS. We assign **additional priorities** to break the ties while respecting precedence.

---

## Modifying Task Parameters for DMS

### Rules

For precedence relationship: **T_i → T_j**

**Ready Time:**
- **R_j* ≥ Max(R_j, R_i*)**

**Deadline:**
- **D_j* ≥ Max(D_j, D_i*)**

**Priority:**
- **Priority(T_i) > Priority(T_j)** (strictly greater)

### Procedure

1. Modify ready times (same as RMS)
2. Modify deadlines in reverse topological order
3. Assign priorities based on modified deadlines

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

