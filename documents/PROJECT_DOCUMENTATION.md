# Real-Time Scheduling Simulator - Complete Documentation

**Version:** 1.0
**Last Updated:** December 2024
**Author:** Shahab Afshar

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Installation & Setup](#2-installation--setup)
3. [Architecture](#3-architecture)
4. [Scheduling Algorithms](#4-scheduling-algorithms)
5. [Data Models](#5-data-models)
6. [Configuration & Presets](#6-configuration--presets)
7. [Visualization Components](#7-visualization-components)
8. [API Reference](#8-api-reference)
9. [Adding New Algorithms](#9-adding-new-algorithms)
10. [Testing](#10-testing)
11. [Troubleshooting](#11-troubleshooting)
12. [References](#12-references)

---

## 1. Project Overview

### 1.1 Purpose

The Real-Time Scheduling Simulator is an educational and analytical tool for exploring real-time task scheduling algorithms. It provides:

- **Interactive visualization** of schedule execution via Gantt charts
- **Schedulability analysis** with utilization tests (RMS, EDF, DMS)
- **Server-based scheduling** for mixed periodic-aperiodic workloads
- **Parameter exploration** to understand algorithm behavior

### 1.2 Supported Algorithms

| Category | Algorithms |
|----------|------------|
| Basic | RMS, EDF, DMS, LLF |
| Server-Based | Polling Server, Deferrable Server, Sporadic Server, Background Scheduler |
| Precedence | RMS with Precedence, EDF with Precedence |
| Overload | Dover, FC-EDF (Feedback Control) |
| Aperiodic | EDF+HVDF (Value-Based) |

### 1.3 Technology Stack

- **Python 3.10+** - Core simulation engine
- **Streamlit** - Web UI framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **NumPy** - Numerical computations

---

## 2. Installation & Setup

### 2.1 Prerequisites

```bash
# Python 3.10 or higher required
python --version
```

### 2.2 Installation

```bash
# Clone repository
git clone <repository-url>
cd Scheduler

# Install dependencies
pip install -r scheduler/requirements.txt
```

### 2.3 Running the Application

```bash
# From project root
streamlit run scheduler/app.py

# Or from scheduler directory
cd scheduler
streamlit run app.py
```

The application will open at `http://localhost:8501`

### 2.4 Dependencies

```
streamlit>=1.28.0
plotly>=5.18.0
pandas>=2.0.0
numpy>=1.24.0
```

---

## 3. Architecture

### 3.1 Directory Structure

```
Scheduler/
├── scheduler/
│   ├── app.py                      # Streamlit web UI (main entry point)
│   ├── configs.py                  # Preset configurations (21 presets)
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── task.py                 # Task data models (6 types)
│   │   ├── scheduler_base.py       # Abstract base class (Template Method)
│   │   ├── scheduler_base_v2.py    # Alternative implementation (legacy)
│   │   ├── scheduler_with_resources.py  # Resource-aware variant
│   │   ├── priority_policy.py      # Composable priority strategies
│   │   │
│   │   ├── algorithms/
│   │   │   ├── __init__.py
│   │   │   ├── rms.py              # Rate Monotonic Scheduling
│   │   │   ├── edf.py              # Earliest Deadline First
│   │   │   ├── dms.py              # Deadline Monotonic Scheduling
│   │   │   ├── llf.py              # Least Laxity First
│   │   │   ├── combined.py         # Server schedulers (Polling, Deferrable, Sporadic, Background)
│   │   │   ├── precedence.py       # Precedence-constrained variants
│   │   │   ├── overload.py         # Overload handling (Dover)
│   │   │   ├── edf_hvdf.py         # EDF+HVDF for aperiodic tasks
│   │   │   ├── edf_hvdf_periodic.py # EDF+HVDF for periodic tasks
│   │   │   ├── feedback_edf.py     # Adaptive feedback control
│   │   │   └── feedback_mk_rms.py  # Dynamic (m,k)-firm control
│   │   │
│   │   ├── analysis/
│   │   │   ├── __init__.py
│   │   │   └── schedulability.py   # Utilization tests
│   │   │
│   │   └── protocols/
│   │       ├── __init__.py
│   │       ├── pip.py              # Priority Inheritance Protocol
│   │       └── pcp.py              # Priority Ceiling Protocol
│   │
│   └── visualization/
│       ├── __init__.py
│       ├── gantt.py                # Gantt chart generation
│       ├── metrics_dashboard.py    # Performance metrics display
│       ├── precedence_graph.py     # Task dependency visualization
│       ├── mk_history.py           # (m,k)-firm history display
│       └── timeline_interactive.py # Step-by-step timeline viewer
│
├── documents/
│   ├── PROJECT_DOCUMENTATION.md    # This file
│   └── final/
│       ├── FINAL_REPORT.md         # Academic report
│       ├── figures/                # Report figures
│       ├── ieee-template.tex       # LaTeX template
│       └── header.tex              # LaTeX header
│
├── _docs/                          # Algorithm documentation (17 files)
│
├── test_*.py                       # Test files (at project root)
├── CLAUDE.md                       # AI assistant instructions
├── README.md                       # Quick start guide
└── FINAL_STATUS.md                 # Project status report
```

### 3.2 Design Patterns

#### 3.2.1 Template Method Pattern

The core architecture uses the Template Method pattern. `SchedulerBase` implements the complete simulation loop, while concrete schedulers only override specific methods:

```python
class SchedulerBase(ABC):
    def simulate(self) -> ScheduleResult:
        """Template method - complete simulation loop"""
        self.assign_priorities()
        for t in range(self.duration):
            self._handle_arrivals(t)
            self._handle_completions(t)
            task = self.get_next_task(self.ready_queue)
            # ... execute task ...
        return self._build_result()

    @abstractmethod
    def assign_priorities(self) -> None:
        """Hook: How to assign priorities"""
        pass

    @abstractmethod
    def get_next_task(self, ready_queue) -> Optional[TaskInstance]:
        """Hook: Which task to run next"""
        pass
```

#### 3.2.2 Strategy Pattern (Priority Policies)

Composable priority calculation using the Strategy pattern:

```python
from scheduler.core.priority_policy import (
    RMSPolicy, EDFPolicy, HVDFPolicy, CompositePriorityPolicy
)

# EDF with HVDF tie-breaking
policy = CompositePriorityPolicy(
    primary=EDFPolicy(),
    tiebreaker=HVDFPolicy(task_values)
)

# Use in scheduler
next_task = min(ready_queue, key=lambda t: policy.calculate_priority(t))
```

### 3.3 Data Flow

```
User Input (UI)
    ↓
Task Configuration (task.py models)
    ↓
Scheduler Selection (app.py)
    ↓
Simulation (scheduler_base.py)
    ↓
ScheduleResult (timeline, metrics)
    ↓
Visualization (gantt.py, metrics_dashboard.py)
    ↓
Display (Streamlit UI)
```

---

## 4. Scheduling Algorithms

### 4.1 Rate Monotonic Scheduling (RMS)

**File:** `scheduler/core/algorithms/rms.py`

**Priority Assignment:** Static, based on period (shorter period = higher priority)

**Schedulability Test:**
$$U = \sum_{i=1}^{n} \frac{C_i}{P_i} \leq n(2^{1/n} - 1)$$

**Usage:**
```python
from scheduler.core.algorithms.rms import RMSScheduler
from scheduler.core.task import PeriodicTask

tasks = [
    PeriodicTask(id="T1", computation_time=2, period=4, deadline=4),
    PeriodicTask(id="T2", computation_time=1, period=8, deadline=8)
]

scheduler = RMSScheduler(tasks, duration=16)
result = scheduler.simulate()
```

### 4.2 Earliest Deadline First (EDF)

**File:** `scheduler/core/algorithms/edf.py`

**Priority Assignment:** Dynamic, based on absolute deadline (earliest deadline = highest priority)

**Schedulability Test:**
$$U = \sum_{i=1}^{n} \frac{C_i}{P_i} \leq 1.0$$

**Usage:**
```python
from scheduler.core.algorithms.edf import EDFScheduler

scheduler = EDFScheduler(tasks, duration=16)
result = scheduler.simulate()
```

### 4.3 Deadline Monotonic Scheduling (DMS)

**File:** `scheduler/core/algorithms/dms.py`

**Priority Assignment:** Static, based on relative deadline (shorter deadline = higher priority)

**Use Case:** When D < P (deadline less than period)

### 4.4 Least Laxity First (LLF)

**File:** `scheduler/core/algorithms/llf.py`

**Priority Assignment:** Dynamic, based on laxity (slack time)

**Laxity Formula:**
$$L_i(t) = D_i - t - C_i^{remaining}$$

**Characteristics:**
- Optimal for uniprocessor (like EDF)
- Higher context switch overhead due to laxity ties

### 4.5 Server-Based Schedulers

**File:** `scheduler/core/algorithms/combined.py`

All server schedulers inherit from `ServerSchedulerBase` and implement:

```python
def _handle_replenishment(self, t: int) -> None:
    """When/how to replenish server capacity"""

def _execute_server_slot(self, t: int) -> bool:
    """What to do when server has highest priority"""
```

#### 4.5.1 Polling Server

```python
from scheduler.core.algorithms.combined import PollingServerScheduler

scheduler = PollingServerScheduler(
    periodic_tasks=periodic,
    aperiodic_tasks=aperiodic,
    server_capacity=2.0,
    server_period=5.0,
    duration=50
)
```

**Behavior:** Capacity lost if no aperiodic tasks pending at server activation

#### 4.5.2 Deferrable Server

```python
from scheduler.core.algorithms.combined import DeferrableServerScheduler
```

**Behavior:** Capacity preserved until period end; can serve aperiodic tasks anytime within period

#### 4.5.3 Sporadic Server

```python
from scheduler.core.algorithms.combined import SporadicServerScheduler
```

**Behavior:** Capacity consumed at time t is replenished at time t + Pₛ

#### 4.5.4 Background Scheduler

```python
from scheduler.core.algorithms.combined import BackgroundScheduler
```

**Behavior:** Aperiodic tasks run only during CPU idle time (no server concept)

### 4.6 EDF+HVDF (Value-Based)

**File:** `scheduler/core/algorithms/edf_hvdf.py`

**Priority:** Combines deadline and value density (V/C)

**Use Case:** Aperiodic tasks with different importance values

```python
from scheduler.core.algorithms.edf_hvdf import EDFHVDFScheduler

tasks = [
    AperiodicTask(id="T1", arrival_time=0, computation_time=3, deadline=8, value=3),
    AperiodicTask(id="T2", arrival_time=0, computation_time=1, deadline=4, value=1),
]

scheduler = EDFHVDFScheduler(tasks, duration=20)
result = scheduler.simulate()
print(f"Total Value: {scheduler.calculate_total_value()}")
```

---

## 5. Data Models

**File:** `scheduler/core/task.py`

### 5.1 PeriodicTask

```python
@dataclass
class PeriodicTask:
    id: str
    computation_time: float
    period: float
    deadline: float          # Usually equals period
    priority: int = 0        # Assigned by scheduler
    value: float = 1.0       # For value-based scheduling
    preemptive: bool = True  # Per-task preemption control
    task_type: str = "periodic"
```

### 5.2 AperiodicTask

```python
@dataclass
class AperiodicTask:
    id: str
    arrival_time: float
    computation_time: float
    deadline: float
    value: float = 1.0
    preemptive: bool = True
    task_type: str = "aperiodic"
```

### 5.3 ImpreciseTask

```python
@dataclass
class ImpreciseTask:
    id: str
    mandatory_time: float    # Must complete
    optional_time: float     # Can be skipped under overload
    period: float
    deadline: float
```

### 5.4 MkFirmTask

```python
@dataclass
class MkFirmTask:
    id: str
    computation_time: float
    period: float
    m: int                   # Required completions
    k: int                   # Window size
    # Must meet m out of k deadlines
```

### 5.5 ScheduleResult

```python
@dataclass
class ScheduleResult:
    timeline: List[ScheduleEvent]      # Complete execution trace
    deadline_misses: List[ScheduleEvent]
    cpu_utilization: float             # Percentage (0-100)
    context_switches: int
```

### 5.6 ScheduleEvent

```python
@dataclass
class ScheduleEvent:
    time: int
    task_id: str
    event_type: str  # 'start', 'complete', 'preempt', 'deadline_miss', 'arrival'
    details: dict    # Additional info (remaining_time, deadline, etc.)
```

---

## 6. Configuration & Presets

**File:** `scheduler/configs.py`

### 6.1 Preset Structure

```python
PRESET_CONFIGS = {
    "preset_key": {
        "name": "Display Name",
        "category": "Category Name",
        "algorithm": "Algorithm Name",
        "tasks": [...],  # List of task objects or dict with periodic/aperiodic
        "description": "What this preset demonstrates",
        "config": {      # Optional algorithm-specific config
            "server_capacity": 2.0,
            "server_period": 5.0
        }
    }
}
```

### 6.2 Available Presets (21 total)

| Category | Presets |
|----------|---------|
| Basic | RMS Example, EDF Example, DMS Example, LLF Examples (2) |
| Server-Based | Polling, Deferrable, Sporadic, Background, Server Capacity Demo |
| Precedence | Chain Dependencies, Fork-Join Dependencies |
| Overload | Deadline Miss Scenario, Gradual Overload |
| Aperiodic | Value Maximization, Staggered Arrivals, Burst Arrivals |

### 6.3 Adding Custom Presets

```python
# In configs.py

MY_CUSTOM_TASKS = [
    PeriodicTask(id="T1", computation_time=1, period=5, deadline=5),
    PeriodicTask(id="T2", computation_time=2, period=10, deadline=10),
]

# Add to PRESET_CONFIGS dict
PRESET_CONFIGS["my_custom"] = {
    "name": "My Custom Preset",
    "category": "Basic",
    "algorithm": "RMS",
    "tasks": MY_CUSTOM_TASKS,
    "description": "Custom test scenario"
}
```

---

## 7. Visualization Components

### 7.1 Gantt Chart

**File:** `scheduler/visualization/gantt.py`

```python
from scheduler.visualization.gantt import create_gantt_chart

fig = create_gantt_chart(
    result=schedule_result,
    tasks=task_list,
    show_deadlines=True,
    show_arrivals=True
)

# In Streamlit
st.plotly_chart(fig)
```

**Features:**
- Color-coded task bars
- Deadline markers (red triangles)
- Arrival markers (green circles)
- Hover details (task info, time, event type)
- Zoom/pan support

### 7.2 Metrics Dashboard

**File:** `scheduler/visualization/metrics_dashboard.py`

```python
from scheduler.visualization.metrics_dashboard import create_metrics_dashboard

fig = create_metrics_dashboard(
    result=schedule_result,
    duration=simulation_duration
)
```

**Displays:**
- CPU utilization gauge
- Context switch count
- Deadline miss count
- Event distribution pie chart

### 7.3 Priority Timeline

**File:** `scheduler/visualization/gantt.py`

```python
from scheduler.visualization.gantt import create_priority_timeline

fig = create_priority_timeline(result, tasks)
```

**Shows:** How task priorities change over time (useful for EDF/LLF)

---

## 8. API Reference

### 8.1 SchedulerBase Methods

```python
class SchedulerBase(ABC):
    def __init__(self, tasks: List, duration: int):
        """Initialize scheduler with tasks and simulation duration"""

    def simulate(self) -> ScheduleResult:
        """Run simulation and return results"""

    @abstractmethod
    def assign_priorities(self) -> None:
        """Assign priorities to tasks (called once before simulation)"""

    @abstractmethod
    def get_next_task(self, ready_queue: List) -> Optional[TaskInstance]:
        """Select next task to execute from ready queue"""
```

### 8.2 SchedulabilityAnalyzer

**File:** `scheduler/core/analysis/schedulability.py`

```python
from scheduler.core.analysis.schedulability import SchedulabilityAnalyzer

analyzer = SchedulabilityAnalyzer(tasks)

# RMS test
rms_result = analyzer.analyze_rms()
# Returns: {'schedulable': bool, 'utilization': float, 'bound': float}

# EDF test
edf_result = analyzer.analyze_edf()
# Returns: {'schedulable': bool, 'utilization': float}

# DMS test
dms_result = analyzer.analyze_dms()

# Check harmonic periods
is_harmonic = analyzer.check_harmonic_periods()
```

### 8.3 Priority Policies

**File:** `scheduler/core/priority_policy.py`

```python
from scheduler.core.priority_policy import (
    RMSPolicy,
    EDFPolicy,
    DMSPolicy,
    LLFPolicy,
    HVDFPolicy,
    FixedPriorityPolicy,
    CompositePriorityPolicy
)

# Create policy
policy = EDFPolicy()

# Calculate priority for a task instance
priority = policy.calculate_priority(task_instance, current_time)

# Composite policy (primary + tiebreaker)
composite = CompositePriorityPolicy(
    primary=EDFPolicy(),
    tiebreaker=HVDFPolicy(task_values)
)
```

---

## 9. Adding New Algorithms

### 9.1 Basic Algorithm Template

```python
# scheduler/core/algorithms/my_algorithm.py

from scheduler.core.scheduler_base import SchedulerBase
from scheduler.core.task import PeriodicTask
from typing import List, Optional

class MyScheduler(SchedulerBase):
    """My custom scheduling algorithm."""

    def __init__(self, tasks: List[PeriodicTask], duration: int):
        super().__init__(tasks, duration)
        # Additional initialization

    def assign_priorities(self) -> None:
        """Assign priorities to all tasks."""
        for i, task in enumerate(self.tasks):
            task.priority = self._calculate_priority(task)

    def get_next_task(self, ready_queue) -> Optional:
        """Select highest priority task from ready queue."""
        if not ready_queue:
            return None
        return max(ready_queue, key=lambda t: t.priority)

    def _calculate_priority(self, task) -> int:
        """Custom priority calculation logic."""
        # Implement your algorithm here
        return 0
```

### 9.2 Server Algorithm Template

```python
from scheduler.core.algorithms.combined import ServerSchedulerBase

class MyServerScheduler(ServerSchedulerBase):
    """My custom server algorithm."""

    def _handle_replenishment(self, t: int) -> None:
        """Handle server capacity replenishment."""
        if t % self.server_period == 0:
            self.server_remaining = self.server_capacity

    def _execute_server_slot(self, t: int) -> bool:
        """Execute one time unit of server work."""
        if self.aperiodic_queue and self.server_remaining > 0:
            # Serve aperiodic task
            self.server_remaining -= 1
            return True
        else:
            # Custom behavior when no work
            return False
```

### 9.3 Registering in UI

Add to `scheduler/app.py`:

```python
# Import
from scheduler.core.algorithms.my_algorithm import MyScheduler

# Add to algorithm dropdown (around line 50-80)
algorithms = {
    ...
    "My Algorithm": "my_algorithm",
}

# Add to scheduler instantiation (around line 766+)
if algorithm == "My Algorithm":
    scheduler = MyScheduler(tasks, duration)
```

---

## 10. Testing

### 10.1 Test File Location

All test files are at the project root:

```
Scheduler/
├── test_scheduler.py
├── test_edf_hvdf_periodic_cli.py
├── test_priority_policies.py
├── test_visualizations.py
└── ...
```

### 10.2 Running Tests

```bash
# Run specific test
python test_scheduler.py

# Run with verbose output
python -v test_scheduler.py
```

### 10.3 Writing Tests

```python
# test_my_algorithm.py

import sys
sys.path.insert(0, 'scheduler')

from core.algorithms.my_algorithm import MyScheduler
from core.task import PeriodicTask

def test_basic_scheduling():
    tasks = [
        PeriodicTask(id="T1", computation_time=2, period=4, deadline=4),
        PeriodicTask(id="T2", computation_time=1, period=8, deadline=8)
    ]

    scheduler = MyScheduler(tasks, duration=16)
    result = scheduler.simulate()

    assert len(result.deadline_misses) == 0, "Expected no deadline misses"
    assert result.cpu_utilization > 0, "Expected non-zero utilization"
    print("Test passed!")

if __name__ == "__main__":
    test_basic_scheduling()
```

---

## 11. Troubleshooting

### 11.1 Common Issues

#### Import Errors

```
ModuleNotFoundError: No module named 'scheduler'
```

**Solution:** Run from project root or add to Python path:
```python
import sys
sys.path.insert(0, 'path/to/Scheduler')
```

#### Streamlit Port in Use

```
Address already in use
```

**Solution:** Kill existing process or use different port:
```bash
streamlit run scheduler/app.py --server.port 8502
```

#### Missing Dependencies

```
ImportError: No module named 'plotly'
```

**Solution:** Install requirements:
```bash
pip install -r scheduler/requirements.txt
```

### 11.2 Performance Issues

**Slow Simulation:**
- Reduce simulation duration
- Use fewer tasks
- Check for infinite loops in custom algorithms

**Memory Issues:**
- Large timelines can consume memory
- Limit duration for very long simulations

### 11.3 Visualization Issues

**Gantt Chart Not Showing:**
- Check if ScheduleResult has events
- Verify Plotly is installed correctly
- Try refreshing the Streamlit app

**Wrong Colors:**
- Task colors are auto-assigned based on task_id
- Customize in `gantt.py` if needed

---

## 12. References

### 12.1 Academic References

1. B. Sprunt, L. Sha, and J. Lehoczky, "Aperiodic task scheduling for hard-real-time systems," *Real-Time Systems*, vol. 1, no. 1, pp. 27-60, 1989.

2. J. P. Lehoczky, L. Sha, and J. K. Strosnider, "Enhanced aperiodic responsiveness in hard real-time environments," *IEEE Real-Time Systems Symposium*, pp. 261-270, 1987.

3. M. Spuri and G. Buttazzo, "Scheduling aperiodic tasks in dynamic priority systems," *Real-Time Systems*, vol. 10, no. 2, pp. 179-210, 1996.

4. C. L. Liu and J. W. Layland, "Scheduling algorithms for multiprogramming in a hard-real-time environment," *Journal of the ACM*, vol. 20, no. 1, pp. 46-61, 1973.

5. L. Sha, R. Rajkumar, and J. P. Lehoczky, "Priority inheritance protocols: An approach to real-time synchronization," *IEEE Transactions on Computers*, vol. 39, no. 9, pp. 1175-1185, 1990.

### 12.2 Project Documentation

- `_docs/` folder contains 17 comprehensive markdown files covering all algorithms
- `CLAUDE.md` provides AI assistant instructions for code navigation
- `FINAL_STATUS.md` documents project completion status

### 12.3 External Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Real-Time Systems Course Materials](https://www.ece.iastate.edu/) (CprE 458/558)

---

## Appendix A: Quick Reference

### A.1 Common Commands

```bash
# Start application
streamlit run scheduler/app.py

# Run tests
python test_scheduler.py

# Generate documentation PDF
pandoc documents/final/FINAL_REPORT.md -o FINAL_REPORT.pdf

# Install dependencies
pip install -r scheduler/requirements.txt
```

### A.2 Key Files

| Purpose | File |
|---------|------|
| Main UI | `scheduler/app.py` |
| Task models | `scheduler/core/task.py` |
| Base scheduler | `scheduler/core/scheduler_base.py` |
| Server algorithms | `scheduler/core/algorithms/combined.py` |
| Presets | `scheduler/configs.py` |
| Gantt chart | `scheduler/visualization/gantt.py` |

### A.3 Algorithm Selection Guide

| Scenario | Recommended Algorithm |
|----------|----------------------|
| Simple periodic tasks | RMS |
| D < P (constrained deadlines) | DMS |
| High utilization needed | EDF |
| Need laxity visibility | LLF |
| Mixed periodic + aperiodic | Polling/Deferrable/Sporadic Server |
| Best aperiodic response | Sporadic Server |
| Minimal complexity | Background Scheduler |
| Value-based scheduling | EDF+HVDF |

---

*End of Documentation*
