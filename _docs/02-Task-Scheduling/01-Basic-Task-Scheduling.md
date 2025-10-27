# Real-Time Task Scheduling - Part 1

## Overview
This document covers fundamental task scheduling algorithms for real-time systems.

## Scheduling Problem

### Input
- Set of real-time tasks {τ₁, τ₂, ..., τₙ}
- Timing constraints for each task
- Resource requirements

### Output
- Execution order (schedule)
- Feasibility determination
- Response time analysis

## Classification of Scheduling Algorithms

### By Priority Assignment
1. **Static Priority**: Fixed priority assignment
2. **Dynamic Priority**: Runtime priority assignment

### By Task Type
1. **Periodic**: Tasks with fixed periods
2. **Aperiodic/Sporadic**: Event-driven tasks
3. **Mixed**: Both periodic and aperiodic

### By System Architecture
1. **Uniprocessor**: Single CPU
2. **Multiprocessor**: Multiple CPUs
3. **Distributed**: Multiple processors over network

## Priority-Based Scheduling

### Static Priority Scheduling

#### Rate Monotonic Scheduling (RMS)
- **Priority Rule**: Shorter period = Higher priority
- Coding of priority: `Pᵢ = -Tᵢ`
- **Key Property**: Optimal among static priority algorithms
- **Assumptions**:
  - Periodic tasks
  - Independent tasks
  - Preemptive scheduling
  - Deadline = Period

**Priority Assignment**:
```
Priority(τ₁) = 1/T₁
if T₁ < T₂ then Priority(τ₁) > Priority(τ₂)
```

#### Deadline Monotonic Scheduling (DMS)
- **Priority Rule**: Shorter relative deadline = Higher priority
- **Advantage**: Handles cases where Dᵢ < Tᵢ
- **Generalization**: RMS is special case when Dᵢ = Tᵢ

**Priority Assignment**:
```
if D₁ < D₂ then Priority(τ₁) > Priority(τ₂)
```

### Dynamic Priority Scheduling

#### Earliest Deadline First (EDF)
- **Priority Rule**: Earlier absolute deadline = Higher priority
- **Key Property**: Optimal among all scheduling algorithms
- **Assumptions**:
  - Preemptive scheduling
  - Tasks are independent
  - Deadline = Period

**Priority Assignment**:
```
At time t, task with minimum dᵢ(t) has highest priority
dᵢ(t) = release_time + relative_deadline
```

## Schedulability Analysis

### Utilization-Based Test

#### RMS Schedulability (Liu & Layland)
For n periodic tasks with utilization:
```
U = Σ(Cᵢ/Tᵢ) ≤ n(2^(1/n) - 1)
```

As n → ∞:
```
U ≤ ln(2) ≈ 0.693
```

#### EDF Schedulability
Necessary and sufficient condition:
```
U = Σ(Cᵢ/Tᵢ) ≤ 1
```
- More efficient than RMS
- 100% processor utilization possible

### Response Time Analysis

#### Completion Time Test
For task τᵢ under static priority scheduling:

```
Rᵢ⁽⁰⁾ = Cᵢ
Rᵢ⁽ᵏ⁺¹⁾ = Cᵢ + Σⱼ (⌈Rᵢ⁽ᵏ⁾/Tⱼ⌉ × Cⱼ)
```

Where the sum is over all higher priority tasks.

Test converges when:
- Rᵢ⁽ᵏ⁺¹⁾ = Rᵢ⁽ᵏ⁾ (fixed point)
- Rᵢ ≤ Dᵢ (deadline met)

#### Example
```
Task 1: C₁ = 1, T₁ = 4
Task 2: C₂ = 2, T₂ = 5

Compute response time for Task 2:
R₂⁽⁰⁾ = 2
R₂⁽¹⁾ = 2 + ⌈2/4⌉ × 1 = 2 + 1 = 3
R₂⁽²⁾ = 2 + ⌈3/4⌉ × 1 = 2 + 1 = 3
R₂ = 3 ≤ 5 ✓ Schedulable
```

## Scheduling Scenarios

### Preemptive Scheduling
- Higher priority tasks can interrupt lower priority tasks
- Better responsiveness
- Context switching overhead

### Non-Preemptive Scheduling
- Tasks run to completion
- No context switching overhead
- Simpler implementation
- Potential for priority inversion

### Hybrid Approaches
- Deferrable preemption
- Limited preemption models
- Co-operative scheduling

## Practical Considerations

### Context Switching Overhead
- Time to save and restore task state
- Adds to effective execution time
- Should be included in schedulability analysis

### Task Jitter
- Variation in release times
- Can be bounded for analysis
- Affects response time

### Worst-Case Execution Time (WCET)
- Must be known or bounded
- Sources of pessimism in estimation
- Safety margins required

## Scheduling Examples

### Example 1: Three Periodic Tasks
```
Task A: C = 3, T = 20
Task B: C = 2, T = 5
Task C: C = 2, T = 10

RMS Priority: B > C > A
Utilization: U = 3/20 + 2/5 + 2/10 = 0.15 + 0.4 + 0.2 = Balancing check...
```

### Example 2: Deadline Constraint
```
Task 1: C = 4, T = 8, D = 6 (D < T)
Task 2: C = 2, T = 10, D = 4 (D < T)

DMS priorities: Task 2 > Task 1 (D₂ < D₁)
```

## Sources
- Lecture 3 - Real-time Task Scheduling, Part 1.pdf
