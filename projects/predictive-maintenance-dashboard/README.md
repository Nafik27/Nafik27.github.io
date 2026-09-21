# Predictive Maintenance & Equipment Health Dashboard

A portfolio project focused on industrial reliability, condition monitoring, and maintenance prioritization.

## What it demonstrates

- Equipment health scoring
- Vibration monitoring
- Bearing-temperature monitoring
- Motor-current monitoring
- Rolling trend visualization
- Rule-based anomaly detection
- Maintenance priority classification
- Recommended maintenance actions
- MTBF-style reliability KPI presentation

## Monitored assets

- Circulation Pump P-101
- Drive Motor M-201
- Filter Unit F-201
- Cooling Pump C-01

## Health-score concept

The MVP intentionally uses an interpretable rule-based approach instead of pretending to use machine learning.

Health score is reduced by abnormal:

- vibration RMS
- bearing temperature
- motor-current deviation
- persistent anomaly conditions

This makes the maintenance logic transparent and suitable for a first engineering prototype.

## Technology

- HTML5
- CSS3
- Vanilla JavaScript
- Canvas API
- GitHub Pages

## Future V2 roadmap

- Python signal simulator
- FastAPI backend
- FFT vibration spectrum
- Bearing-frequency analysis
- Isolation Forest / anomaly detection
- Historical SQLite/PostgreSQL storage
- Remaining Useful Life estimation
- Maintenance work-order history
- CSV/PDF condition report
- React dashboard
- Docker

## Engineering context

All values are simulated. No confidential production or equipment data is used.

## Author

Muhammad Ilman Nafi  
Electrical Engineering · Production Leadership · Industrial Operations
