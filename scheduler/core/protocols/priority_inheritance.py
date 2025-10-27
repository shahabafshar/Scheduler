"""Priority Inheritance Protocol (PIP) implementation."""

from typing import Dict, List, Optional
from ..task import PeriodicTask, ResourceConstraint, TaskInstance


class PriorityInheritanceProtocol:
    """
    Priority Inheritance Protocol (PIP).
    
    When a lower-priority task blocks a higher-priority task,
    the lower task inherits the higher priority.
    Pantomatically handles priority inversion.
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
        self.blocking_tasks = {}  # task_id -> set of blocking task ids
        
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
            self.blocking_tasks.setdefault(task_id, set()).add(blocking_task)
            
            # Apply priority inheritance: blocking task inherits higher priority
            if blocking_task:
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
        
        # Restore original priority if no longer blocking
        self._restore_priority(task_id)
        
        # If a waiting task gets the resource, may need priority adjustments
        if next_task:
            for task_obj in self.tasks:
                if task_obj.id == next_task:
                    self.task_priorities[next_task] = task_obj.priority
                    break
    
    def _restore_priority(self, task_id: str) -> None:
        """Restore task's base priority if not blocking any high-priority tasks."""
        base_priority = self.base_priorities.get(task_id)
        if base_priority is None:
            return
        
        # Check if task is blocking any high-priority tasks
        is_blocking = any(task_id in blockers for blockers in self.blocking_tasks.values())
        
        if not is_blocking:
            # Restore original priority
            self.task_priorities[task_id] = base_priority
            task_obj = next((t for t in self.tasks if t.id == task_id), None)
            if task_obj:
                task_obj.priority = base_priority
        else:
            # Still blocking - keep inherited priority
            # Find highest priority among blocked tasks
            max_inherited = base_priority
            for blocker_task, blocked_set in self.blocking_tasks.items():
                if task_id in blocked_set:
                    inherited_priority = self.base_priorities.get(blocker_task, 0)
                    max_inherited = max(max_inherited, inherited_priority)
            
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

