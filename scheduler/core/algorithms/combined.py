"""Combined scheduling of periodic and aperiodic tasks using servers.

Implements server-based scheduling algorithms per CprE 458/558 course materials:
- Polling Server: Non-bandwidth-preserving (capacity lost if no aperiodic tasks)
- Deferrable Server: Bandwidth-preserving (capacity preserved until used)
- Sporadic Server: Dynamic replenishment (best response time)
"""

from abc import abstractmethod
from typing import List, Optional, Dict, Tuple
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, AperiodicTask, TaskInstance, ScheduleResult, ScheduleEvent
import math


class ServerScheduler(SchedulerBase):
    """
    Base class for server-based scheduling algorithms.

    Creates a periodic server to handle aperiodic tasks.
    Server types: Polling, Deferrable, Sporadic

    Key difference from SchedulerBase: implements custom simulate() that
    properly handles server capacity management and aperiodic task servicing.
    """

    def __init__(self, tasks: List[PeriodicTask], aperiodic_tasks: List[AperiodicTask],
                 server_capacity: float, server_period: float, duration: int = 100):
        """
        Initialize server-based scheduler.

        Args:
            tasks: Periodic tasks (background workload)
            aperiodic_tasks: Aperiodic tasks to service (foreground workload)
            server_capacity: C_s - computation time budget for server per period
            server_period: P_s - period of server
            duration: Simulation duration
        """
        self.aperiodic_tasks = sorted(aperiodic_tasks, key=lambda t: t.arrival_time)
        self.server_capacity = server_capacity
        self.server_period = server_period
        self.server_remaining = server_capacity  # Current available capacity
        self.server_next_replenish = 0  # Time of next replenishment
        self.aperiodic_queue: List[AperiodicTask] = []  # Pending aperiodic tasks

        # Tracking for aperiodic task execution
        self.aperiodic_remaining: Dict[str, float] = {}  # task_id -> remaining computation
        self.aperiodic_completed: List[AperiodicTask] = []  # Completed aperiodic tasks
        self.current_aperiodic: Optional[AperiodicTask] = None  # Currently executing aperiodic

        # Create server as a periodic task (for priority calculation)
        self.server_task = PeriodicTask(
            id="Server",
            computation_time=server_capacity,
            period=server_period,
            deadline=server_period
        )

        # Store original periodic tasks separately
        self.periodic_tasks = list(tasks)

        # Pass all tasks including server to base class
        super().__init__(tasks + [self.server_task], duration)

    def assign_priorities(self) -> None:
        """Assign RMS priorities to ALL tasks including server (based on period)."""
        # RMS: shorter period = higher priority, with task ID as tie-breaker for determinism
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.period, t.id))
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i

    def _update_aperiodic_queue(self, time: float) -> None:
        """Add newly arrived aperiodic tasks to the queue."""
        for apt in self.aperiodic_tasks:
            if abs(time - apt.arrival_time) < 0.001:  # Floating point comparison
                if apt.id not in self.aperiodic_remaining:
                    self.aperiodic_queue.append(apt)
                    self.aperiodic_remaining[apt.id] = apt.computation_time

        # Sort by deadline (EDF for aperiodic tasks within server)
        self.aperiodic_queue.sort(key=lambda t: t.deadline)

    def _create_periodic_instances(self, t: int) -> None:
        """Create new periodic task instances at period boundaries."""
        for task in self.periodic_tasks:  # Only periodic tasks, not server
            periods_passed = int(t // task.period)
            arrival_time = periods_passed * task.period

            # Check if instance already exists
            existing = [inst for inst in self.task_instances
                       if inst.task_id == task.id and abs(inst.arrival_time - arrival_time) < 0.001]

            if not existing and arrival_time <= t:
                instance = TaskInstance(
                    task_id=task.id,
                    instance_number=periods_passed,
                    arrival_time=arrival_time,
                    deadline=arrival_time + task.deadline,
                    remaining_time=task.computation_time
                )
                self.task_instances.append(instance)

    def _get_ready_queue(self, t: int) -> List[TaskInstance]:
        """Get periodic tasks ready to execute."""
        # Note: Tasks remain eligible even after deadline (they just miss the constraint)
        ready = [inst for inst in self.task_instances
                if inst.remaining_time > 0 and t >= inst.arrival_time]
        ready.sort(key=lambda x: self.get_task_priority(x.task_id), reverse=True)
        return ready

    def _check_deadline_misses(self, t: int) -> None:
        """Check for deadline misses on periodic tasks."""
        for inst in self.task_instances:
            if inst.remaining_time > 0 and t > inst.deadline:
                if not any(dm.details.get('instance') == inst.instance_number
                          for dm in self.deadline_misses if dm.task_id == inst.task_id):
                    self.deadline_misses.append(ScheduleEvent(
                        time=float(t), task_id=inst.task_id, event_type='deadline_miss',
                        details={'instance': inst.instance_number}
                    ))

        # Check aperiodic deadline misses
        for apt in self.aperiodic_tasks:
            if apt.id in self.aperiodic_remaining:
                if self.aperiodic_remaining[apt.id] > 0 and t > apt.deadline:
                    if not any(dm.task_id == f"Aperiodic_{apt.id}" for dm in self.deadline_misses):
                        self.deadline_misses.append(ScheduleEvent(
                            time=float(t), task_id=f"Aperiodic_{apt.id}", event_type='deadline_miss',
                            details={'aperiodic': True}
                        ))

    def _should_server_run(self, ready_queue: List[TaskInstance], t: int) -> bool:
        """Determine if server should run based on RMS priority."""
        # Server runs if it's highest priority among ready tasks
        server_priority = self.server_task.priority

        # Check if any periodic task has higher priority
        for inst in ready_queue:
            task_priority = self.get_task_priority(inst.task_id)
            if task_priority > server_priority:
                return False

        return True

    @abstractmethod
    def _execute_server_slot(self, t: int) -> bool:
        """
        Execute server behavior for this time slot.
        Returns True if server actually executed (used CPU), False otherwise.

        Subclasses implement different behaviors:
        - Polling: Lose capacity if no aperiodic tasks
        - Deferrable: Preserve capacity if no aperiodic tasks
        - Sporadic: Dynamic replenishment
        """
        pass

    @abstractmethod
    def _handle_replenishment(self, t: int) -> None:
        """Handle server capacity replenishment."""
        pass

    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select next task based on RMS priority."""
        if not ready_queue:
            return None
        return ready_queue[0]

    def simulate(self) -> ScheduleResult:
        """
        Server-aware simulation loop.

        Key differences from base simulate():
        1. Manages server capacity (replenishment, consumption)
        2. Services aperiodic tasks when server runs
        3. Handles server-specific idle behavior
        """
        self.assign_priorities()

        # Initialize tracking
        self.timeline = []
        self.task_instances = []
        self.deadline_misses = []
        self.aperiodic_remaining = {}
        self.aperiodic_completed = []
        self.aperiodic_queue = []
        self.current_aperiodic = None
        self.running_task = None
        busy_time = 0

        # Create initial periodic task instances at t=0
        for task in self.periodic_tasks:
            instance = TaskInstance(
                task_id=task.id,
                instance_number=0,
                arrival_time=0.0,
                deadline=float(task.deadline),
                remaining_time=task.computation_time
            )
            self.task_instances.append(instance)

        for t in range(int(self.duration)):
            self.current_time = float(t)

            # 1. Check for aperiodic arrivals
            self._update_aperiodic_queue(t)

            # 2. Handle server replenishment
            self._handle_replenishment(t)

            # 3. Create new periodic task instances
            self._create_periodic_instances(t)

            # 4. Check deadline misses
            self._check_deadline_misses(t)

            # 5. Build ready queue for periodic tasks
            ready_queue = self._get_ready_queue(t)

            # 6. Decide: run server or periodic task?
            server_should_run = self._should_server_run(ready_queue, t)
            server_executed = False

            if server_should_run and self.server_remaining > 0:
                # Server slot - handle aperiodic tasks
                server_executed = self._execute_server_slot(t)
                if server_executed:
                    busy_time += 1

            # If server didn't execute (deferred, no aperiodic, or no capacity), run periodic task
            if not server_executed and ready_queue:
                # Run highest priority periodic task
                next_task = self.get_next_task(ready_queue)

                # Handle preemption
                if self.running_task and self.running_task != next_task:
                    if self.running_task.remaining_time > 0:
                        self.timeline.append(ScheduleEvent(
                            time=float(t), task_id=self.running_task.task_id,
                            event_type='preempt',
                            details={'instance': self.running_task.instance_number}
                        ))

                # Start/continue task
                if next_task != self.running_task:
                    self.timeline.append(ScheduleEvent(
                        time=float(t), task_id=next_task.task_id, event_type='start',
                        details={'instance': next_task.instance_number}
                    ))

                self.running_task = next_task
                next_task.remaining_time -= 1
                busy_time += 1

                # Check completion
                if next_task.remaining_time <= 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t + 1), task_id=next_task.task_id, event_type='complete',
                        details={'instance': next_task.instance_number}
                    ))
                    self.running_task = None
            else:
                # Idle
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=None, event_type='idle', details={}
                ))
                self.running_task = None

        # Sort timeline
        self.timeline.sort(key=lambda e: e.time)

        # Count context switches (only 'start' to avoid double-counting preempt+start)
        context_switches = sum(1 for e in self.timeline if e.event_type == 'start')

        # Calculate utilization
        cpu_util = busy_time / self.duration if self.duration > 0 else 0.0

        # Calculate aperiodic response times
        response_times = {}
        for apt in self.aperiodic_completed:
            completion = next((e for e in self.timeline
                              if e.task_id == f"Aperiodic_{apt.id}" and e.event_type == 'complete'), None)
            if completion:
                response_times[apt.id] = completion.time - apt.arrival_time

        return ScheduleResult(
            algorithm=self.__class__.__name__,
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=context_switches,
            cpu_utilization=cpu_util,
            response_times=response_times
        )


class PollingServerScheduler(ServerScheduler):
    """
    Polling Server for combined scheduling.

    Server periodically checks for aperiodic tasks at its invocation times.
    If no aperiodic tasks available when polled, capacity is LOST.

    Characteristics:
    - Bandwidth non-preserving
    - Worst response time among server algorithms
    - Simple implementation
    """

    def _handle_replenishment(self, t: int) -> None:
        """Replenish at start of each server period."""
        if self.server_period > 0 and t % self.server_period < 1:
            self.server_remaining = self.server_capacity
            self.server_next_replenish = t + self.server_period

    def _execute_server_slot(self, t: int) -> bool:
        """
        Polling behavior: Check for aperiodic tasks; lose capacity if none.

        Returns True if server executed work, False otherwise.
        """
        if self.aperiodic_queue and self.server_remaining > 0:
            # Service aperiodic task
            apt = self.aperiodic_queue[0]

            # Record start if this is first execution
            if self.current_aperiodic != apt:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=f"Aperiodic_{apt.id}", event_type='start',
                    details={'server': 'Polling'}
                ))
                self.current_aperiodic = apt

            # Execute one time unit
            work_done = min(1.0, self.server_remaining, self.aperiodic_remaining[apt.id])
            self.server_remaining -= work_done
            self.aperiodic_remaining[apt.id] -= work_done

            # Check completion
            if self.aperiodic_remaining[apt.id] <= 0:
                self.aperiodic_queue.pop(0)
                self.aperiodic_completed.append(apt)
                self.timeline.append(ScheduleEvent(
                    time=float(t + 1), task_id=f"Aperiodic_{apt.id}", event_type='complete',
                    details={'server': 'Polling', 'response_time': t + 1 - apt.arrival_time}
                ))
                self.current_aperiodic = None

            return True
        else:
            # NO APERIODIC TASKS → CAPACITY LOST (Polling behavior)
            if self.server_remaining > 0:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id="Server", event_type='capacity_lost',
                    details={'lost': self.server_remaining, 'reason': 'no_aperiodic_tasks'}
                ))
            self.server_remaining = 0  # Lose all remaining capacity
            self.current_aperiodic = None
            return False


class DeferrableServerScheduler(ServerScheduler):
    """
    Deferrable Server for combined scheduling.

    Server preserves its capacity when no aperiodic tasks are available.
    Capacity can be used at any time during the period.

    Characteristics:
    - Bandwidth preserving
    - Better response time than Polling
    - Capacity replenished at period boundaries
    """

    def _handle_replenishment(self, t: int) -> None:
        """Replenish at start of each server period."""
        if self.server_period > 0 and t % self.server_period < 1:
            self.server_remaining = self.server_capacity
            self.server_next_replenish = t + self.server_period

    def _execute_server_slot(self, t: int) -> bool:
        """
        Deferrable behavior: Preserve capacity if no aperiodic tasks.

        Key difference from Polling: capacity is NOT lost when no aperiodic tasks.
        """
        if self.aperiodic_queue and self.server_remaining > 0:
            # Service aperiodic task (same as Polling)
            apt = self.aperiodic_queue[0]

            if self.current_aperiodic != apt:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=f"Aperiodic_{apt.id}", event_type='start',
                    details={'server': 'Deferrable'}
                ))
                self.current_aperiodic = apt

            work_done = min(1.0, self.server_remaining, self.aperiodic_remaining[apt.id])
            self.server_remaining -= work_done
            self.aperiodic_remaining[apt.id] -= work_done

            if self.aperiodic_remaining[apt.id] <= 0:
                self.aperiodic_queue.pop(0)
                self.aperiodic_completed.append(apt)
                self.timeline.append(ScheduleEvent(
                    time=float(t + 1), task_id=f"Aperiodic_{apt.id}", event_type='complete',
                    details={'server': 'Deferrable', 'response_time': t + 1 - apt.arrival_time}
                ))
                self.current_aperiodic = None

            return True
        else:
            # NO APERIODIC TASKS → CAPACITY PRESERVED (Deferrable behavior)
            # Server defers - does NOT run, keeps capacity for later
            if self.server_remaining > 0:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id="Server", event_type='deferred',
                    details={'capacity_preserved': self.server_remaining}
                ))
            self.current_aperiodic = None
            return False  # Server didn't use CPU, let periodic tasks run


class SporadicServerScheduler(ServerScheduler):
    """
    Sporadic Server for combined scheduling.

    Server dynamically replenishes capacity after consumption.
    Capacity consumed at time t is replenished at time t + Ps.

    Characteristics:
    - Bandwidth preserving
    - Best response time among server algorithms
    - Maintains RMS utilization bound
    - Most complex implementation
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Track replenishment events: [(replenish_time, amount), ...]
        self.replenishment_queue: List[Tuple[float, float]] = []
        # Track when server became active (for replenishment scheduling)
        self.server_active_start: Optional[float] = None

    def _handle_replenishment(self, t: int) -> None:
        """
        Sporadic replenishment: process scheduled replenishments.

        Unlike Polling/Deferrable, replenishment is NOT at fixed period boundaries.
        Instead, capacity is replenished Ps time units after it was consumed.
        """
        # Process any replenishments due at time t
        remaining_queue = []
        for replenish_time, amount in self.replenishment_queue:
            if t >= replenish_time:
                self.server_remaining = min(self.server_capacity,
                                           self.server_remaining + amount)
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id="Server", event_type='replenish',
                    details={'amount': amount, 'new_capacity': self.server_remaining}
                ))
            else:
                remaining_queue.append((replenish_time, amount))

        self.replenishment_queue = remaining_queue

        # Initial replenishment at t=0
        if t == 0:
            self.server_remaining = self.server_capacity

    def _consume_capacity(self, amount: float, t: int) -> None:
        """
        Consume server capacity and schedule replenishment.

        Sporadic Server rule: capacity consumed at t is replenished at t + Ps.
        """
        self.server_remaining -= amount
        # Schedule replenishment
        replenish_time = t + self.server_period
        self.replenishment_queue.append((replenish_time, amount))

    def _execute_server_slot(self, t: int) -> bool:
        """
        Sporadic behavior: Use capacity with dynamic replenishment.

        Key features:
        1. Capacity available immediately when aperiodic arrives
        2. Consumed capacity replenished at consumption_time + Ps
        3. Best response time
        """
        if self.aperiodic_queue and self.server_remaining > 0:
            apt = self.aperiodic_queue[0]

            # Track when server becomes active
            if self.server_active_start is None:
                self.server_active_start = t

            if self.current_aperiodic != apt:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=f"Aperiodic_{apt.id}", event_type='start',
                    details={'server': 'Sporadic'}
                ))
                self.current_aperiodic = apt

            work_done = min(1.0, self.server_remaining, self.aperiodic_remaining[apt.id])

            # Consume with replenishment scheduling
            self._consume_capacity(work_done, t)
            self.aperiodic_remaining[apt.id] -= work_done

            if self.aperiodic_remaining[apt.id] <= 0:
                self.aperiodic_queue.pop(0)
                self.aperiodic_completed.append(apt)
                self.timeline.append(ScheduleEvent(
                    time=float(t + 1), task_id=f"Aperiodic_{apt.id}", event_type='complete',
                    details={'server': 'Sporadic', 'response_time': t + 1 - apt.arrival_time}
                ))
                self.current_aperiodic = None

            return True
        else:
            # No aperiodic tasks - capacity is preserved (like Deferrable)
            # But no explicit deferred event needed
            self.server_active_start = None
            self.current_aperiodic = None
            return False


class PriorityExchangeServerScheduler(ServerScheduler):
    """
    Priority Exchange Server for combined scheduling.

    When aperiodic tasks are unavailable, server exchanges its priority
    with the highest priority periodic task ready for execution.

    Characteristics:
    - Bandwidth preserving
    - Worse response time than Deferrable
    - Better schedulability bound for periodic tasks
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exchanged_priority: Optional[int] = None

    def _handle_replenishment(self, t: int) -> None:
        """Replenish at start of each server period."""
        if self.server_period > 0 and t % self.server_period < 1:
            self.server_remaining = self.server_capacity
            self.server_next_replenish = t + self.server_period
            self.exchanged_priority = None  # Reset exchange

    def _execute_server_slot(self, t: int) -> bool:
        """
        Priority Exchange behavior: Exchange priority when no aperiodic tasks.
        """
        if self.aperiodic_queue and self.server_remaining > 0:
            # Service aperiodic task at server's high priority
            apt = self.aperiodic_queue[0]

            if self.current_aperiodic != apt:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=f"Aperiodic_{apt.id}", event_type='start',
                    details={'server': 'PriorityExchange'}
                ))
                self.current_aperiodic = apt

            work_done = min(1.0, self.server_remaining, self.aperiodic_remaining[apt.id])
            self.server_remaining -= work_done
            self.aperiodic_remaining[apt.id] -= work_done

            if self.aperiodic_remaining[apt.id] <= 0:
                self.aperiodic_queue.pop(0)
                self.aperiodic_completed.append(apt)
                self.timeline.append(ScheduleEvent(
                    time=float(t + 1), task_id=f"Aperiodic_{apt.id}", event_type='complete',
                    details={'server': 'PriorityExchange'}
                ))
                self.current_aperiodic = None

            return True
        else:
            # NO APERIODIC TASKS → EXCHANGE PRIORITY
            # Server gives its high priority to a periodic task
            # This allows periodic tasks to benefit from server's time
            if self.server_remaining > 0:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id="Server", event_type='priority_exchange',
                    details={'capacity_preserved': self.server_remaining}
                ))
            self.current_aperiodic = None
            return False  # Let periodic task run with exchanged priority


class BackgroundScheduler(SchedulerBase):
    """
    Background Scheduler for aperiodic tasks.

    Simple approach: aperiodic tasks execute in idle slots only.
    No dedicated server - just FIFO when CPU is idle.

    Characteristics:
    - Simplest implementation
    - No guaranteed response time for aperiodic tasks
    - Aperiodic tasks only run when no periodic work
    """

    def __init__(self, tasks: List[PeriodicTask], aperiodic_tasks: List[AperiodicTask],
                 duration: int = 100):
        """Initialize background scheduler."""
        self.aperiodic_tasks = sorted(aperiodic_tasks, key=lambda t: t.arrival_time)
        self.aperiodic_queue: List[TaskInstance] = []
        self.aperiodic_remaining: Dict[str, float] = {}
        self.aperiodic_completed: List[AperiodicTask] = []
        super().__init__(tasks, duration)

    def assign_priorities(self) -> None:
        """Assign RMS priorities to periodic tasks."""
        # RMS: shorter period = higher priority, with task ID as tie-breaker for determinism
        sorted_tasks = sorted(self.tasks, key=lambda t: (t.period, t.id))
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i

    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select next task: periodic if ready, aperiodic if idle."""
        if ready_queue:
            return ready_queue[0]
        elif self.aperiodic_queue:
            return self.aperiodic_queue[0]
        return None

    def _update_aperiodic_queue(self, time: float) -> None:
        """Add newly arrived aperiodic tasks to queue."""
        for apt in self.aperiodic_tasks:
            if abs(time - apt.arrival_time) < 0.001:
                if apt.id not in self.aperiodic_remaining:
                    instance = TaskInstance(
                        task_id=f"Aperiodic_{apt.id}",
                        instance_number=0,
                        arrival_time=time,
                        deadline=apt.deadline,
                        remaining_time=apt.computation_time
                    )
                    self.aperiodic_queue.append(instance)
                    self.aperiodic_remaining[apt.id] = apt.computation_time

        # Sort by arrival time (FIFO)
        self.aperiodic_queue.sort(key=lambda t: t.arrival_time)

    def simulate(self) -> ScheduleResult:
        """Run background scheduling simulation."""
        self.assign_priorities()

        self.timeline = []
        self.task_instances = []
        self.deadline_misses = []
        self.aperiodic_queue = []
        self.aperiodic_remaining = {}
        self.aperiodic_completed = []
        self.running_task = None
        busy_time = 0

        # Create initial periodic instances
        for task in self.tasks:
            instance = TaskInstance(
                task_id=task.id,
                instance_number=0,
                arrival_time=0.0,
                deadline=float(task.deadline),
                remaining_time=task.computation_time
            )
            self.task_instances.append(instance)

        for t in range(int(self.duration)):
            self.current_time = float(t)

            # Check aperiodic arrivals
            self._update_aperiodic_queue(t)

            # Create new periodic instances
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
            # Note: Tasks remain eligible even after deadline (they just miss the constraint)
            ready_queue = [inst for inst in self.task_instances
                          if inst.remaining_time > 0 and t >= inst.arrival_time]
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

            if next_task:
                is_aperiodic = next_task.task_id.startswith("Aperiodic_")

                # Handle preemption
                if self.running_task and self.running_task != next_task:
                    if self.running_task.remaining_time > 0:
                        self.timeline.append(ScheduleEvent(
                            time=float(t), task_id=self.running_task.task_id,
                            event_type='preempt',
                            details={'instance': self.running_task.instance_number}
                        ))

                if next_task != self.running_task:
                    self.timeline.append(ScheduleEvent(
                        time=float(t), task_id=next_task.task_id, event_type='start',
                        details={'instance': next_task.instance_number, 'background': is_aperiodic}
                    ))

                self.running_task = next_task
                next_task.remaining_time -= 1
                busy_time += 1

                if next_task.remaining_time <= 0:
                    self.timeline.append(ScheduleEvent(
                        time=float(t + 1), task_id=next_task.task_id, event_type='complete',
                        details={'instance': next_task.instance_number}
                    ))

                    # Remove from aperiodic queue if applicable
                    if is_aperiodic:
                        self.aperiodic_queue = [q for q in self.aperiodic_queue
                                               if q.task_id != next_task.task_id]
                        # Find original aperiodic task
                        apt_id = next_task.task_id.replace("Aperiodic_", "")
                        for apt in self.aperiodic_tasks:
                            if apt.id == apt_id:
                                self.aperiodic_completed.append(apt)
                                break

                    self.running_task = None
            else:
                self.timeline.append(ScheduleEvent(
                    time=float(t), task_id=None, event_type='idle', details={}
                ))
                self.running_task = None

        self.timeline.sort(key=lambda e: e.time)
        # Count only 'start' to avoid double-counting preempt+start as 2 switches
        context_switches = sum(1 for e in self.timeline if e.event_type == 'start')
        cpu_util = busy_time / self.duration if self.duration > 0 else 0.0

        # Calculate response times
        response_times = {}
        for apt in self.aperiodic_completed:
            completion = next((e for e in self.timeline
                              if e.task_id == f"Aperiodic_{apt.id}" and e.event_type == 'complete'), None)
            if completion:
                response_times[apt.id] = completion.time - apt.arrival_time

        return ScheduleResult(
            algorithm=self.__class__.__name__,
            tasks=self.tasks,
            events=self.timeline,
            deadline_misses=self.deadline_misses,
            total_context_switches=context_switches,
            cpu_utilization=cpu_util,
            response_times=response_times
        )
