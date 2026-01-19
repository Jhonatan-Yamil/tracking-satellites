from datetime import datetime, timezone
from tle_manager import load_selected_tles
from tracker import track_satellite
from config import GROUND_STATION
from az_el import satellite_az_el  

def main():
    tle_data = load_selected_tles()
    now = datetime.now(timezone.utc)

    for name, tle in tle_data.items():
        try:
            pos = track_satellite(tle["line1"], tle["line2"], now)
            
            # Calculate azimuth and elevation
            az, el = satellite_az_el(
                pos['latitude'], pos['longitude'], pos['altitude_km'],
                GROUND_STATION['lat'], GROUND_STATION['lon'], GROUND_STATION['alt_km']
            )
            
            print(f"\n🛰 {name}")
            print(f"Latitude: {pos['latitude']:.2f}°")
            print(f"Longitude: {pos['longitude']:.2f}°")
            print(f"Altitude: {pos['altitude_km']:.2f} km")
            print(f"Azimuth: {az:.2f}°")
            print(f"Elevation: {el:.2f}°")
            
            if el > 0:
                print("➡ Satellite visible from your ground station ")
            else:
                print("➡ Satellite NOT visible from your ground station ")
                
        except RuntimeError as e:
            print(f"Error tracking {name}:  {e}")

if __name__ == "__main__":
    main()
