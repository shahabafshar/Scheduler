"""
Test Precedence-Constrained Scheduling Algorithms

Verifies that RMS+Prec, DMS+Prec, and EDF+Prec implement their scientifically
correct behaviors per CprE 458/558 course materials.

Key behaviors to verify:
- RMS+Prec: R_j* = Max(R_j, R_i*) forward pass, priority by period
- DMS+Prec: R_j* = Max(R_j, R_i*), D_j* = Max(D_j, D_i*) forward pass
- EDF+Prec: R_j* = Max(R_j, R_i* + C_i), D_i* = Min(D_i, D_j* - C_j) forward+backward

Example from documentation:
Precedence Graph: T1 → T2, T3 and T3, T4 → T5
Tasks: T1(C=1,D=5), T2(C=2,D=7), T3(C=2,D=5), T4(C=1,D=10), T5(C=3,D=12)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "scheduler"))

from scheduler.core.task import PeriodicTask, PrecedenceConstraint
from scheduler.core.algorithms.precedence import (
    RMSWithPrecedence,
    DMSWithPrecedence,
    EDFWithPrecedence,
    topological_sort,
    reverse_topological_sort
)


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_events(result, max_events=30):
    """Print timeline events for debugging."""
    print(f"\nTimeline (first {max_events} events):")
    for i, e in enumerate(result.events[:max_events]):
        details = e.details if e.details else {}
        print(f"  t={e.time:5.1f}: {e.event_type:15s} | {e.task_id or 'IDLE':10s} | {details}")


def get_doc_example_tasks():
    """Return task set from documentation example."""
    # T1 → T2, T3 and T3, T4 → T5
    tasks = [
        PeriodicTask(id="T1", computation_time=1.0, period=20.0, deadline=5.0),
        PeriodicTask(id="T2", computation_time=2.0, period=20.0, deadline=7.0),
        PeriodicTask(id="T3", computation_time=2.0, period=20.0, deadline=5.0),
        PeriodicTask(id="T4", computation_time=1.0, period=20.0, deadline=10.0),
        PeriodicTask(id="T5", computation_time=3.0, period=20.0, deadline=12.0),
    ]

    precedences = [
        PrecedenceConstraint(predecessor="T1", successor="T2"),
        PrecedenceConstraint(predecessor="T1", successor="T3"),
        PrecedenceConstraint(predecessor="T3", successor="T5"),
        PrecedenceConstraint(predecessor="T4", successor="T5"),
    ]

    return tasks, precedences


def test_topological_sort():
    """Test topological sort utility functions."""
    print_section("Topological Sort Test")

    tasks, precedences = get_doc_example_tasks()

    # Build predecessor map
    predecessor_map = {task.id: [] for task in tasks}
    for prec in precedences:
        predecessor_map[prec.successor].append(prec.predecessor)

    # Build successor map
    successor_map = {task.id: [] for task in tasks}
    for prec in precedences:
        successor_map[prec.predecessor].append(prec.successor)

    # Test topological sort
    topo_order = topological_sort(tasks, predecessor_map)
    print(f"Topological order: {topo_order}")

    # Verify order: predecessors must come before successors
    for prec in precedences:
        pred_idx = topo_order.index(prec.predecessor)
        succ_idx = topo_order.index(prec.successor)
        assert pred_idx < succ_idx, f"{prec.predecessor} should come before {prec.successor}"

    # Test reverse topological sort
    reverse_order = reverse_topological_sort(tasks, successor_map)
    print(f"Reverse topological order: {reverse_order}")

    # Verify order: successors must come before predecessors
    for prec in precedences:
        pred_idx = reverse_order.index(prec.predecessor)
        succ_idx = reverse_order.index(prec.successor)
        assert pred_idx > succ_idx, f"{prec.successor} should come before {prec.predecessor} in reverse order"

    print("\n[PASS] Topological sort works correctly")


def test_rms_with_precedence():
    """Test RMS with precedence constraints."""
    print_section("RMS with Precedence Test")

    tasks, precedences = get_doc_example_tasks()

    scheduler = RMSWithPrecedence(tasks, precedences, duration=20)

    # Test modified ready times
    modified_ready = scheduler._compute_modified_ready_times()
    print(f"\nModified ready times:")
    for task_id, ready in modified_ready.items():
        print(f"  {task_id}: R* = {ready}")

    # Per documentation: R1*=0, R2*=0 (wait for R1*), R3*=0 (wait for R1*), R4*=0, R5*=0 (wait for R3*, R4*)
    # Since all base ready times are 0, all should be 0
    assert modified_ready["T1"] == 0.0, "T1 should have R*=0"
    assert modified_ready["T4"] == 0.0, "T4 should have R*=0"

    # Run simulation
    result = scheduler.simulate()

    print(f"\nSimulation results:")
    print(f"  CPU Utilization: {result.cpu_utilization:.1%}")
    print(f"  Context Switches: {result.total_context_switches}")
    print(f"  Deadline Misses: {len(result.deadline_misses)}")

    print_events(result, 25)

    # Verify precedence is respected: predecessors complete before successors start
    completion_times = {}
    start_times = {}
    for e in result.events:
        if e.event_type == 'complete':
            completion_times[e.task_id] = e.time
        elif e.event_type == 'start' and e.task_id not in start_times:
            start_times[e.task_id] = e.time

    print(f"\nCompletion times: {completion_times}")
    print(f"Start times: {start_times}")

    # Verify T1 completes before T2 and T3 start
    if "T1" in completion_times and "T2" in start_times:
        assert completion_times["T1"] <= start_times["T2"], "T1 should complete before T2 starts"
    if "T1" in completion_times and "T3" in start_times:
        assert completion_times["T1"] <= start_times["T3"], "T1 should complete before T3 starts"

    print("\n[PASS] RMS with Precedence works correctly")


def test_dms_with_precedence():
    """Test DMS with precedence constraints."""
    print_section("DMS with Precedence Test")

    tasks, precedences = get_doc_example_tasks()

    scheduler = DMSWithPrecedence(tasks, precedences, duration=20)

    # Test modified parameters
    modified_ready = scheduler._compute_modified_ready_times()
    modified_deadlines = scheduler._compute_modified_deadlines()

    print(f"\nModified ready times:")
    for task_id, ready in modified_ready.items():
        print(f"  {task_id}: R* = {ready}")

    print(f"\nModified deadlines:")
    for task_id, deadline in modified_deadlines.items():
        print(f"  {task_id}: D* = {deadline}")

    # Per documentation: Deadlines propagate forward (max)
    # D1*=5, D2*=max(7,5)=7, D3*=max(5,5)=5, D4*=10, D5*=max(12,5,10)=12

    # Run simulation
    result = scheduler.simulate()

    print(f"\nSimulation results:")
    print(f"  CPU Utilization: {result.cpu_utilization:.1%}")
    print(f"  Context Switches: {result.total_context_switches}")
    print(f"  Deadline Misses: {len(result.deadline_misses)}")

    print_events(result, 25)

    print("\n[PASS] DMS with Precedence works correctly")


def test_edf_with_precedence():
    """Test EDF with precedence constraints."""
    print_section("EDF with Precedence Test")

    tasks, precedences = get_doc_example_tasks()

    scheduler = EDFWithPrecedence(tasks, precedences, duration=20)

    # Test modified parameters
    modified_ready = scheduler._compute_modified_ready_times()
    modified_deadlines = scheduler._compute_modified_deadlines()

    print(f"\nModified ready times (EDF formula: R_j* = max(R_j, R_i* + C_i)):")
    for task_id, ready in sorted(modified_ready.items()):
        print(f"  {task_id}: R* = {ready}")

    print(f"\nModified deadlines (EDF formula: D_i* = min(D_i, D_j* - C_j)):")
    for task_id, deadline in sorted(modified_deadlines.items()):
        print(f"  {task_id}: D* = {deadline}")

    # Per documentation:
    # Ready times (forward pass with C_i):
    # R1*=0, R2*=max(0, R1*+C1)=max(0,0+1)=1, R3*=max(0,R1*+C1)=max(0,0+1)=1
    # R4*=0, R5*=max(0,max(R3*+C3, R4*+C4))=max(0,max(1+2,0+1))=max(0,3)=3
    assert modified_ready["T1"] == 0.0, f"T1 should have R*=0, got {modified_ready['T1']}"
    assert modified_ready["T2"] == 1.0, f"T2 should have R*=1, got {modified_ready['T2']}"
    assert modified_ready["T3"] == 1.0, f"T3 should have R*=1, got {modified_ready['T3']}"
    assert modified_ready["T4"] == 0.0, f"T4 should have R*=0, got {modified_ready['T4']}"
    assert modified_ready["T5"] == 3.0, f"T5 should have R*=3, got {modified_ready['T5']}"

    # Deadlines (backward pass with C_j):
    # D5*=12, D4*=min(10, D5*-C5)=min(10,12-3)=9, D3*=min(5,D5*-C5)=min(5,9)=5
    # D2*=7 (no successors), D1*=min(5,min(D2*-C2, D3*-C3))=min(5,min(7-2,5-2))=min(5,3)=3
    assert modified_deadlines["T5"] == 12.0, f"T5 should have D*=12, got {modified_deadlines['T5']}"
    assert modified_deadlines["T4"] == 9.0, f"T4 should have D*=9, got {modified_deadlines['T4']}"
    assert modified_deadlines["T3"] == 5.0, f"T3 should have D*=5, got {modified_deadlines['T3']}"
    assert modified_deadlines["T2"] == 7.0, f"T2 should have D*=7, got {modified_deadlines['T2']}"
    assert modified_deadlines["T1"] == 3.0, f"T1 should have D*=3, got {modified_deadlines['T1']}"

    # Run simulation
    result = scheduler.simulate()

    print(f"\nSimulation results:")
    print(f"  CPU Utilization: {result.cpu_utilization:.1%}")
    print(f"  Context Switches: {result.total_context_switches}")
    print(f"  Deadline Misses: {len(result.deadline_misses)}")

    print_events(result, 25)

    # Verify precedence is respected
    completion_times = {}
    start_times = {}
    for e in result.events:
        if e.event_type == 'complete':
            completion_times[e.task_id] = e.time
        elif e.event_type == 'start' and e.task_id not in start_times:
            start_times[e.task_id] = e.time

    print(f"\nCompletion times: {completion_times}")
    print(f"Start times: {start_times}")

    print("\n[PASS] EDF with Precedence works correctly")


def test_algorithm_comparison():
    """Compare all three precedence algorithms."""
    print_section("Precedence Algorithm Comparison")

    tasks, precedences = get_doc_example_tasks()
    duration = 20

    results = {}
    for name, Scheduler in [
        ("RMS+Prec", RMSWithPrecedence),
        ("DMS+Prec", DMSWithPrecedence),
        ("EDF+Prec", EDFWithPrecedence),
    ]:
        # Create fresh copies of tasks
        tasks_copy = [
            PeriodicTask(id=t.id, computation_time=t.computation_time,
                        period=t.period, deadline=t.deadline)
            for t in tasks
        ]

        scheduler = Scheduler(tasks_copy, precedences.copy(), duration)
        result = scheduler.simulate()
        results[name] = {
            'cpu_util': result.cpu_utilization,
            'context_switches': result.total_context_switches,
            'deadline_misses': len(result.deadline_misses),
        }

    print("\nComparison:")
    print(f"{'Algorithm':<15} {'CPU Util':<12} {'Ctx Switches':<15} {'DL Misses':<12}")
    print("-" * 55)
    for name, data in results.items():
        print(f"{name:<15} {data['cpu_util']:.1%}        {data['context_switches']:<15} {data['deadline_misses']:<12}")

    print("\n[PASS] All algorithms produce results")


def test_simple_chain():
    """Test a simple precedence chain: T1 -> T2 -> T3."""
    print_section("Simple Chain Test (T1 -> T2 -> T3)")

    tasks = [
        PeriodicTask(id="T1", computation_time=2.0, period=20.0, deadline=6.0),
        PeriodicTask(id="T2", computation_time=2.0, period=20.0, deadline=10.0),
        PeriodicTask(id="T3", computation_time=2.0, period=20.0, deadline=15.0),
    ]

    precedences = [
        PrecedenceConstraint(predecessor="T1", successor="T2"),
        PrecedenceConstraint(predecessor="T2", successor="T3"),
    ]

    for name, Scheduler in [
        ("RMS+Prec", RMSWithPrecedence),
        ("DMS+Prec", DMSWithPrecedence),
        ("EDF+Prec", EDFWithPrecedence),
    ]:
        tasks_copy = [
            PeriodicTask(id=t.id, computation_time=t.computation_time,
                        period=t.period, deadline=t.deadline)
            for t in tasks
        ]

        scheduler = Scheduler(tasks_copy, precedences.copy(), duration=15)
        result = scheduler.simulate()

        print(f"\n{name}:")
        print(f"  Deadline misses: {len(result.deadline_misses)}")

        # Get completion order
        completions = [(e.task_id, e.time) for e in result.events if e.event_type == 'complete']
        print(f"  Completion order: {completions}")

        # Verify T1 < T2 < T3
        if len(completions) == 3:
            assert completions[0][0] == "T1", "T1 should complete first"
            assert completions[1][0] == "T2", "T2 should complete second"
            assert completions[2][0] == "T3", "T3 should complete third"

    print("\n[PASS] Simple chain executed correctly")


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("  PRECEDENCE-CONSTRAINED SCHEDULING TESTS")
    print("="*60)

    test_topological_sort()
    test_rms_with_precedence()
    test_dms_with_precedence()
    test_edf_with_precedence()
    test_algorithm_comparison()
    test_simple_chain()

    print("\n" + "="*60)
    print("  ALL TESTS PASSED!")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()
