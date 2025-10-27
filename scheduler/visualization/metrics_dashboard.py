"""Metrics dashboard visualization components."""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List
import pandas as pd
from core.task import ScheduleResult


def create_metrics_dashboard(result: ScheduleResult) -> go.Figure:
    """
    Create a comprehensive metrics dashboard.
    
    Shows:
    1. CPU utilization over time
    2. Task execution timeline
    3. Ready queue length
    4. Response time by task
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'CPU Utilization Over Time',
            'Task Execution Timeline',
            'Context Switches',
            'Utilization by Task'
        ),
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "pie"}]]
    )
    
    events_df = pd.DataFrame([
        {
            'time': e.time,
            'task': e.task_id or 'IDLE',
            'event': e.event_type
        }
        for e in result.events
    ])
    
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
    
    # 2. Event Distribution
    event_types = events_df['event'].value_counts()
    fig.add_trace(
        go.Bar(
            x=event_types.index,
            y=event_types.values,
            name='Event Count',
            marker_color='blue'
        ),
        row=1, col=2
    )
    
    # 3. Context Switches
    if result.total_context_switches > 0:
        fig.add_trace(
            go.Scatter(
                x=['Context Switches'],
                y=[result.total_context_switches],
                mode='markers',
                name='Switches',
                marker=dict(size=[result.total_context_switches * 2], color='orange')
            ),
            row=2, col=1
        )
    
    # 4. Utilization by Task
    task_utilization = {}
    for task in result.tasks:
        exec_time = sum(1 for e in result.events if e.task_id == task.id and e.event_type == 'complete')
        task_utilization[task.id] = exec_time
    
    if task_utilization:
        fig.add_trace(
            go.Pie(
                labels=list(task_utilization.keys()),
                values=list(task_utilization.values()),
                name='Task Utilization'
            ),
            row=2, col=2
        )
    
    fig.update_layout(
        height=800,
        title_text="Real-Time Scheduling Metrics Dashboard",
        showlegend=True
    )
    
    return fig


def create_response_time_chart(result: ScheduleResult) -> go.Figure:
    """Create response time chart for each task."""
    fig = go.Figure()
    
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
                    name=task.id
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

