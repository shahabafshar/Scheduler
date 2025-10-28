"""Resource-aware scheduler base class with protocol support."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from .task import PeriodicTask, TaskInstance, ScheduleEvent, ScheduleResult, ResourceConstraint
from .protocols.priority_inheritance import PriorityInheritanceProtocol
from .protocols.priority_ceiling import PriorityCeilingProtocol


class ResourceAwareSchedulerBase(ABC):
    """
    Base scheduler with resource sharing and protocol support.
    
    Extends the basic scheduler to handle:
    - Resource requests and releases
    - Critical section blocking
    - Priority inheritance (PIP)
    - Priority ceiling protocol (PCP)
    """
    
    def __init__(self, tasks: List[PeriodicTask], duration: int = 100,
                 resources: Optional[List[ResourceConstraint]] = None,
                 protocol: str = "none"):
        """
        Initialize resource-aware scheduler.
        
        Args:
            tasks: Periodic tasks
            duration: Simulation duration
            resources: Shared resources (optional)
            protocol: Resource access protocol ("none", "pip", "pcp")
        """
        self.tasks = tasks
        self.duration = duration
        self.resources = resources or []
        self.protocol_type = protocol
        
        # Initialize protocol handler
        if protocol == "pip":
            self.protocol = PriorityInheritanceProtocol(tasks, self.resources)
        elif protocol == "pcp":
            self.protocol = PriorityCeilingProtocol(tasks, self.resources)
        else:
            self.protocol = None
        
        # Simulation state
        self.timeline: List[ScheduleEvent] = []
        self.current_time = 0.0
        self.running_task: Optional[TaskInstance] = None
        self.task_instances: List[TaskInstance] = []
        self.deadline_misses: List[ScheduleEvent] = []
        
        # Resource state tracking
        self.resource_holders = {}  # resource_id -> task_id
        self.task_resource_usage = {task.id: [] for task in tasks}  # Track which resources tasks need
        self.blocked_tasks = set()  # Tasks blocked on resources
        
    @abstractmethod
    def assign_priorities(self) -> None:
        """Assign priorities to tasks (implementation depends on algorithm)."""
        pass
    
    @abstractmethod
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select next task to run based on scheduling algorithm."""
        pass
    
    def get_task_priority(self, task_id: str) -> int:
        """Get current priority for a task (may be inherited if using PIP)."""
        if self.protocol:
            return self.protocol.get_current_priority(task_id)
        
        task = next((t for t in self.tasks if t.id == task_id), None)
        return task.priority if task else 0
    
    def request_resource(self, task_id: str, resource_id: str) -> bool:
        """
        Attempt to acquire a resource for a task.
        
        Returns True if acquired, False if blocked.
        """
        if not self.resources or resource_id not in [r.resource_id for r in self.resources]:
            return True  # No resource, or resource doesn't exist
        
        resource = next((r for r in self.resources if r.resource_id == resource_id), None)
        if not resource:
            return True
        
        # Try using protocol if available
        if self.protocol:
            blocking_task = self.protocol.request_resource hypo, resource_id)
            if blocking_task:
                self.blocked_tasks.add(task_id)
                return False  # Blocked
        else:
            # Simple lock without protocol
            if resource.current_holder is not None:
                self.blocked_tasks.add(task_id)
                if task_id not in resource.queue:
                    resource.queue.append(task_id)
                return False
        
        # Resource acquired
        if resource.current_holder is None:
            resource.current_holder = task_id
            self.resource_holders[resource_id] = task_id
        return True
    
    def release_resource(self, task_id: str, resource_id: str):
        """Release a resource and unblock waiting tasks."""
        resource = next((r for r in self.resources if r.resource_id == resource_id), None)
        if not resource:
            return
        
        if self.protocol:
            self.protocol.release_resource(task_id, resource_id)
        else:
            if resource.current_holder == task_id:
                resource.current_holder = None
                self.resource_holders.pop(resource_id, None)
                
                # Unblock next waiting task
                if resource.queue:
                    next_task = resource.queue.pop(0)
                    self.blocked_tasks.discard(next_task)
    
    def simulate(self) -> ScheduleResult:
        """Run the scheduling simulation with resource handling."""
        self.assign_priorities()
        busy_time = 0
        
        # Initialize first task instances
        for task in self.tasks:
            instance = TaskInstance(
                task_id=task.id,
                instance_number=0,
                arrival_time=0.0,
                deadline=float(task.deadline),
                remaining_time=task.computation_time
            )
            self.task_instances.append(instance)
        
        # Process each time unit
        for t in range(int(self.duration)):
            self.current_time = float(t)
            
            # Create new instances
            for task in self.tasks:
                periods_passed = t // int(task.period)
                if periods_passed > 0:
                    existing = [inst for inst in self.task_instances 
                               if inst.task_id == task.id and inst.arrival_time == float(periods_passed * int(task.period))]
                    if not existing:
                        instance = TaskInstance(
                            task_id=task.id,
                            instance_number=periods_passed,
                            arrival_time=float(periods_passed * int(task.period)),
                            deadline=float(periods_passed * int(task.period) + task.deadline),
                            remaining_time=task.computation_time
                        )
                        self.task_instances.append(instance)
            
            # Update ready queue (exclude blocked tasks)
            ready_queue = [inst for inst in self.task_instances 
                          if inst.remaining_time > 0 and t >= inst.arrival_time and t < inst.de也不敢 and inst.task_id not in self.blocked_tasks]
            
            # Sort by priority
            ready_queue.sort(key=lambda x: self.get_task_priority(x.task_id), reverse=True)
            
            # Check deadline misses
            for inst in self.task_instances:
                if inst.remaining_time > 0 and t >= inst.deadline:
                    if not any(dm.details.get('instance') == inst.instance_number 
                              for dm in self.deadline_misses if dm.task_id == inst.task_id):
                        self.deadline_misses.append(ScheduleEvent(
                            time=float(t), task_id=inst.task_id, event_type='deadline_miss',
                            details={'instance': inst.instance_number}
                        ))
            
            # Select next task
            next_task = self.get_next_task(ready_queue)
            
            # Handle preemption
            if self.running_task and next_task != self.running_task:
                if self.running_task.remaining_time > 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t), task_id=self.running_task.task_id, event_type='preempt',
                        details={'instance': self.running_task.instance_number}
                    ))
            
            # Execute current task (simplified - real implementation needs CS handling)
            if self.running_task:
                self.running_task.remaining_time -= 1
                busy_time += 1
                
                if self.running_task.remaining_time <= 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t+1), task_id=self.running_task.task_id, event_type='complete',
                        details={'instance': self.running_task.instance_number}
                    ))
                    self.running_task = None
            
            # Start new task
            if next_task and next_task != self.running_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=next_task.task_id, event_type='start',
                    details={'instance': next_task.instance_number}
                ))
                self.running_task = next_task
            elif not next_task and not self.running_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=None, event_type='idle', details={}
                ))
        
        # Sort timeline
        self.timeline.sort(key=lambda e: e.time)
        
        # Calculate context switches
        context_switches = sum(1 for e in self.timeline if e.event_type in ['start', 'preempt'])
        
        # CPU utilization
        cpu_util = busy_time / self.duration if self.duration > 0 else 0.0
        
        return ScheduleResult(
            algorithm=self.__class__.__name__,
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=context_switches,
            cpu_utilization=cpu_util,
            response_times={}
        )

