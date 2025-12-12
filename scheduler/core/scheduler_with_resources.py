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
            blocking_task = self.protocol.request_resource(task_id, resource_id)
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
    
    def _get_task_critical_sections(self, task_id: str) -> list:
        """Get critical sections for a task."""
        task = next((t for t in self.tasks if t.id == task_id), None)
        return task.critical_sections if task else []

    def _get_execution_progress(self, task_instance: TaskInstance) -> float:
        """Get how much of the task has been executed so far."""
        task = next((t for t in self.tasks if t.id == task_instance.task_id), None)
        if task:
            return task.computation_time - task_instance.remaining_time
        return 0.0

    def _check_cs_entry(self, task_id: str, progress: float) -> Optional[tuple]:
        """Check if task should enter a critical section at given progress."""
        critical_sections = self._get_task_critical_sections(task_id)
        for cs in critical_sections:
            if not cs.completed and abs(cs.start_offset - progress) < 0.001:
                return (cs.resource_id, cs)
        return None

    def _check_cs_exit(self, task_id: str, progress: float) -> Optional[tuple]:
        """Check if task should exit a critical section at given progress."""
        critical_sections = self._get_task_critical_sections(task_id)
        for cs in critical_sections:
            if not cs.completed:
                cs_end = cs.start_offset + cs.duration
                if progress >= cs_end - 0.001:
                    return (cs.resource_id, cs)
        return None

    def _is_in_critical_section(self, task_id: str, progress: float) -> Optional[str]:
        """Check if task is currently in a critical section."""
        critical_sections = self._get_task_critical_sections(task_id)
        for cs in critical_sections:
            if not cs.completed:
                if cs.start_offset <= progress < cs.start_offset + cs.duration:
                    return cs.resource_id
        return None

    def simulate(self) -> ScheduleResult:
        """Run the scheduling simulation with resource handling."""
        self.assign_priorities()

        # Update protocol priorities after scheduler assigns them (CRITICAL for PCP)
        if self.protocol and hasattr(self.protocol, 'update_priorities'):
            self.protocol.update_priorities()

        busy_time = 0

        # Track active critical sections per task instance
        active_cs: Dict[tuple, str] = {}  # (task_id, instance) -> resource_id

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
                periods_passed = int(t // task.period)
                if periods_passed > 0:
                    arrival_time = periods_passed * task.period
                    existing = [inst for inst in self.task_instances
                               if inst.task_id == task.id and abs(inst.arrival_time - arrival_time) < 0.001]
                    if not existing:
                        instance = TaskInstance(
                            task_id=task.id,
                            instance_number=periods_passed,
                            arrival_time=arrival_time,
                            deadline=arrival_time + task.deadline,
                            remaining_time=task.computation_time
                        )
                        self.task_instances.append(instance)

            # Update ready queue (exclude blocked tasks)
            ready_queue = [inst for inst in self.task_instances
                          if inst.remaining_time > 0 and t >= inst.arrival_time and inst.task_id not in self.blocked_tasks]

            # Sort by priority (use task_id as tie-breaker for deterministic results)
            ready_queue.sort(key=lambda x: (-self.get_task_priority(x.task_id), x.task_id))

            # Check deadline misses
            for inst in self.task_instances:
                if inst.remaining_time > 0 and t > inst.deadline:
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
                    # Check if current task is in critical section (non-preemptive within CS)
                    inst_key = (self.running_task.task_id, self.running_task.instance_number)
                    if inst_key in active_cs:
                        # In critical section - cannot be preempted
                        next_task = self.running_task
                    else:
                        self.timeline.append(ScheduleEvent(
                            time=float(t), task_id=self.running_task.task_id, event_type='preempt',
                            details={'instance': self.running_task.instance_number}
                        ))

            # Start new task
            if next_task and next_task != self.running_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=next_task.task_id, event_type='start',
                    details={'instance': next_task.instance_number}
                ))
                self.running_task = next_task

            # Execute current task with critical section handling
            if self.running_task:
                progress = self._get_execution_progress(self.running_task)
                inst_key = (self.running_task.task_id, self.running_task.instance_number)

                # Check for critical section entry
                cs_entry = self._check_cs_entry(self.running_task.task_id, progress)
                if cs_entry:
                    resource_id, cs = cs_entry
                    if self.request_resource(self.running_task.task_id, resource_id):
                        # Resource acquired - enter critical section
                        active_cs[inst_key] = resource_id
                        self.timeline.append(ScheduleEvent(
                            time=float(t), task_id=self.running_task.task_id, event_type='cs_enter',
                            details={'instance': self.running_task.instance_number, 'resource': resource_id}
                        ))
                    else:
                        # Blocked - cannot execute
                        self.timeline.append(ScheduleEvent(
                            time=float(t), task_id=self.running_task.task_id, event_type='blocked',
                            details={'instance': self.running_task.instance_number, 'resource': resource_id}
                        ))
                        continue  # Skip execution this time unit

                # Execute task
                self.running_task.remaining_time -= 1
                busy_time += 1
                new_progress = self._get_execution_progress(self.running_task)

                # Check for critical section exit
                cs_exit = self._check_cs_exit(self.running_task.task_id, new_progress)
                if cs_exit:
                    resource_id, cs = cs_exit
                    cs.completed = True
                    self.release_resource(self.running_task.task_id, resource_id)
                    if inst_key in active_cs:
                        del active_cs[inst_key]
                    self.timeline.append(ScheduleEvent(
                        time=float(t + 1), task_id=self.running_task.task_id, event_type='cs_exit',
                        details={'instance': self.running_task.instance_number, 'resource': resource_id}
                    ))

                # Check for task completion
                if self.running_task.remaining_time <= 0:
                    # Release any held resources
                    if inst_key in active_cs:
                        resource_id = active_cs[inst_key]
                        self.release_resource(self.running_task.task_id, resource_id)
                        del active_cs[inst_key]

                    self.timeline.append(ScheduleEvent(
                        time=float(t + 1), task_id=self.running_task.task_id, event_type='complete',
                        details={'instance': self.running_task.instance_number}
                    ))
                    self.running_task = None
            elif not next_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=None, event_type='idle', details={}
                ))

        # Sort timeline
        self.timeline.sort(key=lambda e: e.time)

        # Calculate context switches (count only 'start' to avoid double-counting preempt+start)
        context_switches = sum(1 for e in self.timeline if e.event_type == 'start')

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

