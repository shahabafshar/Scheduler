"""Preset task configurations from documentation."""

from scheduler.core.task import PeriodicTask, AperiodicTask

# RMS Example 1: T1=(2,4), T2=(1,8) - Schedulable (U=0.625)
RMS_EXAMPLE_1 = [
    PeriodicTask(id="T1", computation_time=2.0, period=4.0, deadline=4.0),
    PeriodicTask(id="T2", computation_time=1.0, period=8.0, deadline=8.0)
]

# RMS Example 2: Needs completion time test
RMS_EXAMPLE_2 = [
    PeriodicTask(id="T1", computation_time=2.0, period=4.0, deadline=4.0),
    PeriodicTask(id="T2", computation_time=4.0, period=8.0, deadline=8.0)
]

# RMS Example 3: Larger task set
RMS_EXAMPLE_3 = [
    PeriodicTask(id="T1", computation_time=2.0, period=8.0, deadline=8.0),
    PeriodicTask(id="T2", computation_time=4.0, period=12.0, deadline=12.0),
    PeriodicTask(id="T3", computation_time=2.0, period=6.0, deadline=6.0)
]

# EDF Example: Can achieve 100% utilization
EDF_EXAMPLE = [
    PeriodicTask(id="T1", computation_time=1.0, period=3.0, deadline=3.0),
    PeriodicTask(id="T2", computation_time=4.0, period=6.0, deadline=6.0)
]

# DMS Example with different deadlines
DMS_EXAMPLE = [
    PeriodicTask(id="T1", computation_time=3.0, period=20.0, deadline=7.0),
    PeriodicTask(id="T2", computation_time=2.0, period=5.0, deadline=4.0),
    PeriodicTask(id="T3", computation_time=2.0, period=10.0, deadline=9.0)
]

# Completion Time Test Example
COMPLETION_TIME_TEST = [
    PeriodicTask(id="T1", computation_time=20.0, period=100.0, deadline=100.0),
    PeriodicTask(id="T2", computation_time=30.0, period=145.0, deadline=145.0),
    PeriodicTask(id="T3", computation_time=68.0, period=150.0, deadline=150.0)
]

# Harmonic Task Set Example (all periods are multiples)
HARMONIC_EXAMPLE = [
    PeriodicTask(id="T1", computation_time=1.0, period=4.0, deadline=4.0),
    PeriodicTask(id="T2", computation_time=2.0, period=8.0, deadline=8.0),
    PeriodicTask(id="T3", computation_time=3.0, period=16.0, deadline=16.0)
]

# High Utilization Example (near 100%)
HIGH_UTILIZATION = [
    PeriodicTask(id="T1", computation_time=4.0, period=5.0, deadline=5.0),
    PeriodicTask(id="T2", computation_time=3.0, period=6.0, deadline=6.0),
    PeriodicTask(id="T3", computation_time=2.0, period=10.0, deadline=10.0)
]

# Overload Example (will miss deadlines)
OVERLOAD_EXAMPLE = [
    PeriodicTask(id="T1", computation_time=6.0, period=7.0, deadline=7.0),
    PeriodicTask(id="T2", computation_time=4.0, period=5.0, deadline=5.0)
]

# EDF+HVDF Example (Exam Question): T1=(C=3,D=8,V=3), T2=(C=1,D=4,V=1), T3=(C=1,D=4,V=2), T4=(C=2,D=6,V=3)
EDF_HVDF_EXAMPLE = [
    AperiodicTask(id="T1", arrival_time=0, computation_time=3, deadline=8, value=3, preemptive=False),
    AperiodicTask(id="T2", arrival_time=0, computation_time=1, deadline=4, value=1, preemptive=False),
    AperiodicTask(id="T3", arrival_time=0, computation_time=1, deadline=4, value=2, preemptive=False),
    AperiodicTask(id="T4", arrival_time=0, computation_time=2, deadline=6, value=3, preemptive=False),
]

# ============== LLF Examples ==============
LLF_EXAMPLE = [
    PeriodicTask(id="T1", computation_time=1.0, period=4.0, deadline=4.0),
    PeriodicTask(id="T2", computation_time=2.0, period=6.0, deadline=6.0),
    PeriodicTask(id="T3", computation_time=1.0, period=8.0, deadline=8.0)
]

LLF_TIGHT_DEADLINES = [
    PeriodicTask(id="T1", computation_time=2.0, period=5.0, deadline=3.0),
    PeriodicTask(id="T2", computation_time=1.0, period=4.0, deadline=2.0),
]

# ============== Server-Based Examples (Periodic + Aperiodic) ==============
# Server example: Background periodic tasks + foreground aperiodic requests
SERVER_PERIODIC_TASKS = [
    PeriodicTask(id="P1", computation_time=2.0, period=10.0, deadline=10.0),
    PeriodicTask(id="P2", computation_time=1.0, period=8.0, deadline=8.0),
]

SERVER_APERIODIC_TASKS = [
    AperiodicTask(id="A1", arrival_time=3, computation_time=2, deadline=20, value=1),
    AperiodicTask(id="A2", arrival_time=8, computation_time=1, deadline=25, value=2),
    AperiodicTask(id="A3", arrival_time=15, computation_time=2, deadline=35, value=1),
]

# Combined for Server-Based presets
SERVER_EXAMPLE_1 = {
    "periodic": SERVER_PERIODIC_TASKS,
    "aperiodic": SERVER_APERIODIC_TASKS,
    "server_capacity": 2.0,
    "server_period": 5.0
}

SERVER_HEAVY_LOAD = {
    "periodic": [
        PeriodicTask(id="P1", computation_time=3.0, period=8.0, deadline=8.0),
        PeriodicTask(id="P2", computation_time=2.0, period=10.0, deadline=10.0),
        PeriodicTask(id="P3", computation_time=1.0, period=6.0, deadline=6.0),
    ],
    "aperiodic": [
        AperiodicTask(id="A1", arrival_time=2, computation_time=3, deadline=15, value=3),
        AperiodicTask(id="A2", arrival_time=10, computation_time=2, deadline=25, value=2),
        AperiodicTask(id="A3", arrival_time=20, computation_time=4, deadline=40, value=4),
        AperiodicTask(id="A4", arrival_time=30, computation_time=1, deadline=45, value=1),
    ],
    "server_capacity": 3.0,
    "server_period": 8.0
}

# Server Capacity Demo: Large aperiodic tasks that clearly show Cs/Ps effects
# With Cs=2, Ps=5: A1 completes ~t=17 (needs 4 replenishments)
# With Cs=4, Ps=5: A1 completes ~t=9 (needs 2 replenishments)
# With Cs=8, Ps=5: A1 completes ~t=8 (needs 1 replenishment)
SERVER_CAPACITY_DEMO = {
    "periodic": [
        PeriodicTask(id="P1", computation_time=1.0, period=10.0, deadline=10.0),
        PeriodicTask(id="P2", computation_time=1.0, period=15.0, deadline=15.0),
    ],
    "aperiodic": [
        AperiodicTask(id="A1", arrival_time=0, computation_time=8, deadline=50, value=10),
        AperiodicTask(id="A2", arrival_time=12, computation_time=6, deadline=60, value=8),
        AperiodicTask(id="A3", arrival_time=25, computation_time=4, deadline=70, value=6),
    ],
    "server_capacity": 2.0,
    "server_period": 5.0
}

# ============== Precedence-Constrained Examples ==============
# Tasks with dependencies: T1 -> T2 -> T3 (chain)
PRECEDENCE_CHAIN = [
    PeriodicTask(id="T1", computation_time=1.0, period=12.0, deadline=12.0),
    PeriodicTask(id="T2", computation_time=2.0, period=12.0, deadline=12.0),
    PeriodicTask(id="T3", computation_time=1.0, period=12.0, deadline=12.0),
]
PRECEDENCE_CHAIN_CONSTRAINTS = "T1 -> T2\nT2 -> T3"

# Fork pattern: T1 -> T2, T1 -> T3
PRECEDENCE_FORK = [
    PeriodicTask(id="T1", computation_time=2.0, period=15.0, deadline=15.0),
    PeriodicTask(id="T2", computation_time=1.0, period=15.0, deadline=15.0),
    PeriodicTask(id="T3", computation_time=1.0, period=15.0, deadline=15.0),
    PeriodicTask(id="T4", computation_time=2.0, period=10.0, deadline=10.0),  # Independent
]
PRECEDENCE_FORK_CONSTRAINTS = "T1 -> T2\nT1 -> T3"

# Diamond pattern: T1 -> T2, T1 -> T3, T2 -> T4, T3 -> T4
PRECEDENCE_DIAMOND = [
    PeriodicTask(id="T1", computation_time=1.0, period=20.0, deadline=20.0),
    PeriodicTask(id="T2", computation_time=2.0, period=20.0, deadline=20.0),
    PeriodicTask(id="T3", computation_time=2.0, period=20.0, deadline=20.0),
    PeriodicTask(id="T4", computation_time=1.0, period=20.0, deadline=20.0),
]
PRECEDENCE_DIAMOND_CONSTRAINTS = "T1 -> T2\nT1 -> T3\nT2 -> T4\nT3 -> T4"

# ============== More Aperiodic Examples ==============
APERIODIC_STAGGERED = [
    AperiodicTask(id="J1", arrival_time=0, computation_time=2, deadline=5, value=2, preemptive=True),
    AperiodicTask(id="J2", arrival_time=3, computation_time=1, deadline=8, value=3, preemptive=True),
    AperiodicTask(id="J3", arrival_time=5, computation_time=3, deadline=12, value=1, preemptive=True),
    AperiodicTask(id="J4", arrival_time=8, computation_time=2, deadline=15, value=4, preemptive=True),
]

APERIODIC_BURST = [
    AperiodicTask(id="J1", arrival_time=0, computation_time=1, deadline=6, value=1, preemptive=False),
    AperiodicTask(id="J2", arrival_time=0, computation_time=2, deadline=8, value=2, preemptive=False),
    AperiodicTask(id="J3", arrival_time=0, computation_time=1, deadline=4, value=3, preemptive=False),
    AperiodicTask(id="J4", arrival_time=0, computation_time=3, deadline=10, value=2, preemptive=False),
    AperiodicTask(id="J5", arrival_time=0, computation_time=1, deadline=5, value=4, preemptive=False),
]

# ============== More Overload Examples ==============
OVERLOAD_GRADUAL = [
    PeriodicTask(id="T1", computation_time=3.0, period=5.0, deadline=5.0),
    PeriodicTask(id="T2", computation_time=2.0, period=4.0, deadline=4.0),
    PeriodicTask(id="T3", computation_time=2.0, period=6.0, deadline=6.0),
]

# ============== Structured Preset Data ==============
# Each preset has: tasks, category, algorithm, description, and optional config
PRESET_CATALOG = {
    # ===== BASIC ALGORITHMS =====
    "basic_rms_1": {
        "name": "Schedulable Task Set",
        "category": "Basic Algorithms",
        "algorithm": "RMS (Rate Monotonic)",
        "tasks": RMS_EXAMPLE_1,
        "description": "Two tasks with U=62.5%, well within RMS bound",
        "utilization": "62.5%"
    },
    "basic_rms_2": {
        "name": "Exact Test Required",
        "category": "Basic Algorithms",
        "algorithm": "RMS (Rate Monotonic)",
        "tasks": RMS_EXAMPLE_2,
        "description": "Exceeds Liu-Layland bound but passes exact test",
        "utilization": "100%"
    },
    "basic_rms_3": {
        "name": "Three Task Set",
        "category": "Basic Algorithms",
        "algorithm": "RMS (Rate Monotonic)",
        "tasks": RMS_EXAMPLE_3,
        "description": "Three periodic tasks for RMS analysis",
        "utilization": "86%"
    },
    "basic_rms_harmonic": {
        "name": "Harmonic Periods",
        "category": "Basic Algorithms",
        "algorithm": "RMS (Rate Monotonic)",
        "tasks": HARMONIC_EXAMPLE,
        "description": "Harmonic periods (4,8,16) allow 100% utilization",
        "utilization": "68.75%"
    },
    "basic_rms_completion": {
        "name": "Completion Time Analysis",
        "category": "Basic Algorithms",
        "algorithm": "RMS (Rate Monotonic)",
        "tasks": COMPLETION_TIME_TEST,
        "description": "Large task set for response time analysis",
        "utilization": "79%"
    },
    "basic_edf_full": {
        "name": "Full Utilization",
        "category": "Basic Algorithms",
        "algorithm": "EDF (Earliest Deadline First)",
        "tasks": EDF_EXAMPLE,
        "description": "EDF can schedule at 100% utilization",
        "utilization": "100%"
    },
    "basic_edf_stress": {
        "name": "High Load Stress Test",
        "category": "Basic Algorithms",
        "algorithm": "EDF (Earliest Deadline First)",
        "tasks": HIGH_UTILIZATION,
        "description": "Near-maximum utilization stress test",
        "utilization": ">90%"
    },
    "basic_dms_1": {
        "name": "D < P Deadlines",
        "category": "Basic Algorithms",
        "algorithm": "DMS (Deadline Monotonic)",
        "tasks": DMS_EXAMPLE,
        "description": "Tasks where deadline differs from period",
        "utilization": "75%"
    },
    "basic_llf_1": {
        "name": "Basic LLF Example",
        "category": "Basic Algorithms",
        "algorithm": "LLF (Least Laxity First)",
        "tasks": LLF_EXAMPLE,
        "description": "Laxity-based dynamic scheduling",
        "utilization": "70%"
    },
    "basic_llf_tight": {
        "name": "Tight Deadlines",
        "category": "Basic Algorithms",
        "algorithm": "LLF (Least Laxity First)",
        "tasks": LLF_TIGHT_DEADLINES,
        "description": "Tasks with tight deadline constraints (D < P)",
        "utilization": "65%"
    },

    # ===== SERVER-BASED =====
    "server_polling_1": {
        "name": "Basic Polling Server",
        "category": "Server-Based (Combined)",
        "algorithm": "Polling Server",
        "tasks": SERVER_EXAMPLE_1,
        "description": "Periodic background + aperiodic foreground tasks",
        "config": {"server_capacity": 2.0, "server_period": 5.0}
    },
    "server_deferrable_1": {
        "name": "Deferrable Server",
        "category": "Server-Based (Combined)",
        "algorithm": "Deferrable Server",
        "tasks": SERVER_EXAMPLE_1,
        "description": "Capacity preserved when no aperiodic tasks",
        "config": {"server_capacity": 2.0, "server_period": 5.0}
    },
    "server_sporadic_1": {
        "name": "Sporadic Server",
        "category": "Server-Based (Combined)",
        "algorithm": "Sporadic Server",
        "tasks": SERVER_EXAMPLE_1,
        "description": "Best response time for aperiodic tasks",
        "config": {"server_capacity": 2.0, "server_period": 5.0}
    },
    "server_heavy": {
        "name": "Heavy Load Mixed Workload",
        "category": "Server-Based (Combined)",
        "algorithm": "Polling Server",
        "tasks": SERVER_HEAVY_LOAD,
        "description": "High load periodic + frequent aperiodic arrivals",
        "config": {"server_capacity": 3.0, "server_period": 8.0}
    },
    "server_background": {
        "name": "Background Scheduler (Baseline)",
        "category": "Server-Based (Combined)",
        "algorithm": "Background Scheduler",
        "tasks": SERVER_EXAMPLE_1,
        "description": "Aperiodic tasks execute only during CPU idle time (worst-case baseline)"
    },
    "server_capacity_demo": {
        "name": "⭐ Server Capacity Demo",
        "category": "Server-Based (Combined)",
        "algorithm": "Polling Server",
        "tasks": SERVER_CAPACITY_DEMO,
        "description": "Large aperiodic tasks (C=8,6,4) - TRY: Cs=2 vs Cs=4 vs Cs=8 to see completion time differences",
        "config": {"server_capacity": 2.0, "server_period": 5.0}
    },

    # ===== PRECEDENCE-CONSTRAINED =====
    "prec_rms_chain": {
        "name": "Chain Dependencies",
        "category": "Precedence-Constrained",
        "algorithm": "RMS with Precedence",
        "tasks": PRECEDENCE_CHAIN,
        "description": "Linear chain: T1 -> T2 -> T3",
        "precedence": PRECEDENCE_CHAIN_CONSTRAINTS
    },
    "prec_edf_fork": {
        "name": "Fork Pattern",
        "category": "Precedence-Constrained",
        "algorithm": "EDF with Precedence",
        "tasks": PRECEDENCE_FORK,
        "description": "Fork: T1 -> {T2, T3}, T4 independent",
        "precedence": PRECEDENCE_FORK_CONSTRAINTS
    },
    "prec_dms_diamond": {
        "name": "Diamond Pattern",
        "category": "Precedence-Constrained",
        "algorithm": "DMS with Precedence",
        "tasks": PRECEDENCE_DIAMOND,
        "description": "Diamond: T1 -> {T2,T3} -> T4",
        "precedence": PRECEDENCE_DIAMOND_CONSTRAINTS
    },

    # ===== OVERLOAD HANDLING =====
    "overload_miss": {
        "name": "Deadline Miss Scenario",
        "category": "Overload Handling",
        "algorithm": "FC-EDF (Feedback Control)",
        "tasks": OVERLOAD_EXAMPLE,
        "description": "Utilization > 100%, guaranteed misses",
        "utilization": ">140%"
    },
    "overload_gradual": {
        "name": "Gradual Overload",
        "category": "Overload Handling",
        "algorithm": "FC-EDF (Feedback Control)",
        "tasks": OVERLOAD_GRADUAL,
        "description": "Multiple tasks causing cumulative overload",
        "utilization": ">110%"
    },

    # ===== APERIODIC SCHEDULING =====
    "aperiodic_hvdf_exam": {
        "name": "Exam: Value Maximization",
        "category": "Aperiodic Scheduling",
        "algorithm": "EDF+HVDF (Value-Based)",
        "tasks": EDF_HVDF_EXAMPLE,
        "description": "Classic exam problem, optimal value = 9",
        "expected_value": 9
    },
    "aperiodic_staggered": {
        "name": "Staggered Arrivals",
        "category": "Aperiodic Scheduling",
        "algorithm": "EDF+HVDF (Value-Based)",
        "tasks": APERIODIC_STAGGERED,
        "description": "Jobs arriving at different times",
        "expected_value": 10
    },
    "aperiodic_burst": {
        "name": "Burst Arrivals",
        "category": "Aperiodic Scheduling",
        "algorithm": "EDF+HVDF (Value-Based)",
        "tasks": APERIODIC_BURST,
        "description": "All jobs arrive at t=0, non-preemptive",
        "expected_value": 12
    },
}

# Legacy PRESETS dict for backward compatibility
PRESETS = {
    # Basic Algorithms - RMS
    "[Basic|RMS] Example 1 - Schedulable (U=62.5%)": RMS_EXAMPLE_1,
    "[Basic|RMS] Example 2 - Exact Test Required": RMS_EXAMPLE_2,
    "[Basic|RMS] Example 3 - Three Tasks": RMS_EXAMPLE_3,
    "[Basic|RMS] Harmonic Periods - 100% Bound": HARMONIC_EXAMPLE,
    "[Basic|RMS] Completion Time Analysis": COMPLETION_TIME_TEST,
    # Basic Algorithms - EDF
    "[Basic|EDF] Full Utilization (U=100%)": EDF_EXAMPLE,
    "[Basic|EDF] High Load Stress Test (U>90%)": HIGH_UTILIZATION,
    # Basic Algorithms - DMS
    "[Basic|DMS] D < P Deadlines": DMS_EXAMPLE,
    # Basic Algorithms - LLF
    "[Basic|LLF] Basic LLF Example": LLF_EXAMPLE,
    "[Basic|LLF] Tight Deadlines (D < P)": LLF_TIGHT_DEADLINES,
    # Overload Handling
    "[Overload] Deadline Miss Scenario (U>100%)": OVERLOAD_EXAMPLE,
    "[Overload] Gradual Overload": OVERLOAD_GRADUAL,
    # Aperiodic Scheduling
    "[Aperiodic|HVDF] Exam: Value Maximization (V=9)": EDF_HVDF_EXAMPLE,
    "[Aperiodic|HVDF] Staggered Arrivals": APERIODIC_STAGGERED,
    "[Aperiodic|HVDF] Burst Arrivals (t=0)": APERIODIC_BURST,
}

