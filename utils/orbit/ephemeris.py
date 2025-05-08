from dataclasses import dataclass

import numpy as np

from utils.orbit.constants import MU_GPS, OMEGA_EARTH
from utils.orbit.time import compute_tk


@dataclass
class Ephemeris:
    prn: int
    week: int
    toe: float
    ecc: float
    Omega_dot: float
    Omega_0: float
    omega: float
    M0: float
    toc: float
    af0: float
    af1: float
    af2: float
    N0: float
    a: float
    i0: float
    idot: float
    health_prn: int
    antispoof: bool
    cuc: float
    cus: float
    crc: float
    crs: float
    cic: float
    cis: float


def compuse_sat_pos_from_ephemeris(
    ephemeris: Ephemeris, t: float
) -> tuple[float, float, float]:
    tk = compute_tk(t, ephemeris.toe)

    M = ephemeris.M0 + np.sqrt(MU_GPS / (ephemeris.a**3)) * tk

    E = M
    Ek = 0
    sinE = 0
    while np.abs(E - Ek) > 1e-12:
        Ek = E
        sinE = np.sin(E)
        E = M + ephemeris.ecc * sinE
    cosE = np.cos(E)

    v = np.arctan2(np.sqrt(1.0 - ephemeris.ecc**2) * sinE, cosE - ephemeris.ecc)

    u = (
        v
        + ephemeris.omega
        + ephemeris.cuc * np.cos(2 * (ephemeris.omega + v))
        + ephemeris.cus * np.sin(2 * (ephemeris.omega + v))
    )

    r = (
        ephemeris.a * (1.0 - ephemeris.ecc * cosE)
        + ephemeris.crc * np.cos(2 * (ephemeris.omega + v))
        + ephemeris.crs * np.sin(2 * (ephemeris.omega + v))
    )

    i = (
        ephemeris.i0
        + ephemeris.idot * tk
        + ephemeris.cic * np.cos(2 * (ephemeris.omega + v))
        + ephemeris.cis * np.sin(2 * (ephemeris.omega + v))
    )

    Omega = (
        ephemeris.Omega_0
        + (ephemeris.Omega_dot - OMEGA_EARTH) * tk
        - OMEGA_EARTH * ephemeris.toe
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
