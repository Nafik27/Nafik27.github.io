# Production Leadership Command Center

A portfolio project designed around the responsibilities of a Production Group Leader in a manufacturing environment.

## What it demonstrates
- Shift management and daily production control
- Manpower allocation and workload visibility
- Production plan vs actual
- OEE / availability / performance / quality
- Safety and quality gates
- Deviation escalation and corrective-action tracking
- PDCA management cycle
- Shift handover and leader activity logging

## Context
The interface is a simulated copper foil manufacturing management system. All production figures are demonstration data.

## Live demo
https://nafik27.github.io/projects/production-leadership-command-center/

## Author
Muhammad Ilman Nafi — Production Group Leader / Electrical Engineer


## Shift Pattern

The simulated operation uses a **12-hour rotating shift cycle**:

| Cycle day | Shift | Time |
|---|---|---|
| Day 1 | Morning | 07:00–19:00 |
| Day 2 | Morning | 07:00–19:00 |
| Day 3 | Night | 19:00–07:00 |
| Day 4 | Night | 19:00–07:00 |
| Day 5 | Off | Rest day |
| Day 6 | Off | Rest day |

The dashboard treats this as a six-day repeating pattern. The current cycle position is not assumed without an operational reference date.


## Manpower Allocation Engine

The dashboard includes an interactive manpower model for the five-person production team. It allows the leader to:

- mark each operator as present or absent;
- configure the three Floor 1 operator task allocations without assuming a fixed individual assignment;
- view DCS, Floor 2, and Floor 1 role coverage;
- monitor average workload and identify the current bottleneck;
- rebalance Floor 1 task allocation during the shift;
- compare manpower coverage with the 12-hour rotating shift pattern.

The model is intentionally based on simulated workload values for portfolio demonstration and does not represent confidential plant data.
