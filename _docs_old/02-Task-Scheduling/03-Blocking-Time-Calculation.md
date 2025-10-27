# Blocking Time Calculation

## Overview
Blocking time occurs when a higher priority task must wait for a lower priority task to release a shared resource. This document details how to calculate blocking time for schedulability analysis.

## Blocking Scenarios

### Direct Blocking
Higher priority task τᵢ is directly blocked by lower priority task τⱼ when:
1. τⱼ holds a shared resource R
2. τᵢ wants to access R
3. τᵢ must wait until τⱼ releases R

### Indirect Blocking (Priority Inversion)
τᵢ is indirectly blocked when:
1. τⱼ holds resource R
2. Medium priority task τₖ preempts τⱼ
3. τᵢ must wait for τₖ to complete before τⱼ releases R

## Blocking Time Definition

### Maximum Blocking Time
Bᵢ = Maximum time that task τᵢ can be blocked by a lower priority task

### Critical Section
- Code that accesses shared resources
- Must execute atomically
- Protected by synchronization primitives

## Resource Access Patterns

### Nesting
```
Resource R₁ nested in R₂:
- acquire(R₂)
- acquire(R₁)
- ... critical section ...
- release(R₁)
- release(R₂)
```

Blocking time must account for all nested resources.

### Non-Nesting
- Resources accessed in sequence
- Simpler to analyze
- Maximum blocking = maximum critical section length

## Priority Ceiling Protocol (PCP)

### Basic Concept
- Each resource has a priority ceiling
- Ceiling = highest priority of tasks using the resource
- Task inherits ceiling priority when accessing resource

### Blocking Bounds Under PCP
- Each task can be blocked at most once
- Blocking bounded by longest critical section using ceiling ≥ priority

### PCP Implementation
```cpp
// Example priority ceiling
Resource R₁: ceiling = max(Pᵢ) ∀ τᵢ using R₁

// When τⱼ acquires R₁
if (P_j < P(R₁.ceiling))
    P_j = P(R₁.ceiling)  // Priority inheritance
```

## Calculating Blocking Time

### Formula
For task τᵢ with priority Pᵢ:

```
Bᵢ = max{CScⱼ | Pⱼ < Pᵢ AND τⱼ uses resource with ceiling ≥ Pᵢ}
```

Where:
- CSⱼ is the longest critical section of τⱼ
- Only consider lower priority tasks
- Only resources with ceiling ≥ Pᵢ

### Step-by-Step Calculation

#### Step 1: Identify Resources
List all shared resources used by the task set.

#### Step 2: Assign Priority Ceilings
For each resource R:
```
ceiling(R) = max{Pᵢ | τᵢ accesses R}
```

#### Step 3: Find Critical Sections
For each task τⱼ, identify:
- Resources it accesses
- Duration of each critical section
- Maximum critical section length

#### Step 4: Compute Blocking Time
For each task τᵢ:
1. Consider all lower priority tasks (Pⱼ < Pᵢ)
2. For tasks using resources with ceiling ≥ Pᵢ
3. Take maximum critical section length

### Example Calculation

```
Task Set:
τ₁: P₁ = 3, uses R₁ (CS₁ = 2ms)
τ₂: P₂ = 2, uses R₁ (CS₂ = 3ms), R₂ (CS₂ = 1ms)
τ₃: P₃ = 1, uses R₂ (CS₃ = 2ms)

Resources:
R₁: ceiling = max(3,2) = 3
R₂: ceiling = max(2,1) = 2

Calculate B₁ (highest priority):
- No lower priority tasks → B₁ = 0

Calculate B₂:
- Lower priority: τ₃ (P₃ = 1 < P₂ = 2)
- τ₃ uses R₂ with ceiling = 2 ≥ P₂
- B₂ = max(CS₃) = 2ms

Calculate B₃:
- Lower priority: none
- B₃ = 0
```

## Response Time with Blocking

### Modified Response Time Formula
```
Rᵢ⁽⁰⁾ = Cᵢ + Bᵢ
Rᵢ⁽ᵏ⁺¹⁾ = Cᵢ + Bᵢ + Σⱼ∈hp(i) (⌈Rᵢ⁽ᵏ⁾/Tⱼ⌉ × Cⱼ)
```

Key difference: Initial guess includes blocking time.

### Analysis Procedure
1. Calculate Bᵢ for each task
2. Verify Bᵢ is bounded (PCP guarantees this)
3. Perform response time analysis with blocking
4. Check Rᵢ ≤ Dᵢ for all tasks

## Nested Resources

### Handling Nesting
For nested resource access:
- Compute worst-case nested path
- Consider all combinations of critical sections
- May require detailed code analysis

### Example with Nesting
```
Task τⱼ accesses:
  acquire(R₁) → CS₁ = 1ms → release(R₁)
  acquire(R₂) → acquire(R₁) → CS_nest = 2ms → release(R₁) → release(R₂)

Blocking time from τⱼ = max(CS₁, CS_nest) = max(1,2) = 2ms
```

## Best Practices

### Design Guidelines
1. Minimize critical section lengths
2. Use PCP or similar protocol
3. Avoid deep nesting
4. Keep resource usage simple

### Analysis Steps
1. Identify all shared resources
2. Determine priority ceilings
3. Measure critical sections (WCET analysis)
4. Compute blocking times
5. Update schedulability tests

### Verification
- Blocking time should be bounded
- Include in response time calculations
- Verify Bᵢ < Dᵢ for each task
- Consider worst-case scenarios

## Blocking vs. Preemption

### Preemption
- Higher priority task interrupts lower priority task
- Lower priority task resumes later
- Increases interference term in response time

### Blocking
- Lower priority task prevents higher priority task
- Only possible with shared resources
- Adds blocking term to response time

### Combined Analysis
Both effects are accounted for in:
```
Rᵢ = Cᵢ + Bᵢ + Iᵢ
```
Where:
- Cᵢ: Own computation
- Bᵢ: Blocking time
- Iᵢ: Interference from higher priority tasks

## Sources
- Blocking Time Calculation - notes.pdf
