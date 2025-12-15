"""Test EDF+HVDF scheduler with exam question."""

from scheduler.core.task import AperiodicTask
from scheduler.core.algorithms.edf_hvdf import EDFHVDFScheduler, calculate_value_density


def test_value_density_calculation():
    """Test value density calculation."""
    from scheduler.core.task import TaskInstance
    from typing import Dict
    
    # Create task instance
    instance = TaskInstance(
        task_id='T1',
        instance_number=0,
        arrival_time=0,
        deadline=8,
        remaining_time=3
    )
    
    # Test value density
    task_values = {'T1': 3.0}
    vd = calculate_value_density(instance, task_values)
    assert vd == 1.0, f"Expected 1.0, got {vd}"
    
    instance.remaining_time = 2
    vd = calculate_value_density(instance, task_values)
    assert vd == 1.5, f"Expected 1.5, got {vd}"
    
    print("✅ Value density calculation test passed")


def test_edf_hvdf_question():
    """Test EDF+HVDF with the exact exam question."""
    print("\n=== Testing EDF+HVDF with Exam Question ===")
    
    # Create tasks from exam question
    tasks = [
        AperiodicTask(id='T1', arrival_time=0, computation_time=3, deadline=8, value=3, preemptive=False),
        AperiodicTask(id='T2', arrival_time=0, computation_time=1, deadline=4, value=1, preemptive=False),
        AperiodicTask(id='T3', arrival_time=0, computation_time=1, deadline=4, value=2, preemptive=False),
        AperiodicTask(id='T4', arrival_time=0, computation_time=2, deadline=6, value=3, preemptive=False),
    ]
    
    print("\nTasks:")
    for task in tasks:
        print(f"  {task.id}: C={task.computation_time}, D={task.deadline}, V={task.value}, VD={task.value/task.computation_time:.1f}")
    
    # Create scheduler and run
    scheduler = EDFHVDFScheduler(aperiodic_tasks=tasks, duration=10)
    result = scheduler.simulate()
    
    print(f"\nTimeline events ({len(result.events)} events):")
    for event in result.events[:20]:  # Show first 20
        print(f"  {event}")
    
    # Calculate total value
    total_value = scheduler.calculate_total_value()
    
    print(f"\nCompleted tasks: {len(scheduler.completed_tasks)}")
    for inst in scheduler.completed_tasks:
        task = next(t for t in tasks if t.id == inst.task_id)
        met_deadline = inst.completion_time <= inst.deadline
        value_contributed = task.value if met_deadline else 0
        print(f"  {inst.task_id}: completed={inst.completion_time}, deadline={inst.deadline}, "
              f"status={'✓' if met_deadline else '✗'}, value={value_contributed}")
    
    print(f"\nTotal Value Obtained: {total_value}")
    print(f"Deadline Misses: {len(result.deadline_misses)}")
    print(f"CPU Utilization: {result.cpu_utilization:.1f}%")
    
    # Expected results based on EDF+HVDF:
    # T2 and T3 tie at D=4, T3 has higher VD (2.0 vs 1.0) -> T3 first
    # Expected schedule: T3(0-1), T2(1-2), T4(2-4), T1(4-7)
    # All tasks meet deadlines: T1(7<8), T2(2<4), T3(1<4), T4(4<6)
    # Total value = 3 + 1 + 2 + 3 = 9
    
    # Verify results
    assert total_value == 9.0, f"Expected total_value=9, got {total_value}"
    assert len(result.deadline_misses) == 0, f"Expected no deadline misses, got {len(result.deadline_misses)}"
    
    print("\n✅ All assertions passed!")


def test_edf_hvdf_preemptive():
    """Test EDF+HVDF with preemptive tasks."""
    print("\n=== Testing EDF+HVDF with Preemptive Mode ===")
    
    tasks = [
        AperiodicTask(id='T1', arrival_time=0, computation_time=2, deadline=10, value=5, preemptive=True),
        AperiodicTask(id='T2', arrival_time=0, computation_time=3, deadline=5, value=3, preemptive=True),
    ]
    
    scheduler = EDFHVDFScheduler(aperiodic_tasks=tasks, duration=8)
    result = scheduler.simulate()
    
    total_value = scheduler.calculate_total_value()
    
    print(f"Total Value: {total_value}")
    print(f"Deadline Misses: {len(result.deadline_misses)}")
    
    # T2 has earlier deadline (5 < 10), should be scheduled first
    # Preemptive execution: T2 should complete first, then T1
    assert len(result.deadline_misses) == 0, "Expected no deadline misses"
    
    print("✅ Preemptive mode test passed")


def test_tie_breaking():
    """Test HVDF tie-breaking when deadlines are equal."""
    print("\n=== Testing HVDF Tie-Breaking ===")
    
    # Two tasks with same deadline, different value densities
    tasks = [
        AperiodicTask(id='T1', arrival_time=0, computation_time=4, deadline=8, value=4, preemptive=False),  # VD=1.0
        AperiodicTask(id='T2', arrival_time=0, computation_time=2, deadline=8, value=4, preemptive=False),  # VD=2.0
    ]
    
    scheduler = EDFHVDFScheduler(aperiodic_tasks=tasks, duration=8)
    result = scheduler.simulate()
    
    # T2 should execute first (higher value density)
    # Check execution order in timeline
    execution_order = [evt.task_id for evt in result.events if evt.event_type == 'start' and evt.task_id]
    
    print(f"Execution order: {execution_order}")
    
    if len(execution_order) >= 1:
        # T2 should execute first
        assert execution_order[0] == 'T2', f"Expected T2 first, got {execution_order[0]}"
    
    print("✅ Tie-breaking test passed")


if __name__ == "__main__":
    print("="*60)
    print("EDF+HVDF SCHEDULER TEST SUITE")
    print("="*60)
    
    try:
        test_value_density_calculation()
        test_tie_breaking()
        test_edf_hvdf_preemptive()
        test_edf_hvdf_question()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

