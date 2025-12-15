# Feedback Control Based EDF Scheduling

## Feedback Scheduling - Motivation

One of the very successful areas in addressing performance in the presence of uncertainty (e.g., workload or fault) is that of **Robust Control**.

### Key Concepts

- **Feedback** of measured quantities to correct the behavior of a system has been a powerful concept
- Made technological advances in applications such as **amplifiers and avionics**
- Through concerted use of feedback control and its theoretical development, the concept has been used to deal with **uncertainty inherent in most systems**

### Important Note

If a system characteristics is **known precisely**, then the feedback strategies are **not useful**; the **open-loop strategies will outperform** their feedback counterpart.

---

## Feedback Control Technique

### Components

A typical feedback control system is composed of:

1. **Controller**
2. **Plant to be controlled** (RT System)
3. **Actuators**
4. **Sensors**

### Variables

- **Controlled/regulated variable**: The quantity of the output that is measured and controlled/regulated
- **Set point**: Represents the correct value of the controlled variable
- **Error**: The difference between the current value of the controlled variable and the set point
- **Manipulated/control variable**: The quantity that is varied by the controller so as to affect the value of the controlled/regulated variable

---

## Feedback System Operation

The system is composed of a feedback loop as follows:

1. The system **periodically measures** and compares the controlled variable to the set point to determine the error
2. The controller **computes the required control** with the control function of the system based on the error
3. The **actuators change the value** of the manipulated variable to control the system

```
Set Point → Controller → Actuators → RT System → Sensors → Measured Variable (compared to Set Point)
                ↑                                                     ↓
                └────────────────────── Feedback Loop ────────────────┘
```

---

## FC-EDF (Feedback Control - EDF)

### Task Model

**Ti = (I, ET, AS, D)**

- Each Ti has **logical versions**: **I** = (T₁, T₂, ... Tᵢₖ)
- Each version has **different execution time**: **ET** = {ET₁, ET₂, ... ETᵢₖ}
  - Suppose ET₁ ≥ ET₂ ≥ ... ≥ ETᵢₖ
- Each version has **different accuracy**: **AS** = {A₁, A₂, ... Aᵢₖ}
- Each task has a **soft deadline D** and a **start time S**
- Different versions of a task are called **service levels**
- A version with **longer execution time and better accuracy** is called a **higher service level**

---

## FC-EDF Variables

### Set Point
**Desired miss ratio**
```
miss ratio = (# missed tasks) / (# submitted tasks)
```

### Regulated/Measured Variable
**Actual miss ratio**

### Control Variable
**Requested CPU utilization**
```
requested CPU utilization = execution time / (deadline - current time)
```

### Actuators
1. **Server Level Controller**: Adjust service levels
2. **Admission Controller**: Use if requirements are not satisfied
   - If the requirements are not satisfied, use admission controller

---

## FC-EDF Schematic

```
┌─────────────────┐
│   Set Point     │ (Desired miss ratio)
└────────┬────────┘
         │
         v
┌─────────────────┐
│    Controller   │ (PID Controller)
└────────┬────────┘
         │
         v
┌─────────────────┐      ┌─────────────────┐
│    Actuators    │──────│   RT System     │
│ - Server Level  │      │   (Scheduler)   │
│ - Admission     │      │                 │
└─────────────────┘      └────────┬────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │    Sensors      │ (Measure miss ratio)
                         └────────┬────────┘
                                  │
                                  v
                         ┌─────────────────┐
                         │  Feedback Loop  │
                         └─────────────────┘
```

---

## PID Parameters Tuning

Approaches for tuning PID (Proportional-Integral-Derivative) parameters:

1. **Simulation experiments**
2. **Modeling analysis**
3. **Adaptive control** to tune the parameters on-line

**Reference:** C. Lu, J.A. Stankovic, G. Tao, and S.H. Son, "Design and Evaluation of a Feedback Control EDF Scheduling Algorithm," In Proc. Real-Time Systems Symp. pp.56-67, 1999.

---

## Feedback-Based (m,k)-RMS Scheduler

### Task Model

**T** = <c, p, m, k>

Where:
- **cᵢ**: Computation time
- **pᵢ**: Period
- **mᵢ**: Number of mandatory instances (out of k)
- **kᵢ**: Window size

**Requirements:** Tasks should meet **mi deadlines for every ki consecutive instances**

### Performance Index

#### Dynamic Failure Rate (DFR)
For a task Ti, it is the **percentage of instances** of the task miss their (m,k) guarantee.

#### Marginal Quality Received (MQR)

**MQRᵢ = (mᵢ - mᵢ') / (kᵢ - mᵢ)**

Where:
- **mᵢ**: The actual value used
- **MQRᵢ**: Marginal Quality Received of task Ti

**Goal:** To **maximize the quality** of tasks during overloading, **mᵢ'** is increased as much as possible

### Feedback-Based Adaptive Scheduler Architecture

```
┌─────────────┐
│  Set Point  │ (Target DFR)
└──────┬──────┘
       │
       v
┌─────────────┐     ┌bell───────────┐
│ PI Controller│────>│  Actuator     │
└─────────────┘     │ - Admission   │
       ^            │ - Scheduler   │
       │            └──────┬────────┘
       │                   v
       │            ┌─────────────┐
       └────────────│    CPU      │
                    └─────────────┘
                    Submitted tasks
                    ↓
                    Accepted tasks
                    ↓
                    Average Dynamic Failure Rate (feedback)
```

---

## Key Advantages of Feedback Control

### Benefits

1. **Handles uncertainty**: Adapts to unpredictable workload variations
2. **Dynamic response**: Automatically adjusts to maintain performance goals
3. **Graceful degradation**: Manages overload conditions without complete failure
4. **Quality trade-offs**: Allows sacrificing accuracy for timeliness during overload

### Comparison to Open-Loop

| Aspect | Open-Loop | Feedback Control |
|--------|-----------|-----------------|
| **Uncertainty handling** | Poor | Excellent |
| **Known characteristics** | Better | Unnecessary |
| **Overload handling** | Fixed | Adaptive |
| **Accuracy** | Fixed | Variable (trade-off) |

---

## Summary

### Feedback Control Approach

1. **Measure** actual performance (miss ratio, DFR)
2. **Compare** to desired target (set point)
3. **Compute** error
4. **Adjust** control variables (utilization, service levels, admission)
5. **Actuate** changes to the system
6. **Repeat** periodically

### Applications

- **FC-EDF**: Feedback Control with Earliest Deadline First scheduling
- **Feedback-based (m,k)-RMS**: Adaptive (m,k)-firm guarantee enforcement
- **Quality of Service**: Trade-off between accuracy and timeliness during overload

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

