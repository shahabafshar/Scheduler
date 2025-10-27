"""Combined scheduling of periodic and aperiodic tasks using servers."""

from abc import abstractmethod
from typing import List, Optional
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, AperiodicTask, TaskInstance, ScheduleResult
import math


class ServerScheduler(SchedulerBase):
    """
    Base class for server-based scheduling algorithms.
    
    Creates a periodic server to handle aperiodic tasks.
    Server types: Polling, Deferrable, Priority Exchange, Sporadic
    """
    
    def __init__(self, tasks: List[PeriodicTask], aperiodic_tasks: List[AperiodicTask], 
                 server_capacity: float, server_period: float, duration: int = 100):
        """
        Initialize server-based scheduler.
        
        Args:
            tasks: Periodic tasks
            aperiodic_tasks: Aperiodic tasks to service
            server_capacity: C_s - computation time for server
            server_period: P_s - period of server
            duration: Simulation duration
        """
        self.aperiodic_tasks = sorted(aperiodic_tasks, key=lambda t: t.arrival_time)
        self.server_capacity = server_capacity
        self.server_period = server_period
        self.server_remaining = server_capacity
        self.server_next_replenish = 0
        self.aperiodic_queue = []
        
        # Create server as a periodic task
        server_task = PeriodicTask(
            id="Server",
            computation_time=server_capacity,
            period=server_period,
            deadline=server_period
        )
        
        super().__init__(tasks + [server_task], duration)
    
    @abstractmethod
    def should_replenish_server(self, time: float) -> bool:
        """Determine if server capacity should be replenished."""
        pass
    
    def update_aperiodic_queue(self, time: float) -> None:
        """Update aperiodic task ready queue."""
        # Add newly arrived aperiodic tasks
        for apt in self.aperiodic_tasks:
            if abs(time - apt.arrival_time) < 0.001:  # Floating point comparison
                self.aperiodic_queue.append(apt)
        
        # Sort by deadline (earliest first)
        self.aperiodic_queue.sort(key=lambda t: t.deadline)


class PollingServerScheduler(ServerScheduler):
    """
    Polling Server for combined scheduling.
    
    Server periodically checks for aperiodic tasks.
    If none available, capacity is lost (non-bandwidth-preserving).
    """
    
    def should_replenish_server(self, time: float) -> bool:
        """Replenish at start of each server period."""
        return time == self.server_next_replenish
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities to all tasks including server."""
        # Server gets highest priority
        self.tasks[-1].priority = len(self.tasks)  # Server is last in list
        
        # Assign RMS priorities to periodic tasks (excluding server)
        periodic_tasks = self.tasks[:-1]
        sorted_tasks = sorted(periodic_tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i


class DeferrableServerScheduler(ServerScheduler):
    """
    Deferrable Server for combined scheduling.
    
    Server preserves its capacity when no aperiodic tasks available.
    Capacity is deferred but replenished periodically.
    """
    
    def should_replenish_server(self, time: float) -> bool:
        """Replenish at start of each server period."""
        return time == self.server_next_replenish
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities."""
        # Server gets highest priority
        self.tasks[-1].priority = len(self.tasks)
        
        periodic_tasks = self.tasks[:-1]
        sorted_tasks = sorted(periodic_tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i


class SporadicServerScheduler(ServerScheduler):
    """
    Sporadic Server for combined scheduling.
    
    Server dynamically replenishes capacity after consumption.
    Best response time among server algorithms.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.consumption_events = []  # Track when capacity is consumed
    
    def should_replenish_server(self, time: float) -> bool:
        """Replenish capacity at current_time + period after consumption."""
        # Replenish at scheduled times
        return time in [event + self.server_period for event in self.consumption_events]
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities."""
        # Server gets highest priority
        self.tasks[-1].priority = len(self.tasks)
        
        periodic_tasks = self.tasks[:-1]
        sorted_tasks = sorted(periodic_tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i

