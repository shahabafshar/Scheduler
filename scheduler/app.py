"""Real-Time Scheduling Simulator - Streamlit App"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add scheduler package to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Imports from scheduler package
from scheduler.core.task import PeriodicTask, AperiodicTask, ResourceConstraint
from scheduler.core.algorithms.rms import RMSScheduler
from scheduler.core.algorithms.edf import EDFScheduler
from scheduler.core.algorithms.dms import DMSScheduler
from scheduler.core.algorithms.llf import LLFScheduler
from scheduler.core.algorithms.server_schedulers import PollingServerScheduler, DeferrableServerScheduler, SporadicServerScheduler
from scheduler.core.analysis.schedulability import SchedulabilityAnalyzer
from scheduler.visualization.gantt import create_gantt_chart
from scheduler.visualization.metrics_dashboard import create_metrics_dashboard
from scheduler.configs import PRESETS


def main():
    st.set_page_config(
        page_title="Real-Time Scheduling Simulator",
        page_icon="⏰",
        layout="wide"
    )
    
    st.title("⏰ Real-Time Scheduling Simulator")
    st.markdown("Interactive tool for analyzing real-time task scheduling algorithms")
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")
        
        # Algorithm selection
        algorithm_category = st.radio(
            "Algorithm Category",
            ["Basic Algorithms", "Server-Based (Combined)"],
            horizontal=True
        )
        
        if algorithm_category == "Basic Algorithms":
            algorithm = st.selectbox(
                "Scheduling Algorithm",
                ["RMS (Rate Monotonic)", "EDF (Earliest Deadline First)", "DMS (Deadline Monotonic)", "LLF (Least Laxity First)"]
            )
        else:
            algorithm = st.selectbox(
                "Server Type",
                ["Polling Server", "Deferrable Server", "Sporadic Server"]
            )
            st.info("Server-based schedulers integrate periodic and aperiodic tasks")
        
        # Simulation duration
        duration = st.slider("Simulation Duration", min_value=10, max_value=200, value=50, step=10)
        
        st.markdown("---")
        
        # Preset examples
        st.subheader("📚 Preset Examples")
        preset_selection = st.selectbox(
            "Choose a preset configuration:",
            ["None"] + list(PRESETS.keys())
        )
        
        if preset_selection != "None":
            st.session_state.load_preset = preset_selection
    
    # Task input
    st.header("Task Set Definition")
    
    # Initialize session state
    if 'tasks' not in st.session_state:
        st.session_state.tasks = [
            {'id': 'T1', 'computation_time': 2.0, 'period': 8.0, 'deadline': 8.0}
        ]
    
    # Handle preset examples
    if 'load_preset' in st.session_state and st.session_state.load_preset in PRESETS:
        preset_name = st.session_state.load_preset
        preset_tasks = PRESETS[preset_name]
        st.session_state.tasks = [
            {
                'id': task.id,
                'computation_time': task.computation_time,
                'period': task.period,
                'deadline': task.deadline
            }
            for task in preset_tasks
        ]
        st.success(f"✓ Loaded preset: {preset_name}")
        del st.session_state.load_preset
    
    # Task input table
    task_data = st.data_editor(
        st.session_state.tasks,
        column_config={
            "id": st.column_config.TextColumn("Task ID", required=True),
            "computation_time": st.column_config.NumberColumn("C (Computation Time)", min_value=0.1, step=0.1, required=True),
            "period": st.column_config.NumberColumn("P (Period)", min_value=1, step=1, required=True),
            "deadline": st.column_config.NumberColumn("D (Deadline)", min_value=0.1, step=0.1, required=True)
        },
        hide_index=True,
        num_rows="dynamic",
        width='stretch'
    )
    
    st.session_state.tasks = task_data
    
    # Convert to PeriodicTask objects
    if st.session_state.tasks:
        try:
            periodic_tasks = [
                PeriodicTask(
                    id=str(task['id']),
                    computation_time=float(task['computation_time']),
                    period=float(task['period']),
                    deadline=float(task.get('deadline', task['period']))
                )
                for task in st.session_state.tasks
            ]
            
            # Schedulability Analysis
            st.header("Schedulability Analysis")
            
            if algorithm.startswith("RMS"):
                results = SchedulabilityAnalyzer.analyze_rms(periodic_tasks)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Harmonic", "Yes" if results['is_harmonic'] else "No")
                with col2:
                    util_test = results['utilization_test']
                    st.metric("Utilization", f"{util_test['utilization']:.3f}")
                with col3:
                    st.metric("Bound", f"{util_test['bound']:.3f}")
                
                st.info(util_test['explanation'])
                
                if not util_test['schedulable'] and 'exact_analysis' in results:
                    st.subheader("Exact Analysis (Completion Time Test)")
                    exact_df = pd.DataFrame(results['exact_analysis']).T
                    st.dataframe(exact_df, width='stretch', hide_index=True)
            elif algorithm.startswith("EDF"):
                schedulable, utilization, explanation = SchedulabilityAnalyzer.edf_utilization_test(periodic_tasks)
                st.metric("Utilization", f"{utilization:.3f}")
                st.info(explanation)
            elif algorithm.startswith("DMS"):
                schedulable, utilization, bound, explanation = SchedulabilityAnalyzer.dms_utilization_test(periodic_tasks)
                st.metric("Utilization", f"{utilization:.3f}")
                st.metric("Bound", f"{bound:.3f}")
                st.info(explanation)
            
            # Run Simulation
            if st.button("▶️ Run Simulation"):
                st.header("Schedule Results")
                
                # Select scheduler
                if algorithm.startswith("RMS"):
                    scheduler = RMSScheduler(periodic_tasks, duration)
                elif algorithm.startswith("EDF"):
                    scheduler = EDFScheduler(periodic_tasks, duration)
                elif algorithm.startswith("DMS"):
                    scheduler = DMSScheduler(periodic_tasks, duration)
                elif algorithm.startswith("LLF"):
                    scheduler = LLFScheduler(periodic_tasks, duration)
                elif "Polling" in algorithm:
                    scheduler = PollingServerScheduler(periodic_tasks, duration)
                elif "Deferrable" in algorithm:
                    scheduler = DeferrableServerScheduler(periodic_tasks, duration)
                elif "Sporadic" in algorithm:
                    scheduler = SporadicServerScheduler(periodic_tasks, duration)
                
                # Run simulation
                result = scheduler.simulate()
                
                # Display results
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("CPU Utilization", f"{result.cpu_utilization:.1%}")
                with col2:
                    st.metric("Context Switches", result.total_context_switches)
                
                st.metric("Deadline Misses", len(result.deadline_misses))
                
                if result.deadline_misses:
                    st.warning(f"⚠️ {len(result.deadline_misses)} deadline miss(es) detected!")
                else:
                    st.success("✅ All deadlines met!")
                
                # Gantt Chart
                st.subheader("📊 Gantt Chart Visualization")
                fig = create_gantt_chart(result, max_time=duration)
                st.plotly_chart(fig, width='stretch')
                
                # Timeline
                st.subheader("Detailed Timeline")
                timeline_df = pd.DataFrame([
                    {
                        'Time': event.time,
                        'Task': event.task_id or 'IDLE',
                        'Event': event.event_type
                    }
                    for event in result.events[:100]  # Show first 100 events
                ])
                st.dataframe(timeline_df, width='stretch', hide_index=True)
                
                # Metrics Dashboard
                st.subheader("📊 Metrics Dashboard")
                metrics_fig = create_metrics_dashboard(result)
                st.plotly_chart(metrics_fig, width='stretch')
                
                # Export options
                st.subheader("📥 Export Results")
                col1, col2 = st.columns(2)
                
                with col1:
                    # CSV export
                    csv = timeline_df.to_csv(index=False)
                    st.download_button(
                        label="📊 Download Timeline (CSV)",
                        data=csv,
                        file_name=f"schedule_{algorithm.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Add info about features
                    with st.expander("ℹ️ Available Features"):
                        st.markdown("""
                        **✅ Currently Available:**
                        - Basic algorithms (RMS, EDF, DMS, LLF) ✓
                        - Server-based scheduling (Polling, Deferrable, Sporadic) ✓
                        - Metrics dashboard (4 interactive charts) ✓
                        - Schedulability analysis ✓
                        - Gantt chart visualization ✓
                        - CSV export ✓
                        
                        **🚧 Coming Soon (code ready, UI pending):**
                        - Resource access protocols (PIP, PCP)
                        - Precedence-constrained scheduling
                        - Overload handling (Imprecise, HVDF, (m,k)-firm)
                        - Step-by-step execution viewer
                        """)
                
        except Exception as e:
            st.error(f"Error: {e}")
            st.exception(e)


if __name__ == "__main__":
    main()

