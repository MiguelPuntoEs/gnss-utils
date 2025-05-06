import numpy as np

from utils.coordinates.constants import WGS84_ECCENTRICITY_SQUARED, WGS84_SEMI_MAJOR_AXIS

def car2geo(x: float, y: float, z: float) -> tuple[float, float, float]:
    MAX_ITER = 30
    MAX_DELTA_ITER = 1e-15

    lon = np.arctan2(y, x)

    p = np.sqrt(x ** 2 + y ** 2)
    lati = np.arctan(z / p / (1 - WGS84_ECCENTRICITY_SQUARED))

    iter = 0
    while True:
        lati_ = lati
        Ni = WGS84_SEMI_MAJOR_AXIS / np.sqrt(1 - WGS84_ECCENTRICITY_SQUARED * np.sin(lati_) ** 2)
        hi = p / np.cos(lati_) - Ni
        lati = np.arctan(z / p / (1 - Ni / (Ni + hi) * WGS84_ECCENTRICITY_SQUARED))

        if np.fabs(lati - lati_) < MAX_DELTA_ITER:
            break
        iter += 1
        if iter > MAX_ITER:
            break
    return lati, lon, hi


def geo2car(lat: float, lon: float, h: float) -> tuple[float, float, float]:
    N = WGS84_SEMI_MAJOR_AXIS / np.sqrt(1 - WGS84_ECCENTRICITY_SQUARED * np.sin(lat) ** 2)
    x = (N + h) * np.cos(lat) * np.cos(lon)
    y = (N + h) * np.cos(lat) * np.sin(lon)
    z = ((1 - WGS84_ECCENTRICITY_SQUARED) * N + h) * np.sin(lat)
    return x, y, z


def get_enu_difference(x: float, y: float, z: float, x_ref: float, y_ref: float, z_ref:float) -> tuple[float, float, float]:
    lat_ref, lon_ref, h_ref = car2geo(x_ref, y_ref, z_ref)

    delta_x = x - x_ref
    delta_y = y - y_ref
    delta_z = z - z_ref

    delta_E = -np.sin(lon_ref) * delta_x \
              + np.cos(lon_ref) * delta_y
    delta_N = -np.cos(lon_ref) * np.sin(lat_ref) * delta_x \
              - np.sin(lon_ref) * np.sin(lat_ref) * delta_y \
              + np.cos(lat_ref) * delta_z
    delta_U = np.cos(lon_ref) * np.cos(lat_ref) * delta_x \
              + np.sin(lon_ref) * np.cos(lat_ref) * delta_y \
              + np.sin(lat_ref) * delta_z

    return delta_E, delta_N, delta_U


def get_aer(x: float, y: float, z: float, x_ref: float, y_ref: float, z_ref:float) -> tuple[float, float, float]:
    slant = np.sqrt((x - x_ref) ** 2 + (y - y_ref) ** 2 + (z - z_ref) ** 2)

    delta_E, delta_N, delta_U = get_enu_difference(x, y, z, x_ref, y_ref, z_ref)

    elevation = np.arcsin(delta_U / slant)
    azimuth = np.arctan2(delta_E, delta_N)

    return elevation, azimuth, slant
