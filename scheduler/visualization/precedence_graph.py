"""Precedence graph visualization for task dependencies."""

import plotly.graph_objects as go
from typing import List, Dict, Optional
from scheduler.core.task import PrecedenceConstraint, PeriodicTask, ScheduleResult


def create_precedence_graph(precedence_constraints: List[PrecedenceConstraint], 
                           tasks: List[PeriodicTask] = None) -> go.Figure:
    """
    Create a network diagram showing task precedence dependencies.
    
    Args:
        precedence_constraints: List of precedence relationships
        tasks: Optional list of tasks to show modified parameters
        
    Returns:
        Plotly figure object with network diagram
    """
    if not precedence_constraints:
        fig = go.Figure()
        fig.add_annotation(text="No precedence constraints defined", showarrow=False)
        return fig
    
    # Build node positions (simple layout)
    tasks_in_graph = set()
    for prec in precedence_constraints:
        tasks_in_graph.add(prec.predecessor)
        tasks_in_graph.add(prec.successor)
    
    # Create mapping from task to node index
    task_to_node = {task_id: idx for idx, task_id in enumerate(sorted(tasks_in_graph))}
    num_nodes = len(task_to_node)
    
    # Calculate circular positions for nodes
    import math
    positions = {}
    center_x, center_y = 400, 300
    radius = 150
    
    for task_id, node_idx in task_to_node.items():
        angle = (2 * math.pi * node_idx) / num_nodes if num_nodes > 0 else 0
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        positions[task_id] = (x, y)
    
    # Create edges
    edge_x = []
    edge_y = []
    for prec in precedence_constraints:
        pred_pos = positions.get(prec.predecessor)
        succ_pos = positions.get(prec.successor)
        
        if pred_pos and succ_pos:
            edge_x.extend([pred_pos[0], succ_pos[0], None])
            edge_y.extend([pred_pos[1], succ_pos[1], None])
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        showlegend=False
    ))
    
    # Add nodes
    node_x = [pos[0] for pos in positions.values()]
    node_y = [pos[1] for pos in positions.values()]
    
    # Add node trace
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(
            symbol='circle',
            size=60,
            color='lightblue',
            line=dict(width=2, color='black')
        ),
        text=[task_id for task_id in sorted(task_to_node.keys())],
        textposition="middle center",
        textfont=dict(size=14, color='black'),
        hovertemplate='<b>%{text}</b><extra></extra>',
        name='Tasks',
        showlegend=False
    ))
    
    # Add arrows for edges (using annotations)
    for prec in precedence_constraints:
        pred_pos = positions.get(prec.predecessor)
        succ_pos = positions.get(prec.successor)
        
        if pred_pos and succ_pos:
            # Calculate arrow position (near successor)
            dx = succ_pos[0] - pred_pos[0]
            dy = succ_pos[1] - pred_pos[1]
            length = math.sqrt(dx*dx + dy*dy)
            
            if length > 0:
                # Normalize and scale back
                dx_norm = dx / length
                dy_norm = dy / length
                
                # Arrow at 80% from predecessor to successor
                arrow_start = (
                    pred_pos[0] + dx_norm * (length * 0.75),
                    pred_pos[1] + dy_norm * (length * 0.75)
                )
                
                fig.add_annotation(
                    x=succ_pos[0],
                    y=succ_pos[1],
                    ax=arrow_start[0],
                    ay=arrow_start[1],
                    arrowhead=2,
                    arrowsize=1.5,
                    arrowcolor='#333',
                    axref='x',
                    ayref='y'
                )
    
    # Update layout
    fig.update_layout(
        title="Precedence Graph",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=600,
        annotations=[
            dict(
                text=f"{len(precedence_constraints)} dependencies shown",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=-0.1,
                xanchor='center', yanchor='bottom',
                font=dict(size=12, color='gray')
            )
        ]
    )
    
    return fig

