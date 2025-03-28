import asyncio
import json
from digital_sensors import app_logger
from stream_processor import read_gnss_data, read_sensor_data
from utils import create_dir

log = app_logger.get_logger(__name__)


async def main():
    try:
        log.info("Starting usv data collection...")
        with open("../configs/sensors_config.json", "r") as conf_file:
            config_data = json.load(conf_file)
        usv = config_data["usv"]
        gnss_config = config_data["sensors"]["gnss"]
        wave_config = config_data["sensors"]["wave"]
        rain_config = config_data["sensors"]["rain"]
        weather_config = config_data["sensors"]["weather"]
        log.info("Setting up data directory...")
        data_dir = f"outgoing/"
        create_dir(data_dir)
        try:
            await asyncio.gather(
                read_gnss_data(usv, data_dir, gnss_config),
                read_sensor_data(usv, data_dir, wave_config, "wave"),
                read_sensor_data(usv, data_dir, weather_config, "weather"),
                read_sensor_data(usv, data_dir, rain_config, "rain"),
            )
        except (asyncio.CancelledError, KeyboardInterrupt):
            log.debug("Cancelling all coroutines")

    except Exception as e:
        log.error(f"Unexpected error occurred: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
