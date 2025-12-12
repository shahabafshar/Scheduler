# Real-Time Scheduling Simulator - Comprehensive User Guide

**Version:** 1.0  
**Last Updated:** December 2024  
**Author:** Shahab Afshar

---

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Basic Algorithms](#2-basic-algorithms)
3. [Server-Based Algorithms](#3-server-based-algorithms)
4. [Precedence-Constrained Algorithms](#4-precedence-constrained-algorithms)
5. [Aperiodic Scheduling](#5-aperiodic-scheduling)
6. [Overload Handling](#6-overload-handling)
7. [Advanced Features](#7-advanced-features)
8. [Presets System](#8-presets-system)
9. [Visualizations](#9-visualizations)
10. [Analysis Features](#10-analysis-features)
11. [Export Functionality](#11-export-functionality)
12. [Configuration Options](#12-configuration-options)
13. [Error Handling & Edge Cases](#13-error-handling--edge-cases)
14. [Complete Workflow Examples](#14-complete-workflow-examples)
15. [Algorithm Comparison](#15-algorithm-comparison)

---

## 1. Getting Started

### 1.1 Running the Application

The Real-Time Scheduling Simulator is a Streamlit web application. To start it:

```bash
# From project root
streamlit run scheduler/app.py

# Or from scheduler directory
cd scheduler
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

**Screenshot:** `screenshots/part1-getting-started/01-initial-state.png`

### 1.2 Interface Overview

The application has a clean, two-panel layout:

- **Left Panel (Configuration):** Algorithm selection, task configuration, and advanced options
- **Right Panel (Results):** Visualizations, metrics, analysis, and export options

**Screenshots:**
- `screenshots/part1-getting-started/02-full-layout.png` - Complete application layout
- `screenshots/part1-getting-started/03-header-section.png` - Header with Presets and Run buttons
- `screenshots/part1-getting-started/04-configuration-panel.png` - Left configuration panel
- `screenshots/part1-getting-started/05-results-panel-empty.png` - Empty results panel

---

## 2. Basic Algorithms

The simulator supports four fundamental scheduling algorithms for periodic tasks.

### 2.1 RMS (Rate Monotonic Scheduling)

**Algorithm Type:** Fixed Priority  
**Priority Assignment:** Based on period (shorter period = higher priority)  
**Schedulability Test:** U ≤ n(2^(1/n) - 1)

#### Workflow

1. **Select Algorithm:**
   - Category: "Basic Algorithms"
   - Algorithm: "RMS (Rate Monotonic)"
   
   **Screenshot:** `screenshots/part2-basic-algorithms/part2-rms-01-algorithm-selection.png`

2. **Configure Tasks:**
   - Use the task grid to define periodic tasks
   - Example: T1 (C=2, P=4, D=4), T2 (C=1, P=8, D=8)
   
   **Screenshot:** `screenshots/part2-basic-algorithms/part2-rms-02-task-configuration.png`

3. **Set Duration:**
   - Use the slider to set simulation duration (default: 50)

4. **Run Simulation:**
   - Click the "Run" button
   - Results appear in the right panel

5. **View Results:**
   - **Key Metrics:** CPU utilization, deadline misses, context switches
   - **Gantt Chart:** Visual timeline of task execution
   - **Metrics Dashboard:** CPU utilization over time, utilization by task
   - **Timeline Viewer:** Step-by-step event viewer
   - **Analysis:** Schedulability analysis and task statistics
   - **Export:** Download timeline events as CSV

**Screenshots:**
- `screenshots/part2-basic-algorithms/part2-rms-03-results-metrics.png` - Key metrics and success message
- `screenshots/part2-basic-algorithms/part2-rms-04-gantt-chart.png` - Gantt chart visualization
- `screenshots/part2-basic-algorithms/part2-rms-05-metrics-dashboard.png` - Metrics dashboard
- `screenshots/part2-basic-algorithms/part2-rms-06-timeline-viewer.png` - Timeline step viewer
- `screenshots/part2-basic-algorithms/part2-rms-07-analysis-tab.png` - Schedulability analysis
- `screenshots/part2-basic-algorithms/part2-rms-08-export-tab.png` - Export functionality

#### Example Results

For the example task set (T1: C=2, P=4; T2: C=1, P=8):
- **CPU Utilization:** 62.5%
- **Deadline Misses:** 0
- **Context Switches:** 19
- **Schedulable:** Yes (within RMS bound)

### 2.2 EDF (Earliest Deadline First)

**Algorithm Type:** Dynamic Priority  
**Priority Assignment:** Based on absolute deadline (earliest deadline = highest priority)  
**Schedulability Test:** U ≤ 1.0 (100% utilization possible)

#### Key Features

EDF provides the unique **Priority Timeline** visualization showing how task priorities change dynamically over time.

**Screenshots:**
- `screenshots/part2-basic-algorithms/part2-edf-01-algorithm-selection.png` - Algorithm selection
- `screenshots/part2-basic-algorithms/part2-edf-02-task-configuration.png` - Task configuration
- `screenshots/part2-basic-algorithms/part2-edf-03-gantt-chart.png` - Gantt chart
- `screenshots/part2-basic-algorithms/part2-edf-04-priority-timeline.png` - **Priority Timeline (EDF-specific)**
- `screenshots/part2-basic-algorithms/part2-edf-05-analysis.png` - EDF analysis (100% bound)

#### Example: Full Utilization

EDF can achieve 100% CPU utilization while still meeting all deadlines, unlike RMS which has a lower bound.

### 2.3 DMS (Deadline Monotonic Scheduling)

**Algorithm Type:** Fixed Priority  
**Priority Assignment:** Based on relative deadline (shorter deadline = higher priority)  
**Use Case:** When D < P (deadline less than period)

Similar workflow to RMS, but priorities are based on deadlines rather than periods.

### 2.4 LLF (Least Laxity First)

**Algorithm Type:** Dynamic Priority  
**Priority Assignment:** Based on laxity (slack time remaining)  
**Laxity Formula:** L(t) = D - t - C_remaining

LLF also provides a Priority Timeline visualization showing laxity changes over time.

---

## 3. Server-Based Algorithms

Server-based schedulers handle mixed workloads: periodic background tasks and aperiodic foreground tasks.

### 3.1 Polling Server

**Behavior:** Server capacity is lost if no aperiodic tasks are pending when the server activates.

**Configuration:**
- Server Capacity (Cs): Amount of computation time available per period
- Server Period (Ps): Replenishment period

**Screenshots needed:**
- Server configuration inputs
- Task grid showing periodic + aperiodic tasks
- Gantt chart showing server behavior
- Server Analysis section

### 3.2 Deferrable Server

**Behavior:** Capacity is preserved until period end; can serve aperiodic tasks anytime within period.

### 3.3 Sporadic Server

**Behavior:** Best response time for aperiodic tasks. Capacity consumed at time t is replenished at time t + Ps.

### 3.4 Background Scheduler

**Behavior:** Aperiodic tasks execute only during CPU idle time (no server concept).

---

## 4. Precedence-Constrained Algorithms

These algorithms enforce task dependencies (precedence constraints).

### 4.1 RMS with Precedence

**Workflow:**
1. Select "Precedence-Constrained" category
2. Select "RMS with Precedence" algorithm
3. Open "Advanced Options" → "Precedence" tab
4. Enable precedence and define constraints (e.g., "T1 -> T2")
5. Run simulation

**Screenshots needed:**
- Advanced Options expander
- Precedence tab with constraint definition
- Precedence Graph visualization
- Gantt chart showing dependency enforcement

### 4.2 EDF with Precedence

Similar to RMS with Precedence, but uses EDF priority assignment.

### 4.3 DMS with Precedence

Similar to RMS with Precedence, but uses DMS priority assignment.

---

## 5. Aperiodic Scheduling

Value-based scheduling for aperiodic tasks.

### 5.1 EDF+HVDF (Value-Based)

**Priority:** Combines deadline (EDF) and value density (HVDF)

**Configuration:**
- Task grid shows "Value" column
- Tasks have different values (V=3, V=1, V=2, etc.)

**Screenshots needed:**
- Task grid with Value column
- Value Analysis section
- Value breakdown table
- Gantt chart showing value-based scheduling

### 5.2 HVDF Only

Pure value-based scheduling without deadline consideration.

---

## 6. Overload Handling

Algorithms for handling overload scenarios (U > 100%).

### 6.1 FC-EDF (Feedback Control)

**Configuration:**
- Advanced Options → Overload tab
- Target Miss Ratio
- PID parameters (Kp, Ki, Kd)

**Screenshots needed:**
- Overload tab with PID parameters
- Service Level Plot
- Deadline miss handling

### 6.2 Feedback (m,k)-RMS

**Configuration:**
- Target DFR (Deadline Failure Rate)
- PID parameters
- Task grid with (m,k) values

**Screenshots needed:**
- (m,k) History Chart
- Task grid with (m,k) column

### 6.3 Imprecise Computation

**Configuration:**
- Task grid with Mandatory Time and Optional Time columns

**Screenshots needed:**
- Task grid showing mandatory/optional columns
- Gantt chart showing imprecise execution

### 6.4 HVDF (Value-Based) - Overload

Value-based scheduling under overload conditions.

### 6.5 (m,k)-Firm Tasks

Tasks that must meet m out of k deadlines.

---

## 7. Advanced Features

### 7.1 Resource Sharing

**Protocols:**
- Priority Inheritance Protocol (PIP)
- Priority Ceiling Protocol (PCP)

**Configuration:**
- Advanced Options → Resources tab
- Enable Resource Sharing
- Define resources (R1, R2, etc.)
- Assign resources to tasks with critical section durations

**Screenshots needed:**
- Resources tab
- Task grid with Resources and CS columns
- Gantt chart showing blocked intervals (hatched pattern)
- Resource labels on blocked sections

### 7.2 Precedence Constraints

Detailed precedence constraint patterns:
- Chain: T1 -> T2 -> T3
- Fork: T1 -> T2, T1 -> T3
- Diamond: T1 -> {T2,T3} -> T4

**Screenshots needed:**
- Precedence Graph for each pattern
- Gantt chart showing constraint enforcement

---

## 8. Presets System

The application includes 21 preset configurations organized by category.

### 8.1 Preset Dialog

Click the "Presets" button to open the preset dialog.

**Screenshot:** `screenshots/part8-presets/part8-01-preset-dialog.png`

**Categories:**
- Basic Algorithms (10 presets)
- Server-Based (Combined) (6 presets)
- Precedence-Constrained (3 presets)
- Overload Handling (2 presets)
- Aperiodic Scheduling (3 presets)

### 8.2 Loading a Preset

1. Click "Presets" button
2. Select category tab
3. Click "Load" on desired preset
4. Tasks and algorithm are automatically configured
5. Simulation runs automatically

---

## 9. Visualizations

### 9.1 Gantt Chart

Interactive timeline showing:
- Task execution intervals
- Deadline markers (red triangles)
- Arrival markers (green circles)
- Blocked intervals (hatched pattern, when resources enabled)
- Resource labels (when resources enabled)

**Features:**
- Zoom and pan
- Hover tooltips with event details
- Download as PNG

### 9.2 Metrics Dashboard

Four charts:
1. CPU Utilization Over Time
2. Utilization by Task (pie chart)
3. Event Distribution
4. Context Switches visualization

### 9.3 Priority Timeline

**Available for:** EDF, LLF, DMS

Shows how task priorities change dynamically over time.

### 9.4 Precedence Graph

Network diagram showing task dependencies as directed edges.

### 9.5 Timeline Step Viewer

Interactive step-by-step viewer with:
- Slider to navigate through events
- Explanation text for each step
- Visual timeline at current step

### 9.6 (m,k) History Chart

Visualization of (m,k)-firm task compliance over time.

### 9.7 Service Level Plot

Service level over time for feedback control algorithms.

---

## 10. Analysis Features

### 10.1 Schedulability Analysis

**RMS Analysis:**
- Utilization calculation
- RMS bound (n(2^(1/n) - 1))
- Harmonic period detection
- Schedulable status

**EDF Analysis:**
- Utilization calculation
- EDF bound (100%)
- Schedulable status

**DMS Analysis:**
- Utilization calculation
- DMS bound
- Schedulable status

### 10.2 Task Statistics

Table showing:
- Task ID
- Computation Time (C)
- Period (P)
- Deadline (D)
- Utilization (U)
- Priority

### 10.3 Value Analysis

**Available for:** HVDF algorithms

- Total Value metric
- Value breakdown table showing:
  - Task instance
  - Completion time
  - Deadline
  - Status (Met/Missed)
  - Value earned

### 10.4 Server Analysis

**Available for:** Server-based algorithms

- Aperiodic Tasks Completed metric
- Response Times table

---

## 11. Export Functionality

### 11.1 Timeline Export

**Location:** Export tab

- Timeline Events table (first 200 events)
- "Download Timeline (CSV)" button
- CSV includes: Time, Task, Event, Details

### 11.2 Chart Export

All Plotly charts include a camera icon in the toolbar:
- Click camera icon
- PNG image downloads automatically

---

## 12. Configuration Options

### 12.1 Duration Configuration

- **Slider Range:** 10 to 200 time units
- **Default:** 50
- **Step:** 10

### 12.2 Server Configuration

**Available for:** Server-Based algorithms

- **Server Capacity (Cs):** 0.1 to 20.0 (step: 0.5)
- **Server Period (Ps):** 1.0 to 50.0 (step: 1.0)

### 12.3 Overload Configuration

**FC-EDF:**
- Target Miss Ratio: 0.01 to 1.0
- Kp, Ki, Kd: 0.0 to 1.0

**Feedback (m,k)-RMS:**
- Target DFR: 0.01 to 1.0
- Kp, Ki, Kd: 0.0 to 1.0

---

## 13. Error Handling & Edge Cases

### 13.1 Validation Messages

The application provides helpful messages:
- **Error:** When no tasks configured
- **Warning:** When task types don't match algorithm requirements
- **Info:** Algorithm-specific requirements and guidance

### 13.2 Edge Cases

- Empty simulation result
- All deadline misses scenario
- 100% utilization scenario
- Single task scenario

---

## 14. Complete Workflow Examples

### 14.1 Complete RMS Workflow

1. Application start
2. Select "Basic Algorithms" → "RMS (Rate Monotonic)"
3. Configure tasks in task grid
4. Set duration slider
5. Click "Run"
6. View results in all tabs:
   - Gantt: Visual timeline
   - Metrics: Dashboard charts
   - Timeline: Step-by-step viewer
   - Analysis: Schedulability and statistics
   - Export: Download data
7. Export results (CSV or PNG)

### 14.2 Complete Server-Based Workflow

1. Select "Server-Based (Combined)" category
2. Select server algorithm (Polling/Deferrable/Sporadic/Background)
3. Configure server capacity and period
4. Add periodic tasks (background workload)
5. Add aperiodic tasks (foreground workload) with arrival times
6. Run simulation
7. View Server Analysis section

### 14.3 Complete Precedence Workflow

1. Select "Precedence-Constrained" category
2. Select algorithm with precedence
3. Open Advanced Options → Precedence tab
4. Enable precedence checkbox
5. Define constraints (e.g., "T1 -> T2\nT2 -> T3")
6. Configure tasks
7. Run simulation
8. View Precedence Graph in Analysis tab

### 14.4 Complete Overload Workflow

1. Select "Overload Handling" category
2. Select overload algorithm (e.g., FC-EDF)
3. Open Advanced Options → Overload tab
4. Configure PID parameters
5. Configure tasks with overload scenario (U > 100%)
6. Run simulation
7. View Service Level Plot and deadline miss handling

---

## 15. Algorithm Comparison

### 15.1 Basic Algorithms Comparison

| Algorithm | Priority Type | Utilization Bound | Use Case |
|-----------|--------------|-------------------|----------|
| RMS | Fixed | n(2^(1/n) - 1) | Simple periodic tasks |
| EDF | Dynamic | 100% | High utilization needed |
| DMS | Fixed | Varies | D < P scenarios |
| LLF | Dynamic | 100% | Laxity visibility needed |

### 15.2 Server Algorithms Comparison

| Server | Capacity Preservation | Response Time | Complexity |
|--------|---------------------|---------------|------------|
| Polling | No (lost if idle) | Moderate | Low |
| Deferrable | Yes (until period end) | Good | Medium |
| Sporadic | Dynamic replenishment | Best | High |
| Background | N/A (idle only) | Worst | Lowest |

---

## Quick Reference

### Algorithm Selection Guide

**For periodic tasks only:**
- Simple scenarios → RMS
- High utilization → EDF
- D < P → DMS
- Need laxity view → LLF

**For mixed periodic + aperiodic:**
- Best response → Sporadic Server
- Good balance → Deferrable Server
- Simple → Polling Server
- Baseline → Background Scheduler

**For task dependencies:**
- RMS/EDF/DMS with Precedence

**For value-based scheduling:**
- EDF+HVDF or HVDF Only

**For overload scenarios:**
- FC-EDF (Feedback Control)
- Feedback (m,k)-RMS
- Imprecise Computation
- (m,k)-Firm Tasks

### Keyboard Shortcuts

- None currently implemented (all mouse/touch interactions)

### Troubleshooting

**Issue:** Simulation not running  
**Solution:** Ensure tasks are configured and click "Run" button

**Issue:** No results displayed  
**Solution:** Check that tasks are valid (period > 0, computation time > 0)

**Issue:** Algorithm not available  
**Solution:** Check category selection matches algorithm type

**Issue:** Preset not loading  
**Solution:** Click "Load" button in preset dialog

---

## Appendix: Screenshot Index

All screenshots are organized in the `screenshots/` directory:

- `part1-getting-started/` - Initial setup and interface
- `part2-basic-algorithms/` - RMS, EDF, DMS, LLF
- `part3-server-algorithms/` - Server-based schedulers
- `part4-precedence/` - Precedence-constrained algorithms
- `part5-aperiodic/` - Aperiodic scheduling
- `part6-overload/` - Overload handling
- `part7-advanced/` - Advanced features (resources, etc.)
- `part8-presets/` - Preset system
- `part9-visualizations/` - All visualization types
- `part10-analysis/` - Analysis features
- `part11-export/` - Export functionality
- `part12-config/` - Configuration options
- `part13-errors/` - Error handling
- `part14-workflows/` - Complete workflows
- `part15-comparisons/` - Algorithm comparisons

---

*End of User Guide*
