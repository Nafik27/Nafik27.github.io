import os
from pathlib import Path
from sqlalchemy import Boolean, Float, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DEFAULT_SQLITE = "sqlite:///" + str(
    (Path(__file__).resolve().parent.parent / "data" / "production.db").as_posix()
)
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)

class Base(DeclarativeBase):
    pass

class Sample(Base):
    __tablename__ = "samples"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[str] = mapped_column(String(64), nullable=False)
    temp_a: Mapped[float] = mapped_column(Float, nullable=False)
    temp_b: Mapped[float] = mapped_column(Float, nullable=False)
    dirty_level: Mapped[float] = mapped_column(Float, nullable=False)
    clean_level: Mapped[float] = mapped_column(Float, nullable=False)
    flow_rate: Mapped[float] = mapped_column(Float, nullable=False)
    current_density: Mapped[float] = mapped_column(Float, nullable=False)
    output_kg: Mapped[float] = mapped_column(Float, nullable=False)
    availability: Mapped[float] = mapped_column(Float, nullable=False)
    performance: Mapped[float] = mapped_column(Float, nullable=False)
    quality: Mapped[float] = mapped_column(Float, nullable=False)
    oee: Mapped[float] = mapped_column(Float, nullable=False)

class Alarm(Base):
    __tablename__ = "alarms"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    source: Mapped[str] = mapped_column(String(128), nullable=False)
    message: Mapped[str] = mapped_column(String(255), nullable=False)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

def init_db():
    if DATABASE_URL.startswith("sqlite"):
        Path(DEFAULT_SQLITE.replace("sqlite:///", "")).parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)

def sample_to_dict(row: Sample):
    return {
        "id": row.id, "timestamp": row.timestamp, "temp_a": row.temp_a,
        "temp_b": row.temp_b, "dirty_level": row.dirty_level,
        "clean_level": row.clean_level, "flow_rate": row.flow_rate,
        "current_density": row.current_density, "output_kg": row.output_kg,
        "availability": row.availability, "performance": row.performance,
        "quality": row.quality, "oee": row.oee,
    }

def alarm_to_dict(row: Alarm):
    return {
        "id": row.id, "timestamp": row.timestamp, "severity": row.severity,
        "source": row.source, "message": row.message,
        "acknowledged": int(row.acknowledged),
    }

def insert_sample(sample: dict):
    with Session(engine) as session:
        session.add(Sample(**{k: sample[k] for k in (
            "timestamp","temp_a","temp_b","dirty_level","clean_level","flow_rate",
            "current_density","output_kg","availability","performance","quality","oee"
        )}))
        session.commit()

def insert_alarm(alarm: dict):
    with Session(engine) as session:
        session.add(Alarm(
            timestamp=alarm["timestamp"], severity=alarm["severity"],
            source=alarm["source"], message=alarm["message"],
            acknowledged=bool(alarm.get("acknowledged", False)),
        ))
        session.commit()

def history(limit=120):
    with Session(engine) as session:
        rows = session.scalars(select(Sample).order_by(Sample.id.desc()).limit(limit)).all()
        return [sample_to_dict(r) for r in reversed(rows)]

def alarms(limit=30):
    with Session(engine) as session:
        rows = session.scalars(select(Alarm).order_by(Alarm.id.desc()).limit(limit)).all()
        return [alarm_to_dict(r) for r in rows]

def acknowledge_alarm(alarm_id: int):
    with Session(engine) as session:
        alarm = session.get(Alarm, alarm_id)
        if not alarm:
            return False
        alarm.acknowledged = True
        session.commit()
        return True
