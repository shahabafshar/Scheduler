# Real-Time WAN: QoS Routing

## Overview
QoS routing algorithms find paths in networks that satisfy multiple quality of service constraints, including bandwidth, delay, jitter, and packet loss requirements.

## Routing Problem

### Objective
Find path from source to destination that satisfies:
1. **Bandwidth constraint**: Sufficient link capacity
2. **Delay constraint**: End-to-end delay requirement
3. **Jitter constraint**: Delay variation bounds
4. **Reliability constraint**: Packet loss bounds

### Path Selection
```
Path P: source → node₁ → node₂ → ... → destination

Constraints:
  Σ bandwidth(P) ≥ required_bandwidth
  Σ delay(P) ≤ delay_bound
  Σ jitter(P) ≤ jitter_bound
  Product loss(P) ≤ loss_bound
```

## Constraint-Based Routing

### Multi-Constraint Problem
Optimize path subject to multiple constraints:
```
Minimize: f(cost₁, cost₂, ..., costₙ)
Subject to:
  Σ constraint₁(link) ≤ bound₁
  Σ constraint₂(link) ≤ bound₂
  ...
  Σ constraintₘ(link) ≤ boundₘ
```

### Complexity
- NP-complete for multiple constraints
- Polynomial for single constraint
- Heuristics required

## QoS Routing Algorithms

### 1. Widest Shortest Path (WSP)

#### Strategy
Among shortest paths, select one with maximum bandwidth.

#### Algorithm
```python
def widest_shortest_path(graph, source, dest):
    # Find shortest paths first
    distances = dijkstra(graph, source)
    
    # Filter paths with minimum distance
    shortest_paths = find_paths_with_distance(distances, graph, source, dest)
    
    # Select path with maximum bandwidth
    best_path = max(shortest_paths, 
                   key=lambda p: min_bandwidth(p))
    
    return best_path
```

### 2. Shortest Widest Path (SWP)

#### Strategy
Among paths with maximum bandwidth, select shortest one.

#### Algorithm
```python
def shortest_widest_path(graph, source, dest):
    # Find maximum bandwidth path
    max_bw = find_max_bandwidth(graph, source, dest)
    
    # Filter paths with maximum bandwidth
    widest_paths = find_paths_with_bandwidth(graph, source, dest, max_bw)
    
    # Select shortest path
    best_path = min(widest_paths, 
                   key=lambda p: path_length(p))
    
    return best_path
```

### 3. Constrained Shortest Path (CSP)

#### Objective
Find shortest path satisfying delay constraint.

#### Dijkstra's Extension
```python
def constrained_dijkstra(graph, source, dest, delay_bound):
    distances = {}  # Distance to each node
    delays = {}     # Delay to each node
    
    pq = [(0, 0, source)]  # (distance, delay, node)
    distances[source] = 0
    delays[source] = 0
    
    while pq:
        dist, del, node = heapq.heappop(pq)
        
        if node == dest:
            return reconstruct_path(parents, dest)
        
        for neighbor, link in graph[node]:
            new_dist = dist + link.cost
            new_delay = del + link.delay
            
            # Check constraint
            if new_delay > delay_bound:
                continue
            
            # If better path found
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                delays[neighbor] = new_delay
                heapq.heappush(pq, (new_dist, new_delay, neighbor))
                parents[neighbor] = node
    
    return None  # No feasible path
```

### 4. Multiple Constraint Path (MCP)

#### Bellman-Ford Extension
```python
def mcp_bellman_ford(graph, source, dest, constraints):
    # Initialize
    costs = [infinity for each constraint]
    costs[source] = [0] * len(constraints)
    
    # Relax edges
    for _ in range(len(graph.nodes) - 1):
        for u, v, link in graph.edges:
            new_costs = [costs[u][i] + link[i] 
                        for i in range(len(constraints))]
            
            # Check feasibility
            if all(new_costs[i] <= constraints[i] for i in range(len(constraints))):
                if dominates(new_costs, costs[v]):
                    costs[v] = new_costs
                    parents[v] = u
    
    return reconstruct_path(parents, dest)
```

## Path Selection Heuristics

### 1. Sequential Filtering
Apply constraints one by one.

```python
def sequential_filtering(graph, constraints):
    paths = all_paths(graph)
    
    # Apply each constraint sequentially
    for constraint in constraints:
        paths = [p for p in paths if satisfies(p, constraint)]
    
    if paths:
        return min(paths, key=lambda p: path_cost(p))
    return None
```

### 2. Lagrangian Relaxation
Relax constraints into objective function.

```python
def lagrangian_relaxation(graph, constraints, weights):
    def objective(path):
        # Original cost
        cost = path_cost(path)
        
        # Penalty for constraint violation
        penalty = sum(weight * max(0, c(path) - bound) 
                     for weight, c, bound, weight in zip(weights, constraints))
        
        return cost + penalty
    
    return find_minimum(objective, all_paths)
```

### 3. Genetic Algorithm
Evolutionary approach for path selection.

## QoS-Aware Link States

### Link State Advertisement
Routers advertise:
- Available bandwidth
- Current delay
- Queue occupancy
- Packet loss rate

### Update Triggers
1. Periodic updates
2. Threshold-based updates
3. Event-driven updates

### Scalability
- Filter unimportant information
- Aggregate states
- Limit update frequency

## Source Routing vs. Hop-by-Hop

### Source Routing
- Complete path specified at source
- More control
- Overhead in packet headers

### Hop-by-Hop Routing
- Each router decides next hop
- Distributed decision
- Scalable approach

## Admission Control

### Path Reservation
```python
def reserve_path(path, flow):
    # Check all links on path
    for link in path:
        if link.available_bandwidth < flow.bandwidth:
            return RESERVE_FAILED
        
        # Reserve resources
        link.available_bandwidth -= flow.bandwidth
        link.reserved_flows.append(flow)
    
    return RESERVE_SUCCESS
```

### Release
```python
def release_path(path, flow):
    for link in path:
        link.available_bandwidth += flow.bandwidth
        link.reserved_flows.remove(flow)
```

## Dynamic QoS Routing

### Adaptive Path Selection
- Monitor network conditions
- Update link states
- Re-route when better paths available

### Re-routing Triggers
1. Current path violation
2. Better path discovered
3. Link failure detection
4. Load balancing

## Inter-Domain QoS Routing

### End-to-End Path
- Multiple administrative domains
- Independent policies
- Protocol for inter-domain signaling

### Border Gateway Protocol (BGP)
- Path vector protocol
- QoS extension possible
- Policy-based routing

## Optimization Objectives

### Minimize End-to-End Delay
```
Minimize: Σ delay(link) for links in path
```

### Maximize Available Bandwidth
```
Maximize: min(bandwidth(link)) for links in path
```

### Minimize Hop Count
```
Minimize: number of hops
```

### Balance Multiple Metrics
```
Minimize: weighted_sum(metric₁, metric₂, ..., metricₙ)
```

## Practical Considerations

### Computational Complexity
- Polynomial for single constraint
- Exponential for multiple constraints
- Heuristics for real-time decisions

### Route Stability
- Avoid route flapping
- Use hysteresis
- Prioritize stability over optimality

### Security
- Validate route advertisements
- Prevent route hijacking
- Authentication mechanisms

## Sources
- Real-Time WAN -- QoS Routing.pdf
