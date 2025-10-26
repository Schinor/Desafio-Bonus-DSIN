from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class DroneInfo:
    serial: str
    brand: str
    manufacturer: str
    country: str


@dataclass
class Location:
    city: str
    country: str
    latitude: float
    longitude: float
    reference_point: Optional[str] = None


@dataclass
class SuperPower:
    name: str
    description: str
    classification: str  # e.g., bélico, raro, alto risco


@dataclass
class PrimordialDuck:
    id: str
    drone: DroneInfo
    height_cm: float
    weight_g: float
    location: Location
    gps_precision_m: float
    status: str  # 'desperto', 'transe', 'hibernacao profunda'
    heart_bpm: Optional[int] = None
    mutations: int = 0
    superpower: Optional[SuperPower] = None
    notes: Dict = field(default_factory=dict)


@dataclass
class CaptureAssessment:
    id: str
    cost_estimate: float
    military_power: str
    risk_score: float
    scientific_value: float
    recommended_tooling: List[str]
    rationale: str
