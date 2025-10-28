"""EDF+HVDF scheduling algorithm for aperiodic tasks with value tracking."""

from typing import List, Optional, Dict
from ..scheduler_base import SchedulerBase
from ..task import AperiodicTask, TaskInstance, ScheduleResult, ScheduleEvent


def calculate_value_density(task_instance: TaskInstance, task_values: Dict[str, float]) -> float:
    """
    Calculate value density for HVDF scheduling.
    
    Args:
        task_instance: Task instance to calculate density for
        task_values: Mapping of task_id -> value
        
    Returns:
        Value density (value / remaining_time)
    """
    value = task_values.get(task_instance.task_id, 0.0)
    if task_instance.remaining_time > 0:
        return value / task_instance.remaining_time
    return 0.0


class EDFHVDFScheduler(SchedulerBase):
    """
    EDF+HVDF Scheduler for aperiodic tasks.
    
    Primary: Earliest Deadline First (EDF)
    Tie-breaker: Highest Value Density First (HVDF)
    
    Supports both preemptive and non-preemptive task execution.
    Tracks value accumulation for successful task completions.
    """
    
    def __init__(self, aperiodic_tasks: List[AperiodicTask], duration: int = 100):
        """
        Initialize EDF+HVDF scheduler.
        
        Args:
            aperiodic_tasks: List of aperiodic tasks to schedule
            duration: Simulation duration
        """
        # Store aperiodic tasks and value mapping
        self.aperiodic_tasks = sorted(aperiodic_tasks, key=lambda t: t.arrival_time)
        self.task_values = {task.id: task.value for task in aperiodic_tasks}
        
        # Convert aperiodic tasks to periodic tasks for base class compatibility
        periodic_tasks = []
        super().__init__(periodic_tasks, duration)
        
        # Track completed tasks with their values
        self.completed_tasks: List[TaskInstance] = []
    
    def assign_priorities(self) -> None:
        """EDF+HVDF uses dynamic priorities, not fixed."""
        # Dynamic priority assignment based on deadline and value density
        for task in self.tasks:
            task.priority = 0
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """
        Select task with earliest deadline, tie-break by value density.
        
        Args:
            ready_queue: List of ready task instances
            
        Returns:
            Task instance with highest priority (EDF primary, HVDF secondary)
        """
        if not ready_queue:
            return None
        
        # Sort by: (deadline ASC, -value_density DESC)
        # First sort by deadline (earliest first)
        # Then sort by negative value density (highest first)
        def sort_key(instance: TaskInstance) -> tuple:
            value_density = calculate_value_density(instance, self.task_values)
            return (instance.deadline, -value_density)
        
        return min(ready_queue, key=sort_key)
    
    def simulate(self) -> ScheduleResult:
        """
        Run EDF+HVDF simulation for aperiodic tasks.
        
        Returns:
            ScheduleResult with events and value tracking
        """
        self.assign_priorities()
        
        # Initialize tracking
        self.task_instances: List[TaskInstance] = []
        self.timeline: List[ScheduleEvent] = []
        self.current_time = 0.0
        self.running_task: Optional[TaskInstance] = None
        
        # Convert aperiodic tasks to TaskInstances
        for task in self.aperiodic_tasks:
            instance = TaskInstance(
                task_id=task.id,
                instance_number=0,  # Aperiodic tasks only have one instance
                arrival_time=task.arrival_time,
                deadline=task.deadline,  # Already absolute deadline from UI
                remaining_time=task.computation_time
            )
            instance.start_time = None
            instance.completion_time = None
            self.task_instances.append(instance)
        
        # Track running task preemptive flag
        running_task_preemptive = True
        
        # Simulation loop
        for t in range(int(self.duration)):
            time = float(t)
            self.current_time = time
            
            # Add arrived tasks to ready queue
            ready_queue = []
            for instance in self.task_instances:
                if instance.arrival_time <= time and instance.remaining_time > 0:
                    ready_queue.append(instance)
            
            # Sort ready queue by priority (EDF+HVDF)
            next_task = self.get_next_task(ready_queue)
            
            # Check if we should continue current task (non-preemptive mode)
            if self.running_task is not None and not running_task_preemptive:
                # Non-preemptive: continue current task until completion
                if self.running_task.remaining_time > 0:
                    # Continue execution
                    self.running_task.remaining_time -= 1.0
                    
                    # Check completion
                    if self.running_task.remaining_time <= 0:
                        self.running_task.completion_time = time + 1.0
                        self.completed_tasks.append(self.running_task)
                        
                        self.timeline.append(ScheduleEvent(
                            time=time + 1.0,
                            task_id=self.running_task.task_id,
                            event_type='complete',
                            details={'instance': 0}
                        ))
                        
                        self.running_task = None
                        running_task_preemptive = True
                    
                    continue
            
            # Handle task switching (preemptive mode or new task)
            if self.running_task is None and next_task is not None:
                # Start new task
                self.running_task = next_task
                # Get preemptive flag from aperiodic task
                apt = next((t for t in self.aperiodic_tasks if t.id == self.running_task.task_id), None)
                running_task_preemptive = apt.preemptive if apt else True
                
                self.timeline.append(ScheduleEvent(
                    time=time,
                    task_id=self.running_task.task_id,
                    event_type='start',
                    details={'instance': 0}
                ))
            elif self.running_task is not None and running_task_preemptive and next_task is not None:
                # Preemptive mode: can switch to higher priority task
                if next_task.task_id != self.running_task.task_id:
                    self.timeline.append(ScheduleEvent(
                        time=time,
                        task_id=self.running_task.task_id,
                        event_type='preempt',
                        details={'instance': 0}
                    ))
                    self.running_task = next_task
                    apt = next((t for t in self.aperiodic_tasks if t.id == self.running_task.task_id), None)
                    running_task_preemptive = apt.preemptive if apt else True
                    self.timeline.append(ScheduleEvent(
                        time=time,
                        task_id=self.running_task.task_id,
                        event_type='start',
                        details={'instance': 0}
                    ))
            
            # Execute current task
            if self.running_task is not None:
                self.running_task.remaining_time -= 1.0
                
                # Check completion
                if self.running_task.remaining_time <= 0:
                    self.running_task.completion_time = time + 1.0
                    self.completed_tasks.append(self.running_task)
                    
                    self.timeline.append(ScheduleEvent(
                        time=time + 1.0,
                        task_id=self.running_task.task_id,
                        event_type='complete',
                        details={'instance': 0}
                    ))
                    
                    self.running_task = None
                    running_task_preemptive = True
            else:
                # CPU idle
                if time == 0 or self.timeline[-1].event_type != 'idle':
                    self.timeline.append(ScheduleEvent(
                        time=time,
                        task_id=None,
                        event_type='idle',
                        details={}
                    ))
            
            # Check for deadline misses
            for instance in self.task_instances:
                if instance.completion_time is None and time > instance.deadline:
                    # Check if we already recorded this miss
                    existing_miss = any(
                        evt.task_id == instance.task_id and evt.event_type == 'deadline_miss'
                        for evt in self.timeline
                    )
                    if not existing_miss:
                        self.timeline.append(ScheduleEvent(
                            time=instance.deadline,
                            task_id=instance.task_id,
                            event_type='deadline_miss',
                            details={'instance': 0}
                        ))
        
        # Sort timeline by time
        self.timeline.sort(key=lambda e: e.time)
        
        # Calculate deadline misses
        deadline_misses = [evt for evt in self.timeline if evt.event_type == 'deadline_miss']
        
        # Calculate context switches (start and preempt events)
        total_context_switches = len([evt for evt in self.timeline if evt.event_type in ['start', 'preempt']])
        
        # Calculate CPU utilization (sum of computation times / duration)
        busy_time = sum(task.computation_time for task in self.aperiodic_tasks)
        cpu_utilization = (busy_time / self.duration) if self.duration > 0 else 0.0
        
        # Create result
        result = ScheduleResult(
            algorithm="EDF+HVDF",
            tasks=[],  # No periodic tasks
            events=self.timeline,
            deadline_misses=deadline_misses,
            total_context_switches=total_context_switches,
            cpu_utilization=cpu_utilization * 100.0,  # Percentage
            response_times={}
        )
        
        return result
    
    def calculate_total_value(self) -> float:
        """
        Calculate total value from tasks that met their deadlines.
        
        Returns:
            Sum of values from successfully completed tasks
        """
        total = 0.0
        for instance in self.completed_tasks:
            if instance.completion_time <= instance.deadline:
                value = self.task_values.get(instance.task_id, 0.0)
                total += value
        return total

