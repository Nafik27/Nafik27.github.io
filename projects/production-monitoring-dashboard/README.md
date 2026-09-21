# Industrial Production Monitoring Dashboard

A portfolio project that simulates a real-time manufacturing monitoring system inspired by industrial DCS environments.

## Why this project exists

The project demonstrates how production engineering, process control, and software can be combined into a practical manufacturing dashboard. It is designed around process variables commonly monitored in industrial operations rather than generic web-app data.

## Current MVP

- Simulated live DCS/process data
- Production output and shift target
- OEE indicator
- Quality rate
- Downtime tracking
- Active alarm count
- Temperature monitoring
- Tank-level monitoring
- Flow-rate monitoring
- Current-density monitoring
- Equipment status
- Alarm history
- Live process trend chart
- Responsive industrial HMI-style interface

## Process variables

| Variable | Unit |
| --- | --- |
| Dissolution Tank A temperature | °C |
| Dissolution Tank B temperature | °C |
| Dirty solution tank level | mm |
| Clean solution tank level | mm |
| Flow rate | L/min |
| Current density | A/dm² |

## Technology

The MVP is intentionally dependency-free:

- HTML5
- CSS3
- Vanilla JavaScript
- Canvas API
- GitHub Pages

This keeps the first release deployable as a static application. A future version can introduce React, FastAPI, PostgreSQL, WebSockets, and real/simulated OPC-style data ingestion.

## Roadmap

- [ ] Separate frontend and backend
- [ ] FastAPI process-data API
- [ ] SQLite/PostgreSQL historian
- [ ] WebSocket live updates
- [ ] Multi-line / multi-shift view
- [ ] Alarm acknowledgement
- [ ] CSV/PDF shift report
- [ ] OEE breakdown: Availability, Performance, Quality
- [ ] SPC/control-limit charts
- [ ] Predictive-maintenance module
- [ ] Docker deployment

## Engineering context

This is a demonstration project. All displayed production values and alarms are simulated and do not represent confidential plant data.

## Author

Muhammad Ilman Nafi  
Electrical Engineering · Production Leadership · Industrial Operations
