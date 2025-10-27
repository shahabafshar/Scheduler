# Scheduling with Precedence Tasks

## Overview
Tasks with precedence constraints must execute in a specific order, where some tasks cannot start until their predecessors complete.

## Precedence Relationships

### Definition
Task τⱼ has precedence over task τᵢ if τᵢ cannot start until τⱼ completes.

Notation: τⱼ → τᵢ (τⱼ must complete before τᵢ starts)

### Precedence Graph
Directed graph representing task dependencies:
- **Nodes**: Tasks
- **Edges**: Precedence constraints
- **DAG**: Directed Acyclic Graph (assumed)

### Example
```
τ₁ → τ₂
τ₁ → τ₃
τ₂ → τ₄
τ₃ → τ₄
```
Task τ₄ cannot start until both τ₂ and τ₃ complete.

## Precedence Constraints

### Types of Precedence

#### Simple Precedence
τⱼ must complete before τᵢ starts.
```
Constraint: start_time(τᵢ) >= completion_time(τⱼ)
```

#### Timing Constraints
- **Minimum separation**: Minimum time between tasks
- **Maximum separation**: Maximum time between tasks
- **Relative deadlines**: Deadline relative to predecessor completion

### Task Characteristics
```
τᵢ = (rᵢ, Cᵢ, dᵢ, pred(τᵢ))
```
Where pred(τᵢ) is the set of predecessor tasks.

## Scheduling Approaches

### 1. Directed Graph Construction

#### Build Dependency Graph
```python
def build_precedence_graph(tasks):
    graph = {task: [] for task in tasks}
    
    for task in tasks:
        for predecessor in task.predecessors:
            graph[predecessor].append(task)
    
    return graph
```

#### Topological Sorting
Order tasks such that predecessors always come before successors.

```python
def topological_sort(graph):
    # Kahn's algorithm
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    
    queue = [node for node in in_degree if in_degree[node] == 0]
    result = []
    
    while queue:
        node = queue.pop(0)
        result.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result
```

### 2. Priority Assignment

#### Priority Based on Topological Order
Tasks earlier in topological order get higher priority.

#### Static Priority Assignment
```python
def assign_priorities(tasks):
    order = topological_sort(build_graph(tasks))
    
    for i, task in enumerate(order):
        task.priority = len(order) - i  # Higher-duty tasks get higher priority
```

### 3. Modified EDF

#### Precedence-Aware EDF
- Priority based on earliest deadline among ready tasks
- Task ready only when all predecessors complete

```python
def precedence_edf(tasks, current_time):
    # Find ready tasks
    ready = [t for t in tasks if is_ready(t, current_time)]
    
    if not ready:
        return IDLE
    
    # Schedule earliest deadline first
    return min(ready, key=lambda t: t.deadline)

def is_ready(task, current_time):
    # Check if all predecessors completed
    return all(predecessor.completed for predecessor in task.predecessors)
```

## Precedence Task Model

### Task Parameters
```
τᵢ = (Cᵢ, pred(τᵢ), succ(τᵢ), release_time, deadline)
```

Where:
- **Cᵢ**: Execution time
- **pred(τᵢ)**: Set of predecessors
- **succ(τᵢ)**: Set of successors
- **release_time**: Earliest start time
- **deadline**: Latest completion time

### Release and Completion
- Task released when all predecessors complete
- Cannot start before release time
- Must complete by deadline

### Critical Path
Longest path from source to sink task.
- Minimum makespan
- Determines overall completion time

## Scheduling Algorithms

### List Scheduling
Tasks listed in priority order, scheduled when possible.

#### Algorithm
```python
def list_scheduling(tasks):
    schedule = []
    time = 0
    
    # Sort by priority
    sorted_tasks = sort_by_priority(tasks)
    completed = set()
    
    while sorted_tasks:
        ready = [t for t in sorted_tasks if can_start(t, completed)]
        
        if ready:
            # Schedule highest priority ready task
            task = ready[0]
            schedule.append((task, time))
            time += task.C
            completed.add(task)
            sorted_tasks.remove(task)
        else:
            time += 1  # Wait
    
    return schedule

def can_start(task, completed):
    return all(p in completed for p in task.predecessors)
```

### Earliest Start Time (EST)
Start each task as early as possible.

#### Algorithm
```python
def earliest_start_scheduling(tasks):
    schedule = {}
    
    # Process in topological order
    topo_order = topological_sort(tasks)
    
    for task in topo_order:
        if not task.predecessors:
            # No predecessors
            start_time = task.release_time
        else:
            # Start after all predecessors complete
            start_time = max(pred.completion_time 
                            for pred in task.predecessors)
        
        task.start_time = start_time
        task.completion_time = start_time + task.C
        schedule[task] = (start_time, task.completion_time)
    
    return schedule
```

### Latest Start Time (LST)
Calculate latest start time to meet deadlines.

#### Algorithm
```python
def latest_start_scheduling(tasks):
    schedule = {}
    
    # Process in reverse topological order
    reverse_order = reversed(topological_sort(tasks))
    
    for task in reverse_order:
        if not task.successors:
            # No successors
            latest_start = task.deadline - task.C
        else:
            # Finish before any successor must start
            latest_start = min(succ.start_time 
                              for succ in task.successors) - task.C
        
        # Adjust to release time
        task.latest_start = max(task.release_time, latest_start)
        schedule[task] = task.latest_start
    
    return schedule
```

## Schedulability Analysis

### Makespan Calculation
Total time to complete all tasks considering precedence.

```python
def compute_makespan(schedule):
    return max(task.completion_time for task in schedule)
```

### Critical Path Analysis
```python
def find_critical_path(tasks):
    # Longest path through dependency graph
    distances = {task: 0 for task in tasks}
    
    topo_order = topological_sort(tasks)
    
    for task in topo_order:
        for successor in task.successors:
            new_distance = distances[task] + task.C
            if new_distance > distances[successor]:
                distances[successor] = new_distance
    
    return max(distances.values())
```

### Feasibility Check
Schedule is feasible if:
1. All precedence constraints satisfied
2. All deadlines met
3. Resource constraints satisfied

```python
def is_feasible(schedule):
    # Check precedence
    for task in tasks:
        for predecessor in task.predecessors:
            if predecessor.completion_time > task.start_time:
                return False
    
    # Check deadlines
    for task in tasks:
        if task.completion_time > task.deadline:
            return False
    
    return True
```

## Multiprocessor Scheduling

### Precedence on Multiple Processors
Additional complexity: tasks can execute in parallel if no precedence constraint.

### List Scheduling Heuristic
```python
def multiprocessor_list_scheduling(tasks, num_processors):
    available_processors = list(range(num_processors))
    processor_assignment = {}
    
    topo_order = topological_sort(tasks)
    completed = set()
    
    for task in topo_order:
        # Wait until ready
        while not can_start(task, completed):
            # Execute currently running tasks
            run_current_tasks()
        
        # Assign to available processor
        if available_processors:
            processor = available_processors.pop(0)
            assign_to_processor(task, processor)
    
    return processor_assignment
```

## Handling Timing Constraints

### Minimum Separation
```python
def enforce_min_separation(task1, task2, min_sep):
    # Ensure gap between tasks
    if task2.start_time - task1.completion_time < min_sep:
        task2.start_time = task1.completion_time + min_sep
```

### Maximum Separation
```python
def enforce_max_separation(task1, task2, max_sep):
    # Tight constraint
    if task2.start_time - task1.completion_time > max_sep:
        # May violate precedence
        return INFEASIBLE
```

## Practical Examples

### Example: Task Chain
```
τ₁ (C=2) → τ₂ (C=3) → τ₃ (C=1) → τ₄ (C=2)

Total makespan = 2 + 3 + 1 + 2 = 8
```

### Example: Parallel Paths
```
      ┌─ τ₂ (C=3) ─┐
τ₁ ───┤             ├── τ₄ (C=2)
      └─ τ₃ (C=2) ─┘

Critical path: τ₁ → τ₂ → τ₄ = 2 + 3 + 2 = 7
Total makespan = 7
```

## Sources
- Lecture 8 - Scheduling_Precedence_Tasks.pdf
