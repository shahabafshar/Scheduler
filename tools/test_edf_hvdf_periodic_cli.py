"""Command-line test for EDF+HVDF PERIODIC scheduler."""

from scheduler.core.task import PeriodicTask
from scheduler.core.algorithms.edf_hvdf_periodic import EDFHVDFPeriodicScheduler

def main():
    print("=" * 70)
    print("EDF+HVDF PERIODIC SCHEDULER TEST")
    print("=" * 70)
    
    # Create PERIODIC tasks: Ti = (C, P)
    # T1 = (3, 8): C=3, P=8, D=8 (implicit), Value=3
    # T2 = (1, 4): C=1, P=4, D=4, Value=1
    # T3 = (1, 4): C=1, P=4, D=4, Value=2
    # T4 = (2, 6): C=2, P=6, D=6, Value=3
    
    tasks = [
        PeriodicTask(id='T1', computation_time=3, period=8, deadline=8, value=3, preemptive=False, task_type='periodic'),
        PeriodicTask(id='T2', computation_time=1, period=4, deadline=4, value=1, preemptive=False, task_type='periodic'),
        PeriodicTask(id='T3', computation_time=1, period=4, deadline=4, value=2, preemptive=False, task_type='periodic'),
        PeriodicTask(id='T4', computation_time=2, period=6, deadline=6, value=3, preemptive=False, task_type='periodic'),
    ]
    
    print("\nInput Tasks (PERIODIC):")
    print("-" * 70)
    print(f"{'Task':<6} {'C':<5} {'P':<5} {'D':<5} {'Value':<7} {'VD':<7} {'Preemptive'}")
    print("-" * 70)
    for task in tasks:
        vd = task.value / task.computation_time
        print(f"{task.id:<6} {task.computation_time:<5.0f} {task.period:<5.0f} {task.deadline:<5.0f} {task.value:<7.0f} {vd:<7.2f} {task.preemptive}")
    
    print("\nCPU Utilization Check:")
    print("-" * 70)
    total_util = sum(t.computation_time / t.period for t in tasks)
    print(f"U = Σ(C/P) = {total_util:.3f}")
    if total_util <= 1.0:
        print("✓ U ≤ 1.0 - Potentially schedulable")
    else:
        print("✗ U > 1.0 - System overload!")
    
    # Run simulation for multiple hyperperiods
    # LCM(8, 4, 4, 6) = 24, so simulate at least 24 time units
    duration = 24
    print(f"\nSimulation Duration: {duration} time units (1 hyperperiod)")
    print("-" * 70)
    
    scheduler = EDFHVDFPeriodicScheduler(periodic_tasks=tasks, duration=duration)
    result = scheduler.simulate()
    
    print("\n" + "=" * 70)
    print("SIMULATION RESULTS")
    print("=" * 70)
    
    print(f"\nTotal Events: {len(result.events)}")
    print(f"CPU Utilization: {result.cpu_utilization:.1f}%")
    print(f"Context Switches: {result.total_context_switches}")
    print(f"Deadline Misses: {len(result.deadline_misses)}")
    
    # Show all events
    print("\nComplete Timeline:")
    print("-" * 70)
    for i, event in enumerate(result.events, 1):
        if event.task_id:
            instance = event.details.get('instance', '?')
            print(f"{i:3}. t={event.time:5.1f} | {event.task_id}[{instance}] | {event.event_type}")
        else:
            print(f"{i:3}. t={event.time:5.1f} | IDLE       | {event.event_type}")
    
    # Show completed instances
    print("\n" + "=" * 70)
    print("COMPLETED INSTANCES")
    print("=" * 70)
    breakdown = scheduler.get_value_breakdown()
    
    if breakdown:
        print(f"\n{'Task':<8} {'Inst':<6} {'Completed':<12} {'Deadline':<10} {'Status':<10} {'Value'}")
        print("-" * 70)
        for item in breakdown:
            status = "✓ MET" if item['met_deadline'] else "✗ MISSED"
            print(f"{item['task_id']:<8} {item['instance']:<6} {item['completion_time']:<12.1f} "
                  f"{item['deadline']:<10.1f} {status:<10} {item['value']:.1f}")
    else:
        print("No instances completed!")
    
    # Show deadline misses
    if result.deadline_misses:
        print("\n" + "=" * 70)
        print("DEADLINE MISSES")
        print("=" * 70)
        for miss in result.deadline_misses:
            print(f"  {miss.task_id}[{miss.instance_number}]: deadline={miss.deadline}")
    
    # Total value
    print("\n" + "=" * 70)
    total_value = scheduler.calculate_total_value()
    print(f"TOTAL VALUE (All Instances): {total_value:.1f}")
    print("=" * 70)
    
    # Expected instances in 24 time units:
    print("\nExpected Instances:")
    print("-" * 70)
    for task in tasks:
        num_instances = int(duration / task.period)
        expected_value = task.value * num_instances
        print(f"  {task.id}: {num_instances} instances × {task.value} value = {expected_value} total")
    
    expected_total = sum(task.value * int(duration / task.period) for task in tasks)
    print(f"\nExpected Total Value (if all meet deadlines): {expected_total}")
    
    # Verification
    print("\n" + "=" * 70)
    if len(result.deadline_misses) == 0 and total_value == expected_total:
        print("✅ TEST PASSED!")
        print(f"   All {len(breakdown)} instances met deadlines")
        print(f"   Total value: {total_value} (as expected)")
    else:
        print("⚠️  TEST RESULTS:")
        print(f"   Deadline misses: {len(result.deadline_misses)}")
        print(f"   Actual value: {total_value}")
        print(f"   Expected value: {expected_total}")
    print("=" * 70)

if __name__ == "__main__":
    main()


