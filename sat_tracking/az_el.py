import math

def satellite_az_el(sat_lat, sat_lon, sat_alt, gs_lat, gs_lon, gs_alt):
    """
    Calculates azimuth and elevation of a satellite from a ground station.
    lat/lon in degrees, altitudes in km.
    """
    # Convert degrees to radians
    gs_lat_rad = math.radians(gs_lat)
    gs_lon_rad = math.radians(gs_lon)
    sat_lat_rad = math.radians(sat_lat)
    sat_lon_rad = math.radians(sat_lon)

    # Earth radius
    R_E = 6371  # km

    # Ground station vector
    x_gs = (R_E + gs_alt) * math.cos(gs_lat_rad) * math.cos(gs_lon_rad)
    y_gs = (R_E + gs_alt) * math.cos(gs_lat_rad) * math.sin(gs_lon_rad)
    z_gs = (R_E + gs_alt) * math.sin(gs_lat_rad)

    # Satellite vector
    x_sat = (R_E + sat_alt) * math.cos(sat_lat_rad) * math.cos(sat_lon_rad)
    y_sat = (R_E + sat_alt) * math.cos(sat_lat_rad) * math.sin(sat_lon_rad)
    z_sat = (R_E + sat_alt) * math.sin(sat_lat_rad)

    # Relative vector
    dx = x_sat - x_gs
    dy = y_sat - y_gs
    dz = z_sat - z_gs

    # ENU (East, North, Up) vector
    sin_lat = math.sin(gs_lat_rad)
    cos_lat = math.cos(gs_lat_rad)
    sin_lon = math.sin(gs_lon_rad)
    cos_lon = math.cos(gs_lon_rad)

    east = -sin_lon*dx + cos_lon*dy
    north = -cos_lon*sin_lat*dx - sin_lat*sin_lon*dy + cos_lat*dz
    up = cos_lat*cos_lon*dx + cos_lat*sin_lon*dy + sin_lat*dz

    az = math.degrees(math.atan2(east, north)) % 360
    el = math.degrees(math.asin(up / math.sqrt(dx**2 + dy**2 + dz**2)))

    return az, el
