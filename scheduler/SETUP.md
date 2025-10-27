# Quick Setup Guide

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python test_scheduler.py
   ```

## Running the Application

### Using Streamlit

Start the interactive web application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using Python Scripts

Run the test script:
```bash
python test_scheduler.py
```

## Basic Usage

1. **In the Streamlit app:**
   - Select an algorithm (RMS, EDF, DMS, or LLF)
   - Define your task set using the data editor
   - Click "Run Simulation"
   - View the schedulability analysis, Gantt chart, and timeline

2. **Preset Examples:**
   - Click preset example buttons in the sidebar to load documented task sets

3. **Interpreting Results:**
   - **Green checkmark**: All deadlines met
   - **Red warning**: Deadline misses detected
   - **Gantt Chart**: Visual representation of task execution
   - **Timeline**: Detailed event log

## Testing

Run the test script to verify basic functionality:
```bash
python test_scheduler.py
```

Expected output should show:
- Schedulability analysis
- CPU utilization
- Context switches
- Timeline events

## Troubleshooting

1. **Import errors**: Make sure you're running from the scheduler directory
2. **Port already in use**: Change the port with `streamlit run app.py --server.port 8502`
3. **Missing dependencies**: Run `pip install -r requirements.txt` again

