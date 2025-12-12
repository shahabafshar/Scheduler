"""Priority Ceiling Protocol (PCP) implementation."""

from typing import Dict, List, Optional
from ..task import PeriodicTask, ResourceConstraint, TaskInstance


class PriorityCeilingProtocol:
    """
    Priority Ceiling Protocol (PCP).

    Prevents deadlock and at-most-once blocking.
    Each resource has a priority ceiling = max priority of tasks using it.
    Tasks can access resource only if their priority > ceiling of locked resources.
    """

    def __init__(self, tasks: List[PeriodicTask], resources: List[ResourceConstraint]):
        """
        Initialize PCP.

        Args:
            tasks: List of periodic tasks
            resources: List of shared resources
        """
        self.tasks = tasks
        self.resources = {r.resource_id: r for r in resources}
        self.task_priorities = {t.id: t.priority for t in tasks}
        self.locked_resources = {}  # resource_id -> task_id holding it
        self._ceilings_computed = False

    def update_priorities(self) -> None:
        """
        Update task priorities and recompute ceilings.

        Should be called after scheduler assigns priorities.
        """
        self.task_priorities = {t.id: t.priority for t in self.tasks}
        self._compute_ceilings()

    def _compute_ceilings(self) -> None:
        """Compute priority ceiling for each resource based on current task priorities."""
        for resource in self.resources.values():
            if resource.tasks:
                max_priority = max(
                    self.task_priorities.get(tid, 0)
                    for tid in resource.tasks
                )
                resource.priority_ceiling = max_priority
        self._ceilings_computed = True

    def _ensure_ceilings_computed(self) -> None:
        """Lazily compute ceilings on first resource access."""
        if not self._ceilings_computed:
            # Re-read priorities from tasks (they may have been assigned by scheduler)
            self.task_priorities = {t.id: t.priority for t in self.tasks}
            self._compute_ceilings()

    def request_resource(self, task_id: str, resource_id: str) -> Optional[str]:
        """
        Request a resource under PCP.

        Args:
            task_id: Task requesting resource
            resource_id: Resource being requested

        Returns:
            Blocking task ID if access is denied, None if granted
        """
        self._ensure_ceilings_computed()

        if resource_id not in self.resources:
            return None

        resource = self.resources[resource_id]

        # Update task priority from current task state
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            self.task_priorities[task_id] = task.priority

        task_priority = self.task_priorities.get(task_id, 0)

        # First check if resource is already held
        if resource.current_holder is not None and resource.current_holder != task_id:
            # Resource is held by another task
            return resource.current_holder

        # Check priority ceiling condition (only for OTHER locked resources)
        max_ceiling = self._get_max_ceiling_of_locked_resources(exclude_resource=resource_id)

        if task_priority <= max_ceiling:
            # Access denied - priority not strictly greater than system ceiling
            # Return the task causing the ceiling violation
            return self._get_task_causing_ceiling_violation(task_priority)

        # Priority is high enough - try to lock
        success = resource.lock(task_id)

        if success:
            self.locked_resources[resource_id] = task_id

        return None

    def release_resource(self, task_id: str, resource_id: str) -> None:
        """
        Release a resource under PCP.

        Args:
            task_id: Task releasing resource
            resource_id: Resource being released
        """
        if resource_id not in self.resources:
            return

        resource = self.resources[resource_id]
        resource.unlock(task_id)

        if resource_id in self.locked_resources:
            del self.locked_resources[resource_id]

    def _get_max_ceiling_of_locked_resources(self, exclude_resource: str = None) -> int:
        """Get maximum priority ceiling among currently locked resources."""
        if not self.locked_resources:
            return 0

        max_ceiling = 0
        for res_id, holder in self.locked_resources.items():
            if res_id == exclude_resource:
                continue  # Don't count the resource being requested
            resource = self.resources[res_id]
            max_ceiling = max(max_ceiling, resource.priority_ceiling)

        return max_ceiling

    def _get_task_causing_ceiling_violation(self, task_priority: int) -> Optional[str]:
        """
        Get the task that is causing the priority ceiling violation.

        Returns the holder of the resource with the lowest ceiling that still
        blocks the requesting task.
        """
        if not self.locked_resources:
            return None

        blocking_task = None
        blocking_ceiling = float('inf')

        for res_id, holder in self.locked_resources.items():
            resource = self.resources[res_id]
            # This resource blocks if its ceiling >= task_priority
            if resource.priority_ceiling >= task_priority:
                if resource.priority_ceiling < blocking_ceiling:
                    blocking_ceiling = resource.priority_ceiling
                    blocking_task = holder

        return blocking_task

    def _get_task_with_highest_ceiling(self) -> Optional[str]:
        """Get the task holding a resource with the highest priority ceiling."""
        if not self.locked_resources:
            return None

        max_ceiling = 0
        holding_task = None

        for res_id, holder in self.locked_resources.items():
            resource = self.resources[res_id]
            if resource.priority_ceiling > max_ceiling:
                max_ceiling = resource.priority_ceiling
                holding_task = holder

        return holding_task
    
    def get_current_priority(self, task_id: str) -> int:
        """Get current priority of a task."""
        return self.task_priorities.get(task_id, 0)
    
    def calculate_blocking_time(self, task_id: str) -> float:
        """
        Calculate worst-case blocking time for a task under PCP.
        
        Args:
            task_id: Task to calculate blocking time for
            
        Returns:
            Maximum blocking time
        """
        max_blocking = 0.0
        task = next((t for t in self.tasks if t.id == task_id), None)
        
        if not task:
            return 0.0
        
        # Under PCP, a task can be blocked at most once by each resource
        # Find resources used by tasks with lower priority
        for resource in self.resources.values():
            for other_task_id in resource.tasks:
                if other_task_id != task_id:
                    other_task = next((t for t in self.tasks if t.id == other_task_id), None)
                    
                    if other_task and other_task.priority < task.priority:
                        cs_time = resource.critical_sections.get(other_task_id, 0)
                        max_blocking = max(max_blocking, cs_time)
        
        return max_blocking


class PriorityCeilingEmulation:
    """
    Priority Ceiling Emulation.

    Similar to PCP but immediately raises a task's priority to the resource's
    ceiling when it enters a critical section, rather than checking on entry.
    """

    def __init__(self, tasks: List[PeriodicTask], resources: List[ResourceConstraint]):
        """Initialize Priority Ceiling Emulation."""
        self.tasks = tasks
        self.resources = {r.resource_id: r for r in resources}
        self.task_priorities = {t.id: t.priority for t in tasks}
        self.base_priorities = {t.id: t.priority for t in tasks}
        self.resource_holders = {}  # resource_id -> task_id
        self.task_held_resources = {t.id: set() for t in tasks}  # task_id -> {resource_ids}

        # Calculate priority ceiling for each resource
        for resource in self.resources.values():
            if resource.tasks:
                max_priority = max(
                    next((t.priority for t in tasks if t.id == tid), 0)
                    for tid in resource.tasks
                )
                resource.priority_ceiling = max_priority

    def request_resource(self, task_id: str, resource_id: str) -> bool:
        """
        Request a resource with immediate priority raise.

        Args:
            task_id: Task requesting resource
            resource_id: Resource being requested

        Returns:
            True if access granted, False otherwise
        """
        if resource_id not in self.resources:
            return False

        resource = self.resources[resource_id]

        # Try to lock
        success = resource.lock(task_id)

        if success:
            self.resource_holders[resource_id] = task_id
            self.task_held_resources.setdefault(task_id, set()).add(resource_id)

            # Raise priority to max ceiling of all held resources
            new_priority = self._get_max_ceiling_of_held_resources(task_id)
            self.task_priorities[task_id] = new_priority
            task_obj = next((t for t in self.tasks if t.id == task_id), None)
            if task_obj:
                task_obj.priority = new_priority

        return success

    def _get_max_ceiling_of_held_resources(self, task_id: str) -> int:
        """Get the maximum priority ceiling among all resources held by a task."""
        held = self.task_held_resources.get(task_id, set())
        if not held:
            return self.base_priorities.get(task_id, 0)

        max_ceiling = self.base_priorities.get(task_id, 0)
        for res_id in held:
            if res_id in self.resources:
                resource = self.resources[res_id]
                max_ceiling = max(max_ceiling, resource.priority_ceiling)

        return max_ceiling

    def release_resource(self, task_id: str, resource_id: str) -> None:
        """
        Release a resource and restore priority appropriately.

        If task still holds other resources, set priority to max ceiling of those.
        Otherwise, restore to base priority.

        Args:
            task_id: Task releasing resource
            resource_id: Resource being released
        """
        if resource_id not in self.resources:
            return

        resource = self.resources[resource_id]
        resource.unlock(task_id)

        if resource_id in self.resource_holders:
            del self.resource_holders[resource_id]

        # Remove from task's held resources
        if task_id in self.task_held_resources:
            self.task_held_resources[task_id].discard(resource_id)

        # Restore to max ceiling of still-held resources (or base priority if none)
        new_priority = self._get_max_ceiling_of_held_resources(task_id)
        self.task_priorities[task_id] = new_priority
        task_obj = next((t for t in self.tasks if t.id == task_id), None)
        if task_obj:
            task_obj.priority = new_priority

