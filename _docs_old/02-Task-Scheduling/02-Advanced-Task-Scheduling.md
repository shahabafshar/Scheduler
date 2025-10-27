# Real-Time Task Scheduling - Part 2

## Overview
This document covers advanced topics in real-time task scheduling including response time analysis, blocking, and schedulability tests.

## Response Time Analysis

### Fixed-Point Iteration Method
Used to compute worst-case response time for tasks under static priority scheduling.

#### Algorithm
For each task τᵢ in priority order:

```
Rᵢ⁽⁰⁾ = Cᵢ  // Initial guess
Rᵢ⁽ᵏ⁺¹⁾ = Cᵢ + Σⱼ∈hp(i) (⌈Rᵢ⁽ᵏ⁾/Tⱼ⌉ × Cⱼ)
```

Where `hp(i)` is the set of higher priority tasks.

#### Convergence Conditions
- **Convergence**: Rᵢ⁽ᵏ⁺¹⁾ = Rᵢ⁽ᵏ⁾
- **Feasibility**: Rᵢ ≤ Dᵢ
- **Non-convergence**: If Rᵢ⁽ᵏ⁺¹⁾ > Dᵢ for any k, task is not schedulable

### Practical Considerations

#### Workload Analysis
```
Rᵢ = Cᵢ + Σⱼ∈hp(i) (⌈Rᵢ/Tⱼ⌉ × Cⱼ)
```

- First term: Own execution time
- Second term: Interference from higher priority tasks
- Interference computed using ceiling function to account for multiple activations

#### Timing Diagram Interpretation
- Response time seen graphically
- Possible to verify with visual representation
- Helps understand interference patterns

## Blocking and Priority Inversion

### Blocking Time
Time a task waits for a lower priority task to release a shared resource.

### Priority Inversion Problem
1. High priority task τₕ wants resource
2. Resource held by low priority task τₗ
3. Medium priority task τₘ preempts τₗ
4. τₕ blocked by τₗ indirectly blocked by τₘ

### Priority Inversion Duration
Unbounded without resource access control protocols.

## DMS vs RMS

### Deadline Monotonic Scheduling (DMS)
- Priority based on relative deadline
- **Priority Rule**: Dᵢ < Dⱼ → Pᵢ > Pⱼ
- Handles Dᵢ ≠ Tᵢ
- Generalization of RMS

### Rate Monotonic Scheduling (RMS)
- Priority based on period
- **Priority Rule**: Tᵢ < Tⱼ → Pᵢ > Pⱼ
- Special case of DMS where Dᵢ = Tᵢ

### Comparison

| Feature | RMS | DMS |
|---------|-----|-----|
| Scope | Dᵢ = Tᵢ | Dᵢ ≤ Tᵢ |
| Optimality | Optimal when Dᵢ = Tᵢ | Optimal for constrained deadlines |
| Utilization Bound | U ≤ n(2^(1/n)-1) | Same bound |
| Complexity | Low | Low |

## EDF Analysis

### Earliest Deadline First (EDF)
- Optimal dynamic priority algorithm
- **Priority Rule**: Earlier absolute deadline has higher priority
- Preemptive scheduling

### Schedulability Test
For EDF on uniprocessor:

```
Σ(Cᵢ/Tᵢ) ≤ 1  (Necessary and Sufficient)
```

### Key Properties
1. Optimal among all scheduling algorithms
2. Achieves 100% processor utilization
3. Processor never idle when tasks are ready
4. Applies to any task set with utilization ≤ 1

### Dynamic Priority Assignment
```
At time t, priority(t) = -dᵢ(t)
where dᵢ(t) is absolute deadline
```

### Proof of Optimality
- If a task set is schedulable by any algorithm, it's schedulable by EDF
- When processor is not idle under EDF, it must be executing highest priority task

## Schedulability Tests Summary

### Static Priority (RMS/DMS)

#### Utilization-Based Test
```
U = Σ(Cᵢ/Tᵢ) ≤ n(2^(1/n) - 1)
```
- Fast but pessimistic
- Sufficient but not necessary

#### Response Time Test
```
Rᵢ⁽⁰⁾ = Cᵢ
Rᵢ⁽ᵏ⁺¹⁾ = Cᵢ + Σⱼ∈hp(i) (⌈Rᵢ⁽ᵏ⁾/Tⱼ⌉ × Cⱼ)
Rᵢ ≤ Dᵢ
```
- Necessary and sufficient
- More accurate but slower

### Dynamic Priority (EDF)

#### Utilization Test
```
U = Σ(Cᵢ/Tᵢ) ≤ 1
```
- Necessary and sufficient
- Simple and exact

## Task Set Design Guidelines

### For RMS/DMS
1. Assign higher priorities to critical or short deadline tasks
2. Ensure utilization bound
3. Consider response time if deadline < period
4. Account for blocking time with shared resources

### For EDF
1. No explicit priority assignment needed
2. Ensure utilization ≤ 1
3. Consider overhead for dynamic priority updates
4. More efficient than static priority

### Hybrid Approaches
- Use static priority for periodic tasks
- Use EDF for aperiodic tasks
- Balance predictability with efficiency

## Practical Examples

### Example 1: Response Time Analysis
```
Task Set:
τ₁: C₁ = 4, T₁ = 10, D₁ = 10
τ₂: C₂ = 3, T₂ = 15, D₂ = 15
τ₃: C₃ = 5, T₃ = 30, D₃ = 30

RMS priorities: P₁ > P₂ > P₃

Analysis for τ₃:
R₃⁽⁰⁾ = 5
R₃⁽¹⁾ = 5 + ⌈5/10⌉×4 + ⌈5/15⌉×3 = 5 + 4 + 3 = 12
R₃⁽²⁾ = 5 + ⌈12/10⌉×4 + ⌈12/15⌉×3 = 5 + 8 + 3 = 16
R₃⁽³⁾ = 5 + ⌈16/10⌉×4 + ⌈16/15⌉×3 = 5 + 8 + 3 = 16
R₃ = 16 ≤ 30 ✓ Schedulable
```

### Example 2: EDF Utilization
```
Task Set:
τ₁: C₁ = 2, T₁ = 5
τ₂: C₂ = 3, T₂ = 10
τ₃: C₃ = 4, T₃ = 20

Utilization: U = 2/5 + 3/10 + 4/20 = 0.4 + 0.3 + 0.2 = 0.9 ≤ 1 ✓
```

## Sources
- Lecture 4 - Real-Time Task Scheduling, Part 2.pdf
