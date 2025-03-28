from typing import List, Optional, Tuple

from models import GPGGA
from utils import get_date_from_frame


def merge_nmea_sentences(sentence: str) -> Optional[Tuple[str, str]]:
    nmea_sentences = sentence.strip().split('\r\n')
    gga_sentence = None
    hdt_sentence = None
    zda_sentence = None
    for sentence in nmea_sentences:
        if sentence.startswith('$GPGGA'):
            gga_sentence = sentence.strip("\r\n")
        elif sentence.startswith('$GPHDT'):
            hdt_sentence = sentence.strip("\r\n")
        elif sentence.startswith('$GPZDA'):
            zda_sentence = sentence.strip("\r\n")
    frame_date = get_date_from_frame(zda_sentence)

    nmea_data = gga_sentence + "," + hdt_sentence + "," + zda_sentence + "\n"
    if len(nmea_data.split(",")) != 25:
        return None
    return nmea_data, frame_date


def parse_wave_data(wave_data):
    lines = wave_data.strip().split("\r\n")
