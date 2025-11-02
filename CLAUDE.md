# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Real-Time Scheduling Simulator - An educational web application for analyzing and visualizing real-time task scheduling algorithms. Built with Python/Streamlit, implementing 13+ scheduling algorithms from CprE 458/558: Real-Time Systems course materials.

## Running the Application

### Start the Web UI
```bash
# From project root
streamlit run scheduler/app.py

# Or from scheduler directory
cd scheduler
streamlit run app.py
```

### Run Tests
```bash
# Test specific algorithms
python test_scheduler.py
python test_edf_hvdf_periodic_cli.py
python test_priority_policies.py

# Test visualizations
python test_visualizations.py
```

### Install Dependencies
```bash
pip install -r scheduler/requirements.txt
```

## Code Architecture

### Core Design Pattern: Template Method

The system uses an abstract base class (`SchedulerBase`) that implements the complete simulation loop, while concrete schedulers only implement two methods:

```python
class SchedulerBase(ABC):
    @abstractmethod
    def assign_priorities(self) -> None:
        """How to assign priorities to tasks"""

    @abstractmethod
    def get_next_task(self, ready_queue) -> Optional[TaskInstance]:
        """Which task to run next from ready queue"""

    def simulate(self) -> ScheduleResult:
        """Complete simulation loop (implemented in base)"""
```

**Key Point**: All schedulers share the same simulation engine in [scheduler/core/scheduler_base.py](scheduler/core/scheduler_base.py). Only priority assignment and task selection logic differ.

### Task Data Models

Six task types implemented in [scheduler/core/task.py](scheduler/core/task.py):

1. **PeriodicTask** - Repeating tasks with period/deadline/computation time
2. **AperiodicTask** - One-time tasks with arrival time and deadline
3. **ImpreciseTask** - Tasks with mandatory + optional computation time
4. **MkFirmTask** - Tasks with (m,k)-firm deadline constraints
5. **ResourceConstraint** - Resource sharing definitions
6. **PrecedenceConstraint** - Task dependency definitions

All task types have:
- `value` field for value-based scheduling (e.g., HVDF)
- `preemptive` flag for per-task preemption control
- `task_type` identifier for UI rendering

### Priority Policy Framework (NEW - Phase 1 Refactoring)

A composable strategy pattern for priority calculation in [scheduler/core/priority_policy.py](scheduler/core/priority_policy.py):

**Available Policies**:
- `RMSPolicy` - Period-based priority
- `EDFPolicy` - Deadline-based priority
- `DMSPolicy` - Deadline monotonic
- `LLFPolicy` - Laxity-based priority
- `HVDFPolicy` - Value density-based priority
- `FixedPriorityPolicy` - Manual priority assignment
- `CompositePriorityPolicy` - Combines primary + tie-breaker policies

**Usage Example**:
```python
from scheduler.core import EDFPolicy, HVDFPolicy, CompositePriorityPolicy

# EDF with HVDF tie-breaking
policy = CompositePriorityPolicy(
    EDFPolicy(),
    HVDFPolicy(task_values)
)
next_task = min(ready_queue, key=lambda t: policy.calculate_priority(t))
```

**Benefit**: Algorithm combinations (RMS+HVDF, EDF+HVDF, etc.) require only 10 lines instead of 200+ lines of duplicated code.

### Scheduler Organization

All schedulers live in [scheduler/core/algorithms/](scheduler/core/algorithms/):

**Basic Algorithms** (UI-integrated):
- [rms.py](scheduler/core/algorithms/rms.py) - Rate Monotonic Scheduling
- [edf.py](scheduler/core/algorithms/edf.py) - Earliest Deadline First
- [dms.py](scheduler/core/algorithms/dms.py) - Deadline Monotonic Scheduling
- [llf.py](scheduler/core/algorithms/llf.py) - Least Laxity First

**Server-Based** (UI-integrated):
- [combined.py](scheduler/core/algorithms/combined.py) - Polling, Deferrable, Sporadic servers

**Aperiodic Scheduling** (UI-integrated):
- [edf_hvdf.py](scheduler/core/algorithms/edf_hvdf.py) - EDF+HVDF for aperiodic tasks
- [edf_hvdf_periodic.py](scheduler/core/algorithms/edf_hvdf_periodic.py) - EDF+HVDF for periodic tasks

**Advanced** (code complete, UI pending):
- [precedence.py](scheduler/core/algorithms/precedence.py) - Precedence-constrained variants
- [overload.py](scheduler/core/algorithms/overload.py) - Overload handling algorithms
- [feedback_edf.py](scheduler/core/algorithms/feedback_edf.py) - Adaptive feedback control
- [feedback_mk_rms.py](scheduler/core/algorithms/feedback_mk_rms.py) - Dynamic (m,k)-firm control

### Visualization Layer

All visualizations in [scheduler/visualization/](scheduler/visualization/) work with `ScheduleResult` objects (completely decoupled from schedulers):

- [gantt.py](scheduler/visualization/gantt.py) - Interactive Plotly Gantt charts and priority timelines
- [metrics_dashboard.py](scheduler/visualization/metrics_dashboard.py) - CPU utilization, event distribution, service levels
- [precedence_graph.py](scheduler/visualization/precedence_graph.py) - Task dependency visualization
- [mk_history.py](scheduler/visualization/mk_history.py) - (m,k)-firm task history
- [timeline_interactive.py](scheduler/visualization/timeline_interactive.py) - Step-by-step timeline viewer

### Schedulability Analysis

Located in [scheduler/core/analysis/schedulability.py](scheduler/core/analysis/schedulability.py):

- RMS utilization test: n(2^(1/n) - 1) bound
- EDF utilization test: U ≤ 1.0 (necessary and sufficient)
- DMS utilization test: Deadline-based utilization
- Completion time test: Exact schedulability analysis
- Harmonic period detection: Identifies 100% utilization opportunities

### Preset Configurations

[scheduler/configs.py](scheduler/configs.py) contains 10 preset task sets from course exam questions and documentation examples. These are verified to match expected behavior.

## Development Patterns

### Adding a New Scheduling Algorithm

1. **Create scheduler class** in `scheduler/core/algorithms/`:
```python
from scheduler.core.scheduler_base import SchedulerBase

class MyScheduler(SchedulerBase):
    def assign_priorities(self):
        # Assign priorities to self.tasks
        pass

    def get_next_task(self, ready_queue):
        # Return highest priority task from ready_queue
        return max(ready_queue, key=lambda t: ...)
```

2. **Add to UI** in [scheduler/app.py](scheduler/app.py):
   - Import the scheduler class
   - Add to algorithm selection dropdown (around line 50-80)
   - Add to scheduler instantiation logic (around line 766+)
   - Note: There's a 80-line if/elif chain for scheduler selection (known technical debt, registry pattern planned for Phase 4 refactoring)

3. **Create test file** `test_my_scheduler.py` at project root

4. **Optional**: Add preset configuration in [scheduler/configs.py](scheduler/configs.py)

### Using Priority Policies (Preferred Approach)

Instead of creating a new scheduler, consider using `CompositePriorityPolicy`:

```python
from scheduler.core import RMSPolicy, HVDFPolicy, CompositePriorityPolicy

# RMS with HVDF tie-breaking (NEW combination, zero duplication)
policy = CompositePriorityPolicy(
    RMSPolicy(task_periods),
    HVDFPolicy(task_values)
)
```

This reduces code by 95% for algorithm combinations.

### Simulation Results Structure

Every scheduler returns a `ScheduleResult` object with:

```python
@dataclass
class ScheduleResult:
    timeline: List[ScheduleEvent]           # Complete execution trace
    deadline_misses: List[ScheduleEvent]    # All deadline violations
    cpu_utilization: float                  # Percentage (0-100)
    context_switches: int                   # Number of preemptions
```

Event types: `start`, `preempt`, `complete`, `deadline_miss`, `arrival`

### Three Base Scheduler Variants

**Important**: Three different base implementations exist:

1. [scheduler_base.py](scheduler/core/scheduler_base.py) - Main simplified version (use this)
2. [scheduler_base_v2.py](scheduler/core/scheduler_base_v2.py) - Alternative implementation (legacy)
3. [scheduler_with_resources.py](scheduler/core/scheduler_with_resources.py) - Resource-aware variant (for PIP/PCP)

**Always use** `scheduler_base.py` unless working on resource protocols.

## Architecture Status & Refactoring Plan

### Current Flexibility: 60/100 (After Phase 1)

**Completed**: Phase 1 - Priority policies extracted ([REFACTORING_PHASE1_COMPLETE.md](scheduler/REFACTORING_PHASE1_COMPLETE.md))

**Known Limitations**:
- Cannot mix periodic + aperiodic tasks in one simulation
- Scheduler selection uses 80-line if/elif chain (order-dependent bugs possible)
- Each scheduler only accepts one task type
- Resource protocols (PIP/PCP) implemented but not integrated into simulation

**Planned Refactoring** (see [ARCHITECTURE_ASSESSMENT.md](scheduler/ARCHITECTURE_ASSESSMENT.md)):
- Phase 2: Extract behavior mixins (ValueTracking, PreemptiveControl, ResourceManagement)
- Phase 3: Unified scheduler supporting mixed workloads
- Phase 4: Registry pattern for scheduler selection

### Immediate Opportunities

When adding new algorithm combinations:
1. **Prefer**: Using `CompositePriorityPolicy` (10 lines of code)
2. **Avoid**: Creating new monolithic scheduler classes (200+ lines, code duplication)

## Documentation

### Project Documentation
- [README.md](README.md) - Quick start guide
- [FINAL_STATUS.md](FINAL_STATUS.md) - Complete project status report
- [ARCHITECTURE_ASSESSMENT.md](scheduler/ARCHITECTURE_ASSESSMENT.md) - Hardwiring analysis and refactoring roadmap
- [REFACTORING_PHASE1_COMPLETE.md](scheduler/REFACTORING_PHASE1_COMPLETE.md) - Priority policy framework details

### Algorithm Documentation
The `_docs/` directory contains 17 comprehensive markdown files covering:
- Real-time systems fundamentals
- Scheduling algorithms (RMS, EDF, DMS, LLF)
- Resource protocols (PIP, PCP)
- Overload handling (imprecise computation, (m,k)-firm)
- Advanced topics (precedence constraints, network scheduling)
- FreeRTOS implementation tutorials

Implementation follows documentation examples exactly, and results are verified against expected behavior.

## Key Implementation Notes

### Scheduler Selection if/elif Chain

Located in [scheduler/app.py](scheduler/app.py) around line 766+:

**CAUTION**: Order matters! More specific patterns must come before general ones:
```python
# WRONG - "EDF" matches "EDF+HVDF"
if algorithm.startswith("EDF"):
    scheduler = EDFScheduler(...)
elif algorithm_category == "Aperiodic" and "EDF+HVDF" in algorithm:
    scheduler = EDFHVDFScheduler(...)  # Never reached!

# CORRECT - Specific first
if algorithm_category == "Aperiodic" and "EDF+HVDF" in algorithm:
    scheduler = EDFHVDFScheduler(...)
elif algorithm.startswith("EDF"):
    scheduler = EDFScheduler(...)
```

This is a known issue; registry pattern planned for Phase 4 refactoring.

### Value Tracking

Only `EDFHVDFScheduler` and `EDFHVDFPeriodicScheduler` currently track task values. To add value tracking to other schedulers:

```python
# Extract from EDFHVDFScheduler
def calculate_total_value(self) -> float:
    return sum(self.task_values.get(t.task_id, 0)
               for t in self.task_instances if t.completed)
```

Or use the new `HVDFPolicy` from the priority policy framework.

### Resource Protocols

Priority Inheritance (PIP) and Priority Ceiling (PCP) protocols are implemented in [scheduler/core/protocols/](scheduler/core/protocols/) but not yet integrated into the main simulation loop. They work with `scheduler_with_resources.py` base class.

To integrate: See critical section tracking in `SchedulerBase._check_critical_section_entry()` and resource management methods.

## Testing Approach

### Test File Convention
- Place test files at project root (not in `scheduler/`)
- Name pattern: `test_<feature>.py`
- Test files import from `scheduler` package using sys.path manipulation

### Verification Strategy
1. **Preset-based testing**: Use configurations from [scheduler/configs.py](scheduler/configs.py)
2. **Documentation matching**: Verify results match expected behavior from `_docs/`
3. **Visual inspection**: Run UI and check Gantt charts for correctness
4. **Automated tests**: Run individual test files to validate specific algorithms

### Example Test Structure
```python
from scheduler.core.algorithms.rms import RMSScheduler
from scheduler.core.task import PeriodicTask

# Define tasks from preset
tasks = [
    PeriodicTask(id="T1", computation_time=2, period=4, deadline=4),
    PeriodicTask(id="T2", computation_time=1, period=8, deadline=8)
]

# Run simulation
scheduler = RMSScheduler(tasks, duration=16)
result = scheduler.simulate()

# Verify results
assert result.deadline_misses == []
assert abs(result.cpu_utilization - 65.0) < 0.1
```

## Common Tasks

### Running Specific Algorithm
```python
from scheduler.core.algorithms.edf import EDFScheduler
from scheduler.core.task import PeriodicTask

tasks = [PeriodicTask(id="T1", computation_time=3, period=10, deadline=10)]
scheduler = EDFScheduler(tasks, duration=30)
result = scheduler.simulate()
print(f"CPU Utilization: {result.cpu_utilization}%")
print(f"Deadline Misses: {len(result.deadline_misses)}")
```

### Analyzing Schedulability
```python
from scheduler.core.analysis.schedulability import SchedulabilityAnalyzer

analyzer = SchedulabilityAnalyzer(tasks)
result = analyzer.analyze_rms()  # or analyze_edf(), analyze_dms()

print(f"Schedulable: {result['schedulable']}")
print(f"Utilization: {result['utilization']}")
print(f"Bound: {result['bound']}")
```

### Creating Visualizations
```python
from scheduler.visualization.gantt import create_gantt_chart
from scheduler.visualization.metrics_dashboard import create_metrics_dashboard

# After simulation
gantt_fig = create_gantt_chart(result, tasks)
metrics_fig = create_metrics_dashboard(result, simulation_duration)

# Display in Streamlit
st.plotly_chart(gantt_fig)
st.plotly_chart(metrics_fig)
```

## Technology Stack

- **Python 3.10+** (uses dataclasses, type hints extensively)
- **Streamlit** - Web UI framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation for UI tables
- **NumPy** - Numerical computations
- **Matplotlib** - Additional plotting

## Code Style Conventions

- Type hints on all function signatures
- Dataclasses for data models (immutable where possible)
- Abstract base classes for interfaces
- Docstrings on public methods
- Event-driven architecture for simulation results
- Separation of concerns: algorithms, analysis, visualization
