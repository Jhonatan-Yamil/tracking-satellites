import os
import time
import requests
from config import CELESTRAK_URL, TLE_FILE, SATELLITES, TLE_MAX_AGE_DAYS

SECONDS_PER_DAY = 86400


def download_tle():
    """Download the TLE file from CelesTrak"""
    response = requests.get(CELESTRAK_URL, timeout=10)
    response.raise_for_status()

    with open(TLE_FILE, "w") as f:
        f.write(response.text)

    print("TLE downloaded successfully.")


def is_tle_outdated():
    """Check if the TLE file is too old or does not exist"""
    if not os.path.exists(TLE_FILE):
        return True
    age = time.time() - os.path.getmtime(TLE_FILE)
    return age > (TLE_MAX_AGE_DAYS * SECONDS_PER_DAY)


def load_selected_tles():
    """Load only the TLEs of the satellites we are interested in"""
    if is_tle_outdated():
        download_tle()

    tle_data = {}
    with open(TLE_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]  # remove empty lines

    i = 0
    while i < len(lines) - 2:
        name = lines[i]
        if name in SATELLITES:
            line1 = lines[i + 1]
            line2 = lines[i + 2]
            tle_data[name] = {"line1": line1, "line2": line2}
            i += 3
        else:
            i += 1

    # # Print for debugging
    # print("=== Loaded TLEs ===")
    # for name, tle in tle_data.items():
    #     print(name)
    #     print(tle["line1"])
    #     print(tle["line2"])
    # print("====================")

    return tle_data