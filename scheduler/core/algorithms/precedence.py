"""Precedence-constrained scheduling algorithms.

Implements RMS, DMS, and EDF with precedence constraints per CprE 458/558.

Key formulas (all include predecessor completion time C_i):
- RMS: R_j* = Max(R_j, R_i* + C_i) for all predecessors i (forward pass)
- DMS: R_j* = Max(R_j, R_i* + C_i), D_j* = Max(D_j, D_i*) (forward for both)
- EDF: R_j* = Max(R_j, R_i* + C_i), D_i* = Min(D_i, D_j* - C_j) (forward + backward)

Note: DMS uses forward deadline propagation (successors inherit max from predecessors),
while EDF uses backward deadline propagation (predecessors constrained by successors).
"""

from typing import List, Optional, Dict, Set
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, PrecedenceConstraint, ScheduleEvent, ScheduleResult


def topological_sort(tasks: List[PeriodicTask], predecessor_map: Dict[str, List[str]]) -> List[str]:
    """
    Return tasks in topological order (predecessors before successors).

    Args:
        tasks: List of tasks
        predecessor_map: Mapping from task_id to list of predecessor task_ids

    Returns:
        List of task_ids in topological order
    """
    in_degree = {task.id: 0 for task in tasks}
    for task_id, preds in predecessor_map.items():
        in_degree[task_id] = len(preds)

    # Start with tasks that have no predecessors
    queue = [task.id for task in tasks if in_degree.get(task.id, 0) == 0]
    result = []

    # Build successor map
    successor_map: Dict[str, List[str]] = {task.id: [] for task in tasks}
    for task_id, preds in predecessor_map.items():
        for pred in preds:
            if pred in successor_map:
                successor_map[pred].append(task_id)

    while queue:
        task_id = queue.pop(0)
        result.append(task_id)

        for succ in successor_map.get(task_id, []):
            in_degree[succ] -= 1
            if in_degree[succ] == 0:
                queue.append(succ)

    return result


def reverse_topological_sort(tasks: List[PeriodicTask], successor_map: Dict[str, List[str]]) -> List[str]:
    """
    Return tasks in reverse topological order (successors before predecessors).

    Args:
        tasks: List of tasks
        successor_map: Mapping from task_id to list of successor task_ids

    Returns:
        List of task_ids in reverse topological order
    """
    out_degree = {task.id: len(successor_map.get(task.id, [])) for task in tasks}

    # Start with tasks that have no successors
    queue = [task.id for task in tasks if out_degree.get(task.id, 0) == 0]
    result = []

    # Build predecessor map
    predecessor_map: Dict[str, List[str]] = {task.id: [] for task in tasks}
    for task_id, succs in successor_map.items():
        for succ in succs:
            if succ in predecessor_map:
                predecessor_map[succ].append(task_id)

    while queue:
        task_id = queue.pop(0)
        result.append(task_id)

        for pred in predecessor_map.get(task_id, []):
            out_degree[pred] -= 1
            if out_degree[pred] == 0:
                queue.append(pred)

    return result


class RMSWithPrecedence(SchedulerBase):
    """
    RMS with precedence constraints.

    Modifies ready times based on precedence graph (forward pass only).
    Formula: R_j* = Max(R_j, R_i*) for all predecessors i

    Priority: Uses RMS (shorter period = higher priority) with precedence tie-breaking.
    """

    def __init__(self, tasks: List[PeriodicTask], precedences: List[PrecedenceConstraint],
                 duration: int = 100):
        """
        Initialize RMS scheduler with precedence constraints.

        Args:
            tasks: Periodic tasks
            precedences: List of precedence relationships
            duration: Simulation duration
        """
        super().__init__(tasks, duration)
        self.precedences = precedences
        self.predecessor_map = self._build_predecessor_map()
        self.successor_map = self._build_successor_map()

        # Store modified parameters
        self.modified_ready_times: Dict[str, float] = {}

    def _build_predecessor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its predecessors."""
        predecessor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.successor in predecessor_map:
                predecessor_map[prec.successor].append(prec.predecessor)
        return predecessor_map

    def _build_successor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its successors."""
        successor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.predecessor in successor_map:
                successor_map[prec.predecessor].append(prec.successor)
        return successor_map

    def _compute_modified_ready_times(self) -> Dict[str, float]:
        """
        Compute modified ready times using forward pass in topological order.

        Formula: R_j* = Max(R_j, R_i* + C_i) for all predecessors i
        (Successor can't start until predecessor completes)

        Returns:
            Dictionary mapping task_id to modified ready time
        """
        modified = {}
        task_map = {task.id: task for task in self.tasks}

        # Process in topological order
        topo_order = topological_sort(self.tasks, self.predecessor_map)

        for task_id in topo_order:
            task = task_map.get(task_id)
            if not task:
                continue

            # Base ready time (0 for periodic tasks starting at time 0)
            base_ready = 0.0

            # Find max completion time from predecessors (R_i* + C_i)
            max_pred_completion = 0.0
            for pred_id in self.predecessor_map.get(task_id, []):
                pred_task = task_map.get(pred_id)
                if pred_id in modified and pred_task:
                    # R_i* + C_i = earliest completion time of predecessor
                    pred_completion = modified[pred_id] + pred_task.computation_time
                    max_pred_completion = max(max_pred_completion, pred_completion)

            # Modified ready time
            modified[task_id] = max(base_ready, max_pred_completion)

        return modified

    def assign_priorities(self) -> None:
        """
        Assign RMS priorities with precedence constraints.

        1. Base priority by period (shorter = higher)
        2. Ensure predecessors have higher priority than successors
        """
        # Base RMS priority assignment
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i

        # Ensure precedence: predecessors must have higher priority
        changed = True
        while changed:
            changed = False
            for prec in self.precedences:
                pred_task = next((t for t in self.tasks if t.id == prec.predecessor), None)
                succ_task = next((t for t in self.tasks if t.id == prec.successor), None)
                if pred_task and succ_task:
                    if pred_task.priority <= succ_task.priority:
                        # Predecessor must have strictly higher priority
                        pred_task.priority = succ_task.priority + 1
                        changed = True

    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task from ready queue."""
        if not ready_queue:
            return None
        return ready_queue[0]  # Already sorted by priority

    def simulate(self) -> ScheduleResult:
        """
        Run RMS simulation with precedence-modified ready times.
        """
        # Compute modified parameters BEFORE simulation
        self.modified_ready_times = self._compute_modified_ready_times()

        # Assign priorities
        self.assign_priorities()

        # Track execution
        busy_time = 0
        self.timeline = []
        self.deadline_misses = []
        self.task_instances = []

        task_map = {task.id: task for task in self.tasks}

        # Track completion times per (task_id, instance_number) for dynamic precedence
        self.instance_completion_times: Dict[tuple, float] = {}

        # Initialize: create first instances at modified ready times
        for task in self.tasks:
            modified_ready = self.modified_ready_times.get(task.id, 0.0)
            instance = TaskInstance(
                task_id=task.id,
                instance_number=0,
                arrival_time=modified_ready,
                deadline=float(task.deadline),
                remaining_time=task.computation_time
            )
            self.task_instances.append(instance)

        # Track completion times for precedence (legacy)
        completion_times: Dict[str, float] = {}

        # Simulation loop
        for t in range(int(self.duration)):
            self.current_time = float(t)

            # Create new instances at period boundaries
            for task in self.tasks:
                if task.period > 0:
                    instance_number = int(t // task.period)
                    if instance_number > 0:
                        arrival_time = instance_number * task.period

                        existing = any(
                            inst.task_id == task.id and inst.instance_number == instance_number
                            for inst in self.task_instances
                        )

                        if not existing and t >= arrival_time:
                            # Calculate dynamic ready time based on predecessor completion
                            actual_ready = self._get_dynamic_ready_time(task.id, instance_number, arrival_time)

                            instance = TaskInstance(
                                task_id=task.id,
                                instance_number=instance_number,
                                arrival_time=actual_ready,
                                deadline=arrival_time + task.deadline,
                                remaining_time=task.computation_time
                            )
                            self.task_instances.append(instance)

            # Build ready queue - only include tasks whose predecessors are complete
            ready_queue = []
            for inst in self.task_instances:
                if inst.remaining_time > 0 and t >= inst.arrival_time:
                    # Check if all predecessors have completed their corresponding instances
                    predecessors = self.predecessor_map.get(inst.task_id, [])
                    all_preds_done = True
                    for pred_id in predecessors:
                        # Find the corresponding predecessor instance based on time overlap
                        pred_inst = self._find_corresponding_predecessor_instance(
                            pred_id, inst.task_id, inst.instance_number, task_map
                        )
                        if pred_inst and pred_inst.remaining_time > 0:
                            all_preds_done = False
                            break

                    if all_preds_done:
                        ready_queue.append(inst)

            # Sort by priority (use task_id as tie-breaker for deterministic results)
            ready_queue.sort(key=lambda x: (-self.get_task_priority(x.task_id), x.task_id))

            # Check deadline misses (t > deadline, not >=, per RT theory)
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

            # Execute current task
            if self.running_task:
                self.running_task.remaining_time -= 1
                busy_time += 1

                if self.running_task.remaining_time <= 0:
                    # Task completed - record completion time for precedence tracking
                    completion_time = float(t + 1)
                    completion_times[self.running_task.task_id] = completion_time
                    inst_key = (self.running_task.task_id, self.running_task.instance_number)
                    self.instance_completion_times[inst_key] = completion_time

                    self.timeline.append(ScheduleEvent(
                        time=completion_time, task_id=self.running_task.task_id, event_type='complete',
                        details={'instance': self.running_task.instance_number}
                    ))
                    self.running_task = None
            else:
                # Idle
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=None, event_type='idle', details={}
                ))

        # Sort and return result
        self.timeline.sort(key=lambda e: e.time)
        context_switches = sum(1 for e in self.timeline if e.event_type in ['start', 'preempt'])
        cpu_util = busy_time / self.duration if self.duration > 0 else 0.0

        return ScheduleResult(
            algorithm="RMS with Precedence",
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=context_switches,
            cpu_utilization=cpu_util,
            response_times={}
        )

    def _get_dynamic_ready_time(self, task_id: str, instance_number: int, base_arrival: float) -> float:
        """
        Calculate dynamic ready time based on actual predecessor completion.

        R*_j = Max(arrival_time, completion_time(predecessor_instance))

        Args:
            task_id: The successor task
            instance_number: Instance number of the successor
            base_arrival: Base arrival time for this instance

        Returns:
            Actual ready time accounting for predecessor completion
        """
        task_map = {task.id: task for task in self.tasks}
        max_ready = base_arrival

        # Check all predecessors
        for pred_id in self.predecessor_map.get(task_id, []):
            # Find the corresponding predecessor instance
            pred_inst_num = self._get_corresponding_pred_instance_number(
                pred_id, task_id, instance_number, task_map
            )

            # Get predecessor completion time
            pred_key = (pred_id, pred_inst_num)
            if pred_key in self.instance_completion_times:
                pred_completion = self.instance_completion_times[pred_key]
                max_ready = max(max_ready, pred_completion)

        return max_ready

    def _get_corresponding_pred_instance_number(self, pred_id: str, succ_id: str,
                                                 succ_instance: int, task_map: Dict) -> int:
        """
        Find the predecessor instance number that corresponds to a successor instance.

        When tasks have different periods, instance numbers don't match directly.
        We need to find which predecessor instance's execution window overlaps
        with the successor instance's arrival.
        """
        pred_task = task_map.get(pred_id)
        succ_task = task_map.get(succ_id)

        if not pred_task or not succ_task:
            return succ_instance  # Fallback

        # Calculate successor arrival time
        succ_arrival = succ_instance * succ_task.period

        # Find which predecessor instance covers this time
        # The predecessor instance i covers time [i*P_pred, (i+1)*P_pred)
        pred_instance = int(succ_arrival // pred_task.period)

        return pred_instance

    def _find_corresponding_predecessor_instance(self, pred_id: str, succ_id: str,
                                                  succ_instance: int, task_map: Dict) -> Optional[TaskInstance]:
        """
        Find the corresponding predecessor instance for a successor instance.

        Also checks for any EARLIER predecessor instances that haven't completed yet.
        If an earlier predecessor is still running, successor must wait.

        Args:
            pred_id: Predecessor task ID
            succ_id: Successor task ID
            succ_instance: Successor instance number
            task_map: Map of task_id to task

        Returns:
            The predecessor TaskInstance that is blocking (incomplete), or None if all done
        """
        pred_inst_num = self._get_corresponding_pred_instance_number(
            pred_id, succ_id, succ_instance, task_map
        )

        # Check ALL predecessor instances up to and including the corresponding one
        # If ANY earlier instance is still running, return that (it blocks the successor)
        for inst in self.task_instances:
            if inst.task_id == pred_id and inst.instance_number <= pred_inst_num:
                if inst.remaining_time > 0:
                    # This predecessor instance is still running - blocks successor
                    return inst

        return None  # All relevant predecessor instances are complete


class DMSWithPrecedence(SchedulerBase):
    """
    DMS with precedence constraints.

    Modifies both ready times and deadlines based on precedence.
    - Forward pass: R_j* = Max(R_j, R_i*)
    - Backward pass: D_j* = Max(D_j, D_i*)

    Priority: Uses DMS (shorter deadline = higher priority).
    """

    def __init__(self, tasks: List[PeriodicTask], precedences: List[PrecedenceConstraint],
                 duration: int = 100):
        """Initialize DMS scheduler with precedence constraints."""
        super().__init__(tasks, duration)
        self.precedences = precedences
        self.predecessor_map = self._build_predecessor_map()
        self.successor_map = self._build_successor_map()

        # Store modified parameters
        self.modified_ready_times: Dict[str, float] = {}
        self.modified_deadlines: Dict[str, float] = {}

    def _build_predecessor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its predecessors."""
        predecessor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.successor in predecessor_map:
                predecessor_map[prec.successor].append(prec.predecessor)
        return predecessor_map

    def _build_successor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its successors."""
        successor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.predecessor in successor_map:
                successor_map[prec.predecessor].append(prec.successor)
        return successor_map

    def _compute_modified_ready_times(self) -> Dict[str, float]:
        """
        Compute modified ready times using forward pass.

        Formula: R_j* = Max(R_j, R_i* + C_i) for all predecessors i
        (Successor can't start until predecessor completes)
        """
        modified = {}
        task_map = {task.id: task for task in self.tasks}

        topo_order = topological_sort(self.tasks, self.predecessor_map)

        for task_id in topo_order:
            task = task_map.get(task_id)
            if not task:
                continue

            base_ready = 0.0
            max_pred_completion = 0.0

            for pred_id in self.predecessor_map.get(task_id, []):
                pred_task = task_map.get(pred_id)
                if pred_id in modified and pred_task:
                    # R_i* + C_i = earliest completion time of predecessor
                    pred_completion = modified[pred_id] + pred_task.computation_time
                    max_pred_completion = max(max_pred_completion, pred_completion)

            modified[task_id] = max(base_ready, max_pred_completion)

        return modified

    def _compute_modified_deadlines(self) -> Dict[str, float]:
        """
        Compute modified deadlines using forward pass (DMS-style).

        Formula: D_j* = Max(D_j, D_i*) for all predecessors i

        This ensures successors have deadlines at least as late as their predecessors,
        which prevents impossible scheduling where successor deadline < predecessor deadline.
        Note: This differs from EDF which uses backward propagation (Min formula).
        """
        modified = {}
        task_map = {task.id: task for task in self.tasks}

        # Process in topological order (predecessors first)
        topo_order = topological_sort(self.tasks, self.predecessor_map)

        for task_id in topo_order:
            task = task_map.get(task_id)
            if not task:
                continue

            # Start with task's own deadline
            base_deadline = float(task.deadline)

            # Find max deadline from predecessors
            max_pred_deadline = 0.0
            for pred_id in self.predecessor_map.get(task_id, []):
                if pred_id in modified:
                    max_pred_deadline = max(max_pred_deadline, modified[pred_id])

            # Modified deadline is max of own and predecessors
            modified[task_id] = max(base_deadline, max_pred_deadline)

        return modified

    def assign_priorities(self) -> None:
        """
        Assign DMS priorities based on modified deadlines.

        Shorter deadline = higher priority.
        """
        # Compute modified deadlines first
        self.modified_deadlines = self._compute_modified_deadlines()

        # Sort by modified deadline
        sorted_tasks = sorted(self.tasks, key=lambda t: self.modified_deadlines.get(t.id, t.deadline))
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i

        # Ensure precedence constraints
        changed = True
        while changed:
            changed = False
            for prec in self.precedences:
                pred_task = next((t for t in self.tasks if t.id == prec.predecessor), None)
                succ_task = next((t for t in self.tasks if t.id == prec.successor), None)
                if pred_task and succ_task:
                    if pred_task.priority <= succ_task.priority:
                        pred_task.priority = succ_task.priority + 1
                        changed = True

    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task from ready queue."""
        if not ready_queue:
            return None
        return ready_queue[0]

    def _get_corresponding_pred_instance_number(self, pred_id: str, succ_id: str,
                                                 succ_instance: int, task_map: Dict) -> int:
        """
        Find the predecessor instance number that corresponds to a successor instance.

        When tasks have different periods, instance numbers don't match directly.
        """
        pred_task = task_map.get(pred_id)
        succ_task = task_map.get(succ_id)

        if not pred_task or not succ_task:
            return succ_instance  # Fallback

        # Calculate successor arrival time
        succ_arrival = succ_instance * succ_task.period

        # Find which predecessor instance covers this time
        pred_instance = int(succ_arrival // pred_task.period)

        return pred_instance

    def _find_corresponding_predecessor_instance(self, pred_id: str, succ_id: str,
                                                  succ_instance: int, task_map: Dict) -> Optional[TaskInstance]:
        """
        Find the corresponding predecessor instance for a successor instance.

        Also checks for any EARLIER predecessor instances that haven't completed yet.
        """
        pred_inst_num = self._get_corresponding_pred_instance_number(
            pred_id, succ_id, succ_instance, task_map
        )

        # Check ALL predecessor instances up to and including the corresponding one
        for inst in self.task_instances:
            if inst.task_id == pred_id and inst.instance_number <= pred_inst_num:
                if inst.remaining_time > 0:
                    return inst  # This predecessor instance is still running

        return None  # All relevant predecessor instances are complete

    def simulate(self) -> ScheduleResult:
        """Run DMS simulation with precedence-modified parameters."""
        # Compute modified parameters
        self.modified_ready_times = self._compute_modified_ready_times()
        self.modified_deadlines = self._compute_modified_deadlines()

        # Assign priorities
        self.assign_priorities()

        # Track execution
        busy_time = 0
        self.timeline = []
        self.deadline_misses = []
        self.task_instances = []

        task_map = {task.id: task for task in self.tasks}

        # Initialize instances with modified parameters
        for task in self.tasks:
            modified_ready = self.modified_ready_times.get(task.id, 0.0)
            modified_deadline = self.modified_deadlines.get(task.id, float(task.deadline))

            instance = TaskInstance(
                task_id=task.id,
                instance_number=0,
                arrival_time=modified_ready,
                deadline=modified_deadline,
                remaining_time=task.computation_time
            )
            self.task_instances.append(instance)

        # Simulation loop
        for t in range(int(self.duration)):
            self.current_time = float(t)

            # Create new instances at period boundaries
            for task in self.tasks:
                if task.period > 0:
                    instance_number = int(t // task.period)
                    if instance_number > 0:
                        arrival_time = instance_number * task.period
                        modified_ready = self.modified_ready_times.get(task.id, 0.0)
                        modified_deadline = self.modified_deadlines.get(task.id, float(task.deadline))

                        existing = any(
                            inst.task_id == task.id and inst.instance_number == instance_number
                            for inst in self.task_instances
                        )

                        if not existing and t >= arrival_time:
                            instance = TaskInstance(
                                task_id=task.id,
                                instance_number=instance_number,
                                arrival_time=arrival_time + modified_ready,
                                deadline=arrival_time + modified_deadline,
                                remaining_time=task.computation_time
                            )
                            self.task_instances.append(instance)

            # Build ready queue with precedence check (using period-aware instance matching)
            # Note: Tasks remain eligible even after deadline (they just miss the constraint)
            ready_queue = []
            for inst in self.task_instances:
                if inst.remaining_time > 0 and t >= inst.arrival_time:
                    predecessors = self.predecessor_map.get(inst.task_id, [])
                    all_preds_done = True
                    for pred_id in predecessors:
                        # Use period-aware instance matching for different periods
                        pred_inst = self._find_corresponding_predecessor_instance(
                            pred_id, inst.task_id, inst.instance_number, task_map
                        )
                        if pred_inst and pred_inst.remaining_time > 0:
                            all_preds_done = False
                            break

                    if all_preds_done:
                        ready_queue.append(inst)

            # Sort by priority (use task_id as tie-breaker for deterministic results)
            ready_queue.sort(key=lambda x: (-self.get_task_priority(x.task_id), x.task_id))

            # Check deadline misses (t > deadline, not >=)
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

            # Execute current task
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

        # Return result
        self.timeline.sort(key=lambda e: e.time)
        context_switches = sum(1 for e in self.timeline if e.event_type in ['start', 'preempt'])
        cpu_util = busy_time / self.duration if self.duration > 0 else 0.0

        return ScheduleResult(
            algorithm="DMS with Precedence",
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=context_switches,
            cpu_utilization=cpu_util,
            response_times={}
        )


class EDFWithPrecedence(SchedulerBase):
    """
    EDF with precedence constraints.

    Modifies ready times and deadlines based on precedence graph.
    - Forward pass: R_j* = Max(R_j, R_i* + C_i) (accounts for predecessor completion)
    - Backward pass: D_i* = Min(D_i, D_j* - C_j)

    Uses dynamic EDF priorities based on modified deadlines.
    """

    # EDF uses dynamic priority selection, skip redundant base class sorting
    _skip_priority_sort = True

    def __init__(self, tasks: List[PeriodicTask], precedences: List[PrecedenceConstraint],
                 duration: int = 100):
        """Initialize EDF scheduler with precedence constraints."""
        super().__init__(tasks, duration)
        self.precedences = precedences
        self.predecessor_map = self._build_predecessor_map()
        self.successor_map = self._build_successor_map()

        # Store modified parameters
        self.modified_ready_times: Dict[str, float] = {}
        self.modified_deadlines: Dict[str, float] = {}

    def _build_predecessor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its predecessors."""
        predecessor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.successor in predecessor_map:
                predecessor_map[prec.successor].append(prec.predecessor)
        return predecessor_map

    def _build_successor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its successors."""
        successor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.predecessor in successor_map:
                successor_map[prec.predecessor].append(prec.successor)
        return successor_map

    def _compute_modified_ready_times(self) -> Dict[str, float]:
        """
        Compute modified ready times using forward pass.

        Formula: R_j* = Max(R_j, R_i* + C_i) for all predecessors i

        This accounts for predecessor's completion time, not just ready time.
        """
        modified = {}
        task_map = {task.id: task for task in self.tasks}

        topo_order = topological_sort(self.tasks, self.predecessor_map)

        for task_id in topo_order:
            task = task_map.get(task_id)
            if not task:
                continue

            base_ready = 0.0
            max_pred_completion = 0.0

            for pred_id in self.predecessor_map.get(task_id, []):
                pred_task = task_map.get(pred_id)
                if pred_id in modified and pred_task:
                    # R_i* + C_i = earliest completion time of predecessor
                    pred_completion = modified[pred_id] + pred_task.computation_time
                    max_pred_completion = max(max_pred_completion, pred_completion)

            modified[task_id] = max(base_ready, max_pred_completion)

        return modified

    def _compute_modified_deadlines(self) -> Dict[str, float]:
        """
        Compute modified deadlines using backward pass.

        Formula: D_i* = Min(D_i, D_j* - C_j) for all successors j

        Process in reverse topological order (successors before predecessors).
        """
        modified = {}
        task_map = {task.id: task for task in self.tasks}

        # Process in reverse topological order
        reverse_order = reverse_topological_sort(self.tasks, self.successor_map)

        for task_id in reverse_order:
            task = task_map.get(task_id)
            if not task:
                continue

            # Start with task's own deadline
            base_deadline = float(task.deadline)
            min_succ_constraint = float('inf')

            for succ_id in self.successor_map.get(task_id, []):
                succ_task = task_map.get(succ_id)
                if succ_id in modified and succ_task:
                    # D_j* - C_j = latest start time of successor
                    succ_constraint = modified[succ_id] - succ_task.computation_time
                    min_succ_constraint = min(min_succ_constraint, succ_constraint)

            if min_succ_constraint == float('inf'):
                modified[task_id] = base_deadline
            else:
                modified[task_id] = min(base_deadline, min_succ_constraint)

        return modified

    def assign_priorities(self) -> None:
        """EDF uses dynamic priorities based on absolute deadlines (no fixed assignment)."""
        pass

    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select task with earliest modified deadline (EDF)."""
        if not ready_queue:
            return None

        # Sort by modified deadline (earliest first), tie-break by task_id for determinism
        return min(ready_queue, key=lambda inst: (inst.deadline, inst.task_id))

    def _get_corresponding_pred_instance_number(self, pred_id: str, succ_id: str,
                                                 succ_instance: int, task_map: Dict) -> int:
        """
        Find the predecessor instance number that corresponds to a successor instance.

        When tasks have different periods, instance numbers don't match directly.
        """
        pred_task = task_map.get(pred_id)
        succ_task = task_map.get(succ_id)

        if not pred_task or not succ_task:
            return succ_instance  # Fallback

        # Calculate successor arrival time
        succ_arrival = succ_instance * succ_task.period

        # Find which predecessor instance covers this time
        pred_instance = int(succ_arrival // pred_task.period)

        return pred_instance

    def _find_corresponding_predecessor_instance(self, pred_id: str, succ_id: str,
                                                  succ_instance: int, task_map: Dict) -> Optional[TaskInstance]:
        """
        Find the corresponding predecessor instance for a successor instance.

        Also checks for any EARLIER predecessor instances that haven't completed yet.
        """
        pred_inst_num = self._get_corresponding_pred_instance_number(
            pred_id, succ_id, succ_instance, task_map
        )

        # Check ALL predecessor instances up to and including the corresponding one
        for inst in self.task_instances:
            if inst.task_id == pred_id and inst.instance_number <= pred_inst_num:
                if inst.remaining_time > 0:
                    return inst  # This predecessor instance is still running

        return None  # All relevant predecessor instances are complete

    def simulate(self) -> ScheduleResult:
        """Run EDF simulation with precedence-modified parameters."""
        # Compute modified parameters
        self.modified_ready_times = self._compute_modified_ready_times()
        self.modified_deadlines = self._compute_modified_deadlines()

        # Track execution
        busy_time = 0
        self.timeline = []
        self.deadline_misses = []
        self.task_instances = []

        task_map = {task.id: task for task in self.tasks}

        # Initialize instances with modified parameters
        for task in self.tasks:
            modified_ready = self.modified_ready_times.get(task.id, 0.0)
            modified_deadline = self.modified_deadlines.get(task.id, float(task.deadline))

            instance = TaskInstance(
                task_id=task.id,
                instance_number=0,
                arrival_time=modified_ready,
                deadline=modified_deadline,
                remaining_time=task.computation_time
            )
            self.task_instances.append(instance)

        # Simulation loop
        for t in range(int(self.duration)):
            self.current_time = float(t)

            # Create new instances at period boundaries
            for task in self.tasks:
                if task.period > 0:
                    instance_number = int(t // task.period)
                    if instance_number > 0:
                        arrival_time = instance_number * task.period
                        modified_ready = self.modified_ready_times.get(task.id, 0.0)
                        modified_deadline = self.modified_deadlines.get(task.id, float(task.deadline))

                        existing = any(
                            inst.task_id == task.id and inst.instance_number == instance_number
                            for inst in self.task_instances
                        )

                        if not existing and t >= arrival_time:
                            instance = TaskInstance(
                                task_id=task.id,
                                instance_number=instance_number,
                                arrival_time=arrival_time + modified_ready,
                                deadline=arrival_time + modified_deadline,
                                remaining_time=task.computation_time
                            )
                            self.task_instances.append(instance)

            # Build ready queue with precedence check (using period-aware instance matching)
            # Note: Tasks remain eligible even after deadline (they just miss the constraint)
            ready_queue = []
            for inst in self.task_instances:
                if inst.remaining_time > 0 and t >= inst.arrival_time:
                    predecessors = self.predecessor_map.get(inst.task_id, [])
                    all_preds_done = True
                    for pred_id in predecessors:
                        # Use period-aware instance matching for different periods
                        pred_inst = self._find_corresponding_predecessor_instance(
                            pred_id, inst.task_id, inst.instance_number, task_map
                        )
                        if pred_inst and pred_inst.remaining_time > 0:
                            all_preds_done = False
                            break

                    if all_preds_done:
                        ready_queue.append(inst)

            # Check deadline misses (t > deadline, not >=)
            for inst in self.task_instances:
                if inst.remaining_time > 0 and t > inst.deadline:
                    if not any(dm.details.get('instance') == inst.instance_number
                              for dm in self.deadline_misses if dm.task_id == inst.task_id):
                        self.deadline_misses.append(ScheduleEvent(
                            time=float(t), task_id=inst.task_id, event_type='deadline_miss',
                            details={'instance': inst.instance_number}
                        ))

            # Select next task (EDF - earliest deadline)
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
                    details={'instance': next_task.instance_number}
                ))
                self.running_task = next_task

            # Execute current task
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

        # Return result
        self.timeline.sort(key=lambda e: e.time)
        context_switches = sum(1 for e in self.timeline if e.event_type in ['start', 'preempt'])
        cpu_util = busy_time / self.duration if self.duration > 0 else 0.0

        return ScheduleResult(
            algorithm="EDF with Precedence",
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=context_switches,
            cpu_utilization=cpu_util,
            response_times={}
        )
