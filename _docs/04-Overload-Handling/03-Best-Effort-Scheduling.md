# Best Effort Scheduling

## Best-Effort Scheduler Overview

### Characteristics

- **No schedulability check**
- **Schedule construction** – online
- **Overload handling** (handling timing faults)
- Approaches:
  - Value-based scheduling
  - Imprecise computation
  - (m,k)-firm task scheduling

### Value-Based Scheduling

**Task Model:** Ti = <Ci, Pi, Vi>

Where:
- **Ci**: Computation time
- **Pi**: Period
- **Vi**: Value offered by Ti

**Value Function:**
- If Ti finishes by di → offers a value of **Vi**
- Else → offers a value of **0** (sometimes a negative value)

---

## Scheduling Approaches

### Deadline Scheduler (e.g., EDF)
- **Good for**: Under/normal load
- Uses earliest deadline priority

### Value-Based Scheduler (e.g., HVDF)
- **Good for**: Overload
- Uses value density priority

### Hybrid (Adaptive) Scheduler
- **Good for**: All loads
- Combines both approaches

### Heuristics

**Hi = function(value, deadline)**

**Example**: Heuristic Hi = EDF "+" HVDF
- Schedules tasks based on the deadline
- When there is a tie in priority, breaks the tie in favor of **HVDF policy**

---

## HVDF – Highest Value Density First

### Value Density

**Value density = Vi / Ci**

(i.e., value per unit computation time)

### Priority Assignment

- **Higher the value density** → **Higher the importance** → **Higher the priority**
- HVDF scheduler schedules tasks based on **"value density"**

### Key Insight

During overload, it's better to execute high-value tasks efficiently (more value per computation time unit).

---

## Competitive Analysis of Best-Effort Scheduler

### Competitive Factor

The **competitive factor, BA**, of an on-line scheduling algorithm is defined as:

**BA = min (V_A(S) / V_CA(S)) over all S**

Where:
- **S**: A given task set
- **VA(S)**: Value produced by given scheduler A
- **V_CA(S)**: Value produced by **Clairvoyant scheduler**
  - The Clairvoyant scheduler knows complete knowledge of the workload a priori (i.e., at the beginning itself)

### Upper Bound

The upper bound on the competitive factor for any on-line scheduling is:

**1 / (γ + 1 + 2√γ)**

Where **γ = highest value density / lowest value density**

### Special Case

When **γ = 1** (i.e., Vi = Ci for all tasks):
- The competitive factor is **0.25**
- Even an optimal online algorithm can achieve only 25% of the value compared to the clairvoyant scheduler

---

## Overload Handling Summary

### Imprecise Computations
- **Models**: Monotone model, 0/1 model
- **Application**: Both periodic and aperiodic tasks
- **Approach**: Partial execution of optional portions

### (m,k)-Firm Task Model
- **Application**: Periodic tasks only
- **Approach**: Graceful degradation by dropping entire instances
- **Mechanism**: Meet m out of k consecutive deadlines

### Feedback Control Based Scheduler
- **Application**: All task types
- **Approach**: Predictable performance under load uncertainty
- **Mechanism**: Adapts scheduling parameters based on observed performance

### Best Effort Schedulers
- **Application**: All task types
- **Characteristics**: No guarantees on meeting deadlines
- **Approach**: Maximize value under any load condition
- **Heuristic**: Value-based prioritization (e.g., HVDF)

---

## Comparison of Overload Handling Techniques

| Technique | Guarantees | Load Handling | Complexity | Use Case |
|-----------|-----------|---------------|------------|----------|
| **Imprecise Computation** | Partial quality | Graceful degradation | Medium | Image/video processing |
| **(m,k)-Firm** | m/k guarantees | Instance dropping | Low | Control systems |
| **Feedback Control** | Adaptive bounds | Load adaptation | High | Uncertain workloads |
| **Best Effort** | No guarantees | Value maximization | Medium | Overload situations |

---

## Key Takeaways

1. **Best effort schedulers** provide no formal guarantees but attempt to maximize value
2. **Value density** (Vi/Ci) is a key metric for prioritization during overload
3. **Competitive analysis** shows theoretical limits of online scheduling
4. **HVDF** is optimal for maximizing value during overload
5. **Hybrid approaches** combining deadline and value-based scheduling work best across all load conditions

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

