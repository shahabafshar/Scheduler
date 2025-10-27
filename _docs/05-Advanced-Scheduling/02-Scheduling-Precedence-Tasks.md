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

### DMS Deadline Modification Example

**Initial:** D₁ = 5, D₂ = 7, D₃ = 5, D₄ = 10, D₅ = 12

**Modification Steps (backward):**
- D₅' = D₅ = 12 (no successors)
- D₄' = Max(D₄, D₅') = Max(10, 12) = 12
- D₃' = Max(D₃, D₅') = Max(5, 12) = 12
- D₂' = D₂ = 7 (no successors)
- D₁' = Min(Min(D₂'-C₂, D₃'-C₃), D₁) = Min(Min(7-2, 12-2), 5) = Min(5, 5) = 5

---

## Modifying Task Parameters for EDF

### Rules

For precedence relationship: **T_i → T_j**

**Ready Time:**
- **R_j* ≥ Max(R_j, (R_i* + C_i))**

**Deadline:**
- **D_i* ≤ Min(D_i, (D_j* - C_j))**

### Key Differences from RMS/DMS

1. **Ready time modification** accounts for predecessor's **completion**: R_i* + C_i
2. **Deadline modification** is done in reverse order: backward pass
3. No explicit priority assignment needed (EDF uses dynamic priorities based on deadlines)

---

## EDF: Modifying Ready Times - Example

**Initial:** R₁ = 0, R₂ = 5, R₃ = 0, R₄ = 0, R₅ = 0

### Ready Time Modification (Forward Pass)

**Step 1: T1**
- R₁* = 0

**Step 2: T2 (predecessor: T1)**
- R₂* = Max(R₂, R₁* + C₁) = Max(5, 0 + 1) = 5

**Step 3: T3 (predecessor: T1)**
- R₃* = Max(R₃, R₁* + C₁) = Max(0, 0 + 1) = 1

**Step 4: T4 (predecessor: T2)**
- R₄* = Max(R₄, R₂* + C₂) = Max(0, 5 + 2) = 7

**Step 5: T5 (predecessors: T3, T4)**
- R₅* = Max(R₅, Max(R₃* + C₃, R₄* + C₄))
- R₅* = Max(0, Max(1 + 2, 7 + 1)) = Max(0, 8) = 8

### Modified Ready Times
- R₁* = 0, R₂* = 5, R₃* = 1, R₄* = 7, R₅* = 8

---

## EDF: Modifying Deadlines - Example

**Initial:** D₁ = 5, D₂ = 7, D₃ = 5, D₄ = 10, D₅ = 12

### Deadline Modification (Backward Pass)

**Step 1: T5**
- D₅* = 12 (no change, no successors)

**Step 2: T4 (predecessor of T5)**
- D₄' = Min(D₄, D₅* - C₅) = Min(10, 12 - 3) = 9

**Step 3: T3 (predecessor of T5)**
- D₃' = Min(D₃, D₅* - C₅) = Min(5, 12 - 3) = 5

**Step 4: T2 (predecessor of T4)**
- D₂' = Min(D₂, D₄' - C₄) = Min(7, 9 - 1) = 7

**Step 5: T1 (predecessor of T2, T3)**
- D₁' = Min(D₁, Min(D₂' - C₂, D₃' - C₃))
- D₁' = Min(5, Min(7 - 2, 5 - 2)) = Min(5, 3) = 3

### Modified Deadlines
- D₁* = 3, D₂* = 7, D₃* = 5, D₄* = 9, D₅* = 12

---

## Comparison of Approaches

| Aspect | MMS | DMS | EDF |
|--------|-----|-----|-----|
| **Ready Time** | R_j* ≥ Max(R_j, R_i*) | R_j* ≥ Max(R_j, R_i*) | R_j* ≥ Max(R_j, R_i* + C_i) |
| **Deadline** | Not modified | D_j* ≥ Max(D_j, D_i*) | D_i* ≤ Min(D_i, D_j* - C_j) |
| **Priority** | Static (by period) | Static (by deadline) | Dynamic (by deadline) |
| **Processing** | Forward pass only | Forward + Backward | Forward + Backward |

---

## Key Insights

1. **RMS/DMS**: Both require forward pass for ready times; DMS also needs backward pass for deadlines
2. **EDF**: Uses both forward (ready times) and backward (deadlines) passes with execution times accounted for
3. **Precedence Preservation**: All approaches ensure predecessor tasks complete before successors can start
4. **Optimality**: Modifications preserve schedulability if original task set was schedulable

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

