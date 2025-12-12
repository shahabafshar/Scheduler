"""Priority Inheritance Protocol (PIP) implementation."""

from typing import Dict, List, Optional
from ..task import PeriodicTask, ResourceConstraint, TaskInstance


class PriorityInheritanceProtocol:
    """
    Priority Inheritance Protocol (PIP).

    When a lower-priority task blocks a higher-priority task,
    the lower task inherits the higher priority.
    Automatically handles priority inversion.
    """

    def __init__(self, tasks: List[PeriodicTask], resources: List[ResourceConstraint]):
        """
        Initialize PIP.

        Args:
            tasks: List of periodic tasks
            resources: List of shared resources
        """
        self.tasks = tasks
        self.resources = {r.resource_id: r for r in resources}
        self.task_priorities = {t.id: t.priority for t in tasks}
        self.base_priorities = {t.id: t.priority for t in tasks}

        # Bidirectional blocking relationships
        self.blocked_by = {}  # waiting_task -> {holder_tasks blocking it}
        self.is_blocking = {}  # holder_task -> {waiting_tasks it blocks}
        # Track which resource caused each blocking relationship
        self.blocking_resource = {}  # (holder_task, blocked_task) -> resource_id

    def request_resource(self, task_id: str, resource_id: str) -> Optional[str]:
        """
        Request a resource, applying priority inheritance if needed.

        Args:
            task_id: Task requesting resource
            resource_id: Resource being requested

        Returns:
            Blocking task ID if access is denied, None if granted
        """
        if resource_id not in self.resources:
            return None

        resource = self.resources[resource_id]

        # Try to lock
        success = resource.lock(task_id)

        if not success:
            # Resource is held by another task
            blocking_task = resource.current_holder

            if blocking_task:
                # Record bidirectional blocking relationship
                self.blocked_by.setdefault(task_id, set()).add(blocking_task)
                self.is_blocking.setdefault(blocking_task, set()).add(task_id)
                # Track which resource caused this blocking
                self.blocking_resource[(blocking_task, task_id)] = resource_id

                # Apply priority inheritance: blocking task inherits higher priority
                current_priority = self.task_priorities.get(task_id, 0)
                blocking_priority = self.task_priorities.get(blocking_task, 0)

                if current_priority > blocking_priority:
                    # Inherit higher priority
                    self.task_priorities[blocking_task] = current_priority
                    # Update task object
                    blocking_task_obj = next((t for t in self.tasks if t.id == blocking_task), None)
                    if blocking_task_obj:
                        blocking_task_obj.priority = current_priority

            return blocking_task

        return None

    def release_resource(self, task_id: str, resource_id: str) -> None:
        """
        Release a resource and restore priority if needed.

        Args:
            task_id: Task releasing resource
            resource_id: Resource being released
        """
        if resource_id not in self.resources:
            return

        resource = self.resources[resource_id]

        # Unlock resource
        next_task = resource.unlock(task_id)

        # Clear blocking relationships ONLY for this specific resource
        if task_id in self.is_blocking:
            # Get tasks that were blocked by this task ON THIS RESOURCE
            blocked_tasks = self.is_blocking.get(task_id, set()).copy()
            for blocked_task in blocked_tasks:
                # Only clear if this blocking was for the released resource
                blocking_key = (task_id, blocked_task)
                if blocking_key in self.blocking_resource:
                    if self.blocking_resource[blocking_key] == resource_id:
                        # This blocking was for this resource - clear it
                        del self.blocking_resource[blocking_key]
                        self.is_blocking[task_id].discard(blocked_task)
                        if blocked_task in self.blocked_by:
                            self.blocked_by[blocked_task].discard(task_id)
                            if not self.blocked_by[blocked_task]:
                                del self.blocked_by[blocked_task]
            # Clean up is_blocking if empty
            if task_id in self.is_blocking and not self.is_blocking[task_id]:
                del self.is_blocking[task_id]

        # Restore original priority if no longer blocking anyone
        self._restore_priority(task_id)

        # If a waiting task gets the resource, update their blocked state
        if next_task:
            # Remove from blocked_by since they now have the resource
            if next_task in self.blocked_by:
                self.blocked_by[next_task].discard(task_id)
                if not self.blocked_by[next_task]:
                    del self.blocked_by[next_task]

    def _restore_priority(self, task_id: str) -> None:
        """Restore task's base priority if not blocking any high-priority tasks."""
        base_priority = self.base_priorities.get(task_id)
        if base_priority is None:
            return

        # Check if task is STILL blocking any tasks (using correct relationship)
        still_blocking = task_id in self.is_blocking and len(self.is_blocking[task_id]) > 0

        if not still_blocking:
            # Restore original priority
            self.task_priorities[task_id] = base_priority
            task_obj = next((t for t in self.tasks if t.id == task_id), None)
            if task_obj:
                task_obj.priority = base_priority
        else:
            # Still blocking - find highest priority among blocked tasks
            max_inherited = base_priority
            for blocked_task in self.is_blocking.get(task_id, set()):
                blocked_priority = self.base_priorities.get(blocked_task, 0)
                max_inherited = max(max_inherited, blocked_priority)

            self.task_priorities[task_id] = max_inherited
            task_obj = next((t for t in self.tasks if t.id == task_id), None)
            if task_obj:
                task_obj.priority = max_inherited
    
    def get_current_priority(self, task_id: str) -> int:
        """Get current priority of a task (may be inherited)."""
        return self.task_priorities.get(task_id, 0)
    
    def calculate_blocking_time(self, task_id: str) -> float:
        """
        Calculate worst-case blocking time for a task.
        
        Args:
            task_id: Task to calculate blocking time for
            
        Returns:
            Maximum blocking time
        """
        max_blocking = 0.0
        
        # Find all resources this task uses
        task_resources = [r for r in self.resources.values() if task_id in r.tasks]
        
        for resource in task_resources:
            cs_time = resource.critical_sections.get(task_id, 0)
            
            # Find tasks with lower priority that use this resource
            for other_task_id in resource.tasks:
                if other_task_id != task_id:
                    other_task = next((t for t in self.tasks if t.id == other_task_id), None)
                    task = next((t for t in self.tasks if t.id == task_id), None)
                    
                    if other_task and task and other_task.priority < task.priority:
                        other_cs_time = resource.critical_sections.get(other_task_id, 0)
                        max_blocking = max(max_blocking, other_cs_time)
        
        return max_blocking

