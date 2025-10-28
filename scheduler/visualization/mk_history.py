"""(m,k)-Firm guarantee history visualization."""

import plotly.graph_objects as go
from typing import List, Dict, Optional
from scheduler.core.task import ScheduleResult, ScheduleEvent


def create_mk_history_chart(result: ScheduleResult, task_id: str, m: int, k: int) -> go.Figure:
    """
    Create a visualization showing (m,k)-firm guarantee history for a task.
    
    Shows the last k task instances and whether each met its deadline.
    
    Args:
        result: ScheduleResult object from simulation
        task_id: Task ID to visualize
        m: Number of instances that must meet deadline
        k: Window size for (m,k)-firm guarantee
        
    Returns:
        Plotly figure object showing sliding window guarantee
    """
    # Find instances of this task
    instances = []
    instance_num = 0
    current_deadline = None
    
    for event in result.events:
        if event.task_id != task_id:
            continue
        
        if event.event_type == 'start':
            # Extract deadline from event details if available
            if event.details and isinstance(event.details, dict):
                current_deadline = event.details.get('deadline')
            instance_num += 1
        
        elif event.event_type == 'complete':
            # Check if it met deadline
            met_deadline = True
            if current_deadline and event.time > current_deadline:
                met_deadline = False
            
            instances.append({
                'instance': instance_num,
                'completion_time': event.time,
                'deadline': current_deadline,
                'met_deadline': met_deadline
            })
    
    # Get last k instances
    recent_instances = instances[-k:] if len(instances) >= k else instances
    
    if not recent_instances:
        fig = go.Figure()
        fig.add_annotation(text=f"No instances found for task {task_id}", showarrow=False)
        return fig
    
    # Count how many met deadline
    met_count = sum(1 for inst in recent_instances if inst['met_deadline'])
    
    # Create figure
    fig = go.Figure()
    
    # Add bars for each instance
    instance_nums = [inst['instance'] for inst in recent_instances]
    colors = ['green' if inst['met_deadline'] else 'red' for inst in recent_instances]
    
    fig.add_trace(go.Bar(
        x=instance_nums,
        y=[1 for _ in recent_instances],  # Height of 1 for each instance
        marker_color=colors,
        name='Instance',
        hovertemplate='<b>Instance %{x}</b><br>Status: %{customdata}<extra></extra>',
        customdata=[('Met' if inst['met_deadline'] else 'Missed') for inst in recent_instances]
    ))
    
    # Add m-line (horizontal line showing required threshold)
    fig.add_hline(
        y=m, 
        line_dash="dash", 
        line_color="blue",
        annotation_text=f"Required: m={m}",
        annotation_position="right"
    )
    
    # Add status text
    guarantee_met = met_count >= m
    status_color = 'green' if guarantee_met else 'red'
    status_text = f"(m,k)-Firm Guarantee: {'MET' if guarantee_met else 'FAILED'}"
    
    fig.update_layout(
        title=f"(m,k)-Firm Guarantee History for {task_id} (m={m}, k={k})",
        xaxis_title="Instance Number",
        yaxis_title="Number of Instances",
        height=400,
        showlegend=False,
        annotations=[
            dict(
                text=status_text,
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=0.95,
                xanchor='center', yanchor='top',
                font=dict(size=14, color=status_color, family='Arial Black')
            ),
            dict(
                text=f"Last k={k} instances: {met_count} met deadline",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=0.05,
                xanchor='center', yanchor='bottom',
                font=dict(size=12, color='black')
            )
        ]
    )
    
    return fig

