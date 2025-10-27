"""Overload handling algorithms: Imprecise computation, HVDF, and (m,k)-firm."""

from typing import List, Optional, Dict
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, ImpreciseTask, MkFirmTask


class ImpreciseComputationScheduler(SchedulerBase):
    """
    Imprecise computation scheduler.
    
    Tasks have mandatory and optional parts.
    During overload, optional parts may be skipped.
    """
    
    def __init__(self, tasks: List[PeriodicTask], imprecise_tasks: List[ImpreciseTask],
                 duration: int = 100):
        """
        Initialize imprecise computation scheduler.
        
        Args:
            tasks: Regular periodic tasks
            imprecise_tasks: Tasks with mandatory/optional parts
            duration: Simulation duration
        """
        self.imprecise_tasks = imprecise_tasks
        self.task_mandatory_times = {t.id: t.mandatory_time for t in imprecise_tasks}
        self.task_optional_times = {t.id: t.optional_time for t in imprecise_tasks}
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
    
    def is_overloaded(self, time: float) -> bool:
        """Check if system is overloaded based on current workload."""
        # Simple heuristic: if ready queue is consistently full
        return len(self.ready_queue) > len(self.tasks)


class HVDFScheduler(SchedulerBase):
    """
    Highest Value Density First (HVDF) scheduler.
    
    For best-effort scheduling under overload.
    Priority = Value / Computation_time (value density)
    """
    
    def __init__(self, tasks: List[PeriodicTask], task_values: Dict[str, float],
                 duration: int = 100):
        """
        Initialize HVDF scheduler.
        
        Args:
            tasks: Regular periodic tasks
            task_values: Mapping of task_id -> value
            duration: Simulation duration
        """
        self.task_values = task_values
        super().__init__(tasks, duration)
    
    def assign_priorities(self) -> None:
        """Assign priorities based on value density."""
        for task in self.tasks:
            value = self.task_values.get(task.id, 0.0)
            if task.computation_time > 0:
                value_density = value / task.computation_time
                # Use value density as priority (higher = better)
                task.priority = int(value_density * 1000)  # Scale for integer priority
            else:
                task.priority = 0
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select task with highest value density."""
        if not ready_queue:
            return None
        # Ready queue is already sorted by priority (value density)
        return ready_queue[0]


class MkFirmScheduler(SchedulerBase):
    """
    (m,k)-firm task scheduler.
    
    At least m out of k consecutive task instances must meet their deadlines.
    """
    
    def __init__(self, tasks: List[PeriodicTask], mk_tasks: List[MkFirmTask],
                 duration: int = 100):
        """
        Initialize (m,k)-firm scheduler.
        
        Args:
            tasks: Regular periodic tasks
            mk_tasks: (m,k)-firm task specifications
            duration: Simulation duration
        """
        self.mk_tasks = {t.id: t for t in mk_tasks}
        self.task_history = {tid: [] for tid in mk_tasks}  # Track deadline meets
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
    
    def check_mk_constraint(self, task_id: str) -> bool:
        """
        Check if (m,k) constraint is satisfied.
        
        Returns True if at least m out of last k instances met deadline.
        """
        if task_id not in self.mk_tasks:
            return True  # Not an (m,k) task
        
        mk_task = self.mk_tasks[task_id]
        history = self.task_history.get(task_id, [])
        
        if len(history) < mk_task.k:
            return True  # Not enough history yet
        
        # Check last k instances
        last_k = history[-mk_task.k:]
        meets_count = sum(1 for met in last_k if met)
        
        return meets_count >= mk_task.m
    
    def record_deadline_result(self, task_id: str, met_deadline: bool):
        """Record whether a task instance met its deadline."""
        if task_id in self.mk_tasks:
            history = self.task_history.get(task_id, [])
            history.append(met_deadline)
            self.task_history[task_id] = history[-self.mk_tasks[task_id].k:]  # Keep only last k

