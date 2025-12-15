"""Command-line test for EDF+HVDF scheduler - Direct debugging."""

from scheduler.core.task import AperiodicTask
from scheduler.core.algorithms.edf_hvdf import EDFHVDFScheduler

def main():
    print("=" * 60)
    print("EDF+HVDF SCHEDULER - COMMAND LINE TEST")
    print("=" * 60)
    
    # Create the exact tasks from the exam question
    tasks = [
        AperiodicTask(id='T1', arrival_time=0, computation_time=3, deadline=8, value=3, preemptive=False, task_type='aperiodic'),
        AperiodicTask(id='T2', arrival_time=0, computation_time=1, deadline=4, value=1, preemptive=False, task_type='aperiodic'),
        AperiodicTask(id='T3', arrival_time=0, computation_time=1, deadline=4, value=2, preemptive=False, task_type='aperiodic'),
        AperiodicTask(id='T4', arrival_time=0, computation_time=2, deadline=6, value=3, preemptive=False, task_type='aperiodic'),
    ]
    
    print("\nInput Tasks:")
    print("-" * 60)
    for task in tasks:
        vd = task.value / task.computation_time
        print(f"{task.id}: arrival={task.arrival_time}, C={task.computation_time}, D={task.deadline}, V={task.value}, VD={vd:.2f}, preemptive={task.preemptive}")
    
    # Create scheduler
    print("\nCreating scheduler...")
    scheduler = EDFHVDFScheduler(aperiodic_tasks=tasks, duration=10)
    
    # Run simulation
    print("\nRunning simulation...")
    result = scheduler.simulate()
    
    # Display results
    print("\n" + "=" * 60)
    print("SIMULATION RESULTS")
    print("=" * 60)
    
    print(f"\nTotal events: {len(result.events)}")
    print(f"CPU Utilization: {result.cpu_utilization:.1f}%")
    print(f"Context Switches: {result.total_context_switches}")
    print(f"Deadline Misses: {len(result.deadline_misses)}")
    
    # Timeline
    print("\nTimeline (first 20 events):")
    print("-" * 60)
    for i, event in enumerate(result.events[:20]):
        print(f"{i+1}. t={event.time:.1f}, task={event.task_id}, event={event.event_type}")
    
    if len(result.events) > 20:
        print(f"... and {len(result.events) - 20} more events")
    
    # Completed tasks
    print("\nCompleted Tasks:")
    print("-" * 60)
    if scheduler.completed_tasks:
        for task_inst in scheduler.completed_tasks:
            original_task = next((t for t in tasks if t.id == task_inst.task_id), None)
            if original_task:
                met_deadline = task_inst.completion_time <= task_inst.deadline
                status = "✓ MET" if met_deadline else "✗ MISSED"
                value_contrib = original_task.value if met_deadline else 0
                print(f"{task_inst.task_id}: completed at t={task_inst.completion_time:.1f}, deadline={task_inst.deadline:.1f} - {status} (value={value_contrib})")
    else:
        print("No tasks completed!")
    
    # Total value
    print("\n" + "=" * 60)
    total_value = scheduler.calculate_total_value()
    print(f"TOTAL VALUE: {total_value:.1f}")
    print("=" * 60)
    
    # Expected results
    print("\nExpected Results:")
    print("- Execution order: T3(0-1), T2(1-2), T4(2-4), T1(4-7)")
    print("- All tasks meet deadlines")
    print("- Total value: 9.0")
    
    # Verify
    print("\n" + "=" * 60)
    if total_value == 9.0 and len(result.deadline_misses) == 0:
        print("✅ TEST PASSED!")
    else:
        print("❌ TEST FAILED!")
        print(f"   Expected: value=9.0, misses=0")
        print(f"   Got: value={total_value:.1f}, misses={len(result.deadline_misses)}")
    print("=" * 60)

if __name__ == "__main__":
    main()

