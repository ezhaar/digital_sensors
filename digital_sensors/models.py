from dataclasses import dataclass


@dataclass
class GPGGA:
    ggpa_id: str
    ggpa_time_utc: str
    latitude: str
    lat_dir: str
    longitude: str
    lon_dir: str
    fix_quality: str
    num_satellites: str
    hdop: str
    altitude: str
    altitude_units: str
    orthometric_height: str
    orthometric_height_units: str
    age_dgps: str
    ref_and_checksum: str


# @dataclass
# class HDT:
#     id: str
#     heading_degrees: str
#     hdt_checksum: str
#
#
# @dataclass
# class ZDA:
#     id: str
#     zda_utc_timestamp: str
#     zda_day: str
#     zda_month: str
#     zda_year: str
#     zda_hour_offset_from_GMT: str
#     zda_minute_offset_and_checksum: str
#
#
# @dataclass
# class GNSS(GPGGA):
#     HDT_heading_degrees: str


@dataclass
class DigitalSensors:
    sensor_name: str
    ip_address: str
    port: int
    timeout: int
