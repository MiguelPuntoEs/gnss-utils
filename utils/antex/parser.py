import parse
import numpy as np
from utils.antex.types import AntennaInfo, AntennaHeader, FrequencyInfo


def parse_header(lines: list[str]) -> AntennaHeader:
    dazi_: float = 0.0
    zen1_: float = 0.0
    zen2_: float = 0.0
    dzen_: float = 0.0

    antenna_type: str = ""
    antenna_sn: str = ""

    for line in lines:
        line = line.rstrip() + "\n"

        if line[60:] == "TYPE / SERIAL NO\n":
            try:
                antenna_type, antenna_sn = parse.parse(
                    "{:20}{:20}                    TYPE / SERIAL NO\n", line
                )
                antenna_sn = antenna_sn.strip()
            except:
                antenna_type = ""
                antenna_sn = ""
        if line[60:] == "DAZI\n":
            parsed_ = parse.parse(
                "  {:6.1f}                                                    DAZI\n",
                line,
            )
            dazi_ = parsed_[0]
        elif line[60:] == "ZEN1 / ZEN2 / DZEN\n":
            parsed_ = parse.parse(
                "  {:6.1f}{:6.1f}{:6.1f}                                        ZEN1 / ZEN2 / DZEN\n",
                line,
            )
            zen1_, zen2_, dzen_ = parsed_

    return AntennaHeader(
        antenna_type=antenna_type,
        antenna_sn=antenna_sn,
        dazi=dazi_,
        zen1=zen1_,
        zen2=zen2_,
        dzen=dzen_,
    )


def get_antenna_blocks(lines: list[str]) -> list[list[str]]:
    reading_block: bool = False
    antenna_blocks: list[list[str]] = []

    data_block: list[str] = []
    for line in lines:
        line = line.rstrip() + "\n"

        if line[60:] == "START OF ANTENNA\n":
            data_block = [line]
            reading_block = True
        elif reading_block:
            data_block.append(line)

            if line[60:] == "END OF ANTENNA\n":
                antenna_blocks.append(data_block)
                reading_block = False

    return antenna_blocks


def get_frequency_blocks(lines: list[str]) -> list[list[str]]:
    reading_block: bool = False
    frequency_blocks: list[list[str]] = []

    data_block: list[str] = []
    for line in lines:
        line = line.rstrip() + "\n"

        if line[60:] == "START OF FREQUENCY\n":
            data_block = [line]
            reading_block = True

        elif reading_block:
            data_block.append(line)

            if line[60:] == "END OF FREQUENCY\n":
                frequency_blocks.append(data_block)
                reading_block = False

    return frequency_blocks


def parse_frequency_block(
    frequency_block: list[str], num_elev: int, num_azi: int
) -> FrequencyInfo:
    idx: int = 0
    pcv_values: np.ndarray = np.zeros((num_azi, num_elev))
    pcv_mean: np.ndarray = np.zeros(num_elev)
    frequency: str = ""
    pco_n: float = 0.0
    pco_e: float = 0.0
    pco_u: float = 0.0

    for line in frequency_block:
        line = line.rstrip()

        if line[60:] == "START OF FREQUENCY":
            frequency = line[3:6]
        if line[60:] == "NORTH / EAST / UP":
            str_fmt = "{:10.2f}{:10.2f}{:10.2f}                              NORTH / EAST / UP"
            pco_n, pco_e, pco_u = parse.parse(str_fmt, line)
        if line[0:8] == "   NOAZI":
            fmt_string = "   NOAZI" + "{:8.2f}" * num_elev
            pcv_mean = np.array(parse.parse(fmt_string, line).fixed)
        elif (
            ("START OF FREQUENCY" not in line)
            and ("NORTH / EAST / UP" not in line)
            and ("NOAZI" not in line)
            and ("END OF FREQUENCY" not in line)
        ):
            fmt_string = "{:8.1f}" + "{:8.2f}" * num_elev
            _, *pcv_values[idx] = parse.parse(fmt_string, line)
            idx += 1

    return FrequencyInfo(frequency, pco_n, pco_e, pco_u, -pcv_values, pcv_mean)


def get_data_from_ANTEX_file(file_path: str) -> list[AntennaInfo]:
    with open(file_path, "r") as f:
        lines = f.readlines()

        return get_data_from_ANTEX(lines)


def get_data_from_ANTEX(lines: list[str]) -> list[AntennaInfo]:
    antennas: list[AntennaInfo] = []

    for antenna_block in get_antenna_blocks(lines):
        header: AntennaHeader = parse_header(antenna_block)

        num_elev: int = 0
        num_azi: int = 0

        if header.dzen != 0:
            num_elev = int((header.zen2 - header.zen1) / header.dzen + 1)

        if header.dazi != 0:
            num_azi = int(360 / header.dazi + 1)

        elevs = np.arange(header.zen1, header.zen2 + header.dzen, header.dzen)
        azs = np.arange(0, 360 + header.dazi, header.dazi)

        antennas.append(
            AntennaInfo(
                antenna_type=header.antenna_type,
                antenna_sn=header.antenna_sn,
                elevs=elevs,
                azs=azs,
                frequency_data=[
                    parse_frequency_block(frequency_block, num_elev, num_azi)
                    for frequency_block in get_frequency_blocks(antenna_block)
                ],
            )
        )
    return antennas
