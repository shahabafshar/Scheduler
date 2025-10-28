"""Preset task configurations from documentation."""

from scheduler.core.task import PeriodicTask, AperiodicTask

# RMS Example 1: T1=(2,4), T2=(1,8) - Schedulable (U=0.625)
RMS_EXAMPLE_1 = [
    PeriodicTask(id="T1", computation_time=2.0, period=4.0, deadline=4.0),
    PeriodicTask(id="T2", computation_time=1.0, period=8.0, deadline=8.0)
]

# RMS Example 2: Needs completion time test
RMS_EXAMPLE_2 = [
    PeriodicTask(id="T1", computation_time=2.0, period=4.0, deadline=4.0),
    PeriodicTask(id="T2", computation_time=4.0, period=8.0, deadline=8.0)
]

# RMS Example 3: Larger task set
RMS_EXAMPLE_3 = [
    PeriodicTask(id="T1", computation_time=2.0, period=8.0, deadline=8.0),
    PeriodicTask(id="T2", computation_time=4.0, period=12.0, deadline=12.0),
    PeriodicTask(id="T3", computation_time=2.0, period=6.0, deadline=6.0)
]

# EDF Example: Can achieve 100% utilization
EDF_EXAMPLE = [
    PeriodicTask(id="T1", computation_time=1.0, period=3.0, deadline=3.0),
    PeriodicTask(id="T2", computation_time=4.0, period=6.0, deadline=6.0)
]

# DMS Example with different deadlines
DMS_EXAMPLE = [
    PeriodicTask(id="T1", computation_time=3.0, period=20.0, deadline=7.0),
    PeriodicTask(id="T2", computation_time=2.0, period=5.0, deadline=4.0),
    PeriodicTask(id="T3", computation_time=2.0, period=10.0, deadline=9.0)
]

# Completion Time Test Example
COMPLETION_TIME_TEST = [
    PeriodicTask(id="T1", computation_time=20.0, period=100.0, deadline=100.0),
    PeriodicTask(id="T2", computation_time=30.0, period=145.0, deadline=145.0),
    PeriodicTask(id="T3", computation_time=68.0, period=150.0, deadline=150.0)
]

# Harmonic Task Set Example (all periods are multiples)
HARMONIC_EXAMPLE = [
    PeriodicTask(id="T1", computation_time=1.0, period=4.0, deadline=4.0),
    PeriodicTask(id="T2", computation_time=2.0, period=8.0, deadline=8.0),
    PeriodicTask(id="T3", computation_time=3.0, period=16.0, deadline=16.0)
]

# High Utilization Example (near 100%)
HIGH_UTILIZATION = [
    PeriodicTask(id="T1", computation_time=4.0, period=5.0, deadline=5.0),
    PeriodicTask(id="T2", computation_time=3.0, period=6.0, deadline=6.0),
    PeriodicTask(id="T3", computation_time=2.0, period=10.0, deadline=10.0)
]

# Overload Example (will miss deadlines)
OVERLOAD_EXAMPLE = [
    PeriodicTask(id="T1", computation_time=6.0, period=7.0, deadline=7.0),
    PeriodicTask(id="T2", computation_time=4.0, period=5.0, deadline=5.0)
]

# EDF+HVDF Example (Exam Question): T1=(C=3,D=8,V=3), T2=(C=1,D=4,V=1), T3=(C=1,D=4,V=2), T4=(C=2,D=6,V=3)
EDF_HVDF_EXAMPLE = [
    AperiodicTask(id="T1", arrival_time=0, computation_time=3, deadline=8, value=3, preemptive=False),
    AperiodicTask(id="T2", arrival_time=0, computation_time=1, deadline=4, value=1, preemptive=False),
    AperiodicTask(id="T3", arrival_time=0, computation_time=1, deadline=4, value=2, preemptive=False),
    AperiodicTask(id="T4", arrival_time=0, computation_time=2, deadline=6, value=3, preemptive=False),
]

PRESETS = {
    "RMS Example 1 (Schedulable)": RMS_EXAMPLE_1,
    "RMS Example 2 (Needs Exact Test)": RMS_EXAMPLE_2,
    "RMS Example 3 (3 tasks)": RMS_EXAMPLE_3,
    "EDF (100% Util Possible)": EDF_EXAMPLE,
    "DMS (Different Deadlines)": DMS_EXAMPLE,
    "Completion Time Test": COMPLETION_TIME_TEST,
    "Harmonic Task Set": HARMONIC_EXAMPLE,
    "High Utilization (90%+)": HIGH_UTILIZATION,
    "Overload Scenario": OVERLOAD_EXAMPLE,
    "📝 EDF+HVDF Exam Question (Value=9)": EDF_HVDF_EXAMPLE
}

