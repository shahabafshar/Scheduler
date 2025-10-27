# Resource Access Control Protocols

## Overview
Resource access control protocols manage the sharing of resources among real-time tasks while preventing priority inversion and ensuring predictable blocking times.

## The Priority Inversion Problem

### Classic Priority Inversion Scenario
```
Time  |  P=3 (τ₁)  |  P=2 (τ₂)  |  P=1 (τ₃)  |
------+------------+------------+------------+
t₁    |            |            | acquire(R) |
t₂    |            | running    | blocked    |
t₃    | preempts   |            | blocked    |
t₄    | waiting(R) |            | blocked    |
t₅    | blocked    | running    | blocked    |
t₆    | blocked    |            | running    |
t₇    | blocked    |            | release(R) |
t₈    | acquire(R) |            |            |
```

### Problem
- High priority task τ₁ blocked by low priority task τ₃
- Medium priority task τ₂ preempts τ₃
- τ₁ experiences unbounded priority inversion

## Resource Access Control Protocols

### 1. Priority Inheritance Protocol (PIP)

#### Basic Idea
When a low priority task holds a resource needed by a high priority task, the low priority task temporarily inherits the high priority.

#### Rules
1. Resource access: acquire(R) and release(R) operations
2. Priority inheritance: holding task inherits highest priority of waiting tasks
3. Original priority restored: when resource is released

#### Algorithm
```python
def acquire(resource, task):
    if resource.locked:
        # Add to waiting queue
        resource.waiters.append(task)
        # Inherit highest priority from waiters
        current_holder.priority = max(w.priority for w in resource.waiters)
    else:
        resource.lock(task)
        resource.holder = task

def release(resource, task):
    resource.unlock()
    resource.holder.priority = task.original_priority
    if resource.waiters:
        # Wake highest priority waiter
        next_task = max(resource.waiters, key=lambda t: t.priority)
        resource.lock(next_task)
```

#### Properties
- Prevents chained blocking
- Bounded blocking time
- Deadlock may still occur (nesting)

#### Blocking Bound
```
Bᵢ ≤ max{CScⱼ | Pⱼ < Pᵢ AND τⱼ can block τᵢ}
```

### 2. Priority Ceiling Protocol (PCP)

#### Basic Idea
Each resource has a priority ceiling = highest priority of any task that may use it. Task accessing resource immediately assumes ceiling priority.

#### Rules
1. Resource has ceiling(R) = max{Pᵢ | τᵢ uses R}
2. Task attempting to acquire R gets ceiling priority
3. Task can acquire R only if current priority > all locked resource ceilings
4. Priority restored when resource released

#### Algorithm
```python
ceiling = {}  # Resource → priority

def acquire(resource, task):
    # Check ceiling violation
    for r in locked_resources:
        if ceiling[r] >= task.priority:
            return BLOCKED
    
    # Acquire and raise priority
    resource.lock(task)
    task.priority = max(task.priority, ceiling[resource])

def release(resource, task):
    resource.unlock()
    # Restore original priority
    task.priority = task.original_priority
```

#### Properties
- Prevents deadlock
- Prevents transitive blocking
- Each task blocked at most once
- Simplifies schedulability analysis

#### Blocking Bound
```
Bᵢ ≤ max{CScⱼ | Pⱼ < Pᵢ AND ceiling(R) ≥ Pᵢ}
```

### 3. Stack Resource Policy (SRP)

#### Basic Idea
Extends PCP concept. Each task has a preemption level. Resource has a ceiling level. Task can only preempt if its level is greater than maximum ceiling of resources currently locked.

#### Preemption Level
```
Level(τᵢ) ∝ 1/Pᵢ  (inversely proportional to priority)
```

#### SRP Rules
1. Task τᵢ can preempt τⱼ iff Level(τᵢ) > Level(τⱼ) AND Level(τᵢ) > max locked resource ceilings
2. Task can access resource iff Level(τᵢ) > ceiling(R)
3. Resource ceiling = max{Level(τⱼ) | τⱼ uses R}

#### Comparison with PCP
- SRP is more general
- PCP is special case of SRP
- SRP allows earlier release of resources

## Protocol Comparison

| Feature | PIP | PCP | SRP |
|---------|-----|-----|-----|
| Deadlock Prevention | No | Yes | Yes |
| Transitive Blocking | Possible | No | No |
| Blocking Bound | Multiple | Once | Once |
| Complexity | Low | Medium | Medium |
| Priority Inheritance | Yes | No | No |
| Preemption Levels | No | No | Yes |

## Implementation Considerations

### Semaphores
```cpp
// Binary semaphore implementation
Semaphore s = create_semaphore(1);

// Wait/P
wait(s) {
    while (s.value == 0) {
        block(current_task);
    }
    s.value = 0;
}

// Signal/V
signal(s) {
    s.value = 1;
    unblock(waiting_task);
}
```

### Mutexes
- Mutual exclusion lock
- Ownership tracking
- Priority inheritance or priority ceiling support

### Readers-Writers Locks
- Multiple readers allowed
- Single writer exclusive
- Priority-aware implementations

## Blocking Time Analysis

### With PCP
For task τᵢ:

1. List resources R used by lower priority tasks τⱼ where Pⱼ < Pᵢ
2. Check if ceiling(R) ≥ Pᵢ
3. For qualifying resources, compute CSⱼ (critical section length)
4. Bᵢ = max{CSⱼ}

### Calculation Example
```
Tasks:
τ₁: P₁ = 3, uses R₁ (CS₁ = 2)
τ₂: P₂ = 2, uses R₁ (CS₂ = 3), R₂ (CS₂ = 1)
τ₃: P₃ = 1, uses R₂ (CS₃ = 4)

Resource Ceilings:
R₁: ceiling = max(P₁, P₂) = 3
R₂: ceiling = max(P₂, P₃) = 2

Blocking Times:
B₁: No lower priority tasks → 0
B₂: τ₃ uses R₂ with ceiling = 2 ≥ P₂ → B₂ = 4
B₃: No lower priority tasks → 0
```

## Schedulability with Resource Protocols

### Modified Response Time Analysis
```
Rᵢ⁽⁰⁾ = Cᵢ + Bᵢ
Rᵢ⁽ᵏ⁺¹⁾ = Cᵢ + Bᵢ + Σⱼ∈hp(i) (⌈Rᵢ⁽ᵏ⁾/T难度ⱼ⌉ × Cⱼ)
```

Where Bᵢ is calculated using the appropriate protocol.

### Utilization Test
Same utilization bounds apply, but must account for blocking:
```
U + max{Bᵢ/Tᵢ} ≤ bound
```

## Best Practices

### Design Guidelines
1. Minimize critical sections
2. Use priority ceiling or SRP for simplicity
3. Avoid deep nesting of resource access
4. Analyze blocking times during design

### Implementation Tips
1. Use built-in OS primitives when available
2. Consider overhead of protocol enforcement
3. Profile actual blocking times
4. Test under worst-case scenarios

## Sources
- Lecture 5 - Resource Access Control Protocols.pdf
