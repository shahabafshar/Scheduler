# Overload Handling: Imprecise Computation and (m,k)-Firm Task Model

## Overview
When system load exceeds capacity, overload handling techniques ensure graceful degradation and maintain critical task execution.

## Types of Overload

### Transient Overload
- Temporary system overload
- Caused by burst arrivals or mode changes
- Short duration

### Permanent Overload
- Sustained system overload
- More serious than transient
- Requires admission control or degradation

## Imprecise Computation

### Concept
Allow tasks to produce approximate results when exact results cannot be completed by deadline.

### Task Model
Each task τᵢ has two parts:
1. **Mandatory part** (Mᵢ): Must complete by deadline (critical)
2. **Optional part** (Oᵢ): Can be terminated early for approximation

```
Task τᵢ = Mandatory(Mᵢ) + Optional(Oᵢ)
Cᵢ = Mᵢ + Oᵢ
```

### Scheduling Objective
- Always complete mandatory parts on time
- Complete as much optional work as possible
- Maximize total reward/quality

### Scheduling Policies

#### Selection Rules
1. **Early start**: Start mandatory parts as early as possible
2. **Greedy**: Execute optional parts when no mandatory parts are ready
3. **Preference**: Prioritize high-value optional work

### Quality Metrics
- **Completion ratio**: percentage of optional work completed
- **Quality of service**: user-perceived quality
- **Reward**: value gained from optional execution

## (m,k)-Firm Task Model

### Definition
Task τᵢ is characterized by (mᵢ, kᵢ):
- **kᵢ**: window size (consecutive executions)
- **mᵢ**: minimum required completions in window

Task is acceptable if at least mᵢ out of kᵢ executions meet their deadlines.

### Example
```
Task with (3,5)-firm requirement:
- Must complete 3 out of every 5 executions
- Can drop 2 executions
- Still considered acceptable

Example sequence:
Execute: ✓ ✓ ✗ ✓ ✗ (3/5 = acceptable)
Execute: ✓ ✗ ✗ ✓ ✓ (3/5 = acceptable)
Execute: ✗ ✗ ✗ ✓ ✓ (2/5 = violation!)
```

### Window Constraints
- **Sliding window**: Constraint applies to every consecutive k executions
- **Tightest**: Must satisfy from any point in execution history
- **Relaxed**: Allows some window violations

### Scheduling for (m,k) Firm Tasks

#### Priority-Based Approach
- Modify priority based on execution history
- Reduce priority of tasks with good completion record
- Increase priority of tasks needing completion to meet (m,k)

#### Dynamic Priority Assignment
```
Priority depends on:
1. Basic priority (e.g., RMS)
2. Current completion status in window
3. Urgency to meet (m,k) requirement

If task close to violating (m,k):
    Priority += boost
Else if task has margin:
    Priority -= reduction
```

#### Feasibility Checking
For (m,k)-firm tasks, check if:
```
For each window of k consecutive executions,
at least m complete successfully
```

### Mixed Task Systems

#### Combination with Periodic Tasks
- Some tasks have firm (m,k) requirements
- Some tasks have hard deadlines
- Scheduling must balance both constraints

#### Admission Control
- Accept new firm tasks if:
  - Hard tasks still schedulable
  - Firm tasks can meet (m,k) constraints

## Graceful Degradation Strategies

### 1. Mandatory-Optional Decomposition
- Always execute mandatory parts
- Execute optional parts when resources available
- Trade-off: fewer tasks get optional work

### 2. Skip Over Strategy
- Skip some task executions entirely
- Use (m,k) constraint to decide which to skip
- Trade-off: reduced function vs. system stability

### 3. Quality Reduction
- Reduce computation quality
- Use simpler algorithms
- Trade-off: lower quality vs. more tasks complete

### 4. Dynamic QoS Adjustment
- Adjust Quality of Service based on load
- Reduce QoS for less critical tasks
- Trade-off: service levels vs. resource availability

## Schedulability Analysis

### For Imprecise Computation
```
Mandatory parts:
Σ(Mᵢ/Tᵢ) ≤ U_bound

Optional parts scheduled with remaining capacity
```

### For (m,k) Firm Tasks
```
Traditional schedulability:
- May have utilization > 1
- Some tasks can miss deadlines

(m,k) constraint:
- For window of k executions
- At least m complete successfully
- Check feasibility over multiple windows
```

## Application Examples

### Imprecise Computation
**Image Processing**:
- Mandatory: Downsample to 320×240
- Optional: Enhance to full resolution
- Result: Always timely view, sometimes high quality

**Sensor Fusion**:
- Mandatory: Essential sensor data
- Optional: Additional sensors for precision
- Result: Always basic fusion, sometimes enhanced

### (m,k) Firm Tasks
**Video Streaming**:
- (18,20) requirement
- Can drop 2 frames per second
- Still acceptable video quality

**Control Loop**:
- (4,5) requirement
- 4 out of 5 control updates must be on time
- Maintains stability

## Implementation

### Task Structure
```cpp
struct Task {
    int mandatory_time;
    int optional_time;
    int quality_reward;
};

struct FirmTask {
    int m_required;    // m out of k
    int k_window;      // window size
    int completed;     // in current window
    bool recent[k];    // completion history
};
```

### Scheduler Modifications
1. Prioritize mandatory parts
2. Track (m,k) completion status
3. Adjust priorities dynamically
4. Monitor overload conditions

## Performance Metrics

### Imprecise Computation
- Mandatory completion rate: 100%
- Optional completion rate: percentage
- Average quality: weighted by rewards

### (m,k) Firm Tasks
- Window violations: number of times m/k not met
- Acceptance rate: percentage of acceptable intervals
- Dropped task ratio: percentage of skipped executions

## Sources
- Lecture 9 - Overload handling -- Imprecise Computation and (m,k) firm task model-1.pdf
