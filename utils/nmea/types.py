from dataclasses import dataclass
from datetime import datetime

@dataclass
class GGAMessage:
    """GGA message dataclass."""
    date: datetime
    latitude: float
    longitude: float
    fix_quality: int
    number_of_satellites: int
    horizontal_dilution: float
    altitude: float
    altitude_units: str
    geoidal_separation: float
    geoidal_separation_units: str
    age_of_diff_corr: str
    diff_ref_station_id: str

@dataclass
class GNSMessage:
    """GNS message dataclass."""
    date: datetime
    latitude: float
    longitude: float
    mode: str
    number_of_satellites: int
    horizontal_dilution: float
    altitude: float
    geoidal_separation: float
    age_of_diff_corr: str
    diff_ref_station_id: str