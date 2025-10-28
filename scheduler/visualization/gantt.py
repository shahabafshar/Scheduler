"""Gantt chart visualization for scheduling."""

import plotly.graph_objects as go
from typing import List, Dict, Optional
import pandas as pd
from scheduler.core.task import ScheduleEvent, ScheduleResult


def create_gantt_chart(result: ScheduleResult, max_time: Optional[int] = None) -> go.Figure:
    """
    Create an interactive Gantt chart from schedule events.
    
    Args:
        result: ScheduleResult object from simulation
        max_time: Maximum time to display (default: use max event time)
        
    Returns:
        Plotly figure object
    """
    if not result.events:
        fig = go.Figure()
        fig.add_annotation(text="No events to display", showarrow=False)
        return fig
    
    # Determine time range
    if max_time is None:
        max_time = max(event.time for event in result.events)
    
    # Process events to create Gantt chart data
    # Track when each task starts and stops
    task_intervals = {}  # task_id -> [(start, end), ...]
    colors = {}
    
    current_task = None
    start_time = 0
    
    for i, event in enumerate(result.events):
        if event.time > max_time:
            break
            
        if event.event_type == 'start':
            # New task started
            if current_task is not None:
                # End previous task
                if current_task not in task_intervals:
                    task_intervals[current_task] = []
                task_intervals[current_task].append((start_time, event.time))
            current_task = event.task_id
            start_time = event.time
            
        elif event.event_type in ['complete', 'preempt']:
            # Task ended
            if current_task is not None:
                if current_task not in task_intervals:
                    task_intervals[current_task] = []
                task_intervals[current_task].append((start_time, event.time))
                current_task = None
                start_time = event.time
                
    # Close any remaining task at end of simulation
    if current_task is not None:
        if current_task not in task_intervals:
            task_intervals[current_task] = []
        task_intervals[current_task].append((start_time, max_time))
    
    # Create traces for each task
    task_ids = sorted(set(task_id for task_id in task_intervals.keys() if task_id))
    color_palette = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    
    fig = go.Figure()
    
    for idx, task_id in enumerate(task_ids):
        color = color_palette[idx % len(color_palette)]
        colors[task_id] = color
        
        intervals = task_intervals[task_id]
        
        # Create a bar for each execution interval
        for start, end in intervals:
            duration = end - start
            fig.add_trace(go.Bar(
                y=[task_id],
                x=[duration],
                orientation='h',
                base=[start],
                marker_color=color,
                name=task_id,
                showlegend=idx == 0,  # Only show legend once per task
                customdata=[[f"Start: {start}<br>End: {end}<br>Duration: {duration}"]],
                hovertemplate='%{customdata[0]}<extra></extra>'
            ))
    
    # Add deadline markers
    deadline_events = [evt for evt in result.deadline_misses if evt.time <= max_time]
    if deadline_events:
        deadline_times = [evt.time for evt in deadline_events]
        deadline_tasks = [evt.task_id for evt in deadline_events]
        
        fig.add_trace(go.Scatter(
            x=deadline_times,
            y=deadline_tasks,
            mode='markers',
            marker=dict(symbol='x', size=15, color='red'),
            name='Deadline Miss',
            showlegend=True
        ))
    
    # Configure layout
    fig.update_layout(
        title="Schedule Gantt Chart",
        xaxis_title="Time",
        yaxis_title="Tasks",
        barmode='overlay',
        height=max(400, len(task_ids) * 40 + 150),
        xaxis=dict(
            range=[0, max_time],
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            categoryorder='category ascending',
            showgrid=False
        ),
        hovermode='closest'
    )
    
    return fig


def create_simple_timeline(result: ScheduleResult, max_events: int = 100) -> pd.DataFrame:
    """
    Create a simple timeline table from schedule events.
    
    Args:
        result: ScheduleResult object
        max_events: Maximum number of events to display
        
    Returns:
        DataFrame with timeline information
    """
    data = []
    for i, event in enumerate(result.events[:max_events]):
        data.append({
            'Time': event.time,
            'Task': event.task_id if event.task_id else 'IDLE',
            'Event': event.event_type,
            'Details': str(event.details) if event.details else ''
        })
    
    return pd.DataFrame(data)


def extract_execution_blocks(result: ScheduleResult) -> List[Dict]:
    """
    Extract execution blocks for Gantt chart.
    
    Args:
        result: ScheduleResult object
        
    Returns:
        List of execution blocks with [task_id, start, end]
    """
    blocks = []
    current_task = None
    current_start = 0
    
    for event in result.events:
        if event.event_type == 'start':
            # New task starting
            if current_task is not None:
                # Store previous block
                blocks.append({
                    'task': current_task,
                    'start': current_start,
                    'end': event.time
                })
            current_task = event.task_id
            current_start = event.time
            
        elif event.event_type in ['complete', 'preempt']:
            # Task ending
            if current_task is not None:
                blocks.append({
                    'task': current_task,
                    'start': current_start,
                    'end': event.time
                })
                current_task = None
                current_start = event.time
    
    return blocks


def create_priority_timeline(result: ScheduleResult, max_time: Optional[int] = None) -> go.Figure:
    """
    Create a timeline visualization showing priority changes for dynamic priority algorithms.
    
    Args:
        result: ScheduleResult object from simulation
        max_time: Maximum time to display
        
    Returns:
        Plotly figure object showing priority evolution over time
    """
    if not result.events:
        fig = go.Figure()
        fig.add_annotation(text="No events to display", showarrow=False)
        return fig
    
    if max_time is None:
        max_time = max(event.time for event in result.events)
    
    # Track priority changes (we'll infer from task instances)
    priority_data = {}  # task_id -> [(time, priority, task_id), ...]
    
    # Extract priority information from events
    for event in result.events:
        if event.time > max_time:
            break
        
        # For priority display, we'll show task execution time with priority
        if event.event_type == 'start' and event.task_id:
            task_id = event.task_id
            # Try to get priority from details or task
            priority = 1  # Default
            if event.details and isinstance(event.details, dict):
                priority = event.details.get('priority', 1)
            
            if task_id not in priority_data:
                priority_data[task_id] = []
            priority_data[task_id].append((event.time, priority, task_id))
    
    fig = go.Figure()
    
    for task_id, points in priority_data.items():
        if points:
            times = [p[0] for p in points]
            priorities = [p[1] for p in points]
            
            # Add scatter plot with color intensity based on priority
            fig.add_trace(go.Scatter(
                x=times,
                y=priorities,
                mode='markers+lines',
                name=task_id,
                marker=dict(size=10),
                hovertemplate=f'<b>{task_id}</b><br>Time: %{{x}}<br>Priority: %{{y}}<extra></extra>'
            ))
    
    fig.update_layout(
        title="Priority Changes Over Time",
        xaxis_title="Time",
        yaxis_title="Priority (Higher = More Important)",
        height=400,
        hovermode='closest',
        showlegend=True
    )
    
    return fig

