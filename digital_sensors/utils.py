import json
from datetime import datetime
from pathlib import Path
from digital_sensors import app_logger


log = app_logger.get_logger(__name__)


def get_current_ts():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%S_%f")[:-3]


def get_current_date():
    return datetime.utcnow().strftime("%Y%m%d")


def create_dir(dir_path: Path):
    path = Path(dir_path)
    path.mkdir(parents=True, exist_ok=True)


def initialize_data_file(file_path: Path, sensor_name: str):
    if not file_path.exists():
        with open("../configs/iotedge_headers.json", "r") as f:
            headers = json.load(f)
        header = headers.get(sensor_name)
        if header:
            with open(file_path, "w") as f:
                f.write(header + "\n")


async def write_to_file(data, outgoing_dir, usv, sensor_name, frame_date):
    output_file = Path(outgoing_dir) / f"{usv}_{sensor_name}_{frame_date}.txt"
    log.debug(f"Writing data to {output_file}")
    create_dir(outgoing_dir)
    initialize_data_file(output_file, sensor_name)
    with open(output_file, 'a', encoding='utf-8') as file:
        log.debug(repr(data))
        file.write(data)
        file.flush()


def get_date_from_frame(gpzda_frame: str) -> str:
    splits = gpzda_frame.split(",")
    return splits[4] + splits[3] + splits[2]
