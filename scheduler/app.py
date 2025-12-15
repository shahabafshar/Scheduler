"""Real-Time Scheduling Simulator - Streamlit App"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add scheduler package to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Imports from scheduler package
from scheduler.core.task import PeriodicTask, AperiodicTask, ResourceConstraint, CriticalSection, PrecedenceConstraint
from scheduler.core.algorithms.rms import RMSScheduler
from scheduler.core.algorithms.edf import EDFScheduler
from scheduler.core.algorithms.dms import DMSScheduler
from scheduler.core.algorithms.llf import LLFScheduler
from scheduler.core.algorithms.combined import PollingServerScheduler, DeferrableServerScheduler, SporadicServerScheduler, BackgroundScheduler
from scheduler.core.algorithms.precedence import RMSWithPrecedence, DMSWithPrecedence, EDFWithPrecedence
from scheduler.core.algorithms.edf_hvdf import EDFHVDFScheduler, HVDFOnlyScheduler
from scheduler.core.algorithms.edf_hvdf_periodic import EDFHVDFPeriodicScheduler
from scheduler.core.algorithms.resource_aware import (
    ResourceAwareRMSScheduler, ResourceAwareEDFScheduler,
    ResourceAwareDMSScheduler, ResourceAwareLLFScheduler,
    create_resource_constraints, map_protocol_name
)
from scheduler.core.analysis.schedulability import SchedulabilityAnalyzer
from scheduler.visualization.gantt import create_gantt_chart, create_priority_timeline
from scheduler.visualization.metrics_dashboard import create_metrics_dashboard, create_service_level_plot
from scheduler.visualization.precedence_graph import create_precedence_graph
from scheduler.visualization.mk_history import create_mk_history_chart
from scheduler.visualization.timeline_interactive import create_timeline_step_viewer, create_timeline_summary
from scheduler.configs import PRESETS, PRESET_CATALOG


@st.dialog("Sample Presets", width="large")
def show_preset_dialog():
    """Modal dialog for browsing and loading presets."""
    # Group presets by category
    categories = {}
    for preset_id, preset_data in PRESET_CATALOG.items():
        cat = preset_data["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((preset_id, preset_data))

    # Category tabs for compact navigation
    cat_names = list(categories.keys())
    tabs = st.tabs(cat_names)

    for tab, cat in zip(tabs, cat_names):
        with tab:
            presets_in_cat = categories[cat]
            # 3 columns for wider screens
            cols = st.columns(3)
            for idx, (preset_id, preset_data) in enumerate(presets_in_cat):
                with cols[idx % 3]:
                    algo_short = preset_data["algorithm"].split()[0]
                    # Compact card
                    st.markdown(f"**{preset_data['name']}**")
                    st.caption(f"`{algo_short}` {preset_data.get('description', '')[:50]}...")
                    # Info line
                    info = []
                    if "utilization" in preset_data:
                        info.append(f"U={preset_data['utilization']}")
                    if "expected_value" in preset_data:
                        info.append(f"V={preset_data['expected_value']}")
                    if "config" in preset_data:
                        info.append(f"Cs={preset_data['config'].get('server_capacity', '?')}")
                    if info:
                        st.caption(" | ".join(info))
                    if st.button("Load", key=f"dlg_{preset_id}", width='stretch'):
                        st.session_state.load_preset_catalog = preset_id
                        st.rerun()


def main():
    st.set_page_config(
        page_title="Real-Time Scheduling Simulator",
        page_icon="⏰",
        layout="wide"
    )

    # ========== HEADER WITH RUN & PRESETS BUTTONS ==========
    header_col1, header_col2, header_col3 = st.columns([5, 1, 1])
    with header_col1:
        st.title("Real-Time Scheduling Simulator")
    with header_col2:
        if st.button("Presets", type="secondary", width='stretch', key="header_presets_btn", help="Browse 21 ready-to-run task configurations"):
            show_preset_dialog()
    with header_col3:
        run_button = st.button("Run", type="primary", width='stretch', key="header_run_btn")

    # Show hint banner on first visit
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit = True
        st.success("✨ **New here?** Click the **Presets** button above to load ready-made example configurations!", icon="👉")

    # ========== INITIALIZE SESSION STATE ==========
    if 'algorithm_category' not in st.session_state:
        st.session_state.algorithm_category = "Basic Algorithms"
    if 'algorithm' not in st.session_state:
        st.session_state.algorithm = "RMS (Rate Monotonic)"
    if 'current_preset' not in st.session_state:
        st.session_state.current_preset = "None"
    if 'simulation_result' not in st.session_state:
        st.session_state.simulation_result = None
    if 'resources' not in st.session_state:
        st.session_state.resources = []
    if 'resource_protocol' not in st.session_state:
        st.session_state.resource_protocol = None
    if 'tasks' not in st.session_state:
        st.session_state.tasks = [
            {
                'id': 'T1',
                'task_type': 'periodic',
                'computation_time': 2.0,
                'period': 8.0,
                'deadline': 8.0,
                'value': 0.0,
                'preemptive': True,
                'arrival_time': 0.0
            }
        ]

    # Ensure all existing tasks have task_type field
    for task in st.session_state.tasks:
        if 'task_type' not in task:
            task['task_type'] = 'periodic'

    # ========== HANDLE CATALOG PRESET LOADING ==========
    if 'load_preset_catalog' in st.session_state:
        preset_id = st.session_state.load_preset_catalog
        if preset_id in PRESET_CATALOG:
            preset_data = PRESET_CATALOG[preset_id]
            tasks_data = preset_data["tasks"]

            # Handle Server-Based presets (dict with periodic + aperiodic)
            if isinstance(tasks_data, dict) and "periodic" in tasks_data:
                # Server-Based preset with both task types
                all_tasks = []
                for task in tasks_data["periodic"]:
                    all_tasks.append({
                        'id': task.id, 'task_type': 'periodic',
                        'computation_time': task.computation_time,
                        'period': task.period, 'deadline': task.deadline,
                        'value': getattr(task, 'value', 0.0),
                        'preemptive': getattr(task, 'preemptive', True),
                        'arrival_time': 0.0
                    })
                for task in tasks_data["aperiodic"]:
                    all_tasks.append({
                        'id': task.id, 'task_type': 'aperiodic',
                        'computation_time': task.computation_time,
                        'arrival_time': task.arrival_time, 'deadline': task.deadline,
                        'value': task.value, 'preemptive': task.preemptive,
                        'period': 0.0
                    })
                st.session_state.tasks = all_tasks
                # Set server config
                if "config" in preset_data:
                    st.session_state['server_capacity'] = preset_data["config"].get("server_capacity", 2.0)
                    st.session_state['server_period'] = preset_data["config"].get("server_period", 5.0)
            else:
                # Regular task list
                is_aperiodic = all(isinstance(task, AperiodicTask) for task in tasks_data)
                if is_aperiodic:
                    st.session_state.tasks = [
                        {'id': task.id, 'task_type': 'aperiodic',
                         'computation_time': task.computation_time,
                         'arrival_time': task.arrival_time, 'deadline': task.deadline,
                         'value': task.value, 'preemptive': task.preemptive, 'period': 0.0}
                        for task in tasks_data
                    ]
                else:
                    st.session_state.tasks = [
                        {'id': task.id, 'task_type': 'periodic',
                         'computation_time': task.computation_time,
                         'period': task.period, 'deadline': task.deadline,
                         'value': getattr(task, 'value', 0.0),
                         'preemptive': getattr(task, 'preemptive', True), 'arrival_time': 0.0}
                        for task in tasks_data
                    ]

            # Set category and algorithm from preset
            st.session_state.algorithm_category = preset_data["category"]
            st.session_state.algorithm = preset_data["algorithm"]
            st.session_state.current_preset = preset_data["name"]

            # Handle precedence constraints
            if "precedence" in preset_data:
                st.session_state['enable_prec_adv'] = True
                st.session_state['prec_text_adv'] = preset_data["precedence"]
            else:
                st.session_state['enable_prec_adv'] = False

            st.session_state['trigger_simulation'] = True
            del st.session_state.load_preset_catalog
            st.rerun()

    # ========== HANDLE LEGACY PRESET LOADING ==========
    # This MUST happen before selectboxes so they show correct values
    if 'load_preset' in st.session_state and st.session_state.load_preset in PRESETS:
        preset_name = st.session_state.load_preset
        preset_tasks = PRESETS[preset_name]

        # Properly detect aperiodic tasks using isinstance
        is_aperiodic = all(isinstance(task, AperiodicTask) for task in preset_tasks)

        if is_aperiodic:
            st.session_state.tasks = [
                {
                    'id': task.id,
                    'task_type': 'aperiodic',
                    'computation_time': task.computation_time,
                    'arrival_time': task.arrival_time,
                    'deadline': task.deadline,
                    'value': task.value,
                    'preemptive': task.preemptive,
                    'period': 0.0  # Not used for aperiodic
                }
                for task in preset_tasks
            ]
            st.session_state.algorithm_category = "Aperiodic Scheduling"
            st.session_state.algorithm = "EDF+HVDF (Value-Based)"
        else:
            st.session_state.tasks = [
                {
                    'id': task.id,
                    'task_type': 'periodic',
                    'computation_time': task.computation_time,
                    'period': task.period,
                    'deadline': task.deadline,
                    'value': getattr(task, 'value', 0.0),
                    'preemptive': getattr(task, 'preemptive', True),
                    'arrival_time': 0.0
                }
                for task in preset_tasks
            ]
            # Parse category and algorithm from preset name format: [Category|Algorithm] Description
            if preset_name.startswith("["):
                # Extract tag content between [ and ]
                tag_end = preset_name.find("]")
                if tag_end > 0:
                    tag = preset_name[1:tag_end]  # e.g., "Basic|RMS" or "Overload"
                    parts = tag.split("|")
                    category_tag = parts[0].strip()
                    algo_tag = parts[1].strip() if len(parts) > 1 else ""

                    # Map category tag to full category name
                    if category_tag == "Basic":
                        st.session_state.algorithm_category = "Basic Algorithms"
                    elif category_tag == "Overload":
                        st.session_state.algorithm_category = "Overload Handling"
                    elif category_tag == "Aperiodic":
                        st.session_state.algorithm_category = "Aperiodic Scheduling"
                    elif category_tag == "Server":
                        st.session_state.algorithm_category = "Server-Based (Combined)"
                    elif category_tag == "Precedence":
                        st.session_state.algorithm_category = "Precedence-Constrained"
                    else:
                        st.session_state.algorithm_category = "Basic Algorithms"

                    # Map algorithm tag to full algorithm name
                    if algo_tag == "RMS":
                        st.session_state.algorithm = "RMS (Rate Monotonic)"
                    elif algo_tag == "EDF":
                        st.session_state.algorithm = "EDF (Earliest Deadline First)"
                    elif algo_tag == "DMS":
                        st.session_state.algorithm = "DMS (Deadline Monotonic)"
                    elif algo_tag == "LLF":
                        st.session_state.algorithm = "LLF (Least Laxity First)"
                    elif algo_tag == "HVDF":
                        st.session_state.algorithm = "EDF+HVDF (Value-Based)"
                    elif category_tag == "Overload":
                        st.session_state.algorithm = "FC-EDF (Feedback Control)"
                    else:
                        st.session_state.algorithm = "RMS (Rate Monotonic)"
                else:
                    st.session_state.algorithm_category = "Basic Algorithms"
                    st.session_state.algorithm = "RMS (Rate Monotonic)"
            else:
                # Fallback for old-style preset names
                st.session_state.algorithm_category = "Basic Algorithms"
                if "RMS" in preset_name:
                    st.session_state.algorithm = "RMS (Rate Monotonic)"
                elif "EDF" in preset_name:
                    st.session_state.algorithm = "EDF (Earliest Deadline First)"
                elif "DMS" in preset_name:
                    st.session_state.algorithm = "DMS (Deadline Monotonic)"
                else:
                    st.session_state.algorithm = "RMS (Rate Monotonic)"

        # Trigger simulation automatically
        st.session_state['trigger_simulation'] = True

        # Clear the load_preset flag
        del st.session_state.load_preset

        # Force rerun to apply changes
        st.rerun()

    # ========== TWO-COLUMN LAYOUT: CONFIG (30%) | RESULTS (70%) ==========
    config_col, results_col = st.columns([5, 5], gap="medium")

    # ========== LEFT PANEL: CONFIGURATION ==========
    with config_col:
        # Show success message if preset was just loaded
        if st.session_state.get('preset_just_loaded'):
            st.success(f"Loaded preset")
            del st.session_state['preset_just_loaded']

        # Algorithm Selection (compact)
        categories = ["Basic Algorithms", "Server-Based (Combined)", "Precedence-Constrained", "Overload Handling", "Aperiodic Scheduling"]

        # Get current category index
        current_cat = st.session_state.get('algorithm_category', "Basic Algorithms")
        cat_index = categories.index(current_cat) if current_cat in categories else 0

        # Category selectbox without key - use index only
        algorithm_category = st.selectbox(
            "Category",
            categories,
            index=cat_index
        )
        st.session_state.algorithm_category = algorithm_category

        # Algorithm dropdown based on category
        if algorithm_category == "Basic Algorithms":
            options = ["RMS (Rate Monotonic)", "EDF (Earliest Deadline First)", "DMS (Deadline Monotonic)", "LLF (Least Laxity First)"]
        elif algorithm_category == "Server-Based (Combined)":
            options = ["Polling Server", "Deferrable Server", "Sporadic Server", "Background Scheduler"]
        elif algorithm_category == "Precedence-Constrained":
            options = ["RMS with Precedence", "EDF with Precedence", "DMS with Precedence"]
        elif algorithm_category == "Overload Handling":
            options = ["FC-EDF (Feedback Control)", "Feedback (m,k)-RMS", "Imprecise Computation", "HVDF (Value-Based)", "(m,k)-Firm Tasks"]
        else:  # Aperiodic Scheduling
            options = ["EDF+HVDF (Value-Based)", "HVDF Only"]

        # Determine current algorithm index
        current_algo = st.session_state.get('algorithm')
        if current_algo and current_algo in options:
            algo_index = options.index(current_algo)
        else:
            algo_index = 0

        # Algorithm selectbox without key - use index only
        algorithm = st.selectbox("Algorithm", options, index=algo_index)
        st.session_state.algorithm = algorithm

        # Server-specific configuration
        if algorithm_category == "Server-Based (Combined)":
            srv_c1, srv_c2 = st.columns(2)
            with srv_c1:
                # Use consistent key - widget value stored directly in session_state['server_capacity']
                if 'server_capacity' not in st.session_state:
                    st.session_state['server_capacity'] = 2.0
                st.number_input(
                    "Server Capacity (Cs)", min_value=0.1, max_value=20.0,
                    step=0.5, key='server_capacity'
                )
            with srv_c2:
                if 'server_period' not in st.session_state:
                    st.session_state['server_period'] = 5.0
                st.number_input(
                    "Server Period (Ps)", min_value=1.0, max_value=50.0,
                    step=1.0, key='server_period'
                )
            st.caption("Server-Based needs both periodic + aperiodic tasks")

        # Duration slider (compact)
        duration = st.slider("Duration", min_value=10, max_value=200, value=50, step=10)

        st.divider()

        # ===== TASK GRID (Compact) =====
        # Prepare column config
        enable_resources = st.session_state.resource_protocol and st.session_state.resource_protocol != "None"
        resource_ids = [r['id'] for r in st.session_state.resources] if st.session_state.resources else []

        algorithm_category = st.session_state.get('algorithm_category', "Basic Algorithms")
        selected_algorithm = st.session_state.get('algorithm', "RMS (Rate Monotonic)")

        enable_overload_params = algorithm_category == "Overload Handling"
        enable_mk = enable_overload_params and selected_algorithm == "(m,k)-Firm Tasks"
        enable_imprecise = enable_overload_params and selected_algorithm == "Imprecise Computation"
        # Value column needed for: HVDF, Aperiodic scheduling (EDF+HVDF), Server-Based
        enable_value_col = (
            (enable_overload_params and selected_algorithm == "HVDF (Value-Based)") or
            algorithm_category == "Aperiodic Scheduling" or
            algorithm_category == "Server-Based (Combined)"
        )

        has_aperiodic = any(task.get('task_type') == 'aperiodic' for task in st.session_state.tasks)

        # Determine allowed task types based on algorithm category
        if algorithm_category in ["Basic Algorithms", "Precedence-Constrained", "Overload Handling"]:
            allowed_task_types = ['periodic']
            # Auto-set task types to periodic for these categories
            for task in st.session_state.tasks:
                if task.get('task_type') != 'periodic':
                    task['task_type'] = 'periodic'
                # Ensure period > 0 for periodic tasks (fix division by zero)
                if task.get('period', 0) <= 0:
                    task['period'] = max(task.get('deadline', 10.0), task.get('computation_time', 1.0) * 2)
        else:
            # Aperiodic Scheduling and Server-Based allow both types
            allowed_task_types = ['periodic', 'aperiodic']

        # Simplified column config for compact view
        column_config = {
            "id": st.column_config.TextColumn("ID", required=True, width="small"),
            "task_type": st.column_config.SelectboxColumn(
                "Type",
                options=allowed_task_types,
                required=True,
                width="small",
                disabled=(len(allowed_task_types) == 1)  # Disable if only one option
            ),
            "computation_time": st.column_config.NumberColumn("C", min_value=0.1, step=0.1, required=True, width="small"),
            "deadline": st.column_config.NumberColumn("D", min_value=0.1, step=0.1, required=True, width="small"),
            "preemptive": st.column_config.CheckboxColumn("Pre", width="small")
        }
        # Only show value column when relevant algorithms are selected
        if enable_value_col:
            column_config["value"] = st.column_config.NumberColumn("V", min_value=0.0, step=0.1, width="small")
            # Initialize value for tasks if not present
            for task in st.session_state.tasks:
                if 'value' not in task:
                    task['value'] = 1.0  # Default value

        if has_aperiodic:
            column_config["arrival_time"] = st.column_config.NumberColumn("Arr", min_value=0, step=0.1, required=True, width="small")
            column_config["period"] = st.column_config.NumberColumn("P", min_value=0, step=1, width="small")
        else:
            column_config["period"] = st.column_config.NumberColumn("P", min_value=1, step=1, required=True, width="small")
            column_config["arrival_time"] = st.column_config.NumberColumn("Arr", min_value=0, step=0.1, width="small")

        # Handle resource columns
        if not enable_resources or not resource_ids:
            for task in st.session_state.tasks:
                if 'resources' in task:
                    del task['resources']
                if 'cs_durations' in task:
                    del task['cs_durations']
        else:
            column_config["resources"] = st.column_config.MultiselectColumn("Res", options=resource_ids)
            column_config["cs_durations"] = st.column_config.TextColumn("CS")
            for task in st.session_state.tasks:
                if 'resources' not in task:
                    task['resources'] = []
                if 'cs_durations' not in task:
                    task['cs_durations'] = ''

        # Handle overload columns
        if enable_overload_params:
            for task in st.session_state.tasks:
                if enable_mk and 'mk_value' not in task:
                    task['mk_value'] = ""
                if enable_imprecise and 'mandatory_time' not in task:
                    task['mandatory_time'] = 0.0
                    task['optional_time'] = 0.0
                if not enable_mk and 'mk_value' in task:
                    del task['mk_value']
                # Note: We preserve 'value' even when not displayed - never delete user data
                if not enable_imprecise:
                    if 'mandatory_time' in task:
                        del task['mandatory_time']
                    if 'optional_time' in task:
                        del task['optional_time']

            if enable_mk:
                column_config["mk_value"] = st.column_config.TextColumn("(m,k)")
            # Note: value column already handled above via enable_value_col
            if enable_imprecise:
                column_config["mandatory_time"] = st.column_config.NumberColumn("Mand", min_value=0.0, step=0.1)
                column_config["optional_time"] = st.column_config.NumberColumn("Opt", min_value=0.0, step=0.1)

        # Compact task grid with fixed height
        try:
            task_data = st.data_editor(
                st.session_state.tasks,
                column_config=column_config if st.session_state.tasks else {},
                hide_index=True,
                num_rows="dynamic",
                height=200,
                width='stretch',
                key='task_grid_editor'
            )
            st.session_state.tasks = task_data
        except Exception as e:
            st.warning(f"Grid error: {e}")
            st.dataframe(pd.DataFrame(st.session_state.tasks), height=200, width='stretch', hide_index=True)
    
        # ===== ADVANCED OPTIONS (Collapsed Expander) =====
        with st.expander("Advanced Options", expanded=False):
            adv_tab1, adv_tab2, adv_tab3 = st.tabs(["Resources", "Precedence", "Overload"])

            # --- Resources Tab ---
            with adv_tab1:
                enable_resources_adv = st.checkbox("Enable Resource Sharing", value=False, key='enable_res_adv')
                if enable_resources_adv:
                    st.session_state.resource_protocol = st.selectbox(
                        "Protocol",
                        ["Priority Inheritance (PIP)", "Priority Ceiling (PCP)", "None"],
                        key='res_protocol_adv'
                    )
                    if not st.session_state.resources:
                        st.session_state.resources = [{'id': 'R1'}]
                    resource_data = st.data_editor(
                        st.session_state.resources,
                        column_config={"id": st.column_config.TextColumn("Resource ID", required=True)},
                        hide_index=True, num_rows="dynamic", height=100, key='res_grid_adv'
                    )
                    st.session_state.resources = resource_data
                else:
                    st.session_state.resource_protocol = None

            # --- Precedence Tab ---
            with adv_tab2:
                enable_precedence = st.checkbox("Enable Precedence", value=False, key='enable_prec_adv')
                precedence_constraints = []
                if enable_precedence:
                    precedence_text = st.text_area(
                        "Relationships (T1 -> T2)",
                        help="One per line: T1 -> T2",
                        height=80, key='prec_text_adv'
                    )
                    for line in precedence_text.strip().split('\n'):
                        line = line.strip()
                        if '->' in line:
                            parts = [p.strip() for p in line.split('->')]
                            if len(parts) == 2:
                                precedence_constraints.append({'predecessor': parts[0], 'successor': parts[1]})
                    if precedence_constraints:
                        st.caption(f"{len(precedence_constraints)} constraint(s)")

            # --- Overload Tab ---
            with adv_tab3:
                overload_config = {}
                if algorithm_category == "Overload Handling":
                    if "FC-EDF" in algorithm:
                        c1, c2 = st.columns(2)
                        with c1:
                            overload_config['target_miss_ratio'] = st.number_input("Target Miss Ratio", 0.01, 1.0, 0.05, 0.01, key='fc_tmr')
                            overload_config['kp'] = st.number_input("Kp", 0.0, 1.0, 0.1, 0.01, key='fc_kp')
                        with c2:
                            overload_config['ki'] = st.number_input("Ki", 0.0, 1.0, 0.01, 0.01, key='fc_ki')
                            overload_config['kd'] = st.number_input("Kd", 0.0, 1.0, 0.05, 0.01, key='fc_kd')
                    elif "Feedback (m,k)-RMS" in algorithm:
                        c1, c2 = st.columns(2)
                        with c1:
                            overload_config['target_dfr'] = st.number_input("Target DFR", 0.01, 1.0, 0.05, 0.01, key='mk_dfr')
                            overload_config['kp'] = st.number_input("Kp", 0.0, 1.0, 0.1, 0.01, key='mk_kp')
                        with c2:
                            overload_config['ki'] = st.number_input("Ki", 0.0, 1.0, 0.01, 0.01, key='mk_ki')
                            overload_config['kd'] = st.number_input("Kd", 0.0, 1.0, 0.05, 0.01, key='mk_kd')
                    else:
                        st.caption("Configure in task table")
                else:
                    st.caption("Select Overload Handling category")
                # Store overload config in session state
                st.session_state.overload_config = overload_config


    # POST-PROCESSING: Auto-fill CS durations
    enable_resources = st.session_state.resource_protocol and st.session_state.resource_protocol != "None"
    resource_ids = [r['id'] for r in st.session_state.resources] if st.session_state.resources else []
    cs_updated = False
    if enable_resources and resource_ids:
        for i, task in enumerate(st.session_state.tasks):
            selected_resources = task.get('resources', [])
            durations_str = task.get('cs_durations', '')
            try:
                durations = [float(d.strip()) for d in durations_str.split(',')] if durations_str else []
            except:
                durations = []
            if selected_resources and len(durations) < len(selected_resources):
                while len(durations) < len(selected_resources):
                    durations.append(1.0)
                st.session_state.tasks[i]['cs_durations'] = ','.join([str(d) for d in durations])
                cs_updated = True
    if cs_updated:
        st.rerun()

    # ========== CONVERT TASKS AND RUN SIMULATION ==========
    periodic_tasks = []
    aperiodic_tasks = []
    prec_objects = []
    scheduler = None
    result = None

    if st.session_state.tasks:
        try:
            # Convert precedence constraints
            if 'enable_prec_adv' in st.session_state and st.session_state.enable_prec_adv:
                enable_precedence = True
                # Re-parse precedence from session state
                precedence_text = st.session_state.get('prec_text_adv', '')
                precedence_constraints = []
                for line in precedence_text.strip().split('\n'):
                    line = line.strip()
                    if '->' in line:
                        parts = [p.strip() for p in line.split('->')]
                        if len(parts) == 2:
                            precedence_constraints.append({'predecessor': parts[0], 'successor': parts[1]})
                for prec in precedence_constraints:
                    prec_objects.append(PrecedenceConstraint(predecessor=prec['predecessor'], successor=prec['successor']))
            else:
                enable_precedence = False
                precedence_constraints = []

            for task in st.session_state.tasks:
                task_type = task.get('task_type', 'periodic')
                critical_sections = []
                if enable_resources:
                    selected_resources = task.get('resources', [])
                    durations_str = task.get('cs_durations', '')
                    if selected_resources and durations_str:
                        try:
                            durations = [float(d.strip()) for d in durations_str.split(',')]
                            for res_id, cs_duration in zip(selected_resources, durations):
                                critical_sections.append(CriticalSection(
                                    resource_id=res_id, start_offset=0.0, duration=cs_duration,
                                    task_id=str(task['id']), completed=False
                                ))
                        except:
                            pass

                if task_type == 'aperiodic':
                    aperiodic_tasks.append(AperiodicTask(
                        id=str(task['id']), arrival_time=float(task.get('arrival_time', 0)),
                        computation_time=float(task['computation_time']),
                        deadline=float(task.get('deadline', task['computation_time'])),
                        value=float(task.get('value', 0.0)), preemptive=bool(task.get('preemptive', True)),
                        task_type='aperiodic'
                    ))
                else:
                    # Ensure period > 0 to avoid division by zero
                    period_val = float(task.get('period', 0))
                    if period_val <= 0:
                        period_val = max(float(task.get('deadline', 10.0)), float(task['computation_time']) * 2)
                    periodic_tasks.append(PeriodicTask(
                        id=str(task['id']), computation_time=float(task['computation_time']),
                        period=period_val, deadline=float(task.get('deadline', period_val)),
                        critical_sections=critical_sections, value=float(task.get('value', 0.0)),
                        preemptive=bool(task.get('preemptive', True)), task_type='periodic'
                    ))

            # Create ResourceConstraint objects if resources enabled
            resource_constraints = []
            resource_protocol = "none"
            if enable_resources and periodic_tasks:
                # Assign priorities first so we can calculate priority ceiling
                sorted_by_period = sorted(periodic_tasks, key=lambda t: t.period)
                for i, task in enumerate(sorted_by_period):
                    task.priority = len(sorted_by_period) - i

                # Create resource constraints from session state
                session_resources = st.session_state.get('resources', [])
                resource_constraints = create_resource_constraints(session_resources, periodic_tasks)
                resource_protocol = map_protocol_name(st.session_state.get('resource_protocol', 'None'))

            # Check if we should run simulation
            run_sim = run_button or st.session_state.get('trigger_simulation', False)
            if run_sim:
                if 'trigger_simulation' in st.session_state:
                    del st.session_state['trigger_simulation']

                # Show resource protocol info if enabled
                if enable_resources and resource_constraints:
                    protocol_display = st.session_state.get('resource_protocol', 'None')
                    st.info(f"🔒 Resource Protocol: {protocol_display} | {len(resource_constraints)} resource(s) configured")

                # Select scheduler based on algorithm category
                overload_config = st.session_state.get('overload_config', {})

                # Validate task types match algorithm requirements
                if algorithm_category in ["Basic Algorithms", "Precedence-Constrained", "Overload Handling"]:
                    if aperiodic_tasks and not periodic_tasks:
                        st.error(f"⚠️ {algorithm_category} requires periodic tasks. Add periodic tasks to continue.")
                    elif aperiodic_tasks:
                        st.info(f"ℹ️ {len(aperiodic_tasks)} aperiodic task(s) will be ignored by {algorithm_category}")
                elif algorithm_category == "Server-Based (Combined)":
                    if not periodic_tasks:
                        st.warning("⚠️ Add periodic tasks for background workload")
                    if not aperiodic_tasks:
                        st.warning("⚠️ Add aperiodic tasks for foreground workload")
                elif algorithm_category == "Aperiodic Scheduling":
                    if not aperiodic_tasks and not periodic_tasks:
                        st.error("⚠️ Add tasks to simulate")
                    elif not aperiodic_tasks and periodic_tasks:
                        st.info(f"ℹ️ No aperiodic tasks. Using {len(periodic_tasks)} periodic task(s) with EDF+HVDF")

                if algorithm_category == "Aperiodic Scheduling":
                    if "EDF+HVDF" in algorithm:
                        if aperiodic_tasks:
                            if periodic_tasks:
                                st.info(f"Using {len(aperiodic_tasks)} aperiodic task(s). {len(periodic_tasks)} periodic task(s) not used by EDF+HVDF.")
                            scheduler = EDFHVDFScheduler(aperiodic_tasks, duration)
                        elif periodic_tasks:
                            st.info(f"No aperiodic tasks found. Using {len(periodic_tasks)} periodic task(s) with EDF+HVDF periodic mode.")
                            scheduler = EDFHVDFPeriodicScheduler(periodic_tasks, duration)
                        else:
                            st.error("No tasks to simulate")
                            scheduler = RMSScheduler([], duration)
                    elif "HVDF Only" in algorithm:
                        if aperiodic_tasks:
                            if periodic_tasks:
                                st.info(f"Using {len(aperiodic_tasks)} aperiodic task(s). {len(periodic_tasks)} periodic task(s) not used by HVDF Only.")
                            scheduler = HVDFOnlyScheduler(aperiodic_tasks, duration)
                        else:
                            st.error("HVDF Only requires aperiodic tasks. Please add aperiodic tasks (type='aperiodic').")
                            scheduler = RMSScheduler([], duration)
                    else:
                        scheduler = RMSScheduler(periodic_tasks if periodic_tasks else [], duration)
                elif algorithm_category == "Overload Handling":
                    if "FC-EDF" in algorithm:
                        # FC-EDF uses EDF with admission control (config available in overload_config)
                        scheduler = EDFScheduler(periodic_tasks, duration)
                    elif "Feedback (m,k)-RMS" in algorithm:
                        from scheduler.core.task import MkFirmTask
                        from scheduler.core.algorithms.feedback_mk_rms import FeedbackMkFirmScheduler
                        mk_tasks = [MkFirmTask(id=t.id, computation_time=t.computation_time, period=t.period, deadline=t.deadline, m=1, k=1) for t in periodic_tasks]
                        # Use user-configured overload parameters
                        scheduler = FeedbackMkFirmScheduler(
                            mk_tasks,
                            target_dfr=overload_config.get('target_dfr', 0.05),
                            kp=overload_config.get('kp', 0.1),
                            ki=overload_config.get('ki', 0.01),
                            kd=overload_config.get('kd', 0.05),
                            duration=duration
                        )
                    elif "Imprecise Computation" in algorithm:
                        from scheduler.core.task import ImpreciseTask
                        from scheduler.core.algorithms.overload import ImpreciseComputationScheduler
                        # Create imprecise tasks from session state data
                        imprecise_tasks = []
                        for task_data in st.session_state.get('tasks', []):
                            if task_data.get('type', 'periodic') == 'periodic':
                                mand = task_data.get('mandatory_time', task_data.get('computation_time', 1.0))
                                opt = task_data.get('optional_time', 0.0)
                                # ImpreciseTask doesn't have period - only id, mandatory_time, optional_time, deadline
                                imprecise_tasks.append(ImpreciseTask(
                                    id=task_data.get('id', 'T1'),
                                    mandatory_time=mand,
                                    optional_time=opt,
                                    deadline=task_data.get('deadline', 10.0)
                                ))
                        if imprecise_tasks:
                            scheduler = ImpreciseComputationScheduler(periodic_tasks, imprecise_tasks, duration)
                        else:
                            st.warning("No imprecise tasks configured. Using RMS scheduler.")
                            scheduler = RMSScheduler(periodic_tasks, duration)
                    elif "HVDF (Value-Based)" in algorithm:
                        from scheduler.core.algorithms.overload import HVDFScheduler
                        # Extract task values from periodic tasks
                        task_values = {t.id: t.value for t in periodic_tasks}
                        if any(v > 0 for v in task_values.values()):
                            scheduler = HVDFScheduler(periodic_tasks, task_values, duration)
                        else:
                            st.warning("No task values configured. Using RMS scheduler. Add values in the 'Value' column.")
                            scheduler = RMSScheduler(periodic_tasks, duration)
                    elif "(m,k)-Firm Tasks" in algorithm:
                        from scheduler.core.task import MkFirmTask
                        from scheduler.core.algorithms.overload import MkFirmScheduler
                        # Parse mk_value from session state
                        mk_tasks = []
                        for task_data in st.session_state.get('tasks', []):
                            if task_data.get('type', 'periodic') == 'periodic':
                                mk_str = task_data.get('mk_value', '1,2')
                                try:
                                    parts = mk_str.split(',')
                                    m_val = int(parts[0].strip()) if len(parts) > 0 and parts[0].strip() else 1
                                    k_val = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip() else 2
                                except (ValueError, IndexError):
                                    m_val, k_val = 1, 2
                                comp_time = task_data.get('computation_time', 1.0)
                                # Default: split computation time equally if not specified
                                mk_tasks.append(MkFirmTask(
                                    id=task_data.get('id', 'T1'),
                                    computation_time=comp_time,
                                    period=task_data.get('period', 10.0),
                                    deadline=task_data.get('deadline', 10.0),
                                    mandatory_time=comp_time * 0.5,  # Default 50% mandatory
                                    critical_section_time=0.0,      # No critical section by default
                                    optional_time=comp_time * 0.5,  # Default 50% optional
                                    m=m_val,
                                    k=k_val
                                ))
                        if mk_tasks:
                            scheduler = MkFirmScheduler(periodic_tasks, mk_tasks, duration)
                        else:
                            st.warning("No (m,k)-firm tasks configured. Using RMS scheduler.")
                            scheduler = RMSScheduler(periodic_tasks, duration)
                    else:
                        scheduler = RMSScheduler(periodic_tasks, duration)
                elif algorithm_category == "Precedence-Constrained":
                    if enable_precedence and prec_objects:
                        if "RMS" in algorithm:
                            scheduler = RMSWithPrecedence(periodic_tasks, prec_objects, duration)
                        elif "EDF" in algorithm:
                            scheduler = EDFWithPrecedence(periodic_tasks, prec_objects, duration)
                        elif "DMS" in algorithm:
                            scheduler = DMSWithPrecedence(periodic_tasks, prec_objects, duration)
                        else:
                            scheduler = RMSScheduler(periodic_tasks, duration)
                    else:
                        if "RMS" in algorithm:
                            scheduler = RMSScheduler(periodic_tasks, duration)
                        elif "EDF" in algorithm:
                            scheduler = EDFScheduler(periodic_tasks, duration)
                        else:
                            scheduler = DMSScheduler(periodic_tasks, duration)
                elif algorithm_category == "Server-Based (Combined)":
                    server_cap = st.session_state.get('server_capacity', 2.0)
                    server_per = st.session_state.get('server_period', 5.0)
                    if not periodic_tasks or not aperiodic_tasks:
                        st.warning("Server-Based algorithms need both periodic and aperiodic tasks for optimal results")
                    if "Polling" in algorithm:
                        scheduler = PollingServerScheduler(periodic_tasks, aperiodic_tasks, server_cap, server_per, duration)
                    elif "Deferrable" in algorithm:
                        scheduler = DeferrableServerScheduler(periodic_tasks, aperiodic_tasks, server_cap, server_per, duration)
                    elif "Sporadic" in algorithm:
                        scheduler = SporadicServerScheduler(periodic_tasks, aperiodic_tasks, server_cap, server_per, duration)
                    elif "Background" in algorithm:
                        # Background Scheduler doesn't use server capacity/period
                        scheduler = BackgroundScheduler(periodic_tasks, aperiodic_tasks, duration)
                    else:
                        scheduler = PollingServerScheduler(periodic_tasks, aperiodic_tasks, server_cap, server_per, duration)
                elif algorithm.startswith("RMS"):
                    if enable_precedence and prec_objects:
                        scheduler = RMSWithPrecedence(periodic_tasks, prec_objects, duration)
                    elif enable_resources and resource_constraints:
                        scheduler = ResourceAwareRMSScheduler(periodic_tasks, duration, resource_constraints, resource_protocol)
                    else:
                        scheduler = RMSScheduler(periodic_tasks, duration)
                elif algorithm.startswith("EDF"):
                    if enable_precedence and prec_objects:
                        scheduler = EDFWithPrecedence(periodic_tasks, prec_objects, duration)
                    elif enable_resources and resource_constraints:
                        scheduler = ResourceAwareEDFScheduler(periodic_tasks, duration, resource_constraints, resource_protocol)
                    else:
                        scheduler = EDFScheduler(periodic_tasks, duration)
                elif algorithm.startswith("DMS"):
                    if enable_precedence and prec_objects:
                        scheduler = DMSWithPrecedence(periodic_tasks, prec_objects, duration)
                    elif enable_resources and resource_constraints:
                        scheduler = ResourceAwareDMSScheduler(periodic_tasks, duration, resource_constraints, resource_protocol)
                    else:
                        scheduler = DMSScheduler(periodic_tasks, duration)
                elif algorithm.startswith("LLF"):
                    if enable_resources and resource_constraints:
                        scheduler = ResourceAwareLLFScheduler(periodic_tasks, duration, resource_constraints, resource_protocol)
                    else:
                        scheduler = LLFScheduler(periodic_tasks, duration)
                else:
                    if enable_resources and resource_constraints:
                        scheduler = ResourceAwareRMSScheduler(periodic_tasks, duration, resource_constraints, resource_protocol)
                    else:
                        scheduler = RMSScheduler(periodic_tasks, duration)

                # Run simulation and store in session state
                result = scheduler.simulate()
                st.session_state.simulation_result = result
                st.session_state.simulation_scheduler = scheduler
                st.session_state.simulation_duration = duration
                st.session_state.simulation_algorithm = algorithm
                st.session_state.periodic_tasks = periodic_tasks
                st.session_state.aperiodic_tasks = aperiodic_tasks
                st.session_state.precedence_constraints = precedence_constraints if enable_precedence else []

        except Exception as e:
            st.session_state.simulation_error = str(e)

    # ========== RIGHT PANEL: RESULTS WITH TABS ==========
    with results_col:
        result = st.session_state.get('simulation_result')
        scheduler = st.session_state.get('simulation_scheduler')
        sim_duration = st.session_state.get('simulation_duration', duration)
        sim_algorithm = st.session_state.get('simulation_algorithm', algorithm)

        if result:
            # Key metrics bar (always visible)
            m1, m2, m3 = st.columns(3)
            m1.metric("CPU", f"{result.cpu_utilization:.1f}%")
            m2.metric("Misses", len(result.deadline_misses))
            m3.metric("Switches", result.total_context_switches)

            if result.deadline_misses:
                st.warning(f"{len(result.deadline_misses)} deadline miss(es)")
            else:
                st.success("All deadlines met")

            # Tabbed visualizations
            tab_gantt, tab_metrics, tab_timeline, tab_analysis, tab_export = st.tabs(
                ["Gantt", "Metrics", "Timeline", "Analysis", "Export"]
            )

            with tab_gantt:
                fig = create_gantt_chart(result, max_time=sim_duration)
                st.plotly_chart(fig, width='stretch')

            with tab_metrics:
                metrics_fig = create_metrics_dashboard(result)
                st.plotly_chart(metrics_fig, width='stretch')

                # Priority timeline for dynamic algorithms
                if any(x in sim_algorithm for x in ["EDF", "LLF", "DMS"]):
                    try:
                        priority_fig = create_priority_timeline(result, max_time=sim_duration)
                        st.plotly_chart(priority_fig, width='stretch')
                    except:
                        pass

            with tab_timeline:
                # Step-by-Step Viewer as main component
                timeline_summary = create_timeline_summary(result)
                step = st.slider("Step through timeline", 0, max(0, timeline_summary['total_events'] - 1), 0,
                                help="Use slider or arrow keys to step through events")
                viewer_data = create_timeline_step_viewer(result, current_step=step)
                if viewer_data['figure']:
                    st.plotly_chart(viewer_data['figure'], width='stretch')
                    st.caption(viewer_data['explanation'])

            with tab_analysis:
                # Schedulability Analysis section
                periodic_tasks = st.session_state.get('periodic_tasks', [])
                if periodic_tasks:
                    st.subheader("Schedulability Analysis")

                    # Detect algorithm type and run appropriate analysis
                    try:
                        if "RMS" in sim_algorithm or "Rate Monotonic" in sim_algorithm:
                            # RMS Analysis
                            analysis = SchedulabilityAnalyzer.analyze_rms(periodic_tasks)
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Utilization", f"{analysis['utilization_test']['utilization']:.1%}")
                            with col2:
                                st.metric("RMS Bound", f"{analysis['utilization_test']['bound']:.1%}")
                            with col3:
                                is_sched = analysis['final_result']
                                st.metric("Schedulable", "Yes" if is_sched else "No")

                            st.info(analysis['utilization_test']['explanation'])
                            if analysis['is_harmonic']:
                                st.success(analysis['harmonic_check'])

                        elif "EDF" in sim_algorithm and "HVDF" not in sim_algorithm:
                            # EDF Analysis
                            schedulable, util, explanation = SchedulabilityAnalyzer.edf_utilization_test(periodic_tasks)
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Utilization", f"{util:.1%}")
                            with col2:
                                st.metric("EDF Bound", "100%")
                            with col3:
                                st.metric("Schedulable", "Yes" if schedulable else "No")
                            st.info(explanation)

                        elif "DMS" in sim_algorithm or "Deadline Monotonic" in sim_algorithm:
                            # DMS Analysis
                            schedulable, util, bound, explanation = SchedulabilityAnalyzer.dms_utilization_test(periodic_tasks)
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Utilization", f"{util:.1%}")
                            with col2:
                                st.metric("DMS Bound", f"{bound:.1%}")
                            with col3:
                                st.metric("Schedulable", "Yes" if schedulable else "No")
                            st.info(explanation)

                        elif "LLF" in sim_algorithm:
                            # LLF uses EDF bound
                            schedulable, util, explanation = SchedulabilityAnalyzer.edf_utilization_test(periodic_tasks)
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Utilization", f"{util:.1%}")
                            with col2:
                                st.metric("LLF Bound", "100%")
                            with col3:
                                st.metric("Schedulable", "Yes" if schedulable else "No")
                            st.info(f"LLF (like EDF): {explanation}")

                        else:
                            # Generic analysis
                            total_util = sum(t.utilization for t in periodic_tasks)
                            st.metric("Total Utilization", f"{total_util:.1%}")
                    except Exception as e:
                        st.warning(f"Schedulability analysis unavailable: {e}")

                    # Task Statistics
                    st.subheader("Task Statistics")
                    task_stats = []
                    for task in periodic_tasks:
                        task_stats.append({
                            'Task': task.id,
                            'C': task.computation_time,
                            'P': task.period,
                            'D': task.deadline,
                            'U': f"{task.utilization:.1%}",
                            'Priority': getattr(task, 'priority', '-')
                        })
                    if task_stats:
                        st.dataframe(pd.DataFrame(task_stats), width='stretch', hide_index=True)

                # Value analysis for HVDF
                if hasattr(scheduler, 'calculate_total_value') or "HVDF" in sim_algorithm:
                    try:
                        st.subheader("Value Analysis")
                        total_value = scheduler.calculate_total_value()
                        st.metric("Total Value", f"{total_value:.2f}")
                        if hasattr(scheduler, 'get_value_breakdown'):
                            breakdown = scheduler.get_value_breakdown()
                            value_data = [
                                {'Task': f"{item['task_id']}[{item['instance']}]",
                                 'Completed': f"{item['completion_time']:.2f}",
                                 'Deadline': f"{item['deadline']:.2f}",
                                 'Status': 'Met' if item['met_deadline'] else 'MISSED',
                                 'Value': f"{item['value']:.2f}"}
                                for item in breakdown
                            ]
                            if value_data:
                                st.dataframe(pd.DataFrame(value_data), width='stretch', hide_index=True)
                    except:
                        pass

                # Precedence graph
                prec_constraints = st.session_state.get('precedence_constraints', [])
                if prec_constraints:
                    try:
                        st.subheader("Precedence Graph")
                        p_tasks = st.session_state.get('periodic_tasks', [])
                        prec_fig = create_precedence_graph(prec_constraints, p_tasks)
                        st.plotly_chart(prec_fig, width='stretch')
                    except:
                        pass

                # Server analysis for server-based algorithms
                if "Server" in sim_algorithm or "Polling" in sim_algorithm or "Deferrable" in sim_algorithm or "Sporadic" in sim_algorithm:
                    st.subheader("Server Analysis")
                    aperiodic_completed = getattr(scheduler, 'aperiodic_completed', [])
                    st.metric("Aperiodic Tasks Completed", len(aperiodic_completed))
                    if result.response_times:
                        st.write("**Response Times:**")
                        rt_data = [{'Task': k, 'Response Time': f"{v:.1f}"} for k, v in result.response_times.items()]
                        st.dataframe(pd.DataFrame(rt_data), width='stretch', hide_index=True)

            with tab_export:
                # Timeline events table
                st.subheader("Timeline Events")
                timeline_df = pd.DataFrame([
                    {'Time': e.time, 'Task': e.task_id or 'IDLE', 'Event': e.event_type,
                     'Details': str(e.details) if e.details else ''}
                    for e in result.events[:200]
                ])
                st.dataframe(timeline_df, height=350, width='stretch', hide_index=True)

                # Download buttons
                st.subheader("Download Data")
                csv = timeline_df.to_csv(index=False)
                st.download_button(
                    "Download Timeline (CSV)",
                    data=csv,
                    file_name=f"schedule_{sim_algorithm.replace(' ', '_')}.csv",
                    mime="text/csv"
                )
                st.caption("To export Gantt chart as PNG, click the camera icon on the chart")

        else:
            # Placeholder when no results
            st.info("Configure tasks and click **Run** to see results")
            st.caption("Results will appear here with Gantt chart, metrics, and timeline")

        # Show error if any
        if st.session_state.get('simulation_error'):
            st.error(f"Error: {st.session_state.simulation_error}")


if __name__ == "__main__":
    main()

