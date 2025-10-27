# Real-Time WAN: Packet Scheduling

## Overview
Packet scheduling algorithms manage the transmission order of packets in wide area networks to meet real-time constraints and QoS requirements.

## Network Scheduling Challenges

### Characteristics
- **Variable latency**: Network propagation delays
- **Packet loss**: Network congestion and errors
- **Jitter**: Variable end-to-end delay
- **Bandwidth limits**: Link capacity constraints

### Requirements
- Meet packet deadlines
- Manage bandwidth allocation
- Handle packet bursts
- Provide QoS guarantees

## Traffic Models

### Periodic Traffic
- Regular packet arrivals
- Fixed inter-arrival time
- Predictable pattern

### Bursty Traffic
- Variable packet arrivals
- Bursts of packets
- Statistical characteristics

### Leaky Bucket Model
```
Parameters:
- ρ: Average rate
- σ: Burst size
- Maximum rate: ρ + σ/B
```

Where B is time window.

### Token Bucket Model
- Tokens accumulated at rate ρ
- Each token allows one packet transmission
- Maximum burst: σ tokens

## Packet Scheduling Algorithms

### 1. First-Come-First-Served (FCFS)

#### Concept
Packets served in order of arrival.

#### Characteristics
- Simple implementation
- No priority differentiation
- May starve low-rate flows

#### Implementation
```python
class FCFS_Scheduler:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, packet):
        self.queue.append(packet)
    
    def schedule(self):
        if self.queue:
            return self.queue.pop(0)  # FIFO
        return None
```

### 2. Priority Queuing (PQ)

#### Concept
Multiple priority queues, higher priority always served first.

#### Characteristics
- Simple priority enforcement
- May starve lower priority
- Strict priority hierarchy

#### Implementation
```python
class Priority_Queue:
    def __init__(self, num_priorities):
        self.queues = [[] for _ in range(num_priorities)]
    
    def enqueue(self, packet, priority):
        self.queues[priority].append(packet)
    
    def schedule(self):
        # Check highest priority first
        for queue in reversed(self.queues):
            if queue:
                return queue.pop(0)
        return None
```

### 3. Weighted Fair Queuing (WFQ)

#### Concept
Service rate proportional to weights.

#### Bandwidth Allocation
```
Service_rate_i = (w_i / Σw_j) × Total_bandwidth
```

#### Virtual Time
Each flow has virtual time indicating fair service share.

#### Implementation
```python
class WFQ_Scheduler:
    def __init__(self, weights):
        self.weights = weights
        self.virtual_times = [0] * len(weights)
        self.queues = [[] for _ in weights]
    
    def enqueue(self, packet, flow_id):
        self.queues[flow_id].append(packet)
    
    def schedule(self):
        # Find flow with minimum virtual time
        candidate_flows = [i for i, q in enumerate(self.queues) if q]
        if not candidate_flows:
            return None
        
        flow = min(candidate_flows, 
                  key=lambda i: self.virtual_times[i])
        
        packet = self.queues[flow].pop(0)
        
        # Update virtual time
        packet_size = len(packet.data)
        self.virtual_times[flow] += packet_size / self.weights[flow]
        
        return packet
```

### 4. Earliest Deadline First (EDF) for Packets

#### Concept
Packets scheduled by earliest deadline.

#### Deadline Assignment
```
d_k = arrival_time + delay_bound
```

#### Characteristics
- Optimal for meeting deadlines
- May starve non-real-time traffic
- Requires deadline information

#### Implementation
```python
class EDF_Packet_Scheduler:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, packet, deadline):
        packet.deadline = deadline
        heapq.heappush(self.queue, (deadline, packet))
    
    def schedule(self):
        if self.queue:
            _, packet = heapq.heappop(self.queue)
            return packet
        return None
```

## Rate Allocation

### Guaranteed Rate

#### Network Calculus Approach
- Each flow guaranteed minimum rate
- Envelope-based analysis
- Arrival and service curves

### Service Curve
```
S(t) = max(0, σ + ρt)
```

- σ: Burst allowance
- ρ: Guaranteed rate

### Delay Bound
```
Delay ≤ σ / rate
```

## QoS Mechanisms

### DiffServ (Differentiated Services)
- Traffic classification at edge
- Per-hop behaviors (PHB)
- Expedited Forwarding (EF)
- Assured Forwarding (AF)

### IntServ (Integrated Services)
- Per-flow reservation
- RSVP signaling
- Guaranteed Service
- Controlled Load Service

## End-to-End Delay Analysis

### Network Delay Components
1. **Propagation delay**: Physical transmission
2. **Transmission delay**: Packet size / link rate
3. **Queuing delay**: Waiting in queues
4. **Processing delay**: Router processing

### Worst-Case Delay
```
T_total = T_prop + T_trans + T_queue + T_proc
```

### Delay Bound Calculation
Using network calculus:
```
Delay ≤ (burst / rate) + propagation_delay
```

## Admission Control

### Bandwidth Check
```
Σ reserved_rates ≤ link_capacity
```

### Delay Check
```
Total_delay ≤ delay_requirement
```

### Admission Decision
```python
def admit_flow(new_flow, link):
    # Check bandwidth
    if sum(r.rate for r in link.flows) + new_flow.rate > link.capacity:
        return REJECT
    
    # Check delay
    estimated_delay = compute_delay(link.flows + [new_flow])
    if estimated_delay > new_flow.delay_requirement:
        return REJECT
    
    return ADMIT
```

## Traffic Shaping and Policing

### Traffic Shaping
Smooth outgoing traffic to conform to envelope.

#### Leaky Bucket Shaper
```python
class Leaky_Bucket_Shaper:
    def __init__(self, rate, bucket_size):
        self.rate = rate
        self.bucket = bucket_size
        self.last_update = current_time()
    
    def shape(self, packet):
        # Update bucket
        elapsed = current_time() - self.last_update
        self.bucket = min(self.bucket + self.rate * elapsed, 
                         self.bucket_size)
        self.last_update = current_time()
        
        # Check if can transmit
        if len(packet) <= self.bucket:
            self.bucket -= len(packet)
            return TRANSMIT
        else:
            return DELAY
```

### Traffic Policing
Drop or mark non-conforming packets.

### Token Bucket Policer
```python
class Token_Bucket_Policer:
    def __init__(self, rate, burst):
        self.rate = rate
        self.burst = burst
        self.tokens = burst
        self.last_update = current_time()
    
    def police(self, packet):
        # Add tokens
        elapsed = current_time() - self.last_update
        self.tokens = min(self.tokens + self.rate * elapsed, self.burst)
        self.last_update = current_time()
        
        # Check conformance
        if len(packet) <= self.tokens:
            self.tokens -= len(packet)
            return CONFORMING
        else:
            return NON_CONFORMING
```

## Schedulability Analysis

### Utilization Test
```
Σ (packet_size / period) ≤ link_rate
```

### Delay Analysis
Compute worst-case queuing delay using:
- Traffic characteristics
- Service curve
- Link capacity

### Response Time
```
Response_time = queuing_delay + propagation_delay + transmission_delay
```

## Sources
- Real-Time WAN -- Packet Scheduling, Part 1.pdf
- Real-Time WAN -- Packet Scheduling, Part 2.pdf
- Real-Time WAN -- Traffic Models.pdf
- Real-Time WAN -- Traffic Shaping_Policing.pdf
