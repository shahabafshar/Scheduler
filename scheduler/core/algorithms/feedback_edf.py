"""Feedback Control EDF (FC-EDF) implementation with adaptive service levels."""

from dataclasses import dataclass
from typing import List, Dict, Optional
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, ScheduleEvent, ScheduleResult
import math


class TaskVersion:
    """A task version with specific execution time and service level."""
    def __init__(self, service_level: int, execution_time: float, accuracy: float = 1.0):
        self.service_level = service_level  # 0 = lowest, higher = better
        self.execution_time = execution_time
        self.accuracy = accuracy  # Quality metric (0-1)
    
    def __str__(self) -> str:
        return f"Level{self.service_level}: ET={self.execution_time:.1f}, Acc={self.accuracy:.2f}"


@dataclass
class TaskWithVersions:
    """A task with multiple service level versions."""
    id: str
    versions: List[TaskVersion]  # Ordered from lowest to highest level
    period: float
    deadline: float
    current_version_index: int = 0  # Current active version
    
    @property
    def current_version(self) -> TaskVersion:
        """Get the currently active version."""
        return self.versions[self.current_version_index]
    
    @property
    def current_execution_time(self) -> float:
        """Get current execution time."""
        return self.current_version.execution_time


class FCEDFScheduler(SchedulerBase):
    """
    Feedback Control EDF (FC-EDF) scheduler.
    
    Uses PID control to adapt service levels based on deadline miss ratio.
    Target: maintain target miss ratio while maximizing quality.
    """
    
    def __init__(self, tasks_with_versions: List[TaskWithVersions], 
                 target_miss_ratio: float = 0.05,
                 kp: float = 0.1, ki: float = 0.01, kd: float = 0.05,
                 sampling_period: int = 10,
                 duration: int = 100):
        """
        Initialize FC-EDF scheduler.
        
        Args:
            tasks_with_versions: Tasks with multiple service levels
            target_miss_ratio: Target deadline miss ratio (0-1)
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            sampling_period: How often to adjust service levels
            duration: Simulation duration
        """
        # Convert to regular tasks using current versions
        tasks = [
            PeriodicTask(
                id=tv.id,
                computation_time=tv.current_execution_time,
                period=tv.period,
                deadline=tv.deadline
            )
            for tv in tasks_with_versions
        ]
        
        super().__init__(tasks, duration)
        
        self.tasks_with_versions = tasks_with_versions
        self.target_miss_ratio = target_miss_ratio
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.sampling_period = sampling_period
        
        # PID control state
        self.integral_error = 0.0
        self.previous_error = 0.0
        self.miss_count_history = []  # Track misses over time
        
        # Service level history for visualization
        self.service_level_history = {tv.id: [] for tv in tasks_with_versions}
        
    def assign_priorities(self) -> None:
        """EDF priorities are dynamic - no assignment needed."""
        pass
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select task with earliest deadline (EDF) with deterministic tie-breaking."""
        if not ready_queue:
            return None

        # Get real-time deadlines from task instances (tie-break by task_id for determinism)
        sorted_queue = sorted(ready_queue, key=lambda inst: (self._get_abs_deadline(inst), inst.task_id))
        return sorted_queue[0]
    
    def _get_abs_deadline(self, instance: TaskInstance) -> float:
        """Get absolute deadline for an instance."""
        return instance.deadline
    
    def simulate(self) -> ScheduleResult:
        """Run simulation with adaptive service level adjustment."""
        # Initialize instances and service levels
        for task in self.tasks:
            self.task_instances.append(TaskInstance(
                task_id=task.id,
                instance_number=0,
                arrival_time=0.0,
                deadline=float(task.deadline),
                remaining_time=task.computation_time
            ))

        # Track CPU busy time for utilization
        busy_time = 0

        # Run simulation
        for t in range(int(self.duration)):
            self.current_time = float(t)
            
            # Sample miss ratio and adjust service levels periodically
            if t > 0 and t % self.sampling_period == 0:
                self._adjust_service_levels(t)
            
            # Record current service levels
            for tv in self.tasks_with_versions:
                self.service_level_history[tv.id].append((t, tv.current_version_index))
            
            # Create new task instances
            for task in self.tasks:
                periods_passed = int(t // task.period)

                if periods_passed > 0:
                    arrival_time = periods_passed * task.period
                    existing = [inst for inst in self.task_instances
                               if inst.task_id == task.id
                               and abs(inst.arrival_time - arrival_time) < 0.001]

                    if not existing:
                        instance = TaskInstance(
                            task_id=task.id,
                            instance_number=periods_passed,
                            arrival_time=arrival_time,
                            deadline=arrival_time + task.deadline,
                            remaining_time=task.computation_time
                        )
                        self.task_instances.append(instance)
            
            # Update ready queue (EDF)
            # Note: Tasks remain eligible even after deadline (they just miss the constraint)
            ready_queue = [inst for inst in self.task_instances
                          if inst.remaining_time > 0 and t >= inst.arrival_time]
            ready_queue.sort(key=lambda x: (x.deadline, x.task_id))
            
            # Check deadline misses (t > deadline, not >=, since at t=deadline task is still "at deadline")
            for inst in self.task_instances:
                if inst.remaining_time > 0 and t > inst.deadline:
                    if not any(dm.details.get('instance') == inst.instance_number 
                              for dm in self.deadline_misses if dm.task_id == inst.task_id):
                        self.deadline_misses.append(ScheduleEvent(
                            time=float(t), task_id=inst.task_id, event_type='deadline_miss',
                            details={'instance': inst.instance_number}
                        ))
                        self.miss_count_history.append((t, True))
            
            # Select and execute task
            next_task = self.get_next_task(ready_queue)
            
            if self.running_task and next_task != self.running_task:
                if self.running_task.remaining_time > 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t), task_id=self.running_task.task_id, event_type='preempt',
                        details={'instance': self.running_task.instance_number}
                    ))
            
            if next_task and next_task != self.running_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=next_task.task_id, event_type='start',
                    details={'instance': next_task.instance_number}
                ))
                self.running_task = next_task
            
            if self.running_task:
                self.running_task.remaining_time -= 1
                busy_time += 1

                if self.running_task.remaining_time <= 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t+1), task_id=self.running_task.task_id, event_type='complete',
                        details={'instance': self.running_task.instance_number}
                    ))
                    self.running_task = None

            if not self.running_task and not next_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=None, event_type='idle', details={}
                ))

            self.miss_count_history.append((t, False))

        self.timeline.sort(key=lambda e: e.time)

        # Calculate metrics (count only 'start' to avoid double-counting preempt+start)
        context_switches = sum(1 for e in self.timeline if e.event_type == 'start')
        cpu_util = busy_time / self.duration if self.duration > 0 else 0.0

        return ScheduleResult(
            algorithm="FC-EDF",
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=context_switches,
            cpu_utilization=cpu_util,
            response_times={},
            details={'service_level_history': self.service_level_history}
        )
    
    def _adjust_service_levels(self, time: float) -> None:
        """
        Adjust service levels using PID control.
        
        If miss ratio > target: lower service levels (faster execution)
        If miss ratio < target: raise service levels (better quality)
        """
        # Calculate actual miss ratio in recent history
        recent_misses = [miss for (t, miss) in self.miss_count_history if t >= time - self.sampling_period]
        actual_miss_ratio = sum(recent_misses) / len(recent_misses) if recent_misses else 0.0
        
        # Calculate PID error
        error = actual_miss_ratio - self.target_miss_ratio
        
        # PID control
        p_term = self.kp * error
        self.integral_error += error
        i_term = self.ki * self.integral_error
        d_term = self.kd * (error - self.previous_error)
        
        control_signal = p_term + i_term + d_term
        self.previous_error = error
        
        # Adjust each task's service level based on control signal
        for tv in self.tasks_with_versions:
            if control_signal > 0.1:  # Too many misses - lower level
                if tv.current_version_index > 0:
                    tv.current_version_index -= 1
            elif control_signal < -0.1:  # Too few misses - raise level
                if tv.current_version_index < len(tv.versions) - 1:
                    tv.current_version_index += 1

