"""Schedulability analysis for real-time scheduling algorithms."""

from typing import List, Tuple, Dict
from ..task import PeriodicTask
import math


class SchedulabilityAnalyzer:
    """Analyze schedulability of task sets under various algorithms."""
    
    @staticmethod
    def rms_utilization_test(tasks: List[PeriodicTask]) -> Tuple[bool, float, float, str]:
        """
        RMS utilization-based schedulability test.
        
        Args:
            tasks: List of periodic tasks
            
        Returns:
            Tuple of (schedulable, utilization, bound, explanation)
        """
        n = len(tasks)
        if n == 0:
            return True, 0.0, 1.0, "Empty task set"
        
        # Calculate total utilization
        total_utilization = sum(task.utilization for task in tasks)
        
        # Calculate RMS bound: n(2^(1/n) - 1)
        rms_bound = n * (math.pow(2, 1/n) - 1)
        
        schedulable = total_utilization <= rms_bound
        
        explanation = f"RMS utilization test: U={total_utilization:.3f}, bound={rms_bound:.3f}"
        if schedulable:
            explanation += " → SCHEDULABLE"
        else:
            explanation += " → Test FAILED (may still be schedulable with exact analysis)"
        
        return schedulable, total_utilization, rms_bound, explanation
    
    @staticmethod
    def edf_utilization_test(tasks: List[PeriodicTask]) -> Tuple[bool, float, str]:
        """
        EDF utilization test (necessary and sufficient for D_i = P_i).
        
        Args:
            tasks: List of periodic tasks
            
        Returns:
            Tuple of (schedulable, utilization, explanation)
        """
        if not tasks:
            return True, 0.0, "Empty task set"
        
        total_utilization = sum(task.utilization for task in tasks)
        schedulable = total_utilization <= 1.0
        
        explanation = f"EDF utilization test: U={total_utilization:.3f} ≤ 1.0"
        if schedulable:
            explanation += " → SCHEDULABLE"
        else:
            explanation += " → NOT SCHEDULABLE"
        
        return schedulable, total_utilization, explanation
    
    @staticmethod
    def dms_utilization_test(tasks: List[PeriodicTask]) -> Tuple[bool, float, float, str]:
        """
        DMS (Deadline Monotonic Scheduling) utilization test.
        
        Uses C_i / d_i instead of C_i / P_i.
        
        Args:
            tasks: List of periodic tasks with deadlines
            
        Returns:
            Tuple of (schedulable, utilization, bound, explanation)
        """
        n = len(tasks)
        if n == 0:
            return True, 0.0, 1.0, "Empty task set"
        
        # Calculate total utilization using deadlines
        total_utilization = sum(task.computation_time / task.deadline for task in tasks)
        
        # Calculate DMS bound: n(2^(1/n) - 1)
        dms_bound = n * (math.pow(2, 1/n) - 1)
        
        schedulable = total_utilization <= dms_bound
        
        explanation = f"DMS utilization test (using deadlines): U={total_utilization:.3f}, bound={dms_bound:.3f}"
        if schedulable:
            explanation += " → SCHEDULABLE"
        else:
            explanation += " → Test FAILED (may still be schedulable with exact analysis)"
        
        return schedulable, total_utilization, dms_bound, explanation
    
    @staticmethod
    def completion_time_test(tasks: List[PeriodicTask], max_iterations: int = 20) -> Dict[str, Dict]:
        """
        Exact schedulability analysis using completion time test.
        
        For each task Ti, compute the worst-case completion time W_i(t) and check if W_i ≤ d_i.
        
        Workload function: W_i(t) = sum_j [⌈t/P_j⌉ × C_j] for all tasks j with higher priority
        
        Args:
            tasks: List of periodic tasks
            max_iterations: Maximum iterations for convergence
            
        Returns:
            Dictionary with results for each task
        """
        if not tasks:
            return {}
        
        # Sort tasks by priority (assumed to be set)
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)
        
        results = {}
        
        for i, task_i in enumerate(sorted_tasks):
            # Collect all tasks with higher or equal priority
            higher_priority_tasks = sorted_tasks[:i+1]
            
            # Initial estimate: t_0 = sum of all computation times
            t_prev = sum(t.computation_time for t in higher_priority_tasks)
            
            # Iterative computation until convergence
            for iteration in range(max_iterations):
                # Calculate workload W_i(t)
                workload = sum(
                    math.ceil(t_prev / t.period) * t.computation_time
                    for t in higher_priority_tasks
                )
                
                # Check convergence
                if abs(workload - t_prev) < 0.001:
                    break
                
                t_prev = workload
            
            # Check schedulability
            schedulable = workload <= task_i.deadline
            
            results[task_i.id] = {
                'completion_time': workload,
                'deadline': task_i.deadline,
                'schedulable': schedulable,
                'iterations': iteration + 1,
                'margin': task_i.deadline - workload
            }
        
        return results
    
    @staticmethod
    def harmonic_check(tasks: List[PeriodicTask]) -> Tuple[bool, str]:
        """
        Check if a task set has harmonic periods.
        
        A task set is harmonic if for every pair (P_i, P_j) with P_i < P_j, 
        P_j is an integer multiple of P_i.
        
        If harmonic, schedulability bound increases to 100% (utilization ≤ 1).
        
        Args:
            tasks: List of periodic tasks
            
        Returns:
            Tuple of (is_harmonic, explanation)
        """
        if len(tasks) < 2:
            return True, "Task set is harmonic (trivially)"
        
        periods = [task.period for task in tasks]
        periods.sort()
        
        is_harmonic = True
        for i in range(len(periods)):
            for j in range(i+1, len(periods)):
                # Use tolerance for floating-point comparison
                remainder = periods[j] % periods[i]
                # Check if remainder is effectively 0 (within tolerance)
                # remainder close to 0 OR close to periods[i] (wraparound) means harmonic
                if remainder > 0.001 and abs(remainder - periods[i]) > 0.001:
                    is_harmonic = False
                    break
            if not is_harmonic:
                break
        
        if is_harmonic:
            explanation = f"Harmonic task set detected. Schedulability bound = 100% (U ≤ 1.0)"
        else:
            explanation = f"Non-harmonic task set. Use standard RMS bound."
        
        return is_harmonic, explanation
    
    @staticmethod
    def analyze_rms(tasks: List[PeriodicTask]) -> Dict:
        """
        Comprehensive RMS schedulability analysis.
        
        Args:
            tasks: List of periodic tasks
            
        Returns:
            Dictionary with complete analysis results
        """
        results = {}
        
        # Step 1: Check if harmonic
        is_harmonic, harmonic_explanation = SchedulabilityAnalyzer.harmonic_check(tasks)
        results['is_harmonic'] = is_harmonic
        results['harmonic_check'] = harmonic_explanation
        
        # Step 2: Utilization test
        if is_harmonic:
            # For harmonic sets, use simple utilization ≤ 1 test
            total_util = sum(task.utilization for task in tasks)
            schedulable = total_util <= 1.0
            results['utilization_test'] = {
                'schedulable': schedulable,
                'utilization': total_util,
                'bound': 1.0,
                'explanation': f"Harmonic set: U={total_util:.3f} ≤ 1.0 → {'SCHEDULABLE' if schedulable else 'NOT SCHEDULABLE'}"
            }
        else:
            # Standard RMS utilization test
            schedulable, util, bound, explanation = SchedulabilityAnalyzer.rms_utilization_test(tasks)
            results['utilization_test'] = {
                'schedulable': schedulable,
                'utilization': util,
                'bound': bound,
                'explanation': explanation
            }
        
        # Step 3: If utilization test fails, try exact analysis
        if not results['utilization_test']['schedulable']:
            results['exact_analysis'] = SchedulabilityAnalyzer.completion_time_test(tasks)
            estimated_rms_schedulable = all(
                task_result['schedulable'] 
                for task_result in results.get('exact_analysis', {}).values()
            )
            results['final_result'] = estimated_rms_schedulable
        else:
            results['final_result'] = True
        
        return results

