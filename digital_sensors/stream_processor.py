import asyncio
import socket
from typing import Optional, Tuple

from digital_sensors.app_logger import get_logger
from digital_sensors.utils import write_to_file, get_current_ts, get_current_date
from data_parsers import merge_nmea_sentences

log = get_logger(__name__)


async def read_gnss_data(usv, outgoing_dir, gnss_config, reconnect_delay=10, buffer_size=1024):
    host = gnss_config["ip_address"]
    port = gnss_config["port"]
    sensor_name = "gnss"
    reader = await connect_to_sensor(host, port, reconnect_delay)
    while True:
        try:
            gpzda_frame = (await reader.read(buffer_size)).decode('utf-8', errors='ignore')
            gpgga_frame = (await reader.read(buffer_size)).decode('utf-8', errors='ignore')
            merged = gpgga_frame + gpzda_frame
            sensor_data, frame_date = merge_nmea_sentences(merged)
            await write_to_file(sensor_data, outgoing_dir, usv, sensor_name, frame_date)
            await asyncio.sleep(1)
        except TypeError:
            log.exception("Invalid data received.. skipping write")
        await asyncio.sleep(1)


async def read_sensor_data(usv, outgoing_dir, sensor_config, sensor_name, reconnect_delay=10, buffer_size=1024):
    host = sensor_config["ip_address"]
    port = sensor_config["port"]
    reader = await connect_to_sensor(host, port, reconnect_delay)
    while True:
        try:
            sensor_data = (await reader.read(buffer_size)).decode('utf-8', errors='ignore')
            await write_to_file(sensor_data, outgoing_dir, usv, sensor_name, get_current_date())
            await asyncio.sleep(1)
        except Exception as e:
            log.error(f"Error reading {sensor_name} data: {e}")
            return None


async def connect_to_sensor(host, port, reconnect_delay=10):
    while True:
        try:
            log.info(f"Connecting to sensor {host}:{port}")
            reader, _ = await asyncio.open_connection(host, port)
            log.info(f"Connected to {host}:{port}")
            return reader
        except (socket.error, ConnectionResetError) as e:
            log.exception(f"Connection error on {host}:{port}: {e}. Reconnecting in {reconnect_delay} seconds...")
            await asyncio.sleep(reconnect_delay)
