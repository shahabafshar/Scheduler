# Real-Time WAN Packet Scheduling

## Scheduler Overview

### Purpose
- **Ensuring bandwidth** (and delay), and buffer guarantees to connections
- **Determining the service order** among packets from different connections
- **Scheduling algorithm** has an associated admission control that is used during channel setup

---

## Scheduler Requirements

1. **Fairness** – achieving fairness among competing flows
2. **Performance bounds** for the guaranteed flows
3. **Efficiency** – schedulability
4. **Protection** – guarantees of well-behaving flows are protected from ill-behaving flows
5. **Flexibility** – accommodating a diverse mix of traffic class and rates
6. **Ease of implementation** – high speed implementation

---

## Fairness and Max-Min Fairness

### Fairness Definition
- Providing **equal share** of the resource to all the flows
- The notion of fairness is obvious if all the flows demand equal share of the resource
- Typically different flows exhibit **varying resource demands**. The notion of **Max-min fairness** is employed in such situations

### Max-Min Fairness

**Basic Idea:**
- A fair share allocates a source with a **small demand what it wants**, and **evenly distributes unused resources** to the big sources

**Formal Definition:**
- Resources are allocated in order of **increasing demands**
- **No source gets a resource share larger than its demands**
- Sources with unsatisfied demands get an **equal share** of the resource

---

## Max-Min Fairness: Example

### Example Problem
**Four incoming flows** with their corresponding demands:
- Flow 1: 2 units
- Flow 2: 2.6 units
- Flow 3: 4 units
- Flow 4: 5 units

**Output Link:** 10 units total bandwidth

### Step-by-Step Allocation

**Round #1:**
- Tentatively divide the resource (output bandwidth) into four equal portions
- Allocation = **10 / 4 = 2.5** for each
- Result: [2.5, 2.5, 2.5, 2.5]

**Round #2:**
- Source 1's demand is only 2.0, so deduct (2.5 - 2.0 = 0.5)
- Distribute the remaining 0.5 / 3 = 0.167 to each of the rest three
- Result: [2.0, 2.67, 2.67, 2.67]

**Round #3:**
- Source 2's demand is only 2.6, so deduct (2.67 - 2.6 = 0.07)
- Distribute 0.07 / 2 = 0.035 to each of the rest two
- Result: [2.0, 2.6, 2.7, 2.7]

**Final Allocation:** [2.0, 2.6, 2.7, 2.7] (sum = 10.0)

---

## Weighted Max-Min Fairness

### Definition
- Resources are allocated in order of **increasing demand, normalized by the weight**
- No source gets a resource share **larger than its demand**
- Sources with unsatisfied demands get resource shares **in proportion to their weights**

### Example
**Four flows with weights:**
- Flow 1: 4 units (W₁ = 2.5)
- Flow 2: 2 units (W₂ = 4)
- Flow 3: 10 units (W₃ = 0.5)
- Flow 4: 4 units (W₄ = 1.0)

**Normalized weights:** [5, 8, 1, 2] (total = 16)

**Approach:** Treat as if there are 16 flows instead of 4, then allocate proportionally.

---

## General Processor Sharing (GPS) / Fluid Flow Model

### Ideal Model
- Achieves **perfect max-min fairness**
- **Ideal but not practical** (assumes infinitesimally small packets)
- Not realizable in actual networks

### Approximate Implementation
- **Packetized GPS**: Practical approximation
- Serves one complete packet at a time
- Still maintains good fairness properties

---

## Simple Round Robin (RR)

### Characteristics
- **Cannot achieve max-min fairness**
- Treats all flows equally regardless of packet sizes
- Simple implementation but **unfair** for variable length packets

**Limitations:**
- Need to handle weighted flows
- Need to handle variable length packets

---

## Weighted Round Robin (WRR)

### Characteristics
- **Cannot achieve max-min fairness**
- Handles weighted flows
- Still cannot handle variable length packets efficiently

### Example
Flows with weights [2, 3, 1, 1]:
- Serve packets in proportion to weights
- But variable packet sizes cause unfairness

---

## Work-Conserving vs. Non-Work-Conserving

### Work-Conserving Scheduler
- **Never leaves the link idle** if there is a packet to be transmitted
- **Offers better link utilization**
- Examples: RR, WRR, WFQ

### Non-Work-Conserving Scheduler
- **Associate eligibility time** with each packet
- Transmits packets **only when they are eligible**
- Can provide **delay-jitter control**, easier implementation
- Example: HRR (Hierarchical Round Robin)

---

## Fair Queuing (FQ)

### Concept
- **Byte-by-byte Round Robin emulation**
- Assigns finish time to each packet
- Schedules packets with **earliest finish time** first

### Problem
- Gives **all flows the same priority**
- Treats all flows equally regardless of their requirements

---

## Weighted Fair Queuing (WFQ)

### Concept
- Extends FQ with **weights**
- Finish time calculation accounts for flow weight
- Packet with **earliest finish time** is transmitted first

### Finish Time Expression

**General Expression:**
**F(i,k,t) = Max(F(i,k-1,t), R(t)) + P(i,k,t) × φᵢ**

Where:
- **F(i,k,t)**: Finish number for the kth packet on connection "i"
- **R(t)**: Round number (number of rounds of service completed)
- **P(i,k,t)**: Size of the kth packet on connection "i" at time "t"
- **φᵢ**: Normalized weight ratio of connection "i"

### Active vs. Inactive Connection

**Inactive:**
- F(i,k,t) = R(t) + P(i,k,t) × φᵢ

**Active:**
- F(i,k,t) = F(i,k-1,t) + P(i,k,t) × φᵢ

**Round Number R(t):**
- Number of rounds of service a bit-by-bit round-robin scheduler has completed
- Example: R(t) = 3.5 means three full rounds and fourth round is half-way through

**Active Connection:**
- Largest finish number of a packet either in its queue or last served from its queue is **larger than the current round number**

---

## Hierarchical Round Robin (HRR)

### Structure
- **Number of levels**, each with a fixed number of slots serviced in a round-robin fashion
- A channel is allocated a given number of **service slots** at a selected level
- The scheduler **cycles through the slots** at each level

### Frame Time
- The time taken to service all the slots at a given level is called the **"frame time"** at that level
- The total link bandwidth is **partitioned** among these levels
- Each level gets a **constant share** of the link's bandwidth

### Frame Time Calculation

**Level 1:**
- **FT₁ = n₁** (basic cycle time)

**Level 2:**
- **FT₂ = (n₁ / b₁) × n₂**
- Where b₁ is the number of level 1 slots allocated to higher levels

**Level i:**
- **FTᵢ = (n₁ / b₁) × (n₂ / b₂) × … × (nᵢ₋₁ / bᵢ₋₁) × nᵢ**

**Bandwidth per slot at level i:**
- **Link_BW / FTᵢ**

### HRR Design Example (4 Mbps Link)

| Level | nᵢ | bᵢ | FTᵢ | Slot Bandwidth |
|-------|----|----|-----|----------------|
| 1 | 4 | 1 | 4 | 1 Mbps |
| 2 | 4 | 1 | 16 | 250 Kbps |
| 3 | 2 | 0 | 32 | 125 Kbps |

### Connection Allocation Example

| Channel | Bandwidth Need | Level | # of Slots | Allocation |
|---------|---------------|-------|------------|------------|
| C1 | 2 Mbps | 1 | 2 | Direct access |
| C2 | 1 Mbps | 1 | 1 | Direct access |
| C3 | 250 Kbps | 2 | 1 | Level 2 slot |
| C4 | 500 Kbps | 2 | 2 | Two Level 2 slots |
| C5 | 125 Kbps | 3 | 1 | Level 3 slot |
| C6 | 100 Kbps | 3 | 1 | Level 3 slot |

---

## Real-Time WAN Summary

### QoS Parameters
- **Bandwidth**
- **Delay**
- **Delay jitter**
- **Packet loss**

### Traffic Types
- **CBR** (Constant Bit Rate)
- **VBR** (Variable Bit Rate)

### Traffic Models
- **Peak rate model**
- **LBAP** (Linear Bounded Arrival Process)

### Channel Setup
- **QoS routing**
- **Resource reservation**

### Data Transmission
- **Traffic shaping/policing**: Leaky Bucket, Token Bucket
- **Packet scheduling**: RR, WRR, WFQ, HRR

---

## Algorithm Comparison

| Algorithm | Fairness | Bandwidth Control | Delay Bounds | Complexity |
|-----------|----------|------------------|--------------|-----------|
| **RR** | Poor | No | No | Low |
| **WRR** | Fair for fixed packets | Yes | No | Low |
| **FQ** | Good | No | Yes | Medium |
| **WFQ** | Excellent | Yes | Yes | Medium |
| **HRR** | Yes | Yes | Yes | High |

**Source:** CprE 458/558: Real-Time Systems (Prof. G. Manimaran, Iowa State University)

