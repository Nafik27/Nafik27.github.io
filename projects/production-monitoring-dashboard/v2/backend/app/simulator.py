import asyncio
import math
import random
from datetime import datetime, timezone
from .database import insert_alarm, insert_sample

class ProcessSimulator:
    def __init__(self):
        self.tick = 0
        self.output_kg = 0.0
        self.downtime_minutes = 0.0
        self.latest = None
        self.listeners = set()
        self.last_alarm_tick = -999

    def snapshot(self):
        t = self.tick
        temp_a = 89.0 + math.sin(t / 9) * 0.7 + random.uniform(-0.18, 0.18)
        temp_b = 88.7 + math.sin(t / 11 + 0.7) * 0.6 + random.uniform(-0.18, 0.18)
        dirty = 1960 + math.sin(t / 15) * 55 + random.uniform(-10, 10)
        clean = 1810 + math.sin(t / 17 + 0.8) * 48 + random.uniform(-8, 8)
        flow = 122.0 + math.sin(t / 12) * 3.5 + random.uniform(-0.6, 0.6)
        current = 43.8 + math.sin(t / 14) * 1.1 + random.uniform(-0.25, 0.25)

        availability = max(0.94, 0.985 - self.downtime_minutes / 480)
        performance = min(1.0, max(0.86, 0.935 + math.sin(t / 25) * 0.018))
        quality = min(0.999, max(0.965, 0.986 + math.sin(t / 22) * 0.004))
        oee = availability * performance * quality
        self.output_kg += random.uniform(0.35, 0.55)

        sample = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temp_a": round(temp_a, 2),
            "temp_b": round(temp_b, 2),
            "dirty_level": round(dirty, 2),
            "clean_level": round(clean, 2),
            "flow_rate": round(flow, 2),
            "current_density": round(current, 2),
            "output_kg": round(self.output_kg, 2),
            "availability": round(availability * 100, 2),
            "performance": round(performance * 100, 2),
            "quality": round(quality * 100, 2),
            "oee": round(oee * 100, 2),
            "downtime_minutes": round(self.downtime_minutes, 1),
            "line_status": "RUNNING",
        }
        return sample

    def alarm_for(self, sample):
        rules = [
            (sample["temp_b"] > 89.35, "MEDIUM", "Dissolution Tank B", "Temperature approaching upper control band"),
            (sample["flow_rate"] < 119.5, "HIGH", "Circulation Loop", "Flow rate below operating band"),
            (sample["dirty_level"] > 2010, "MEDIUM", "Dirty Solution Tank", "Tank level high"),
        ]
        for hit, severity, source, message in rules:
            if hit and self.tick - self.last_alarm_tick > 12:
                self.last_alarm_tick = self.tick
                return {
                    "timestamp": sample["timestamp"],
                    "severity": severity,
                    "source": source,
                    "message": message,
                    "acknowledged": 0,
                }
        return None

    async def run(self):
        while True:
            self.tick += 1
            sample = self.snapshot()
            self.latest = sample
            insert_sample(sample)
            alarm = self.alarm_for(sample)
            if alarm:
                insert_alarm(alarm)

            dead = []
            for queue in self.listeners:
                try:
                    queue.put_nowait(sample)
                except asyncio.QueueFull:
                    dead.append(queue)
            for queue in dead:
                self.listeners.discard(queue)
            await asyncio.sleep(2)
