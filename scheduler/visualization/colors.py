"""Shared color utilities for consistent visualization across all charts."""

from typing import Dict, List, Set

# Standard 10-color palette for task visualization
# These colors are colorblind-friendly and have good contrast
TASK_COLOR_PALETTE = [
    '#1f77b4',  # Blue
    '#ff7f0e',  # Orange
    '#2ca02c',  # Green
    '#d62728',  # Red
    '#9467bd',  # Purple
    '#8c564b',  # Brown
    '#e377c2',  # Pink
    '#7f7f7f',  # Gray
    '#bcbd22',  # Olive
    '#17becf',  # Cyan
]

# Semantic colors for events (not tied to task identity)
EVENT_COLORS = {
    'start': '#2ca02c',       # Green - task starting
    'complete': '#1f77b4',    # Blue - task completed
    'preempt': '#ff7f0e',     # Orange - task preempted
    'deadline_miss': '#d62728',  # Red - deadline missed
    'idle': '#cccccc',        # Light gray - CPU idle
    'arrival': '#9467bd',     # Purple - task arrival
}

# Special colors
DEADLINE_MARKER_COLOR = '#d62728'  # Red for deadline markers
CURRENT_HIGHLIGHT_COLOR = 'gold'   # Gold for currently selected event
IDLE_COLOR = '#e0e0e0'             # Light gray for idle periods


def get_task_color_map(task_ids: List[str]) -> Dict[str, str]:
    """
    Create a deterministic task-to-color mapping.

    Task IDs are sorted alphabetically to ensure consistent color assignment
    across different visualizations and simulation runs.

    Args:
        task_ids: List of task identifiers

    Returns:
        Dictionary mapping task_id -> hex color string
    """
    # Sort to ensure consistent ordering
    sorted_ids = sorted(set(tid for tid in task_ids if tid))

    return {
        task_id: TASK_COLOR_PALETTE[i % len(TASK_COLOR_PALETTE)]
        for i, task_id in enumerate(sorted_ids)
    }


def get_task_color(task_id: str, task_color_map: Dict[str, str]) -> str:
    """
    Get color for a specific task from a color map.

    Args:
        task_id: Task identifier
        task_color_map: Pre-computed color mapping

    Returns:
        Hex color string, or gray if task not in map
    """
    return task_color_map.get(task_id, '#7f7f7f')


def extract_task_ids_from_events(events) -> List[str]:
    """
    Extract unique task IDs from a list of schedule events.

    Args:
        events: List of ScheduleEvent objects

    Returns:
        Sorted list of unique task IDs
    """
    return sorted(set(e.task_id for e in events if e.task_id))


def extract_task_ids_from_result(result) -> List[str]:
    """
    Extract unique task IDs from a ScheduleResult.

    Args:
        result: ScheduleResult object

    Returns:
        Sorted list of unique task IDs
    """
    task_ids = set()

    # From events
    if hasattr(result, 'events') and result.events:
        for e in result.events:
            if e.task_id:
                task_ids.add(e.task_id)

    # From tasks list
    if hasattr(result, 'tasks') and result.tasks:
        for t in result.tasks:
            if hasattr(t, 'id'):
                task_ids.add(t.id)

    return sorted(task_ids)
