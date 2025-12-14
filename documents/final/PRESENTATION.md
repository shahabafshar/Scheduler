# Real-Time Scheduling Simulator
## Server-Based Algorithms for Mixed Periodic-Aperiodic Workloads

**Shahab Afshar**

*CPR E 458/558: Real-Time Systems, Fall 2024*

*Department of Electrical and Computer Engineering*
*Iowa State University*

*Instructor: Dr. G. Manimaran*

---

# Slide 1: Title

## Real-Time Scheduling Simulator
### Server-Based Algorithms for Mixed Periodic-Aperiodic Workloads

**Shahab Afshar**

CPR E 458/558: Real-Time Systems
Fall 2024

Department of Electrical and Computer Engineering
Iowa State University

---

# Slide 2: Problem Statement

## The Challenge

**Real-time systems must satisfy timing constraints** in addition to functional correctness.

### The Gap

- **Theoretical analysis** provides utilization bounds but doesn't show temporal behavior
- **Manual schedule construction** is tedious and error-prone
- **RTOS testing** requires significant development effort
- Engineers need to **explore algorithm behavior** before committing to implementation

### Research Questions

| ID | Question |
|----|----------|
| **RQ1** | Can a discrete-event simulator faithfully implement server capacity management policies? |
| **RQ2** | Does interactive visualization help users understand algorithm differences? |
| **RQ3** | Can parameter exploration (varying Cₛ/Pₛ) reveal optimal configurations? |

![System Model](figures/system_diagram.png)

---

# Slide 3: Solution Overview (1/2)

## Four Server-Based Scheduling Algorithms

| Algorithm | Capacity Management | Response Time |
|-----------|-------------------|---------------|
| **Polling Server** | Lost if no aperiodic tasks | Moderate |
| **Deferrable Server** | Preserved until period end | Good |
| **Sporadic Server** | Dynamic replenishment at t+Pₛ | Best |
| **Background Scheduler** | Runs during idle only | Worst |

### Key Differentiator: Capacity Management Policy

![Server Algorithm Comparison](figures/server_comparison.jpg)

*Figure: Visual comparison of server capacity management strategies*

---

# Slide 4: Solution Overview (2/2)

## Interactive Simulation Platform

### Core Features

1. **Discrete-event simulation** with exact algorithm implementation
2. **Interactive Gantt charts** showing capacity events
3. **Parameter exploration** via sliders (Cₛ, Pₛ)
4. **21 preset configurations** for quick experimentation
5. **Schedulability analysis** (RMS, EDF, DMS bounds)

### Supported Algorithms

- **Basic:** RMS, EDF, DMS, LLF
- **Server-Based:** Polling, Deferrable, Sporadic, Background
- **Advanced:** Precedence-constrained, Overload handling, Value-based (HVDF)

![Full Application Layout](../../user_guide/screenshots/part1-getting-started/part1-02-full-layout.png)

---

# Slide 5: Implementation Details (1/2)

## Software Architecture

### Layered Design with Clear Separation of Concerns

![Layered Architecture](figures/layered_architecture.png)

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Core Logic | Python 3.10+ | Simulation engine |
| Web UI | Streamlit | Interactive dashboard |
| Visualization | Plotly | Gantt charts, metrics |
| Data Handling | Pandas | Task tables, export |

---

# Slide 6: Implementation Details (2/2)

## Design Pattern: Template Method

**Key Insight:** All schedulers share the same simulation loop; only priority assignment differs.

![Class Hierarchy](figures/class_hierarchy.png)

### Server-Specific Hooks

```python
class ServerSchedulerBase(SchedulerBase):
    def _handle_replenishment(self, t):
        """When/how to replenish capacity"""

    def _execute_server_slot(self, t):
        """What to do when server has priority"""
```

### Capacity Management Difference

| Server | `_execute_server_slot()` when no aperiodic tasks |
|--------|--------------------------------------------------|
| Polling | `self.server_remaining = 0` (capacity lost) |
| Deferrable | `return False` (capacity preserved) |
| Sporadic | Schedule replenishment at `t + Pₛ` |

---

# Slide 7: Testing & Evaluation Results (1/2)

## Correctness Validation (RQ1)

### Server Behavior Verification

| Server Type | Expected Behavior | Verified |
|-------------|-------------------|----------|
| Polling | `capacity_lost` events when idle | ✓ |
| Deferrable | `deferred` events preserve capacity | ✓ |
| Sporadic | `replenish` events at t + Pₛ | ✓ |
| Background | Runs only during CPU idle | ✓ |

### Gantt Chart Evidence

![Polling Server Gantt](../../user_guide/screenshots/part3-server-algorithms/part3-polling-02-gantt-chart.png)

*Polling Server: Gantt chart shows task execution and server events*

---

# Slide 8: Testing & Evaluation Results (2/2)

## Parameter Sensitivity Results (RQ3)

### Server Capacity Effect on Aperiodic Response Time

**Workload:** P1(C=1,P=10), P2(C=1,P=15), A1(C=8, arrives t=0)

| Cₛ | Pₛ | A1 Response Time | Replenishments |
|----|----|-----------------:|---------------:|
| 2 | 5 | 17 | 4 |
| 4 | 5 | 9 | 2 |
| 8 | 5 | 8 | 1 |

**Finding:** Larger Cₛ reduces aperiodic response time by reducing replenishment cycles.

### Visualization Effectiveness (RQ2)

- Color-coded task bars distinguish periodic vs. aperiodic
- Red triangles mark deadlines
- Server events (`replenish`, `deferred`, `capacity_lost`) labeled on timeline
- Hover tooltips show remaining computation time

![Sporadic Server Gantt with Events](../../user_guide/screenshots/part3-server-algorithms/part3-sporadic-01-gantt.png)

---

# Slide 9: Conclusions

## Research Question Answers

### RQ1: Faithful Implementation ✓
Simulator correctly implements capacity management as verified by observing expected events (`capacity_lost`, `deferred`, `replenish`).

### RQ2: Visualization Effectiveness ✓
Gantt charts clearly show when capacity is lost vs. preserved. Users can visually compare algorithm behavior.

### RQ3: Parameter Exploration ✓
Varying Cₛ from 2→8 shows response time reduction (17→8 time units), enabling optimal configuration discovery.

## Key Contributions

1. **Open-source simulator** with 4 server algorithms
2. **Interactive Gantt charts** displaying capacity events
3. **21 preset configurations** from literature examples
4. **Parameter exploration** via sliders
5. **Schedulability analysis** (RMS, EDF, DMS)

---

# Slide 10: Learning Achieved

## Technical Skills Developed

### Real-Time Systems Concepts
- Deep understanding of server-based scheduling (Polling, Deferrable, Sporadic)
- RMS utilization bounds and schedulability analysis
- Capacity management policies and their trade-offs

### Software Engineering
- **Template Method pattern** for extensible scheduler architecture
- **Strategy pattern** for composable priority policies
- Event-driven simulation design

### Tools & Technologies
- Python for discrete-event simulation
- Streamlit for rapid web UI development
- Plotly for interactive visualizations

## Lessons Learned

1. **Simulation reveals behavior** that formulas cannot show
2. **Visualization is essential** for understanding scheduling dynamics
3. **Parameter exploration** enables informed design decisions
4. **Modular architecture** simplifies adding new algorithms

---

# Appendix: Additional Screenshots

## Server Algorithm Comparisons

### Deferrable Server
![Deferrable Server Gantt](../../user_guide/screenshots/part3-server-algorithms/part3-deferrable-01-gantt.png)

### Server Analysis Dashboard

![Server Analysis](../../user_guide/screenshots/part3-server-algorithms/part3-polling-03-server-analysis.png)

### Background Scheduler
![Background Scheduler Gantt](../../user_guide/screenshots/part3-server-algorithms/part3-background-01-gantt.png)

---

## Basic Algorithm Results

### RMS Gantt Chart
![RMS Gantt](../../user_guide/screenshots/part2-basic-algorithms/part2-rms-04-gantt-chart.png)

### EDF Priority Timeline
![EDF Priority Timeline](../../user_guide/screenshots/part2-basic-algorithms/part2-edf-04-priority-timeline.png)

---

## UI Overview

### Full Application Layout
![Full Layout](../../user_guide/screenshots/part1-getting-started/part1-02-full-layout.png)

### Preset System
![Preset Dialog](../../user_guide/screenshots/part8-presets/part8-01-preset-dialog.png)

---

# References

[1] B. Sprunt, L. Sha, and J. Lehoczky, "Aperiodic task scheduling for hard-real-time systems," *Real-Time Systems*, vol. 1, no. 1, pp. 27-60, 1989.

[2] J. P. Lehoczky, L. Sha, and J. K. Strosnider, "Enhanced aperiodic responsiveness in hard real-time environments," *IEEE RTSS*, pp. 261-270, 1987.

[3] M. Spuri and G. Buttazzo, "Scheduling aperiodic tasks in dynamic priority systems," *Real-Time Systems*, vol. 10, no. 2, pp. 179-210, 1996.

[4] C. L. Liu and J. W. Layland, "Scheduling algorithms for multiprogramming in a hard-real-time environment," *JACM*, vol. 20, no. 1, pp. 46-61, 1973.

---

*End of Presentation*
