"""Interactive step-by-step timeline viewer."""

import plotly.graph_objects as go
from typing import List, Optional, Dict
from scheduler.core.task import ScheduleResult, ScheduleEvent
from scheduler.visualization.colors import get_task_color_map, extract_task_ids_from_result, EVENT_COLORS, CURRENT_HIGHLIGHT_COLOR


def create_timeline_step_viewer(result: ScheduleResult, current_step: int = 0) -> dict:
    """
    Create an interactive step-by-step timeline viewer showing execution up to current step.

    Args:
        result: ScheduleResult object from simulation
        current_step: Current timeline step to display

    Returns:
        Dictionary with visualization data and state information
    """
    if not result.events:
        return {
            'figure': None,
            'state': {},
            'total_steps': 0,
            'current_step': 0,
            'explanation': 'No events to display'
        }

    total_steps = len(result.events)
    if current_step < 0:
        current_step = 0
    if current_step >= total_steps:
        current_step = total_steps - 1

    # Get event at current step
    current_event = result.events[current_step]

    # Extract state information from event context
    state = {
        'time': current_event.time,
        'current_task': current_event.task_id if current_event.task_id else 'IDLE',
        'event_type': current_event.event_type,
        'details': current_event.details if hasattr(current_event, 'details') else {}
    }

    # Build explanation
    explanations = []
    explanations.append(f"**Step {current_step + 1}/{total_steps}**")
    explanations.append(f"Time: {current_event.time}")
    explanations.append(f"Event: {current_event.event_type.upper()}")

    if current_event.task_id:
        explanations.append(f"Task: {current_event.task_id}")
    else:
        explanations.append("CPU: IDLE")

    if hasattr(current_event, 'details') and current_event.details:
        if isinstance(current_event.details, dict):
            for key, value in current_event.details.items():
                explanations.append(f"{key}: {value}")

    explanation = " | ".join(explanations)

    # Create visual timeline showing execution up to current step
    fig = go.Figure()

    # Process events up to current step to build execution intervals
    task_intervals: Dict[str, List[tuple]] = {}  # task_id -> [(start, end, is_current), ...]
    running_task = None
    start_time = 0

    # Get ALL task IDs from result for consistent coloring (shared across all visualizations)
    all_task_ids = extract_task_ids_from_result(result)
    task_colors = get_task_color_map(all_task_ids)

    # Process events up to current step
    for i, event in enumerate(result.events[:current_step + 1]):
        is_current = (i == current_step)

        if event.event_type == 'start':
            if running_task is not None:
                # End previous task
                if running_task not in task_intervals:
                    task_intervals[running_task] = []
                task_intervals[running_task].append((start_time, event.time, False))
            running_task = event.task_id
            start_time = event.time

        elif event.event_type in ['complete', 'preempt']:
            if running_task is not None:
                if running_task not in task_intervals:
                    task_intervals[running_task] = []
                task_intervals[running_task].append((start_time, event.time, is_current))
                running_task = None
                start_time = event.time

    # If a task is still running at current step, extend to current time
    if running_task is not None:
        if running_task not in task_intervals:
            task_intervals[running_task] = []
        task_intervals[running_task].append((start_time, current_event.time + 0.5, True))

    # Determine time range for display
    max_time = max(e.time for e in result.events) if result.events else 10
    current_time = current_event.time

    # Draw all tasks (for context)
    legend_shown = set()
    for task_id in all_task_ids:
        color = task_colors[task_id]

        # Draw a faded background line for future execution
        fig.add_trace(go.Scatter(
            x=[0, max_time],
            y=[task_id, task_id],
            mode='lines',
            line=dict(color='lightgray', width=20),
            showlegend=False,
            hoverinfo='skip'
        ))

        # Draw executed intervals
        intervals = task_intervals.get(task_id, [])
        for start, end, is_current in intervals:
            duration = end - start
            if duration > 0:
                show_legend = task_id not in legend_shown
                if show_legend:
                    legend_shown.add(task_id)

                # Use brighter color for current event, normal for past
                bar_color = color if not is_current else CURRENT_HIGHLIGHT_COLOR
                border_color = 'black' if is_current else color

                fig.add_trace(go.Bar(
                    y=[task_id],
                    x=[duration],
                    orientation='h',
                    base=[start],
                    marker=dict(
                        color=bar_color,
                        line=dict(color=border_color, width=3 if is_current else 0)
                    ),
                    name=task_id,
                    showlegend=show_legend,
                    legendgroup=task_id,
                    hovertemplate=f'{task_id}<br>Start: {start}<br>End: {end}<extra></extra>'
                ))

    # Add vertical line for current time
    fig.add_vline(
        x=current_time,
        line=dict(color='red', width=2, dash='dash'),
        annotation_text=f"t={current_time}",
        annotation_position="top"
    )

    # Add event markers (using shared event colors for consistency)
    event_markers = {
        'start': ('triangle-up', EVENT_COLORS['start'], 12),
        'complete': ('circle', EVENT_COLORS['complete'], 10),
        'preempt': ('diamond', EVENT_COLORS['preempt'], 10),
        'deadline_miss': ('x', EVENT_COLORS['deadline_miss'], 15),
        'idle': ('square', EVENT_COLORS['idle'], 8),
    }

    # Show current event marker
    marker_info = event_markers.get(current_event.event_type, ('circle', 'purple', 10))
    fig.add_trace(go.Scatter(
        x=[current_time],
        y=[current_event.task_id if current_event.task_id else 'IDLE'],
        mode='markers',
        marker=dict(
            symbol=marker_info[0],
            color=marker_info[1],
            size=marker_info[2],
            line=dict(color='black', width=2)
        ),
        name=f'Current: {current_event.event_type}',
        showlegend=True
    ))

    # Configure layout
    fig.update_layout(
        title=f"Timeline at Step {current_step + 1}: {current_event.event_type.upper()} at t={current_time}",
        xaxis_title="Time",
        yaxis_title="Tasks",
        barmode='overlay',
        height=max(300, len(all_task_ids) * 50 + 150),
        xaxis=dict(
            range=[-0.5, max_time + 1],
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            dtick=max(1, int(max_time / 20))
        ),
        yaxis=dict(
            categoryorder='category ascending',
            showgrid=False
        ),
        hovermode='closest',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        )
    )

    return {
        'figure': fig,
        'state': state,
        'total_steps': total_steps,
        'current_step': current_step,
        'explanation': explanation
    }


def create_timeline_summary(result: ScheduleResult) -> dict:
    """
    Create a summary of the timeline with all events.

    Args:
        result: ScheduleResult object

    Returns:
        Dictionary with timeline summary
    """
    if not result.events:
        return {
            'total_events': 0,
            'events_by_type': {},
            'time_range': (0, 0)
        }

    events_by_type = {}
    for event in result.events:
        event_type = event.event_type
        if event_type not in events_by_type:
            events_by_type[event_type] = 0
        events_by_type[event_type] += 1

    min_time = min(e.time for e in result.events)
    max_time = max(e.time for e in result.events)

    return {
        'total_events': len(result.events),
        'events_by_type': events_by_type,
        'time_range': (min_time, max_time)
    }
