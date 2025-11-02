# CprE 458/558: Real-Time Systems
## Term Project Proposal

---

## Title of the Project

**Comprehensive Real-Time Scheduling Simulator with Interactive Visualization and Multi-Algorithm Performance Analysis**

---

## Team Member(s)

**[Your Name]**
**ISU Email:** [your-email@iastate.edu]
**Course Number:** CprE 458 (or 558)
**Section:** [Your Section]

**Team Size:** 1 member

---

## Project Type

**Type 1: GUI Simulator Tool**

An interactive web-based application providing visual input/output for real-time scheduling algorithms with comprehensive performance metrics and educational visualization capabilities.

**Justification for Type 1:**
- Enables hands-on exploration of scheduling concepts through immediate visual feedback
- Provides an educational tool for understanding complex real-time scheduling behaviors
- Delivers practical utility for schedulability analysis and algorithm comparison
- Allows systematic performance evaluation through configurable test cases and metrics

---

## Project Objectives

### Primary Focus Areas

**1. Algorithm-Related (Core Focus):**
- Implement and compare fundamental real-time scheduling algorithms (RMS, EDF, DMS, LLF)
- Integrate server-based scheduling mechanisms for mixed periodic/aperiodic workloads (Polling Server, Deferrable Server, Sporadic Server)
- Demonstrate value-based scheduling with HVDF (Highest Value Density First) for resource-constrained systems
- Support precedence-constrained scheduling variants

**2. OS-Related (Secondary Focus):**
- Visualize priority inversion scenarios and resource access control protocols
- Demonstrate preemption, context switching, and task lifecycle management
- Model critical section behavior and resource contention

**3. Architecture-Related (Tertiary Focus):**
- Provide extensible framework for adding new scheduling policies through composable priority policy architecture
- Support schedulability analysis using theoretical bounds (RMS utilization test, EDF optimality test, completion time analysis)

### Specific Project Goals

1. **Multi-Algorithm Implementation:** Develop a unified simulation engine supporting 7+ distinct scheduling algorithms with identical task sets for direct comparison

2. **Interactive Visualization:** Create rich visual representations including:
   - Interactive Gantt charts showing task execution timelines
   - Real-time metrics dashboards (CPU utilization, deadline misses, context switches)
   - Priority change visualization for dynamic priority algorithms
   - Precedence constraint graphs

3. **Schedulability Analysis:** Integrate analytical tools for pre-runtime schedulability verification using established theoretical tests

4. **Educational Value:** Design intuitive interface requiring no programming knowledge, with preset configurations from course examples for immediate experimentation

5. **Performance Evaluation:** Enable systematic comparison of algorithm behavior under varied workloads (harmonic vs. non-harmonic periods, overload conditions, different utilization levels)

---

## Solution Approach

### Algorithms and Techniques

#### 1. Basic Fixed-Priority Scheduling
- **Rate Monotonic Scheduling (RMS):** Period-based priority assignment (shorter period = higher priority)
- **Deadline Monotonic Scheduling (DMS):** Deadline-based priority assignment for tasks where D ≤ P
- **Utilization Test:** n(2^(1/n) - 1) bound for RMS schedulability analysis

#### 2. Dynamic Priority Scheduling
- **Earliest Deadline First (EDF):** Dynamic priority based on absolute deadlines (earliest deadline = highest priority)
- **Least Laxity First (LLF):** Dynamic priority based on slack time (laxity = deadline - current_time - remaining_execution_time)
- **Utilization Test:** U ≤ 1.0 necessary and sufficient condition for EDF

#### 3. Server-Based Combined Scheduling
- **Polling Server:** Periodic server for handling aperiodic tasks with bandwidth preservation
- **Deferrable Server:** Preserves unused server capacity until next period for improved aperiodic response time
- **Sporadic Server:** Dynamic replenishment strategy maintaining schedulability guarantees

#### 4. Value-Based Scheduling (Extended)
- **EDF+HVDF:** Combined scheduling using deadline as primary criterion and value density (value/computation_time) as tie-breaker
- **Composable Priority Policies:** Framework enabling arbitrary algorithm combinations (e.g., RMS+HVDF, DMS+HVDF)

#### 5. Advanced Features (Stretch Goals)
- **Precedence-Constrained Scheduling:** RMS/EDF/DMS variants respecting task dependencies
- **Resource Access Control:** Priority Inheritance Protocol (PIP) and Priority Ceiling Protocol (PCP) for demonstrating priority inversion and deadlock avoidance
- **(m,k)-Firm Scheduling:** Overload handling using weakly-hard real-time constraints
- **Feedback Control EDF:** Adaptive scheduling under dynamic workload conditions

### Technical Implementation Strategy

#### Core Architecture: Template Method Pattern
```
SchedulerBase (Abstract Base Class)
├── simulate() - Complete simulation loop (implemented)
├── assign_priorities() - Abstract method (algorithm-specific)
└── get_next_task() - Abstract method (algorithm-specific)

Concrete Schedulers inherit and implement only priority logic
```

**Benefits:**
- Code reuse: Simulation loop written once, used by all algorithms
- Consistency: Identical event handling, deadline checking, and metrics calculation
- Extensibility: New algorithms require only 2 methods (~30-50 lines)

#### Composable Priority Policy Framework
Implemented using Strategy Pattern to eliminate code duplication:
- `RMSPolicy`, `EDFPolicy`, `LLFPolicy`, `HVDFPolicy` - Individual strategies
- `CompositePriorityPolicy` - Combines primary + secondary policies
- Enables RMS+HVDF, EDF+HVDF combinations with **zero code duplication**

#### Task Models (Dataclass-Based)
- `PeriodicTask`: (period, computation_time, deadline, priority, value)
- `AperiodicTask`: (arrival_time, computation_time, deadline, value)
- `ImpreciseTask`: (mandatory_time, optional_time) for QoS management
- `MkFirmTask`: (m, k) constraints for weakly-hard deadlines
- `PrecedenceConstraint`: Task dependency specifications
- `ResourceConstraint`: Critical section and resource access definitions

#### Schedulability Analysis Toolkit
- **RMS Analysis:** Liu & Layland utilization bound with harmonic period detection (100% utilization possible)
- **EDF Analysis:** Total utilization test (U ≤ 1.0)
- **Completion Time Test:** Exact schedulability analysis for fixed-priority systems
- **Visual Feedback:** Clear indication of schedulability with utilization percentage and theoretical bounds

#### Visualization Layer (Plotly-Based)
- **Interactive Gantt Charts:** Hover details, color-coded tasks, preemption markers
- **Metrics Dashboard:** CPU utilization timeline, event distribution pie charts, context switch visualization
- **Priority Timeline:** Shows priority changes over time for dynamic algorithms
- **Event Log:** Detailed timeline table (arrivals, starts, preemptions, completions, deadline misses)

### Development Platform
- **Language:** Python 3.10+ (type hints, dataclasses)
- **GUI Framework:** Streamlit (web-based, responsive, no frontend coding required)
- **Visualization:** Plotly (interactive charts), Matplotlib (supplementary)
- **Data Handling:** Pandas (task input tables), NumPy (numerical computations)

### Software Engineering Practices
- **Separation of Concerns:** Algorithm, analysis, and visualization modules are independent
- **Event-Driven Simulation:** Complete execution trace stored as event timeline
- **Modular Design:** Each scheduler is self-contained; visualizations work with any ScheduleResult
- **Type Safety:** Full type annotations for maintainability

---

## Expected Outcomes

### 1. Deliverable: Web-Based GUI Tool

**Functional Capabilities:**
- Algorithm selection dropdown with 5 categories:
  - Basic Algorithms (RMS, EDF, DMS, LLF)
  - Server-Based Combined Scheduling (Polling, Deferrable, Sporadic)
  - Precedence-Constrained (RMS/EDF/DMS with dependencies)
  - Overload Handling (HVDF, (m,k)-firm, Feedback EDF)
  - Aperiodic Scheduling (EDF+HVDF)

- Task definition interface:
  - Interactive table editor for task parameters
  - Support for periodic and aperiodic task types
  - 10+ preset configurations from course examples and exam questions

- Real-time schedulability analysis:
  - Pre-simulation verification with theoretical bounds
  - Harmonic period detection and warnings
  - Utilization breakdown by task

- Execution simulation:
  - Discrete-time simulation with configurable duration
  - Automatic task instance generation based on periods
  - Preemption and deadline miss detection

- Rich visualization suite:
  - Interactive Gantt chart (zoom, pan, hover for details)
  - 4-panel metrics dashboard (CPU utilization over time, event distribution, context switches, per-task utilization)
  - Priority timeline for dynamic priority algorithms
  - Service level plots for (m,k)-firm tasks
  - Precedence dependency graphs

- Export capabilities:
  - CSV download of complete event timeline
  - Schedulability analysis reports

**User Experience:**
- Zero programming knowledge required
- Immediate visual feedback (results appear within seconds)
- Educational tooltips and explanations
- Error handling and input validation

### 2. Performance Evaluation Metrics

**Quantitative Metrics:**
- **CPU Utilization (%):** Percentage of time CPU is executing tasks (target: match theoretical utilization)
- **Deadline Miss Count:** Number of task instances missing deadlines (target: 0 for schedulable sets)
- **Deadline Miss Rate (%):** Percentage of task instances missing deadlines
- **Context Switches:** Number of preemptions (comparison metric between algorithms)
- **Average Response Time:** For aperiodic tasks (server-based scheduling comparison)
- **Total Value Achieved:** Sum of values for completed tasks (HVDF evaluation)
- **Service Level:** For (m,k)-firm tasks, percentage of windows meeting m-out-of-k constraint

**Qualitative Metrics:**
- **Schedulability Verification:** Comparison of simulation results vs. theoretical predictions
- **Algorithm Behavior:** Visual patterns in Gantt charts (e.g., EDF "pushing deadlines," RMS fixed ordering)
- **Priority Inversion Duration:** For resource access control protocols (if implemented)

### 3. Test Cases and Validation Strategy

**Test Case Categories:**

**A. Baseline Schedulability Tests**
1. **RMS Example 1:** T1=(2,4), T2=(1,8)
   - Expected: Schedulable (U=65%), 0 deadline misses
   - Validates: Basic RMS implementation, utilization calculation

2. **EDF Example 1:** T1=(3,6,6), T2=(2,8,8), T3=(2,12,12)
   - Expected: Schedulable (U=87.5%), 0 deadline misses
   - Validates: EDF dynamic priority, high utilization handling

3. **Harmonic Task Set:** T1=(1,4), T2=(1,8), T3=(1,16)
   - Expected: Schedulable at U=87.5% (RMS bound relaxed for harmonic periods)
   - Validates: Harmonic period detection logic

**B. Deadline Miss Scenarios**
4. **Overloaded RMS:** U > RMS bound
   - Expected: Deadline misses for lowest priority tasks
   - Validates: Deadline detection, priority ordering

5. **Overloaded EDF:** U > 100%
   - Expected: Deadline misses (domino effect)
   - Validates: EDF overload behavior

**C. Algorithm Comparison Tests**
6. **RMS vs. EDF:** Same task set (U=85%)
   - Expected: EDF succeeds, RMS may fail (below 69% bound for 3 tasks)
   - Validates: Relative performance of fixed vs. dynamic priority

7. **LLF Behavior:** Task set with tight laxity margins
   - Expected: Frequent priority changes, many context switches
   - Validates: Laxity calculation, dynamic priority updates

**D. Server-Based Scheduling Tests**
8. **Polling Server:** Periodic tasks + aperiodic server
   - Expected: Aperiodic tasks serviced at server periods
   - Validates: Server capacity management, aperiodic response time

9. **Deferrable vs. Polling:** Same workload
   - Expected: Deferrable achieves lower aperiodic response time
   - Validates: Capacity preservation logic

**E. Value-Based Scheduling Tests**
10. **EDF+HVDF:** Aperiodic tasks with different values
    - Expected: Higher value density tasks complete first among equal deadlines
    - Validates: Composite priority policy, value tracking

**F. Advanced Features (Stretch Goals)**
11. **Precedence Constraints:** Tasks with dependencies
    - Expected: Predecessors complete before successors
    - Validates: Precedence checking in ready queue

12. **Priority Inheritance:** Resource sharing with potential priority inversion
    - Expected: PIP prevents unbounded priority inversion
    - Validates: Resource protocols, priority boosting

**Validation Methodology:**
- **Automated Testing:** Python test scripts verify expected metrics for each test case
- **Visual Inspection:** Gantt charts reviewed for correct execution ordering
- **Documentation Cross-Reference:** Results compared against course lecture examples and textbook scenarios
- **Boundary Testing:** Edge cases (U=100%, single task, very short/long periods)

### 4. Documentation and Educational Materials

**User Documentation:**
- Quick start guide with screenshots
- Algorithm descriptions with complexity analysis
- Preset configuration explanations
- Troubleshooting guide

**Technical Documentation:**
- Architecture overview (Template Method pattern, Priority Policy framework)
- API documentation for extensibility
- Code comments explaining scheduling logic
- Refactoring roadmap (current: Phase 1 complete, flexibility score 60/100)

---

## Description of Expected Outcomes

### Minimum Viable Product (Core Scope for 1-Member Team)

**Must-Have Features:**
1. ✅ Implementation of 4 basic algorithms (RMS, EDF, DMS, LLF)
2. ✅ Web-based GUI with task input and algorithm selection
3. ✅ Interactive Gantt chart visualization
4. ✅ Schedulability analysis for RMS and EDF
5. ✅ Metrics dashboard with CPU utilization and deadline misses
6. ✅ 5+ preset test cases from course materials
7. ✅ CSV export functionality
8. ✅ Validation against textbook examples

**Evaluation Criteria for MVP:**
- All 4 algorithms produce correct schedules for standard test cases
- Gantt charts accurately reflect task execution timeline
- Utilization calculations match theoretical values
- GUI is responsive and intuitive
- Test cases reproduce expected behavior from course lectures

### Extended Features (Demonstration of Enhanced Scope)

**Should-Have Features (Already Implemented):**
1. ✅ Server-based scheduling (3 algorithms: Polling, Deferrable, Sporadic)
2. ✅ Value-based scheduling (EDF+HVDF for aperiodic and periodic tasks)
3. ✅ Composable priority policy framework (Phase 1 refactoring)
4. ✅ Advanced metrics (context switches, event distribution, per-task utilization)
5. ✅ 10 preset configurations including exam questions

**Could-Have Features (Code Complete, UI Integration Pending):**
1. ✅ Precedence-constrained scheduling (RMS/EDF/DMS variants)
2. ✅ Resource access protocols (PIP, PCP implementations exist)
3. ✅ Overload handling ((m,k)-firm scheduler, Feedback EDF)
4. ✅ Additional task types (ImpreciseTask, MkFirmTask)

**Future Extensions (Stretch Goals Beyond Proposal Scope):**
1. ⚠️ Unified scheduler supporting mixed periodic + aperiodic workloads (Phase 3 refactoring)
2. ⚠️ Multiprocessor scheduling (partitioned or global scheduling)
3. ⚠️ Energy-aware scheduling (DVS techniques)
4. ⚠️ Real-time network scheduling (CAN bus simulation)
5. ⚠️ Integration with FreeRTOS or VxWorks for hardware validation

### Success Metrics

**Technical Success:**
- ✅ All implemented algorithms pass validation test suite
- ✅ Simulation results match analytical predictions for schedulable task sets
- ✅ GUI handles edge cases gracefully (empty task sets, invalid inputs)
- ✅ Performance is acceptable (simulation completes in <5 seconds for duration=100)

**Educational Success:**
- ✅ Tool enables exploration of concepts covered in CprE 458/558 lectures
- ✅ Visual feedback aids understanding of algorithm differences
- ✅ Preset configurations allow immediate experimentation
- ✅ Documentation is clear and comprehensive

**Project Scope Calibration:**
- **Core Features (MVP):** Appropriate for 1-member team, achievable within semester timeline
- **Extended Features:** Demonstrate ambition and depth, show progress beyond minimum requirements
- **Future Extensions:** Acknowledge broader context and potential for continued development

### Deliverables Summary

1. **Source Code:** Modular Python codebase (~3000+ lines) with type annotations
2. **Web Application:** Deployed Streamlit app accessible via browser
3. **Test Suite:** 7+ test scripts validating individual algorithms and components
4. **Documentation:** README, architecture guide, user manual, API documentation
5. **Preset Configurations:** 10+ verified test cases from course materials
6. **Final Report:** Comprehensive analysis of implementation, results, and evaluation
7. **Presentation:** Slides and live demo of key features

---

## List of References

### Foundational Textbooks

1. **Liu, J. W. S.** (2000). *Real-Time Systems*. Prentice Hall.
   - Chapters 4-7: Task scheduling (RMS, EDF, DMS, LLF)
   - Chapter 8: Resource access control (PIP, PCP)
   - Chapter 9: Server-based scheduling (Polling, Deferrable, Sporadic)

2. **Buttazzo, G. C.** (2011). *Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications* (3rd ed.). Springer.
   - Chapter 4: Periodic task scheduling
   - Chapter 5: Fixed priority servers
   - Chapter 6: Resource access protocols
   - Chapter 9: Overload handling techniques

3. **Burns, A., & Wellings, A.** (2009). *Real-Time Systems and Programming Languages* (4th ed.). Addison-Wesley.
   - Chapter 10: Scheduling real-time systems
   - Chapter 11: Schedulability analysis

### Course Materials

4. **Manimaran, G.** (2024). *CprE 458/558: Real-Time Systems - Lecture Notes*. Iowa State University.
   - Lecture 3-4: RMS and EDF scheduling
   - Lecture 5: Deadline Monotonic Scheduling
   - Lecture 6: Server-based scheduling (Polling, Deferrable, Sporadic)
   - Lecture 7-8: Resource access protocols
   - Lecture 9-10: Overload handling and (m,k)-firm scheduling
   - Lecture 11: Precedence-constrained scheduling

### Research Papers (Value-Based and Advanced Scheduling)

5. **Buttazzo, G., & Stankovic, J.** (1993). "RED: Robust Earliest Deadline scheduling." *Proceedings of the Third International Workshop on Responsive Computing Systems*, pp. 100-111.
   - HVDF algorithm for value-based scheduling

6. **Hamdaoui, M., & Ramanathan, P.** (1995). "A dynamic priority assignment technique for streams with (m, k)-firm deadlines." *IEEE Transactions on Computers*, 44(12), 1443-1451.
   - (m,k)-firm real-time constraints and DBP algorithm

7. **Lu, C., Stankovic, J. A., Abdelzaher, T. F., Tao, G., & Son, S. H.** (2002). "Feedback control real-time scheduling: Framework, modeling, and algorithms." *Real-Time Systems*, 23(1-2), 85-126.
   - Feedback control EDF for adaptive scheduling

8. **Sprunt, B., Sha, L., & Lehoczky, J.** (1989). "Aperiodic task scheduling for hard-real-time systems." *Real-Time Systems*, 1(1), 27-60.
   - Sporadic Server algorithm and analysis

### Resource Access Control Protocols

9. **Sha, L., Rajkumar, R., & Lehoczky, J. P.** (1990). "Priority inheritance protocols: An approach to real-time synchronization." *IEEE Transactions on Computers*, 39(9), 1175-1185.
   - Original Priority Inheritance Protocol paper

10. **Rajkumar, R.** (1991). *Synchronization in Real-Time Systems: A Priority Inheritance Approach*. Kluwer Academic Publishers.
    - Priority Ceiling Protocol and Priority Ceiling Emulation

### Implementation and Tools

11. **Barry, R.** (2016). *Mastering the FreeRTOS Real Time Kernel - A Hands-On Tutorial Guide*. Real Time Engineers Ltd.
    - Reference for potential RTOS integration (stretch goal)

12. **VxWorks Documentation** (Wind River Systems). *Programmer's Guide*.
    - Alternative RTOS platform reference (stretch goal)

### Online Resources and Documentation

13. **Python Streamlit Documentation**. https://docs.streamlit.io/
    - GUI framework reference

14. **Plotly Python Documentation**. https://plotly.com/python/
    - Interactive visualization library

15. **Real-Time Systems Research Group, Iowa State University**. Course materials and supplementary readings.

---

## Project Timeline (Proposed)

### Weeks 1-3: Foundation (COMPLETED)
- ✅ Core architecture (SchedulerBase with Template Method pattern)
- ✅ Task data models (PeriodicTask, AperiodicTask, etc.)
- ✅ Basic algorithms (RMS, EDF, DMS, LLF)
- ✅ Schedulability analysis module
- ✅ Initial GUI with Streamlit

### Weeks 4-6: Visualization & Testing (COMPLETED)
- ✅ Interactive Gantt chart implementation
- ✅ Metrics dashboard (4 panels)
- ✅ Preset configurations from course examples
- ✅ Validation test suite
- ✅ CSV export functionality

### Weeks 7-9: Advanced Features (COMPLETED)
- ✅ Server-based scheduling (Polling, Deferrable, Sporadic)
- ✅ Value-based scheduling (EDF+HVDF variants)
- ✅ Priority policy framework (Phase 1 refactoring)
- ✅ Additional visualizations (priority timeline, service level plots)

### Weeks 10-12: Extended Implementation (IN PROGRESS)
- ✅ Precedence-constrained scheduling (code complete)
- ✅ Resource access protocols (PIP/PCP code complete)
- ⚠️ UI integration for advanced features (partial)
- ⚠️ Comprehensive testing and bug fixes

### Weeks 13-14: Documentation & Polish (PLANNED)
- 📝 Final report preparation
- 📝 User documentation and tutorial
- 📝 Code cleanup and commenting
- 📝 Presentation slide development

### Week 15: Final Presentation & Submission
- 📊 Live demo preparation
- 📊 Final testing and validation
- 📊 Submission of final report and code

---

## Alignment with Course Objectives

This project directly addresses multiple learning objectives from CprE 458/558:

1. **Understanding Scheduling Algorithms:** Hands-on implementation of RMS, EDF, DMS, LLF, and server-based algorithms reinforces theoretical concepts through practical application.

2. **Schedulability Analysis:** Integration of utilization tests and completion time analysis demonstrates mastery of analytical techniques.

3. **Resource Management:** Implementation of critical section tracking and resource protocols (PIP/PCP) illustrates OS-level resource access control.

4. **Performance Evaluation:** Systematic testing and metrics collection enable quantitative comparison of algorithm behavior under varied workloads.

5. **Real-World Application:** GUI tool has practical utility for schedulability verification in embedded systems design, bridging academic concepts and industry practice.

---

## Conclusion

This project proposes a **comprehensive real-time scheduling simulator** that serves both as an educational tool and a practical schedulability analysis platform. The **Type 1 GUI approach** enables immediate visual feedback and interactive exploration of scheduling concepts, making it ideal for learning and experimentation.

The **1-member team scope** is calibrated to deliver a robust core implementation (4 basic algorithms, full visualization suite, schedulability analysis) while demonstrating extended capability through additional features (server-based scheduling, value-based scheduling, composable priority policies). This represents a substantial but achievable scope appropriate for a semester-long term project.

The project's **modular architecture** (Template Method pattern, Strategy pattern for priorities, event-driven simulation) ensures maintainability and extensibility, with clear pathways for future enhancements (unified scheduler, multiprocessor scheduling, hardware integration) that acknowledge the broader context of real-time systems research.

**Current Status:** The project has already made significant progress with core features implemented and validated. The proposal formalizes this work within the academic framework and establishes clear evaluation criteria for successful completion.

---

**Prepared by:** [Your Name]
**Date:** [Current Date]
**Course:** CprE 458/558: Real-Time Systems
**Instructor:** Dr. G. Manimaran
