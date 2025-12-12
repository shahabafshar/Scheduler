"""Base scheduler class with core simulation loop - Simplified version."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from .task import PeriodicTask, TaskInstance, ScheduleEvent, ScheduleResult, CriticalSection


class SchedulerBase(ABC):
    """Base class for all scheduling algorithms."""

    # Subclasses with dynamic priority (EDF, LLF) should set this to True
    # to skip redundant ready queue sorting in the base simulation loop
    _skip_priority_sort: bool = False

    def __init__(self, tasks: List[PeriodicTask], duration: int = 100):
        """
        Initialize scheduler.
        
        Args:
            tasks: List of periodic tasks to schedule
            duration: Simulation duration in time units
        """
        self.tasks = tasks
        self.duration = duration
        self.timeline: List[ScheduleEvent] = []
        self.current_time = 0.0
        self.running_task: Optional[TaskInstance] = None
        self.task_instances: List[TaskInstance] = []
        self.deadline_misses: List[ScheduleEvent] = []
        
        # Resource tracking for critical sections
        self.active_critical_sections: Dict[str, List[CriticalSection]] = {}  # task_id -> [CS, CS, ...]
        self.resource_locks: Dict[str, Optional[str]] = {}  # resource_id -> task_id that holds it
        self.blocked_tasks: Dict[str, str] = {}  # task_id -> resource_id it's waiting for
        
    @abstractmethod
    def assign_priorities(self) -> None:
        """Assign priorities to tasks (implementation depends on algorithm)."""
        pass
    
    @abstractmethod
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select next task to run based on scheduling algorithm."""
        pass
    
    def get_task_priority(self, task_id: str) -> int:
        """Get priority for a task."""
        task = next((t for t in self.tasks if t.id == task_id), None)
        return task.priority if task else 0
    
    def _check_critical_section_entry(self, task_id: str, progress: float) -> Optional[CriticalSection]:
        """Check if task should enter a critical section based on execution progress."""
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task or not task.critical_sections:
            return None
        
        # Check if task has reached start_offset of any CS
        for cs in task.critical_sections:
            if not cs.completed and cs.start_offset <= progress < cs.start_offset + cs.duration:
                return cs
        return None
    
    def _request_resource(self, task_id: str, resource_id: str) -> bool:
        """Request a resource. Returns True if granted, False if blocked."""
        if resource_id not in self.resource_locks:
            self.resource_locks[resource_id] = None
        
        if self.resource_locks[resource_id] is None:
            # Resource is free, grant it
            self.resource_locks[resource_id] = task_id
            return True
        else:
            # Resource is held by another task, block requesting task
            self.blocked_tasks[task_id] = resource_id
            return False
    
    def _release_resource(self, task_id: str, resource_id: str) -> Optional[str]:
        """Release a resource. Returns task_id of next waiting task, or None."""
        if resource_id in self.resource_locks and self.resource_locks[resource_id] == task_id:
            self.resource_locks[resource_id] = None
            # Unblock any task waiting for this resource
            if task_id in self.blocked_tasks and self.blocked_tasks[task_id] == resource_id:
                del self.blocked_tasks[task_id]
            return None
        return None
    
    def simulate(self) -> ScheduleResult:
        """Run the scheduling simulation."""
        # Assign priorities
        self.assign_priorities()
        
        # Track execution time
        busy_time = 0
        
        # Initialize: create first instances at time 0
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
            # Update current time
            self.current_time = float(t)
            
            # Create new task instances based on periods
            for task in self.tasks:
                # Check if a new instance should arrive
                # At time t = 0, P, 2P, 3P, ...
                periods_passed = int(t // task.period)

                if periods_passed > 0:
                    # Check if we already created this instance
                    arrival_time = periods_passed * task.period
                    existing = [inst for inst in self.task_instances
                               if inst.task_id == task.id and abs(inst.arrival_time - arrival_time) < 0.001]

                    if not existing:
                        # Create new instance
                        instance = TaskInstance(
                            task_id=task.id,
                            instance_number=periods_passed,
                            arrival_time=arrival_time,
                            deadline=arrival_time + task.deadline,
                            remaining_time=task.computation_time
                        )
                        self.task_instances.append(instance)
            
            # Update ready queue (active instances)
            # Note: Tasks remain eligible even after deadline (they just miss the constraint)
            # Deadline misses are recorded separately below
            ready_queue = [inst for inst in self.task_instances
                          if inst.remaining_time > 0 and t >= inst.arrival_time]

            # Sort by priority (skip for dynamic algorithms like EDF/LLF that use their own selection)
            if not self._skip_priority_sort:
                ready_queue.sort(key=lambda x: (-self.get_task_priority(x.task_id), x.task_id))
            
            # Check deadline misses
            for inst in self.task_instances:
                if inst.remaining_time > 0 and t >= inst.deadline:
                    if not any(dm.details.get('instance') == inst.instance_number 
                              for dm in self.deadline_misses if dm.task_id == inst.task_id):
                        self.deadline_misses.append(ScheduleEvent(
                            time=float(t), task_id=inst.task_id, event_type='deadline_miss',
                            details={'instance': inst.instance_number}
                        ))
            
            # Select next task to run
            next_task = self.get_next_task(ready_queue)
            
            # Handle preemption
            if self.running_task and next_task != self.running_task:
                if self.running_task.remaining_time > 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t), task_id=self.running_task.task_id, event_type='preempt',
                        details={'instance': self.running_task.instance_number}
                    ))
            
            # First, start new task if different from current (before execution)
            if next_task and next_task != self.running_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=next_task.task_id, event_type='start',
                    details={'instance': next_task.instance_number}
                ))
                self.running_task = next_task
            
            # Execute current task
            if self.running_task:
                # Calculate execution progress
                task = next((t for t in self.tasks if t.id == self.running_task.task_id), None)
                total_time = task.computation_time if task else 0
                progress = (total_time - self.running_task.remaining_time) + 1
                
                # Check if entering critical section
                cs = self._check_critical_section_entry(self.running_task.task_id, progress)
                if cs:
                    # Request resource
                    granted = self._request_resource(self.running_task.task_id, cs.resource_id)
                    if granted:
                        self.timeline.append(ScheduleEvent(
                            time=float(t), task_id=self.running_task.task_id, event_type='block',
                            details={'instance': self.running_task.instance_number, 'resource': cs.resource_id, 'action': 'enter'}
                        ))
                    else:
                        # Blocked - task can't execute in this time slot
                        self.timeline.append(ScheduleEvent(
                            time=float(t), task_id=self.running_task.task_id, event_type='block',
                            details={'instance': self.running_task.instance_number, 'resource': cs.resource_id, 'action': 'wait'}
                        ))
                        self.running_task = None  # Stop executing
                        continue  # Move to next iteration
                
                # Check if exiting critical section
                if cs:
                    cs_end = cs.start_offset + cs.duration
                    if progress >= cs_end and not cs.completed:
                        # Release resource
                        self._release_resource(self.running_task.task_id, cs.resource_id)
                        cs.completed = True
                        self.timeline.append(ScheduleEvent(
                            time=float(t), task_id=self.running_task.task_id, event_type='block',
                            details={'instance': self.running_task.instance_number, 'resource': cs.resource_id, 'action': 'exit'}
                        ))
                
                self.running_task.remaining_time -= 1
                busy_time += 1
                
                if self.running_task.remaining_time <= 0:
                    # Task completed
                    self.timeline.append(ScheduleEvent(
                        time=float(t+1), task_id=self.running_task.task_id, event_type='complete',
                        details={'instance': self.running_task.instance_number}
                    ))
                    # Release any held resources
                    if task and task.critical_sections:
                        for cs in task.critical_sections:
                            if not cs.completed and cs.resource_id in self.resource_locks:
                                self._release_resource(self.running_task.task_id, cs.resource_id)
                    self.running_task = None
            
            # Record idle if no task running
            if not self.running_task and not next_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=None, event_type='idle', details={}
                ))
        
        # Sort timeline by time
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

