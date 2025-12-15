# FreeRTOS Tutorial – A Beginner's Guide

## Introduction to FreeRTOS

### What is FreeRTOS?

**FreeRTOS** (Free Real-Time Operating System) is a popular, **open-source real-time operating system kernel** for embedded systems. It is designed to be **small, simple, and easy to use** while providing powerful features for real-time applications.

### Official Resources

- **Official Documentation**: https://www.freertos.org/Documentation/00-Overview
- **FreeRTOS Kernel**: https://github.com/FreeRTOS/FreeRTOS-Kernel

---

## Key Features

### Core Features
- **Preemptive multitasking**: Tasks can be interrupted and resumed
- **Cooperative multitasking**: Tasks voluntarily yield control
- **Multiple scheduling algorithms**: Including priority-based
- **Inter-task communication**: Queues, semaphores, mutexes
- **Memory management**: Multiple heap allocation schemes
- **Portable**: Runs on many different microcontrollers

---

## Basic Concepts

### Tasks vs. Co-routines

**Tasks:**
- Each runs independently and has its own **stack**
- Full API access
- Preemptive/cooperative scheduling
- Suitable for most applications

**Co-routines:**
- All share **one stack** (saves RAM)
- Cooperative scheduling only
- Macro-based implementation
- Many usage restrictions
- **Rarely used today**

---

## Task States

### State Diagram

**Task States:**
1. **Running**: Currently executing on the CPU
2. **Ready**: Ready to run but waiting for CPU time
3. **Blocked**: Waiting for an event (delay, semaphore, etc.)
4. **Suspended**: Explicitly suspended and won't run until resumed

### State Transitions
```
Ready → (scheduled) → Running
Running → (preemption) → Ready
Running → (event wait) → Blocked
Blocked → (event occurs) → Ready
Running → (suspend) → Suspended
Suspended → (resume) → Ready
```

---

## Configuration

### FreeRTOSConfig.h

FreeRTOSConfig.h contains **all configuration options** for FreeRTOS:

```c
// Enable preemptive scheduling
#define configUSE_PREEMPTION 1

// Tick rate (Hz)
#define configTICK_RATE_HZ ﺍ
```

```c
// Stack size for idle task
#define configMINIMAL_STACK_SIZE (64)

// Total heap size
#define configTOTAL_HEAP_SIZE (64 * 1024)

// Maximum number of priorities
#define configMAX_PRIORITIES (10)

// Enable mutexes
#define configUSE_MUTEXES 1
```

---

## Scheduling Algorithms

### Fixed Priority Preemptive Scheduling

**Configuration:** `configUSE_PREEMPTION = 1`

**Behavior:**
- Higher priority tasks **preempt** lower priority tasks
- Same priority tasks **share CPU time** (Round Robin with time slice)

### Fixed Priority Cooperative Scheduling

**Configuration:** `configUSE_PREEMPTION = 0`

**Behavior:**
- Tasks voluntarily yield control using `taskYIELD()`
- **No preemption**: Tasks run until they explicitly give up CPU

### Time Slicing Scheduling

**Behavior:**
- Tasks with the same priority **share CPU time equally**
- Tasks switch between these tasks at each tick interrupt

---

## Task Management

### Priorities

- `configMAX_PRIORITIES` defines the maximum priority level in FreeRTOSConfig.h
- **Higher numbers = higher priority**

### Task Function

```c
void ATaskFunction( void *pvParameters );
```

### Task Creation

```c
void vTaskFunction(void* pvParameters);

TaskHandle_t xTaskHandle;

int main(void) {
    // Create a task
    xTaskCreate(
        vTaskFunction,              // Task function
        "TaskName",                 // Task name
        configMINIMAL_STACK_SIZE,   // Stack size
        NULL,                       // Parameters passed to task
        1,                          // Priority (0 = lowest)
        &xTaskHandle                // Task handle
    );
    
    vTaskStartScheduler();  // Start the scheduler
    ...
}
```

### Task Handling

**Task Deletion:**
```c
void vTaskDelete(TaskHandle_t pxTaskToDelete);
vTaskDelete(xTaskHandle);  // Delete the task
```

**Task Suspension/Resumption:**
```c
vTaskSuspend(xTaskHandle);  // Suspend the task
vTaskResume(xTaskHandle);   // Resume the task
```

**Priority Management:**
```c
vTaskPrioritySet(xTaskHandle, 2);  // Change priority
```

### Task Delays

```c
// Delay for a specific number of ticks
vTaskDelay(pdMS_TO_TICKS(1000));  // Delay for 1000ms

// Delay until a specific time
TickType_t xLastWakeTime = xTaskGetTickCount();
vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(100));
```

---

## Interrupt Management

### Interrupt Safe API

FreeRTOS provides a set of **"Interrupt Safe" API functions** that can be safely called from within an Interrupt Service Routine (ISR).

**Interrupt Safe API Implementation Files:**
- `queue.c` - Core interrupt-safe queue and semaphore functions
- `tasks.c` - Interrupt-safe task notification functions
- `timers.c` - Interrupt-safe timer functions
- `stream_buffer.c` - Interrupt-safe stream buffer functions

### Key Points

- **Only use FreeRTOS API functions ending with FromISR in ISRs**
  - Examples: `xQueueSendFromISR`, `xSemaphoreGiveFromISR`
- These are safe and fast for ISRs
- Often needing an extra parameter for context switching

---

## FreeRTOS Kernel Installation

### Kernel Repository
- https://github.com/FreeRTOS/FreeRTOS-Kernel

### Platform-Specific Files
Each real-time kernel port contains three common files and **platform-specific files**. Find the associated architecture in portable folder of chip you use.

### Platform Resources

**Arduino:**
- https://docs.arduino.cc/libraries/freertos/

**ESP32:**
- https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/freertos.html
- https://github.com/espressif/esp-idf/tree/v5.5.1/components/freertos

---

## FreeRTOS EDF Scheduling Implementation

### Overview

FreeRTOS uses **fixed-priority scheduling** but lacks EDF support. EDF ensures better deadline adherence and resource utilization for real-time applications.

### Task Structure for EDF

```c
typedef struct task {
    int id;  // Task ID
    int at;  // Arrival time
    int et;  // Execution time
    int pd;  // Period
    int dd;  // Deadline
} task;

// Example task set
task taskSet[] = {
    {1, 0, 4, 12, 12},  // Task 1: 4 exec, 12 period, 12 ddl
    {2, 0, 3, 9, 9},    // Task 2: 3 exec, 9 period, 9 ddl
    {3, 0, 3, 6, 6}     // Task 3: 3 exec, 6 period, 6 ddl
};
```

### Configuration

```c
// Enable EDF scheduler in FreeRTOSConfig.h
#define configUSE_EDF_SCHEDULER 1

// Create EDF task
xTaskCreate_EDF(
    vTaskFunction,              // Task function
    "EDFTask",                  // Task name
    configMINIMAL_STACK_SIZE,   // Stack size
    NULL,                       // Parameters
    1,                          // Default priority
    &xEDFTaskHandle             // Task handle
);
```

---

## Summary

### FreeRTOS Capabilities
- ✅ Multiple scheduling algorithms (fixed priority, cooperative, time-slicing)
- ✅ Task management (create, delete, suspend, resume)
- ✅ Inter-task communication (queues, semaphores, mutexes)
- ✅ Interrupt-safe APIs
- ✅ Portable across many platforms

### Use Cases
- IoT systems where task timing is critical
- Embedded systems requiring real-time guarantees
- Systems where delays can cause failures or poor performance

**Source:** CprE 4580/5580: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

