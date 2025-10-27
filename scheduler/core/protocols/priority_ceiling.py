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
        self.locked_resources = set()  # Currently locked resources
        
        # Calculate priority ceiling for each resource
        for resource in self.resources.values():
            if resource.tasks:
                max_priority = max(
                    next((t.priority for t in tasks if t.id == tid), 0)
                    for tid in resource.tasks
                )
                resource.priority_ceiling = max_priority
    
    def request_resource(self, task_id: str, resource_id: str) -> Optional[str]:
        """
        Request a resource under PCP.
        
        Args:
            task_id: Task requesting resource
            resource_id: Resource being requested
            
        Returns:
            Blocking task ID if access is denied, None if granted
        """
        if resource_id not in self.resources:
            return None
        
        resource = self.resources[resource_id]
        task_priority = self.task_priorities.get(task_id, 0)
        
        # Check priority ceiling condition
        max_ceiling = self._get_max_ceiling_of_locked_resources()
        
        if task_priority <= max_ceiling:
            # Access denied - priority too low
            # Return the task holding the resource with highest ceiling
            return self._get_task_with_highest_ceiling()
        
        # Priority is high enough - try to lock
        success = resource.lock(task_id)
        
        if success:
            self.locked_resources.add(resource_id)
        else:
            # Resource is already held
            return resource.current_holder
        
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
        self.locked_resources.discard(resource_id)
    
    def _get_max_ceiling_of_locked_resources(self) -> int:
        """Get maximum priority ceiling among currently locked resources."""
        if not self.locked_resources:
            return 0
        
        max_ceiling = 0
        for res_id in self.locked_resources:
            resource = self.resources[res_id]
            max_ceiling = max(max_ceiling, resource.priority_ceiling)
        
        return max_ceiling
    
    def _get_task_with_highest_ceiling(self) -> Optional[str]:
        """Get the task holding a resource with the highest priority ceiling."""
        if not self.locked_resources:
            return None
        
        max_ceiling = 0
        holding_task = None
        
        for res_id in self.locked_resources:
            resource = self.resources[res_id]
            if resource.priority_ceiling > max_ceiling:
                max_ceiling = resource.priority_ceiling
                holding_task = resource.current_holder
        
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
            
            # Immediately raise priority to ceiling
            self.task_priorities[task_id] = resource.priority_ceiling
            task_obj = next((t for t in self.tasks if t.id == task_id), None)
            if task_obj:
                task_obj.priority = resource.priority_ceiling
        
        return success
    
    def release_resource(self, task_id: str, resource_id: str) -> None:
        """
        Release a resource and restore original priority.
        
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
        
        # Restore original priority
        base_priority = self.base_priorities.get(task_id)
        if base_priority is not None:
            self.task_priorities[task_id] = base_priority
            task_obj = next((t for t in self.tasks if t.id == task_id), None)
            if task_obj:
                task_obj.priority = base_priority

