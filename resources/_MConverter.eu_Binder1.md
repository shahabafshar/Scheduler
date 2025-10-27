**CprE 458/558: Real-Time Systems**

Introduction to Real-Time Systems

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**Real-time Systems -- Defined**

• Real-time systems are defined as those 

systems in which the correctness of the system 

depends not only on the **logical result** of 

computation, but also on the **time** at which the 

results are produced. 

****

• The performance of real-time systems must be 

predictable. 

• Real-time systems often operate in a 

constrained environment – workload variations, 

fault conditions, resource constraints. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

**Real-time System – Examples**

• Hard real-time systems \(e.g., Avionics, 

Command & Control Systems\). 

• Firm real-time systems \(e.g., radar 

tracking, manufacturing assembly line\). 

• Soft real-time systems \(e.g., Video 

conferencing, multimedia applications\). 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3



**A typical real-time system**

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4





**Sample Applications**

Agile Manufacturing

Traffic control system

5





**Industrial Internet & Internet of Things**

End devices, wireless 

network, cloud back-

end, analytics

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6



**Real-Time Systems -- Introduction**

•Hard deadline: penalty due to missing deadline is a higher 

order of magnitude than the reward in meeting the 

deadline

•Firm deadline: penalty and reward are in the same order 

of magnitude

•Soft deadline: penalty often lesser magnitude than 

reward

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7



**Example – Car Driver**

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8



**Controller area network \(CAN\) bus in an autonomous vehicle**

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**Example – Car driver**

• ***Mission:*** Reaching the destination safely. 

• **Controlled System:** Car. 

• **Operating environment:** Road conditions. 

• **Controlling System** 

* - Human driver:* Sensors - Eyes and Ears of the driver. 

* - Computer:* Sensors - Cameras, Infrared receiver, 

Laser telemeter, Navigation system, Street maps. 

• **Controls:** Accelerator, Steering wheel, Break-pedal. 

• **Actuators:** Wheels, Engines, and Brakes. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Example – Car driver \(contd\)**

• **Critical tasks:** Steering and breaking. 

• **Non-critical tasks:** Turning on radio. 

• **Performance** is not an absolute one. It measures the 

goodness of the outcome relative to the best outcome 

possible under a given circumstance. 

• **Cost** of fulfilling the mission → Efficient solution. 

• **Reliability** of the driver → Fault-tolerance is a must. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**Real-Time Tasks \(Workload\)**

• **Periodic tasks** 

- Time-driven. Characteristics are known *a priori* 

- Task *Ti* is characterized by \( *ci, pi*\)

* E.g.:* Task monitoring temperature of a patient in an ICU. 

• **Aperiodic tasks** 

- Event-driven. Characteristics are **not** known *a priori* 

- Task *Ti* is characterized by \( *ai*, * ri*, *ci*, *di*\) *E.g.:* Task activated upon detecting change in patient’s condition. 

• **Sporadic Tasks**

– Known minimum inter-arrival time among successive 

instances of a \(periodic\) task, rather strictly being periodic. 

*pi* : task period *ai* : arrival time *ri* : ready time *di* : deadline *ci* : worst-case execution time. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

12

**Task constraints**

• Deadline constraint

• Resource constraints 

– Shared access \(read-read\)

– Exclusive access \(write-x, where x: read or write\)

• Precedence constraints

– Task T1 precedes T2 denoted as T1 → T2

– i.e., Task T2 can start its execution only after T1 finishes

– Precedence relations among tasks are denoted in the 

form of a graph, known as precedence graph

• Fault-tolerant Requirements 

– Redundancy in task execution to achieve higher reliability

CprE 458/558: Real-Time Systems \(G. Manimaran\)

13

**Notion of Predictability**

• The most common denominator that is expected from a real-time 

system is *predictability*. 

– **The behavior of the real-time system must be **

**predictable which means that with certain **

**assumptions about workload and failures, it **

**should be possible to show at “design time” **

**that all the timing constraints of the **

**application will be met. **

• For static systems, 100% guarantees can be given at design time. 



• For dynamic systems, 100% guarantee cannot be given since the 

characteristics of tasks are not known a priori. 

• In dynamic systems, predictability means that once a task is 

admitted into the system \(based on online admission test\), its 

guarantee should never be violated as long as the assumptions 

under which the task was admitted hold. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

14



**Computing systems**

Uniprocessor, multiprocessor \(multicore systems\), 

distributed system, networked control systems

CprE 458/558: Real-Time Systems \(G. Manimaran\)

15

**Common Misconceptions**

• Real-time computing is equivalent to fast 

computing. 



• Real-time programming is assembly coding, 

priority interrupt programming, and writing 

device drivers. 

• Real-time systems operate in a static 

environment. 

• The problems in real-time system design have 

all been solved in other areas of computer 

science. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

16

**FreeRTOS Tutorial – A Beginner’s Guide**

CPRE 4580/5580 - 2025 Fall

Prof. Manimaran Govindarasu

Zhi Wang - danryw@iastate.edu

Department of Electrical and Computer Engineering, Iowa State University 1

**Table of Contents**

1. Introduction to FreeRTOS

2. Basic Concepts

3. Task Management

4. Interrupt Management

5. FreeRTOS Kernel

6. Project Demo

7. Project Proposal Ideas

8. Implementation Suggestions

9. Other Open-Source RTOS

2

**Introduction to FreeRTOS**

FreeRTOS \(Free Real-Time Operating System\) is a popular, open-source real-time operating system kernel for embedded systems. It is designed to be small, simple, and easy to use while providing powerful features for real-time applications. 

3

**Introduction to FreeRTOS**

**Official Documentation**

• https://www.freertos.org/Documentation/00-Overview

**FreeRTOS Kernel**

• https://github.com/FreeRTOS/FreeRTOS-Kernel

4

**Introduction to FreeRTOS**

**Key Features**

• **Preemptive multitasking**: Tasks can be interrupted and resumed

• **Cooperative multitasking**: Tasks voluntarily yield control

• **Multiple scheduling algorithms**: Including priority-based

• **Inter-task communication**: Queues, semaphores, mutexes

• **Memory management**: Multiple heap allocation schemes

• **Portable**: Runs on many different microcontrollers

5





**Introduction to FreeRTOS - Application**

**OV Watch**

https://github.com/No-Chicken/OV-Watch

6

**Basic Concepts - Tasks**

**Tasks**

Each runs independently and has its own stack, full API access, 

preemptive/cooperative scheduling, suitable for most applications. 

**Co-routines**

All share one stack \(saves RAM\), cooperative scheduling only, 

macro-based implementation, many usage restrictions, rarely used today. 

7

**Basic Concepts - Task States**

**Task States**

• **Running**: Currently executing on the CPU

• **Ready**: Ready to run but waiting for CPU time

• **Blocked**: Waiting for an event \(delay, semaphore, etc.\)

• **Suspended**: Explicitly suspended and won’t run until resumed 8



**Basic Concepts - Task States**

9

**Basic Concepts - Configuration**

FreeRTOSConfig.h contains all configuration options for FreeRTOS

*// Enable preemptive scheduling*

\#define configUSE\_PREEMPTION

1

*// Tick rate \(Hz\)*

\#define configTICK\_RATE\_HZ

\(1000\)

*// Stack size for idle task*

\#define configMINIMAL\_STACK\_SIZE

\(64\)

*// Total heap size*

\#define configTOTAL\_HEAP\_SIZE

\(64 \* 1024\)

*// Maximum number of priorities*

\#define configMAX\_PRIORITIES

\(10\)

*// Enable mutexes*

\#define configUSE\_MUTEXES

1

10

**Basic Concepts - Scheduling Algorithms**

**Fixed Priority Preemptive Scheduling**

• Configuration: configUSE\_PREEMPTION = 1

• Higher priority tasks preempt lower priority tasks

• Same priority tasks share CPU time \(Round Robin with time slice\) **Fixed Priority Cooperative Scheduling**

• Configuration: configUSE\_PREEMPTION = 0

• Tasks voluntarily yield control using taskYIELD\(\)

• No preemption: Tasks run until they explicitly give up CPU

**Time Slicing Scheduling**

• Tasks with the same priority share CPU time equally

• Tasks switches between these tasks at each tick interrupt

11

**Task Management - Priorities**

**Task Priorities**

• configMAX\_PRIORITIES defines the maximum priority level in

FreeRTOSConfig.h

• Higher numbers = higher priority

12

**Task Management - Task Functions**

void ATaskFunction\( void \*pvParameters \); 

13

**Task Management - Creation**

void vTaskFunction\(void\* pvParameters\); 

TaskHandle\_t xTaskHandle; 

int main\(void\) \{

.. 

xTaskCreate\(

*// Create a task*

vTaskFunction, 

*// Task function*

"TaskName", 

*// Task name*

configMINIMAL\_STACK\_SIZE, 

*// Stack size*

NULL, 

*// Parameters passed to task*

1, 

*// Priority \(0 = lowest\)*

&xTaskHandle

*// Task handle*

\); 

vTaskStartScheduler\(\); 

*// Start the scheduler*

... 

\}

14

**Task Management - Handling**

**Define Task Deletion**

void vTaskDelete\( TaskHandle\_t pxTaskToDelete \); 

**Deleting a Task**

vTaskDelete\(xTaskHandle\); 

*// Delete the task*

**Other Handler**

vTaskSuspend\(xTaskHandle\); 

*// Suspend the task*

vTaskResume\(xTaskHandle\); 

*// Resume the task*

vTaskPrioritySet\(xTaskHandle, 2\); 

*// Change priority*

15

**Task Management - Delays**

*// Delay for a specific number of ticks*

vTaskDelay\(pdMS\_TO\_TICKS\(1000\)\); 

*// Delay for 1000ms*

*// Delay until a specific time*

TickType\_t xLastWakeTime = xTaskGetTickCount\(\); 

vTaskDelayUntil\(&xLastWakeTime, pdMS\_TO\_TICKS\(100\)\); 

16

**Interrupt Management**

**Interrupt Safe API**

FreeRTOS provides a set of “Interrupt Safe” API functions that can be safely called from within an Interrupt Service Routine \(ISR\). These functions are specifically designed to handle the restrictions and requirements of running in an interrupt context. 

**Interrupt Safe API Implementation Files**

• queue.c - Core interrupt-safe queue and semaphore functions

• tasks.c - Interrupt-safe task notification functions

• timers.c - Interrupt-safe timer functions

• stream\_buffer.c - Interrupt-safe stream buffer functions

**Key Points:**

• **Only use FreeRTOS API functions ending with FromISR in ISRs** \(e.g., xQueueSendFromISR, xSemaphoreGiveFromISR\). 

• These are safe and fast for ISRs, often needing an extra parameter for context switching. 

17

**FreeRTOS Kernel - Installation**

**FreeRTOS Kernel Repository**

• https://github.com/FreeRTOS/FreeRTOS-Kernel

**Protable \(Architecture Platform Specific\)**

• Each real-time kernel port contains three common files and

platform-specific files. Find the associated architecture in protable folder of chip you use

**Arduino**

• https://docs.arduino.cc/libraries/freertos/

**ESP32**

• https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos.html

• https://github.com/espressif/esp-idf/tree/v5.5.1/components/freertos 18



**FreeRTOS Kernel - Structure**

19

**Project Demo - FreeRTOS EDF Scheduling**

**FreeRTOS EDF Scheduling**

FreeRTOS uses fixed-priority scheduling but lacks EDF support. EDF

ensures better deadline adherence and resource utilization for real-time applications. 

This demo project implements Earliest Deadline First \(EDF\) scheduling in FreeRTOS for IoT systems where task timing is critical and delays can cause failures or poor performance.real-time applications. 

20

**Project Demo - EDF Scheduler Implementation edf.c** **typedef struct **\_task

*// Task structure for EDF*

\{

int id; 

*// Task ID*

int at; 

*// Arrival time*

int et; 

*// Execution time*

int pd; 

*// Period*

int dd; 

*// Deadline*

\} task; 

task taskSet\[\] = \{

*// Example task set, time unit in ticks*

\{1, 0, 4, 12, 12\}, 

*// Task 1: 4 exec, 12 period, 12 ddl*

\{2, 0, 3, 9, 9\}, 

*// Task 2: 3 exec, 9*

*period, 9*

*ddl*

\{3, 0, 3, 6, 6\}, 

*// Task 3: 3 exec, 6*

*period, 6*

*ddl*

\}; 

21

**Project Demo - EDF Scheduler Implementation**

*// Enable EDF scheduler in FreeRTOSConfig.h*

\#define configUSE\_EDF\_SCHEDULER

1

*// Create EDF task*

xTaskCreate\_EDF\(

vTaskFunction, 

*// Task function*

"EDFTask", 

*// Task name*

configMINIMAL\_STACK\_SIZE, 

NULL, 

*// Parameters*

1, 

*// Priority \(used for tie-breaking\)*

NULL, 

*// Task handle*

TASK\_PERIOD, 

*// Period*

TASK\_DEADLINE

*// Deadline*

\); 

22

**Project Proposal Ideas**

**1. Implementation of RMS / LLF / . . . **

**2. Implementation to handle priority inversion**

**3. IoT Data Logger**

Build a embeded device using an ESP32/ESP32 that reads sensors, stores data, control LED. 

FreeRTOS can manage tasks for periodic sensor sampling, data storage, controlling

23

**Implementation Suggestions**

**Priority Assignment**

• Use as few priority levels as possible

• Reserve highest priority for critical tasks

• Avoid priority inversion scenarios

**Task Design**

• Keep tasks simple and use appropriate delays to prevent CPU hogging

• Use task not croutine, design for preemption not yield

24

**Implementation Suggestions**

**Memory Management**

• Choose appropriate heap allocation scheme

• heap\_1 - the very simplest, does not permit memory to be freed

• heap\_2 - permits memory to be freed, but does not coalescence

adjacent free blocks

• heap\_3 - simply wraps the standard malloc\(\) and free\(\) for thread safety

• heap\_4 - coalescences adjacent free blocks to avoid fragmentation. 

Includes absolute address placement option

• heap\_5 - as per heap\_4, with the ability to span the heap across multiple non-adjacent memory areas

25

**Other Free and Open-source RTOS**

**Zephyr**

• https://www.zephyrproject.org/

• https://github.com/zephyrproject-rtos

**Apache NuttX**

• https://nuttx.apache.org/

• https://github.com/apache/nuttx

26

**References**

\[1\] FreeRTOS, “FreeRTOS Documentation: Overview,” \[Online\]. Available: https://www.freertos.org/Documentation/00-Overview. 

\[Accessed: Jun. 2024\]. 

\[2\] R. Barry, “Mastering the FreeRTOS Real Time Kernel: A Hands-On Tutorial Guide,” FreeRTOS, 2018. \[Online\]. Available: https://www.freertos.org/media/2018/161204\_Mastering\_the\_FreeRTOS\_Real\_Time\_Kernel-A\_Hands-On\_Tutorial\_Guide.pdf. 

\[Accessed: Jun. 2024\]. 

\[3\] “FreeRTOS Tutorial Video Series,” YouTube. \[Online\]. Available: https://www.youtube.com/watch?v=QGVAayFI5ZQ&list=PLnMKNibPkDnFeFV4eBfDQ9e5IrGL\_dx1Q. \[Accessed: Jun. 2024\]. 

27

**Questions**

**Questions? **

**Zhi Wang**

• danryw@iastate.edu

28

CprE 558: Real-Time Systems

Lectures 15-16: 

Dependability Concepts

& Faul-Tolerance

**CprE 545**

**Iowa State University**

Dependable System



A system is **dependable **when it is trustworthy enough 

that reliance can be placed on the service that it delivers. 

For a system to be dependable, it must be



**Available **- e.g., ready for use when we need it. 



**Reliable **- e.g., able to provide continuity of service while we are using it. 



**Safe **- e.g., does not have a catastrophic consequence on the environment. 



**Secure **- e.g., able to preserve confidentiality. 

**CprE 545**

**Iowa State University**

**2**

Why Dependability ? 



With a greater reliance on computers in a variety of 

safety-critical applications, the consequences of failure and 

down time have become more severe. 



For example, in safety-critical applications - such as flight 

control, medical life support, process control, 

telecommunication switching, and on-line transaction 

processing systems - failure of computing resources can 

cost lives and/or money. 

**CprE 545**

**Iowa State University**

**3**

Example for Dependable Systems



The reliability figure usually stated as a goal for computer 

systems in commercial aircraft is less than 10^\{-9\} 

failures per hour. 



Modern telephone switching systems achieve a down time 

of at most one hour in 40 years. 



Medical life support system. 



Command and control systems. 



Process control applications. 

**CprE 545**

**Iowa State University**

**4**

Attributes of Dependability

**FAULTS**

**IMPAIRMENTS**

**ERRORS**

**FAILURES**

**FAULT AVOIDANCE**

**DEPENDABILITY**

**PROCUREMENT**

**FAULT TOLERANCE**

**MEANS**

**VALIDATION**

**FAULT REMOVAL**

**FAULT FORECASTING**

**RELIABILITY**

**QUANTITATIVE**

**AVAILABILITY**

**MEASURES**

**FAIL-SAFE**

**FAIL-OPERATIONAL**

**QUALITATIVE**

**NO SINGLE PT. FAILURE**

**CONSISTENCY**

**CprE 545**

**Iowa State University**

**5**

Approaches to Achieving Dependability



**Fault Avoidance **- how to prevent, by construction, the 

fault occurrence or introduction. 



**Fault Removal **- how to minimize, by verification, the 

presence of faults. 



**Fault Tolerance **- how to provide, by redundancy, a 

service complying with the specification in spite of faults. 



**Fault Forecasting **- how to estimate, by evaluation, the 

presence, the creation, and the consequence of faults. 

**CprE 545**

**Iowa State University**

**6**

Fault Avoidance



Fault avoidance uses various tools and techniques to 

design the system in such a manner that the introduction 

of faults is minimized. 



A fault avoided is one that does not have to be dealt with 

at a later time. 



Techniques used include design methodologies, 

verification and validation methodologies, modeling, and 

code inspections and walk-throughs. 

**CprE 545**

**Iowa State University**

**7**

Fault Removal



Fault Removal uses verification and testing techniques to 

locate faults enabling the necessary changes to be made 

to the system. 



The techniques include unit testing and integration testing. 



It is generally much more expensive to remove a fault 

than to avoid a fault. 

**CprE 545**

**Iowa State University**

**8**

Fault Tolerance



A system built with fault tolerance capabilities will manage 

to keep operating, perhaps at a degraded level, in the 

presence of these faults. 



In other words, fault-tolerance is informally defined as the 

ability of a system to deliver the expected service even in 

the presence of faults. 



For a system to be fault-tolerant, it must be able to detect, 

diagnose, confine, mask, compensate and recover from 

faults. 

**CprE 545**

**Iowa State University**

**9**

Fault Forecasting



It is possible to observe the behavior of a system and use 

this information to take action to compensate for faults 

before they occur. 



When a system deviates from its normal behavior, even if 

the behavior continues to meet system specifications, it 

may be appropriate to reconfigure the system to reduce 

the stress on a component with a high failure potential. 

**CprE 545**

**Iowa State University**

**10**

Achieving Dependability - Summary



Fault avoidance and fault tolerance may be seen as 

constituting dependability **procurement: **how to provide

the system with the ability to deliver the specified service. 



Fault removal and fault forecasting may be seen as 

constituting dependability **validation: **how to reach 

confidence in the system's ability to deliver the specified 

service. 

**CprE 545**

**Iowa State University**

**11**

Fault, Error, and Failure



A **fault **is a deviation in a hardware or software 

component from its intended function. 



An **error **is a manifestation of a fault in a system, in which the logical state of an element differs from its intended 

value. 



The time between fault occurrence and the first 

appearance of an error is called the **fault latency**. 



The time between occurrence of an error and its detection 

is called **error latency**. 

**CprE 545**

**Iowa State University**

**12**

Fault, Error, and Failure \(Contd.\)



When the fault-tolerance mechanisms **detect **an error, 

they may initiate several actions to handle the fault and 

contain its errors. 



Recovery occurs if these actions are successful; 

otherwise, the system eventually malfunctions and a 

**failure **occurs. 

**CprE 545**

**Iowa State University**

**13**

Example of a fault, an error, and a failure

Detection

Recovery or

Fault

Error

of error

failure

Fault

Error

Latency of 

latency latency

fault tolerance

mechanism

*s-a-0 fault Write *

*Reads s-a-0*

*Proper service*

*occurs in bitvalue 1 value instead of*

*continues or is*

*with value 0 into bit*

*the correct value 1disrupted*

*with s-a-0*

**CprE 545**

**Iowa State University**

**14**

Fault



Faults can arise during all stages in a computer system's 

evolution - specification, design, development, 

manufacturing, assembly, and installation - and 

throughout its operational life. 



Most faults that occur before full system deployment are 

discovered through testing and eliminated. 



Faults that are not removed can reduce a system's 

dependability when it is in the field. 



A fault can be classified by its duration, nature of output, 

and correlation to other faults. 

**CprE 545**

**Iowa State University**

**15**

Fault types - Based on Duration



**Permanent faults **are caused by irreversible device 

failures within a component due to damage, fatigue, or 

improper manufacturing. Once a permanent fault has 

occurred, the faulty component can be restored by 

replacement or repair. 



**Transient faults **are triggered by environmental 

disturbances such as voltage fluctuations, electro-magnetic 

interference, or radiation. These events typically have a 

short duration, returning the affected circuitry to a normal 

operating state without causing any lasting damage. 

**CprE 545**

**Iowa State University**

**16**

Fault types - Based on Duration \(Contd.\)



**Intermittent faults **are those which tend to oscillate 

between periods of erroneous activity and dormancy, may 

also surface during system operation. They are often 

attributed to design errors that result in marginal or 

unstable hardware. 

Example: fault due to a loose wire. 

**CprE 545**

**Iowa State University**

**17**

Fault Types - Based on Nature of Output



**Malicious fault: **Whenever a fault can cause a unit to 

behave arbitrarily, malicious or **Byzantine failure **is said to happen. 



A sensor sending conflicting outputs to different processors. 



An output line that stays afloat rather than stuck-at to 0 or 1 is considered to be malicious, because it is difficult to conclude 

consistently whether the output is 0 or 1. 



**Non-malicious: **Stuck-at faults are non-malicious. 

Malicious faults are much harder to detect than non-

malicious faults. 

**CprE 545**

**Iowa State University**

**18**

Fail-stop Unit



A unit is said to be fail-stop if it responds to up to a certain maximum number of faults by simply stopping, rather than 

producing incorrect output. 



A fail-stop unit typically has many processors running the 

same tasks and comparing the outputs. If the outputs do 

not agree, the whole unit turns itself off. 



A system is said to be fail-safe if one or more safe states 

can be identified, that can be accessed in case of a system 

failure, in order to avoid catastrophe. Example: Railway 

signaling. 

**CprE 545**

**Iowa State University**

**19**

Fault Types - Based on Correlation



Components fault may be independent of one another or 

correlated. 



A fault is said to be **independent **if it does not directly or indirectly cause another fault. 



Faults are said to be **correlated **if they are related. Faults could be correlated due to physical or electrical coupling of 

units. 



Correlated faults are more difficult to detect than 

independent faults. 

**CprE 545**

**Iowa State University**

**20**

Software Faults



Software faults are caused by incorrect specification, 

design, or coding of a program. 



Although software does not physically "break" after being installed in a computer system, latent faults or bugs in the 

code can surface during operation - especially under heavy 

or unusual workloads - and eventually lead to system 

failures. 

**CprE 545**

**Iowa State University**

**21**

Error



A fault in a system does not necessarily result in an error. 



An error occurs only when a fault is "sensitized", i.e., for a particular system state and input excitation, an incorrect 

next state and/or output results. 



A error may be latent or detected. An error is latent when 

it has not been recognized as such; an error is detected by 

a detection mechanism. An error may disappear before 

being detected. 



An error may, and in general does, propagate; by 

propagating, an error creates other \(new\) error\(s\). 

**CprE 545**

**Iowa State University**

**22**

Error Recovery



Error recovery is the process by which the system 

attempts to recover from the effects of an error. 



**Forward error recovery**: 

In this approach, the error is masked without any computations 

having to be redone. 



**Backward error recovery:**

In this approach, the system is rolled back to a state before the error is believed to have occurred and the computation is carried out again. 

**CprE 545**

**Iowa State University**

**23**

Failure



Failure denotes an element's inability to perform its 

designated function because of errors in the element or its 

environment, which in turn caused by various faults. The 

ways a system can fail may be classed according to two 

viewpoints:



**Mode of failure:**



Fail-controlled: the mode of failure has been specified and the 

system complies with this specification. 



Fail-uncontrolled: the mode of failure either does not comply with the specification or has not been specified? 

**CprE 545**

**Iowa State University**

**24**

Failure \(Contd.\)



**Severities of failure: **The failure severities result from grading the consequences of the failure modes upon the 

system environment. 



benign failures: where the consequences are of the same order of magnitude as the benefit provided by proper service delivery. 



catastrophic failures: where the consequences are 

incommensurable with the benefit provided by proper service 

delivery. 

**CprE 545**

**Iowa State University**

**25**

Classes of faults, errors, and failures



Related faults manifest themselves as similar errors and 

lead to common-mode failures, whereas independent 

faults usually cause distinct errors and separate failures. 

**Independent**

**Distinct**

**Separate**

**faults**

**errors**

**failures**

**Related**

**Similar**

**Common-mode**

**faults**

**errors**

**failures**

**CprE 545**

**Iowa State University**

**26**

Load and Fault Hypothesis



Any system has a finite processing power. If we intend to 

guarantee by design that certain performance 

requirements can be met, then we have to postulate a set 

of assumptions about the behavior of the environment. 



**Load hypothesis **defines the peak load that is assumed to be generated by the environment. 



**Fault hypothesis **defines the types and frequency of faults that a system must be capable of handling. 



The worst scenario that a fault-tolerant system must be 

capable of handling is at peak load with the maximum 

number of faults. 

**CprE 545**

**Iowa State University**

**27**

Graceful Degradation



If a specified fault scenario develops, the system must still 

provide a specified level of service. If more faults are 

generated than what is specified in the fault hypothesis, 

then, sometimes, the performance of

the system must **degrade gracefully**; i.e., the system 

must not suddenly collapse as the size of the faults 

increases, rather it should continue to execute part of the 

work load. 



The concept of **assumption coverage **defines the 

probability that the load and fault hypotheses - and all 

other assumptions made about the behavior of the 

environment - are in agreement with the reality. 

**CprE 545**

**Iowa State University**

**28**

Dependability Measures - Quantitative



A life of a system is perceived by its users as an 

alternation between two states of the delivered service: 

proper service and improper service. 



A failure is thus a transition from proper to improper 

service. 

Quantifying the alternation of proper-improper service 

leads to the two main measures of dependability: reliability 

and availability. 

**CprE 545**

**Iowa State University**

**29**

Reliability



Reliability is a measure of continuous delivery of proper 

service - or, equivalently, of the time to failure. In other 

words, it is the probability of surviving \(potentially despite 

failures\) over an interval of time. 



For instance, the reliability requirement might be stated as 

a 0.999999 availability for a 10-hour mission. In other 

words, the probability of failure during the mission may be 

at most 10^\{-6\}. 



Hard real-time systems such as flight control and process 

control demand high reliability, in which a failure could 

mean loss of life. 



**CprE 545**

**Iowa State University**

**30**

Availability



Availability is a measure of the delivery of proper service 

with respect to the alternation of proper and improper 

service. In other words, it is the probability of being 

operational at a given instant of time. 



A 0.999999 availability means that the system is not 

operational at most one hour in a million hours. 



It is important to note that a system with high availability 

may in fact fail. However, failure frequency and recovery 

time should be small enough to achieve the desired 

availability. 



Soft real-time systems such as telephone switching and 

airline reservation require high availability. 

**CprE 545**

**Iowa State University**

**31**

Dependability Measures - Qualitative



**Fail-safe: **Design the system in such a way that one or 

more safe states can be identified that can be accessed in 

case of a system failure. 

Example: A railway signaling system in which, on detection 

of a failure, all trains can be stopped to avoid severe 

consequences. 



**Fail-operational: **Design the system so that, when it 

sustains a specified number of faults, it still provides a 

subset of its specified service. In such systems, safe states 

cannot be identified. Example: A flight control system in 

which the system must deliver minimal level of service 

even in the case of failure. 

**CprE 545**

**Iowa State University**

**32**

Dependability Measures - Qualitative 

\(Cont’d\)



**No single point of failure**



Design the system so that the failure of any single component will not cause the system to fail. 



**Consistency**



Design the system so that all information delivered by the system is equivalent to the information that would be delivered by an 

instance of a non-faulty system. 

**CprE 545**

**Iowa State University**

**33**

**A case study of real-world **

**Safety-critical system failures**

**- Boeing 737 Max accidents**

CprE 458/558 Real-Time Systems

Iowa State University

1

**A case study article**

How the Boeing 737 Max Disaster Looks to a Software 

Developer

Design shortcuts meant to make a new plane seem like an old, 

familiar one are to blame

IEEE Spectrum, 18 April 2019

https://spectrum.ieee.org/aerospace/aviation/how-the-boeing-

737-max-disaster-looks-to-a-software-developer

2

CprE 458/558: Real-Time Systems

Lecture 17

Fault-tolerant design techniques

**CprE 458/558**

**G. Manimaran \(ISU\)**

Fault Tolerant Strategies



Fault tolerance in computer system is achieved through 

redundancy in hardware, software, information, and/or 

computations. Such redundancy can be implemented in 

static, dynamic, or hybrid configurations. 



Fault tolerance can be achieved by many techniques:



**Fault masking **is any process that prevents faults in a system from introducing errors. Example: Error correcting memories and 

majority voting. 



**Reconfiguration **is the process of eliminating faulty component from a system and restoring the system to some operational state. 

**CprE 458/558**

**G. Manimaran \(ISU\)**

**2**

Reconfiguration Approach



**Fault detection **is the process of recognizing that a fault has occurred. Fault detection is often required before any 

recovery procedure can be initiated. 



**Fault location **is the process of determining where a fault has occurred so that an appropriate recovery can be 

initiated. 



**Fault containment **is the process of isolating a fault and preventing the effects of that fault from propagating 

throughout the system. 



**Fault recovery **is the process of remaining operational or regaining operational status via reconfiguration even in the 

presence of faults. 

**CprE 458/558**

**G. Manimaran \(ISU\)**

**3**

The Concept of Redundancy



Redundancy is simply the addition of information, 

resources, or time beyond what is needed for normal 

system operation. 



**Hardware redundancy **is the addition of extra 

hardware, usually for the purpose either detecting or 

tolerating faults. 



**Software redundancy **is the addition of extra software, 

beyond what is needed to perform a given function, to 

detect and possibly tolerate faults. 



**Information redundancy **is the addition of extra 

information beyond that required to implement a given 

function; for example, error detection codes. 

**CprE 458/558**

**G. Manimaran \(ISU\)**

**4**

The Concept of Redundancy \(Cont’d\)



**Time redundancy **uses additional time to perform the 

functions of a system such that fault detection and often 

fault tolerance can be achieved. Transient faults are 

tolerated by this. 



The use of redundancy can provide additional capabilities 

within a system. But, redundancy can have very important 

impact on a system's performance, size, weight, power 

consumption, and reliability. 

**CprE 458/558**

**G. Manimaran \(ISU\)**

**5**

Hardware Redundancy



**Passive techniques **use the concept of fault masking. 

These techniques are designed to achieve fault tolerance 

without requiring any action on the part of the system. 

Relies on voting mechanisms. 



**Active techniques **achieve fault tolerance by detecting 

the existence of faults and performing some action to 

remove the faulty hardware from the system. That is, 

active techniques use fault detection, fault location, and 

fault recovery in an attempt to achieve fault tolerance. 

**CprE 458/558**

**G. Manimaran \(ISU\)**

**6**

Hardware Redundancy \(Cont’d\)



**Hybrid techniques **combine the attractive features of 

both the passive

and active approaches. 



Fault masking is used in hybrid systems to prevent erroneous 

results from being generated. 



Fault detection, location, and recovery are also used to improve fault tolerance by removing faulty hardware and replacing it with spares. 

**CprE 458/558**

**G. Manimaran \(ISU\)**

**7**

Hardware Redundancy - A Taxonomy

**Triple Modular Redundancy**

**Passive**

**N-Modular Redundancy**

**Techniques**

**Duplication with Comparison**

**Hot standby**

**Standby Sparing**

**Hardware**

**Active**

**Cold standby**

**Pair-and-a-Spair**

**Redundancy**

**Techniques**

**Watchdog timer**

**NMR with Spares**

**Hybrid**

**Slef-Purging Redundancy**

**Techniques**

**Sift-Out Redundancy**

**Triple-Duplex Architecture**

**CprE 458/558**

**G. Manimaran \(ISU\)**

**8**

Triple Modular Redundancy \(TMR\)

**Input 1**

**MODULE 1**

**Input 2**

**MODULE 2**

**VOTER**

**Output**

**Input 3**

**MODULE 3**

**CprE 458/558**

**G. Manimaran \(ISU\)**

**9**

Software Redundancy - to Detect 

Software Faults



There are two popular approaches: **N-Version **

**Programming **\(NVP\) and **Recovery Blocks \(RB\)**. 



NVP is a forward recovery scheme - it masks faults. 



NVP: multiple versions of the same task is executed 

concurrently. 



NVP relies on voting. 



RB is a backward error recovery scheme. 



RB: the versions of a task are executed serially. 



RB relies on acceptance test. 

**CprE 458/558**

**G. Manimaran \(ISU\)**

**10**

N-Version Programming \(NVP\) 



NVP is based on the principle of **design diversity**, that is coding a software module by different teams of programmers, to have multiple versions. 



Diversity can also be introduced by employing different algorithms for obtaining the same solution or by choosing different programming languages. 



NVP can tolerate both hardware and software faults. 



Correlated faults are not tolerated by the NVP. 



In NVP, deciding the number of versions required to ensure acceptable levels of software reliability is an important design consideration. 

**CprE 458/558**

**G. Manimaran \(ISU\)**

**11**

N-Version Programming \(Cont’d\)

**VERSION 1**

**Input**

**VERSION 2**

**VOTER**

**Output**

**VERSION 3**

**CprE 458/558**

**G. Manimaran \(ISU\)**

**12**

Recovery Blocks \(RB\)



RB uses multiple alternates \(backups\) to perform the same 

function; one module \(task\) is primary and the others are 

secondary. 



The primary task executes first. When the primary task 

completes execution, its outcome is checked by an 

**acceptance test. **



If the output is not acceptable, a secondary task executes 

after undoing the effects of primary \(i.e., rolling back to 

the state at which primary was invoked\) until either an 

acceptable output is obtained or the alternates are 

exhausted. 

**CprE 458/558**

**G. Manimaran \(ISU\)**

**13**

Recovery Blocks \(Cont’d\)

**Time**

**Success**

**Output**

**VERSION 1**

**ACCEPTANCE TEST**

**Failure**

**Success**

**Output**

**VERSION 2**

**ACCEPTANCE TEST**

**Failure**

**... **

**Output**

**VERSION N**

**ACCEPTANCE TEST**

**Failure**

**CprE 458/558**

**G. Manimaran \(ISU\)**

**14**

Recovery Blocks \(Cont’d\)



The acceptance tests are usually sanity checks; these 

consist of making sure that the output is within a certain 

acceptable range or that the output does not change at 

more than the allowed maximum rate. 



Selecting the range for acceptance test is crucial. If the 

allowed ranges are too small, the acceptance tests may 

label correct outputs as bad. If they are too large, the 

probability that incorrect outputs will be accepted is more. 



RB can tolerate software faults because the alternates are 

usually implemented with different approaches; RB is also 

known as **Primary-Backup approach. **

**CprE 458/558**

**G. Manimaran \(ISU\)**

**15**

*Application Report*

*SLOA101B – August 2002 – Revised May 2016*

***Introduction to the Controller Area Network \(CAN\)***

*Steve Corrigan*........................................................................................................ *Industrial Interface* **ABSTRACT**

A controller area network \(CAN\) is ideally suited to the many high-level industrial protocols embracing CAN and ISO-11898:2003 as their physical layer. Its cost, performance, and upgradeability provide for tremendous flexibility in system design. This application report presents an introduction to the CAN

fundamentals, operating principles, and the implementation of a basic CAN bus with TI's CAN transceivers and DSPs. The electrical layer requirements of a CAN bus are discussed along with the importance of the different features of a TI CAN transceiver. 

**Contents**

1

Introduction ................................................................................................................... 2

2

The CAN Standard .......................................................................................................... 2

3

Standard CAN or Extended CAN .......................................................................................... 3

3.1

The Bit Fields of Standard CAN and Extended CAN .......................................................... 3

4

A CAN Message ............................................................................................................. 4

4.1

Arbitration ............................................................................................................ 4

4.2

Message Types ..................................................................................................... 5

4.3

A Valid Frame ....................................................................................................... 6

4.4

Error Checking and Fault Confinement .......................................................................... 6

5

The CAN Bus................................................................................................................. 7

5.1

CAN Transceiver Features....................................................................................... 10

5.2

CAN Transceiver Selection Guide .............................................................................. 14

6

Conclusion .................................................................................................................. 16

7

Additional Reading ......................................................................................................... 16

**List of Figures**

1

The Layered ISO 11898 Standard Architecture ......................................................................... 2

2

Standard CAN: 11-Bit Identifier ............................................................................................ 3

3

Extended CAN: 29-Bit Identifier............................................................................................ 4

4

The Inverted Logic of a CAN Bus ......................................................................................... 4

5

Arbitration on a CAN Bus ................................................................................................... 5

6

Details of a CAN Bus........................................................................................................ 7

7

CAN Dominant and Recessive Bus States............................................................................... 8

8

CAN Bus Traffic.............................................................................................................. 9

9

CAN Test Bus ................................................................................................................ 9

10

3.3-V CAN Transceiver Power Savings ................................................................................ 10

11

Common-Mode Noise Coupled Onto Four Twisted-Pair Bus Lines ................................................. 11

12

Split Termination ........................................................................................................... 13

**List of Tables**

SLOA101B – August 2002 – Revised May 2016

*Introduction to the Controller Area Network \(CAN\)*

1

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

*Introduction*

www.ti.com

**Trademarks**

CANopen is a trademark of CAN in Automation. 

DeviceNet is a trademark of Open DeviceNet Vendor Association, Inc. 

**1**

**Introduction**

The CAN bus was developed by BOSCH \(1\) as a multi-master, message broadcast system that specifies a maximum signaling rate of 1 megabit per second \(bps\). Unlike a traditional network such as USB or Ethernet, CAN does not send large blocks of data point-to-point from node A to node B under the supervision of a central bus master. In a CAN network, many short messages like temperature or RPM

are broadcast to the entire network, which provides for data consistency in every node of the system. 

Once CAN basics such as message format, message identifiers, and bit-wise arbitration -- a major benefit of the CAN signaling scheme are explained, a CAN bus implementation is examined, typical waveforms presented, and transceiver features examined. 

**2**

**The CAN Standard**

CAN is an International Standardization Organization \(ISO\) defined serial communications bus originally developed for the automotive industry to replace the complex wiring harness with a two-wire bus. The specification calls for high immunity to electrical interference and the ability to self-diagnose and repair data errors. These features have led to CAN’s popularity in a variety of industries including building automation, medical, and manufacturing. 

The CAN communications protocol, ISO-11898: 2003, describes how information is passed between devices on a network and conforms to the Open Systems Interconnection \(OSI\) model that is defined in terms of layers. Actual communication between devices connected by the physical medium is defined by the physical layer of the model. The ISO 11898 architecture defines the lowest two layers of the seven layer OSI/ISO model as the data-link layer and physical layer in Figure 1. 

**DSP**

**or**

**Application Layer**

µ**Controller**

**Logic Link Control**

**Data-Link**

**Embedded**

CAN Controller, 

**Layer**

**Medium Access**

**CAN**

Embedded or

**Control**

Separate

**Physical Signaling**

**Controller**

**Physical**

**Physical Medium Attachment**

Electrical

**Layer**

**CAN**

Specifications:

Transceivers, 

**Medium-Dependant Interface**

**Transceiver**

Connectors, 

Cable

**CAN Bus-Line**

**Figure 1. The Layered ISO 11898 Standard Architecture**

In Figure 1, the application layer establishes the communication link to an upper-level application specific protocol such as the vendor-independent CANopen™ protocol. This protocol is supported by the international users and manufacturers group, CAN in Automation \(CiA\). Additional CAN information is located at the CiA Web site, can-cia.de. Many protocols are dedicated to particular applications like industrial automation, diesel engines, or aviation. Other examples of industry-standard, CAN-based protocols are KVASER's CAN Kingdom and Rockwell Automation's DeviceNet™. 

\(1\)

Robert Bosch GmbH, www.bosch.com

2

*Introduction to the Controller Area Network \(CAN\)*

SLOA101B – August 2002 – Revised May 2016

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

www.ti.com

*Standard CAN or Extended CAN*

**3**

**Standard CAN or Extended CAN**

The CAN communication protocol is a carrier-sense, multiple-access protocol with collision detection and arbitration on message priority \(CSMA/CD\+AMP\). CSMA means that each node on a bus must wait for a prescribed period of inactivity before attempting to send a message. CD\+AMP means that collisions are resolved through a bit-wise arbitration, based on a preprogrammed priority of each message in the identifier field of a message. The higher priority identifier always wins bus access. That is, the last logic-high in the identifier keeps on transmitting because it is the highest priority. Since every node on a bus takes part in writing every bit "as it is being written," an arbitrating node knows if it placed the logic-high bit on the bus. 

The ISO-11898:2003 Standard, with the standard 11-bit identifier, provides for signaling rates from 125

kbps to 1 Mbps. The standard was later amended with the “extended” 29-bit identifier. The standard 11-bit identifier field in Figure 2 provides for 211, or 2048 different message identifiers, whereas the extended 29-bit identifier in Figure 3 provides for 229, or 537 million identifiers. 

***3.1***

***The Bit Fields of Standard CAN and Extended CAN***

**3.1.1**

**Standard CAN**

**S**

**R**

**I**

**E**

**E**

**I**

**11- bit**

**O**

**T**

**D r0**

**D L C**

**0…8 Bytes Data**

**C R C**

**ACK O**

**O**

**F**

**Iden tifier**

**F**

**R**

**F**

**E**

**F**

**S**

**Figure 2. Standard CAN: 11-Bit Identifier**

The meaning of the bit fields of Figure 2 are:

•

SOF–The single dominant start of frame \(SOF\) bit marks the start of a message, and is used to synchronize the nodes on a bus after being idle. 

•

Identifier-The Standard CAN 11-bit identifier establishes the priority of the message. The lower the binary value, the higher its priority. 

•

RTR–The single remote transmission request \(RTR\) bit is dominant when information is required from another node. All nodes receive the request, but the identifier determines the specified node. The responding data is also received by all nodes and used by any node interested. In this way, all data being used in a system is uniform. 

•

IDE–A dominant single identifier extension \(IDE\) bit means that a standard CAN identifier with no extension is being transmitted. 

•

r0–Reserved bit \(for possible use by future standard amendment\). 

•

DLC–The 4-bit data length code \(DLC\) contains the number of bytes of data being transmitted. 

•

Data–Up to 64 bits of application data may be transmitted. 

•

CRC–The 16-bit \(15 bits plus delimiter\) cyclic redundancy check \(CRC\) contains the checksum \(number of bits transmitted\) of the preceding application data for error detection. 

•

ACK–Every node receiving an accurate message overwrites this recessive bit in the original message with a dominate bit, indicating an error-free message has been sent. Should a receiving node detect an error and leave this bit recessive, it discards the message and the sending node repeats the message after rearbitration. In this way, each node acknowledges \(ACK\) the integrity of its data. ACK is 2 bits, one is the acknowledgment bit and the second is a delimiter. 

•

EOF–This end-of-frame \(EOF\), 7-bit field marks the end of a CAN frame \(message\) and disables bit-stuffing, indicating a stuffing error when dominant. When 5 bits of the same logic level occur in succession during normal operation, a bit of the opposite logic level is *stuffed * into the data. 

•

IFS–This 7-bit interframe space \(IFS\) contains the time required by the controller to move a correctly received frame to its proper position in a message buffer area. 

SLOA101B – August 2002 – Revised May 2016

*Introduction to the Controller Area Network \(CAN\)*

3

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

*A CAN Message*

www.ti.com

**3.1.2**

**Extended CAN**

**S**

**1 1-bit**

**S**

**I**

**R**

**1 8-bit**

**E**

**E**

**I**

**O**

**R D**

**T r 1 r 0 D L C**

**0 …8 Bytes Data**

**C R C**

**A C K O**

**O**

**F**

**Identifi er**

**F**

**R E**

**Identifier R**

**F**

**F**

**S**

**Figure 3. Extended CAN: 29-Bit Identifier**

As shown in Figure 3, the Extended CAN message is the same as the Standard message with the addition of:

•

SRR–The substitute remote request \(SRR\) bit replaces the RTR bit in the standard message location as a placeholder in the extended format. 

•

IDE–A recessive bit in the identifier extension \(IDE\) indicates that more identifier bits follow. The 18-bit extension follows IDE. 

•

r1–Following the RTR and r0 bits, an additional reserve bit has been included ahead of the DLC bit. 

**4**

**A CAN Message**

***4.1***

***Arbitration***

A fundamental CAN characteristic shown in Figure 4 is the opposite logic state between the bus, and the driver input and receiver output. Normally, a logic-high is associated with a one, and a logic-low is associated with a zero - but not so on a CAN bus. This is why TI CAN transceivers have the driver input and receiver output pins passively pulled high internally, so that in the absence of any input, the device automatically defaults to a recessive bus state on all input and output pins. 

VCANH

CANH

D = 1 0 1

V

CANL

CANL

1

0

1

Recessive

Dominant

Recessive

R = 1 0 1

**Figure 4. The Inverted Logic of a CAN Bus**

Bus access is event-driven and takes place randomly. If two nodes try to occupy the bus simultaneously, access is implemented with a nondestructive, bit-wise arbitration. Nondestructive means that the node winning arbitration just continues on with the message, without the message being destroyed or corrupted by another node. 

The allocation of priority to messages in the identifier is a feature of CAN that makes it particularly attractive for use within a real-time control environment. The lower the binary message identifier number, the higher its priority. An identifier consisting entirely of zeros is the highest priority message on a network because it holds the bus dominant the longest. Therefore, if two nodes begin to transmit simultaneously, the node that sends a last identifier bit as a zero \(dominant\) while the other nodes send a one \(recessive\) retains control of the CAN bus and goes on to complete its message. A dominant bit always overwrites a recessive bit on a CAN bus. 

4

*Introduction to the Controller Area Network \(CAN\)*

SLOA101B – August 2002 – Revised May 2016

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

www.ti.com

*A CAN Message*

Note that a transmitting node constantly monitors each bit of its own transmission. This is the reason for the transceiver configuration of Figure 4 in which the CANH and CANL output pins of the driver are internally tied to the receiver's input. The propagation delay of a signal in the internal loop from the driver input to the receiver output is typically used as a qualitative measure of a CAN transceiver. This propagation delay is referred to as the loop time \(tLOOP in a TI data sheet\), but takes on varied nomenclature from vendor to vendor. 

Figure 5 displays the CAN arbitration process that is handled automatically by a CAN controller. Because each node continuously monitors its own transmissions, as node B's recessive bit is overwritten by node C’s higher priority dominant bit, B detects that the bus state does not match the bit that it transmitted. 

Therefore, node B halts transmission while node C continues on with its message. Another attempt to transmit the message is made by node B once the bus is released by node C. This functionality is part of the ISO 11898 physical signaling layer, which means that it is contained entirely within the CAN controller and is completely transparent to a CAN user. 

C wins

B wins

arbitration

arbitration

Node C

Transmits

Node B

Transmits

CAN Bus

**Figure 5. Arbitration on a CAN Bus**

The allocation of message priority is up to a system designer, but industry groups mutually agree on the significance of certain messages. For example, a manufacturer of motor drives may specify that message 0010 is a winding current feedback signal from a motor on a CAN network and that 0011 is the tachometer speed. Because 0010 has the lowest binary identifier, messages relating to current values always have a higher priority on the bus than those concerned with tachometer readings. 

In the case of DeviceNet™, devices from many manufacturers such as proximity switches and temperature sensors can be incorporated into the same system. Because the messages generated by DeviceNet sensors have been predefined by their professional association, the Open DeviceNet Vendors Association \(ODVA\), a certain message always relates to the specific type of sensor such as temperature, regardless of the actual manufacturer. 

***4.2***

***Message Types***

The four different message types, or frames \(see Figure 2 and Figure 3\), that can be transmitted on a CAN bus are the data frame, the remote frame, the error frame, and the overload frame. 

SLOA101B – August 2002 – Revised May 2016

*Introduction to the Controller Area Network \(CAN\)*

5

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

*A CAN Message*

www.ti.com

**4.2.1**

**The Data Frame**

The data frame is the most common message type, and comprises the Arbitration Field, the Data Field, the CRC Field, and the Acknowledgment Field. The Arbitration Field contains an 11-bit identifier in

Figure 2 and the RTR bit, which is dominant for data frames. In Figure 3, it contains the 29-bit identifier and the RTR bit. Next is the Data Field which contains zero to eight bytes of data, and the CRC Field which contains the 16-bit checksum used for error detection. Last is the Acknowledgment Field. 

**4.2.2**

**The Remote Frame**

The intended purpose of the remote frame is to solicit the transmission of data from another node. The remote frame is similar to the data frame, with two important differences. First, this type of message is explicitly marked as a remote frame by a recessive RTR bit in the arbitration field, and secondly, there is no data. 

**4.2.3**

**The Error Frame**

The error frame is a special message that violates the formatting rules of a CAN message. It is transmitted when a node detects an error in a message, and causes all other nodes in the network to send an error frame as well. The original transmitter then automatically retransmits the message. An elaborate system of error counters in the CAN controller ensures that a node cannot tie up a bus by repeatedly transmitting error frames. 

**4.2.4**

**The Overload Frame**

The overload frame is mentioned for completeness. It is similar to the error frame with regard to the format, and it is transmitted by a node that becomes too busy. It is primarily used to provide for an extra delay between messages. 

***4.3***

***A Valid Frame***

A message is considered to be error free when the last bit of the ending EOF field of a message is received in the error-free recessive state. A dominant bit in the EOF field causes the transmitter to repeat a transmission. 

***4.4***

***Error Checking and Fault Confinement***

The robustness of CAN may be attributed in part to its abundant error-checking procedures. The CAN

protocol incorporates five methods of error checking: three at the message level and two at the bit level. If a message fails any one of these error detection methods, it is not accepted and an error frame is generated from the receiving node. This forces the transmitting node to resend the message until it is received correctly. However, if a faulty node hangs up a bus by continuously repeating an error, its transmit capability is removed by its controller after an error limit is reached. 

Error checking at the message level is enforced by the CRC and the ACK slots displayed in Figure 2 and

Figure 3. The 16-bit CRC contains the checksum of the preceding application data for error detection with a 15-bit checksum and 1-bit delimiter. The ACK field is two bits long and consists of the acknowledge bit and an acknowledge delimiter bit. 

Also at the message level is a form check. This check looks for fields in the message which must always be recessive bits. If a dominant bit is detected, an error is generated. The bits checked are the SOF, EOF, ACK delimiter, and the CRC delimiter bits

At the bit level, each bit transmitted is monitored by the transmitter of the message. If a data bit \(not arbitration bit\) is written onto the bus and its opposite is read, an error is generated. The only exceptions to this are with the message identifier field which is used for arbitration, and the acknowledge slot which requires a recessive bit to be overwritten by a dominant bit. 

The final method of error detection is with the bit-stuffing rule where after five consecutive bits of the same logic level, if the next bit is not a complement, an error is generated. Stuffing ensures that rising edges are available for on-going synchronization of the network. Stuffing also ensures that a stream of bits are not mistaken for an error frame, or the seven-bit interframe space that signifies the end of a message. Stuffed bits are removed by a receiving node’s controller before the data is forwarded to the application. 

6

*Introduction to the Controller Area Network \(CAN\)*

SLOA101B – August 2002 – Revised May 2016

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

www.ti.com

*The CAN Bus*

With this logic, an active error frame consists of six dominant bits—violating the bit stuffing rule. This is interpreted as an error by all of the CAN nodes which then generate their own error frame. This means that an error frame can be from the original six bits to twelve bits long with all the replies. This error frame is then followed by a delimiter field of eight recessive bits and a bus idle period before the corrupted message is retransmitted. It is important to note that the retransmitted message still has to contend for arbitration on the bus. 

**5**

**The CAN Bus**

The data link and physical signaling layers of Figure 1, which are normally transparent to a system operator, are included in any controller that implements the CAN protocol, such as TI's TMS320LF2812

3.3-V DSP with integrated CAN controller. Connection to the physical medium is then implemented through a line transceiver such as TI's SN65HVD230 3.3-V CAN transceiver to form a system node as shown in Figure 6. 

**\(Node \#1\)**

**\(Node \#2\)**

**\(Node \#3\)**

**\(Node \#n\)**

**DSP or C**

µ

**DSP or C**

µ

**DSP or C**

µ

**DSP or C**

µ

**CAN**

**CAN**

**CAN**

**CAN**

**Controller**

**Controller**

**Controller**

**Controller**

**CAN**

**CAN**

**CAN**

**CAN**

**Transceiver**

**Transceiver**

**Transceiver**

**Transceiver**

**CANH**

R

**CAN Bus -Line**

R

L

L

**CANL**

**Figure 6. Details of a CAN Bus**

Signaling is differential which is where CAN derives its robust noise immunity and fault tolerance. 

Balanced differential signaling reduces noise coupling and allows for high signaling rates over twisted-pair cable. Balanced means that the current flowing in each signal line is equal but opposite in direction, resulting in a field-canceling effect that is a key to low noise emissions. The use of balanced differential receivers and twisted-pair cabling enhance the common-mode rejection and high noise immunity of a CAN

bus. 

The High-Speed ISO 11898 Standard specifications are given for a maximum signaling rate of 1 Mbps with a bus length of 40 m with a maximum of 30 nodes. It also recommends a maximum unterminated stub length of 0.3 m. The cable is specified to be a shielded or unshielded twisted-pair with a 120-Ω

characteristic impedance \(Zo\). The ISO 11898 Standard defines a single line of twisted-pair cable as the network topology as shown in Figure 6, terminated at both ends with 120-Ω resistors, which match the characteristic impedance of the line to prevent signal reflections. According to ISO 11898, placing R on a L

node must be avoided because the bus lines lose termination if the node is disconnected from the bus. 

The two signal lines of the bus, CANH and CANL, in the quiescent recessive state, are passively biased to

≉ 2.5 V. The dominant state on the bus takes CANH ≉ 1 V higher to ≉ 3.5 V, and takes CANL ≉ 1 V lower to ≉ 1.5 V, creating a typical 2-V differential signal as displayed in Figure 7. 

SLOA101B – August 2002 – Revised May 2016

*Introduction to the Controller Area Network \(CAN\)*

7

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated



*The CAN Bus*

www.ti.com

Driver

Input

**Recessive**

CANH

CAN

**Dominant**

**Recessive**

Bus

CANL

Receiver

Output

**Figure 7. CAN Dominant and Recessive Bus States**

The CAN standard defines a communication network that links all the nodes connected to a bus and enables them to talk with one another. There may or may not be a central control node, and nodes may be added at any time, even while the network is operating \(hot-plugging\). 

The nodes in Figure 8 and Figure 9 could theoretically be sending messages from smart sensing technology and a motor controller. An actual application may include a temperature sensor sending out a temperature update that is used to adjust the motor speed of a fan. If a pressure sensor node wants to send a message at the same time, arbitration ensures that the message is sent. 

For example, Node A in Figure 8 and Figure 9 finishes sending its message \(on the left side of Figure 8\) as nodes B and C acknowledge a correct message being received. Nodes B and C then begin arbitration—node C wins the arbitration and sends its message. Nodes A and B acknowledge C's message, and node B then continues on with its message. Again note the opposite polarity of the driver input and output on the bus. 

8

*Introduction to the Controller Area Network \(CAN\)*

SLOA101B – August 2002 – Revised May 2016

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated





www.ti.com

*The CAN Bus*

**CAN**

**Bus**

**Node A**

**Data**

ACK bit

**Node B**

ACK bit

**Data**

ACK bit

Node C wins arbitration

**Node C**

**Data**

**Figure 8. CAN Bus Traffic**

TEKTRONIX

784D

OSCILLOSCOPE

TEKTRONIX

P6247

DIFFERENTIAL

PROBE

**CANH**

**CH. 1**

120 \! 

120 \! 

**CANL**

**SN65HVD233**

**SN65HVD230**

**SN65HVD235**

TEKTRONIX

P6243

**C**

**2**

**3**

SINGLE-ENDED

**H**

**. **

**. **

**. **

**H**

**H**

PROBES

**4**

**C**

**C**

**D**

**R**

**D**

**R**

**D**

**R**

**Node A**

**Node B**

**Node C**

**TMS320LF2407A**

**TMS320LF2812**

**TMS320LF2810**

**DSP with CAN**

**DSP with CAN**

**DSP with CAN**

**Controller**

**Controller**

**Controller**

**to other sensor or**

**to other sensor or**

**to other sensor or**

**control equipment**

**control equipment**

**control equipment**

**Figure 9. CAN Test Bus**

SLOA101B – August 2002 – Revised May 2016

*Introduction to the Controller Area Network \(CAN\)*

9

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

*The CAN Bus*

www.ti.com

***5.1***

***CAN Transceiver Features***

**5.1.1**

**3.3-V Supply Voltage**

Most CAN transceivers require a 5-V power supply to reach the signal levels required by the ISO 11898

standard. However, by superior attention to high-efficiency circuit design, the TI 3.3-V CAN transceiver family operates with a 3.3-V power supply and is fully interoperable with 5-V CAN transceivers on the same bus. This allows designers to reduce total node power by 50% or more \(Figure 10\). 

**Power \(mW\)**

200

150

100

50

0

3.3-V CAN

5-V CAN

Transceiver

Transceiver

**Figure 10. 3.3-V CAN Transceiver Power Savings**

In addition to the inherent power savings of using a 3.3-V transceiver, for applications using 3.3-V

technology, such as the TI TMS320C28xx family of DSPs with integrated CAN controllers, the need for a 5-V power supply can be eliminated. This lowers the overall part count for the node, reducing system cost and increasing system reliability. 

For designers with an existing system design which requires a 5-V-powered transceiver, the TI 5-V

transceivers are available with a wide variety of features such as high ESD protection and wide common-mode range. 

**5.1.2**

**ESD Protection**

Static charge is an unbalanced electrical charge at rest, typically created by the physical contact of different materials. One surface gains electrons, whereas the other surface loses electrons. This results in an unbalanced electrical condition known as a static charge. When a static charge moves from one surface to another, it is referred to as an electrostatic discharge \(ESD\). It can occur only when the voltage differential between the two surfaces is sufficiently high to break down the dielectric strength of the medium separating the two surfaces. 

ESD can occur in any one of four ways: a charged body can touch an integrated circuit \(IC\), a charged IC

can touch a grounded surface, a charged machine can touch an IC, or an electrostatic field can induce a voltage across a dielectric sufficient to break it down. 

The main threat of ESD damage occurs during the assembly and manufacturing of circuits. After assembly and installation, the main protection required for the bus pins is surge protection. 

**5.1.3**

**Common-Mode Voltage Operating Range**

Common-mode voltage is the difference in potential between grounds of sending and receiving nodes on a bus. This is often the case in the networked equipment typically found in a CAN application. Possible effects of this problem are intermittent reboots, lock-ups, bad data transfer, or physical damage to a transceiver. 

Network interface cards, parallel ports, serial ports, and especially transceivers are prime targets for some form of failure if not designed to accommodate high levels of ground shift and power supply imbalance between typical CAN nodes. 

10

*Introduction to the Controller Area Network \(CAN\)*

SLOA101B – August 2002 – Revised May 2016

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated



www.ti.com

*The CAN Bus*

With this in mind, most TI CAN transceivers are designed to operate with complete safety well beyond the bus voltage range of –2 V to 7 V required by the ISO 11898 Standard **5.1.4**

**Common-Mode Noise Rejection**

Common-mode noise of varied magnitudes exist within the networks associated with CAN applications. 

Noise from pulsing motor controllers, switch-mode power supplies, or from fluorescent lighting load are the typical sources of noises that couple onto bus lines as displayed in Figure 11. These would otherwise be straight lines. 

**Figure 11. Common-Mode Noise Coupled Onto Four Twisted-Pair Bus Lines** A CAN transceiver's receiver not specifically designed to reject this coupled noise can respond to common-mode noise as if it were data on a bus and send meaningless data to a controller. TI CAN

transceivers are specifically designed and tested for their ability to reject this common-mode noise. 

**5.1.5**

**Controlled Driver Output Transition Times**

Controlling the driver output slew rate dampens the rise time of a dominant bit to improve signal quality and provides for longer stub lengths and a better bit-error rate. For a discussion on how slew-rate control provides for longer stub lengths, see application report SLLA270. 

**5.1.6**

**Low-Current Bus Monitor, Standby and Sleep Modes**

Many applications are looking to lower-power opportunities as more electronics are added to designs. The standby mode in many TI transceivers is generally referred to as the “listen only” mode, because in standby, the driver circuitry is switched off while the receiver continues to monitor bus activity. In the occurrence of a dominant bit on the bus, the receiver passes this information along to its DSP/CAN

controller which in turn activates the circuits that are in standby. This is achieved by placing a logic-low level on the Rs pin \(pin 8\) of the device. 

The difference between the standby mode and the sleep mode is that both driver and receiver circuits can be switched off to create an extremely low-power sleep mode with no bus monitor. The local controller actively places the device into and out of sleep mode. 

The HVD1040 contains the best of both standby and sleep features with a low-power \(5 μA typical\) bus monitor. The device driver and receiver circuitry is switched off while a small comparator monitors the bus and toggles the receiver output on bus activity. 

SLOA101B – August 2002 – Revised May 2016

*Introduction to the Controller Area Network \(CAN\)*

11

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

*The CAN Bus*

www.ti.com

**5.1.7**

**Bus Pin Short-Circuit Protection**

The ISO 11898 Standard recommends that a transceiver survive bus wire short-circuits to each other, to the power supply, and to ground. This ensures that transceivers are not damaged by bus cable polarity reversals, cable crush, and accidental shorts to high power supplies. The short-circuit protection in TI devices protects for an unlimited time. Once a problem is removed, the devices perform as designed whereas the CAN transceivers offered from competing vendors are permanently damaged and require replacement. 

**5.1.8**

**Thermal Shutdown Protection**

Another desirable safety feature for a CAN transceiver is the thermal shutdown circuitry of TI CAN

transceivers. This feature protects a device against the destructive currents and resulting heat that can occur in a short-circuit condition. Once thermal shutdown is activated, the device remains shut down until the circuitry is allowed to cool. Once cooled down to normal operating temperature, the device automatically returns to active operation without damage. 

**5.1.9**

**Bus Input Impedance**

A high bus input impedance increases the number of nodes that can be added to a bus above the ISO

11898 Standard’s 30 nodes. The high impedance restricts the amount of current that a receiver sinks or sources onto a bus over common-mode voltage conditions. This ensures that a driver transmitting a message into such a condition is not required to sink or source a damaging amount of current from the sum of the receiver leakage currents on a bus. 

**5.1.10**

**Glitch-Free Power Up and Power Down**

This feature provides for hot-plugging onto a powered bus without disturbing the network. The TI driver and receiver pins are passively pulled high internally while the bus pins are biased internally to a high-impedance recessive state. This provides for a power up into a known recessive condition without disturbing ongoing bus communication. 

**5.1.11**

**Unpowered Node Protection**

Many CAN transceivers on the market today have a low output impedance when unpowered. This low impedance causes the device to sink any signal present on the bus and shuts down all data transmission. 

TI CAN transceivers have a high output impedance in powered and unpowered conditions and maintain the integrity of the bus any time power or ground is removed from the circuit. 

**5.1.12**

**Reference Voltage**

Reference voltage on a CAN transceiver is the Vref pin \(pin 5\) of what is considered to be the standard CAN transceiver footprint. This is the footprint of the first CAN transceiver to market, the NXP

PCA82C250. 

When first introduced, the Vcc/2 Vref pin served a particular NXP CAN controller as a voltage reference used to compare the bus voltage of a remaining single bus line in the event of an accident. If the voltages were the same, it was a recessive bit; if different, it was a dominant bit. 

Although some users consider it handy for use as an actual voltage reference at the node, it is typically unused. 

**5.1.13**

**V-Split**

V-split is a fortified Vcc/2 Vref pin with the same ESD protection rating, short-circuit protection, and common-mode operating range as the bus pins. It is used to stabilize bus voltage at Vcc/2 and prevent it from drifting to a high common-mode voltage during periods of inactivity. 

12

*Introduction to the Controller Area Network \(CAN\)*

SLOA101B – August 2002 – Revised May 2016

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

www.ti.com

*The CAN Bus*

It also filters unwanted high-frequency noise from bus lines with the termination technique of Figure 12. 

This is accomplished with a coupling capacitor between two ~60 Ω ±1% termination resistors to couple high-frequency noise to a solid ground potential. Care must be taken to match the two resistors carefully so as not to reduce the effective immunity. This technique improves the electromagnetic compatibility of a network. A typical value of CL for a high-speed CAN is 4.7 nF, which generates a 3-dB point at 1.1 Mbps. 

This, of course, is a signaling-rate-dependant value. 

**node**

**node**

**node**

**\#1**

**\#2**

CANH

**\#n**

60 W

60 W

Vsplit

Vsplit

60 W

60 W

CANL

CL

CL

1

Low-pass filter with fc = 2pRCL

**Figure 12. Split Termination**

**5.1.14**

**Loopback**

This function places the bus input and output in a high-impedance state. The remaining transceiver circuitry remains active and available for driver-to-receiver loopback and self-diagnostic node functions without disturbing the bus. 

**5.1.15**

**Autobaud Loopback**

In autobaud loopback, the “bus-transmit” function of the transceiver is disabled, while the “bus-receive” 

function and all of the normal operating functions of the device remain intact. With the autobaud function engaged, normal bus activity can be monitored by the device. 

Autobaud detection is best suited to applications that have a known selection of baud rates. For example, a popular industrial application has optional settings of 125 kbps, 250 kbps, or 500 kbps. Once a logic-high has been applied to pin 5 \(AB\) of the HVD235, assume a baud rate such as 125 kbps; then wait for a message to be transmitted by another node on the bus. If the wrong baud rate has been selected, an error message is generated by the host CAN controller. However, because the “bus-transmit” function of the device has been disabled, no other nodes receive the error message of the controller. 

This procedure makes use of the CAN controller’s status register indications of message received and error warning status to signal if the current baud rate is correct or not. The warning status indicates that the CAN chip error counters have been incremented. A message-received status indicates that a good message has been received. 

If an error is generated, reset the CAN controller with another baud rate and wait to receive another message. When an error-free message has been received, the correct baud rate has been detected. 

SLOA101B – August 2002 – Revised May 2016

*Introduction to the Controller Area Network \(CAN\)*

13

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

*The CAN Bus*

www.ti.com

***5.2***

***CAN Transceiver Selection Guide***

**Transceiver**

**Supply**

**Short**

**Common-**

**ESD \(kV\)**

**Standby**

**Sleep**

**Silent**

**Shutdown**

**Low-Power**

**Vref**

**Vsplit**

**Loopback**

**Autobaud**

**Slew**

**Fault**

**VIO**

**5-Mbps FD**

**Voltage**

**Circuit**

**Mode**

**\(SHDN\)**

**Bus**

**Rate**

**\(V\)**

**Voltage**

**Voltage**

**Monitor**

**Control**

**\(V\)**

**Range \(V\)**

SN65HVD230

3.3

–4 to 16

–2 to 7

HBM: ±16

X

X

X

SN65HVD231

3.3

–4 to 16

–2 to 7

HBM: ±16

X

X

X

SN65HVD232

3.3

–4 to 16

–2 to 7

HBM: ±16

SN65HVD233

3.3

±36

–7 to 12

HBM: ±16

X

X

X

SN65HVD234

3.3

±36

–7 to 12

HBM:±16

X

X

X

SN65HVD235

3.3

±36

–7 to 12

HBM: ±16

X

X

X

SN65HVD251

5

±36

–7 to 12

HBM: ±12

X

X

X

SN65HVD1040

5

–27 to 40

±12

IEC ±6

X

X

HBM: ±12

SN65HVD1050

5

–27 to 40

±12

IEC: ±6

X

X

HBM: ±8

SN65HVD255

5

–27 to 40

–2 to 7

IEC: ±8

X

X

HBM: ±12

SN65HVD256

5

–27 to 40

–2 to 7

IEC: ±8

X

X

X

HBM: ±12

SN65HVD257

5

–27 to 40

–2 to 7

IEC: ±8

X

X

X

HBM: ±12

SN65HVD265

5

–27 to 40

–2 to 7

IEC: ±8

X

X

HBM: ±12

SN65HVD266

5

–27 to 40

–2 to 7

IEC: ±8

X

X

X

HBM: ±12

SN65HVD267

5

–27 to 40

–2 to 7

IEC: ±8

X

X

X

HBM: ±12

SN65HVDA540-5-Q1

5

–27 to 40

±12

IEC: ±7

X

HBM: ±12

SN65HVDA541-5-Q1

5

–27 to 40

±12

IEC: ±7

X

HBM: ±12

SN65HVDA542-5-Q1

5

–27 to 40

±12

IEC: ±7

X

HBM: ±12

SN65HVDA540-Q1

5

–27 to 40

±12

IEC: ±7

X

X

HBM: ±12

SN65HVDA541-Q1

5

–27 to 40

±12

IEC: ±7

X

X

HBM: ±12

SN65HVDA542-Q1

5

–27 to 40

±12

IEC: ±7

X

X

HBM: ±12

HVDA551-Q1

5

–27 to 40

±12

IEC: ±7

X

X

HBM: ±12

HVDA553-Q1

5

–27 to 40

±12

IEC: ±7

X

X

HBM: ±12

TCAN330\(G\)

3.3

±14

±12

IEC ±12

X

X

X

X\(G\)

HBM: ±4

TCAN332\(G\)

3.3

±14

±12

IEC ±12

X\(G\)

HBM: ±4

TCAN334\(G\)

3.3

±14

±12

IEC ±12

X

X

X\(G\)

HBM: ±4

14

*Introduction to the Controller Area Network \(CAN\)*

SLOA101B – August 2002 – Revised May 2016

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

www.ti.com

*The CAN Bus*

**Transceiver**

**Supply**

**Short**

**Common-**

**ESD \(kV\)**

**Standby**

**Sleep**

**Silent**

**Shutdown**

**Low-Power**

**Vref**

**Vsplit**

**Loopback**

**Autobaud**

**Slew**

**Fault**

**VIO**

**5-Mbps FD**

**Voltage**

**Circuit**

**Mode**

**\(SHDN\)**

**Bus**

**Rate**

**\(V\)**

**Voltage**

**Voltage**

**Monitor**

**Control**

**\(V\)**

**Range \(V\)**

TCAN337\(G\)

3.3

±14

±12

IEC ±12

X

X

X

X\(G\)

HBM: ±4

TCAN1042\(H\)\(G\)\(V\)-Q1

5

±58

±30

IEC: ±8

X

X

X\(V\)

X\(G\)

±70 \(H\)

HBM: ±10

TCAN1051\(H\)\(G\)\(V\)-Q1

5

±58

±30

IEC: ±8

X

X

X\(V\)

X\(G\)

±70 \(H\)

HBM: ±10

SLOA101B – August 2002 – Revised May 2016

*Introduction to the Controller Area Network \(CAN\)*

15

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

*Conclusion*

www.ti.com

**6**

**Conclusion**

CAN is ideally suited in applications requiring a large number of short messages with high reliability in rugged operating environments. Because CAN is message based and not address based, it is especially well suited when data is needed by more than one location and system-wide data consistency is mandatory. 

Fault confinement is also a major benefit of CAN. Faulty nodes are automatically dropped from the bus, which prevents any single node from bringing a network down, and ensures that bandwidth is always available for critical message transmission. This error containment also allows nodes to be added to a bus while the system is in operation, otherwise known as hot-plugging. 

The many features of the TI CAN transceivers make them ideally suited for the many rugged applications to which the CAN protocol is being adapted. Among the applications finding solutions with CAN are automobiles, trucks, motorcycles, snowmobiles trains, buses, airplanes, agriculture, construction, mining, and marine vehicles. 

**7**

**Additional Reading**

1. Controller Area Network, Basics Protocols, Chips and Applications; Dr. Konrad Etschberger; ISBN 3-00-007376-0 \(www.ixxat.com\)

2. CAN Systems Engineering, From Theory to Practical Applications; Wolfhard Lawrenz, ISBN 0-387-94939-9

**Revision History**

NOTE: Page numbers for previous revisions may differ from page numbers in the current version. 

**Changes from A Revision \(July 2008\) to B Revision **..................................................................................................... **Page**

•

Updated *CAN Transceiver Selection Guide*. ......................................................................................... 14

16

*Revision History*

SLOA101B – August 2002 – Revised May 2016

*Submit Documentation Feedback*

Copyright © 2002–2016, Texas Instruments Incorporated

**IMPORTANT NOTICE FOR TI DESIGN INFORMATION AND RESOURCES**

Texas Instruments Incorporated \(‘TI”\) technical, application or other design advice, services or information, including, but not limited to, reference designs and materials relating to evaluation modules, \(collectively, “TI Resources”\) are intended to assist designers who are developing applications that incorporate TI products; by downloading, accessing or using any particular TI Resource in any way, you \(individually or, if you are acting on behalf of a company, your company\) agree to use it solely for this purpose and subject to the terms of this Notice. 

TI’s provision of TI Resources does not expand or otherwise alter TI’s applicable published warranties or warranty disclaimers for TI products, and no additional obligations or liabilities arise from TI providing such TI Resources. TI reserves the right to make corrections, enhancements, improvements and other changes to its TI Resources. 

You understand and agree that you remain responsible for using your independent analysis, evaluation and judgment in designing your applications and that you have full and exclusive responsibility to assure the safety of your applications and compliance of your applications \(and of all TI products used in or for your applications\) with all applicable regulations, laws and other applicable requirements. You represent that, with respect to your applications, you have all the necessary expertise to create and implement safeguards that \(1\) anticipate dangerous consequences of failures, \(2\) monitor failures and their consequences, and \(3\) lessen the likelihood of failures that might cause harm and take appropriate actions. You agree that prior to using or distributing any applications that include TI products, you will thoroughly test such applications and the functionality of such TI products as used in such applications. TI has not conducted any testing other than that specifically described in the published documentation for a particular TI Resource. 

You are authorized to use, copy and modify any individual TI Resource only in connection with the development of applications that include the TI product\(s\) identified in such TI Resource. NO OTHER LICENSE, EXPRESS OR IMPLIED, BY ESTOPPEL OR OTHERWISE TO

ANY OTHER TI INTELLECTUAL PROPERTY RIGHT, AND NO LICENSE TO ANY TECHNOLOGY OR INTELLECTUAL PROPERTY

RIGHT OF TI OR ANY THIRD PARTY IS GRANTED HEREIN, including but not limited to any patent right, copyright, mask work right, or other intellectual property right relating to any combination, machine, or process in which TI products or services are used. Information regarding or referencing third-party products or services does not constitute a license to use such products or services, or a warranty or endorsement thereof. Use of TI Resources may require a license from a third party under the patents or other intellectual property of the third party, or a license from TI under the patents or other intellectual property of TI. 

TI RESOURCES ARE PROVIDED “AS IS” AND WITH ALL FAULTS. TI DISCLAIMS ALL OTHER WARRANTIES OR

REPRESENTATIONS, EXPRESS OR IMPLIED, REGARDING TI RESOURCES OR USE THEREOF, INCLUDING BUT NOT LIMITED TO

ACCURACY OR COMPLETENESS, TITLE, ANY EPIDEMIC FAILURE WARRANTY AND ANY IMPLIED WARRANTIES OF

MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT OF ANY THIRD PARTY INTELLECTUAL

PROPERTY RIGHTS. 

TI SHALL NOT BE LIABLE FOR AND SHALL NOT DEFEND OR INDEMNIFY YOU AGAINST ANY CLAIM, INCLUDING BUT NOT

LIMITED TO ANY INFRINGEMENT CLAIM THAT RELATES TO OR IS BASED ON ANY COMBINATION OF PRODUCTS EVEN IF

DESCRIBED IN TI RESOURCES OR OTHERWISE. IN NO EVENT SHALL TI BE LIABLE FOR ANY ACTUAL, DIRECT, SPECIAL, COLLATERAL, INDIRECT, PUNITIVE, INCIDENTAL, CONSEQUENTIAL OR EXEMPLARY DAMAGES IN CONNECTION WITH OR

ARISING OUT OF TI RESOURCES OR USE THEREOF, AND REGARDLESS OF WHETHER TI HAS BEEN ADVISED OF THE

POSSIBILITY OF SUCH DAMAGES. 

You agree to fully indemnify TI and its representatives against any damages, costs, losses, and/or liabilities arising out of your non-compliance with the terms and provisions of this Notice. 

This Notice applies to TI Resources. Additional terms apply to the use and purchase of certain types of materials, TI products and services. 

These include; without limitation, TI’s standard terms for semiconductor products http://www.ti.com/sc/docs/stdterms.htm\), evaluation

modules, and samples \(http://www.ti.com/sc/docs/sampterms.htm\). 

Mailing Address: Texas Instruments, Post Office Box 655303, Dallas, Texas 75265

Copyright © 2018, Texas Instruments Incorporated

**CprE 458/558: Real-Time Systems**

Overload Handling in Real-Time Systems – Part 2

Feedback Control based EDF Scheduling

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

Feedback scheduling – motivation

One of the very successful areas in addressing performance 

in the presence of uncertainty \(e.g., workload or fault\) is 

that of Robust Control. Feedback of measured quantities to 

correct the behavior of a system has been a powerful 

concept that has made technological advances in 

applications such as amplifiers and avionics. 

Through concerted use of feedback control and its theoretical 

development, the concept has been used to deal with 

uncertainty inherent in most systems. 

It also needs to be stated that if a system characteristics is 

known precisely, then the feedback strategies are not 

useful; the open-loop strategies will outperform their 

feedback counterpart. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

**Feedback control technique**

Control

disturbance

Regulated 

variable

variables

s

**\+**

Controlled

Controller

Actuators

RT System

**-**

Sensors

Set 

Measured 

Points

variables

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

Feedback System Operation

• A typical feedback control system is composed of a 

controller, a plant to be controlled, actuators, and 

sensors. 



• Controlled/regulated variable, the quantity of the 

output that is measured and controlled/regulated. 

• The set point represents the correct value of the 

controlled variable. 

• The difference between the current value of the 

controlled variable and the set point is the error. 

• The manipulated/control variable is the quantity that is 

varied by the controller so as to affect the value of the 

controlled/regulated variable. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

Feedback system operation \(contd.\)

The system is composed of a feedback loop as follows. 

• The system periodically measures and compares the 

controlled variable to the set point to determine the 

error. 

• The controller computes the required control with the 

control function of the system based on the error. 

• The actuators change the value of the manipulated 

variable to control the system. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**FC-EDF**

• Task Model



*T *= \( *I *, *ET *, , 

*A S*, *D*\)

*i*

- Each Ti has logical versions: *I *= \( *T *, *T *,... *T *\) *i* 1

*i * 2

*ik*

- Each version has different execution time: 

*ET *= \{ *ET *, *ET *,... *ET *\}

*i* 1

*i * 2

*ik*

suppose *ET * *ET * ...  *ET*

*i* 1

*i * 2

*ik*

- Each version has different accuracy: *A *= \{ *A *, *A *,... *A *\}

*i* 1

*i * 2

*ik*

- Each task has a soft deadline 

*D * and a start time *S*

*i*

*i*

- Different versions of a task are called service levels. 

- A version with longer execution time and better 

accuracy is called a higher service level. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

FC-EDF -- Variables

• Set point: desired miss ratio 



\# *missed tasks *

 *miss ratio *=





\# *submitted tasks *

• Regulated/Measured variable: miss ratio

• Control variable: requested CPU utilization

*execution time*

*requested CPU utilization *= *deadline *− *current time*

• Actuators: Server Level Controller & 

Admission Controller– use server level 

controller, if the requirements are not satisfied, 

use admission controller. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7



FC-EDF Schematic

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**FC-EDF**

• PID Parameters Tuning

– Simulation experiments

– Modeling analysis

– Adaptive control to tune the parameters on-line

\[Read the paper for details\]

Reference: C. Lu, J.A. Stankovic, G. Tao, and S.H. Son, "Design and Evaluation of a Feedback Control EDF Scheduling Algorithm," In Proc. 

Real-Time Systems Symp. pp.56-67, 1999. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

Case study:

Feedback-based \(m,k\)-RMS Scheduler \[3\]

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Task model and performance index**

• Task Model - firm periodic tasks \[1,2\]

*T *= *c *, *p *, *m *, *k *

*c *: *comp*. *time*

*p *: *period*

*i*

*i*

*i*

*i*

*i*

*i*

*i*

• Tasks should meet mi deadlines for every ki consecutive 

instances

• Performance Index

– **Dynamic Failure Rate \(DFR\):** for a task Ti, it is the percentage of instances of the task miss their \(m,k\) guarantee. 

– **Marginal Quality Received \(MQR\):**

*m *− *m*

*m *: *the actual value used*

*i*

*i*

*i*

*MQR *=

*i*

*k *− *m*

*MQR *: *MQR of task T*

*i*

*i*

*i*

*i*

• To maximize the quality of tasks during overloading, 

*m* *i* is 

increased as much as possible

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**Feedback-based Adaptive Scheduler Architecture**

\+

PI Controller

Actuator

Set 

point

Admission Controller

Scheduler

-

CPU

Submitted tasks

Accepted tasks

Average Dynamic Failure Rate

CprE 458/558: Real-Time Systems \(G. Manimaran\)

12

Scheduling Example

**Task 1**

**120**

**Task 2**

**120**

**RMS**

**120**

**\(a\) T1: <4,8,2,10> T2: <4,6,1,5> **

**Task 1**

**120**

**Task 2**

**120**

**RMS**

**120**

**\(b\) T1: <4,8,4,10> T2: <4,6,2,5> **

**Task 1**

**120**

**Task 2**

**120**

**RMS**

**120**

**Task 1 misses its deadline**

**\(c\) T1: <4,8,6,10> T2: <4,6,3,5> **

CprE 458/558: Real-Time Systems \(G. Manimaran\)

13

**Example \(Cont.\)**

• We can increase the 

*m* values to increase the 

*i*

QoS when the system is underloaded, and 

decrease the values 

*m*

to handle overloading. 

*i*

• Feedback method can be used to adjust the 

*m * 

*i*

values. 

– Regulated/measured variable: *DFR*

– Set point: desired value of *DFR*

– Control variable: estimation factor, 

*e * , 

*tf * of *mi*

CprE 458/558: Real-Time Systems \(G. Manimaran\)

14

**Feedback-based Adaptive scheduling \(Cont.\)**

• Admit tasks based on minimum quality requirement

• The actual execution time of tasks are normally less 

than or equal to the worst case execution time used in 

the admission test

– Try to increase the quality as much as possible

– Use feedback method to adjust 

*m* . *i*

• Non-zero set point is used – achieve high CPU 

utilization and low dynamic failure rate

• is zero with respect to 

*mi * – 

*D * 

*FR * is changed with 

*DFR*

respect to the current 

*m * later

*i*

CprE 458/558: Real-Time Systems \(G. Manimaran\)

15

**Feedback control algorithm**

•  *etf *= *K *\( *DFR *− *DFR *\)

*t*

*s*

*t * 1

−

• *etf *= *etf *\+  *etf*

*t*

*t * 1

−

*t*

• *m *= *m *\+ *etf *\( *k *− *m *\)

*it*

*i*

*t*

*i*

*i*

*etf *: *estimation factor*

*K *: *controller*. *parameter*

*confine etf in *\[

\]

1

, 

0

*t*

*etf*

= 0.0

*inital*

CprE 458/558: Real-Time Systems \(G. Manimaran\)

16

**Online controller design**

*etf*

0

. 

1

max

• Initial Value of K: *K *=

=

= 10

*DFR *−

0

. 

0

1

. 

0

−

0

. 

0

*s*

• Halve K when DFR fluctuate across set point 

g

K on-line

design

ion

Controller

angin

parameters

ch vater

Control 

obs

Reference

signal

Output 

Controller

System

Output

• K

– high value will lead to fluctuation

– Low value will lead to a long time to reach the final value

CprE 458/558: Real-Time Systems \(G. Manimaran\)

17



*n*

*n*

*c*

*c * *m*

**Simulation studies ** *Load *=  *i*

*mkLoad *=  *i*

*i*

*i *=1

*p*

1

*p*

*k*

*i*

*i *=



*i*

*i*

• Feedback algorithm vs. iterative algorithm

MQR performance: Load = 1.1 and MKLoad varied

– MQR decreases as MKLoad increases

– ACET < WCET can be exploited to increase MQR

– Feedback algo offers better MQR than non-feedback algo

CprE 458/558: Real-Time Systems \(G. Manimaran\)

18



**Simulation studies \(Cont.\)**

Fairness \(f\): 

– Fairness obtained by the feedback approach is higher than 

that obtained by non-feedback algo \(MK-RMS\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

19

**Overload handling in RT Systems -- Summary**

• Imprecise computation & \(m,k\)-firm model

– Offers scheduling flexibility to achieve graceful 

degradation \(i.e., means to achieve predictable 

timing faults without violating system spec\)

– Applicable only to a class of applications

• Feedback-based resource management

– Periodically monitors system performance

– Adapts/controls system operation

– Suitable sensing, control, and regulated variables 

needed

CprE 458/558: Real-Time Systems \(G. Manimaran\)

20

**References**

\[1\] C. Lu, J.A. Stankovic, G. Tao, and S.H. Son, "Design and Evaluation of a Feedback Control EDF Scheduling 

Algorithm," In Proc. Real-Time Systems Symp. pp.56-67, 

1999. 

\[2\]** **Overload management in real-time control 

applications using \(m, k\)-firm guarantee

Ramanathan, P.; IEEE Transactions on Parallel and 

Distributed Systems, Volume 10, Issue 6, June 1999 

Page\(s\):549 – 559. 

\[3\] Suzhen Lin, Ph.D Dissertation, ISU, 2005. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

21

**CprE 458/558: Real-Time Systems**

Basic Concepts \(Contd.\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**Real-Time Systems - Issues**

• Resource Management \(RM\) Issues

– Scheduling, Fault-tolerance, Resource reclaiming, 

Communication

• Architectural Issues

– Computing subsystem, Communication subsystem, 

I/O subsystem

• Software Issues

– Requirements, specification, and verification, Real-

time languages, Real-time databases

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2



**Real-time Scheduling Paradigms – RM Issue**

• Allocate time slots for tasks onto processor\(s\). 

• \[i.e., Where and When a given task executes\]

• Objective: **predictably meeting task deadlines. **

• \(schedulability check, schedule construction\) 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**Preemptive vs Non-preemptive scheduling**

• **Preemptive Scheduling**

– Task execution is preempted and resumed later

– Preemption occurs to execute higher priority task. 

– Offers higher schedulability 

– Involves higher scheduling overhead due to context 

switching

• **Non-preemptive Scheduling** 

– Once a task starts executing, it completes its full 

execution

– Offers lower schedulability

– Less overhead due to less context switching

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

**Optimal scheduling -- definition**

• A **static scheduling** algorithm is said to be optimal if, for any set of tasks, it always produces a feasible 

schedule \(i.e., a schedule that satisfies the constraints 

of the tasks\) whenever any other algorithm can do so. 

• A **dynamic scheduling** algorithm is said to be optimal 

if it always produces a feasible schedule whenever a 

static algorithm with complete prior knowledge of all 

the possible tasks can do so. 

• Static scheduling is used for scheduling periodic tasks, 

whereas dynamic scheduling is used to schedule both 

periodic and aperiodic tasks. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**Architectural Issues**

• Predictability in: Instruction execution time, Memory 

access, Context switching, Interrupt handling. 

• RT systems usually avoid caches and superscalar 

features. 

• Support for error handling \(self-checking circuitry, 

voters, system monitors\). 

• Support for fast and reliable communication \(routing, 

priority handling, buffer and timer management\). 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Architectural Issues \(contd..\)**

• Support for scheduling algorithms \(fast preemptability, 

priority queues\). 

• Support for RTOS \(multiple contexts, memory 

management, garbage collection, interrupt handling, 

clock synchronization\). 

• Support for RT language features \(language 

constructs for estimating worst-case execution time of 

tasks\). 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**Requirement, Specification, Verification **

• **Functional requirements**: Operation of the system 

and their effects. 

• **Non-Functional requirements**: e.g., timing 

constraints. 

• F & NF requirements must be precisely defined and 

together used to construct the specification of the 

system. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**Requirement, Specification, Verification \(contd..\)**

• A **specification** is a mathematical statement of the 

properties to be exhibited by a system. It is abstracted 

such that 

– it can be checked for conformity against the 

requirement. 

– its properties can be examined independently of the 

way in which it will be implemented. 

• The usual approaches for specifying computing 

system behavior entail enumerating events or actions 

that the system participates in and describing orders in 

which they can occur. It is not well understood how to 

extend such approaches for real-time systems. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**Real-time Languages**

• Support for the management of time 

– Language constructs for expressing timing 

constraint, keeping track of resource utilization. 

• Schedulability analysis

– Aid compile-time schedulability check. 

• Reusable real-time software modules

– Object-oriented methodology. 

• Support for distributed programming and fault-

tolerance

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Real-time Databases**

Conventional database systems 

• Disk-based. 

• Use transaction logging and two-phase locking protocols to 

ensure transaction *atomicity* and *serializability*. 

• These characteristics preserve data integrity, but they also result in relatively slow and unpredictable response times. 

Real-time database system, issues include:

– transaction scheduling to meet deadlines. 

– explicit semantics for specifying timing and other constraints. 

– checking the database system’s ability of meeting transaction 

deadlines during application initialization. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**Introduction: Summary**

• Real-time systems require logical correctness and timeliness. 

• Real-time system consists of a controlling system, controlled 

system, and the environment. 

• Real-time systems are classified as: hard, firm, and soft RT 

systems. 

• Workload \(tasks\) are periodic, aperiodic, sparodic. 

• The notion of predictability is very important in real-time systems. 

• Important issues include: 

– scheduling, resource reclaiming, fault-tolerance, 

communication, architectural issues, system specification and 

verification, programming languages, and databases. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

12

**CprE 458/558: Real-Time Systems**

RMS and EDF Schedulers

\(Priority-driven Preemptive Schedulers\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**Priority-driven Preemptive Scheduling**

Assumptions & Definitions

• Tasks are periodic 

• No aperiodic or sporadic tasks

• Job \(instance\) deadline = end of period

• No resource constraints

• Tasks are preemptable

• Laxity of a Task Ti, 

C’i

Li = d

t

d

i – \(t \+ ci’\) 

i

where di: deadline; 

Laxity

t : current time; 

ci’ : remaining computation time. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2



**Rate Monotonic Scheduling \(RMS\)**

• **Schedulability check \(off-line\)** 

- A set of ***n*** tasks is schedulable on a 

uniprocessor by the RMS algorithm if the 

processor utilization \(utilization test\):



The term *n\(2**1/n **-1\)* approaches *ln 2*, 

\(0.69 as *n* → \). 

- This condition is sufficient, but not necessary. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**RMS \(cont.\)**

• **Schedule construction \(online\)** 

- Smaller the period higher the priority. 

E.g., Task with the smallest period is assigned the 

highest priority. 

- At any time, the highest priority task is executed. 

RMS is an optimal preemptive scheduling algorithm 

with fixed priorities. 

Static/fixed priority algorithm assigns the same 

priority to all the jobs \(instances\) in each task. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

**RMS Scheduler -- Example 1**

Task set: Ti = \(ci, pi\)

T1 = \(2,4\) and T2 = \(1,8\)

Schedulability check:

2/4 \+ 1/8 = 0.5 \+ 0.125 = 0.625 ≤ 2\(√2 -1\) = 0. 82

Active 

Active 

Active 

Tasks :

Tasks :

Tasks :

\{T2\}

\{T1\}

\{T1, T2\}

T 1

1

2

1

T2

T1

0

2

3

4

6

8

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**RMS scheduler -- Example-2**

Task set: Ti = \(ci, pi\)

T1 = \(2,4\) and T2 = \(4,8\)

Schedulability check:

2/4 \+ 4/8 = 0.5 \+ 0.5 = 1.0 > 2\(√2 -1\) = 0. 82

Active 

Active 

Active 

Active 

Tasks :

Tasks :

Tasks :

Tasks :

\{T2\}

\{T2, T1\}

\{T2\}

\{T1, T2\}

T 1

1

2

1

1

T2

T1

T2

0

2

3

4

6

8

Some task sets that FAIL the utilization-based schedulability test are also schedulable under RMS ➔ We need exact analysis \(necessary & sufficient\) CprE 458/558: Real-Time Systems \(G. Manimaran\)

6



**Earliest Deadline First \(EDF\)**

• **Schedulability check \(off-line\)** 

- A set of ***n*** tasks is schedulable on a 

uniprocessor by the EDF algorithm if the 

processor utilization. 



• This condition is both necessary and sufficient. 

- **Least Laxity First \(LLF\)** algorithm has the 

same schedulability check. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**EDF/LLF \(cont.\)**

• **Schedule construction \(online\)** 

– EDF/LLF: Smaller the deadline/laxity, higher 

the priority. 

E.g., Task with the smallest deadline/laxity is assigned 

the highest priority. 

– At any time, the highest priority task is 

executed. 

EDF/LLF is an optimal preemptive scheduling 

algorithm with dynamic priorities. 

Dynamic priority algorithm assigns different priorities 

to the individual jobs \(instances\) in each task. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**EDF scheduler -- Example**

Task set: Ti = \(ci, pi, di\)

T1 = \(1,3,3\) and T2 = \(4,6,6\)

Schedulability check:

1/3 \+ 4/6 = 0.33 \+ 0.67 = 1.0

Active 

Active 

Active 

Active 

Tasks :

Tasks :

Tasks :

Tasks :

\{T2\}

\{T2, T1\}

\{T1\}

\{T1, T2\}

T 1

1

1

2

1

T2

T2

T1

0

1

3

5

6

Unlike RMS, Only those task sets which pass the schedulability test are schedulable under EDF

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**RMS vs. EDF/LLF**

• RMS is an optimal preemptive scheduling 

algorithm with fixed priorities. 

• EDF/LLF is an optimal preemptive scheduling 

algorithm with dynamic priorities. 

• RMS schedulability properties can be 

analyzed for complex scenarios; rich theory 

exists and it is widely used in practice. 

• EDF/LLF offers higher schedulability than 

RMS, but it is more difficult to implement. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**CprE 458/558: Real-Time Systems**

RMS, EDF Schedulers \(contd\) --

Exact Analysis

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**Exact Analysis \(necessary & sufficient\)**

Critical Zone Theorem:

For a set of independent periodic tasks, if a 

task Ti meets its first deadline di <= pi, when all 

other higher priority tasks are started \(ie., 

ready\) at the same time, then it meets all its 

future deadlines with any other task start 

times. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2





**Completion Time Test**

Let there be n tasks ordered in decreasing 

priority. Consider any task Ti. The workload 

over \[0,t\] \(for arbitrary t > 0\) due to all tasks of 

equal or higher priority than Ti is given by



The term represents the number of times 

task Tj arrives in time t, and therefore 

represents its computational demand in time t. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**Completion Time Test \(Contd.\)**

Suppose that task Ti completes its execution 

exactly at time t. This means that the total 

cumulative demand from the i tasks up to time 

t, Wi\(t\), is exactly equal to t, that is, Wi\(t\) = t. A 

method for finding the completion time of task 

Ti, that is, the time at which Wi\(t\) = t, is known 

as completion time test. 



CprE 458/558: Real-Time Systems \(G. Manimaran\)

4



**Completion Time Test \(Contd.\)**

A task Ti is schedulable if Wi <= di, where 

Wi\(t\)=t. An entire task set is schedulable if this 

condition holds for all the tasks in the set. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**Completion Time Test — Example**

Task T1: c1 = 20; p1 = 100; d1 = 100. 

Task T2: c2 = 30; p2 = 145; d2 = 145. 

Task T3: c3 = 68; p3 = 150; d2 = 150. 

This task set fails the \(utilization-based\) schedulability 

test for RMS. So, perform completion time test for T1, 

T2, T3. Task T3’s completion time test is as follows. 

t0 = c1 \+ c2 \+ c3 = 20 \+ 68 \+ 30 = 118. 

t1 = W3\(t0\) = 2c1 \+ c2 \+ c3 = 40 \+ 68 \+ 30 = 138. 

W3\(t1\) = 2c1 \+ c2 \+ c3 = 40 \+ 68 \+ 30 = 138 = t1. 

Task T3 is schedulable\!; Tasks T1 and T2 too. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Deadline monotonic scheduling \(DMS\)**

• Task Ti: \(ci, pi, di\); with relative deadline di <= pi

\[Please note: “di” is a fixed parameter, whereas the “absolute 

deadline” used in EDF is a dynamic parameter\]



• Assigns priority based on di; smaller the di, higher the priority

• Similar to RMS utilization-based schedulability test, except 

ci/di used instead of ci/pi ∑ Ci/di ≤ n\(21/n – 1\)

• Similar to RMS exact analysis, except the ordering of tasks is based on di instead of pi

• Example: \(ci,pi,di\): \(3,20,7\), \(2,5,4\), \(2,10,9\). This task set is schedulable even though Sum\(ci/di\) > 1. 

• DMS is also an optimal fixed-priority scheduling algorithm; it is a generalization of RMS. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**RMS/DMS Schedulability test**

Example task set:

T1 = \(2,4\) 

T2 = \(3,12\)

NO

Is the task set 

Harmonic ? 

YES

RMS/DMS 

Is ∑U

Pass

i ≤ 1 ? 

utilization

based test

NO

YES

Fail

**NOT** 

Schedulable

RMS/DMS 

Schedulable

Schedulable

Exact analysis

Fail

**NOT** 

Schedulable

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**EDF Revisited: Schedulability test**

Different possible scenarios

Sufficient 

but **NOT**

necessary

If di ≥ pi

If di < pi

Necessary 

and 

Necessary 

sufficient

and 

sufficient

∑ Ci/pi ≤ 1

∑ Ci/di ≤ 1

Fail

Pass

Processor demand 

Schedulable

based test

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**Periodic task scheduling - summary**

Di = Pi

Di ≤ Pi

RMS

DMS

Static

Processor 

Exact Analysis

priority

Utilization test

EDF/LLF

EDF

Dynamic Processor 

Processor 

priority

utilization test

demand based 

\(U ≤ 1\)

test \(not covered\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**CprE 458/558: Real-Time Systems**

Resource Access Control 

Protocols

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**Assumptions**

• Periodic tasks

• Task can have resource access

• Semaphore is used for mutual exclusion

• RMS scheduling

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

**Background – Task State diagram**

• Ready State: waiting in ready queue

• Running State: CPU executing the task

• Blocked: waiting in the semaphore 

queue until the shared resource is free

• Semaphore types – mutex \(binary 

semaphore\), counting semaphore

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

Task State Diagram

scheduling

Activate

Termination

READY

RUN

Preemption

Signal 

Wait on 

free 

busy 

resource

resource

WAITING

Process/Task state diagram with resource constraints

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

**Priority Inversion Problem**

Priority inversion is an undesirable situation in 

which a higher priority task gets blocked \(waits 

for CPU\) for more time than that it is supposed 

to, by lower priority tasks. 



Example:

• Let *T1 *, *T2 *, and *T3* be the three periodic tasks with decreasing order of priorities. 

• Let *T1* and *T3* share a resource “S”. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**Priority Inversion -- Example**

• T3 obtains a lock on the semaphore *S* and enters its 

critical section to use a shared resource. 

• T1 becomes ready to run and preempts T3. Then, T1 

tries to enter its critical section by first trying to lock *S*. 

But, *S* is already locked by T3 * * and hence T1 is 

blocked. 

• T2 becomes ready to run. Since only T2 and T3 are 

ready to run, T2 preempts T3 while T3 is in its critical 

section. 

Ideally, one would prefer that the highest priority task 

\(T1\) be blocked no longer than the time for T3 to 

complete its critical section. However, the duration of 

blocking is, in fact, unpredictable because task T2 * * got executed in between. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Priority Inversion example**

Makes a 

A hi

R

gher esource **S** is 

request for 

priority avail

task able and T1 

resource **S** and waits for is 

a scheduled 

gets blocked

lower priority here

T1

task

Highest 

T1

T1

priority

T2 completes

Preempted by 

L1

T2

higher priority 

T3 completes

T3 is the 

T

task T1

2

Medium only 

priority active 

Preempted by 

task

higher pri

K3 ority 

K1

K2

task T2

T3

T3

T3

T3

Least 

priority

0

T1 and T3 

share 

Total blocking time for task T1 = \(K1\+K2\+K3\) \+ \(L1\)

resource 

**S**

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**Priority Inheritance Protocol**

Priority inheritance protocol solves the 

problem of priority inversion. 

Under this protocol, if a higher priority task T ***H*** 

is blocked by a lower priority task *T**L***, because 

*T**L*** is currently executing critical section 

needed by *T**H***, *T**L *** temporarily inherits the priority of *T**H***. 

When blocking ceases \(i.e., *T**L*** exits the critical section\), *T**L*** resumes its original priority. 

Unfortunately, priority inheritance may lead to 

deadlock. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8



**Priority Inheritance Protocol – Deadlock **

**Assume T2 > T1 \(i.e., T2 has high priority\)**

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**Priority Ceiling Protocol**

• Priority ceiling protocol solves the priority 

inversion problem without getting into 

deadlock. 

• For each semaphore, a *priority ceiling* is 

defined, whose value is the highest priority of 

all the tasks that may lock it. 

• When a task *Ti* attempts to execute one of its 

critical sections, it will be suspended unless its 

priority is higher than the priority ceiling of all 

semaphores currently locked by tasks other 

than *Ti*. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Priority Ceiling Protocol \(Contd.\)**

• If task *Ti* is unable to enter its critical section 

for this reason, the task that holds the lock on 

the semaphore with the highest priority ceiling 

is said to be blocking *Ti* and hence inherits the 

priority of *Ti*. 

• As long as a task *Ti* is not attempting to enter 

one of its critical sections, it will preempt every 

task that has a lower priority. 



CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**Priority Ceiling Protocol -- properties**

• This protocol is the same as the priority 

inheritance protocol, except that a task *Ti* can 

also be blocked from entering a critical section 

if any other task is currently holding a 

semaphore whose priority ceiling is greater 

than or equal to the priority of task *Ti*. 

• Prevents mutual deadlock among tasks

• A task can be blocked by lower priority tasks at 

most once

CprE 458/558: Real-Time Systems \(G. Manimaran\)

12

**Priority Celiling Protocol - Example**

• For the previous example, the priority ceiling 

for both CS**1** and *CS**2*** is the priority of *T**2***. 

• From time *t**0*** to *t**2***, the operations are the same as before. 

• At time t ***3***, *T**2*** attempts to lock *CS**1***, but is blocked since *CS**2*** \(which has been locked by 

*T**1***\) has a priority ceiling equal to the priority of *T**2***. 

• Thus *T**1*** inherits the priority of *T**2 *** and proceeds to completion, thereby preventing deadlock 

situation. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

13

**Resource access control -- example**

Task Ti

c

x

y

z

i

pi

ci

ci

ci

T1

2

8

2

0

0

T2

4

12

0

4

0

T3

2

6

1

1

0

T2 and T3 have access to a shared resource R

c xi : Task duration before entering the critical section

c yi : Critical section duration

c zi : Task duration after the critical section

ci = c x

y

z

i \+ ci \+ ci

By RMS, T3 > T1 > T2

CprE 458/558: Real-Time Systems \(G. Manimaran\)

14

**Schedules**

Locks R

RMS Schedule

Direct blocking of T3 by T2

Preempted by T3

Release R

T3

T1

T2

T3 T2

T1

T2 T3

T3

T2

0

2

4

6

7 8

10

11 12

14

16

Task Ti

c

x

y

z

i

pi

ci

ci

ci

Priority inversion of T3 by T1

T1

2

8

2

0

0

T2

4

12 0

4

0

RMS Schedule with Priority Inheritance Protocol

T3

2

6

1

1

0

Direct blocking of T3 by T2

T3

T1

T2

T3

T2

T3

T1

T3

T2

0

Inheritance blocking of T1 by T2

CprE 458/558: Real-Time Systems \(G. Manimaran\)

15

**Priority Inversion - Real-world Example**

• Mars Pathfinder mission \(July 4, 1997\)

• VxWorks \(real-time OS\), preemptive priority 

scheduling of threads \(e.g., RMS\)

• Priority inversion involving three threads:

– Information bus task \(T1\), meteorological data 

gathering task \(T3\), communication task \(T2\). 

Priority order: T1>T2>T3

– Shared resource: information bus \(used mutex\)

• Same situation as described in the previous example 

had occurred 

• Findings: Priority ceiling protocol was found to be 

disabled initially, then it was enabled online and the 

problem was corrected 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

16

**Priority Ceiling Emulation**

• Once a task locks a semaphore, its priority is 

immediately raised to the level of the priority 

ceiling of the semaphore. 

• Deadlock avoidance and block at-most-once 

result of priority ceiling protocol still holds. 

• Restriction: A task cannot suspend its 

execution within the critical section. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

17

**Modeling Blocking Time and Earlier Deadline**

• Blocking time \(Bi\) encountered by task Ti by 

lower priority tasks can be modeled by 

increasing Ti’s utilization by Bi/Pi. 

• Earlier deadline \(Di < Pi\) can also be modeled 

as blocking time for Ei = Pi – Di. 

• Net increase in task Ti’s utilization is 

\(Bi \+ Ei\) / Pi. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

18

**Modeling Blocking and Earlier Deadline \(Cont.\) **

• Schedulability Check \(sorted order T1 > T2 > … > Tn\) -- sufficient, but not necessary

*C*

*C*

\( *C *\+ *B *\+ *E *\)

1

2

*i*

*i*

*i*

1/

 *i * 1

,  *i * , 

*n*

\+

\+\+

 \(2 *i*

*i*

− \)

1

*p*

*p*

*p*

1

2

*i*

• Completion time Test \(Exact analysis\)

– Earlier deadline \(di < pi\) case: same as DMS exact analysis

– Blocking time \(Bi\) case: 

• Let Ci’ = Ci \+ Bi

• While calculating Wi\(t\) for task Ti, use Ci’ for task Ti and for all other higher priority tasks Tj simply use Cj

\(Note: Blocking Time calculation will be learned thro homework, 

a reading notes will be provided\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

19

**CprE 458/558: Real-Time Systems**

Combined Scheduling of 

Periodic and Aperiodic Tasks

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

Assumptions & Issues

• RMS scheduling algorithm used

• All periodic tasks start at time t=0 \(same as 

before\)

• Periodic tasks relative deadlines are equal to 

end of period

• Arrival times of aperiodic tasks unknown

• Schedulability of periodic tasks

• Response time for aperiodic tasks

• Implementation considerations

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

Background Scheduling Algorithm

• No server is created. 

• Aperiodic tasks are executed when there is no periodic 

task to execute. 

• Simple, but no guarantee on aperiodic schedulability 

**RMS**

Periodic tasks

High priority Queue

CPU

**FIFO/EDF…**

Aperiodic tasks

Low priority Queue

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**Normal **RMS schedule: Notice the holes

Task set: Ti = \(ci, pi\)

T1 = \(2,6\) and T2 = \(4,10\)

Schedulability check:

2/6 \+ 4/10 = 0.33 \+ 0.40 = 0.73 ≤ 2\(√2 -1\) = 0. 82

Background 

scheduling: basic 

idea --

T1

T 1

2

Scheduling 

1

T1

aperiodic tasks in 

0

2

6

8

10

holes like this

Hole

T2

T 1

2

2

T2

0

2

6

10

Schedule continues

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

Background Scheduling: Example

T1

T 1

2

3

4

1

T1

T1

T1

1 un

0

2

6

8 Hole110

Hole 18

2

2 unitits

2 units

T2

T 1

2

2

T2

T 2

2

0

2

6

10

12

14

16

18

Aperiodic 

tasks

1

2

A1

A2

0

2

6

10

12

14

16

18

Periodic tasks

**RMS**

High priority Queue

CPU

Aperiodic tasks

**FIFO**

Low priority Queue

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

Combined Scheduling 

• Creating a *periodic server* Ts=\(Cs, Ps\) for processing 

aperiodic workload. Create one or more server tasks. 

• Aperiodic tasks are scheduled in the periodic server’s 

time slots. This policy could be based on deadline, 

arrival time, or computation time. 

• Algorithms – all algorithms behave the same manner when 

there are enough aperiodic tasks to execute 

- Polling Server \(bandwidth non-preserving\) 

- Deferrable Server \(bandwidth preserving\)

- Priority Exchange Server \(bandwidth preserving\)

- Sporadic Server \(bandwidth preserving\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

Polling Server

• A periodic server is created. 

• If there are no aperiodic tasks at an invocation of the 

server \(as per RMS\), the server suspends itself during 

its current period and gets invoked again at its next 

period. 

• If there are enough aperiodic tasks in an invocation, it 

serves up to Cs capacity. 

• The computation time allowance for the server is 

replenished at the start of its period

• Include Ts in the task set and do schedulability test 

• Poor response time for aperiodic tasks

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**Polling **

Ts should 

This 

**serve**

be sch

aperiodic

**r: Example**

eduled here 

task 

as per RMS. However, as 

cannot be scheduled 

there is no aperiodic task to 

now as there is no 

Task set: Ti = \(c

T i, pi

ask \)

schedule, Ts suspends itself 

server available till 

set: Ti = \(ci, pi\)

and is again available T1 

on = 

ly \(1,4\) 

at , T2 = 

T \(2,6\)

1 = \(1 an

,4\) d 

, T

T s = 

2 = \(2,5\)

time = 5

\(2,6\) and Ts = \(2,5\)

time = 5

T1

0

4

8

12

16

20

24

T2

Server becomes 

Server becomes 

available and available and can 

schedules schedule for 2 

aperiodic task units. However, 

1

3

6 7

10

12 13

15

Waits till 18

20

24

A1 for 2 units

Waits till aperiodic task A2 

Aperiodic 

Preempted 

time = 10 needs only 1 

time = 15

by T1

tasks

2

1

2

A1

A2

A3

A3

0

2

5

8

10

13

15 16 17 18

24

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**Polling server: Example \(no animations\)**

Task set: Ti = \(ci, pi\)

T1 = \(1,4\) , T2 = \(2,6\) and Ts = \(2,5\)

T1

0

4

8

12

16

20

24

T2

1

3

6 7

10

12 13

15

18

20

24

Aperiodic 

tasks

2

1

2

A1

A2

A3

A3

0

2

5

8

10

13

15 16 17 18

24

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**Polling server: Schedulability Analysis**

• Schedulability analysis involves

– Schedulability of periodic tasks

– Schedulability of Aperiodic tasks

• Schedulability of periodic tasks can be 

evaluated by introducing a periodic task 

equivalent to the server. Therefore, the 

schedulability test is:

∑i=1 to n \(Ci / Pi\) \+ \(Cs / Ps\) ≤ \(n\+1\)\[2 1/\(n\+1\) -1\]

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Polling server: Schedulability Analysis**

• Aperiodic task guarantees:

– Consider a single aperiodic task Ai, arrived 

at ra, with computation time Ca and deadline 

Da. Since an aperiodic task can wait at most 

for one period before receiving service, if Ca 

≤ Cs the request is certainly completed 

within two server periods. Thus it is 

guaranteed if 2Ps ≤ Da

Ca

Cs

0

Ps

Ps

r

d

a

a

Da > Ps

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**Polling server: Schedulability Analysis**

• Aperiodic task guarantees:

– For arbitrary computation times, the 

aperiodic task is certainly completed in 

ceil\(Ca/Cs\) server periods; hence it is 

guaranteed if

• Ps \+ ceil\(Ca/Cs\) \* Ps ≤ Da

CprE 458/558: Real-Time Systems \(G. Manimaran\)

12

Deferrable Server

• A periodic server task is created. 

• When the server is invoked with no 

outstanding aperiodic tasks, the server does 

not execute but defers its assigned time slot. 

• When an aperiodic task arrives, the server is 

invoked \(as per RMS\) to execute aperiodic 

tasks and maintains its priority. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

13

Deferrable Server \(Contd.\)

• The computation time allowance for the server 

is replenished at the start of its period. 

• Provides better response time for aperiodic 

tasks than Polling server

• Under overload, deadlines are missed 

predictably. 

• Similar schedulability test like polling server

CprE 458/558: Real-Time Systems \(G. Manimaran\)

14

**Deferrable Server: Example**

Server defers 

Task set: Ti = \(ci, pi\)

its capacity to 

handle any 

T1 = \(1,4\) , T2 = \(2,6\) and Ts = \(2,5\)

future 

aperiodic task

T1

0

4

8

12

16

20

24

T2

Why is A2 

not 

scheduled 

at time = 8 

Don’t need 

itself??? 

1

3Don’t n

6

eed 

8

10

to wait 12

till 13

15

18

20

24

Aperiodic 

to wait till 

time = 10

time = 5

T1 runs from 8 to 

tasks

2

9 and hence Ts a 

1

lower priority task 

A1

A2

cannot run till 9

0

2

4

8 9

24

CprE 458/558: Real-Time Systems \(G. Manimaran\)

15

Priority Exchange Server

• A periodic server task is created. 

• When the server invoked, the server runs if 

there are any outstanding aperiodic tasks. 

• If no aperiodic task exists, the high priority 

server exchanges its priority with a lower 

priority periodic task for a duration of Cs’, 

where Cs’ is the remaining computation time 

of the server. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

16

Priority Exchange Server \(Contd.\)

• In this way, the priority of the server 

decreases, but its computation time is 

maintained. 

• The computation time allowance for the server 

is replenished at the start of its period. 

• As a consequence, the aperiodic tasks get low 

preference for execution. Offers worse 

response time compared to Deferrable Server. 

• Better schedulability bound for periodic task 

set compared to Deferrable Server. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

17

**Priority Exchange server: example**

Aperiodic task exists to 

utilize the server capacity

TH

Cs

TS

T**f**

TL

No more Aperiodic tasks to 

Server executing at TL’s 

utilize the server capacity

priority when there are 

aperiodic tasks to serve

TH

e

Cs - e

TS

T**f**

Cs - e

TL

T**L** executing at the 

T**L** executing at its own 

server’s priority

priority

CprE 458/558: Real-Time Systems \(G. Manimaran\)

18

Sporadic Server

• This algorithm allows to enhance the average 

response time for aperiodic tasks without 

degrading the utilization bound for periodic 

task set

• This is achieved by varying the points at which 

the computation time of the server is 

replenished, rather than merely at the start of 

each server period. 

• In other words, any spare capacity \(i.e., not 

being used by periodic tasks\) is available for 

an aperiodic task on its arrival. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

19

**Spora**

Si

**dic**

nce no ** server: example**

aperiodic 

task is 

Server has the 

there, the 

Task set: T

highest 

i = \(ci, pi\)

server 

priority

T1 = \(3,10\) , T2 = \(4,15\) and Ts = \(2,8\)

defers its 

capacity

And, replenishes 

its capacity at 

T1

time = 

current\_time \+ 

period

0

2

4

10

12

15 16

20

24

T2

Server has 

Server 

capacity to 

schedules the 

schedule A2

aperiodic task 

right away with 

its ca

5

pacity

9

Server has no 15

18

20

24

Aperiodic 

capacity to 

handle

tasks

2

1

A2

A1

0

2

4

7

10

12

24

CprE 458/558: Real-Time Systems \(G. Manimaran\)

20

**Priority-driven preemptive scheduling- summary **

• Scheduling algorithms

– RMS & EDF utilization test

– RMS & DMS Exact analysis

• Combined Scheduling

– Polling, Deferrable, PE, Sporadic servers

• Resource Access Control

– Priority Inversion

– Priority Inheritance & Pri. Ceiling Protocols

– Schedulability tests accounting Blocking

CprE 458/558: Real-Time Systems \(G. Manimaran\)

21

**Scheduling tasks with precedence relations**

Conventional task set

\{T1, T2\}

Scheduler

task set with 

precedence constraints

T1

T2

Modify task parameters 

in order to respect 

Scheduler

precedence constraints

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**Modifying the task parameters for RMS**

• While using the RMS scheduler the task 

parameters \(ready time\) need to be 

modified in order to respect the 

precedence constraints

Ti

Tj

• Rj\* ≥ Max \(Rj, Ri\*\) where Ri\* is the 

modified ready time of the task Ti

• Priority Prioi ≥ Prioj \(strictly greater\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

**Modifying ready times for RMS: example**

T1

T2

1

2

Initial Task Parameters

Task

Ri

Ci

Di

T3

T4

2

1

T1

0

1

5

T2

5

2

7

T3

0

2

5

T5

T4

0

1

10

3

T5

0

3

12

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**Modifying the Ready times for RMS**

R1 = 0

R2 = 5

T1

T2

1

2

R4’ = max\(R1, R2,R4\)

R3’ = 

Initial Task Parameters

max\(R1, R3\) R3 = 0

R3’ = 0

Task

Ri

Ci

Di

T3

T4 R4 = 0

R4’ = 5

2

1

T1

0

1

5

T2

5

2

7

T3

0

2

5

T5

R5 = 0

T4

0

1

10

3

R5’ = 5

T5

0

3

12

R5’ = max\(R3’, R4’,R5\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

**Modified Ready times for RMS**

R1 = 0

R2 = 5

T1

T2

1

2

Modified Task Parameters

R3’ = 0

Task

Ri

Ci

Di

T3

T4

R4’ = 5

2

1

T1

0

1

5

T2

5

2

7

T3

0

2

5

T5

T4

5

1

10

3

R5’ = 5

T5

5

3

12

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**Assigning task priorities for RMS**

Assume all tasks of a 

R1 = 0

R2 = 5

connected component 

T1

T2

have the same period. 

1

2

Therefore, as per RMS 

all tasks will have a tie. 

We assign priorities to 

break the ties. 

R3’ = 0

T3

T4

R4’ = 5

Modified Task Parameters

2

1

Task Ri

Ci

Di

Priority

T1

0

1

5

3

T2

5

2

7

4

T5

3

R5’ = 5

T3

0

2

5

2

T4

5

1

10

1

T5

5

3

12

0

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Modifying task parameters for DMS**

• While using the DMS scheduler the task 

parameters \(ready time, relative 

deadline\) need to be modified in order to 

respect the precedence constraints

Ti

Tj

• Rj\* ≥ Max \(Rj, Ri\*\)

• Dj\* ≥ Max \(Dj, Di\*\) 

• Prioi ≥ Prioj \(Strictly greater\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**Modifying the Deadlines for DMS**

The procedure to modify 

D1 = 5

D2 = 7

the ready times is same 

as that of RMS

T1

T2

1

2

D4’ = max\(D1, D2,D4\)

D3’ = 

max\(D1, D3\)D3 = 5

D3’ = 5

T3

T4 D4 = 10

D4’ = 10

Modified Task Parameters

2

1

Task

Ri

Ci

Di

T1

0

1

5

T2

5

2

7

T5

D5 = 12

3

D5’ = 12

T3

0

2

5

T4

5

1

10

D5’ = max\(D3’, D4’,D5\)

T5

5

3

12

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**Modifying task parameters for EDF**

• While using the EDF scheduler the task 

parameters need to be modified in order 

to respect the precedence constraints

Ti

Tj

• Rj\* ≥ Max \(Rj, \(Ri\* \+ Ci\)\)

• Di\* ≥ Min \(Di, \(Dj\* – Cj\)\) 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**Modifying the Ready times for EDF**

R1 = 0

R2 = 5

T1

T2

1

2

R4’ = max\(R1\+C1, R2\+C2,R4\)

R3’ = max\(R1 \+ C1, R3\)

Initial Task Parameters

R3 = 0

R3’ = 1

Task

Ri

Ci

Di

T3

T4 R4 = 0

R4’ = 7

2

1

T1

0

1

5

T2

5

2

7

T3

0

2

5

T5

R5 = 0

T4

0

1

10

3

R5’ = 8

T5

0

3

12

R5’ = max\(R3’\+C3, 

R4’\+C4,R5\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Modifying the Ready times for EDF**

R1 = 0

R2 = 5

T1

T2

1

2

Modified Task Parameters

R3’ = 1

Task

Ri

Ci

Di

T3

T4

R4’ = 7

2

1

T1

0

1

5

T2

5

2

7

T3

1

2

5

T5

T4

7

1

10

3

R5’ = 8

T5

8

3

12

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**Modifying the Deadlines for EDF**

D2’ = Min\( \(D4’ – C4\), \(D3’ – C3\), D1\)

D1 = 5

D2 = 7

D1’ = 3

D2’ = 7

T1

T2

D2’ = Min\( \(D4’ – C4\), D2\)

1

2

Modified Task Parameters

D3 = 5

Task

Ri

Ci

Di

T3

D3’ = 5

T4

D4 = 10

D4’ = 9

2

1

T1

0

1

5

T2

5

2

7

T3

1

2

5

T5

T4

7

1

10

3

D5 = 12

T5

8

3

12

D3’ = Min\( \(D5 – C5\), D3\)D4’ = Min\( \(D5 – C5\), D4\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

12

**Modifying the Deadlines for EDF**

D1’ = 3

D2’ = 7

T1

T2

1

2

Modified Task Parameters

Task

Ri

Ci

Di

T3

D3’ = 5

T4

D4’ = 9

2

1

T1

0

1

3

T2

5

2

7

T3

1

2

5

T5

T4

7

1

9

3

D5 = 12

T5

8

3

12

CprE 458/558: Real-Time Systems \(G. Manimaran\)

13

**CprE 458/558: Real-Time Systems**

Overload Handlin in Real-Time Systems 

• Imprecise Computations \(Part 1\)

• \(m,k\)-firm task model \(Part 2\)

• Best-Effort Scheduling \(Part 3\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**How Overloads occur? **

• Dynamic workload beyond anticipated

– Aperiodic tasks and/or dynamically arriving 

periodic tasks

• Unanticipated faults

– Frequency and duration of the faults

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

**Imprecise Computational Model**

• A way to avoid timing faults during transient 

overloads and a way to introduce fault-

tolerance by graceful degradation is the use of 

Imprecise Computation \(IC\) technique. 

• The IC model provides scheduling flexibility by 

trading off result quality to meet task 

deadlines. A task is divided into a *mandatory *

and an *optional part*. 

• The mandatory part must be completed before 

the task's deadline for an acceptable quality of 

result. ** **

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**Precise vs Imprecise results**

• The optional part, which can be skipped in 

order to conserve system resources, refines 

the result. 

• A task is said to have produced a **precise** * *

result if it has executed its mandatory as well 

as optional parts before its deadline; 

• otherwise it is said to have produced 

**imprecise **\(i.e., approximate\) result when it 

executes the mandatory part alone. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

**Monotone vs 0/1 constraint tasks**

• There are two types of imprecise 

computational tasks, namely, **monotone **

**tasks** and **0/1 constraint tasks**. 

• A task is *monotone* if the quality of its 

intermediate result does not decrease as it 

executes longer. 

• An imprecise task with *0/1 constraint* requires 

the optional part to be either fully executed or 

not at all. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**Applications of Imprecise Computations**

• Applications are where one may prefer timely 

imprecise results to late precise results. 

• In image processing, it is often better to have 

frames of fuzzy images in time than perfect 

images. 

• In radar tracking, it is often better to have 

estimates of target locations in time than 

accurate location data too late. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Applications \(Contd’\)**

• For example, in a tracking and control system, 

a transient fault may cause tracking 

computation to terminate prematurely and 

produce an approximate result. No recovery 

action is needed if the result still allows the 

system to maintain a track of its targets. 

• Similarly, as long as the approximate result 

produced by a control law computation is 

sufficiently accurate for the controlled system 

to remain stable, the fault that causes the 

computation to terminate prematurely can be 

tolerated. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**Error Function & Objective Functions**

• Monotone task, Ti: \(mi, oi, di\)

Mandatory comp. time \(mi\), optional comp time \(oi\), 

deadline \(di\)

– Error ei = F\(oi, ki\) = oi – ki. 

where ei: Error incurred by task Ti

ki: optional portion completed

• Minimize the total error

• Minimize the number of optional tasks 

discarded

– Shortest processing time first strategy

• Minimize the number of tardy tasks

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**Algo F \(Min Total Error, monotone task, **

**identical weights, optimal, O\(n logn\)\)**

• Treat all mandatory tasks as optional. 

• Use *ED policy* to schedule all the tasks. \(St\)

• If a feasible schedule is found, precise 

schedule is obtained, stop. 

• Else use ED to schedule mandatory tasks. 

\(Sm\) 

• If feasible schedule is not found, infeasible 

schedule, stop. 

• Else use Sm as a template, transform St into 

an optimal schedule that is feasible and 

minimizes the total error. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**Scheduling to Minimize Total Error \(for **

**IC tasks with 0/1 constraints\)**

• The general problem of optimal scheduling of IC tasks 

with 0/1 constraints is NP-complete. 

• Optimal schedule: A schedule in which the number of 

discarded optional tasks is minimum. 



• Special case: Optional tasks have equal comp. time

– LDF algorithm 

• Same ready time

• O\(n logn\) complexity

– DFS algorithm

• Arbitrary ready time

• O\(n^2\) complexity

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Scheduling periodic tasks**

• Error-cumulative

– Tracking and control applications

• Error-non-cumulative

– Image enhancement and speech processing 

applications

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**\(m, k\) firm real-time tasks**

• A periodic task is said to have an \(m,k\)-firm guarantee 

if it is adequate to meet the deadlines of m out of k 

consecutive instances of the task, where m ≤ k. 

• The adaptive QoS management problem

– Admit the tasks to satisfy at least the \(m,k\) guarantee

– Maximize the QoS of admitted tasks beyond the \(m,k\) 

property, at run-time, without violating \(m,k\) property of any of the admitted tasks. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

12

**\(m,k\)-firm deadline model**

• A periodic task is said to have an \(m,k\)-firm guarantee 

if it is adequate to meet the deadlines of m out of k 

consecutive instances of the task, where m <= k. 

• Periodic task: \(pi, ci, mi, ki\)

• A flexible method for expressing timing requirements. 

• Allows “graceful degradation” during overloads. 

• Choose values for m and k such that desired m/k is 

obtained. 

• \(1,1\)-firm ➔ hard real-time task. 

• Apps: Radar tracking, Automobile control

• \(m,k\) vs. imprecise computation \(IC\): In \(m,k\) model 

instances can be dropped in full; in IC, portion of a 

instance can be dropped. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

13

**Task model and performance index**

• Task Model - firm periodic tasks \[1,2\]

*T *= *c *, *p *, *m *, *k *

*c *: *comp*. *time*

*p *: *period*

*i*

*i*

*i*

*i*

*i*

*i*

*i*

• Tasks should meet mi deadlines for every ki consecutive 

instances

• Dynamic failure \(Timing failure\) is said to occur when 

\(m,k\) property is violated for one or more tasks. 

• State diagram model – to keep track of temporal history 

of task execution \(M: Meeting deadline, m: missing 

deadline\). This was discussed in the lecture. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

14

**MK-RMS Schedulability Check \[2\]**

•

Utilization-based MK-RMS-schedulability check \(sufficient, but not necessary\)

*mk Load*



*n*

*c *

=

*m*

*i*

*i*

*i *=1

*p * *k*

*i*

*i*





MKLoad <= *n\(2**1/n **-1\)*

•

Classification of mandatory and optional instances 



- Instances of task Ti activated at times api is mandatory if

 *a * *m * *k *

*a *= 

*i*





 *i *

*a *=

, 

1

, 

0

, 

2 

 *ki * *mi *

•

Optional instance is assigned the lowest priority

•

Mandatory instances are assigned priority as per RMS

CprE 458/558: Real-Time Systems \(G. Manimaran\)

15

**References**

1. J.W.S. Liu, K.J. Lin, W.K. Shih, A.C. Yu, 

J.Y.Chung, and W. Zhao, “Algorithms for 

scheduling imprecise computations,” *IEEE *

*Computer, * vol.24, no.5, pp.58-68, May 1991. 

2. P. Ramanathan, “Graceful degradation in 

real-time control applications using \(m,k\)-firm 

guarantee,” In Proc. of Fault-Tolerant 

Computing Symposium, pp.132-141, 1997. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

16

**CprE 458/558: Real-Time Systems**

Overload Handling in RT Systems – Part 3

Best Effort Scheduling

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

Best-Effort Scheduler

• No schedulability check

• Schedule construction – online

• Overload handling \(handling timing faults\)

– Value based scheduling

– Imprecise computation

– \(m,k\)-firm task scheduling

• Value based scheduling

– Task Ti : <Ci, Pi, Vi> where Vi is the value offered by Ti. 

– If Ti finishes by di, it offers a value of Vi. 

Else, it offers a value of 0 \(sometimes a negative value\). 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

Best-Effort Scheduler \(Contd.\)

• Deadline scheduler \(eg., EDF\) – good for 

under/normal load

• Value-based scheduler \(e.g., HVDF: Highest 

Value Density First\) – good for overload

• Hybrid \(Adaptive\) scheduler: good for all loads

• Heuristics Hi = function\(value, deadline\). 

• Example: Heuristic Hi = EDF “\+” HVDF that 

schedules tasks based on the deadline; when 

there is a tie in priority, breaks the tie in favor of 

HVDF policy. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

HVDF – Highest Value Density First

• Value density = Vi/Ci 

\(i.e., value per unit computation time\). 

• Higher the value density, higher the 

importance and hence higher the priority. 

• HDVF scheduler schedules tasks based on 

“value density” 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

Competitive Analysis of BE scheduler

• The competitive factor, BA , of an on-line 

scheduling algorithm is defined as

*V *\( *S*\)

*A*

 *B *, 

*for all S*

*V *\( *S*

*A*

\)

*CA*

Where 

S: a given task set

VA\(S\): value produced by given scheduler A

VCA\(S\): value produced by Clairvoyant scheduler, the 

scheduler that knows complete knowledge of the 

workload a priori \(i.e., at the beginning itself\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

Competitive Analysis of BE scheduler \(contd.\)

• The upper bound on the competitive factor for any 

on-line scheduling is

1

\( \+1\+ 2  \)

Where Y = highest value density / lowest value density

• When Y = 1 \(i.e., Vi = Ci\), the competitive factor is 

0.25. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Overload handing -- Summary**

• Imprecise computations

– Monotone model, 0/1 model

– For both periodic and aperiodic tasks

• \(m,k\)-firm task model

– For periodic tasks only

– Graceful degradation during overloads

• Feedback control based scheduler

– Predictable performance under load uncertainty

• Best effort schedulers

– No guarantees on meeting deadlines

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7





**Real-Time LAN –**

**Controller Area Network \(CAN\)**

**Presented by**

***Souradeep Bhattacharya***

***Instructor: *****Prof. Manimaran Govindarasu**

**CprE 4580/5580: Real-Time Systems**

**Department of Electrical and Computer Engineering**

**Electrical and Computer Engineering**

1



Presentation Outline

❖ Introduction to LAN and Fieldbus

❖ Overview of CAN

❖ Working of CAN

❖ Project Demo

❖ Example Project Ideas

**Electrical and Computer Engineering**

2





LAN – Basic Concepts

A local area network \(LAN\) interconnects

network equipment within a limited area. 

Ethernet and Wi-Fi are the two most common

technologies used for LAN. 

Key Features:

▪

*Limited Coverage*

▪

*High Data Transfer Speeds*

▪

*Resource Sharing*

▪

*Secure and Controlled Access*

**Ref: https://en.wikipedia.org/wiki/Local\_area\_network**

**Electrical and Computer Engineering**

3





Common Topologies in LAN

Ring Topology

Bus Topology

➢ Easy Installation

➢ Less Amount of Cable

➢ Number of supported devices limited by the length of 

➢ Low Cost

the backbone cable

➢ Efficient Data Transfer

➢ Single Point of Failure

**Electrical and Computer Engineering**

4



Application of LAN in ICS Environments

LAN communication technologies and products used in:

▪

Intra-vehicular communication

▪

Robotics

▪

Process control industries

▪

Smart Grid and Energy Systems

▪

Maritime and Railway Systems

▪

Building Automation

Bus topology \(Fieldbus\) is most common in **legacy and embedded industrial control networks** **Electrical and Computer Engineering**

5



How do we connect these control devices? 

➢ With conventional systems, data is exchanged by means of dedicated signal lines or wires. 

➢ But this is becoming increasingly difficult and expensive as control functions become ever more complex. 

➢ In the case of complex control systems in particular, the number of connections cannot be increased much further. 

➢ Solution: Use Fieldbus networks for connecting the control devices **Electrical and Computer Engineering**

6





Fieldbus Networks: basic motivation

**Why use Fieldbus Networks? **

**To avoid this…**

**Traditional Wiring - *two pairs of cables can substitute all typical connections*****. **

**Electrical and Computer Engineering**

7





Fieldbus Real-Time Communication Architecture

**Three different communication networks in real-time application. **

**Electrical and Computer Engineering**

8



Fieldbus Networks

Fieldbuses are communication technologies and products used in vehicular, automation, and process control industries. 

**1\) Proprietary Fieldbuses \(Closed Fieldbuses\)**

Proprietary Fieldbuses are the intellectual property of a particular company or body. 

**2\) Open Fieldbuses**

For a Fieldbus to be Open, it must satisfy the following criteria. 

a\) The full Fieldbus Specification must be published and available at a reasonable price. 

b\) Critical ASIC components must be available, also at a reasonable price. 

c\) Well defined validation process, open to all of the Fieldbus users. 

**Electrical and Computer Engineering**

9



Fieldbus Advantages

1\) Reduces the complexity of the control system in terms of hardware outlay. 

2\) Resulting in the reduced complexity of the control system, project design engineering is made simpler, more efficient, and conversely less expensive. 

3\) By selecting a recognized and well-established system, this will make the Fieldbus equipment in your plant or plants interchangeable between suppliers. 

4\) The need to be concerned about connections, compatibility, and other potential problems is eradicated. 

**Electrical and Computer Engineering**

10





What constitutes a Fieldbus? 

The specification of a Fieldbus should ideally cover all 

of the seven layers of the OSI model. 

**Electrical and Computer Engineering**

11



Fieldbus: OSI layer details

▪

Physical Layer \[1\] What types of signals are present, levels, representation of 1's and 0's, what type of media connects, etc. 

▪

Link Layer \[2\] Techniques for establishing links between communicating parties. 

▪

Network Layer \[3\] Method of selecting the node of interest, method of routing data. 

▪

Transport Layer \[4\] Ensuring what was sent arrives at the receiver correcting any correctable problems. 

▪

Session Layer \[5\] Not applicable to Fieldbuses. 

▪

Presentation Layer \[6\] Not applicable to Fieldbuses. 

▪

Application Layer \[7\] Meaning of data. 

▪

The best way to cover layer 7 is to define standard profiles for standard devices. 

**Electrical and Computer Engineering**

12



What Fieldbus Networks are currently on the market? 

Some of the Fieldbus technologies currently on the market 

▪

AS-Interface \(Europe\)

▪

**CAN \(German, Bosch, we will discuss in detail\)**

▪

Interbus \(German, Phoenix Contract\)

▪

ModBus \(America, Modicon\)

▪

Profibus \(German, Siemens\)

▪

EtherNet \(America, AB\)

▪

Controlnet \(America, AB\)

**Electrical and Computer Engineering**

13



Controller Area Network \(CAN\)

❖ Fast serial bus. 

❖ Advantages:

✓ *Low cost*

❖ Designed to provide an efficient and reliable

✓ *Handles high sensor data volumes with*

link between sensors and actuators. 

*minimal latency. *

✓ *Supports integration of advanced control*

*systems, sensors, actuators, etc. *

❖ CAN uses a twisted pair cable \(dual-wire\) to

communicate at speeds up to 8Mbit/s \(max\)

with up to 255 devices. 

❖ CAN Bus supports multiple data rates – high

data rate bus, low data rate bus. 

**Electrical and Computer Engineering**

14





Types of CAN

**Electrical and Computer Engineering**

15



CAN Features

1\) Any node can access the bus when the bus is quiet. 

2\) Non-destructive bit-wise arbitration to allow 100% use of the bandwidth without loss of data. 

3\) Variable message priority based on 11-bit / 29-bit packet identifier. 

4\) Peer-to-peer and multi-cast reception. 

5\) Automatic error detection, signaling and retries. 

6\) Data packets 4 or 8 bytes long. 

7\) Asynchronous communication \(Even Triggered\). 

**Electrical and Computer Engineering**

16





Applications of CAN

**Intra-vehicular communication**

**Concrete State Monitor & Control System**

**Rear Active **

**Stabilizer ECU**

**Airbag **

**Control ECU**

**Gear Ratio **

**Steering ECU**

**Body Control **

**ECU**

**Powertrain **

**Engine **

**LEGEND**

**ECU**

**Control ECU**

**CAN bus**

**Brake Control **

**ECU**

**Lighting **

**Branch Information Flow**

**Control ECU**

**Information Sink Node**

**ECU**

**CAN Node**

**Electrical and Computer Engineering**

17





Applications of CAN

**MRI Cooling System**

**Tram Energy Recycle System**

**Electrical and Computer Engineering**

18





CAN Standard

**CAN Layered ISO 11898 Standard \(conforming to OSI model\)**

**Electrical and Computer Engineering**

19





CAN Architecture

**Standard CAN \(11-bit\)**

**Extended CAN \(29-bit\)**

**Electrical and Computer Engineering**

20





Working of the CAN Network: *Intra-vehicular Communication*

**Electrical and Computer Engineering**

21





Working of the CAN Network: *Intra-vehicular Communication*

**A schematic diagram of a current in-vehicle network**

**Electrical and Computer Engineering**

22





Working of the CAN Network: *CAN Message Structure*

**Electrical and Computer Engineering**

23





Working of the CAN Network: *Transmission/Reception*

***CAN bus versus point-to-point ***

***connections***

▪

By introducing a single bus as the only 

means of communication, as opposed to 

the point-to-point network, we traded off 

channel access simplicity for circuit 

simplicity

▪

Since two devices might want to transmit 

simultaneously, we need to have a MAC 

protocol to handle the situation. 

▪

CAN manages MAC issues by using a 

unique identifier for each of the outgoing 

messages

▪

The identifier of a message represents 

its priority. 

**Electrical and Computer Engineering**

24



Working of the CAN Network: *Implicit collision handling *

➢ If two messages are simultaneously sent over the CAN bus, the bus takes the “logical AND” of all of them. 

➢ Hence, the message identifiers with the lowest binary number get the highest priority. 

➢ Every device listens on the channel and backs off when it notices a mismatch between the bus’s bit and its identifier’s bit. 

**Electrical and Computer Engineering**

25





Working of the CAN Network: *Implicit collision handling *

**Electrical and Computer Engineering**

26



Project Demo

**Electrical and Computer Engineering**

27





***Project ***

Problem 

Project 

Implementation 

Experimental 

Design Solution

Conclusion

Statement

Resources

Description

Evaluation

***Overview***

**Title:**

Implementation of real-time CANbus communication to study the protocol performance **Option:**

Type 2: Implementation-oriented Project

**Objectives:**

➢ Development of a circuit using Arduino UNO and Raspberry Pi to implement a real-time CANbus communication architecture. 

➢ The obtained CAN messages are then monitored to demonstrate the bitwise arbitration method for contention resolution. 

**Electrical and Computer Engineering**

28





Project 

Problem 

***Project ***

Implementation 

Experimental 

Design Solution

Conclusion

Overview

Statement

***Resources***

Description

Evaluation

***Platforms & Tools***

***Controller Area Network \(CAN\) Protocol***

**Hardware:**

**Features:**

➢ *Raspberry Pi 3 Model B\+*

*Peer-to-peer communication. *

➢ *Arduino UNO*

*Short messages broadcasted over network. *

➢ *MCP2515 CANbus Transceiver Board*

*Logic-high = 0, Logic-low = 1. *

➢ *10kΩ Potentiometer Sensor*

*Robust noise immunity and fault tolerance. *

*Lacks data security and privacy*

**Software:**

➢ *Raspbian OS \(Linux & Python based\) for RPi*

➢ *Arduino UNO IDE \(Code written in C\)*

➢ *SocketCAN Linux CANbus Driver Package*

➢ *Python Library – canutils, cantools, PyQt5*

**Accessories:**

*Figure-3: CAN Input/Output Characteristics. *

➢ *Breadboard, Jumper cables, Peripherals*

*Figure-1: Differential voltage between CAN\_H and CAN\_L. *

*Figure-4: Types of CAN protocols in Automotive Industry. *

*Figure-2: The inverted logic of a CAN bus. *

*Figure-5: CAN 2.0 bus length v/s signaling rate. *

**Ref: https://www.ti.com/lit/an/sloa101b/sloa101b.pdf?ts=1670653821828&ref\_url=https%253A%252F%252Fwww.google.com%252F**

**Electrical and Computer Engineering**

29





Project 

Problem 

Project 

***Design ***

Implementation 

Experimental 

Conclusion

Overview

Statement

Resources

***Solution***

Description

Evaluation

***CANbus Bitwise Arbitration Method for Contention Resolution***

❖ *A collision may occur when two or more nodes in the network are attempting to* *access the bus at the same time, which may result in delays or corruption of* *messages. *

❖ *CAN averts message/data collisions by using the message ID of the node, i.e. the* *message with the highest priority \(= lowest message ID\) will gain access to the* *bus, while all other nodes \(with lower priority message IDs\) switch to a listening* *mode. *

***Standard CAN Frame \(11-bit identifier\)***

***Extended CAN Frame \(29-bit identifier\)***

*Figure-6: Illustration of CAN communication with two types of* *message formats. *

*Figure-7: CAN bitwise arbitration flowchart. *

**Ref:**

**\(1\) https://www.ti.com/lit/an/sloa101b/sloa101b.pdf?ts=1670653821828&ref\_url=https%253A%252F%252Fwww.google.com%252F. **

**\(2\) https://copperhilltech.com/blog/controller-area-network-can-bus-bus-arbitration/**

**Electrical and Computer Engineering**

30





Project 

Problem 

Project 

***Design ***

Implementation 

Experimental 

Conclusion

Overview

Statement

Resources

***Solution***

Description

Evaluation

***Conceptual Block Diagram***

***Real-time CAN Communication Design Circuit***

➢ *The bus network is built using a two-wire circuit comprising of* *CAN High and CAN Low. *

➢ *MCP2515 board is used to convert the CAN messages into SPI* *signals, and vice versa. *

➢ *The Arduino UNO and Raspberry Pi \(acting as two nodes in the* *bus\) are connected with the MCP2515 interface board \(SPI-to-CAN\). *

➢ *The Arduino UNO is programmed using C, and Raspberry Pi is* *programmed using Python. *

➢ *The real-time CAN messages are obtained on the Raspberry Pi,* *which acts as the HMI. *

**Electrical and Computer Engineering**

31





Project 

Problem 

Project 

Implementation 

***Experimental ***

Design Solution

Conclusion

Overview

Statement

Resources

Description

***Evaluation***

***Experiment-I: Transmitting and Receiving CAN messages for each node***

➢ *The objective was to ensure that the CAN communication has been configured correctly for each node within the bus. *

➢ *The Arduino UNO acts as Node A and Raspberry Pi acts as Node B. *

➢ *We were able to leverage the mcp2515 and SPI C-programming libraries to develop the code for Arduino UNO to enable transmission and reception* *of CAN messages. *

*Figure-8: Experiment-I: Node B \(TX\) to Node A \(RX\). CAN frames are transmitted with constant data to test the* *Figure-9: Experiment-I: Node A \(TX\) to Node B \(RX\). CAN frames are transmitted with constant data to test the* *connection. *

*connection. *

**Electrical and Computer Engineering**

32





Project 

Problem 

Project 

Implementation 

***Experimental ***

Design Solution

Conclusion

Overview

Statement

Resources

Description

***Evaluation***

***Experiment-II: Replicating ECU transmission and reception over ***

***CANbus***

➢ *For this experiment, we have designed Arduino UNO \(Node A\) to* *replicate an actual ECU of a vehicle. *

➢ *We have updated our initial circuit by adding a Potentiometer sensor. *

➢ *This sensor sends voltage signals to the Arduino which acts as an ECU. *

➢ *The sensor data is then converted into CAN frames and transmitted* *over the bus. *

*Figure-10: Experiment-II: Sensor data being transmitted over CANbus. As the the resistance of the Potentiometer* *changes, the voltage input to the Arduino UNO changes. Depending on the input signal, the CAN frames are created with* *the respective HEX values representing the data. *

**Electrical and Computer Engineering**

33





Project 

Problem 

Project 

Implementation 

***Experimental ***

Design Solution

Conclusion

Overview

Statement

Resources

Description

***Evaluation***

***Experiment-III: Demonstrating the bitwise arbitration method for ***

***contention resolution***

➢ *For this experiment, our objective was to demonstrate how the CAN *

*protocol performs lossless bitwise arbitration method of contention* *resolution. *

➢ *The experimental setup from the earlier experiments have been updated* *to enable multiple nodes to transmit and receive CAN messages at the* *same time. *

➢ *We can observe that as we monitor the CAN traffic, the message with* *the lowest ID gets transmitted first, which is also indicated by the* *timestamp data. Therefore, we can understand that the bitwise* *arbitration method is successful in resolving collision between the* *messages. *

➢ *We had initially aimed to provide deeper insights into the arbitration* *method by visualizing the actual CAN frames and showing the bit-by-bit* *voltage graphs. While working on this project we realized that* *additional equipments, such as a CANlogger and an oscilloscope, are* *required to visualize the signals. The python libraries have limited* *capabilities for plotting CAN data. *

*Figure-10: Experiment-III: CAN bitwise arbitration. Here, we can observe that the messages with the lowest ID gets* *transmitted first, as indicated by timestamp. Messages with ID 0x70, 0x20, and 0x50 are virtual CAN frames with* *constant data transmitted by RPi. Message ID 0x140 is the variable sensor data transmitted by Arduino UNO. Hence, the* *graph for 0x140 varies over time. *

**Electrical and Computer Engineering**

34



CAN Project Ideas

**1\) Two-node CAN \(Arduino \+ MCP2515\) with deadline monitoring**

*Objective – * Measure end-to-end latency, bus utilization vs. deadline misses. 

*Resources – * Arduino, Raspberry Pi, MCP2515, PICAN. 

**2\) SocketCAN logger for jitter analysis**

*Objective – * To time-stamp frames and compute jitter; To study scheduling & interrupt latency. 

*Resources – * SocketCAN, can-utils, Raspberry Pi, MCP2515, PICAN. 

**3\) FreeRTOS \+ CAN on STM32/ESP32**

*Objective – * Implementing a multi-priority CAN node using FreeRTOS to analyze CAN message prioritization and RTOS task scheduling. 

*Resources – * FreeRTOS, STM32/ESP32, SocketCAN, can-utils **Electrical and Computer Engineering**

35





Resources

**Hardware:**

• MCP2551 / MCP2561

• PICAN 2

• SparkFun CAN-BUS Shield

• Adafruit CAN Pal Transceiver

**Software:**

• SocketCAN

• can-utils

• STM32\_CAN \(for Arduino-STM32 core\)

• Arduino CAN library

• Zephyr CAN APIs

https://bambooapps.eu/blog/can-bus-testing-alternative

**Github:**

• https://github.com/iDoka/awesome-canbus

**Electrical and Computer Engineering**

36



References

\[1\] L. b. Othmane, L. Dhulipala, M. Abdelkhalek, N. Multari, and M. Govindarasu, “On the performance of detecting injection of fabricated messages into the can bus,” IEEE Transactions on Dependable and Secure Computing, vol. 19, no. 1, pp. 468–481, 2022. 

\[2\] F. G. Tinetti, F. L. Romero, and A. D. Pérez, “Can bus experiments of real-time communications,” in Computer Science – CACIC 2017 \(A. E.De Giusti, ed.\), \(Cham\), pp. 253–262, Springer International Publishing, 2018. 

\[3\] P. H. Nymann, “Can bus protocol: The ultimate guide \(2022\),” 3 2021. 

\[4\] L. Dhulipala, “Detection of injection attacks on in-vehicle network using data analytics,” Master’s Thesis, Iowa State University, 2018. 

\[5\] Antaira, “The basics of a fi eldbus network,” 4 2021. 

\[6\] N. Velichkov, “How raspberry pi connects to can bus,” Oct 2021. 

\[7\] S. Corrigan, “Introduction to the controller area network \(can\) application report introduction to the controller area network \(can\),” 2002. 

\[8\] M. Falch, “Can bus explained - a simple intro \(2022\),” April 2022. 

\[9\] W. Voss, “Controller area network \(can bus\) - bus arbitration,” November 2018. 

\[10\] “Raspberry Pi 3 Model B\+.” https://www.raspberrypi.com/. 

\[11\] “Arduino UNO Rev3.” https://docs.arduino.cc/resources/. 

**Electrical and Computer Engineering**

37



References

\[12\] “MCP2515, Stand-Alone CAN Controller with SPI Interface.” https://ww1.microchip.com/downloads/en/DeviceDoc/MCP2515. 

\[13\] “SocketCAN.” https://python-can.readthedocs.io/socketcan. 

\[14\] “canutils.” https://github.com/linux-can/can-utils. 

\[15\] “cantools.” https://github.com/cantools/cantools. 

\[16\] “canopy.” https://github.com/Tbruno25/canopy. 

\[17\] “PyQt5.” https://pypi.org/project/PyQt5/. 

\[18\] “DBC Introduction.” https://docs.openvehicles.com/en/latest/. 

**Electrical and Computer Engineering**

38



**Thank you**

**Questions? **

**Electrical and Computer Engineering**

39

**CprE 458/558: Real-Time Systems**

Real-Time Networks – WAN

Packet Scheduling \(Part 1\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**Scheduler**

• Ensuring bandwidth \(and delay\), and buffer 

guarantees to connections

• Determining the service order among packets from 

different connections

• Scheduling algorithm has an associated admission 

control that is used during channel setup

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

**Scheduler requirements**

• Fairness – achieving fairness among competing flows

• Performance bounds for the guaranteed flows

• Efficiency -- schedulability

• Protection – guarantees of well-behaving flows are 

protected from ill-behaving flows

• Flexibility – accommodating a diverse mix of traffic 

class and rates

• Ease of implementation – high speed implementation

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**Fairness and Max-Min Fairness**

• Fairness

– Providing equal share of the resource to all the 

flows

– The notion of fairness is obvious if all the flows 

demand equal share of the resource

– Typically different flows exhibit varying resource 

demands. The notion of Max-min fairness is 

employed in such situations

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

**Max-Min Fairness**

• Basic Idea: A fair share allocates 

– a source with a small demand what it wants, and

evenly distributes unused resources to the big sources

• Formally, max-min fair share allocation is defined as:

– Resources are allocated in order of increasing demands

– No source gets a resource share larger than its demands

– Sources with unsatisfied demands get an equal share of the 

resource

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**Max-Min Fairness: Example**

Four incoming flows with their 

corresponding demands

2

Output Link

2.6

Max-Min

Scheduler

10

4

5

The max-min fairness allocation proceeds in several rounds

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Max-Min Fairness: Example \(1\)**

• Round \#1: Tentatively divide the resource \(output 

bandwidth\) into four equal portions of size 10 / 4 = 2.5

• Allocation = \[2.5, 2.5, 2.5, 2.5\]

• Round \#2: Deduct the excess resource allocation and 

redistribute equally among others

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**Max-Min Fairness: Example \(2\)**

• Source 1’s demand is only 2.0 so deduct \(2.5 - 2.0 = 

0.5\) and distribute the remaining amount of \(0.5 / 3 = 

0.167\) to each of the rest three

• Allocation = \[2.0, 2.67, 2.67, 2.67\] 

• Source 2’s demand is only 2.6 so deduct \(2.67 - 2.6 = 

0.07\) and distribute the remaining amount of \(0.07 / 2\) 

to each of the rest two

• Final Allocation = \[2.0, 2.6, 2.7, 2.7\] 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**Working of the example**

\[2.5, 2.5, 2.5, 2.5\]

Flow 1 has excess = 0.5

add \(0.5 / 3\) to each of 

the rest

\[2.0, 2.67, 2.67, 2.67\]

Flow 2 has excess = 0.07

add \(0.07 / 2\) to each of the 

rest

\[2.0, 2.6, 2.7, 2.7\]

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**Max-Min Fairness: Example**

Four incoming flows with their 

max-min resource \(bandwidth\) 

allocations / demands

2 / 2

Max-Min

Output Link

2.6 / 2.6

Fairness 

10

Resource Allocation

2.7 / 4

2.7 / 5

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Weighted Max-Min Fairness**

• A max-min weighted fairness share is as 

follows

– Resources are allocated in order of increasing 

demand, normalized by the weight

– No source gets a resource share larger than its 

demand

– Sources with unsatisfied demands get resource 

shares in proportion to their weights

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**Weighted Max-Min Fairness: Example**

Four incoming flows with their 

corresponding demands

W1 = 2.5

4

Output Link

W2 = 4

2

Max-Min

Scheduler

16

W3 = 0.5

10

W4 = 1.0

4

The normalized weights are: \[5, 8, 1, 2\]

Now pretend as if the number of flows are \(5 \+ 8 \+ 1 \+ 2\) = 16 instead of just 4

CprE 458/558: Real-Time Systems \(G. Manimaran\)

12

**Working of the example**

• Divide the capacity into 16 equal parts

– Flow 1’s share \(capacity / 16\) \* 5 = \(16 / 16\) \* 5 = 5

• Assign each flow an amount equal to its corresponding 

normalized weight

• If there is excess allocation deduct it and redistribute it 

for the rest in a weighted manner

CprE 458/558: Real-Time Systems \(G. Manimaran\)

13

**Working of the example**

\[5, 8, 1, 2\]

Flow 2 has excess = 6

Flow 1 has excess = 1

\[4, 2, 3.33, 6.66\]

•We have to distribute excess “7” units among flows 3 and 4

•Their weights are 1 and 2 respectively

•Therefore, flow 3 will get an additional share of \(7/3\) \* 1 and flow 4 will get an additional share of \(7/3\) \* 2

CprE 458/558: Real-Time Systems \(G. Manimaran\)

14

**Working of the example**

\[5, 8, 1, 2\]

Flow 2 has excess = 6

Flow 1 has excess = 1

\[4, 2, 3.33, 6.66\]

Flow 4 has excess = 2.66 

allocate it to flow 3

Final Allocation \[4, 2, 6, 4\]

CprE 458/558: Real-Time Systems \(G. Manimaran\)

15

**General Processor Sharing \(GPS\) or Fluid Flow Model** **for achieving Max-min Fairness**

Two incoming flows with their 

resource demands

5

GPS

Output Link

Resource Allocation

10

5

\(Ideal, but Not practical\)

The schedule \(ideal, but not realizable in networks\)

0

5

10

CprE 458/558: Real-Time Systems \(G. Manimaran\)

16

**Max-Min fairness Approximation**

Two incoming flows with their 

resource demands

Packetized GPS

5

Output Link

\(Max-Min

Fairness 

10

5

Approximation\)

The schedule

5 units of time

5 units of time

0

5

10

CprE 458/558: Real-Time Systems \(G. Manimaran\)

17

**A Simple Round Robin Scheduler**

Cannot achieve max-min fairness

Four incoming flows

•Need to handle weighted flows

•Need to handle variable length packets

Output Link

Round Robin

Scheduler

The schedule

0

CprE 458/558: Real-Time Systems \(G. Manimaran\)

18

**Weighted Round Robin Scheduler**

Four incoming flows with their 

Normalized weights are as 

corresponding weights

follows:

\[2, 3, 1, 1\]

10

Output Link

15

Round Robin

Scheduler

5

5

Cannot achieve max-min fairness

•Need to handle variable length packets

0

CprE 458/558: Real-Time Systems \(G. Manimaran\)

19

**CprE 458/558: Real-Time Systems**

Real-Time Networks – WAN

Packet scheduling \(Part 2\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**Work-conserving vs. Non work-conserving**

• Work conserving scheduler

– Never leaves the link idle if there is a packet to be 

transmitted

– Offers better link utilization

– E.g., RR, WRR, WFQ

• Non work-conserving scheduler

– Associate eligibility time with each packet and 

transmits packets only when they are eligible

– Can provide delay-jitter control, easier 

implementation

– E.g., HRR

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

**Fair Queuing \(FQ\) : Byte-by-Byte RR emulation** A

Packet

Finish

1 6 11 15 19 20

Time

B

2 7 12 16

C

8

C

3 8

B

16

D

D

17

4 9 13 17

E

18

E

5 10 14 18

A

20 Problem: 

Gives all 

Earliest Finish Time FQ Schedule

the 

flows 

the same 

priority

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**Weighted Fair Queuing \(WFQ\)**

A \(3\)

Packet

Finish

1 2 3 12 13 14

Time

B \(2\)

4 5 15 16

A

14

C \(1\)

6 17

B

16

D \(2\)

C

17

7 8 18 19

D

19

E \(3\)

9 10 11 20

E

20

Earliest Finish Time WFQ Schedule

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

**Finish time/number expressions \(1\)**

• Round Number \[ R\(t\) \]: number of rounds of service a 

bit-by-bit round-robin scheduler has completed at a 

given time. 

– Eg: round number 3.5 means, three full rounds and 

fourth round is half-way through

• A connection is said to be active if the largest finish 

number of a packet either in its queue or last served 

from its queue is larger than the current round number

• Thus, the length of a round, that is, the time taken to 

serve one bit from each active connection, is 

proportional to the number of active connections

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**Finish time/number expressions \(2\)**

• Finish time for an inactive connection is:

– F\(i, k, t\) = R\(t\) \+ P\(i,k,t\) \* øi

– Where F\(i, k, t\) is the finish number for the kth packet on 

connection “i’

– Where, R\(t\) is the round number

– P\(i,k,t\) is the size of the kth packet that arrives on 

connection “i” at time “t” 

– Where øi is the normalized weight ratio of the connection 

“i”. 

• Finish time for an active connection is:

– F\(i, k, t\) = F\(i, k-1,t\) \+ P\(i,k,t\) \* øi

• The general expression for finish time is:

– F\(i, k, t\) = Max \( F\(i, k-1,t\) , R\(t\) \) \+ P\(i,k,t\) \* øi

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Hierarchical Round Robin \(HRR\)**

• In HRR, there are number of levels, each with a fixed number of slots serviced in a round-robin fashion

• A channel is allocated a given number of service slots at a 

selected level

• The scheduler cycles through the slots at each level

• The time taken to service all the slots at a given level is called the 

“frame time” at that level 

• The total link bandwidth is partitioned in among these levels

• The key to HRR lies in its ability to give each level a constant share of the link’s bandwidth

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**Hierarchical Round Robin – contd. **

• The frame time for level 1, which is the smallest of all 

the levels, is the basic cycle time. 

• If there are n1 slots in a level 1 frame, then b1 slots are 

allocated to higher levels, and the remaining \(n1 – b1\) 

slots are used for the level 1 connections

• The frame time for level-1 = FT1 = n1

• The frame time for level-2 = FT2 = \(n1 / b1\) \* n2

• The frame time for level-I = FTi = 

\(n1 / b1\) \* \(n2 / b2\) \* … \(ni-1 / bi-1\) \* ni 

• Bandwidth allocated to each slot in level i = Link\_BW / FTi



where Link\_BW is the total link bandwidth

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**HRR design for a 4Mbps link**

Level i

n

n1

i

bi

FTi Slot b/w

b1

Level 1

1

4

1

4

1 Mbps

L2 slot

2

4

1

16

250 Kbps

Level 2

b2

3

2

0

32

125 Kbps

L3 slot

Level 3

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**HRR – connection allocation example**

Channel Bandwidth Level 

\# of 

need

Assigned slots

n1

C1

2 Mbps

1

2

b1

Level 1

c1

c1

c2 L2

C2

1 Mbps

1

1

C3

250 Kbps

2

1

Level 2

b2

c3 c4 c4 L3

C4

500 Kbps

2

2

C5

125 Kbps

3

1

Level 3

C6

100 Kbps

3

1

c5 c6

c1

c1

c2 c3 c1 c1 c2 c4 c1 c1 c2 c4 c1 c1 c2 c5

HRR Schedule up to 16 slots

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Real-Time WAN -- Summary**

• QoS parameters – bandwidth, delay, delay 

jitter, packet loss

• Traffic types – CBR and VBR

• Traffic models – Peak rate model, LBAP

• Real-time channel setup

– QoS routing and Resource reservation

• Data transmission phase

– Traffic shaping: Leaky bucket, Token bucket

– Packet scheduling: RR, WRR, WFQ, HRR

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**CprE 458/558: Real-Time Systems**

Real-Time Networks – WAN

Channel establishment

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**QoS metrics: types of constraint**

Metrics and their nature

• End-to-end delay: additive metric, path metric

• Delay jitter: additive metric, path metric

• Bandwidth: convex \(min\), link metric

• Packet loss: multiplicative, path metric

Theorem: A problem with two or more path constraints is 

NP-Complete, assuming the constraints are 

independent and the values are real. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

**QoS routing problem instances**

Given a graph G\(V,E\), with each edge labeled 

with \(cost, delay, available bw\). 

• Bandwidth-constrained least-cost routing

– Polynomial time problem

– Solution: Remove edges that don’t satisfy BW 

constraint and then run shortest path algorithm on 

the reduced graph. 

• Delay-constrained, BW-constrained, least-cost routing

– NP-complete problem

– Heuristics exists

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**Channel establishment – QoS routing**

• Source Routing

– Source computes the routing path

– Obtaining global state is difficult

– Not scalable

• Distributed Routing \(hop-by-hop\)

– Each node decides what is the next hop

– Lack of global knowledge → inferior paths

– Scalable

• Hierarchical Routing

– Based on aggregate state information

– Scalable \(works well for inter-domain routing\)

– Compromise between source and distributed routings

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

**Source Routing**

Choose the 

entire path 

from source to 

destination

Connection 1

1

S

D

•The source has the entire network state information \(cost, 

delay, etc.. of each edge\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**Distributed / Hop-by-hop Routing**

Connection 1

1

S

D

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Hierarchical Routing**

S

D

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**Hierarchical Rou**

Routin **ting**

g

based on 

precise 

1

state

S

Routing 

based on 

aggregate 

state

Routing 

based on 

precise 

state

D

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**QoS Source Routing**

Choose the path from 

source to destination that 

satisfies the QoS 

requirements based on some 

Connection 1

1

heuristic function

With some S

QoS 

requirements

D

•The source has the entire network state information \(cost, 

delay, etc.. of each edge\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**QoS Hop-by-hop Connection setup**

No outgoing edge 

satisfies the required 

Connection 1

QoS

1

With some 

Therefore, back off

S

QoS 

requirements

D

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Channel establishment – Resource reservation**

• Once a feasible path is found, resources such as 

bandwidth, buffers are reserved along the path

• Resource Reservation Protocol \(RSVP\)

– Receiver-driven protocol

– Supports multicast as well as unicast

– Provides different type of reservation styles

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**CprE 458/558: Real-Time Systems**

Real-Time Networks --

Wide-Area Networks \(WAN\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**Real-Time communications: Introduction**

source

destination

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

**Performance metrics**

• Bandwidth of the connection

• End-to-end delay: The total time the packet 

experienced from source to destination

• Delay jitter: It is the maximum variation in 

delay experienced by packets that travel 

across the connection

• Packet Loss: Percentage of packets lost

• The nature of the applications dictate the kind 

of performance requirements required

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**Performance metrics**

• Delay

Delay, D2

Delay, D1

M3

M2

M1

• Delay jitter

D3

D2

M3

M2

D1

M4

M1

• Delay-jitter = Max\_delay – Min\_delay

– In the example, Delay-jitter = \(D1 – D3\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4

**Applications and Guarantee requirements**

• Interactive applications require

– Bound on both delay and delay-jitter

– Can tolerate occasional message loss

– Examples: continuous media traffic \(video 

or audio playback\)

• Discrete applications require

– Error-free service

– Can tolerate both delay and jitter

– Examples: File transfer, Image retrieval

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**Providing performance guarantees: Issues**

• Choice of the packet scheduling 

algorithm at the intermediate node 

\(switch\)

• The message scheduling algorithms at 

the switches determine the order in 

which the packets from different 

connections are serviced

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Approaches to Real-time Communication**

• Pure circuit switching: It reserves the entire 

physical/virtual channel for the connection. E.g., 

telephone networks

• Pure packet switching: It can efficiently utilize network 

bandwidth but cannot provide real-time guarantees. 

E.g., Internet

• Packet-oriented switching: A virtual channel is 

established before transmission begins, employs 

statistical multiplexing to utilize bandwidth efficiently. 

E.g., ATM \(Asynchronous Transfer Mode\) network

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7

**Types of service**

• Guaranteed service: \(Deterministic or hard guaranteed 

service\). This approach is conservative in resource 

reservation \(for peak workload\) and is the simplest 

method for real-time services. 

• Predictive service: This service is meant for adaptive 

applications that can tolerate occasional violation of 

delay bound. Multimedia playback applications 

function well with this category of service. 

• As-soon-as-possible service: This is best-effort service 

with priorities, the highest to be given to interactive 

burst traffic and the lowest to asynchronous bulk 

transfer. This category of service provides no 

guarantees, and no resources are reserved for it. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**Real-Time Channel**

• A virtual circuit that provides the required 

end-to-end QoS guarantees. 

• QoS parameters: bandwidth, delay, 

delay jitter, packet loss, etc. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**Life-cycle of a Real-Time Channel**

• Channel establishment phase

– QoS routing

– Resource reservation

• Data Transmission phase

– Traffic policing/shaping

– Packet scheduling

– Rate adaptation

• Channel tear-down phase

– Releasing session resources

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Chan**

If yes admit 

Request **ne**

for a **l Establishment Phase**

the 

new 

Can the current network 

connection

If NO 

connection: 

condition provide the 

reject the 

I need the so 

required QoS ?? 

connection

and so QoS 

guarantees

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**Run-time scheduling phase**

Which 

Router

flow 

to 

Set of Per-flow 

send 

queues

first? 

? 

1

2

3

4

Output Link

5

Node

CprE 458/558: Real-Time Systems \(G. Manimaran\)

12

**Characterization of Real-Time Traffic**

• The traffic generated by the real-time sources fall in 

one of the two categories:

• Constant bit rate \(CBR\): In CBR, fixed-size packets 

are generated at regular intervals. It is smooth and 

nonbursty. The data generated by sensors \(periodic\). 

• Variable bit rate \(VBR\): \(1\) fixed sized packets arriving 

at irregular intervals or \(2\) variable-sized packets 

arriving at regular intervals

– Voice traffic \(talk spurts alternate with periods of silence\) 

– video source \(different compression ratios result in variable 

size packets generated at regular intervals\)

CprE 458/558: Real-Time Systems \(G. Manimaran\)

13

**CBR and VBR examples**

CBR

1

1

1

1

1

1

0

6

12

18

24

30

Source

VBR

1

1

1

1

1

3

1

1

0

6

12

14 16 18

21 23

30

Source

CprE 458/558: Real-Time Systems \(G. Manimaran\)

14

**Change in Traffic characteristics**

Source

1

1

1 1 1 1 1 1 1

1

1

0

6

Switch

The CBR now becomes bursty 

because of cross traffic

Source

CprE 458/558: Real-Time Systems \(G. Manimaran\)

15

**Traffic Models**

• Peak-Rate Model: Most hard real-time systems use 

the peak-rate model for traffic characterization. The 

parameters of this model, for a connection i, are

– Minimum inter arrival time between messages \(Ti\) 

– Maximum message rate \(1 / Ti\)

– Maximum message length \(μi\)

– End-to-end delay bound \(Di\)

• The peak bandwidth requirement of the connection is 

\(μi / Ti\)

• The peak-rate model is exact only for the CBR traffic 

and overstates the bandwidth requirement for all VBR 

sources

CprE 458/558: Real-Time Systems \(G. Manimaran\)

16

**Peak-rate model: Illustrative example**

CBR

1

1

1

1

1

1

0

6

12

18

24

30

Source

Minimum inter-arrival time \(Ti\) = 6 sec

Maximum message rate \(1 / Ti\) = 1 / 6 = 0.16 message/sec

Maximum message length \(μi\) = 1 kbits Exact B/W 

Bandwidth required = 1 / 6 = 0.16 kbits/secrequirement

CprE 458/558: Real-Time Systems \(G. Manimaran\)

17

**Peak-rate model: Illustrative example**

Burst

VBR

1

1

1

1

1

3

1

1

0

6

12

14 16 18

21 23

30

Source

An 

Minimum inter arrival time \(Ti\) = 2 sec

overstatement 

Maximum message rate \(1 / Ti\) = 0.5 messages/sec

of the B/W 

requirement

Maximum message length \(μi\) = 3 Kbits

Peak bandwidth required = 3/2 = 1.5 Kbits/sec

CprE 458/558: Real-Time Systems \(G. Manimaran\)

18

**Traffic Models \(contd.\)**

• Linear Bounded Arrival Process \(LBAP\) 

Model

– This model uses an additional parameter 

representing the maximum burst size \(Bi\)

– In this model, the number of bits transmitted 

during any interval of length t is bounded by 

Bi \+ \(t / Ti\) μi 

– This model can guarantee deterministic 

delay bounds

CprE 458/558: Real-Time Systems \(G. Manimaran\)

19

**LBAP model: Illustrative example**

Burst

VBR

1

1

1

1

1

3

1

1

0

6

12

14 16 18

21 23

30

Source

An over 

estimate of the 

Average inter-arrival time \(Ti\) = 6 sec

B/W req., but 

Maximum message rate \(1 / Ti\) = 0.16 messages/sec

better than 

peak model

Burst size \(Bi\) = 1 Kbits

Maximum message length \(μi\) = 3 Kbits

Bandwidth required = 3/6 \+ 1 = 1.5 Kbits/sec

CprE 458/558: Real-Time Systems \(G. Manimaran\)

20

**CprE 458/558: Real-Time Systems**

Real-Time Networks – WAN

Traffic Shaping/Policing

CprE 458/558: Real-Time Systems \(G. Manimaran\)

1

**Regulating flow control**

• The bursty traffic in the network results in 

congestion

• Traffic shaping reduces congestion and 

thus helps the carrier live up to its 

guarantees

• Traffic shaping is about regulating the 

average rate \(and burstiness\) of data 

transmission

CprE 458/558: Real-Time Systems \(G. Manimaran\)

2

**Traffic Shaping**

• Traffic shaping controls the *rate * at which 

packets are sent \(not just how many\) 

• At connection set-up time, the sender and 

carrier negotiate a traffic pattern \(shape\)

• Two traffic shaping algorithms are:

– Leaky Bucket

– Token Bucket

CprE 458/558: Real-Time Systems \(G. Manimaran\)

3

**The Leaky Bucket Algorithm**

• The **Leaky Bucket Algorithm** used to 

control rate in a network. It is 

implemented as a single-server queue 

with constant service time. If the bucket 

\(buffer\) overflows then packets are 

discarded. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

4



**The Leaky Bucket Algorithm**

\(a\) A leaky bucket with water. \(b\) a leaky bucket with 

packets. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

5

**Leaky Bucket Algorithm \(contd.\)**

• The leaky bucket enforces a constant output rate 

regardless of the burstiness of the input. Does nothing 

when input is idle. 

• The host injects one packet per clock tick onto the 

network. This results in a uniform flow of packets, 

smoothing out bursts and reducing congestion. 

• When packets are the same size \(as in ATM cells\), the 

one packet per tick is okay. For variable length packets 

though, it is better to allow a fixed number of bytes per 

tick. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

6

**Token Bucket Algorithm**

• In contrast to the LB, the Token Bucket \(TB\) 

algorithm, allows the output rate to vary, depending 

on the size of the burst. 

• In the TB algorithm, the bucket holds tokens. To 

transmit a packet, the host must capture and destroy 

one token. 

• Tokens are generated by a clock at the rate of one 

token every t sec. 

• Idle hosts can capture and save up tokens \(up to the 

max. size of the bucket\) in order to send larger bursts 

later. 

CprE 458/558: Real-Time Systems \(G. Manimaran\)

7



**Token Bucket Algorithm \(contd.\)**

5-34

\(a\) Before \(b\) After

CprE 458/558: Real-Time Systems \(G. Manimaran\)

8

**Token bucket operation**

• TB accumulates fixed size tokens in a token 

bucket

• Transmits a packet \(from data buffer, if any are 

there\) or arriving packet if the sum of the token 

sizes in the bucket add up to packet size

• More tokens are periodically added to the 

bucket \(at rate t\). If tokens are to be added 

when the bucket is full, they are discarded

CprE 458/558: Real-Time Systems \(G. Manimaran\)

9

**Token bucket properties**

• Does not bound the peak rate of small 

bursts, because bucket may contain 

enough token to cover a complete burst 

size

• Performance depends only on the sum 

of the data buffer size and the token 

bucket size

CprE 458/558: Real-Time Systems \(G. Manimaran\)

10

**Token bucket - example**

• 2 tokens of size 100 bytes added each second 

to the token bucket of capacity 500 bytes

– Avg. rate = 200 bytes/sec, burst size = 500 bytes

– Packets bigger than 500 bytes will never be sent

– Peak rate is unbounded – i.e., 500 bytes of burst 

can be transmitted arbitrarily fast

CprE 458/558: Real-Time Systems \(G. Manimaran\)

11

**Leaky Bucket vs Token Bucket**

• LB discards packets; TB does not. TB discards 

tokens. 

• With TB, a packet can only be transmitted if there are 

enough tokens to cover its length in bytes. 

• LB sends packets at an average rate. TB allows for 

large bursts to be sent faster by speeding up the 

output. 

• TB allows saving up tokens \(permissions\) to send 

large bursts. LB does not allow saving. 



CprE 458/558: Real-Time Systems \(G. Manimaran\)

12


# Document Outline

+ Blocking Time Calculation - notes 
+ Concepts of Real-Times Systems, Part 1  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Real-time Systems -- Defined 
	+ Slide 3: Real-time System – Examples 
	+ Slide 4: A typical real-time system 
	+ Slide 5: Sample Applications 
	+ Slide 6: Industrial Internet & Internet of Things 
	+ Slide 7: Real-Time Systems -- Introduction 
	+ Slide 8: Example – Car Driver 
	+ Slide 9: Controller area network \(CAN\) bus in an autonomous vehicle 
	+ Slide 10: Example – Car driver 
	+ Slide 11: Example – Car driver \(contd\) 
	+ Slide 12: Real-Time Tasks \(Workload\) 
	+ Slide 13: Task constraints 
	+ Slide 14: Notion of Predictability 
	+ Slide 15: Computing systems 
	+ Slide 16: Common Misconceptions 

+ CPRE4580-5580 FreeRTOS Tutorial – A Beginner’s Guide 
+ Dependability Concepts - Overview 
+ Failures-CaseStudy 
+ Fault-Tolerant Design Techniques 
+ Introoduction to CAN BUS\_\(TI \)  
	+ Introduction to the Controller Area Network \(CAN\)  
		+ 1 Introduction 
		+ 2 The CAN Standard 
		+ 3 Standard CAN or Extended CAN  
			+ 3.1 The Bit Fields of Standard CAN and Extended CAN  
				+ 3.1.1 Standard CAN 
				+ 3.1.2 Extended CAN 


		+ 4 A CAN Message  
			+ 4.1 Arbitration 
			+ 4.2 Message Types  
				+ 4.2.1 The Data Frame 
				+ 4.2.2 The Remote Frame 
				+ 4.2.3 The Error Frame 
				+ 4.2.4 The Overload Frame 

			+ 4.3 A Valid Frame 
			+ 4.4 Error Checking and Fault Confinement 

		+ 5 The CAN Bus  
			+ 5.1 CAN Transceiver Features  
				+ 5.1.1 3.3-V Supply Voltage 
				+ 5.1.2 ESD Protection 
				+ 5.1.3 Common-Mode Voltage Operating Range 
				+ 5.1.4 Common-Mode Noise Rejection 
				+ 5.1.5 Controlled Driver Output Transition Times 
				+ 5.1.6 Low-Current Bus Monitor, Standby and Sleep Modes 
				+ 5.1.7 Bus Pin Short-Circuit Protection 
				+ 5.1.8 Thermal Shutdown Protection 
				+ 5.1.9 Bus Input Impedance 
				+ 5.1.10 Glitch-Free Power Up and Power Down 
				+ 5.1.11 Unpowered Node Protection 
				+ 5.1.12 Reference Voltage 
				+ 5.1.13 V-Split 
				+ 5.1.14 Loopback 
				+ 5.1.15 Autobaud Loopback 

			+ 5.2 CAN Transceiver Selection Guide 

		+ 6 Conclusion 
		+ 7 Additional Reading 

	+ Revision History 

+ Lectrue 10 - Overload handling -- Feedback-control based scheduling-1  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Feedback scheduling – motivation 
	+ Slide 3: Feedback control technique 
	+ Slide 4: Feedback System Operation 
	+ Slide 5: Feedback system operation \(contd.\) 
	+ Slide 6: FC-EDF 
	+ Slide 7: FC-EDF -- Variables 
	+ Slide 8: FC-EDF Schematic 
	+ Slide 9: FC-EDF 
	+ Slide 10 
	+ Slide 11: Task model and performance index 
	+ Slide 12: Feedback-based Adaptive Scheduler Architecture 
	+ Slide 13: Scheduling Example 
	+ Slide 14: Example \(Cont.\) 
	+ Slide 15: Feedback-based Adaptive scheduling \(Cont.\) 
	+ Slide 16: Feedback control algorithm 
	+ Slide 17: Online controller design 
	+ Slide 18: Simulation studies 
	+ Slide 19: Simulation studies \(Cont.\) 
	+ Slide 20: Overload handling in RT Systems -- Summary 
	+ Slide 21: References 

+ Lecture 2 - Basics of Real-Time Systems, Part 1-2  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Real-Time Systems - Issues 
	+ Slide 3: Real-time Scheduling Paradigms – RM Issue 
	+ Slide 4: Preemptive vs Non-preemptive scheduling 
	+ Slide 5: Optimal scheduling -- definition 
	+ Slide 6: Architectural Issues 
	+ Slide 7: Architectural Issues \(contd..\) 
	+ Slide 8: Requirement, Specification, Verification  
	+ Slide 9: Requirement, Specification, Verification \(contd..\) 
	+ Slide 10: Real-time Languages 
	+ Slide 11: Real-time Databases 
	+ Slide 12: Introduction: Summary 

+ Lecture 3 - Real-time Task Scheduling, Part 1  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Priority-driven Preemptive Scheduling 
	+ Slide 3: Rate Monotonic Scheduling \(RMS\) 
	+ Slide 4: RMS \(cont.\) 
	+ Slide 5: RMS Scheduler -- Example 1 
	+ Slide 6: RMS scheduler -- Example-2 
	+ Slide 7: Earliest Deadline First \(EDF\) 
	+ Slide 8: EDF/LLF \(cont.\) 
	+ Slide 9: EDF scheduler -- Example 
	+ Slide 10: RMS vs. EDF/LLF 

+ Lecture 4 - Real-Time Task Scheduling, Part 2  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Exact Analysis \(necessary & sufficient\) 
	+ Slide 3: Completion Time Test 
	+ Slide 4: Completion Time Test \(Contd.\) 
	+ Slide 5: Completion Time Test \(Contd.\) 
	+ Slide 6: Completion Time Test — Example 
	+ Slide 7: Deadline monotonic scheduling \(DMS\) 
	+ Slide 8: RMS/DMS Schedulability test 
	+ Slide 9: EDF Revisited: Schedulability test 
	+ Slide 10: Periodic task scheduling - summary 

+ Lecture 5 - Resource Access Control Protocols  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Assumptions 
	+ Slide 3: Background – Task State diagram 
	+ Slide 4: Task State Diagram 
	+ Slide 5: Priority Inversion Problem 
	+ Slide 6: Priority Inversion -- Example 
	+ Slide 7: Priority Inversion example 
	+ Slide 8: Priority Inheritance Protocol 
	+ Slide 9: Priority Inheritance Protocol – Deadlock Assume T2 > T1 \(i.e., T2 has high priority\) 
	+ Slide 10: Priority Ceiling Protocol 
	+ Slide 11: Priority Ceiling Protocol \(Contd.\) 
	+ Slide 12: Priority Ceiling Protocol -- properties 
	+ Slide 13: Priority Celiling Protocol - Example 
	+ Slide 14: Resource access control -- example 
	+ Slide 15: Schedules 
	+ Slide 16: Priority Inversion - Real-world Example 
	+ Slide 17: Priority Ceiling Emulation 
	+ Slide 18: Modeling Blocking Time and Earlier Deadline 
	+ Slide 19: Modeling Blocking and Earlier Deadline \(Cont.\)  

+ Lecture 7 - Combined Scheduling  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Assumptions & Issues 
	+ Slide 3: Background Scheduling Algorithm 
	+ Slide 4: Normal RMS schedule: Notice the holes 
	+ Slide 5: Background Scheduling: Example 
	+ Slide 6: Combined Scheduling  
	+ Slide 7: Polling Server 
	+ Slide 8: Polling server: Example 
	+ Slide 9: Polling server: Example \(no animations\) 
	+ Slide 10: Polling server: Schedulability Analysis 
	+ Slide 11: Polling server: Schedulability Analysis 
	+ Slide 12: Polling server: Schedulability Analysis 
	+ Slide 13: Deferrable Server 
	+ Slide 14: Deferrable Server \(Contd.\) 
	+ Slide 15: Deferrable Server: Example 
	+ Slide 16: Priority Exchange Server 
	+ Slide 17: Priority Exchange Server \(Contd.\) 
	+ Slide 18: Priority Exchange server: example 
	+ Slide 19: Sporadic Server 
	+ Slide 20: Sporadic server: example 
	+ Slide 21: Priority-driven preemptive scheduling- summary  

+ Lecture 8 - Scheduling\_Precedence\_Tasks  
	+ Slide 1: Scheduling tasks with precedence relations 
	+ Slide 2: Modifying the task parameters for RMS 
	+ Slide 3: Modifying ready times for RMS: example 
	+ Slide 4: Modifying the Ready times for RMS 
	+ Slide 5: Modified Ready times for RMS 
	+ Slide 6: Assigning task priorities for RMS 
	+ Slide 7: Modifying task parameters for DMS 
	+ Slide 8: Modifying the Deadlines for DMS 
	+ Slide 9: Modifying task parameters for EDF 
	+ Slide 10: Modifying the Ready times for EDF 
	+ Slide 11: Modifying the Ready times for EDF 
	+ Slide 12: Modifying the Deadlines for EDF 
	+ Slide 13: Modifying the Deadlines for EDF 

+ Lecture 9 - Overload handling -- Imprecise Computation and \(m,k\) firm task model-1  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: How Overloads occur?  
	+ Slide 3: Imprecise Computational Model 
	+ Slide 4: Precise vs Imprecise results 
	+ Slide 5: Monotone vs 0/1 constraint tasks 
	+ Slide 6: Applications of Imprecise Computations 
	+ Slide 7: Applications \(Contd’\) 
	+ Slide 8: Error Function & Objective Functions 
	+ Slide 9: Algo F \(Min Total Error, monotone task, identical weights, optimal, O\(n logn\)\) 
	+ Slide 10: Scheduling to Minimize Total Error \(for IC tasks with 0/1 constraints\) 
	+ Slide 11: Scheduling periodic tasks 
	+ Slide 12: \(m, k\) firm real-time tasks 
	+ Slide 13: \(m,k\)-firm deadline model 
	+ Slide 14: Task model and performance index 
	+ Slide 15: MK-RMS Schedulability Check \[2\] 
	+ Slide 16: References 

+ Lecture 11 - Overload handling -- Best effort scheduling  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Best-Effort Scheduler 
	+ Slide 3: Best-Effort Scheduler \(Contd.\) 
	+ Slide 4: HVDF – Highest Value Density First 
	+ Slide 5: Competitive Analysis of BE scheduler 
	+ Slide 6: Competitive Analysis of BE scheduler \(contd.\) 
	+ Slide 7: Overload handing -- Summary 

+ Real-Time LAN -- CANbus  
	+ Slide 1 
	+ Slide 2 
	+ Slide 3 
	+ Slide 4 
	+ Slide 5 
	+ Slide 6 
	+ Slide 7 
	+ Slide 8 
	+ Slide 9 
	+ Slide 10 
	+ Slide 11 
	+ Slide 12 
	+ Slide 13 
	+ Slide 14 
	+ Slide 15 
	+ Slide 16 
	+ Slide 17 
	+ Slide 18 
	+ Slide 19 
	+ Slide 20 
	+ Slide 21 
	+ Slide 22 
	+ Slide 23 
	+ Slide 24 
	+ Slide 25 
	+ Slide 26 
	+ Slide 27 
	+ Slide 28 
	+ Slide 29 
	+ Slide 30 
	+ Slide 31 
	+ Slide 32 
	+ Slide 33 
	+ Slide 34 
	+ Slide 35 
	+ Slide 36 
	+ Slide 37 
	+ Slide 38 
	+ Slide 39 

+ Real-Time WAN -- Packet Scheduling, Part 1  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Scheduler 
	+ Slide 3: Scheduler requirements 
	+ Slide 4: Fairness and Max-Min Fairness 
	+ Slide 5: Max-Min Fairness 
	+ Slide 6: Max-Min Fairness: Example 
	+ Slide 7: Max-Min Fairness: Example \(1\) 
	+ Slide 8: Max-Min Fairness: Example \(2\) 
	+ Slide 9: Working of the example 
	+ Slide 10: Max-Min Fairness: Example 
	+ Slide 11: Weighted Max-Min Fairness 
	+ Slide 12: Weighted Max-Min Fairness: Example 
	+ Slide 13: Working of the example 
	+ Slide 14: Working of the example 
	+ Slide 15: Working of the example 
	+ Slide 16: General Processor Sharing \(GPS\) or Fluid Flow Model for achieving Max-min Fairness 
	+ Slide 17: Max-Min fairness Approximation 
	+ Slide 18: A Simple Round Robin Scheduler 
	+ Slide 19: Weighted Round Robin Scheduler 

+ Real-Time WAN -- Packet Scheduling, Part 2  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Work-conserving vs. Non work-conserving 
	+ Slide 3: Fair Queuing \(FQ\) : Byte-by-Byte RR emulation 
	+ Slide 4: Weighted Fair Queuing \(WFQ\) 
	+ Slide 5: Finish time/number expressions \(1\) 
	+ Slide 6: Finish time/number expressions \(2\) 
	+ Slide 7: Hierarchical Round Robin \(HRR\) 
	+ Slide 8: Hierarchical Round Robin – contd.  
	+ Slide 9: HRR design for a 4Mbps link 
	+ Slide 10: HRR – connection allocation example 
	+ Slide 11: Real-Time WAN -- Summary 

+ Real-Time WAN -- QoS Routing  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: QoS metrics: types of constraint 
	+ Slide 3: QoS routing problem instances 
	+ Slide 4: Channel establishment – QoS routing 
	+ Slide 5: Source Routing 
	+ Slide 6: Distributed / Hop-by-hop Routing 
	+ Slide 7: Hierarchical Routing 
	+ Slide 8: Hierarchical Routing 
	+ Slide 9: QoS Source Routing 
	+ Slide 10: QoS Hop-by-hop Connection setup 
	+ Slide 11: Channel establishment – Resource reservation 

+ Real-Time WAN -- Traffic Models  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Real-Time communications: Introduction 
	+ Slide 3: Performance metrics 
	+ Slide 4: Performance metrics 
	+ Slide 5: Applications and Guarantee requirements 
	+ Slide 6: Providing performance guarantees: Issues 
	+ Slide 7: Approaches to Real-time Communication 
	+ Slide 8: Types of service 
	+ Slide 9: Real-Time Channel 
	+ Slide 10: Life-cycle of a Real-Time Channel 
	+ Slide 11: Channel Establishment Phase 
	+ Slide 12: Run-time scheduling phase 
	+ Slide 13: Characterization of Real-Time Traffic 
	+ Slide 14: CBR and VBR examples 
	+ Slide 15: Change in Traffic characteristics 
	+ Slide 16: Traffic Models 
	+ Slide 17: Peak-rate model: Illustrative example 
	+ Slide 18: Peak-rate model: Illustrative example 
	+ Slide 19: Traffic Models \(contd.\) 
	+ Slide 20: LBAP model: Illustrative example 

+ Real-Time WAN -- Traffic Shaping\_Policing  
	+ Slide 1: CprE 458/558: Real-Time Systems 
	+ Slide 2: Regulating flow control 
	+ Slide 3 
	+ Slide 4: The Leaky Bucket Algorithm 
	+ Slide 5: The Leaky Bucket Algorithm 
	+ Slide 6 
	+ Slide 7: Token Bucket Algorithm 
	+ Slide 8: Token Bucket Algorithm \(contd.\) 
	+ Slide 9: Token bucket operation 
	+ Slide 10: Token bucket properties 
	+ Slide 11: Token bucket - example 
	+ Slide 12



