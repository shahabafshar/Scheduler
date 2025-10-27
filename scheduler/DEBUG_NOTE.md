# Debug Notes - Simulation Issues Identified

## Problem Summary

The RMS simulation was producing irrational results:
- CPU utilization > 100% (impossible)
- Timeline events out of order
- Possible event duplication issues

## Root Causes Identified

1. **CPU Utilization Calculation Error**: Was counting events instead of actual execution time
2. **Event Recording**: Creating duplicate events or recording at wrong times
3. **Instance Management**: May be creating incorrect instance numbers

## Test Case: RMS Example 1

Expected from documentation:
- T1=(2,4), T2=(1,8)
- Utilization = 2/4 + 1/8 = 0.625 (62.5%)
- Should be schedulable
- T2 is higher priority (smaller period = 8 vs 4)

Correct schedule for first 8 time units:
- t=0: T1 starts (C=2, but will be preempted)
- t=2: T1 completes (if no preemption)
- Actually: T2 arrives at t=0 with P=8, T1 arrives at t=0 with P=4
- Higher priority (T1 with P=4) should run first

Wait - T1 has period=4, T2 has period=8
In RMS, smaller period = higher priority
So T1 is higher priority and should preempt T2

Expected timeline:
- t=0: T1 arrives and starts (T1 P=4, higher priority)
- t=2: T1 completes (C=2)
- t=2: T2 arrives and starts (only task ready)
- t=3: T2 completes (C=1)
- t=4: T1 arrives again
- etc.

Current output shows:
- CPU Util: 85% (should be 62.5%)
- Timeline events out of order (t=3.00 comes before t=2.00)

## Fixes Applied

1. Changed CPU utilization to track `total_execution_time` instead of counting events
2. Simplified simulation loop to avoid duplicate event recording
3. Added proper instance counter tracking

## Remaining Issues

The timeline still shows some issues. Need to:
1. Verify task priority assignment in RMS
2. Check timeline event ordering
3. Ensure no duplicate events

