"""EDF+HVDF scheduling for PERIODIC tasks with value tracking."""

from typing import List, Optional, Dict
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, ScheduleResult, ScheduleEvent


def calculate_value_density(task_instance: TaskInstance, task_values: Dict[str, float]) -> float:
    """Calculate value density for HVDF scheduling."""
    value = task_values.get(task_instance.task_id, 0.0)
    if task_instance.remaining_time > 0:
        return value / task_instance.remaining_time
    return 0.0


class EDFHVDFPeriodicScheduler(SchedulerBase):
    """
    EDF+HVDF Scheduler for PERIODIC tasks.
    
    - Primary: Earliest Deadline First (EDF)
    - Tie-breaker: Highest Value Density First (HVDF)
    - Mode: Non-preemptive (configurable per task)
    - Task type: Periodic (multiple instances over time)
    
    Tracks value across ALL task instances that meet their deadlines.
    """
    
    def __init__(self, periodic_tasks: List[PeriodicTask], duration: int = 100):
        """Initialize EDF+HVDF periodic scheduler.
        
        Args:
            periodic_tasks: List of periodic tasks to schedule
            duration: Simulation duration (time window)
        """
        super().__init__(periodic_tasks, duration)
        
        # Store task values
        self.task_values = {task.id: task.value for task in periodic_tasks}
        
        # Track ALL completed instances for value calculation
        self.completed_instances: List[TaskInstance] = []
        self.total_value_accumulated = 0.0
    
    def assign_priorities(self) -> None:
        """EDF+HVDF uses dynamic priorities, not fixed."""
        # Dynamic priority based on deadline and value density
        pass
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select task with earliest deadline, tie-break by value density.
        
        Args:
            ready_queue: List of ready task instances
            
        Returns:
            Task instance with highest priority (EDF primary, HVDF secondary)
        """
        if not ready_queue:
            return None
        
        # Sort by: (deadline ASC, -value_density DESC)
        def sort_key(instance: TaskInstance) -> tuple:
            value_density = calculate_value_density(instance, self.task_values)
            return (instance.deadline, -value_density)
        
        return min(ready_queue, key=sort_key)
    
    def simulate(self) -> ScheduleResult:
        """Run EDF+HVDF simulation for periodic tasks.
        
        Returns:
            ScheduleResult with events and value tracking
        """
        self.assign_priorities()
        
        # Initialize tracking
        self.task_instances: List[TaskInstance] = []
        self.timeline: List[ScheduleEvent] = []
        self.deadline_misses: List[TaskInstance] = []
        self.completed_instances = []
        self.total_value_accumulated = 0.0
        self.current_time = 0.0
        self.running_task: Optional[TaskInstance] = None
        busy_time = 0  # Track actual CPU busy time
        
        # Track which tasks are preemptive
        task_preemptive_map = {task.id: task.preemptive for task in self.tasks}
        running_task_preemptive = True
        
        # Simulation loop
        for t in range(int(self.duration)):
            time = float(t)
            self.current_time = time
            
            # Create new task instances at their arrival times (every period)
            for task in self.tasks:
                # Check if new instance should arrive
                instance_number = int(time / task.period)
                arrival_time = instance_number * task.period
                
                if abs(time - arrival_time) < 0.001:  # Floating point comparison
                    # Check if this instance already exists
                    existing = any(
                        inst.task_id == task.id and 
                        inst.instance_number == instance_number
                        for inst in self.task_instances
                    )
                    
                    if not existing:
                        deadline = arrival_time + (task.deadline if task.deadline else task.period)
                        instance = TaskInstance(
                            task_id=task.id,
                            instance_number=instance_number,
                            arrival_time=arrival_time,
                            deadline=deadline,
                            remaining_time=task.computation_time
                        )
                        self.task_instances.append(instance)
            
            # Build ready queue (arrived, not completed, before deadline)
            ready_queue = [
                inst for inst in self.task_instances
                if inst.arrival_time <= time and 
                   inst.remaining_time > 0 and
                   time <= inst.deadline
            ]
            
            # Check for deadline misses
            for inst in self.task_instances:
                if inst.remaining_time > 0 and time > inst.deadline:
                    if inst not in self.deadline_misses:
                        self.deadline_misses.append(inst)
                        self.timeline.append(ScheduleEvent(
                            time=time,
                            task_id=inst.task_id,
                            event_type='deadline_miss',
                            details={'instance': inst.instance_number}
                        ))
            
            # Handle non-preemptive task continuation
            if self.running_task is not None and not running_task_preemptive:
                if self.running_task.remaining_time > 0:
                    # Continue non-preemptive task
                    self.running_task.remaining_time -= 1.0
                    busy_time += 1

                    if self.running_task.remaining_time <= 0:
                        # Task completed
                        self.running_task.completion_time = time + 1.0
                        self._handle_completion(self.running_task, time + 1.0)
                        self.running_task = None
                        running_task_preemptive = True

                    continue  # Skip rest of loop
            
            # Get next task
            next_task = self.get_next_task(ready_queue)
            
            # Handle task switching
            if self.running_task is None and next_task is not None:
                # Start new task
                self.running_task = next_task
                running_task_preemptive = task_preemptive_map.get(self.running_task.task_id, True)
                
                self.timeline.append(ScheduleEvent(
                    time=time,
                    task_id=self.running_task.task_id,
                    event_type='start',
                    details={'instance': self.running_task.instance_number}
                ))
            elif self.running_task is not None and running_task_preemptive and next_task is not None:
                # Preemptive mode: can switch to higher priority task
                if next_task.task_id != self.running_task.task_id or next_task.instance_number != self.running_task.instance_number:
                    # Different task/instance has higher priority
                    if self.get_next_task([self.running_task, next_task]) != self.running_task:
                        # Preempt current task
                        self.timeline.append(ScheduleEvent(
                            time=time,
                            task_id=self.running_task.task_id,
                            event_type='preempt',
                            details={'instance': self.running_task.instance_number}
                        ))
                        self.running_task = next_task
                        running_task_preemptive = task_preemptive_map.get(self.running_task.task_id, True)
                        self.timeline.append(ScheduleEvent(
                            time=time,
                            task_id=self.running_task.task_id,
                            event_type='start',
                            details={'instance': self.running_task.instance_number}
                        ))
            
            # Execute current task
            if self.running_task is not None:
                self.running_task.remaining_time -= 1.0
                busy_time += 1

                # Check completion
                if self.running_task.remaining_time <= 0:
                    self.running_task.completion_time = time + 1.0
                    self._handle_completion(self.running_task, time + 1.0)
                    self.running_task = None
                    running_task_preemptive = True
            else:
                # CPU idle
                if len(self.timeline) == 0 or self.timeline[-1].event_type != 'idle' or self.timeline[-1].time != time:
                    self.timeline.append(ScheduleEvent(
                        time=time,
                        task_id=None,
                        event_type='idle',
                        details={}
                    ))
        
        # Sort timeline by time
        self.timeline.sort(key=lambda e: e.time)
        
        # Calculate metrics
        total_context_switches = len([evt for evt in self.timeline if evt.event_type in ['start', 'preempt']])

        # CPU utilization (based on actual busy time tracked during simulation)
        cpu_utilization = (busy_time / self.duration) if self.duration > 0 else 0.0
        
        # Create result
        result = ScheduleResult(
            algorithm="EDF+HVDF (Periodic)",
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=total_context_switches,
            cpu_utilization=cpu_utilization,
            response_times={}
        )
        
        return result
    
    def _handle_completion(self, task_instance: TaskInstance, completion_time: float):
        """Handle task completion and value accumulation."""
        task_instance.completion_time = completion_time
        self.completed_instances.append(task_instance)
        
        # Check if deadline met
        if completion_time <= task_instance.deadline:
            value = self.task_values.get(task_instance.task_id, 0.0)
            self.total_value_accumulated += value
        
        self.timeline.append(ScheduleEvent(
            time=completion_time,
            task_id=task_instance.task_id,
            event_type='complete',
            details={'instance': task_instance.instance_number}
        ))
    
    def calculate_total_value(self) -> float:
        """Calculate total value from ALL instances that met deadlines.
        
        Returns:
            Sum of values from all successfully completed instances
        """
        return self.total_value_accumulated
    
    def get_value_breakdown(self) -> List[Dict]:
        """Get per-instance value breakdown.
        
        Returns:
            List of dicts with task_id, instance, completion, deadline, value
        """
        breakdown = []
        for inst in self.completed_instances:
            met_deadline = inst.completion_time <= inst.deadline
            value = self.task_values.get(inst.task_id, 0.0) if met_deadline else 0.0
            breakdown.append({
                'task_id': inst.task_id,
                'instance': inst.instance_number,
                'completion_time': inst.completion_time,
                'deadline': inst.deadline,
                'met_deadline': met_deadline,
                'value': value
            })
        return breakdown


