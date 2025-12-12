"""Metrics dashboard visualization components."""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List
import pandas as pd
from scheduler.core.task import ScheduleResult
from scheduler.visualization.colors import get_task_color_map, extract_task_ids_from_result, TASK_COLOR_PALETTE


def create_metrics_dashboard(result: ScheduleResult) -> go.Figure:
    """
    Create a compact metrics dashboard.

    Shows:
    1. CPU utilization over time
    2. Utilization by task (pie chart)
    """
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            'CPU Utilization Over Time',
            'Utilization by Task'
        ),
        specs=[[{"type": "scatter"}, {"type": "pie"}]]
    )

    # 1. CPU Utilization Over Time
    if len(result.events) > 0:
        max_time = max(e.time for e in result.events)
        timeline = list(range(int(max_time) + 1))
        utilization = []

        for t in timeline:
            busy_count = sum(1 for e in result.events if e.time == t and e.event_type == 'complete')
            utilization.append(busy_count)

        fig.add_trace(
            go.Scatter(
                x=timeline,
                y=utilization,
                mode='lines',
                name='CPU Busy',
                fill='tozeroy',
                line_color='green'
            ),
            row=1, col=1
        )

    # 2. Utilization by Task (using shared colors for consistency with Gantt chart)
    task_utilization = {}
    for task in result.tasks:
        exec_time = sum(1 for e in result.events if e.task_id == task.id and e.event_type == 'complete')
        task_utilization[task.id] = exec_time

    if task_utilization:
        # Get consistent colors using ALL task IDs from result (matching Gantt chart)
        all_task_ids = extract_task_ids_from_result(result)
        task_colors = get_task_color_map(all_task_ids)
        task_ids = sorted(task_utilization.keys())
        pie_colors = [task_colors[tid] for tid in task_ids]

        fig.add_trace(
            go.Pie(
                labels=task_ids,
                values=[task_utilization[tid] for tid in task_ids],
                name='Task Utilization',
                marker=dict(colors=pie_colors)
            ),
            row=1, col=2
        )

    fig.update_layout(
        height=400,
        title_text="Scheduling Metrics",
        showlegend=True
    )

    return fig


def create_response_time_chart(result: ScheduleResult) -> go.Figure:
    """Create response time chart for each task."""
    fig = go.Figure()

    # Get consistent task colors using ALL task IDs from result
    all_task_ids = extract_task_ids_from_result(result)
    task_colors = get_task_color_map(all_task_ids)

    for task in result.tasks:
        task_events = [e for e in result.events if e.task_id == task.id]
        if task_events:
            times = [e.time for e in task_events]
            response_times = [e.time for e in task_events if e.event_type == 'complete']

            if response_times:
                fig.add_trace(go.Scatter(
                    x=list(range(len(response_times))),
                    y=response_times,
                    mode='lines+markers',
                    name=task.id,
                    line=dict(color=task_colors.get(task.id)),
                    marker=dict(color=task_colors.get(task.id))
                ))
    
    fig.update_layout(
        title='Response Times by Task',
        xaxis_title='Instance Number',
        yaxis_title='Completion Time',
        height=400
    )
    
    return fig


def create_laxity_over_time(result: ScheduleResult) -> go.Figure:
    """Create laxity chart over time (if LLF scheduler)."""
    fig = go.Figure()
    
    # This would need to track laxity during simulation
    # For now, show as placeholder
    fig.add_trace(go.Scatter(
        x=[1, 2, 3],
        y=[5, 3, 2],
        mode='lines',
        name='Laxity (placeholder)'
    ))
    
    fig.update_layout(
        title='Laxity Over Time',
        xaxis_title='Time',
        yaxis_title='Laxity',
        height=400
    )
    
    return fig


def create_service_level_plot(result: ScheduleResult) -> go.Figure:
    """
    Create a plot showing FC-EDF service level changes over time.
    
    Args:
        result: ScheduleResult object from simulation with service level information
        
    Returns:
        Plotly figure object showing version changes
    """
    # Try to extract service level information from result
    service_level_data = []
    
    # Look for version change events or service level information
    for event in result.events:
        if hasattr(event, 'details') and event.details:
            if isinstance(event.details, dict) and 'version' in event.details:
                service_level_data.append({
                    'time': event.time,
                    'task': event.task_id,
                    'version': event.details.get('version')
                })
    
    if not service_level_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No service level changes detected (FC-EDF not used or no version changes)",
            showarrow=False
        )
        fig.update_layout(title="Service Level Changes", height=300)
        return fig
    
    fig = go.Figure()

    # Group by task and get consistent colors using ALL task IDs from result
    all_task_ids = extract_task_ids_from_result(result)
    task_colors = get_task_color_map(all_task_ids)
    tasks = sorted(set(item['task'] for item in service_level_data if item['task']))

    for task in tasks:
        task_data = [item for item in service_level_data if item['task'] == task]
        times = [item['time'] for item in task_data]
        versions = [item['version'] for item in task_data]
        color = task_colors.get(task)

        fig.add_trace(go.Scatter(
            x=times,
            y=versions,
            mode='markers+lines',
            name=task,
            marker=dict(size=8, color=color),
            line=dict(color=color),
            hovertemplate=f'<b>{task}</b><br>Time: %{{x}}<br>Version: %{{y}}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Service Level Changes Over Time (FC-EDF)",
        xaxis_title="Time",
        yaxis_title="Service Level Version",
        height=400,
        hovermode='closest'
    )
    
    return fig
