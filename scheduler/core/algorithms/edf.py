"""Earliest Deadline First (EDF) Scheduling algorithm."""

from typing import List, Optional
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, ScheduleResult


class EDFScheduler(SchedulerBase):
    """
    Earliest Deadline First (EDF) Scheduling.

    Dynamic priority assignment: smaller absolute deadline = higher priority
    EDF is optimal for preemptive scheduling with dynamic priorities.
    """

    # EDF uses dynamic priority selection, skip redundant base class sorting
    _skip_priority_sort = True

    def assign_priorities(self) -> None:
        """EDF doesn't use fixed priorities."""
        # EDF uses dynamic priorities based on absolute deadline
        # Set all priorities to 0 initially
        for task in self.tasks:
            task.priority = 0
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """
        Select task with earliest absolute deadline.
        
        Args:
            ready_queue: List of ready task instances
            
        Returns:
            Task instance with earliest deadline, or None if queue is empty
        """
        if not ready_queue:
            return None
        
        # Return task with earliest deadline
        return min(ready_queue, key=lambda t: t.deadline)
    
    def simulate(self) -> ScheduleResult:
        """Run EDF simulation."""
        # Assign priorities first
        self.assign_priorities()
        
        # Run base simulation
        return super().simulate()

