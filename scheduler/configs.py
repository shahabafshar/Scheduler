"""Preset task configurations from documentation."""

from core.task import PeriodicTask

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

PRESETS = {
    "RMS Example 1 (Schedulable)": RMS_EXAMPLE_1,
    "RMS Example 2 (Needs Exact Test)": RMS_EXAMPLE_2,
    "RMS Example 3 (3 tasks)": RMS_EXAMPLE_3,
    "EDF (100% Util Possible)": EDF_EXAMPLE,
    "DMS (Different Deadlines)": DMS_EXAMPLE,
    "Completion Time Test": COMPLETION_TIME_TEST
}

