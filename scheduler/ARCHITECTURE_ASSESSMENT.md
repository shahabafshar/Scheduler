# Architecture Assessment: Hardwiring vs Flexibility

## Executive Summary

**Current Flexibility Score: 35/100** 🔴

The system is **highly hardwired** to specific scenarios, making it difficult to:
- Mix periodic and aperiodic tasks in one schedule
- Combine different priority policies (e.g., RMS + HVDF)
- Reuse components (value tracking, non-preemptive control)
- Add new scheduling combinations without duplicating code

## Detailed Analysis

### 🔴 Critical Hardwiring Issues

#### 1. Scheduler-Task Type Coupling (Severity: HIGH)
**Current**: Each scheduler only accepts one task type
```python
RMSScheduler(periodic_tasks)      # ← Can't add aperiodic
EDFHVDFScheduler(aperiodic_tasks) # ← Can't add periodic
```

**Impact**: Cannot simulate real-world systems with mixed workloads.

**Solution**: Unified scheduler accepting both task types with per-type policies.

---

#### 2. Giant If/Elif Scheduler Selection (Severity: HIGH)
**Current**: 80+ line if/elif chain in app.py
```python
if algorithm_category == "Aperiodic":
    scheduler = EDFHVDFScheduler(...)
elif algorithm.startswith("RMS"):
    scheduler = RMSScheduler(...)
elif algorithm.startswith("EDF"):  # BUG: Matched "EDF+HVDF"!
    scheduler = EDFScheduler(...)
```

**Impact**: 
- Order-dependent bugs (we just fixed one!)
- Hard to add new algorithms
- Each algorithm needs manual UI integration

**Solution**: Registry pattern with self-describing schedulers.

---

#### 3. Duplicated Value Tracking (Severity: MEDIUM)
**Current**: Only `EDFHVDFScheduler` has `calculate_total_value()`

**Impact**: Can't track values for RMS/EDF even though tasks have `value` field.

**Solution**: Extract to mixin or base class.

---

#### 4. Reimplemented Non-Preemptive Logic (Severity: MEDIUM)
**Current**: Each scheduler reimplements preemptive control

**Impact**: Code duplication, inconsistent behavior.

**Solution**: Centralize in `SchedulerBase` or mixin.

---

### 🟡 Moderate Hardwiring Issues

#### 5. Inflexible Priority Assignment (Severity: MEDIUM)
**Current**: Each scheduler has hardcoded priority logic

**Impact**: Can't do RMS+HVDF tie-breaking without new scheduler.

**Solution**: Strategy pattern for priority policies.

---

#### 6. Monolithic Ready Queue (Severity: LOW)
**Current**: Single ready queue for all tasks

**Impact**: Can't implement multi-level feedback queues or separate periodic/aperiodic queues.

**Solution**: Pluggable queue managers.

---

### 🟢 Good Separation

#### 7. Task Dataclasses (Score: 8/10)
✅ Generic `value`, `preemptive`, `task_type` fields
✅ Not tied to specific schedulers

#### 8. Visualization Layer (Score: 9/10)
✅ Works with any `ScheduleResult`
✅ No scheduler-specific logic

---

## Comparison: Current vs Ideal Architecture

### Current: Monolithic Schedulers
```
┌─────────────────┐
│  RMSScheduler   │  ← Hardwired to periodic tasks
├─────────────────┤  ← Hardwired priority: period-based
│ assign_priority │  ← Hardwired execution: preemptive
│ simulate()      │  ← No value tracking
└─────────────────┘

┌─────────────────┐
│ EDFHVDFScheduler│  ← Hardwired to aperiodic tasks
├─────────────────┤  ← Hardwired priority: EDF+HVDF
│ assign_priority │  ← Reimplements non-preemptive
│ simulate()      │  ← Custom value tracking
└─────────────────┘

RESULT: To add RMS+HVDF, must create new scheduler 
        and duplicate 70% of code from RMS + 30% from HVDF
```

### Ideal: Composable Architecture
```
┌─────────────────────────────────────┐
│      UnifiedScheduler               │
├─────────────────────────────────────┤
│ tasks: List[PeriodicTask |          │
│            AperiodicTask]           │
│                                     │
│ priority_policy: PriorityPolicy     │ ← Pluggable!
│ preemptive_control: PreemptiveCtrl  │ ← Pluggable!
│ value_tracker: ValueTracker         │ ← Pluggable!
│ resource_manager: ResourceMgr       │ ← Pluggable!
└─────────────────────────────────────┘
           ▲
           │
    ┌──────┴──────────────┐
    │                     │
┌───────────┐      ┌──────────────┐
│ EDFPolicy │      │  HVDFPolicy  │
└───────────┘      └──────────────┘
         ▲                ▲
         └────────┬───────┘
          ┌───────▼──────────┐
          │ CompositePolicy  │
          │  (EDF + HVDF)    │
          └──────────────────┘

RESULT: To add RMS+HVDF, just:
        policy = CompositePolicy(RMSPolicy(), HVDFPolicy())
        scheduler = UnifiedScheduler(tasks, policy)
```

---

## Evidence of Hardwiring in Recent Bug

### Bug We Just Fixed
```python
# Line 766 in app.py - ORDER MATTERS!
elif algorithm.startswith("EDF"):  # ← This matched "EDF+HVDF" !!
    scheduler = EDFScheduler(...)

elif algorithm_category == "Aperiodic":  # ← Never reached!
    if "EDF+HVDF" in algorithm:
        scheduler = EDFHVDFScheduler(...)
```

**Root Cause**: String matching in order-dependent if/elif chain.

**Flexible Solution**: 
```python
SCHEDULER_REGISTRY = {
    ("Aperiodic Scheduling", "EDF+HVDF"): EDFHVDFScheduler,
    ("Basic Algorithms", "EDF"): EDFScheduler,
    ("Basic Algorithms", "RMS"): RMSScheduler,
}

scheduler_class = SCHEDULER_REGISTRY.get((category, algorithm))
scheduler = scheduler_class(tasks, duration)
```

---

## Missing Scenarios (Due to Hardwiring)

### Cannot Currently Support:

1. **Mixed Periodic + Aperiodic**
   - Example: RMS for control loops + HVDF for event responses
   - Workaround: None (fundamental limitation)

2. **RMS with HVDF Tie-Breaking**
   - Example: Two tasks with same period, choose by value density
   - Workaround: Create new `RMSHVDFScheduler` (code duplication)

3. **EDF for Periodic, HVDF for Aperiodic**
   - Example: Deadline-driven periodic + value-driven aperiodic
   - Workaround: None

4. **Value Tracking in Existing Schedulers**
   - Example: Track value for RMS-scheduled tasks
   - Workaround: None (no `calculate_total_value()` method)

5. **Per-Task Policies**
   - Example: Task T1 uses RMS, Task T2 uses EDF
   - Workaround: None

---

## Refactoring Roadmap

### Phase 1: Extract Policies (Week 1)
**Goal**: Decouple priority logic from schedulers

**Tasks**:
- [ ] Create `PriorityPolicy` abstract base class
- [ ] Extract `RMSPolicy`, `EDFPolicy`, `DMSPolicy`, `LLFPolicy`, `HVDFPolicy`
- [ ] Add `CompositePolicy` for combining policies
- [ ] Keep existing schedulers as thin wrappers (backward compatibility)

**Benefit**: Can now create RMS+HVDF without new scheduler class.

---

### Phase 2: Behavior Mixins (Week 2)
**Goal**: Reusable components for common features

**Tasks**:
- [ ] Extract `ValueTracking` mixin
- [ ] Extract `PreemptiveControl` mixin
- [ ] Extract `ResourceManagement` mixin
- [ ] Update `SchedulerBase` to use mixins

**Benefit**: All schedulers get value tracking, no code duplication.

---

### Phase 3: Unified Scheduler (Week 3)
**Goal**: Single scheduler supporting all scenarios

**Tasks**:
- [ ] Create `UnifiedScheduler(tasks, policy, mixins)`
- [ ] Support mixed periodic + aperiodic tasks
- [ ] Per-task-type policy assignment
- [ ] Update UI to use unified scheduler with policy selection

**Benefit**: Can simulate any real-world scenario.

---

### Phase 4: Registry Pattern (Week 4)
**Goal**: Self-describing schedulers, no if/elif chain

**Tasks**:
- [ ] Create `SchedulerRegistry`
- [ ] Each scheduler registers itself with metadata
- [ ] UI generates algorithm list from registry
- [ ] Remove 80-line if/elif chain in app.py

**Benefit**: No more order-dependent bugs, easy to add algorithms.

---

## Immediate Quick Win (1 Day)

Add policy-based EDF+HVDF **without major refactoring**:

```python
# New file: scheduler/core/priority_policy.py
class PriorityPolicy(ABC):
    @abstractmethod
    def calculate_priority(self, task_instance, task_values):
        pass

class EDFPolicy(PriorityPolicy):
    def calculate_priority(self, task, values):
        return task.deadline

class HVDFPolicy(PriorityPolicy):
    def calculate_priority(self, task, values):
        v = values.get(task.task_id, 0)
        return -v / task.remaining_time if task.remaining_time > 0 else 0

class CompositePolicy(PriorityPolicy):
    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary
    
    def calculate_priority(self, task, values):
        return (self.primary.calculate_priority(task, values),
                self.secondary.calculate_priority(task, values))

# Usage in EDFHVDFScheduler:
self.policy = CompositePolicy(EDFPolicy(), HVDFPolicy())

def get_next_task(self, ready_queue):
    return min(ready_queue, 
               key=lambda t: self.policy.calculate_priority(t, self.task_values))
```

This enables RMS+HVDF in 10 lines:
```python
rms_hvdf_policy = CompositePolicy(RMSPolicy(), HVDFPolicy())
```

---

## Conclusion

**Your intuition is correct**: The system is **highly hardwired** (35/100 flexibility score).

**Good news**: The task model and visualization are well-separated.

**Bad news**: Schedulers are monolithic, making mixed scenarios impossible.

**Recommended action**: 
1. **Short-term** (this week): Extract policies for EDF+HVDF to enable reuse
2. **Medium-term** (next month): Refactor to mixin-based architecture
3. **Long-term** (3 months): Full unified scheduler with plugin system

**Trade-off**: Current system works for 19 isolated algorithms. To support mixed scenarios, we need architectural changes. The refactoring is justified if you need:
- Mixed periodic + aperiodic workloads
- Policy combinations (RMS+HVDF, EDF+HVDF for different task types)
- Custom scheduling research (easy to add new policies)

Let me know if you want to proceed with Phase 1 refactoring or stay with current architecture.


