"""Feedback-based (m,k)-RMS scheduler with dynamic failure rate control."""

from typing import List, Dict, Optional, Tuple
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, ScheduleEvent, ScheduleResult, MkFirmTask


class FeedbackMkFirmScheduler(SchedulerBase):
    """
    Feedback-based (m,k)-firm RMS scheduler.
    
    Uses PID control to adjust m_i values dynamically based on DFR (Dynamic Failure Rate).
    Maximizes Marginal Quality Received (MQR) while maintaining (m,k) guarantees.
    """
    
    def __init__(self, mk_tasks: List[MkFirmTask],
                 target_dfr: float = 0.05,
                 kp: float = 0.1, ki: float = 0.01, kd: float = 0.05,
                 sampling_period: int = 10,
                 duration: int = 100):
        """
        Initialize Feedback (m,k)-RMS scheduler.
        
        Args:
            mk_tasks: List of (m,k)-firm tasks
            target_dfr: Target dynamic failure rate (0-1)
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            sampling_period: How often to adjust mi values
            duration: Simulation duration
        """
        # Convert to regular PeriodicTask objects
        tasks = [
            PeriodicTask(
                id=t.id,
                computation_time=t.computation_time,
                period=t.period,
                deadline=t.deadline
            )
            for t in mk_tasks
        ]
        
        super().__init__(tasks, duration)
        
        self.mk_tasks = mk_tasks
        self.target_dfr = target_dfr
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.sampling_period = sampling_period
        
        # Track (m,k) guarantee history for each task
        # Format: {task_id: [(instance_num, deadline_met), ...]}
        self.task_history = {task.id: [] for task in mk_tasks}
        
        # Current effective m values (adjusted by feedback)
        self.current_m_values = {task.id: task.m for task in mk_tasks}
        
        # PID control state
        self.integral_error = 0.0
        self.previous_error = 0.0
        
        # DFR history for visualization
        self.dfr_history = []  # [(time, dfr), ...]
        self.mqr_history = {task.id: [] for task in mk_tasks}  # {(time, mqr), ...}
        
    def assign_priorities(self) -> None:
        """Assign RMS priorities based on periods."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task (RMS)."""
        if not ready_queue:
            return None
        
        # Sort by priority (use task_id as tie-breaker for deterministic results)
        ready_queue.sort(key=lambda x: (-self.get_task_priority(x.task_id), x.task_id))
        return ready_queue[0]
    
    def simulate(self) -> ScheduleResult:
        """Run simulation with dynamic m value adjustment."""
        # Assign priorities
        self.assign_priorities()
        
        # Initialize task instances
        for task in self.tasks:
            self.task_instances.append(TaskInstance(
                task_id=task.id,
                instance_number=0,
                arrival_time=0.0,
                deadline=float(task.deadline),
                remaining_time=task.computation_time
            ))
        
        # Run simulation
        for t in range(int(self.duration)):
            self.current_time = float(t)
            
            # Sample DFR and adjust m values periodically
            if t > 0 and t % self.sampling_period == 0:
                self._adjust_m_values(t)
            
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
            
            # Update ready queue
            # Note: Tasks remain eligible even after deadline (they just miss the constraint)
            ready_queue = [inst for inst in self.task_instances
                          if inst.remaining_time > 0 and t >= inst.arrival_time]
            ready_queue.sort(key=lambda x: (-self.get_task_priority(x.task_id), x.task_id))
            
            # Check deadline misses (t > deadline, not >=, since at t=deadline task is still "at deadline")
            for inst in self.task_instances:
                if inst.remaining_time > 0 and t > inst.deadline:
                    if not any(dm.details.get('instance') == inst.instance_number 
                              for dm in self.deadline_misses if dm.task_id == inst.task_id):
                        self.deadline_misses.append(ScheduleEvent(
                            time=float(t), task_id=inst.task_id, event_type='deadline_miss',
                            details={'instance': inst.instance_number}
                        ))
                        # Record deadline miss in history
                        self.task_history[inst.task_id].append((inst.instance_number, False))
            
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
                
                if self.running_task.remaining_time <= 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t+1), task_id=self.running_task.task_id, event_type='complete',
                        details={'instance': self.running_task.instance_number}
                    ))
                    # Record successful completion in history
                    self.task_history[self.running_task.task_id].append((self.running_task.instance_number, True))
                    self.running_task = None
            
            if not self.running_task and not next_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=None, event_type='idle', details={}
                ))
        
        self.timeline.sort(key=lambda e: e.time)
        
        # Store diagnostic data in scheduler for later access
        self.diagnostic_details = {
            'current_m_values': self.current_m_values,
            'dfr_history': self.dfr_history,
            'mqr_history': self.mqr_history,
            'task_history': self.task_history
        }

        return ScheduleResult(
            algorithm="Feedback (m,k)-RMS",
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=sum(1 for e in self.timeline if e.event_type in ['start', 'preempt']),
            cpu_utilization=sum(1 for e in self.timeline if e.task_id and e.event_type == 'start') / self.duration,
            response_times={}
        )
    
    def _calculate_dynamic_failure_rate(self, task_id: str) -> float:
        """
        Calculate Dynamic Failure Rate (DFR) for a task.
        
        DFR = (k - actual_m) / k
        where actual_m = number of deadlines met in last k instances
        """
        task = next((t for t in self.mk_tasks if t.id == task_id), None)
        if not task:
            return 0.0
        
        k = task.k
        history = self.task_history.get(task_id, [])
        
        # Get last k instances
        recent_history = history[-k:] if len(history) >= k else history
        
        # Count deadlines met
        deadlines_met = sum(1 for (_, met) in recent_history if met)
        
        # DFR
        dfr = (k - deadlines_met) / k if k > 0 else 0.0
        
        return dfr
    
    def _calculate_marginal_quality_received(self, task_id: str) -> float:
        """
        Calculate Marginal Quality Received (MQR) for a task.
        
        MQR = (mi - mi') / (ki - mi)
        where mi = original m, mi' = current adjusted m, ki = k parameter
        """
        task = next((t for t in self.mk_tasks if t.id == task_id), None)
        if not task:
            return 0.0
        
        original_m = task.m
        current_m = self.current_m_values.get(task_id, original_m)
        k = task.k
        
        if k == original_m:  # Avoid division by zero
            return 0.0
        
        mqr = (original_m - current_m) / (k - original_m)
        
        return mqr
    
    def _adjust_m_values(self, time: float) -> None:
        """
        Adjust m values using PID control based on DFR.
        
        If DFR > target: increase mi' (more lenient, lower quality)
        If DFR < target: decrease mi' (stricter, higher quality)
        """
        # Calculate overall DFR across all tasks
        total_dfr = 0.0
        for task in self.mk_tasks:
            task_dfr = self._calculate_dynamic_failure_rate(task.id)
            total_dfr += task_dfr
            
            # Calculate and record MQR
            mqr = self._calculate_marginal_quality_received(task.id)
            self.mqr_history[task.id].append((time, mqr))
        
        avg_dfr = total_dfr / len(self.mk_tasks) if self.mk_tasks else 0.0
        self.dfr_history.append((time, avg_dfr))
        
        # Calculate PID error
        error = avg_dfr - self.target_dfr
        
        # PID control
        p_term = self.kp * error
        self.integral_error += error
        i_term = self.ki * self.integral_error
        d_term = self.kd * (error - self.previous_error)
        
        control_signal = p_term + i_term + d_term
        self.previous_error = error
        
        # Adjust each task's m value based on control signal
        # Higher m = STRICTER (more deadlines must be met)
        # Lower m = MORE LENIENT (fewer deadlines must be met)
        for task in self.mk_tasks:
            current_m = self.current_m_values[task.id]

            if control_signal > 0.1:  # DFR too high (too many failures) - decrease m (more lenient)
                if current_m > 1:
                    self.current_m_values[task.id] = max(current_m - 1, 1)
            elif control_signal < -0.1:  # DFR too low (few failures) - increase m (stricter)
                if current_m < task.k:
                    self.current_m_values[task.id] = min(current_m + 1, task.k)

            # Note: Adjusted m values affect future guarantee checking
            # but don't change already-started task instances

