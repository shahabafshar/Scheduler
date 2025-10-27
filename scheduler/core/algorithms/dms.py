"""Deadline Monotonic Scheduling (DMS) algorithm."""

from typing import List, Optional
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, ScheduleResult


class DMSScheduler(SchedulerBase):
    """
    Deadline Monotonic Scheduling (DMS).
    
    Priority assignment: smaller relative deadline = higher priority
    DMS is a generalization of RMS for tasks where D_i ≤ P_i.
    """
    
    def assign_priorities(self) -> None:
        """Assign priorities based on relative deadlines (DMS)."""
        # Sort tasks by relative deadline (ascending)
        sorted_tasks = sorted(self.tasks, key=lambda t: t.deadline)
        
        # Assign priorities: smaller deadline = higher priority
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """
        Select task with highest priority from ready queue.
        
        Args:
            ready_queue: List of ready task instances
            
        Returns:
            Highest priority task instance, or None if queue is empty
        """
        if not ready_queue:
            return None
        
        # Return task with highest priority (already sorted by base class)
        return ready_queue[0]
    
    def simulate(self) -> ScheduleResult:
        """Run DMS simulation."""
        # Assign priorities first
        self.assign_priorities()
        
        # Run base simulation
        return super().simulate()

