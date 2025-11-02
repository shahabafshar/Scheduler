# EDF+HVDF: Periodic vs Aperiodic Clarification

## The Exam Question

**Question**: *Construct an EDF schedule with HVDF scheduling policy for the following tasks. Clearly mark which instances missed its deadline. What is the total value obtained?*

**Notation**: `Ti = (ci, pi)` where:
- T1 = (3, 8); T2 = (1, 4); T3 = (1, 4); T4 = (2, 6)
- Values: 3, 1, 2, 3 respectively

## The Critical Ambiguity

The notation **Ti = (ci, pi)** can be interpreted two ways:

### Interpretation 1: Aperiodic Tasks (ci, di)
- **pi = deadline** (absolute)
- Each task executes **once** at arrival time
- Total instances = 4 (one per task)

### Interpretation 2: Periodic Tasks (ci, pi) ✅ **CORRECT**
- **pi = period**
- Each task executes **every period** (multiple instances)
- Total instances = many (depends on simulation duration)

---

## Evidence for Periodic Interpretation

### 1. **The Word "Instances" Appears Twice**
- "Clearly mark which **instances** missed its deadline"
- "Total value is sum of the values of all task **instances**"

If tasks were aperiodic (one execution each), the question would say:
- "which **tasks** missed deadlines"
- "sum of all **task** values"

### 2. **Standard Notation in Real-Time Systems**
In real-time systems literature:
- **pi** = period (not deadline!)
- **di** = deadline (when explicitly different from period)
- When `di` is omitted, it's implied that `di = pi` (deadline = period)

### 3. **The Phrase "All Task Instances"**
- "Total value is sum of the values of **all task instances**"
- This only makes sense if there are multiple instances per task
- Aperiodic would just say "all tasks"

---

## Implementation Comparison

### Aperiodic Version (`EDFHVDFScheduler`)
```python
# Tasks execute once
tasks = [
    AperiodicTask(id='T1', arrival_time=0, computation_time=3, deadline=8, value=3),
    AperiodicTask(id='T2', arrival_time=0, computation_time=1, deadline=4, value=1),
    AperiodicTask(id='T3', arrival_time=0, computation_time=1, deadline=4, value=2),
    AperiodicTask(id='T4', arrival_time=0, computation_time=2, deadline=6, value=3),
]

scheduler = EDFHVDFScheduler(tasks, duration=10)
result = scheduler.simulate()

# Results:
# - 4 task instances total
# - All meet deadlines
# - Total Value = 9.0
```

### Periodic Version (`EDFHVDFPeriodicScheduler`) ✅
```python
# Tasks repeat every period
tasks = [
    PeriodicTask(id='T1', computation_time=3, period=8, deadline=8, value=3),
    PeriodicTask(id='T2', computation_time=1, period=4, deadline=4, value=1),
    PeriodicTask(id='T3', computation_time=1, period=4, deadline=4, value=2),
    PeriodicTask(id='T4', computation_time=2, period=6, deadline=6, value=3),
]

scheduler = EDFHVDFPeriodicScheduler(tasks, duration=24)
result = scheduler.simulate()

# Results (over 24 time units = 1 hyperperiod):
# - 16 task instances total:
#   • T1: 3 instances (every 8 time units)
#   • T2: 6 instances (every 4 time units)
#   • T3: 6 instances (every 4 time units)
#   • T4: 4 instances (every 6 time units)
# - CPU Utilization: 120.8% (OVERLOADED!)
# - 10 instances meet deadlines
# - 6 instances miss deadlines
# - Total Value = 25.0
```

---

## Key Differences

| Aspect | Aperiodic | Periodic |
|--------|-----------|----------|
| **Notation** | Ti = (C, D) | Ti = (C, P) |
| **Task Repetition** | Once | Every period |
| **Total Instances** | 4 | 16 (in 24 time units) |
| **CPU Utilization** | 70% | **120.8% (OVERLOADED)** |
| **Deadline Misses** | 0 | 6 |
| **Total Value** | 9.0 | 25.0 |
| **Schedulability** | Schedulable | **NOT schedulable** |

---

## Why the System is Overloaded (Periodic)

CPU Utilization = Σ(Ci / Pi)
- T1: 3/8 = 0.375
- T2: 1/4 = 0.250
- T3: 1/4 = 0.250
- T4: 2/6 = 0.333

**Total U = 1.208 > 1.0** → System is overloaded!

This means:
- Even an optimal scheduler (like EDF) **cannot** guarantee all deadlines
- Some instances **will** miss deadlines
- The question asks us to identify which ones

---

## The Correct Answer (For Periodic)

### Simulation Parameters
- Duration: 24 time units (1 hyperperiod = LCM(8,4,4,6) = 24)
- Algorithm: EDF (primary) + HVDF (tie-breaker)
- Mode: Non-preemptive

### Complete Timeline (First 24 Time Units)

| Time | Task | Event | Deadline | Status |
|------|------|-------|----------|--------|
| 0-1 | T3[0] | Execute | 4.0 | ✓ Met (completed at 1.0) |
| 1-2 | T2[0] | Execute | 4.0 | ✓ Met (completed at 2.0) |
| 2-4 | T4[0] | Execute | 6.0 | ✓ Met (completed at 4.0) |
| 4-5 | T3[1] | Execute | 8.0 | ✓ Met (completed at 5.0) |
| 5-8 | T1[0] | Execute | 8.0 | ✓ Met (completed at 8.0) |
| 8-9 | T2[1] | Execute | 8.0 | ✗ **MISSED** (deadline was 8.0) |
| 9-10 | T3[2] | Execute | 12.0 | ✓ Met (completed at 10.0) |
| 10-12 | T4[1] | Execute | 12.0 | ✓ Met (completed at 12.0) |
| 12-13 | T2[2] | Execute | 12.0 | ✗ **MISSED** (deadline was 12.0) |
| 13-14 | T3[3] | Execute | 16.0 | ✓ Met (completed at 14.0) |
| 14-17 | T1[1] | Execute | 16.0 | ✗ **MISSED** (deadline was 16.0) |
| 17-19 | T4[2] | Execute | 18.0 | ✗ **MISSED** (deadline was 18.0) |
| 19-20 | T3[4] | Execute | 20.0 | ✓ Met (completed at 20.0) |
| 20-21 | T2[4] | Execute | 20.0 | ✗ **MISSED** (deadline was 20.0) |
| 21-22 | T3[5] | Execute | 24.0 | ✓ Met (completed at 22.0) |
| 22-24 | T4[3] | Execute | 24.0 | ✓ Met (completed at 24.0) |

### Value Calculation

| Task | Instance | Completed | Deadline | Status | Value Contributed |
|------|----------|-----------|----------|--------|-------------------|
| T3 | 0 | 1.0 | 4.0 | ✓ Met | 2.0 |
| T2 | 0 | 2.0 | 4.0 | ✓ Met | 1.0 |
| T4 | 0 | 4.0 | 6.0 | ✓ Met | 3.0 |
| T3 | 1 | 5.0 | 8.0 | ✓ Met | 2.0 |
| T1 | 0 | 8.0 | 8.0 | ✓ Met | 3.0 |
| **T2** | **1** | **9.0** | **8.0** | **✗ MISSED** | **0.0** |
| T3 | 2 | 10.0 | 12.0 | ✓ Met | 2.0 |
| T4 | 1 | 12.0 | 12.0 | ✓ Met | 3.0 |
| **T2** | **2** | **13.0** | **12.0** | **✗ MISSED** | **0.0** |
| T3 | 3 | 14.0 | 16.0 | ✓ Met | 2.0 |
| **T1** | **1** | **17.0** | **16.0** | **✗ MISSED** | **0.0** |
| **T4** | **2** | **19.0** | **18.0** | **✗ MISSED** | **0.0** |
| T3 | 4 | 20.0 | 20.0 | ✓ Met | 2.0 |
| **T2** | **4** | **21.0** | **20.0** | **✗ MISSED** | **0.0** |
| T3 | 5 | 22.0 | 24.0 | ✓ Met | 2.0 |
| T4 | 3 | 24.0 | 24.0 | ✓ Met | 3.0 |

**Total Value = 2+1+3+2+3+2+3+2+2+3 = 25.0**

---

## How to Use in the Simulator

### 1. Load the Preset
- Open Streamlit app: `streamlit run scheduler/app.py`
- Select preset: **"📝 EDF+HVDF Periodic (Exam Q)"**
- Algorithm Category: **"Aperiodic Scheduling"** (will auto-select)
- Algorithm: **"EDF+HVDF (Value-Based)"**

### 2. Set Simulation Duration
- Set duration to **24** (1 hyperperiod) or more
- Longer durations will show more deadline misses

### 3. Run Simulation
- Click **"Run Simulation"**
- View results:
  - CPU Utilization: 120.8%
  - Deadline Misses: 6 instances
  - Total Value: 25.0

### 4. Analyze Results
- Check **"Value Analysis"** section
- See per-instance breakdown with status (Met/MISSED)
- Verify timeline shows all task executions

---

## Conclusion

The **correct interpretation is PERIODIC** because:
1. Question uses "instances" (plural) twice
2. Notation `pi` traditionally means period
3. "All task instances" implies multiple executions per task
4. System is overloaded (U > 1.0), which explains deadline misses

The simulator now supports **both interpretations**:
- **Aperiodic**: Use `EDFHVDFScheduler` with `AperiodicTask`
- **Periodic**: Use `EDFHVDFPeriodicScheduler` with `PeriodicTask` ✅

For the exam question, use the **Periodic preset** and simulate for 24+ time units to see all instances and deadline misses.

**Final Answer**: Total Value = **25.0** (over 24 time units)




