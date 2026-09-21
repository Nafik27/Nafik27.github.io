# Industrial Production Monitoring System — V2

A full-stack manufacturing monitoring project that models a small industrial historian and DCS-style operator dashboard.

> All process values are simulated. This repository does not contain confidential plant data.

## Architecture

```text
Process Simulator (Python)
          |
          v
FastAPI + WebSocket
          |
          +---- SQLite / PostgreSQL Historian
          |
          v
React Operator Dashboard
```

## V2 features

- FastAPI REST API
- WebSocket live process stream
- SQLite development historian\n- PostgreSQL production database support
- React + Recharts dashboard
- Calculated OEE
  - Availability
  - Performance
  - Quality
- Production output
- Temperature, tank level, flow and current-density monitoring
- Rule-based alarm generation
- Alarm history
- Alarm acknowledgement
- Responsive industrial UI
- Dockerized frontend and backend

## Run with Docker

Requirements:

- Docker Desktop
- Docker Compose

From the `v2` directory:

```bash
docker compose up --build
```

Open:

- Dashboard: http://localhost:8080
- API: http://localhost:8000
- Swagger API docs: http://localhost:8000/docs

## Run without Docker

Backend:

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173.

## API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Service health |
| GET | `/api/current` | Latest process snapshot |
| GET | `/api/history` | Historical samples |
| GET | `/api/alarms` | Alarm history |
| POST | `/api/alarms/{id}/acknowledge` | Acknowledge an alarm |
| WS | `/ws/live` | Live 2-second process stream |

## Engineering concepts demonstrated

- Industrial process monitoring
- DCS/HMI interface concepts
- Data historian design
- OEE calculation
- Alarm management
- REST API design
- Real-time WebSocket communication
- SQL persistence
- Containerized application architecture

## Next engineering milestones

- User authentication and operator roles
- Shift model and shift handover report
- CSV/PDF reporting
- Statistical Process Control charts
- Configurable alarm limits
- Equipment downtime reasons
- Multi-line comparison
- PostgreSQL production deployment
- Automated tests and GitHub Actions
- Predictive-maintenance analytics

## Author

**Muhammad Ilman Nafi**  
Electrical Engineering · Production Leadership · Industrial Operations


## Public deployment

The repository now contains production deployment configuration.

### Backend + database — Render

The `render.yaml` Blueprint provisions:

- FastAPI web service
- Managed PostgreSQL database
- Health check at `/api/health`
- `DATABASE_URL` injection

In Render, create a new Blueprint from this GitHub repository and select the repository root. After the backend is created, set:

```text
FRONTEND_ORIGIN=https://YOUR-FRONTEND.vercel.app
```

### Frontend — Vercel

Import the GitHub repository and set the project Root Directory to:

```text
projects/production-monitoring-dashboard/v2/frontend
```

Set the environment variable:

```text
VITE_API_URL=https://YOUR-RENDER-API.onrender.com
```

Then deploy.

### CI

GitHub Actions validates both sides of V2 on relevant pushes and pull requests:

- Python dependency installation + byte-code compilation
- Node dependency installation + Vite production build

Workflow:

```text
.github/workflows/production-monitoring-v2-ci.yml
```
