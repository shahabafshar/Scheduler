"""Overload handling algorithms: Imprecise computation, HVDF, and (m,k)-firm."""

from typing import List, Optional, Dict
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, ImpreciseTask, MkFirmTask


class ImpreciseComputationScheduler(SchedulerBase):
    """
    Imprecise computation scheduler.

    Tasks have mandatory and optional parts.
    During overload, optional parts may be skipped to guarantee mandatory completion.
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
        self.ready_queue: List[TaskInstance] = []  # Track for overload detection
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

    def is_overloaded(self, ready_queue: List[TaskInstance]) -> bool:
        """
        Check if system is overloaded based on current workload.

        Overload is detected when total remaining work exceeds available time.
        """
        if not ready_queue:
            return False

        # Calculate total remaining work
        total_work = sum(inst.remaining_time for inst in ready_queue)

        # Calculate available time until earliest deadline
        earliest_deadline = min(inst.deadline for inst in ready_queue)
        available_time = max(0, earliest_deadline - self.current_time)

        # Overloaded if work exceeds time
        return total_work > available_time

    def get_effective_computation_time(self, task_id: str, is_overloaded: bool) -> float:
        """
        Get effective computation time based on overload status.

        During overload: return mandatory time only
        Normal operation: return mandatory + optional time
        """
        mandatory = self.task_mandatory_times.get(task_id, 0.0)
        optional = self.task_optional_times.get(task_id, 0.0)

        if is_overloaded:
            return mandatory  # Skip optional part
        return mandatory + optional

    def simulate(self) -> 'ScheduleResult':
        """
        Run imprecise computation simulation.

        During overload, optional parts are skipped to guarantee mandatory completion.
        """
        from ..task import ScheduleResult, ScheduleEvent

        self.assign_priorities()

        # Initialize tracking
        self.timeline = []
        self.task_instances = []
        self.deadline_misses = []
        busy_time = 0
        optional_skipped = {}  # task_id -> count of skipped optional parts

        # Track whether each instance has had optional skipped
        instance_optional_skipped: Dict[tuple, bool] = {}

        # Create initial instances at t=0
        for task in self.tasks:
            # Use full computation time initially
            instance = TaskInstance(
                task_id=task.id,
                instance_number=0,
                arrival_time=0.0,
                deadline=float(task.deadline),
                remaining_time=task.computation_time
            )
            self.task_instances.append(instance)

        # Simulation loop
        for t in range(int(self.duration)):
            self.current_time = float(t)

            # Create new instances at period boundaries
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

            # Build ready queue
            ready_queue = [inst for inst in self.task_instances
                          if inst.remaining_time > 0 and t >= inst.arrival_time]
            self.ready_queue = ready_queue

            # Check for overload
            overloaded = self.is_overloaded(ready_queue)

            # If overloaded, truncate tasks to mandatory-only
            if overloaded:
                for inst in ready_queue:
                    inst_key = (inst.task_id, inst.instance_number)
                    if inst_key not in instance_optional_skipped:
                        mandatory_time = self.task_mandatory_times.get(inst.task_id, inst.remaining_time)
                        # Calculate how much of optional we can skip
                        original_comp = next((t.computation_time for t in self.tasks if t.id == inst.task_id), inst.remaining_time)
                        executed_so_far = original_comp - inst.remaining_time

                        if executed_so_far < mandatory_time:
                            # Still in mandatory portion - can truncate at mandatory boundary
                            new_remaining = max(0, mandatory_time - executed_so_far)
                            if new_remaining < inst.remaining_time:
                                skipped = inst.remaining_time - new_remaining
                                inst.remaining_time = new_remaining
                                optional_skipped[inst.task_id] = optional_skipped.get(inst.task_id, 0) + 1
                                instance_optional_skipped[inst_key] = True
                                self.timeline.append(ScheduleEvent(
                                    time=float(t), task_id=inst.task_id, event_type='optional_skipped',
                                    details={'instance': inst.instance_number, 'skipped_time': skipped}
                                ))

            # Check deadline misses
            for inst in self.task_instances:
                if inst.remaining_time > 0 and t > inst.deadline:
                    if not any(dm.details.get('instance') == inst.instance_number
                              for dm in self.deadline_misses if dm.task_id == inst.task_id):
                        self.deadline_misses.append(ScheduleEvent(
                            time=float(t), task_id=inst.task_id, event_type='deadline_miss',
                            details={'instance': inst.instance_number}
                        ))

            # Re-build ready queue after potential truncation
            ready_queue = [inst for inst in self.task_instances
                          if inst.remaining_time > 0 and t >= inst.arrival_time]
            ready_queue.sort(key=lambda x: (-self.get_task_priority(x.task_id), x.task_id))

            # Select next task
            next_task = self.get_next_task(ready_queue)

            # Handle preemption
            if self.running_task and next_task != self.running_task:
                if self.running_task.remaining_time > 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t), task_id=self.running_task.task_id, event_type='preempt',
                        details={'instance': self.running_task.instance_number}
                    ))

            # Start new task
            if next_task and next_task != self.running_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=next_task.task_id, event_type='start',
                    details={'instance': next_task.instance_number, 'overloaded': overloaded}
                ))
                self.running_task = next_task

            # Execute
            if self.running_task:
                self.running_task.remaining_time -= 1
                busy_time += 1

                if self.running_task.remaining_time <= 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t + 1), task_id=self.running_task.task_id, event_type='complete',
                        details={'instance': self.running_task.instance_number}
                    ))
                    self.running_task = None
            else:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=None, event_type='idle', details={}
                ))

        # Sort timeline
        self.timeline.sort(key=lambda e: e.time)

        # Calculate metrics
        context_switches = sum(1 for e in self.timeline if e.event_type in ['start', 'preempt'])
        cpu_util = busy_time / self.duration if self.duration > 0 else 0.0

        return ScheduleResult(
            algorithm="Imprecise Computation",
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=context_switches,
            cpu_utilization=cpu_util,
            response_times={},
            details={'optional_skipped': optional_skipped}
        )


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
    Tasks at risk of violating (m,k) constraints get higher priority.
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
        self.task_history = {t.id: [] for t in mk_tasks}  # Track deadline meets
        self.completed_instances: set = set()  # Track (task_id, instance_number)
        super().__init__(tasks, duration)

    def assign_priorities(self) -> None:
        """Assign RMS priorities."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i

    def is_at_risk(self, task_id: str) -> bool:
        """
        Check if task is at risk of violating (m,k) constraint.

        A task is "at risk" if missing the next deadline would violate (m,k).
        At-risk tasks should be prioritized to meet their constraint.
        """
        if task_id not in self.mk_tasks:
            return False

        mk_task = self.mk_tasks[task_id]
        history = self.task_history.get(task_id, [])

        if len(history) < mk_task.k - 1:
            return False  # Not enough history to be at risk

        # Check if missing next deadline would violate constraint
        # Look at last (k-1) instances + assume next misses
        recent = history[-(mk_task.k - 1):] if len(history) >= mk_task.k - 1 else history
        meets_count = sum(1 for met in recent if met)

        # If we miss the next one, would we violate (m,k)?
        return meets_count < mk_task.m

    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """
        Select task with (m,k)-aware priority.

        1. Skip tasks that have already violated their (m,k) constraint
        2. Tasks at risk of violating (m,k) get higher priority
        3. Among non-at-risk tasks, use RMS priority
        """
        if not ready_queue:
            return None

        # Filter out tasks that have ALREADY violated their (m,k) constraint
        # These instances are "useless" - constraint already failed
        schedulable = [inst for inst in ready_queue
                      if self.check_mk_constraint(inst.task_id)]

        if not schedulable:
            # All tasks have violated constraints - still schedule by RMS
            # (system is in failure mode but should continue operating)
            ready_queue.sort(key=lambda x: (-self.get_task_priority(x.task_id), x.task_id))
            return ready_queue[0]

        # Separate at-risk and normal tasks (only from schedulable tasks)
        at_risk = [inst for inst in schedulable if self.is_at_risk(inst.task_id)]
        normal = [inst for inst in schedulable if not self.is_at_risk(inst.task_id)]

        # At-risk tasks get priority (sorted by RMS among themselves)
        if at_risk:
            at_risk.sort(key=lambda x: (-self.get_task_priority(x.task_id), x.task_id))
            return at_risk[0]

        # Normal RMS priority
        if normal:
            normal.sort(key=lambda x: (-self.get_task_priority(x.task_id), x.task_id))
            return normal[0]

        return None

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

    def simulate(self) -> 'ScheduleResult':
        """
        Run (m,k)-firm aware simulation.

        Extends base simulation to:
        1. Track deadline results for (m,k) constraint checking
        2. Prioritize at-risk tasks
        """
        from ..task import ScheduleResult, ScheduleEvent

        self.assign_priorities()

        # Initialize tracking
        self.timeline = []
        self.task_instances = []
        self.deadline_misses = []
        self.completed_instances = set()
        busy_time = 0

        # Create initial instances at t=0
        for task in self.tasks:
            instance = TaskInstance(
                task_id=task.id,
                instance_number=0,
                arrival_time=0.0,
                deadline=float(task.deadline),
                remaining_time=task.computation_time
            )
            self.task_instances.append(instance)

        # Simulation loop
        for t in range(int(self.duration)):
            self.current_time = float(t)

            # Create new instances at period boundaries
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

            # Build ready queue
            ready_queue = [inst for inst in self.task_instances
                          if inst.remaining_time > 0 and t >= inst.arrival_time]

            # Check deadline misses and record results
            for inst in self.task_instances:
                inst_key = (inst.task_id, inst.instance_number)
                if inst.remaining_time > 0 and t > inst.deadline:
                    # Deadline missed
                    if inst_key not in self.completed_instances:
                        self.deadline_misses.append(ScheduleEvent(
                            time=float(t), task_id=inst.task_id, event_type='deadline_miss',
                            details={'instance': inst.instance_number}
                        ))
                        # Record miss for (m,k) tracking
                        self.record_deadline_result(inst.task_id, False)
                        self.completed_instances.add(inst_key)

            # Select next task (with (m,k) awareness)
            next_task = self.get_next_task(ready_queue)

            # Handle preemption
            if self.running_task and next_task != self.running_task:
                if self.running_task.remaining_time > 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t), task_id=self.running_task.task_id, event_type='preempt',
                        details={'instance': self.running_task.instance_number}
                    ))

            # Start new task
            if next_task and next_task != self.running_task:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=next_task.task_id, event_type='start',
                    details={'instance': next_task.instance_number, 'at_risk': self.is_at_risk(next_task.task_id)}
                ))
                self.running_task = next_task

            # Execute
            if self.running_task:
                self.running_task.remaining_time -= 1
                busy_time += 1

                if self.running_task.remaining_time <= 0:
                    completion_time = t + 1
                    inst_key = (self.running_task.task_id, self.running_task.instance_number)

                    # Check if deadline was met
                    met_deadline = completion_time <= self.running_task.deadline
                    if inst_key not in self.completed_instances:
                        self.record_deadline_result(self.running_task.task_id, met_deadline)
                        self.completed_instances.add(inst_key)

                    self.timeline.append(ScheduleEvent(
                        time=float(completion_time), task_id=self.running_task.task_id, event_type='complete',
                        details={'instance': self.running_task.instance_number, 'met_deadline': met_deadline}
                    ))
                    self.running_task = None
            else:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=None, event_type='idle', details={}
                ))

        # Sort timeline
        self.timeline.sort(key=lambda e: e.time)

        # Calculate metrics
        context_switches = sum(1 for e in self.timeline if e.event_type in ['start', 'preempt'])
        cpu_util = busy_time / self.duration if self.duration > 0 else 0.0

        return ScheduleResult(
            algorithm="(m,k)-firm RMS",
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=context_switches,
            cpu_utilization=cpu_util,
            response_times={},
            details={'task_history': self.task_history}
        )

