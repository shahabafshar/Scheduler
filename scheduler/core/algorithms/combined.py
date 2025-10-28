"""Combined scheduling of periodic and aperiodic tasks using servers."""

from abc import abstractmethod
from typing import List, Optional
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, AperiodicTask, TaskInstance, ScheduleResult, ScheduleEvent
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


class PriorityExchangeServerScheduler(ServerScheduler):
    """
    Priority Exchange Server for combined scheduling.
    
    When aperiodic tasks are unavailable, server exchanges its priority
    with the highest priority periodic task ready for execution.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_base_priority = 0
        self.swapped_with = None  # Task that has server priority
    
    def should_replenish_server(self, time: float) -> bool:
        """Replenish at start of each server period."""
        return time == self.server_next_replenish
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities with priority exchange capability."""
        self.server_base_priority = len(self.tasks)
        self.tasks[-1].priority = self.server_base_priority
        
        periodic_tasks = self.tasks[:-1]
        sorted_tasks = sorted(periodic_tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
        
        self.server_base_priority = self.tasks[-1].priority
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Custom selection with priority exchange."""
        # Get next task using base logic
        next_task = super().get_next_task(ready_queue)
        
        # Implement priority exchange logic
        # When server is ready but has no aperiodic work, exchange with highest priority periodic task
        if next_task and next_task.task_id == "Server" and not self.aperiodic_queue:
            # Exchange server priority with highest priority periodic task
            # Server temporarily gets highest priority periodic task's priority
            periodic_tasks = [t for t in ready_queue if t.task_id != "Server"]
            if periodic_tasks:
                # Find highest priority periodic task
                highest_pri_task = max(periodic_tasks, key=lambda t: t.priority)
                # Exchange priorities
                self.swapped_with = highest_pri_task
                # Make server appear as if it has that priority for this decision
                return highest_pri_task
        
        return next_task


class BackgroundScheduler(SchedulerBase):
    """
    Background Scheduler for aperiodic tasks.
    
    Simple approach: aperiodic tasks execute in idle slots only.
    No dedicated server - just FIFO when CPU is idle.
    """
    
    def __init__(self, tasks: List[PeriodicTask], aperiodic_tasks: List[AperiodicTask], duration: int = 100):
        """Initialize background scheduler."""
        self.aperiodic_tasks = sorted(aperiodic_tasks, key=lambda t: t.arrival_time)
        self.aperiodic_queue = []
        super().__init__(tasks, duration)
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities to periodic tasks."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select next task: periodic if ready, aperiodic if idle."""
        if ready_queue:
            # Periodic task ready - return it
            return ready_queue[0]
        else:
            # Idle - check for aperiodic tasks
            if self.aperiodic_queue:
                return self.aperiodic_queue.pop(0)
        return None
    
    def update_aperiodic_queue(self, time: float) -> None:
        """Add newly arrived aperiodic tasks to queue."""
        for apt in self.aperiodic_tasks:
            if abs(time - apt.arrival_time) < 0.001:
                # Convert AperiodicTask to TaskInstance
                instance = TaskInstance(
                    task_id=f"Aperiodic_{apt.id}",
                    instance_number=0,
                    arrival_time=time,
                    deadline=apt.deadline if hasattr(apt, 'deadline') else time + apt.computation_time * 10,
                    remaining_time=apt.computation_time
                )
                self.aperiodic_queue.append(instance)
        
        # Sort by arrival time (FIFO)
        self.aperiodic_queue.sort(key=lambda t: t.arrival_time)
    
    def simulate(self) -> ScheduleResult:
        """Override simulate to add aperiodic task handling."""
        result = super().simulate()
        
        # Inject aperiodic task arrivals into timeline
        aperiodic_arrivals = []
        for apt in self.aperiodic_tasks:
            aperiodic_arrivals.append(ScheduleEvent(
                time=apt.arrival_time,
                task_id=f"Aperiodic_{apt.id}",
                event_type='start'
            ))
        
        # Merge aperiodic arrivals into timeline
        all_events = list(result.events) + aperiodic_arrivals
        all_events.sort(key=lambda e: e.time)
        result.events = all_events
        
        return result

