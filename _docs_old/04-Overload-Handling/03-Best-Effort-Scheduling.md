# Overload Handling: Best Effort Scheduling

## Overview
Best effort scheduling prioritizes tasks based on utility and importance rather than strict deadlines, ensuring the most valuable work is completed first during overload conditions.

## Best Effort Philosophy

### Key Principle
"Complete the most important tasks first, given available resources."

### Characteristics
- No hard deadline guarantees
- Prioritization based on value/utility
- Graceful degradation under load
- Maximize total system utility

### When to Use
- Soft real-time systems
- Performance-critical applications
- Overloaded conditions
- Non-critical workloads

## Utility-Based Scheduling

### Task Utility Function
Each task τᵢ has a utility function Uᵢ(t):
- **Uᵢ(t)**: Value/reward if task completes at time t
- Typically decreases as delay increases
- May have deadline where utility drops to zero

### Common Utility Functions

#### Constant Utility
```
U(t) = c  for t < d
U(t) = 0  for t >= d
```
- Fixed value before deadline
- Zero after deadline

#### Linear Decay
```
U(t) = U_max × (1 - t/d)  for t < d
U(t) = 0                   for t >= d
```
- Value decreases linearly with time
- Zero at deadline

#### Exponential Decay
```
U(t) = U_max × e^(-λt)  for t < d
U(t) = 0                for t >= d
```
- Rapid initial decay
- Controlled by parameter λ

#### Step Function
```
U(t) = U_high    for t < d_early
U(t) = U_low     for d_early <= t < d
U(t) = 0         for t >= d
```
- High value for early completion
- Lower value for late completion
- Zero after deadline

### Example
```python
class UtilityFunction:
    def constant(self, time, deadline, value):
        return value if time < deadline else 0
    
    def linear(self, time, deadline, max_value):
        if time >= deadline:
            return 0
        return max_value * (1 - time / deadline)
    
    def exponential(self, time, deadline, max_value, decay_rate):
        if time >= deadline:
            return 0
        return max_value * math.exp(-decay_rate * time)
```

## Best Effort Scheduling Algorithms

### 1. Greedy Algorithm

#### Principle
Always schedule task with highest current utility next.

#### Algorithm
```python
def greedy_best_effort_schedule(tasks, current_time):
    # Compute utility for each ready task
    for task in ready_tasks:
        task.current_utility = task.utility_function(current_time)
    
    # Sort by utility (descending)
    tasks_sorted = sorted(tasks, 
                         key=lambda t: t.current_utility, 
                         reverse=True)
    
    # Execute highest utility task
    next_task = tasks_sorted[0]
    return next_task
```

#### Characteristics
- Simple scalable
- Can select locally optimal choices
- May not find globally optimal solution

### 2. Maximum Total Utility Scheduling

#### Objective
Maximize total utility over all tasks:
```
Maximize Σ Uᵢ(completion_timeᵢ)
```

#### Complexity
- NP-hard in general case
- Heuristics required for practical implementation

#### Approximation Heuristics

##### Weighted Earliest Deadline First (WEDF)
```
Priority = U(t) / (d - t)
```
- Higher utility and urgency = higher priority
- Balance value and timeliness

##### Dynamic Value Densities
```
Value density = U(t) / remaining_time
```
- Select highest value density task
- Similar to WEDF

### 3. Resource Allocation with Utility

#### Multi-Resource Scheduling
Distribute resources (CPU, memory, bandwidth) to maximize utility.

#### Optimization Problem
```
Maximize: Σ Uᵢ(f_i)
Subject to:
    Σ f_i ≤ F (total resources)
    f_i ≥ f_min (minimum allocation)
```

Where f_i is resource allocation fraction for task i.

## Implementation Strategies

### Online Scheduling

#### Local Decisions
- Decide which task to run next
- Based on current state only
- No knowledge of future arrivals

#### Utility Updating
```python
def online_scheduler(tasks, current_time):
    # Update utilities for all ready tasks
    for task in ready_tasks:
        elapsed = current_time - task.release_time
        task.current_utility = task.utility(elapsed)
    
    # Select highest utility
    return max(tasks, key=lambda t: t.current_utility)
```

### Offline Scheduling

#### Global Optimization
- Know all tasks in advance
- Compute optimal schedule
- More complex but better results

### Hybrid Approaches

#### Window-Based
- Plan schedule over short window
- Recompute periodically
- Balance optimality with responsiveness

#### Predictive
- Estimate future arrivals
- Adapt schedule proactively
- More intelligent decisions

## Admission Control

### Best Effort Admission
Accept tasks if:
1. System not in critical state
2. Can provide reasonable utility
3. Other tasks maintain acceptable quality

### Admission Strategy
```python
def admit_task(new_task, current_tasks):
    # Estimate utility with new task
    estimated_utility = estimate_total_utility(current_tasks + [new_task])
    
    # Estimate utility without
    baseline_utility = estimate_total_utility(current_tasks)
    
    # Admit if marginal utility positive
    if estimated_utility > baseline_utility:
        return ADMIT
    else:
        return REJECT
```

## Quality Adaptation

### Adaptive Quality Levels
Adjust task quality based on system load to maintain utility.

### Strategies

#### Uniform Reduction
Reduce all task qualities equally to maintain throughput.

#### Priority-Based Reduction
Reduce lower priority task qualities first.

#### Value-Based Reduction
Reduce qualities for tasks with lower utility first.

### Implementation
```python
def adapt_quality(tasks, load_factor):
    if load_factor > 1.0:  # Overload
        reduction = load_factor - 1.0
        
        for task in tasks:
            # Reduce quality proportional to priority
            quality_factor = 1.0 - (reduction * task.utility_weight)
            task.quality = max(min_quality, 
                              task.base_quality * quality_factor)
```

## Performance Evaluation

### Metrics

#### Total Utility
```
U_total = Σ Uᵢ(completion_timeᵢ)
```

#### Utility Ratio
```
Utility_ratio = U_achieved / U_maximum
```

#### Task Completion Rate
```
Completion_rate = tasks_completed / tasks_arrived
```

#### Average Utility
```
U_avg = U_total / tasks_completed
```

### Comparison with Deadline-Based
- Different objectives (utility vs. deadlines)
- Different metrics (total value vs. miss ratio)
- May schedule different tasks

## Application Scenarios

### Media Streaming
- Value decreases with delay
- Best effort ensures high-value packets prioritized
- Lower-value packets may be dropped

### Web Services
- Different request values
- High-value requests processed first
- Maximize revenue or satisfaction

### Cloud Computing
- Different job priorities
- Resources allocated to high-value jobs
- Maximize total value delivered

## Sources
- Lecture 11 - Overload handling -- Best effort scheduling.pdf
