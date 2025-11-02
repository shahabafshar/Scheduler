# CprE 558: Real-Time Systems
## Term Project Proposal

---

## Title of the Project

**Performance Evaluation of Server-Based Scheduling Algorithms for Mixed Periodic-Aperiodic Real-Time Workloads**

---

## Team Member(s)

**Name:** Shahab Afshar
**ISU Email:** safshar@iastate.edu
**Course Number:** CprE 5580
**Section:** Online

**Team Size:** 1 member

---

## Project Type

**Type 3: Simulation (Performance) Study**

This project involves implementing server-based scheduling algorithms from seminal research papers, developing a discrete-event simulator, and conducting systematic performance evaluation under varying workload conditions. The project includes independent reading of multiple research papers and industry-recognized algorithms to understand their theoretical foundations and implementation details.

---

## Project Objectives

### Primary Focus: Algorithm-Related and OS-Related

This project addresses the fundamental challenge of **mixed workload scheduling** in real-time systems, where both periodic tasks (with regular deadlines) and aperiodic tasks (with sporadic arrivals) must coexist while meeting timing constraints.

**Core Objectives:**

1. **Algorithm Implementation from Research Literature**
   Implement 6-7 server-based scheduling algorithms directly from their original research papers, including:
   - Polling Server
   - Deferrable Server
   - Sporadic Server
   - Priority Exchange Server
   - Total Bandwidth Server (TBS)
   - Slack Stealer
   - Background Scheduler (baseline)

2. **Systematic Performance Evaluation**
   Conduct comprehensive comparative analysis measuring:
   - Aperiodic task response time (average and worst-case)
   - Periodic task schedulability preservation
   - Server capacity utilization efficiency
   - Behavior under overload conditions

3. **Theoretical Validation**
   Compare simulation results against theoretical predictions from research papers to validate implementation correctness and understand practical performance limits.

4. **OS-Level Resource Management**
   Demonstrate how servers act as resource abstraction mechanisms, allowing operating systems to manage mixed workloads within fixed-priority scheduling frameworks (specifically RMS-based systems).

### Research Questions

- How do different server mechanisms trade off between aperiodic response time and periodic task schedulability?
- Under what workload conditions does each server type perform optimally?
- How close do simulation results match theoretical worst-case bounds?
- What is the practical impact of server capacity on system behavior?

---

## Solution Approach

### Algorithms and Protocols

The project implements seven server-based scheduling algorithms, each representing a distinct approach to mixed workload management:

#### 1. Polling Server
**Reference:** Lehoczky et al. (1987)
**Mechanism:** Periodic server checks for aperiodic tasks at fixed intervals. If no aperiodic tasks are ready, capacity is **lost** (non-bandwidth-preserving).
**Priority Assignment:** Server treated as high-priority periodic task under RMS.
**Key Characteristic:** Simple but inefficient capacity utilization.

#### 2. Deferrable Server
**Reference:** Lehoczky, Rajkumar, Sha (1987)
**Mechanism:** Server capacity is **preserved** when no aperiodic tasks are available, allowing deferred use within the same period.
**Replenishment:** Capacity fully replenished at start of each server period.
**Key Characteristic:** Better aperiodic response time than Polling, but can cause priority inversion.

#### 3. Sporadic Server
**Reference:** Sprunt, Sha, Lehoczky (1989) - *IEEE Real-Time Systems Symposium*
**Mechanism:** **Dynamic replenishment** - capacity is replenished at time T_consume + P_server (one period after consumption starts).
**Schedulability:** Maintains RMS schedulability guarantees (server treated like periodic task).
**Key Characteristic:** Best aperiodic response time among periodic-server approaches.

#### 4. Priority Exchange Server
**Reference:** Lehoczky, Rajkumar, Sha (1987)
**Mechanism:** When no aperiodic tasks available, server **exchanges priority** with highest-priority ready periodic task, allowing periodic task to use server capacity.
**Key Characteristic:** Improved CPU utilization by avoiding idle capacity.

#### 5. Total Bandwidth Server (TBS)
**Reference:** Spuri & Buttazzo (1996) - *IEEE Transactions on Computers*
**Mechanism:** Each aperiodic task assigned a dynamic deadline: d_i = max(r_i, d_{i-1}) + C_i/U_s, where U_s is server utilization.
**Scheduling:** Uses EDF for both periodic and aperiodic tasks.
**Key Characteristic:** Optimal for EDF-based systems, guarantees server bandwidth.

#### 6. Slack Stealer
**Reference:** Lehoczky & Ramos-Thuel (1992) - *Real-Time Systems Journal*
**Mechanism:** Computes available **slack time** (spare CPU capacity) dynamically and uses it for aperiodic tasks without affecting periodic schedulability.
**Complexity:** Higher runtime overhead due to slack computation at each scheduling point.
**Key Characteristic:** Exploits all available slack, achieves best possible aperiodic response time.

#### 7. Background Scheduler (Baseline)
**Reference:** Standard technique (Liu 2000, *Real-Time Systems*)
**Mechanism:** Aperiodic tasks execute only during **idle time** when no periodic tasks are ready.
**Key Characteristic:** Worst aperiodic response time, used as baseline comparison.

---

### Technical Implementation Strategy

#### Discrete-Event Simulation Framework

**Simulation Model:**
- Time-driven discrete-event simulation with unit time steps
- Event types: task arrival, task start, task preemption, task completion, deadline miss
- Ready queue management with priority-based selection

**Task Models:**
- **PeriodicTask:** (id, period, computation_time, deadline, priority)
- **AperiodicTask:** (id, arrival_time, computation_time, deadline, value)
- **Server:** Modeled as special periodic task with capacity management logic

**Server Implementation Pattern:**
Each server inherits from base scheduler and implements two key methods:
1. `should_replenish_server(time)` - Determines capacity replenishment timing
2. `get_next_task(ready_queue)` - Selects periodic or aperiodic task based on server capacity

**Schedulability Analysis:**
- RMS utilization test: U ≤ n(2^(1/n) - 1)
- Server treated as periodic task with U_server = C_server / P_server
- Combined utilization: U_periodic + U_server ≤ schedulability bound

---

### Development Platform and Tools

**Language:** Python 3.10+
**Simulation Engine:** Custom discrete-event simulator with object-oriented design
**Visualization:** Plotly (interactive Gantt charts), Matplotlib (statistical plots)
**Data Analysis:** Pandas (metrics aggregation), NumPy (statistical computations)
**Architecture:** Abstract base class pattern with concrete server implementations

---

## Expected Outcomes

### 1. Deliverable: Functional Simulator

**Core Capabilities:**
- Configurable task set definition (periodic + aperiodic)
- Server parameter configuration (capacity, period, priority)
- Algorithm selection (7 server types)
- Simulation execution with complete event logging
- Real-time visualization of execution timeline

**Technical Outputs:**
- Event timeline with microsecond-level detail
- Task execution Gantt charts
- Priority assignment visualization
- Server capacity usage tracking

### 2. Performance Evaluation Results

**Experimental Design:**

**Independent Variables:**
- Server capacity: {10%, 20%, 30%, 40%} of CPU bandwidth
- Server period: {5, 10, 20} time units
- Aperiodic arrival rate: {low: λ=0.1, medium: λ=0.3, high: λ=0.5, bursty: Poisson}
- Periodic task utilization: {50%, 70%, 85%}

**Dependent Variables (Metrics):**
- **Average Aperiodic Response Time:** Mean time from arrival to completion
- **Worst-Case Aperiodic Response Time:** 95th percentile response time
- **Periodic Deadline Miss Rate:** Percentage of periodic task deadlines missed
- **Server Utilization Efficiency:** Actual capacity used / Available capacity
- **Context Switches:** Number of task preemptions (overhead indicator)

**Test Scenarios:**

**Scenario 1: Baseline Comparison**
- Fixed workload: 3 periodic tasks (U=60%), 10 aperiodic tasks
- Server capacity: 20%, Period: 10
- Compare all 7 algorithms
- **Expected:** Sporadic < Deferrable < Polling < Background (response time ordering)

**Scenario 2: Capacity Sensitivity**
- Vary server capacity from 10% to 40%
- Fixed arrival rate (λ=0.3)
- Measure response time vs. capacity tradeoff
- **Expected:** Diminishing returns beyond schedulability limit

**Scenario 3: Overload Behavior**
- Total utilization > 100% (U_periodic + U_aperiodic > 1.0)
- Measure graceful degradation
- **Expected:** Sporadic maintains periodic schedulability longest

**Scenario 4: Bursty Arrivals**
- Poisson arrival process with varying λ
- Stress-test server responsiveness
- **Expected:** Slack Stealer performs best, Background worst

**Scenario 5: Server Period Impact**
- Fixed capacity (20%), vary period {5, 10, 20}
- Measure response time sensitivity
- **Expected:** Shorter period → better response time, higher overhead

### 3. Validation Against Theory

**Theoretical Bounds to Verify:**

**Sporadic Server:**
- Schedulability: Server with (C_s, P_s) treated as periodic task → U_total ≤ n(2^(1/n)-1)
- Response time: Should match worst-case analysis from Sprunt et al. paper

**Deferrable Server:**
- Known to violate standard RMS bounds (requires modified analysis)
- Verify against Lehoczky's correction factors

**Total Bandwidth Server:**
- With EDF: Should be schedulable if U_periodic + U_server ≤ 1.0
- Deadline assignment formula: d_i = max(r_i, d_{i-1}) + C_i/U_s

**Validation Method:**
- Generate task sets at known utilization levels
- Compare simulation deadline miss rate vs. theoretical schedulability
- Plot simulation response time vs. worst-case analytical bounds

### 4. Comparative Analysis

**Deliverable Visualizations:**
- Response time comparison (bar chart: all 7 algorithms)
- Capacity utilization efficiency (line plot: capacity % vs. utilization)
- Schedulability regions (2D plot: periodic U vs. server U, showing schedulable/unschedulable boundaries)
- Overload behavior (time series: deadline misses over time)

**Statistical Analysis:**
- Mean and standard deviation for all metrics
- 95% confidence intervals
- ANOVA test for statistical significance of differences

### 5. Final Report Content

**Structure:**
1. Introduction and motivation
2. Background: Server-based scheduling concepts
3. Implementation details for each algorithm
4. Experimental methodology
5. Results and analysis
6. Comparison with theoretical predictions
7. Conclusions and insights

**Length:** 10-12 pages + appendices with code excerpts

---

## Description of Expected Outcomes

### Evaluation Metrics (Detailed)

**1. Aperiodic Response Time**
- **Definition:** R_i = C_i + W_i, where C_i is computation time, W_i is waiting time
- **Measurement:** Average over all aperiodic tasks, worst-case (95th percentile)
- **Target:** Sporadic < 2× Polling, Background > 5× Polling

**2. Periodic Schedulability Maintenance**
- **Definition:** Percentage of periodic task instances meeting deadlines
- **Target:** 100% for utilization below RMS bound, graceful degradation above
- **Verification:** Compare against Liu & Layland test

**3. Server Capacity Utilization**
- **Definition:** (Actual capacity consumed) / (Total capacity allocated)
- **Target:** Deferrable/Sporadic > 80%, Polling < 60% (due to capacity loss)

**4. Context Switch Overhead**
- **Definition:** Number of task preemptions during simulation
- **Impact:** Higher context switches → higher OS overhead
- **Comparison:** Slack Stealer likely highest (dynamic slack computation)

### Test Cases (Concrete Examples)

**Test Case 1: RMS Example with Polling Server**
```
Periodic Tasks:
  T1 = (C=2, P=5, D=5)   → U=0.40
  T2 = (C=3, P=10, D=10) → U=0.30
  Total U_periodic = 0.70

Polling Server:
  C_s = 2, P_s = 5 → U_server = 0.40
  Total U = 1.10 (overloaded!)

Aperiodic Tasks:
  A1 arrives at t=0, C=1
  A2 arrives at t=7, C=2

Expected Results:
  - Periodic tasks may miss deadlines (U > bound)
  - Aperiodic tasks served only at server periods (t=0, 5, 10, ...)
  - Polling loses capacity if no aperiodic tasks ready
```

**Validation:** Manually verify Gantt chart matches expected execution order.

**Test Case 2: Sporadic Server Under Utilization Limit**
```
Periodic Tasks: U_periodic = 0.60
Sporadic Server: U_server = 0.20 → Total U = 0.80 < 0.82 (RMS bound for 3 tasks)

Expected Results:
  - 100% periodic schedulability
  - Aperiodic tasks served with dynamic capacity replenishment
  - Response time < 50% of Background scheduler

Validation: Zero deadline misses, response time analysis from Sprunt paper.
```

**Test Case 3: Slack Stealer vs. Sporadic**
```
Same workload, compare:
  - Sporadic: Fixed capacity (e.g., 20%)
  - Slack Stealer: Uses all available slack (dynamic, unbounded)

Expected Results:
  - Slack Stealer: Lower response time (exploits all slack)
  - Slack Stealer: Higher computational overhead (slack calculation)

Validation: Slack Stealer never worse than Sporadic.
```

### Success Criteria

**Minimum Viable Product (Required):**
- ✅ 6 algorithms implemented and functional (all except Slack Stealer if time-constrained)
- ✅ 3+ test scenarios executed with complete data
- ✅ Response time and schedulability metrics for all algorithms
- ✅ At least 2 visualizations (Gantt chart + comparison plot)

**Complete Success (Target):**
- ✅ All 7 algorithms implemented
- ✅ 5 test scenarios with statistical analysis
- ✅ Validation against theoretical bounds
- ✅ Comprehensive final report with insights

**Exceptional Outcome (Stretch):**
- ✅ Sensitivity analysis (how do results change with parameter variations?)
- ✅ Hybrid server configurations (e.g., multiple servers with different priorities)
- ✅ Comparison with real-world RTOS behavior (FreeRTOS, VxWorks)

---

## List of References

### Foundational Research Papers

1. **Sprunt, B., Sha, L., & Lehoczky, J. P.** (1989). "Aperiodic task scheduling for hard-real-time systems." *Real-Time Systems*, 1(1), 27-60.
   → **Sporadic Server** - Seminal paper introducing dynamic replenishment

2. **Lehoczky, J. P., Sha, L., & Strosnider, J. K.** (1987). "Enhanced aperiodic responsiveness in hard real-time environments." *Proceedings of the IEEE Real-Time Systems Symposium*, pp. 261-270.
   → **Deferrable Server and Priority Exchange Server**

3. **Spuri, M., & Buttazzo, G. C.** (1996). "Scheduling aperiodic tasks in dynamic priority systems." *Real-Time Systems*, 10(2), 179-210.
   → **Total Bandwidth Server** for EDF systems

4. **Lehoczky, J. P., & Ramos-Thuel, S.** (1992). "An optimal algorithm for scheduling soft-aperiodic tasks in fixed-priority preemptive systems." *Proceedings of IEEE Real-Time Systems Symposium*, pp. 110-123.
   → **Slack Stealing Algorithm**

5. **Liu, C. L., & Layland, J. W.** (1973). "Scheduling algorithms for multiprogramming in a hard-real-time environment." *Journal of the ACM*, 20(1), 46-61.
   → **RMS Foundations** - Original rate monotonic scheduling paper

### Textbooks and Comprehensive References

6. **Buttazzo, G. C.** (2011). *Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications* (3rd ed.). Springer.
   → Chapter 5: Fixed Priority Servers (comprehensive coverage of all server types)

7. **Liu, J. W. S.** (2000). *Real-Time Systems*. Prentice Hall.
   → Chapter 7: Scheduling Aperiodic and Sporadic Jobs in Priority-Driven Systems

8. **Burns, A., & Wellings, A.** (2009). *Real-Time Systems and Programming Languages* (4th ed.). Addison-Wesley.
   → Chapter 11: Scheduling Servers

### Course Materials

9. **Manimaran, G.** (2024). *CprE 458/558: Real-Time Systems - Lecture Notes*. Iowa State University.
   → Lecture 6: Combined Scheduling (Polling, Deferrable, Sporadic Servers)
   → Lecture 7: Advanced Server Mechanisms

### Supplementary References

10. **Rajkumar, R., Sha, L., & Lehoczky, J. P.** (1988). "Real-time synchronization protocols for multiprocessors." *Proceedings of the IEEE Real-Time Systems Symposium*, pp. 259-269.
    → Context for server behavior with resource sharing

11. **Stankovic, J. A., Spuri, M., Ramamritham, K., & Buttazzo, G. C.** (1998). *Deadline Scheduling for Real-Time Systems: EDF and Related Algorithms*. Kluwer Academic Publishers.
    → EDF-based servers (TBS) theoretical foundations

12. **Strosnider, J. K., Lehoczky, J. P., & Sha, L.** (1995). "The deferrable server algorithm for enhanced aperiodic responsiveness in hard real-time environments." *IEEE Transactions on Computers*, 44(1), 73-91.
    → Extended Deferrable Server analysis and proofs

---

## Project Timeline

**Total Duration:** 4 Weeks (One Month)

### Week 1: Foundation and Basic Servers
**Days 1-2:** Discrete-event simulation framework
- Task models (PeriodicTask, AperiodicTask)
- Base scheduler class with RMS priority assignment
- Event timeline generation
- Basic Gantt chart visualization

**Days 3-4:** Basic server implementations
- Polling Server (simplest, non-bandwidth-preserving)
- Background Scheduler (baseline for comparison)
- Initial testing with simple task sets

**Days 5-7:** Intermediate servers
- Deferrable Server (capacity preservation logic)
- Priority Exchange Server (priority swapping mechanism)
- Validation against lecture examples

**Deliverable:** 4 working server implementations, basic simulator framework

---

### Week 2: Advanced Servers and Algorithm Completion
**Days 8-10:** Advanced server implementations
- Sporadic Server (dynamic replenishment tracking)
- Total Bandwidth Server (EDF-based, dynamic deadline assignment)
- Complexity: Replenishment queue management

**Days 11-12:** Slack Stealer implementation
- Slack computation algorithm
- Dynamic slack tracking
- Integration with existing framework

**Days 13-14:** Testing and debugging
- Test all 7 algorithms with common task sets
- Verify correctness against paper examples
- Fix bugs and edge cases

**Deliverable:** All 7 server algorithms implemented and verified

---

### Week 3: Systematic Evaluation and Data Collection
**Days 15-16:** Experimental setup
- Design 5 test scenarios (baseline, capacity sensitivity, overload, bursty, period impact)
- Implement workload generators (Poisson arrivals, utilization control)
- Set up automated experiment runner

**Days 17-19:** Data collection
- Run all scenarios for all algorithms
- Collect metrics: response time, deadline misses, utilization, context switches
- Store results in structured format (CSV, Pandas DataFrames)

**Days 20-21:** Statistical analysis
- Compute means, standard deviations, confidence intervals
- Generate comparison tables
- Identify statistically significant differences

**Deliverable:** Complete dataset with metrics for all algorithms across all scenarios

---

### Week 4: Analysis, Visualization, and Reporting
**Days 22-23:** Visualization
- Response time comparison charts (bar plots, box plots)
- Capacity utilization plots (line graphs)
- Schedulability region visualization
- Gantt charts for representative scenarios

**Days 24-25:** Validation and interpretation
- Compare simulation results vs. theoretical bounds
- Analyze discrepancies and explain causes
- Draw insights about algorithm performance characteristics

**Days 26-27:** Report writing
- Introduction and background
- Implementation details
- Experimental methodology
- Results and analysis sections
- Conclusions

**Day 28:** Final polish
- Proofread report
- Finalize visualizations
- Prepare presentation slides
- Code cleanup and documentation

**Deliverable:** Final project report, presentation slides, complete codebase

---

## Risk Mitigation

**Potential Risks:**

1. **Implementation Complexity (Slack Stealer):**
   - Mitigation: Implement simpler version first, can be treated as "optional 7th algorithm"
   - Fallback: Focus on 6 algorithms if time-constrained

2. **Validation Difficulty:**
   - Mitigation: Use worked examples from papers and textbooks
   - Cross-check with lecture notes

3. **Time Constraints:**
   - Mitigation: Prioritize core 4 algorithms (Polling, Deferrable, Sporadic, Background)
   - Advanced algorithms (TBS, Slack Stealer) as stretch goals

---

## Alignment with CprE 558 Objectives

This project directly addresses graduate-level learning objectives:

1. **Research Paper Implementation:** Reading and implementing from original research publications (Type 3 requirement)
2. **Systematic Evaluation:** Rigorous experimental methodology with statistical validation
3. **Theoretical Validation:** Comparing simulation results against analytical models
4. **Algorithm Comparison:** Understanding trade-offs and applicability of different approaches
5. **OS Concepts:** Server abstraction, priority management, resource scheduling

The project demonstrates graduate-level understanding by not just implementing algorithms, but critically evaluating their performance, validating against theory, and drawing meaningful insights about practical applicability.

---

**Prepared by:** [Your Name]
**Date:** [Current Date]
**Course:** CprE 558: Real-Time Systems
**Instructor:** Dr. G. Manimaran
**Project Type:** Type 3 - Simulation (Performance) Study
