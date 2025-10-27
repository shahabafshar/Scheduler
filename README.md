# Real-Time Scheduling Simulator

A comprehensive simulator for real-time task scheduling algorithms with intuitive visualization and analysis tools.

## Features

✅ **7 Scheduling Algorithms**:
- RMS (Rate Monotonic)
- EDF (Earliest Deadline First)
- DMS (Deadline Monotonic)
- LLF (Least Laxity First)
- Polling Server
- Deferrable Server
- Sporadic Server

✅ **Schedulability Analysis**: Utilization tests, completion time test, harmonic detection

✅ **Interactive Visualizations**:
- Gantt charts (execution timeline)
- Metrics dashboard (4 charts)
- Detailed event timeline

✅ **6 Preset Examples** from documentation

✅ **Export**: CSV download capability

## Quick Start

### Run the Simulator

```bash
# From project root
streamlit run scheduler/app.py

# Or
cd scheduler
streamlit run app.py
```

### Test Without UI

```bash
python test_scheduler.py
```

## What You Get

1. **Task Definition**: Define periodic tasks with computation time, period, and deadline
2. **Algorithm Selection**: Choose from 7 scheduling algorithms
3. **Schedulability Analysis**: Automatic verification of schedule feasibility
4. **Visualization**: Interactive Gantt charts and metrics
5. **Export**: Download results for further analysis

## Test Results

RMS Example 1 (T1=(2,4), T2=(1,8)):
- ✅ CPU Utilization: 65%
- ✅ No deadline misses
- ✅ Verified against documentation

## Documentation

- `FINAL_STATUS.md` - Complete project status
- `scheduler/COMPLETE_STATUS.md` - Implementation details
- `scheduler/UI_UPDATE.md` - UI features and updates
- `scheduler/README_RUNNING.md` - How to run guide

## Architecture

```
scheduler/
├── app.py                 # Streamlit UI
├── configs.py             # Preset examples
├── core/                  # Core algorithms
├── visualization/         # Charts and graphs
└── requirements.txt       # Dependencies
```

## Requirements

- Python 3.10+
- Streamlit
- Plotly
- Pandas

Install:
```bash
pip install -r scheduler/requirements.txt
```

## Status

✅ **Production Ready** - Fully functional with verified accuracy
🎯 **All core features implemented and tested**
📊 **Rich visualizations and analysis tools**

The simulator is ready to use for real-time scheduling analysis!

