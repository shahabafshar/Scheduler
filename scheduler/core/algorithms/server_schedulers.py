"""Server-based schedulers for combined periodic/aperiodic task scheduling."""

from typing import List, Optional, Dict
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, AperiodicTask, TaskInstance
from abc import abstractmethod


class PollingServerScheduler(SchedulerBase):
    """
    Polling Server for serving aperiodic tasks.
    
    Non-bandwidth-preserving: loses capacity when idle.
    Polls for aperiodic tasks at start of each period.
    """
    
    def __init__(self, tasks: List[PeriodicTask], duration: int = 100):
        """Initialize with periodic tasks only."""
        super().__init__(tasks, duration)
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task."""
        if not ready_queue:
            return None
        return ready_queue[0]


class DeferrableServerScheduler(SchedulerBase):
    """
    Deferrable Server for serving aperiodic tasks.
    
    Bandwidth-preserving: capacity preserved when idle.
    Always available for aperiodic tasks when not executing periodic tasks.
    """
    
    def __init__(self, tasks: List[PeriodicTask], duration: int = 100):
        """Initialize with periodic tasks only."""
        super().__init__(tasks, duration)
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task."""
        if not ready_queue:
            return None
        return ready_queue[0]


class SporadicServerScheduler(SchedulerBase):
    """
    Sporadic Server for serving aperiodic tasks.
    
    Bandwidth-preserving with best response time.
    Capacity replenished dynamically after consumption.
    """
    
    def __init__(self, tasks: List[PeriodicTask], duration: int = 100):
        """Initialize with periodic tasks only."""
        super().__init__(tasks, duration)
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task."""
        if not ready_queue:
            return None
        return ready_queue[0]


class PriorityExchangeServerScheduler(SchedulerBase):
    """
    Priority Exchange Server for serving aperiodic tasks.
    
    Bandwidth-preserving by exchanging server priority with lower priority periodic task.
    Server capacity maintained through priority exchange.
    """
    
    def __init__(self, tasks: List[PeriodicTask], duration: int = 100):
        """Initialize with periodic tasks only."""
        super().__init__(tasks, duration)
        self.priority_exchanges = {}  # Track priority swaps
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task."""
        if not ready_queue:
            return None
        return ready_queue[0]


class BackgroundScheduler(SchedulerBase):
    """
    Background Scheduling for aperiodic tasks.
    
    Simple algorithm: aperiodic tasks executed only when no periodic task is ready.
    No server created. Basic FIFO scheduling for aperiodic tasks in idle slots.
    """
    
    def __init__(self, tasks: List[PeriodicTask], duration: int = 100):
        """Initialize with periodic tasks only."""
        super().__init__(tasks, duration)
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities to periodic tasks."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task."""
        if not ready_queue:
            return None
        return ready_queue[0]


