# CprE 558: Real-Time Systems - Term Project Proposal

---

**Title:** Performance Evaluation of Server-Based Scheduling Algorithms for Mixed Periodic-Aperiodic Real-Time Workloads

**Student:** Shahab Afshar
**Email:** safshar@iastate.edu
**Course:** CprE 558 - Real-Time Systems
**Section:** Online
**Team Size:** 1 member
**Project Type:** Type 3 - Simulation (Performance) Study

---

## Project Objectives

This project implements and evaluates six server-based scheduling algorithms for mixed periodic-aperiodic real-time workloads. Objectives include:

1. **Implementation:** Implement Polling Server, Deferrable Server, Sporadic Server, Priority Exchange Server, Total Bandwidth Server, and Background Scheduler from research literature [1-3].

2. **Performance Evaluation:** Conduct systematic comparative analysis using deterministic benchmarks and randomly generated task sets via UUniFast algorithm [4], measuring aperiodic response time, deadline miss rates, and CPU utilization.

3. **Validation:** Verify implementation correctness against literature examples and analyze performance trends.

Research questions: (i) How do server mechanisms balance aperiodic responsiveness versus periodic schedulability? (ii) Under what utilization conditions does each algorithm perform optimally?

---

## Solution Approach

### Algorithms

Six server algorithms will be implemented, each using a different capacity management policy:

- **Polling Server** [2]: Checks for aperiodic tasks periodically; unused capacity is lost.
- **Deferrable Server** [2]: Preserves unused capacity within the same period.
- **Sporadic Server** [1]: Dynamic replenishment (capacity restored T_period after consumption).
- **Priority Exchange Server** [2]: Exchanges priority with periodic tasks when idle.
- **Total Bandwidth Server** [3]: EDF-based with dynamic deadline assignment (d_i = max(r_i, d_{i-1}) + C_i/U_s).
- **Background Scheduler**: Serves aperiodic tasks only during CPU idle time (baseline).

### Simulation Framework

A discrete-event simulator will be developed in Python using time-driven execution with logical time units. The simulator maintains ready queues, tracks task instances, generates event timelines, and computes performance metrics. Each server extends an abstract base class implementing priority assignment and task selection methods.

### Random Task Generation

Task sets will be generated using UUniFast algorithm [4], which distributes utilizations uniformly: u_i = sum_u × random()^(1/(n-i)) for i = 1..n-1. Periods are randomly selected from [10,100], and computation times computed as C_i = u_i × P_i.

---

## Evaluation Methodology

**Phase 1 - Validation:** 5-7 benchmark scenarios from [5-6] and course materials verify implementation correctness.

**Phase 2 - Systematic Evaluation:** For each utilization level U ∈ {50%, 65%, 80%, 95%}, 30 random task sets (n=5 tasks, periods in [10,100]) will be generated and simulated with all 6 algorithms, yielding 720 total simulations (30 × 4 × 6).

**Metrics:**
- Aperiodic response time (average, maximum)
- Periodic deadline miss rate
- CPU utilization
- Context switches

**Analysis:** Statistical summaries (mean, standard deviation, min, max) computed across 30 trials per utilization level. Comparative visualizations (box plots, response time curves) will reveal performance trends.

---

## Expected Outcomes

1. **Simulation tool** with 6 server implementations, response time calculation, and batch experiment capability
2. **Validation results** on 5-7 benchmarks demonstrating correctness
3. **Performance dataset** from 720 simulations exported as CSV
4. **Comparative analysis** with statistical tables and visualizations
5. **Technical report** (10-12 pages) documenting methodology, results, and conclusions

**Success Criteria:** Correct implementation (Phase 1 validation), reasonable performance trends consistent with algorithm theory, graduate-level analysis demonstrating understanding of real-time scheduling principles.

---

## Timeline

| Week | Tasks | Hours |
|------|-------|-------|
| 1 | Implement Total Bandwidth Server; validate using [3] examples | 6 |
| 2 | Build infrastructure: response time calculation, UUniFast generator, batch runner, CSV export | 10 |
| 3 | Execute validation (5-7 benchmarks) and systematic evaluation (720 simulations) | 6 |
| 4 | Statistical analysis, visualizations, report writing | 8 |

**Total:** 30 hours (7.5 hours/week)

---

## References

[1] B. Sprunt, L. Sha, and J. P. Lehoczky, "Aperiodic task scheduling for hard-real-time systems," *Real-Time Systems*, vol. 1, no. 1, pp. 27-60, 1989.

[2] J. P. Lehoczky, L. Sha, and J. K. Strosnider, "Enhanced aperiodic responsiveness in hard real-time environments," in *Proc. IEEE Real-Time Systems Symposium*, 1987, pp. 261-270.

[3] M. Spuri and G. C. Buttazzo, "Scheduling aperiodic tasks in dynamic priority systems," *Real-Time Systems*, vol. 10, no. 2, pp. 179-210, 1996.

[4] E. Bini and G. C. Buttazzo, "Measuring the performance of schedulability tests," *Real-Time Systems*, vol. 30, no. 1-2, pp. 129-154, 2005.

[5] C. L. Liu and J. W. Layland, "Scheduling algorithms for multiprogramming in a hard-real-time environment," *Journal of the ACM*, vol. 20, no. 1, pp. 46-61, 1973.

[6] G. C. Buttazzo, *Hard Real-Time Computing Systems: Predictable Scheduling Algorithms and Applications*, 3rd ed. New York: Springer, 2011.

[7] T. P. Baker, "Comparison of empirical success rates of global vs. partitioned fixed-priority and EDF scheduling for hard real time," Florida State University, Tech. Rep. TR-050601, 2005.

---

**Prepared by:** Shahab Afshar
**Date:** November 2, 2025
**Instructor:** Dr. G. Manimaran
**Department:** Electrical and Computer Engineering, Iowa State University
