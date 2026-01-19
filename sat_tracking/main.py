from datetime import datetime, timezone
from tle_manager import load_selected_tles
from tracker import track_satellite

def main():
    tle_data = load_selected_tles()
    now = datetime.now(timezone.utc)  # timestamp timezone-aware

    for name, tle in tle_data.items():
        try:
            pos = track_satellite(
                tle["line1"],
                tle["line2"],
                now
            )
            print(f"\n🛰 {name}")
            print(f"Latitude:  {pos['latitude']:.2f}°")
            print(f"Longitude: {pos['longitude']:.2f}°")
            print(f"Altitude:  {pos['altitude_km']:.2f} km")
        except RuntimeError as e:
            print(f"Error tracking {name}: {e}")

if __name__ == "__main__":
    main()