"""Test suite for priority policy framework."""

from scheduler.core.task import TaskInstance
from scheduler.core.priority_policy import (
    RMSPolicy, EDFPolicy, DMSPolicy, LLFPolicy, HVDFPolicy,
    CompositePriorityPolicy, FixedPriorityPolicy
)


def test_rms_policy():
    """Test RMS: shorter period = higher priority."""
    task_periods = {'T1': 10.0, 'T2': 5.0, 'T3': 20.0}
    policy = RMSPolicy(task_periods)
    
    t1 = TaskInstance('T1', 0, 0, 10, 2)
    t2 = TaskInstance('T2', 0, 0, 5, 1)
    t3 = TaskInstance('T3', 0, 0, 20, 3)
    
    # T2 has shortest period (5), should have lowest priority value
    assert policy.calculate_priority(t2) < policy.calculate_priority(t1)
    assert policy.calculate_priority(t1) < policy.calculate_priority(t3)
    assert policy.name() == "RMS (Rate Monotonic)"


def test_edf_policy():
    """Test EDF: earlier deadline = higher priority."""
    policy = EDFPolicy()
    
    t1 = TaskInstance('T1', 0, 0, 10, 2)
    t2 = TaskInstance('T2', 0, 0, 5, 1)
    t3 = TaskInstance('T3', 0, 0, 15, 3)
    
    # T2 has earliest deadline (5), should have lowest priority value
    assert policy.calculate_priority(t2) < policy.calculate_priority(t1)
    assert policy.calculate_priority(t1) < policy.calculate_priority(t3)
    assert policy.name() == "EDF (Earliest Deadline First)"


def test_llf_policy():
    """Test LLF: lower laxity = higher priority."""
    policy = LLFPolicy(current_time=0.0)
    
    # Laxity = deadline - current_time - remaining_time
    t1 = TaskInstance('T1', 0, 0, 10, 2)  # Laxity = 10 - 0 - 2 = 8
    t2 = TaskInstance('T2', 0, 0, 5, 3)   # Laxity = 5 - 0 - 3 = 2
    t3 = TaskInstance('T3', 0, 0, 15, 5)  # Laxity = 15 - 0 - 5 = 10
    
    # T2 has lowest laxity (2), should have lowest priority value
    assert policy.calculate_priority(t2) < policy.calculate_priority(t1)
    assert policy.calculate_priority(t1) < policy.calculate_priority(t3)
    
    # Update current time
    policy.current_time = 5.0
    # Laxity recalculated: T1 = 10-5-2=3, T2 = 5-5-3=-3, T3 = 15-5-5=5
    assert policy.calculate_priority(t2) < policy.calculate_priority(t1)


def test_hvdf_policy():
    """Test HVDF: higher value density = higher priority."""
    task_values = {'T1': 10.0, 'T2': 6.0, 'T3': 15.0}
    policy = HVDFPolicy(task_values)
    
    t1 = TaskInstance('T1', 0, 0, 10, 2)  # VD = 10/2 = 5.0
    t2 = TaskInstance('T2', 0, 0, 5, 1)   # VD = 6/1 = 6.0
    t3 = TaskInstance('T3', 0, 0, 15, 5)  # VD = 15/5 = 3.0
    
    # T2 has highest value density (6.0), should have lowest priority value (negated)
    assert policy.calculate_priority(t2) < policy.calculate_priority(t1)
    assert policy.calculate_priority(t1) < policy.calculate_priority(t3)


def test_composite_policy_edf_hvdf():
    """Test composite policy: EDF primary, HVDF tie-breaker."""
    task_values = {'T1': 10.0, 'T2': 20.0, 'T3': 5.0}
    
    edf = EDFPolicy()
    hvdf = HVDFPolicy(task_values)
    policy = CompositePriorityPolicy(edf, hvdf)
    
    # T2 and T3 have same deadline (10), but T2 has higher value density
    t1 = TaskInstance('T1', 0, 0, 5, 2)   # Deadline=5
    t2 = TaskInstance('T2', 0, 0, 10, 2)  # Deadline=10, VD=20/2=10
    t3 = TaskInstance('T3', 0, 0, 10, 1)  # Deadline=10, VD=5/1=5
    
    p1 = policy.calculate_priority(t1)
    p2 = policy.calculate_priority(t2)
    p3 = policy.calculate_priority(t3)
    
    # T1 has earliest deadline, should be first
    assert p1 < p2
    assert p1 < p3
    
    # T2 and T3 tie on deadline, but T2 has higher VD, so should be scheduled before T3
    assert p2 < p3
    
    assert "EDF" in policy.name() and "HVDF" in policy.name()


def test_composite_policy_rms_hvdf():
    """Test composite policy: RMS primary, HVDF tie-breaker."""
    task_periods = {'T1': 10.0, 'T2': 10.0, 'T3': 20.0}
    task_values = {'T1': 5.0, 'T2': 15.0, 'T3': 10.0}
    
    rms = RMSPolicy(task_periods)
    hvdf = HVDFPolicy(task_values)
    policy = CompositePriorityPolicy(rms, hvdf)
    
    # T1 and T2 have same period (10), but T2 has higher value density
    t1 = TaskInstance('T1', 0, 0, 10, 2)  # Period=10, VD=5/2=2.5
    t2 = TaskInstance('T2', 0, 0, 10, 2)  # Period=10, VD=15/2=7.5
    t3 = TaskInstance('T3', 0, 0, 20, 5)  # Period=20
    
    p1 = policy.calculate_priority(t1)
    p2 = policy.calculate_priority(t2)
    p3 = policy.calculate_priority(t3)
    
    # T1 and T2 have same period, both should be before T3
    assert p1[0] < p3[0]  # Check primary (RMS)
    assert p2[0] < p3[0]
    
    # T2 has higher value density than T1, so should be scheduled first
    assert p2 < p1


def test_fixed_priority_policy():
    """Test fixed priority assignment."""
    task_priorities = {'T1': 1, 'T2': 3, 'T3': 2}
    policy = FixedPriorityPolicy(task_priorities)
    
    t1 = TaskInstance('T1', 0, 0, 10, 2)
    t2 = TaskInstance('T2', 0, 0, 5, 1)
    t3 = TaskInstance('T3', 0, 0, 15, 3)
    
    # T1 has priority 1 (highest), T3 has 2, T2 has 3 (lowest)
    assert policy.calculate_priority(t1) < policy.calculate_priority(t3)
    assert policy.calculate_priority(t3) < policy.calculate_priority(t2)


def test_unknown_task_handling():
    """Test that policies handle unknown tasks gracefully."""
    task_periods = {'T1': 10.0}
    policy = RMSPolicy(task_periods)
    
    unknown_task = TaskInstance('T_UNKNOWN', 0, 0, 10, 2)
    
    # Should return inf for unknown tasks
    assert policy.calculate_priority(unknown_task) == float('inf')


def test_zero_remaining_time_hvdf():
    """Test HVDF with zero remaining time."""
    task_values = {'T1': 10.0}
    policy = HVDFPolicy(task_values)
    
    t1 = TaskInstance('T1', 0, 0, 10, 0)  # Zero remaining time
    
    # Should return inf (lowest priority) for zero remaining time
    assert policy.calculate_priority(t1) == float('inf')


if __name__ == "__main__":
    print("=" * 60)
    print("PRIORITY POLICY TEST SUITE")
    print("=" * 60)
    
    test_rms_policy()
    print("✅ RMS Policy")
    
    test_edf_policy()
    print("✅ EDF Policy")
    
    test_llf_policy()
    print("✅ LLF Policy")
    
    test_hvdf_policy()
    print("✅ HVDF Policy")
    
    test_composite_policy_edf_hvdf()
    print("✅ Composite EDF+HVDF Policy")
    
    test_composite_policy_rms_hvdf()
    print("✅ Composite RMS+HVDF Policy")
    
    test_fixed_priority_policy()
    print("✅ Fixed Priority Policy")
    
    test_unknown_task_handling()
    print("✅ Unknown Task Handling")
    
    test_zero_remaining_time_hvdf()
    print("✅ Zero Remaining Time (HVDF)")
    
    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)

