"""Least Laxity First (LLF) Scheduling algorithm."""

from typing import List, Optional
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, ScheduleResult


class LLFScheduler(SchedulerBase):
    """
    Least Laxity First (LLF) Scheduling.
    
    Priority assignment: smaller laxity = higher priority
    Laxity = deadline - current_time - remaining_computation_time
    LLF has the same schedulability as EDF but uses dynamic priority by laxity.
    """
    
    def assign_priorities(self) -> None:
        """LLF doesn't use fixed priorities."""
        # LLF uses dynamic priorities based on laxity
        # Set all priorities to 0 initially
        for task in self.tasks:
            task.priority = 0
    
    def calculate_laxity(self, instance: TaskInstance, current_time: float) -> float:
        """
        Calculate laxity for a task instance.
        
        Laxity = d_i - (t + c_i')
        where:
        - d_i: deadline
        - t: current time
        - c_i': remaining computation time
        
        Args:
            instance: Task instance
            current_time: Current simulation time
            
        Returns:
            Laxity value (smaller = higher priority)
        """
        laxity = instance.deadline - current_time - instance.remaining_time
        return max(0, laxity)  # Ensure non-negative laxity
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """
        Select task with smallest laxity (highest priority).
        
        Args:
            ready_queue: List of ready task instances
            
        Returns:
            Task instance with smallest laxity, or None if queue is empty
        """
        if not ready_queue:
            return None
        
        # Return task with smallest laxity
        # Note: Base class passes current_time through self.current_time
        return min(ready_queue, key=lambda t: self.calculate_laxity(t, self.current_time))
    
    def process_time_unit(self, time: float) -> None:
        """Process time unit (current_time updated in base class)."""
        return super().process_time_unit(time)
    
    def simulate(self) -> ScheduleResult:
        """Run LLF simulation."""
        # Assign priorities first
        self.assign_priorities()
        
        # Run base simulation
        return super().simulate()
