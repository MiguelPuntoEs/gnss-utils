from dataclasses import dataclass
import numpy as np
from utils.orbit.constants import MU_GPS, OMEGA_EARTH
from utils.orbit.time import compute_tk


@dataclass
class Almanac:
    prn: int
    week: int
    toa: float
    ecc: float
    Omega_dot: float
    Omega_0: float
    omega: float
    M0: float
    af0: float
    af1: float
    N0: float
    a: float
    delta_i: float
    health_prn: int
    health_alm: int
    antispoof: bool


def compute_sat_pos_from_almanac(
    almanac: Almanac, t: float
) -> tuple[float, float, float]:
    tk = compute_tk(t, almanac.toa)

    i0 = 0.3 * np.pi + almanac.delta_i

    M = almanac.M0 + np.sqrt(MU_GPS / (almanac.a**3)) * tk

    E = M
    Ek = 0
    sinE = 0
    while np.abs(E - Ek) > 1e-12:
        Ek = E
        sinE = np.sin(E)
        E = M + almanac.ecc * sinE
    cosE = np.cos(E)

    u = (
        np.arctan2(np.sqrt(1.0 - almanac.ecc**2) * sinE, cosE - almanac.ecc)
        + almanac.omega
    )
    r = almanac.a * (1.0 - almanac.ecc * cosE)

    i = i0
    Omega = (
        almanac.Omega_0
        + (almanac.Omega_dot - OMEGA_EARTH) * tk
        - OMEGA_EARTH * almanac.toa
    )
    xp = r * np.cos(u)
    yp = r * np.sin(u)

    cosO = np.cos(Omega)
    sinO = np.sin(Omega)
    cosi = np.cos(i)

    x = xp * cosO - yp * cosi * sinO
    y = xp * sinO + yp * cosi * cosO
    z = yp * np.sin(i)

    return x, y, z
