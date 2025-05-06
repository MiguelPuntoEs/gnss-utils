from dataclasses import dataclass
import numpy as np

@dataclass
class AntennaHeader:
    antenna_type: str
    antenna_sn: str
    dazi: float
    zen1: float
    zen2: float
    dzen: float

@dataclass
class FrequencyInfo:
    frequency: str
    pco_n: float
    pco_e: float
    pco_u: float
    pcv_values: np.ndarray
    pcv_mean: np.ndarray

@dataclass
class AntennaInfo:
    antenna_type: str
    antenna_sn: str
    elevs: np.ndarray
    azs: np.ndarray
    frequency_data: list[FrequencyInfo]