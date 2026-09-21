import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .database import acknowledge_alarm, alarms, history, init_db
from .simulator import ProcessSimulator

simulator = ProcessSimulator()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(simulator.run())
    yield
    task.cancel()

app = FastAPI(
    title="Industrial Production Monitoring API",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "production-monitoring-api", "version": "2.0.0"}

@app.get("/api/current")
def current():
    if simulator.latest is None:
        raise HTTPException(status_code=503, detail="Simulator is warming up")
    return simulator.latest

@app.get("/api/history")
def get_history(limit: int = 120):
    return history(min(max(limit, 10), 1000))

@app.get("/api/alarms")
def get_alarms(limit: int = 30):
    return alarms(min(max(limit, 1), 200))

@app.post("/api/alarms/{alarm_id}/acknowledge")
def ack_alarm(alarm_id: int):
    if not acknowledge_alarm(alarm_id):
        raise HTTPException(status_code=404, detail="Alarm not found")
    return {"ok": True, "alarm_id": alarm_id}

@app.websocket("/ws/live")
async def live(websocket: WebSocket):
    await websocket.accept()
    queue = asyncio.Queue(maxsize=3)
    simulator.listeners.add(queue)
    try:
        while True:
            sample = await queue.get()
            await websocket.send_json(sample)
    except WebSocketDisconnect:
        pass
    finally:
        simulator.listeners.discard(queue)
