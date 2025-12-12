"""Resource-aware scheduler implementations with PIP/PCP protocol support."""

from typing import List, Optional
from ..scheduler_with_resources import ResourceAwareSchedulerBase
from ..task import PeriodicTask, TaskInstance, ResourceConstraint


class ResourceAwareRMSScheduler(ResourceAwareSchedulerBase):
    """RMS scheduler with resource protocol support (PIP/PCP)."""

    def assign_priorities(self) -> None:
        """Assign RMS priorities (shorter period = higher priority)."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i

    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task from ready queue."""
        if not ready_queue:
            return None
        return ready_queue[0]  # Already sorted by priority


class ResourceAwareEDFScheduler(ResourceAwareSchedulerBase):
    """EDF scheduler with resource protocol support (PIP/PCP)."""

    # EDF uses dynamic priority selection, skip redundant base class sorting
    _skip_priority_sort = True

    def assign_priorities(self) -> None:
        """EDF uses dynamic priorities based on deadline."""
        for task in self.tasks:
            task.priority = 0  # Will be computed dynamically

    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select task with earliest deadline."""
        if not ready_queue:
            return None
        return min(ready_queue, key=lambda t: (t.deadline, t.task_id))


class ResourceAwareDMSScheduler(ResourceAwareSchedulerBase):
    """DMS scheduler with resource protocol support (PIP/PCP)."""

    def assign_priorities(self) -> None:
        """Assign DMS priorities (shorter deadline = higher priority)."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.deadline)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i

    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task from ready queue."""
        if not ready_queue:
            return None
        return ready_queue[0]  # Already sorted by priority


class ResourceAwareLLFScheduler(ResourceAwareSchedulerBase):
    """LLF scheduler with resource protocol support (PIP/PCP)."""

    # LLF uses dynamic priority selection, skip redundant base class sorting
    _skip_priority_sort = True

    def assign_priorities(self) -> None:
        """LLF uses dynamic priorities based on laxity."""
        for task in self.tasks:
            task.priority = 0  # Will be computed dynamically

    def calculate_laxity(self, instance: TaskInstance, current_time: float) -> float:
        """Calculate laxity (slack time) for a task instance."""
        return instance.deadline - current_time - instance.remaining_time

    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select task with least laxity (most urgent)."""
        if not ready_queue:
            return None
        return min(ready_queue, key=lambda t: (self.calculate_laxity(t, self.current_time), t.task_id))


def create_resource_constraints(
    session_resources: List[dict],
    tasks: List[PeriodicTask]
) -> List[ResourceConstraint]:
    """
    Create ResourceConstraint objects from session state data.

    Args:
        session_resources: List of resource dicts from session state [{'id': 'R1'}, ...]
        tasks: List of PeriodicTask objects (with critical_sections already attached)

    Returns:
        List of ResourceConstraint objects
    """
    resources = []

    for res_data in session_resources:
        resource_id = res_data.get('id', '')
        if not resource_id:
            continue

        # Find all tasks that use this resource
        tasks_using_resource = []
        critical_section_durations = {}

        for task in tasks:
            for cs in task.critical_sections:
                if cs.resource_id == resource_id:
                    if task.id not in tasks_using_resource:
                        tasks_using_resource.append(task.id)
                    # Sum durations if multiple CS for same resource
                    critical_section_durations[task.id] = critical_section_durations.get(task.id, 0) + cs.duration

        if tasks_using_resource:
            # Calculate priority ceiling (max priority of tasks using this resource)
            max_priority = max(
                (t.priority for t in tasks if t.id in tasks_using_resource),
                default=0
            )

            resources.append(ResourceConstraint(
                resource_id=resource_id,
                tasks=tasks_using_resource,
                critical_sections=critical_section_durations,
                priority_ceiling=max_priority
            ))

    return resources


def map_protocol_name(ui_protocol: str) -> str:
    """Map UI protocol name to internal protocol identifier."""
    if not ui_protocol:
        return "none"
    ui_protocol = ui_protocol.lower()
    if "inheritance" in ui_protocol or "pip" in ui_protocol:
        return "pip"
    elif "ceiling" in ui_protocol or "pcp" in ui_protocol:
        return "pcp"
    return "none"
