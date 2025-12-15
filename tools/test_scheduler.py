"""Simple test script to verify scheduler functionality."""

from scheduler.core.task import PeriodicTask
from scheduler.core.algorithms.rms import RMSScheduler
from scheduler.core.analysis.schedulability import SchedulabilityAnalyzer

# Test with RMS Example 1 from documentation
print("=== RMS Example 1: T1=(2,4), T2=(1,8) ===")

tasks = [
    PeriodicTask(id="T1", computation_time=2.0, period=4.0, deadline=4.0),
    PeriodicTask(id="T2", computation_time=1.0, period=8.0, deadline=8.0)
]

# Schedulability Analysis
print("\nSchedulability Analysis:")
results = SchedulabilityAnalyzer.analyze_rms(tasks)
print(results['utilization_test']['explanation'])

# Run Simulation
print("\nRunning Simulation...")
scheduler = RMSScheduler(tasks, duration=20)
result = scheduler.simulate()

print(f"\nResults:")
print(f"  CPU Utilization: {result.cpu_utilization:.1%}")
print(f"  Context Switches: {result.total_context_switches}")
print(f"  Deadline Misses: {len(result.deadline_misses)}")
print(f"  Is Schedulable: {'Yes' if result.is_schedulable else 'No'}")

print("\nFirst 20 Timeline Events:")
for event in result.events[:20]:
    print(f"  {event}")

