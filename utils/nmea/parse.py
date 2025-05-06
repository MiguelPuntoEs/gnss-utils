import numpy as np
from datetime import datetime

from utils.nmea.checksum import check_NMEA_checksum
from utils.nmea.types import GGAMessage, GNSMessage


def parse_nmea_file(file_path: str):
    with open(file_path, 'r') as f:
        lines: list[str] = f.readlines()

    records: list= []

    for line in lines:

        line: str = line.rstrip()
        
        if not check_NMEA_checksum(line):
            continue

        line: str = line.split('*')[0]

        line_split: list[str] = line.split(",")
        nmea_message: str = line_split[0]

        if nmea_message[3:6] == 'GGA':
            try:
                records.append(parse_gga(line_split))
            except ValueError as _:
                continue

        if nmea_message[3:6] == 'GNS':
            try:
                records.append(parse_gns(line_split))
            except ValueError as _:
                continue

    return records
            
        
def parse_gga(line_split: list[str]) -> GGAMessage:
    now: datetime = datetime.now()

    date: datetime = datetime.strptime(line_split[1], '%H%M%S.%f').replace(year=now.year, month=now.month, day=now.day)
        

    lat_raw: str = line_split[2]
    lon_raw: str = line_split[4]

    lat: float = np.deg2rad(float(lat_raw[0:2]) + float(lat_raw[2:]) / 60.0)
    lon: float = np.deg2rad(float(lon_raw[0:3]) + float(lon_raw[3:]) / 60.0)

    lat = lat if line_split[3] == 'N' else -lat
    lon = lon if line_split[5] == 'E' else -lon
    
    altitude: float = float(line_split[9])
    pos_quality: int = int(line_split[6])

    num_sats: int = int(line_split[7])
    hdop: float = float(line_split[8])
    altitude_unit: str = line_split[10]
    geoidal_separation = float(line_split[11])
    geoidal_separation_unit: str = line_split[12]
    age_of_differential_data: str = line_split[13]
    differential_ref_station_id: str = line_split[14]

    return GGAMessage(
        date=date,
        latitude=lat,
        longitude=lon,
        fix_quality=pos_quality,
        number_of_satellites=num_sats,
        horizontal_dilution=hdop,
        altitude=altitude,
        altitude_units=altitude_unit,
        geoidal_separation=geoidal_separation,
        geoidal_separation_units=geoidal_separation_unit,
        age_of_diff_corr=age_of_differential_data,
        diff_ref_station_id=differential_ref_station_id
    )

def parse_gns(line_split: list[str]):
    date: datetime = datetime.strptime(line_split[1], '%H%M%S.%f')

    lat_raw: str = line_split[2]
    lon_raw: str = line_split[4]

    lat: float = np.deg2rad(float(lat_raw[0:2]) + float(lat_raw[2:]) / 60.0)
    lon: float = np.deg2rad(float(lon_raw[0:3]) + float(lon_raw[3:]) / 60.0)

    lat = lat if line_split[3] == 'N' else -lat
    lon = lon if line_split[5] == 'E' else -lon

    mode: str = line_split[6]
    num_sats: int = int(line_split[7])
    hdop: float = float(line_split[8])
    altitude: float = float(line_split[9])
    geoidal_separation: float = float(line_split[10])
    age_of_data: str = line_split[11]
    ref_station_id: str = line_split[12]

    return GNSMessage(
        date=date,
        latitude=lat,
        longitude=lon,
        mode=mode,
        number_of_satellites=num_sats,
        horizontal_dilution=hdop,
        altitude=altitude,
        geoidal_separation=geoidal_separation,
        age_of_diff_corr=age_of_data,
        diff_ref_station_id=ref_station_id
    )
