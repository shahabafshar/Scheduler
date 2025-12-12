"""Base scheduler class with core simulation loop - Simplified version."""

from abc import ABC, abstractmethod
from typing import List, Optional
from .task import PeriodicTask, TaskInstance, ScheduleEvent, ScheduleResult


class SchedulerBase(ABC):
    """Base class for all scheduling algorithms."""
    
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
        for t in range(self.duration):
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
            ready_queue = [inst for inst in self.task_instances
                          if inst.remaining_time > 0 and t >= inst.arrival_time]
            
            # Sort by priority (use task_id as tie-breaker for deterministic results)
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
            
            # Execute current task
            if self.running_task:
                self.running_task.remaining_time -= 1
                busy_time += 1
                
                if self.running_task.remaining_time <= 0:
                    # Task completed
                    self.timeline.append(ScheduleEvent(
                        time=float(t+1), task_id=self.running_task.task_id, event_type='complete',
                        details={'instance': self.running_task.instance_number}
                    ))
                    self.running_task = None
            
            # Start new task if different from current
            if next_task and next_task != self.running_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=next_task.task_id, event_type='start',
                    details={'instance': next_task.instance_number}
                ))
                self.running_task = next_task
            elif not next_task and not self.running_task:
                # Idle
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

