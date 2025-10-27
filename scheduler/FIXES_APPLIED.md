# Critical Fixes Applied - Simulation Logic

## Problem Summary

The scheduler was producing irrational results:
- **CPU utilization 174%** (impossible!)
- Timeline events out of order
- Duplicate "start" events for the same task

## Root Cause

The simulation loop had the execution order reversed:
1. It was executing the task first
2. Then checking if next_task was different
3. Then starting the new task

This caused the same task to generate multiple "start" events because `self.running_task` was being updated at the wrong time in the loop.

## Fix Applied

Reordered the logic in `scheduler_base.py`:

**Before (incorrect):**
```python
# Execute current task
if self.running_task:
    self.running_task.remaining_time -= 1
    
# Start new task
if next_task and next_task != self.running_task:
    start_event()
    self.running_task = next_task
```

**After (correct):**
```python
# First, start new task if different from current
if next_task and next_task != self.running_task:
    start_event()
    self.running_task = next_task

# Then, execute current task
if self.running_task:
    self.running_task.remaining_time -= 1
```

## Verification

Test results now show correct behavior:
- **CPU Utilization**: 62.5% (matches expected: 2+1+2 = 5 units out of 8)
- **Timeline**: Proper event ordering
- **No duplicate events**
- **Correct task priorities**: T1 (priority=2) preempts T2 (priority=1)

## Expected Behavior (RMS Example 1)

Task set: T1=(2,4), T2=(1,8)
- T1 has period=4, priority=2 (higher)
- T2 has period=8, priority=1 (lower)

Timeline for t=0 to t=8:
- t=0: T1 starts
- t=2: T1 completes (C=2), T2 starts  
- t=3: T2 completes (C=1), IDLE
- t=4: T1 starts (new instance)
- t=6: T1 completes, IDLE
- t=8: T1 and T2 both arrive

This is now correctly simulated! ✅

