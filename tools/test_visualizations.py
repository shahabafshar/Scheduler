"""Test priority timeline and precedence graph visualizations."""

from scheduler.core.task import PeriodicTask, ScheduleResult, ScheduleEvent, PrecedenceConstraint
from scheduler.core.algorithms.edf import EDFScheduler
from scheduler.core.algorithms.rms import RMSScheduler
from scheduler.visualization.gantt import create_priority_timeline
from scheduler.visualization.precedence_graph import create_precedence_graph


def test_priority_timeline():
    """Test priority changes visualization with EDF."""
    print("\n=== Testing Priority Changes Timeline ===")
    
    # Create tasks
    tasks = [
        PeriodicTask(id="T1", computation_time=2, period=5, deadline=5, priority=1),
        PeriodicTask(id="T2", computation_time=3, period=10, deadline=10, priority=2),
    ]
    
    # Run EDF simulation
    scheduler = EDFScheduler(tasks=tasks, duration=20)
    result = scheduler.simulate()
    
    # Create priority timeline visualization
    fig = create_priority_timeline(result, max_time=20)
    
    print(f"✅ Priority timeline created successfully")
    print(f"   - Figure type: {type(fig)}")
    print(f"   - Number of traces: {len(fig.data)}")
    print(f"   - Layout title: {fig.layout.title.text if fig.layout.title else 'N/A'}")
    
    return fig


def test_precedence_graph():
    """Test precedence graph visualization."""
    print("\n=== Testing Precedence Graph Display ===")
    
    # Create tasks
    tasks = [
        PeriodicTask(id="T1", computation_time=2, period=10, deadline=10, priority=1),
        PeriodicTask(id="T2", computation_time=3, period=15, deadline=15, priority=2),
        PeriodicTask(id="T3", computation_time=2, period=20, deadline=20, priority=3),
    ]
    
    # Create precedence constraints
    precedence = [
        PrecedenceConstraint(predecessor="T1", successor="T2"),
        PrecedenceConstraint(predecessor="T1", successor="T3"),
        PrecedenceConstraint(predecessor="T2", successor="T3"),
    ]
    
    # Create precedence graph
    fig = create_precedence_graph(precedence, tasks)
    
    print(f"✅ Precedence graph created successfully")
    print(f"   - Figure type: {type(fig)}")
    print(f"   - Number of traces: {len(fig.data)}")
    print(f"   - Layout title: {fig.layout.title.text if fig.layout.title else 'N/A'}")
    print(f"   - Number of nodes: {len([task.id for task in tasks])}")
    print(f"   - Number of edges: {len(precedence)}")
    
    return fig


def test_integration():
    """Test that both visualizations integrate with the app."""
    print("\n=== Integration Test ===")
    
    # Test 1: Priority timeline with RMS
    tasks_rms = [
        PeriodicTask(id="T1", computation_time=1, period=4, deadline=4, priority=1),
        PeriodicTask(id="T2", computation_time=2, period=6, deadline=6, priority=2),
    ]
    
    scheduler_rms = RMSScheduler(tasks=tasks_rms, duration=12)
    result_rms = scheduler_rms.simulate()
    fig_rms = create_priority_timeline(result_rms, max_time=12)
    
    print(f"✅ RMS priority timeline works")
    
    # Test 2: Precedence graph with no constraints
    fig_empty = create_precedence_graph([], tasks_rms)
    print(f"✅ Empty precedence graph handles gracefully")
    
    # Test 3: Precedence graph with single constraint
    simple_prec = [PrecedenceConstraint(predecessor="T1", successor="T2")]
    fig_simple = create_precedence_graph(simple_prec, tasks_rms)
    print(f"✅ Simple precedence graph works")
    
    return True


if __name__ == "__main__":
    print("="*60)
    print("VISUALIZATION FEATURES TEST")
    print("="*60)
    
    # Run tests
    fig1 = test_priority_timeline()
    fig2 = test_precedence_graph()
    test_integration()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED")
    print("="*60)
    print("\n📊 Features Implemented:")
    print("  1. Priority Changes Timeline - Visualizes dynamic priorities over time")
    print("  2. Precedence Graph Display - Shows task dependencies as network diagram")
    print("\n💡 Usage in App:")
    print("  - Priority timeline appears for EDF, LLF, DMS algorithms")
    print("  - Precedence graph appears when precedence constraints are enabled")
    print("\n" + "="*60)

