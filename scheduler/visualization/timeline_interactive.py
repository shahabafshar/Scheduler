"""Interactive step-by-step timeline viewer."""

import plotly.graph_objects as go
from typing import List, Optional
from scheduler.core.task import ScheduleResult, ScheduleEvent


def create_timeline_step_viewer(result: ScheduleResult, current_step: int = 0) -> dict:
    """
    Create data for step-by-step timeline viewer at a specific step.
    
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
    event = result.events[current_step]
    
    # Extract state information from event context
    state = {
        'time': event.time,
        'current_task': event.task_id if event.task_id else 'IDLE',
        'event_type': event.event_type,
        'details': event.details if hasattr(event, 'details') else {}
    }
    
    # Build explanation
    explanations = []
    explanations.append(f"Time: {event.time}")
    explanations.append(f"Event: {event.event_type}")
    
    if event.task_id:
        explanations.append(f"Task: {event.task_id}")
    else:
        explanations.append("CPU: IDLE")
    
    if hasattr(event, 'details') and event.details:
        if isinstance(event.details, dict):
            for key, value in event.details.items():
                explanations.append(f"{key}: {value}")
    
    explanation = "<br>".join(explanations)
    
    # Create a simple figure showing the current state
    fig = go.Figure()
    
    # Add a text display
    fig.add_annotation(
        text=f"<b>Step {current_step + 1}/{total_steps}</b><br><br>{explanation}",
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        xanchor='center', yanchor='middle',
        showarrow=False,
        font=dict(size=14)
    )
    
    fig.update_layout(
        title="Timeline Step View",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        showlegend=False
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

