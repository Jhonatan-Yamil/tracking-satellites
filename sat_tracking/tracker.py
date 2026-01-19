from sgp4.api import Satrec, jday
import math
from datetime import datetime, timezone

def track_satellite(tle_line1, tle_line2, timestamp=None):
    sat = Satrec.twoline2rv(tle_line1, tle_line2)

    if timestamp is None:
        timestamp = datetime.now(timezone.utc)

    # Conversion to Julian date
    jd, fr = jday(timestamp.year, timestamp.month, timestamp.day,
                  timestamp.hour, timestamp.minute, timestamp.second + timestamp.microsecond*1e-6)

    error_code, position, velocity = sat.sgp4(jd, fr)
    if error_code != 0:
        raise RuntimeError(f"SGP4 error code: {error_code}")

    x, y, z = position  # km

    # Conversion from Cartesian to lat/lon/alt
    r = math.sqrt(x**2 + y**2 + z**2)
    lat = math.degrees(math.asin(z / r))
    lon = math.degrees(math.atan2(y, x))
    if lon > 180:
        lon -= 360
    elif lon < -180:
        lon += 360
    alt = r - 6371  # km above Earth's average radius

    return {
        "latitude": lat,
        "longitude": lon,
        "altitude_km": alt
    }
