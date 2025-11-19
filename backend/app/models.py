from pydantic import BaseModel
from datetime import date
class Hotspot(BaseModel):
    agg_date: date
    district: str
    lat: float
    lon: float
    incident_count: int
    rolling_7d_avg: float
    alert: bool
