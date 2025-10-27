# Overload Handling: Feedback-Control Based Scheduling

## Overview
Feedback-control scheduling uses control theory principles to adaptively manage system resources and meet performance objectives under varying workloads.

## Control System Principles

### Basic Feedback Loop
```
Reference Input → Controller → System → Output
                       ↑                    ↓
                       └── Feedback ─────────┘
```

### Application to Real-Time Scheduling
- **Reference**: Desired performance metrics (miss ratio, utilization, etc.)
- **Controller**: Scheduler that adjusts parameters
- **System**: Real-time application with tasks
- **Output**: Actual performance metrics
- **Feedback**: Measured current performance

## Control-Theoretic Scheduling

### Key Concepts

#### Controlled Variables
1. **Miss ratio**: Percentage of missed deadlines
2. **Response time**: Task completion time
3. **Utilization**: CPU usage
4. **Quality of Service**: Application-specific metrics

#### Control Parameters
1. **Task priorities**: Static or dynamic adjustments
2. **Execution frequencies**: Task period modifications
3. **Quality settings**: Optional work allocation
4. **Admission control**: Accept/reject new tasks

#### Disturbance
- Workload variations
- Execution time changes
- Aperiodic arrivals
- Mode transitions

### Proportional-Integral-Derivative (PID) Controller

#### Controller Design
```
u(t) = Kₚ × e(t) + Kᵢ × ∫e(τ)dτ + Kₐ × de(t)/dt
```

Where:
- **u(t)**: Control output (e.g., period change, priority adjustment)
- **e(t)**: Error (reference - measured)
- **Kₚ**: Proportional gain
- **Kᵢ**: Integral gain
- **Kₐ**: Derivative gain

#### Application Example
**Regulating miss ratio**:
```python
miss_ratio_error = target_miss_ratio - measured_miss_ratio

# Proportional term
priority_boost = K_p * miss_ratio_error

# Integral term (accumulates error)
accumulated_error += miss_ratio_error
priority_boost += K_i * accumulated_error

# Adjust task priorities
for task in tasks:
    task.priority += priority_boost
```

### PI Controller for Utilization

#### Problem
Regulate CPU utilization to target value (e.g., 0.75) by adjusting task periods.

#### Controller Design
```
U_error(k) = U_target - U_measured(k)
P_adjust(k) = P_adjust(k-1) + K_p × U_error(k) + K_i × ΣU_error
T_new = T_nominal × (1 - P_adjust)
```

#### Period Scaling
- Scale periods proportionally
- Higher utilization → longer periods (less frequent execution)
- Lower utilization → shorter periods (more frequent execution)

## Miss Ratio Control

### Objective
Maintain miss ratio below threshold while maximizing quality.

### Control Strategy
1. **Monitor miss ratio**: Measure over sliding window
2. **Calculate error**: M_target - M_measured
3. **Adjust quality**: Reduce optional work when overloaded
4. **Track history**: Use integral term to eliminate steady-state error

### Implementation
```python
class MissRatioController:
    def __init__(self, K_p, K_i, target_miss_ratio=0.05):
        self.K_p = K_p
        self.K_i = K_i
        self.target = target_miss_ratio
        self.integral = 0
        self.window = []
    
    def update(self, missed, total):
        miss_ratio = missed / total if total > 0 else 0
        self.window.append(miss_ratio)
        if len(self.window) > WINDOW_SIZE:
            self.window.pop(0)
        
        # Average over window
        avg_miss_ratio = sum(self.window) / len(self.window)
        
        # Error
        error = self.target - avg_miss_ratio
        
        # Control output
        integral += error
        control = self.K_p * error + self.K_i * integral
        
        # Adjust quality (decrease quality to reduce miss ratio)
        quality_factor = 1.0 - control
        quality_factor = max(0.5, min(1.0, quality_factor))
        
        return quality_factor
```

## Adaptive Period Adjustment

### Motivation
Adjust task execution frequencies based on workload to maintain schedulability.

### Two-Layer Control

#### Inner Loop: Period Controller
```
Maintains target utilization per task:
- Monitors task utilization U_i
- Adjusts period T_i inversely proportional to load
```

#### Outer Loop: Global Controller
```
Maintains global system utilization:
- Monitors overall utilization
- Adjusts all periods proportionally
- Ensures bounded miss ratio
```

### Implementation
```python
def adjust_periods(tasks, target_utilization=0.90):
    # Measure current utilization
    current_util = sum(task.C / task.T for task in tasks)
    
    if current_util > 1.0:  # Overload
        # Scale periods to reduce utilization
        scale_factor = target_utilization / current_util
        
        for task in tasks:
            # Increase period (reduce frequency)
            task.T = task.T / scale_factor
            
    elif current_util < 0.7:  # Underutilization
        # Scale periods to increase utilization
        scale_factor = 0.9 / current_util
        
        for task in tasks:
            # Decrease period (increase frequency)
            task.T = task.T / scale_factor
```

## Quality-Based Feedback

### Imprecise Computation with Feedback
- Mandatory work always completes
- Optional work adjusted based on system state
- Feedback controller selects quality level

### Quality Levels
```
Quality 0: Mandatory only (minimal)
Quality 1: Mandatory + Basic optional
Quality 2: Mandatory + Extended optional
Quality 3: Mandatory + Full optional (maximum)
```

### Controller Action
```python
def select_quality(tasks, controller):
    miss_ratio = compute_miss_ratio(tasks)
    quality = controller.update(miss_ratio)
    
    # Map quality to execution modes
    for task in tasks:
        if quality >= 0.9:
            task.mode = FULL_QUALITY
        elif quality >= 0.7:
            task.mode = HIGH_QUALITY
        elif quality >= 0.5:
            task.mode = BASIC_QUALITY
        else:
            task.mode = MANDATORY_ONLY
```

## Admission Control

### Feedback-Based Admission
- Monitor system performance continuously
- Admit new tasks only if system remains stable
- Reject tasks when overload likely

### Admission Control Algorithm
```python
def admit_task(new_task, current_tasks, controller):
    # Predict utilization with new task
    predicted_util = current_utilization
    predicted_util += new_task.C / new_task.T
    
    # Check miss ratio with controller
    miss_ratio = controller.current_value
    
    if predicted_util < 1.0 and miss_ratio < target:
        return ADMIT
    elif predicted_util < 0.95 and miss_ratio < target + margin:
        return ADMIT  # Small margin
    else:
        return REJECT
```

## Stability and Performance

### Stability Analysis
- Ensure controller stable (doesn't oscillate)
- Tune gains (K_p, K_i, K_d) appropriately
- Consider system delays and lag

### Performance Metrics
1. **Response time**: How quickly system adapts
2. **Steady-state error**: Final offset from target
3. **Overshoot**: Maximum deviation during transient
4. **Settling time**: Time to reach steady state

### Gain Tuning
- **K_p**: Reacts to current error (fast but may oscillate)
- **K_i**: Eliminates steady-state error (slow)
- **K_d**: Dampens oscillations (may amplify noise)

## Practical Considerations

### Sensor/Actuator Delays
- Measurement delays affect stability
- Actuation delays reduce responsiveness
- Must account for in controller design

### Noise and Jitter
- Measurement noise
- Control signal smoothing
- Filtering techniques

### Multi-Objective Control
- Balance multiple metrics
- Weighted objectives
- Pareto optimization

## Sources
- Lectrue 10 - Overload handling -- Feedback-control based scheduling-1.pdf
