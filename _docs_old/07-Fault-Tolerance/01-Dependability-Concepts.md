# Dependability Concepts - Overview

## Introduction
Dependability encompasses the ability of a system to deliver services that can be justified relied upon, particularly critical in real-time and safety-critical systems.

## Fundamental Concepts

### Dependability Attributes

#### Reliability
- **Definition**: Continuity of correct service
- Probability system performs correctly over time interval
- Reliability R(t) = P(system operational at time t)

#### Availability
- **Definition**: Readiness for correct service
- Fraction of time system is operational
- Availability A = MTBF / (MTBF + MTTR)

Where:
- **MTBF**: Mean Time Between Failures
- **MTTR**: Mean Time To Repair

#### Safety
- **Definition**: Absence of catastrophic consequences
- Prevention of failures causing harm
- System safe even when faults occur

#### Integrity
- **Definition**: Absence of improper system alterations
- Prevention of unauthorized modifications
- Data and code protection

#### Maintainability
- **Definition**: Ability to undergo modifications and repairs
- Ease of detecting and fixing faults
- Support for evolution

### Threats to Dependability

#### Faults
- **Definition**: Cause of errors
- Types: Hardware, software, human, specification
- Status: Active (error-producing) or dormant

#### Errors
- **Definition**: Part of system state that may lead to failure
- Incorrect state representation
- Caused by faults

#### Failures
- **Definition**: Deviation from correct service
- Observable behavior
- Service not delivered as specified

### Fault-Error-Failure Chain
```
Fault → Error → Failure
```

Fault activation produces error, error propagation causes failure.

## Dependability Means

### Fault Prevention
- **Objective**: Prevent fault occurrence or introduction
- Design methods and coding standards
- Development process improvements

### Fault Tolerance
- **Objective**: Avoid service failures despite faults
- Redundancy techniques
- Error detection and recovery
- Graceful degradation

### Fault Removal
- **Objective**: Reduce number or severity of faults
- Verification and testing
- Debugging and correction
- Quality assurance

### Fault Forecasting
- **Objective**: Estimate present number, future incidence, and consequences of faults
- Performance evaluation
- Reliability modeling
- Failure analysis

## Redundancy Techniques

### Temporal Redundancy
- Retry operations
- Re-execution with checkpoints
- Time-triggered retries

### Spatial Redundancy
- Multiple independent components
- Replication in space
- N-version programming

### Information Redundancy
- Error detecting/correcting codes
- Checksums and CRCs
- Parity bits

## Error Detection

### Encoding Techniques
- Parity checking
- Cyclic Redundancy Check (CRC)
- Hamming codes
- Reed-Solomon codes

### Structural Detection
- Watchdog timers
- Sanity checks
- Invariant checking
- Assertions

### Comparison Techniques
- Duplicate execution and compare
- Modular redundancy
- Majority voting

## Error Recovery

### Forward Recovery
- Correct error without rollback
- Error masking
- Compensation actions

### Backward Recovery
- Roll back to previous correct state
- Checkpointing
- Message logging

### Error Masking
- Automatic error correction
- Redundancy hides error
- System continues without interruption

## Failure Modes

### Crash Failure
- Component halts
- No further outputs
- Easier to handle

### Omission Failure
- Component fails to produce outputs
- Missed responses
- More subtle

### Timing Failure
- Output produced but outside timing window
- Critical for real-time systems
- Timing constraint violation

### Byzantine Failure
- Component produces arbitrary outputs
- Most difficult to handle
- Malicious or random behavior

## Reliability Metrics

### Failure Rate (λ)
Frequency of failures per unit time.

### Mean Time to Failure (MTTF)
Expected time until first failure.

### Mean Time Between Failures (MTBF)
MTBF = MTTF + MTTR

### Reliability Function
```
R(t) = e^(-λt)
```
Exponential failure law.

### Failure Probability
```
F(t) = 1 - R(t) = 1 - e^(-λt)
```

## Availability Models

### Steady-State Availability
```
A = MTBF / (MTBF + MTTR)
```

### Single Component
Availability depends on MTBF and MTTR.

### Parallel Redundancy
```
A_parallel = 1 - (1 - A₁)(1 - A₂)...(1 - Aₙ)
```

For identical components:
```
A_parallel = 1 - (1 - A)ⁿ
```

### Serial System
```
A_serial = A₁ × A₂ × ... × Aₙ
```

Weakest link dominates.

## Safety and Security

### Safety
- Prevention of hazards
- Fail-safe design
- Hazard analysis
- Risk assessment

### Security
- Protection against threats
- Authentication and authorization
- Confidentiality, integrity, availability
- Attack prevention

## Validation and Verification

### Verification
- "Are we building the product right?"
- Checking against specifications
- Testing and analysis

### Validation
- "Are we building the right product?"
- Checking requirements correctness
- User acceptance

### Testing Strategies
- Unit testing
- Integration testing
- System testing
- Stress testing
- Fault injection

## Sources
- Dependability Concepts - Overview.pdf
