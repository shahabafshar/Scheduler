# Visualization Features Guide

This document details the advanced visualization features implemented in the Real-Time Scheduling Simulator.

## 1. Priority Changes Timeline 📈

### Purpose
Visualizes how task priorities change over time for dynamic priority scheduling algorithms.

### Applicable Algorithms
- **EDF (Earliest Deadline First)** - Priorities based on absolute deadlines
- **LLF (Least Laxity First)** - Priorities based on laxity (deadline - remaining time)
- **DMS (Deadline Monotonic)** - Priorities based on relative deadlines

### Features
- **Interactive Plot**: Hover to see exact priority values at each time point
- **Multi-Task View**: All tasks are displayed on the same chart for comparison
- **Color-Coded**: Each task has a distinct color for easy identification
- **Timeline Range**: Matches the simulation duration

### Implementation Details

#### Function Signature
```python
def create_priority_timeline(result: ScheduleResult, max_time: Optional[int] = None) -> go.Figure
```

#### Parameters
- `result`: ScheduleResult object from simulation
- `max_time`: Maximum time to display (optional)

#### Returns
- Plotly Figure object with interactive timeline

### Usage in App
The priority timeline automatically appears when running:
- EDF scheduling
- LLF scheduling  
- DMS scheduling

Located in the results section after the Gantt chart.

### Example Output
```
Priority Changes Over Time
├── X-axis: Time (0 to simulation duration)
├── Y-axis: Priority (Higher = More Important)
└── Legend: Task IDs (T1, T2, T3, etc.)
```

---

## 2. Precedence Graph Display 🔗

### Purpose
Visualizes task dependencies and precedence constraints as a network diagram.

### Applicable Scenarios
- When precedence constraints are defined
- For RMS/EDF/DMS with Precedence algorithms
- Task dependency analysis

### Features
- **Network Diagram**: Tasks as nodes, dependencies as directed edges
- **Circular Layout**: Tasks arranged in a circle for clarity
- **Arrow Indicators**: Clear directional arrows showing predecessor → successor
- **Interactive Nodes**: Hover over tasks to see their IDs
- **Constraint Count**: Shows total number of dependencies

### Implementation Details

#### Function Signature
```python
def create_precedence_graph(
    precedence_constraints: List[PrecedenceConstraint], 
    tasks: List[PeriodicTask] = None
) -> go.Figure
```

#### Parameters
- `precedence_constraints`: List of PrecedenceConstraint objects
- `tasks`: Optional list of PeriodicTask objects (for enhanced display)

#### Returns
- Plotly Figure object with network diagram

### Usage in App
The precedence graph appears when:
1. Precedence constraints are enabled (checkbox)
2. At least one constraint is defined (e.g., "T1 -> T2")

Located in the results section after the metrics dashboard.

### Defining Precedence Constraints
In the app's "Precedence Constraints" section, enter dependencies as:
```
T1 -> T2
T1 -> T3
T2 -> T3
```

This creates a precedence graph:
```
    T1
   ↙  ↘
  T2   T3
   ↘  ↗
    T3
```

### Example Output
```
Precedence Graph
├── Nodes: Task circles with IDs
├── Edges: Lines with arrows showing dependencies
├── Layout: Circular arrangement
└── Caption: "N dependencies shown"
```

---

## Integration with Main App

### Location in app.py
Both visualizations are integrated in the results display section:

```python
# Line 666-672: Priority Changes Timeline
if "EDF" in algorithm or "LLF" in algorithm or "DMS" in algorithm:
    st.subheader("📈 Priority Changes Timeline")
    priority_fig = create_priority_timeline(result, max_time=duration)
    st.plotly_chart(priority_fig, use_container_width=True)

# Line 657-663: Precedence Graph
if enable_precedence and precedence_constraints:
    st.subheader("🔗 Precedence Graph")
    prec_fig = create_precedence_graph(precedence_constraints, periodic_tasks)
    st.plotly_chart(prec_fig, use_container_width=True)
```

### Error Handling
Both visualizations include try-catch blocks to gracefully handle:
- Empty data
- Missing constraints
- Invalid inputs

### User Experience Flow
1. User configures tasks and selects algorithm
2. User runs simulation
3. Results appear in order:
   - Schedulability Analysis
   - Gantt Chart
   - Metrics Dashboard
   - **Precedence Graph** (if applicable)
   - **Priority Timeline** (if applicable)
   - Additional visualizations (service levels, (m,k) history, etc.)

---

## Technical Implementation

### File Structure
```
scheduler/visualization/
├── __init__.py              # Exports all visualization functions
├── gantt.py                 # Gantt chart + Priority Timeline
└── precedence_graph.py      # Precedence Graph
```

### Dependencies
- `plotly.graph_objects` - Interactive plotting
- `pandas` - Data manipulation
- `scheduler.core.task` - Data models

### Import Paths
All imports use absolute paths for consistency:
```python
from scheduler.core.task import ScheduleResult, PrecedenceConstraint
from scheduler.visualization.gantt import create_priority_timeline
from scheduler.visualization.precedence_graph import create_precedence_graph
```

---

## Testing

### Test Suite
Run comprehensive tests with:
```bash
python test_visualizations.py
```

### Test Coverage
- ✅ Priority timeline with EDF
- ✅ Priority timeline with RMS
- ✅ Precedence graph with multiple constraints
- ✅ Precedence graph with empty constraints
- ✅ Precedence graph with single constraint
- ✅ Integration with schedulers

### Expected Output
```
============================================================
VISUALIZATION FEATURES TEST
============================================================

=== Testing Priority Changes Timeline ===
✅ Priority timeline created successfully

=== Testing Precedence Graph Display ===
✅ Precedence graph created successfully

=== Integration Test ===
✅ RMS priority timeline works
✅ Empty precedence graph handles gracefully
✅ Simple precedence graph works

============================================================
✅ ALL TESTS PASSED
============================================================
```

---

## Future Enhancements (Optional)

### Priority Timeline
- [ ] Add priority threshold markers
- [ ] Show preemption events on timeline
- [ ] Export priority data as CSV

### Precedence Graph
- [ ] Hierarchical layout (top-down)
- [ ] Show modified parameters on nodes
- [ ] Critical path highlighting
- [ ] Interactive node editing

---

## Troubleshooting

### Issue: Priority timeline shows empty chart
**Solution**: Ensure events contain priority information in details dict

### Issue: Precedence graph shows "No constraints"
**Solution**: Verify precedence_constraints list is not empty

### Issue: Import errors
**Solution**: Use absolute imports: `from scheduler.visualization.gantt import ...`

---

## Summary

| Feature | Status | Location | Applicable Algorithms |
|---------|--------|----------|----------------------|
| Priority Changes Timeline | ✅ Complete | gantt.py | EDF, LLF, DMS |
| Precedence Graph Display | ✅ Complete | precedence_graph.py | All with precedence |

Both features are production-ready and fully integrated into the Streamlit app.

