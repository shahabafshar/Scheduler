# Analysis: EDF + HVDF Scheduling Problem

## Question Breakdown

### Problem Statement
**Construct an EDF schedule with HVDF scheduling policy for the following tasks. Clearly mark which instances missed its deadline. What is the total value obtained?**

**Given Tasks**:
- T1 = (C=3, D=8), Value=3
- T2 = (C=1, D=4), Value=1
- T3 = (C=1, D=4), Value=2
- T4 = (C=2, D=6), Value=3

**Notation**: Task = (Computation_time, Deadline)

### Key Requirements
1. **Primary Scheduling**: EDF (Earliest Deadline First)
   - Tasks ordered by absolute deadline
   
2. **Tie-Breaking**: HVDF (Highest Value Density First)
   - When two tasks have same deadline, choose by value density
   - Value Density = Value / Computation_time
   
3. **Task Characteristics**:
   - **Aperiodic tasks** (one-time execution, not periodic)
   - All arrive at time 0
   - Must complete within their deadlines
   - No partial execution allowed
   
4. **Value Calculation**:
   - Task meets deadline → contributes its value
   - Task misses deadline → contributes 0
   - Total value = sum of all values from successful completions

---

## What the Current System Lacks

### ❌ Critical Missing Features

#### 1. **Aperiodic Task Scheduling with EDF**
**Current State**: 
- `EDFScheduler` only handles **periodic tasks**
- Creates task instances at regular intervals (every period)
- No support for one-time aperiodic tasks

**What's Needed**:
- Handle tasks that arrive once at a specific time
- Support tasks without periods (aperiodic)
- Allow different arrival times (not just time 0)

**Current Code** (scheduler/core/algorithms/edf.py):
```python
class EDFScheduler(SchedulerBase):
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        if not ready_queue:
            return None
        return min(ready_queue, key=lambda t: t.deadline)  # Only sorts by deadline
```

**Issue**: No tie-breaking logic, only periodic task support.

---

#### 2. **HVDF Tie-Breaking in EDF**
**Current State**:
- `HVDFScheduler` exists but is standalone
- Uses value density as **primary** priority (not tie-breaker)
- No integration with EDF

**What's Needed**:
- **Hybrid scheduler**: EDF + HVDF
- Sort by deadline first (EDF)
- When deadlines equal, sort by value density (HVDF)

**Current Code** (scheduler/core/algorithms/overload.py):
```python
class HVDFScheduler(SchedulerBase):
    def assign_priorities(self) -> None:
        for task in self.tasks:
            value = self.task_values.get(task.id, 0.0)
            value_density = value / task.computation_time
            task.priority = int(value_density * 1000)  # Primary priority
```

**Issue**: HVDF is primary, not a tie-breaker for EDF.

---

#### 3. **Value Tracking and Calculation**
**Current State**:
- Tasks have no `value` attribute in `PeriodicTask`
- `ImpreciseTask` has value, but not general tasks
- No mechanism to track:
  - Which tasks completed on time
  - Which tasks missed deadlines
  - Total value accumulated

**What's Needed**:
- Add `value` field to tasks
- Track deadline meets/misses per task
- Calculate total value = Σ(value | deadline met)

**Current Data Model** (scheduler/core/task.py):
```python
@dataclass
class PeriodicTask:
    id: str
    computation_time: float
    period: float
    deadline: Optional[float] = None
    priority: int = -1
    # ❌ No value field
```

---

#### 4. **Non-Preemptive Scheduling**
**Current State**:
- All schedulers are **preemptive**
- Tasks can be preempted and resumed
- Problem explicitly states: "No partial execution of tasks is allowed"

**What's Needed**:
- **Non-preemptive mode**
- Once a task starts, it runs to completion
- Cannot interrupt a running task

**Current Simulation Loop** (scheduler/core/scheduler_base.py):
```python
# Allows preemption at every time unit
if new_task and new_task.task_id != current_running:
    # Preempt and switch
```

**Issue**: Always preemptive, no option for non-preemptive.

---

#### 5. **Single-Instance Aperiodic Task Instances**
**Current State**:
- `AperiodicTask` exists but not well-integrated
- Server schedulers handle aperiodic tasks via servers
- No direct EDF scheduling of aperiodic tasks

**What's Needed**:
- Direct scheduling of aperiodic tasks with EDF
- Tasks arrive once, execute once
- No periodic repetition

---

### ⚠️ Additional Considerations

#### 6. **Value Density Calculation**
**Formula**: Value Density = Value / Computation_time

For the given problem:
- T1: 3 / 3 = **1.0**
- T2: 1 / 1 = **1.0**
- T3: 2 / 1 = **2.0**
- T4: 3 / 2 = **1.5**

When T2 and T1 compete (both have different deadlines), EDF chooses by deadline.
If they had same deadline, HVDF would choose T2 (higher density).

---

#### 7. **Absolute vs Relative Deadlines**
**Current**: Tasks have periods, deadlines are relative to arrival
**Needed**: Absolute deadlines (e.g., "deadline = 8" means time 8, not 8 time units from now)

---

## Implementation Checklist

To solve this specific problem, the system needs:

- [ ] **Hybrid EDF-HVDF Scheduler**
  - Primary: Sort by absolute deadline (EDF)
  - Secondary: Sort by value density when deadlines tie (HVDF)
  
- [ ] **Aperiodic Task Support in EDF**
  - Handle tasks that arrive once
  - Support varying arrival times
  - No periodic repetition
  
- [ ] **Value Tracking**
  - Add `value` field to tasks
  - Track which tasks completed successfully
  - Calculate total value from successful completions
  
- [ ] **Non-Preemptive Mode**
  - Option to run tasks to completion without interruption
  - Flag: `preemptive: bool = True` with ability to set `False`
  
- [ ] **Deadline Miss Detection**
  - Flag tasks that didn't complete by their deadline
  - Mark value contribution as 0 for missed tasks
  
- [ ] **One-Time Execution**
  - Tasks execute exactly once (not repeated every period)
  - Track execution completion status

---

## Example Solution (Manual)

### Given
All tasks arrive at **t=0** with absolute deadlines:

| Task | C | D | Value | VD | 
|------|---|---|-------|-----|
| T1   | 3 | 8 | 3     | 1.0 |
| T2   | 1 | 4 | 1     | 1.0 |
| T3   | 1 | 4 | 2     | 2.0 |
| T4   | 2 | 6 | 3     | 1.5 |

### Schedule (Non-preemptive)

**t=0-1**: 
- Ready: T1(D=8), T2(D=4), T3(D=4), T4(D=6)
- EDF: T2 and T3 tie (D=4)
- HVDF: T3 has VD=2.0 > T2 VD=1.0
- **Execute T3** (C=1)

**t=1-2**:
- Ready: T1(D=8), T2(D=4), T4(D=6)
- EDF: T2 (D=4) earliest
- **Execute T2** (C=1)

**t=2-4**:
- Ready: T1(D=8), T4(D=6)
- EDF: T4 (D=6) < T1 (D=8)
- **Execute T4** (C=2)

**t=4-7**:
- Ready: T1(D=8)
- **Execute T1** (C=3)

### Results
- ✅ T3 completed at t=1 (deadline=4) → Value = 2
- ✅ T2 completed at t=2 (deadline=4) → Value = 1
- ✅ T4 completed at t=4 (deadline=6) → Value = 3
- ✅ T1 completed at t=7 (deadline=8) → Value = 3

**Total Value = 2 + 1 + 3 + 3 = 9**

---

## Conclusion

The current system **cannot solve this problem** without significant enhancements:

1. **No hybrid EDF+HVDF scheduler**
2. **No aperiodic task support in EDF**
3. **No value tracking mechanism**
4. **No non-preemptive scheduling mode**
5. **All schedulers assume periodic tasks**

### Priority for Implementation
1. **CRITICAL**: Aperiodic task EDF scheduler
2. **CRITICAL**: HVDF tie-breaking logic
3. **CRITICAL**: Value field and tracking
4. **HIGH**: Non-preemptive scheduling option
5. **MEDIUM**: UI for aperiodic task configuration

---

## Recommended New Scheduler

```python
class EDFHVDFScheduler(SchedulerBase):
    """
    EDF with HVDF tie-breaking for aperiodic tasks.
    
    - Primary: Earliest Deadline First
    - Tie-breaker: Highest Value Density First
    - Mode: Non-preemptive (optional)
    - Task type: Aperiodic (one-time execution)
    """
    
    def __init__(self, tasks: List[AperiodicTask], task_values: Dict[str, float],
                 preemptive: bool = False, duration: int = 100):
        self.task_values = task_values
        self.preemptive = preemptive
        self.completed_tasks = []
        # ... rest of implementation
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select by EDF, tie-break by HVDF."""
        if not ready_queue:
            return None
        
        # Calculate value density for each task
        def sort_key(task):
            vd = self.task_values.get(task.task_id, 0) / task.remaining_time
            return (task.deadline, -vd)  # EDF primary, HVDF secondary (negative for DESC)
        
        return min(ready_queue, key=sort_key)
    
    def calculate_total_value(self) -> float:
        """Sum values of tasks that met deadlines."""
        total = 0
        for task in self.completed_tasks:
            if task.completion_time <= task.deadline:
                total += self.task_values.get(task.task_id, 0)
        return total
```

This is the **minimum viable implementation** to solve the given problem.

