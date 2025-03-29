import asyncio
import os
import socket
from pathlib import Path
from typing import Dict, Union

from digital_sensors.app_logger import get_logger
from digital_sensors.utils import write_to_file, get_current_date, create_dir
from data_parsers import merge_nmea_sentences

log = get_logger(__name__)


async def read_gnss_data(
        usv: str,
        outgoing_dir: Path,
        gnss_config: Dict[str, Union[str, int]],
        buffer_size: int,
        reconnect_delay: int = 10
):
    sensor_name = "gnss"
    host = gnss_config["ip_address"]
    port = gnss_config["port"]

    while True:
        try:
            log.info(f"Connecting to sensor {host}:{port}")
            reader, _ = await asyncio.open_connection(host, port)
            log.info(f"Connected to {host}:{port}")
            while True:
                try:
                    gpzda_frame = (await reader.read(buffer_size)).decode('utf-8', errors='ignore')
                    log.debug(repr(gpzda_frame))
                    gpgga_frame = (await reader.read(buffer_size)).decode('utf-8', errors='ignore')
                    log.debug(repr(gpgga_frame))
                    merged = gpgga_frame + gpzda_frame
                    if merged:
                        sensor_data, frame_date = merge_nmea_sentences(merged)
                        await write_to_file(sensor_data, outgoing_dir, usv, sensor_name, frame_date)
                    await asyncio.sleep(1)
                except TypeError:
                    log.exception("Invalid data received.. skipping write")
        except (socket.error, ConnectionResetError) as e:
            log.exception(f"Connection error on {host}:{port}: {e}. Reconnecting in {reconnect_delay} seconds...")
            await asyncio.sleep(reconnect_delay)


async def read_sensor_data(
        usv: str,
        outgoing_dir: Path,
        sensor_config: Dict[str, Union[str, int]],
        sensor_name: str,
        buffer_size: int,
        reconnect_delay: int = 10,
):
    host = sensor_config["ip_address"]
    port = sensor_config["port"]
    outgoing_dir = outgoing_dir / sensor_name
    create_dir(outgoing_dir)
    while True:
        try:
            log.info(f"Connecting to sensor {host}:{port}")
            reader, _ = await asyncio.open_connection(host, port)
            log.info(f"Connected to {host}:{port}")
            while True:
                try:
                    sensor_data = (await reader.read(buffer_size)).decode('utf-8', errors='ignore')
                    if sensor_data:
                        await write_to_file(sensor_data, outgoing_dir, usv, sensor_name, get_current_date())
                    await asyncio.sleep(1)
                except Exception as e:
                    log.error(f"Error reading {sensor_name} data: {e}")
        except (socket.error, ConnectionResetError) as e:
            log.exception(f"Connection error on {host}:{port}: {e}. Reconnecting in {reconnect_delay} seconds...")
            await asyncio.sleep(reconnect_delay)
