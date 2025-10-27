# Real-Time Scheduling Simulator

A comprehensive, easy-to-debug Python + Streamlit application for visualizing and analyzing real-time task scheduling algorithms.

## Project Status

### Completed Components ✅

1. **Project Structure** - All directories and module structure in place
2. **Task Data Models** (`core/task.py`) - Complete task types:
   - PeriodicTask
   - AperiodicTask
   - ImpreciseTask
   - MkFirmTask
   - ResourceConstraint
   - PrecedenceConstraint
   - TaskInstance
   - ScheduleEvent
   - ScheduleResult

3. **Base Scheduler Class** (`core/scheduler_base.py`) - Core simulation loop with:
   - Instance creation and management
   - Ready queue updates
   - Time unit processing
   - Event generation
   - Result analysis

4. **Basic Algorithms**:
   - **RMS** (`algorithms/rms.py`) - Rate Monotonic Scheduling
   - **EDF** (`algorithms/edf.py`) - Earliest Deadline First
   - **DMS** (`algorithms/dms.py`) - Deadline Monotonic Scheduling

5. **Schedulability Analysis** (`analysis/schedulability.py`):
   - RMS utilization test
   - EDF utilization test
   - DMS utilization test
   - Completion time test (exact analysis)
   - Harmonic task set check
   - Comprehensive RMS analysis

6. **Basic Streamlit UI** (`app.py`) - Interactive web interface with:
   - Task input and editing
   - Algorithm selection
   - Schedulability analysis display
   - Simulation execution
   - Timeline visualization

7. **Dependencies** (`requirements.txt`)

### In Progress 🚧

- Visualization components (Gantt charts, metrics dashboard)
- Advanced algorithms (LLF, Combined scheduling, Precedence)
- Resource protocols (PIP, PCP)
- Overload handling algorithms

### Not Started 📋

- Advanced visualization with Plotly
- Step-by-step timeline viewer
- Export functionality
- Documentation examples
- Comprehensive testing

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r scheduler/requirements.txt
   ```

2. **Test basic functionality:**
   ```bash
   python test_scheduler.py
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run scheduler/app.py
   ```

## Architecture

The simulator follows a modular architecture:

```
scheduler/
├── core/                 # Core scheduling logic
│   ├── task.py          # Data models
│   ├── scheduler_base.py # Base scheduler class
│   ├── algorithms/       # Scheduling algorithms
│   ├── analysis/         # Schedulability tests
│   └── protocols/        # Resource access protocols
├── visualization/        # Visualization components
├── utils/               # Utility functions
└── app.py              # Streamlit UI
```

## Key Features

- **Easy to Debug**: Pure Python with clear data structures
- **Comprehensive**: Covers all major scheduling algorithms
- **Interactive**: Streamlit web interface for experimentation
- **Educational**: Clear visualization of scheduling decisions
- **Extensible**: Modular design for adding new algorithms

## Next Steps

1. Implement LLF algorithm
2. Add Gantt chart visualization with Plotly
3. Implement combined scheduling (servers)
4. Add precedence-constrained scheduling
5. Implement resource protocols
6. Add overload handling algorithms
7. Create comprehensive test suite
8. Add export functionality

