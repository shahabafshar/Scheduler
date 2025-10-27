"""Task data models for real-time scheduling."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class PeriodicTask:
    """Periodic task model."""
    id: str
    computation_time: float  # C_i
    period: float            # P_i
    deadline: Optional[float] = None  # D_i (default = period)
    priority: int = -1       # Assigned by algorithm
    
    def __post_init__(self):
        """Set default deadline to period if not specified."""
        if self.deadline is None:
            self.deadline = self.period
            
    @property
    def utilization(self) -> float:
        """Calculate task utilization C_i / P_i."""
        return self.computation_time / self.period if self.period > 0 else 0.0
    
    def __str__(self) -> str:
        return f"Task {self.id}: C={self.computation_time}, P={self.period}, D={self.deadline}"


@dataclass
class AperiodicTask:
    """Aperiodic task model."""
    id: str
    arrival_time: float      # a_i
    computation_time: float  # C_i
    deadline: float          # d_i
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    
    @property
    def response_time(self) -> Optional[float]:
        """Calculate response time if task completed."""
        if self.start_time is not None and self.completion_time is not None:
            return self.completion_time - self.arrival_time
        return None
    
    def __str__(self) -> str:
        return f"Task {self.id}: arrival={self.arrival_time}, C={self.computation_time}, D={self.deadline}"


@dataclass
class ImpreciseTask:
    """Imprecise computation task model."""
    id: str
    mandatory_time: float    # m_i
    optional_time: float     # o_i
    deadline: float
    value: float = 0.0       # For value-based scheduling
    
    @property
    def total_time(self) -> float:
        """Total computation time if fully executed."""
        return self.mandatory_time + self.optional_time
    
    @property
    def value_density(self) -> float:
        """Value density per unit computation time."""
        total = self.total_time
        return self.value / total if total > 0 else 0.0


@dataclass
class MkFirmTask:
    """(m,k)-firm task model."""
    id: str
    computation_time: float  # C x_i + C y_i + C z_i
    period: float
    deadline: float
    mandatory_time: float    # C x_i: before entering critical section
    critical_section_time: float  # C y_i: in critical section
    optional_time: float     # C z_i: after critical section
    m: int                   # m out of k deadlines must be met
    k: int
    
    @property
    def utilization(self) -> float:
        """Calculate task utilization."""
        return self.computation_time / self.period if self.period > 0 else 0.0


@dataclass
class ResourceConstraint:
    """Resource sharing constraint model."""
    resource_id: str
    tasks: List[str]         # Tasks accessing this resource
    critical_sections: Dict[str, float]  # task_id -> CS duration
    priority_ceiling: int = -1
    current_holder: Optional[str] = None
    queue: List[str] = field(default_factory=list)  # Waiting tasks
    
    def lock(self, task_id: str) -> bool:
        """Lock resource for a task."""
        if self.current_holder is None:
            self.current_holder = task_id
            return True
        else:
            if task_id not in self.queue:
                self.queue.append(task_id)
            return False
    
    def unlock(self, task_id: str) -> Optional[str]:
        """Unlock resource and return next waiting task."""
        if self.current_holder == task_id:
            self.current_holder = None
            if self.queue:
                next_task = self.queue.pop(0)
                self.current_holder = next_task
                return next_task
        return None


@dataclass
class PrecedenceConstraint:
    """Precedence relationship between tasks."""
    predecessor: str  # Task that must complete first
    successor: str    # Task that can start after predecessor
    
    def __str__(self) -> str:
        return f"{self.predecessor} → {self.successor}"


@dataclass
class TaskInstance:
    """Instance of a periodic task at a specific time."""
    task_id: str
    instance_number: int
    arrival_time: float
    deadline: float
    remaining_time: float
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    
    def is_active(self, time: float) -> bool:
        """Check if task instance is currently active."""
        if self.completion_time is not None:
            return False
        return time >= self.arrival_time
    
    def is_overdue(self, time: float) -> bool:
        """Check if task instance has missed its deadline."""
        if self.completion_time is not None:
            return self.completion_time > self.deadline
        return time > self.deadline
    
    @property
    def laxity(self) -> float:
        """Calculate current laxity (requires time parameter)."""
        # This would need the current time to calculate properly
        # For now, return 0 as placeholder
        return 0.0


@dataclass
class ScheduleEvent:
    """Event in the scheduling timeline."""
    time: float
    task_id: Optional[str]
    event_type: str  # 'start', 'complete', 'preempt', 'block', 'deadline_miss', 'idle'
    details: Dict[str, any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        task_str = self.task_id if self.task_id else "IDLE"
        return f"t={self.time:.2f}: {task_str} - {self.event_type}"


@dataclass
class ScheduleResult:
    """Results from a scheduling simulation."""
    algorithm: str
    tasks: List[PeriodicTask]
    events: List[ScheduleEvent]
    deadline_misses: List[ScheduleEvent] = field(default_factory=list)
    total_context_switches: int = 0
    cpu_utilization: float = 0.0
    response_times: Dict[str, float] = field(default_factory=dict)
    
    @property
    def is_schedulable(self) -> bool:
        """Check if schedule met all deadlines."""
        return len(self.deadline_misses) == 0
    
    def get_task_utilization(self, task_id: str) -> float:
        """Calculate actual CPU utilization for a specific task."""
        task_execution_time = sum(
            evt.details.get('duration', 0) 
            for evt in self.events 
            if evt.task_id == task_id and evt.event_type == 'complete'
        )
        max_time = max((evt.time for evt in self.events), default=1.0)
        return task_execution_time / max_time if max_time > 0 else 0.0

