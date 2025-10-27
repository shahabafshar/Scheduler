# Combined Scheduling

## Overview
Combined scheduling integrates multiple scheduling approaches to handle heterogeneous task sets with different characteristics and requirements.

## Motivation

### Task Heterogeneity
Real systems contain:
- **Periodic tasks**: Regular, predictable workload
- **Aperiodic tasks**: Event-driven, unpredictable
- **Sporadic tasks**: Random arrivals with minimum separation
- **Mixed criticalities**: Different timing guarantees needed

### Single Algorithm Limitations
- RMS: Only handles periodic tasks
- EDF: Requires utilization ≤ 1
- Aperiodic servers: Limited for periodic tasks

## Server-Based Approaches

### Background Scheduling

#### Concept
- Periodic tasks scheduled using fixed priority (e.g., RMS)
- Aperiodic tasks scheduled in background (lowest priority)
- Background execution when no periodic tasks ready

#### Implementation
```python
def background_scheduling():
    # Periodic tasks have fixed priorities
    periodic_ready = [t for t in periodic_tasks if t.is_ready()]
    
    if periodic_ready:
        # Run highest priority periodic task
        return max(periodic_ready, key=lambda t: t.priority)
    else:
        # Background execution for aperiodic tasks
        if aperiodic_queue:
            return aperiodic_queue.pop(0)  # FIFO
        return IDLE
```

#### Characteristics
- Simple implementation
- Poor aperiodic response time
- Periodic tasks not affected
- May starve aperiodic tasks

#### Schedulability
- Periodic tasks analyzed with RMS
- Aperiodic tasks have no guarantees

### Polling Server

#### Concept
Periodic task that services aperiodic tasks at fixed intervals.

#### Server Parameters
- **Period Tₛ**: Server activation period
- **Capacity Cₛ**: Execution budget per period
- **Priority Maybe**: Based on period (RMS)

#### Operation
```python
class PollingServer:
    def __init__(self, period, capacity):
        self.T = period
        self.C = capacity
        self.budget = 0
        self.next_activation = period
    
    def activate(self):
        # Refill budget
        self.budget = self.C
        invoked:
        # Check for aperiodic tasks
        if aperiodic_queue:
            # Service aperiodic task
            task = aperiodic_queue.pop(0)
            execute(task, budget)
            self.budget -= task.execution_time
    
    def deplete(self):
        # Budget exhausted
        self.budget = 0
```

#### Response Time
- Worst-case depends on polling period
- May serve instantaneously if polled at right time
- Worst-case: Wait full polling period

#### Schedulability
Server treated as periodic task:
```
U_periodic + C_s/T_s ≤ U_bound
```

### Sporadic Server

#### Concept
Server with replenishment of budget based on actual usage.

#### Key Idea
- Budget replenished when used
- Maintains long-term utilization bound
- Better response than polling server

#### Budget Management
```python
class SporadicServer:
    def __init__(self, period, capacity):
        self.T = period
        self.C = capacity
        self.budget = capacity
        self.available = 0
    
    def replenish(self):
        # Available budget
        if not self.active:
            self.available = self.budget
    
    def consume(self, amount):
        # Use budget
        self.available -= amount
        self.replenish_time = current_time + self.T
    
    def replenishment_check(self):
        # Check if ready to replenish
        if current_time >= self.replenish_time:
            self.available = self.budget
```

#### Advantage Over Polling
- Budget available immediately after use
- No waiting for polling period
- Better average response time

#### Schedulability
Similar to periodic task with period Tₛ and execution time Cₛ.

### Deferrable Server

#### Concept
Server maintains budget throughout its period until consumed.

#### Budget Conservation
- Budget remains available after replenishment
- Carried forward within period
- Not consumed if not used

#### Operation
```python
class DeferrableServer:
    def __init__(self, period, capacity):
        self.T = period
        self.C = capacity
        self.budget = capacity
        self.priority = 1 / period  # RMS style
    
    def consume(self, amount):
        self.budget -= amount
    
    def replenish(self):
        self.budget = self.C
```

#### Characteristic
- Maximum responsiveness for aperiodic tasks
- Budget available throughout period
- May interfere more with periodic tasks

### Total Bandwidth Server (TBS)

#### Concept
Assign deadline to aperiodic tasks based on bandwidth reservation.

#### Deadline Assignment
```
d_k = max(r_k, d_{k-1}) + C_k / U_s
```

Where:
- d_k: Deadline for aperiodic task k
- r_k: Release time
- C_k: Execution time
- U_s: Server utilization (C_s / T_s)

#### Priority
Aperiodic tasks scheduled by EDF using assigned deadlines.

#### Properties
- Optimal bandwidth allocation
- Maintains bound on server utilization
- Integrated with EDF scheduler

## Integrated Scheduling

### RMS + Sporadic Server

#### Approach
- Periodic tasks use RMS priorities
- Aperiodic tasks use sporadic server
- Server has periodic priority

#### Example
```python
tasks = [
    periodic_1: C=1, T=4,
    periodic_2: C=2, T=8,
    sporadic_server: C_s=1, T_s=5
]

priorities = RMS_priorities(tasks)
```

#### Schedulability
```
U_p + C_s/T_s ≤ U_bound
```

Where U_p is periodic task utilization.

### EDF + TBS

#### Approach
- All tasks (periodic and aperiodic) scheduled by EDF
- Aperiodic tasks get dynamically assigned deadlines

#### Implementation
```python
def edf_tbs_schedule():
    all_tasks = periodic_tasks + aperiodic_tasks
    
    # Assign deadlines to aperiodic tasks
    for ap_task in new_aperiodic_tasks:
        ap_task.deadline = max(ap_task.release, 
                               last_dead++) + ap_task.C / U_s
    
    # EDF schedule all tasks
    return min(all_tasks, key=lambda t: t.deadline)
```

#### Schedulability
```
Σ(C_i/T_i) for periodic + U_s ≤ 1
```

## Adaptive Server Tuning

### Load-Based Server Capacity
Adjust server capacity based on aperiodic load.

```python
def adapt_server_capacity(server, load_metric):
    if load_metric > threshold_high:
        # Increase server capacity
        server.C = min(server.C_max, server.C + increment)
    elif load_metric < threshold_low:
        # Decrease server capacity
        server.C = max(server.C_min, server.C - decrement)
```

### Priority Adjustment
Adjust server priority based on backlog.

## Multi-Server Systems

### Multiple Servers
Run multiple servers concurrently for different aperiodic classes.

```python
servers = [
    high_priority_server: C=2, T=10, priority=High,
    low_priority_server: C=1, T=20, priority=Low
]
```

### Server Hierarchy
- Higher priority server for critical aperiodics
- Lower priority server for best-effort aperiodics
- Periodic tasks unaffected

## Design Guidelines

### Selecting Server Type
- **Background**: Simple, no guarantees
- **Polling**: Simple, predictable, higher latency
- **Sporadic**: Good balance, moderate complexity
- **Deferrable**: Best responsiveness, higher interference
- **TBS**: Optimal bandwidth, EDF integration

### Server Parameter Selection
- **Capacity**: Trade-off between periodic performance and aperiodic responsiveness
- **Period**: Smaller period = better responsiveness = higher overhead
- **Priority**: Based on period (RMS) for static priority

## Sources
- Lecture 7 - Combined Scheduling.pdf
