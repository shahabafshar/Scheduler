"""Rate Monotonic Scheduling (RMS) algorithm."""

from typing import List, Optional
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, ScheduleResult


class RMSScheduler(SchedulerBase):
    """
    Rate Monotonic Scheduling (RMS).
    
    Priority assignment: smaller period = higher priority
    RMS is optimal for fixed-priority preemptive scheduling of periodic tasks.
    """
    
    def assign_priorities(self) -> None:
        """Assign priorities based on periods (RMS)."""
        # Sort tasks by period (ascending), with task ID as tie-breaker for determinism
        # When periods are equal, lower task ID gets higher priority (consistent ordering)
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.period, t.id))

        # Assign priorities: smaller period = higher priority
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
        """Run RMS simulation."""
        # Assign priorities first
        self.assign_priorities()
        
        # Run base simulation
        return super().simulate()

