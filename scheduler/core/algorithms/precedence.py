"""Precedence-constrained scheduling algorithms."""

from typing import List, Optional, Dict
from ..scheduler_base import SchedulerBase
from ..task import PeriodicTask, TaskInstance, PrecedenceConstraint


class RMSWithPrecedence(SchedulerBase):
    """
    RMS with precedence constraints.
    
    Modifies ready times based on precedence graph.
    Ready time: R_j* = max(R_j, R_i* + C_i) for all predecessors i.
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
        self.precedences = precedences
        self.predecessor_map = self._build_predecessor_map()
        super().__init__(tasks, duration)
    
    def _build_predecessor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its predecessors."""
        predecessor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.successor not in predecessor_map:
                predecessor_map[prec.successor] = []
            predecessor_map[prec.successor].append(prec.predecessor)
        return predecessor_map
    
    def assign_priorities(self) -> None:
        """Assign RMS priorities based on periods."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
    
    def get_modified_deadline(self, task_id: str, base_deadline: float) -> float:
        """
        Modify deadline based on precedence constraints.
        
        For RMS: No deadline modification (only ready times modified)
        """
        return base_deadline
    
    def get_modified_ready_time(self, task_id: str, base_ready_time: float,
                                completion_times: Dict[str, float]) -> float:
        """
        Calculate modified ready time based on precedence.
        
        R_j* = max(R_j, max(R_i* + C_i) for all predecessors i)
        """
        predecessors = self.predecessor_map.get(task_id, [])
        
        if not predecessors:
            return base_ready_time
        
        # Find maximum ready time from predecessors
        max_predecessor_ready = 0.0
        for pred_id in predecessors:
            pred_task = next((t for t in self.tasks if t.id == pred_id), None)
            if pred_task:
                # Get completion time of predecessor (approximation)
                comp_time = completion_times.get(pred_id, pred_task.computation_time)
                predecessor_ready = comp_time  # Simplified: assumes predecessor completes before this starts
                max_predecessor_ready = max(max_predecessor_ready, predecessor_ready)
        
        return max(base_ready_time, max_predecessor_ready)
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task from ready queue."""
        if not ready_queue:
            return None
        return ready_queue[0]


class DMSWithPrecedence(SchedulerBase):
    """
    DMS with precedence constraints.
    
    Modifies both ready times and deadlines based on precedence.
    Forward pass: ready times
    Backward pass: deadlines
    """
    
    def __init__(self, tasks: List[PeriodicTask], precedences: List[PrecedenceConstraint],
                 duration: int = 100):
        """Initialize DMS scheduler with precedence constraints."""
        self.precedences = precedences
        self.predecessor_map = self._build_predecessor_map()
        self.successor_map = self._build_successor_map()
        super().__init__(tasks, duration)
    
    def _build_predecessor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its predecessors."""
        predecessor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.successor not in predecessor_map:
                predecessor_map[prec.successor] = []
            predecessor_map[prec.successor].append(prec.predecessor)
        return predecessor_map
    
    def _build_successor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its successors."""
        successor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.predecessor not in successor_map:
                successor_map[prec.predecessor] = []
            successor_map[prec.predecessor].append(prec.successor)
        return successor_map
    
    def assign_priorities(self) -> None:
        """Assign DMS priorities based on relative deadlines."""
        sorted_tasks = sorted(self.tasks, key=lambda t: t.deadline)
        for i, task in enumerate(sorted_tasks):
            task.priority = len(sorted_tasks) - i
    
    def get_modified_deadline(self, task_id: str, base_deadline: float) -> float:
        """
        Modify deadline based on precedence constraints (backward pass).
        
        D_i* = min(D_i, D_j* - C_j) for all successors j
        """
        successors = self.successor_map.get(task_id, [])
        
        if not successors:
            return base_deadline
        
        # Find minimum deadline from successors
        min_successor_deadline = float('inf')
        for succ_id in successors:
            succ_task = next((t for t in self.tasks if t.id == succ_id), None)
            if succ_task:
                # Modified deadline of successor minus its computation
                succ_modified = succ_task.deadline - succ_task.computation_time
                min_successor_deadline = min(min_successor_deadline, succ_modified)
        
        return min(base_deadline, min_successor_deadline)
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select highest priority task from ready queue."""
        if not ready_queue:
            return None
        return ready_queue[0]


class EDFWithPrecedence(SchedulerBase):
    """
    EDF with precedence constraints.
    
    Modifies ready times and deadlines based on precedence graph.
    """
    
    def __init__(self, tasks: List[PeriodicTask], precedences: List[PrecedenceConstraint],
                 duration: int = 100):
        """Initialize EDF scheduler with precedence constraints."""
        self.precedences = precedences
        self.predecessor_map = self._build_predecessor_map()
        self.successor_map = self._build_successor_map()
        super().__init__(tasks, duration)
    
    def _build_predecessor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its predecessors."""
        predecessor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.successor not in predecessor_map:
                predecessor_map[prec.successor] = []
            predecessor_map[prec.successor].append(prec.predecessor)
        return predecessor_map
    
    def _build_successor_map(self) -> Dict[str, List[str]]:
        """Build mapping from task to its successors."""
        successor_map = {task.id: [] for task in self.tasks}
        for prec in self.precedences:
            if prec.predecessor not in successor_map:
                successor_map[prec.predecessor] = []
            successor_map[prec.predecessor].append(prec.successor)
        return successor_map
    
    def assign_priorities(self) -> None:
        """EDF uses dynamic priorities (no fixed assignment needed)."""
        pass
    
    def get_next_task(self, ready_queue: List[TaskInstance]) -> Optional[TaskInstance]:
        """Select task with earliest absolute deadline (EDF)."""
        if not ready_queue:
            return None
        
        # Sort by deadline (earliest first)
        ready_queue_sorted = sorted(ready_queue, key=lambda inst: inst.deadline)
        return ready_queue_sorted[0]

