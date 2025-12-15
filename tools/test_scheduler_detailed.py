"""Detailed test to debug scheduler issues."""

from scheduler.core.task import PeriodicTask
from scheduler.core.algorithms.rms import RMSScheduler

# Test with RMS Example 1 from documentation
print("=== Detailed RMS Test: T1=(2,4), T2=(1,8) ===\n")

tasks = [
    PeriodicTask(id="T1", computation_time=2.0, period=4.0, deadline=4.0),
    PeriodicTask(id="T2", computation_time=1.0, period=8.0, deadline=8.0)
]

# Run Simulation
print("Running Simulation for first 8 time units...\n")
scheduler = RMSScheduler(tasks, duration=8)

# Assign priorities
scheduler.assign_priorities()

# Print assigned priorities
print("Task Priorities:")
for task in scheduler.tasks:
    print(f"  {task.id}: period={task.period}, priority={task.priority}")

# Run simulation
result = scheduler.simulate()

print(f"\nResults:")
print(f"  CPU Utilization: {result.cpu_utilization:.1%}")
print(f"  Context Switches: {result.total_context_switches}")
print(f"  Deadline Misses: {len(result.deadline_misses)}")

print(f"\nTimeline (sorted by time):")
events_sorted = sorted(result.events, key=lambda e: e.time)
for event in events_sorted:
    print(f"  t={event.time:.0f}: {event.task_id or 'IDLE'} - {event.event_type}")

print(f"\nActual execution sequence (what should happen):")
print("""
Expected for t=0 to t=8:
- t=0: T1 arrives (P=4, C=2, higher priority), T2 arrives (P=8, C=1, lower)
- t=0: T1 starts executing
- t=2: T1 completes
- t=2: T2 starts executing (only task ready)
- t=3: T2 completes
- t=3: IDLE
- t=4: T1 arrives (new instance)
- t=4: T1 starts executing
- t=6: T1 completes
- t=6: IDLE
- t=8: T1 arrives, T2 arrives
...

CPU should be busy for: 2 + 1 + 2 = 5 time units out of 8 = 62.5%
""")

