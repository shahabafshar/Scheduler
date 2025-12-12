"""Priority policy framework for flexible scheduling algorithms.

This module provides a composable architecture for defining task priorities,
enabling combinations like RMS+HVDF, EDF+HVDF without duplicating code.
"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
from .task import TaskInstance


class PriorityPolicy(ABC):
    """Base class for all priority policies.
    
    A priority policy calculates a priority value for a task instance.
    Lower priority values indicate higher urgency (earlier scheduling).
    """
    
    @abstractmethod
    def calculate_priority(self, task_instance: TaskInstance, 
                          task_metadata: Optional[Dict] = None) -> float:
        """Calculate priority for a task instance.
        
        Args:
            task_instance: The task instance to prioritize
            task_metadata: Optional metadata (e.g., task values, periods)
            
        Returns:
            Priority value (lower = higher priority)
        """
        pass
    
    @abstractmethod
    def name(self) -> str:
        """Return human-readable name of this policy."""
        pass


class RMSPolicy(PriorityPolicy):
    """Rate Monotonic Scheduling: Priority based on period.
    
    Shorter period = higher priority.
    """
    
    def __init__(self, task_periods: Dict[str, float]):
        """Initialize RMS policy.
        
        Args:
            task_periods: Mapping of task_id -> period
        """
        self.task_periods = task_periods
    
    def calculate_priority(self, task_instance: TaskInstance, 
                          task_metadata: Optional[Dict] = None) -> float:
        """Lower period = higher priority (lower value)."""
        period = self.task_periods.get(task_instance.task_id, float('inf'))
        return period
    
    def name(self) -> str:
        return "RMS (Rate Monotonic)"


class EDFPolicy(PriorityPolicy):
    """Earliest Deadline First: Priority based on absolute deadline.
    
    Earlier deadline = higher priority.
    """
    
    def calculate_priority(self, task_instance: TaskInstance, 
                          task_metadata: Optional[Dict] = None) -> float:
        """Earlier deadline = higher priority (lower value)."""
        return task_instance.deadline
    
    def name(self) -> str:
        return "EDF (Earliest Deadline First)"


class DMSPolicy(PriorityPolicy):
    """Deadline Monotonic Scheduling: Priority based on relative deadline.
    
    Shorter relative deadline = higher priority.
    """
    
    def __init__(self, task_deadlines: Dict[str, float]):
        """Initialize DMS policy.
        
        Args:
            task_deadlines: Mapping of task_id -> relative deadline
        """
        self.task_deadlines = task_deadlines
    
    def calculate_priority(self, task_instance: TaskInstance, 
                          task_metadata: Optional[Dict] = None) -> float:
        """Shorter deadline = higher priority (lower value)."""
        deadline = self.task_deadlines.get(task_instance.task_id, float('inf'))
        return deadline
    
    def name(self) -> str:
        return "DMS (Deadline Monotonic)"


class LLFPolicy(PriorityPolicy):
    """Least Laxity First: Priority based on laxity (slack time).
    
    Laxity = deadline - current_time - remaining_time
    Lower laxity = higher priority.
    """
    
    def __init__(self, current_time: float = 0.0):
        """Initialize LLF policy.
        
        Args:
            current_time: Current simulation time (updated externally)
        """
        self.current_time = current_time
    
    def calculate_priority(self, task_instance: TaskInstance, 
                          task_metadata: Optional[Dict] = None) -> float:
        """Lower laxity = higher priority (lower value)."""
        laxity = task_instance.deadline - self.current_time - task_instance.remaining_time
        return laxity
    
    def name(self) -> str:
        return "LLF (Least Laxity First)"


class HVDFPolicy(PriorityPolicy):
    """Highest Value Density First: Priority based on value per unit time.

    IMPORTANT: Value Density = value / computation_time (INVARIANT)
    This should NOT change during task execution.
    Higher value density = higher priority.
    """

    def __init__(self, task_values: Dict[str, float],
                 task_computation_times: Optional[Dict[str, float]] = None):
        """Initialize HVDF policy.

        Args:
            task_values: Mapping of task_id -> value
            task_computation_times: Mapping of task_id -> original computation time
        """
        self.task_values = task_values
        self.task_computation_times = task_computation_times or {}

    def calculate_priority(self, task_instance: TaskInstance,
                          task_metadata: Optional[Dict] = None) -> float:
        """Higher value density = higher priority (lower value, so negate).

        Uses computation_time (invariant) rather than remaining_time.
        """
        value = self.task_values.get(task_instance.task_id, 0.0)

        # Use original computation_time if available (correct HVDF behavior)
        if task_instance.task_id in self.task_computation_times:
            comp_time = self.task_computation_times[task_instance.task_id]
            if comp_time > 0:
                value_density = value / comp_time
                return -value_density  # Negate so higher density = lower priority value
            return float('inf')

        # Fallback: use remaining_time (incorrect but backward compatible)
        if task_instance.remaining_time > 0:
            value_density = value / task_instance.remaining_time
            return -value_density
        return float('inf')  # No remaining time = lowest priority

    def name(self) -> str:
        return "HVDF (Highest Value Density First)"


class CompositePriorityPolicy(PriorityPolicy):
    """Composite policy: Primary policy with secondary tie-breaker.
    
    Example: EDF+HVDF uses EDF as primary, HVDF breaks ties.
    """
    
    def __init__(self, primary: PriorityPolicy, secondary: PriorityPolicy):
        """Initialize composite policy.
        
        Args:
            primary: Primary priority policy
            secondary: Secondary policy for tie-breaking
        """
        self.primary = primary
        self.secondary = secondary
    
    def calculate_priority(self, task_instance: TaskInstance, 
                          task_metadata: Optional[Dict] = None) -> Tuple[float, float]:
        """Return tuple: (primary_priority, secondary_priority).
        
        Python's tuple comparison naturally handles tie-breaking.
        """
        primary_prio = self.primary.calculate_priority(task_instance, task_metadata)
        secondary_prio = self.secondary.calculate_priority(task_instance, task_metadata)
        return (primary_prio, secondary_prio)
    
    def name(self) -> str:
        return f"{self.primary.name()} + {self.secondary.name()}"


class FixedPriorityPolicy(PriorityPolicy):
    """Fixed priority policy: Uses pre-assigned task priorities.
    
    Useful for systems where priorities are manually configured.
    """
    
    def __init__(self, task_priorities: Dict[str, int]):
        """Initialize fixed priority policy.
        
        Args:
            task_priorities: Mapping of task_id -> priority (lower = higher priority)
        """
        self.task_priorities = task_priorities
    
    def calculate_priority(self, task_instance: TaskInstance, 
                          task_metadata: Optional[Dict] = None) -> float:
        """Use pre-assigned priority."""
        return self.task_priorities.get(task_instance.task_id, float('inf'))
    
    def name(self) -> str:
        return "Fixed Priority"


# Utility function for backward compatibility
def calculate_value_density(task_instance: TaskInstance, task_values: Dict[str, float],
                            task_computation_times: Optional[Dict[str, float]] = None) -> float:
    """Calculate value density for HVDF scheduling.

    IMPORTANT: Value density = value / computation_time (INVARIANT)
    This should NOT change during task execution.

    This is kept for backward compatibility with existing code.
    New code should use HVDFPolicy instead.

    Args:
        task_instance: Task instance to calculate density for
        task_values: Mapping of task_id -> value
        task_computation_times: Mapping of task_id -> original computation time

    Returns:
        Value density (value / computation_time)
    """
    value = task_values.get(task_instance.task_id, 0.0)

    # Use original computation_time if available (correct HVDF behavior)
    if task_computation_times and task_instance.task_id in task_computation_times:
        comp_time = task_computation_times[task_instance.task_id]
        if comp_time > 0:
            return value / comp_time
        return 0.0

    # Fallback: use remaining_time (incorrect but backward compatible)
    if task_instance.remaining_time > 0:
        return value / task_instance.remaining_time
    return 0.0


