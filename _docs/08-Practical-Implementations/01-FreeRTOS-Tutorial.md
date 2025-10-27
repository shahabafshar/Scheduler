# FreeRTOS Tutorial - A Beginner's Guide

## Overview
FreeRTOS (Free Real-Time Operating System) is a popular open-source real-time kernel for embedded systems. This guide covers fundamental concepts and practical usage.

## FreeRTOS Architecture

### Kernel Components
- Task scheduler
- Task management
- Interrupt management
- Resource management
- Memory management

### Task States
```
Running → Ready → Blocked → Suspended
```
- **Running**: Currently executing on CPU
- **Ready**: Ready to run, waiting for CPU
- **Blocked**: Waiting for event or time
- **Suspended**: Explicitly suspended (not ready)

## Task Creation

### Basic Task Structure
```c
void TaskFunction(void *pvParameters) {
    for(;;) {
        // Task code here
        // Block to allow other tasks
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}
```

### Creating Tasks
```c
xTaskCreate(
    TaskFunction,      // Task function
    "Task Name",       // Task name
    configMINIMAL_STACK_SIZE,  // Stack size
    NULL,              // Parameters
    tskIDLE_PRIORITY + 1,  // Priority
    &taskHandle        // Task handle
);
```

## Task Priorities

### Priority Levels
- Higher priority number = higher priority
- Configurable maximum priority
- Lower priority tasks only run when higher priority tasks blocked

### Priority Assignment
```c
// Low priority
#define LOW_PRIORITY   1

// Medium priority
#define MEDIUM_PRIORITY 2

// High priority
#define HIGH_PRIORITY  3
```

### Priority Inversion
FreeRTOS uses priority inheritance to prevent unbounded priority inversion.

## Interrupt Management

### ISR Restrictions
ISR functions must be very short and use special API functions.

### Standard ISR
```c
void IRQ_Handler(void) {
    // ISR code
    // Use FromISR API versions
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    xSemaphoreGiveFromISR(xSemaphore, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

## Synchronization

### Mutexes
```c
SemaphoreHandle_t xMutex = xSemaphoreCreateMutex();

// Task taking mutex
xSemaphoreTake(xMutex, portMAX_DELAY);
// Critical section
xSemaphoreGive(xMutex);

// Different task
xSemaphoreTake(xMutex, portMAX_DELAY);
// Critical section
xSemaphoreGive(xMutex);
```

### Binary Semaphores
```c
SemaphoreHandle_t xBinarySemaphore = xSemaphoreCreateBinary();

// Task signaling
xSemaphoreGive(xBinarySemaphore);

// Task waiting
xSemaphoreTake(xBinarySemaphore, portMAX_DELAY);
```

### Counting Semaphores
```c
SemaphoreHandle_t xCountingSemaphore = xSemaphoreCreateCounting(10, 0);

// Multiple gives
xSemaphoreGive(xCountingSemaphore);
xSemaphoreGive(xCountingSemaphore);
// Count = 2

// Take twice
xSemaphoreTake(xCountingSemaphore, portMAX_DELAY);
xSemaphoreTake(xCountingSemaphore, portMAX_DELAY);
```

### Queues
```c
QueueHandle_t xQueue = xQueueCreate(10, sizeof(int));

// Sending data
int data = 42;
xQueueSend(xQueue, &data, portMAX_DELAY);

// Receiving data
int receivedData;
xQueueReceive(xQueue, &receivedData, portMAX_DELAY);
```

## Timing

### Delays
```c
// Delay by ticks
vTaskDelay(100);

// Delay by milliseconds
vTaskDelay(pdMS_TO_TICKS(100));

// Delay until absolute time
vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(100));
```

### System Tick
FreeRTOS uses a periodic timer interrupt for scheduling.
- Default tick rate: 1000 Hz (1ms)
- Configurable in FreeRTOSConfig.h

## Scheduling Policies

### Preemptive Scheduling
Default behavior - higher priority tasks preempt lower priority tasks.

### Time Slicing
Equal priority tasks share CPU time in round-robin fashion.

### Co-operative Scheduling
Can be enabled in FreeRTOSConfig.h - tasks must yield explicitly.

## Memory Management

### Heap Management
FreeRTOS provides several heap implementations:
- heap_1.c: Simple, deterministic
- heap_2.c: Fragments but faster
- heap_3.c: Standard malloc/free
- heap_4.c: Minimal fragmentation
- heap_5.c: Multiple memory regions

## Schedulability Considerations

### Priority Assignment
Use rate monotonic or deadline monotonic for periodic tasks.

### Stack Sizing
- Monitor stack usage
- Provide safety margin
- Use FreeRTOS stack overflow detection

### Determinism
- Avoid dynamic memory allocation in real-time tasks
- Use fixed-size buffers
- Minimize ISR processing time

## Best Practices

### Task Design
1. Keep tasks small and focused
2. Block on events or delays
3. Avoid busy-wait loops
4. Use appropriate priorities

### Resource Management
1. Use mutexes for mutual exclusion
2. Minimize critical section duration
3. Use semaphores for signaling
4. Avoid priority inversion

### Debugging
1. Enable stack overflow detection
2. Use trace hooks
3. Monitor CPU usage
4. Check for deadlocks

## Configuration

### FreeRTOSConfig.h
Key configuration parameters:
```c
#define configMAX_PRIORITIES       (5)
#define configUSE_PREEMPTION       1
#define configUSE_TIME_SLICING     1
#define configUSE_IDLE_HOOK        1
#define configUSE_TICK_HOOK        0
#define configCHECK_FOR_STACK_OVERFLOW  2
```

## Example Application

### Multi-Task System
```c
void setup(void) {
    // Create tasks
    xTaskCreate(task1, "Task1", 256, NULL, 1, NULL);
    xTaskCreate(task2, "Task2", 256, NULL, 2, NULL);
    
    // Start scheduler
    vTaskStartScheduler();
}

void task1(void *pvParameters) {
    for(;;) {
        // Task 1 work
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void task2(void *pvParameters) {
    for(;;) {
        // Task 2 work
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}
```

## Sources
- CPRE4580-5580 FreeRTOS Tutorial – A Beginner's Guide.pdf
