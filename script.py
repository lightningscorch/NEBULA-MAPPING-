import astropy.units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pytz
from datetime import datetime
import sys

# Dictionary of famous nebulae with their J2000 equatorial coordinates (RA, Dec)
NEBULAE = {
    1: {
        "name": "Orion Nebula (M42)",
        "ra": "05h35m16.8s",
        "dec": "-05d23m15s",
        "constellation": "Orion"
    },
    2: {
        "name": "Ring Nebula (M57)",
        "ra": "18h53m35.097s",
        "dec": "+33d01m44.88s",
        "constellation": "Lyra"
    },
    3: {
        "name": "Dumbbell Nebula (M27)",
        "ra": "19h59m36.319s",
        "dec": "+22d43m16.312s",
        "constellation": "Vulpecula"
    },
    4: {
        "name": "Crab Nebula (M1)",
        "ra": "05h34m31.97s",
        "dec": "+22d00m52.1s",
        "constellation": "Taurus"
    },
    5: {
        "name": "North America Nebula (NGC 7000)",
        "ra": "20h59m17.1s",
        "dec": "+44d31m44s",
        "constellation": "Cygnus"
    },
    6: {
        "name": "Pelican Nebula (IC 5070)",
        "ra": "20h50m48.0s",
        "dec": "+44d20m60.0s",
        "constellation": "Cygnus"
    },
    7: {
        "name": "Veil Nebula (NGC 6960)",
        "ra": "20h45m38.0s",
        "dec": "+30d42m30s",
        "constellation": "Cygnus"
    },
    8: {
        "name": "Helix Nebula (NGC 7293)",
        "ra": "22h29m38.55s",
        "dec": "-20d50m13.6s",
        "constellation": "Aquarius"
    },
    9: {
        "name": "Lagoon Nebula (M8)",
        "ra": "18h03m37s",
        "dec": "-24d23m12s",
        "constellation": "Sagittarius"
    },
    10: {
        "name": "Trifid Nebula (M20)",
        "ra": "18h02m23s",
        "dec": "-23d01m48s",
        "constellation": "Sagittarius"
    },
    11: {
        "name": "Owl Nebula (M97)",
        "ra": "11h14m47.734s",
        "dec": "+55d01m08.50s",
        "constellation": "Ursa Major"
    },
    12: {
        "name": "Heart Nebula (IC 1805)",
        "ra": "02h32m36s",
        "dec": "+61d29m00s",
        "constellation": "Cassiopeia"
    },
    13: {
        "name": "Soul Nebula (IC 1848)",
        "ra": "02h51m36s",
        "dec": "+60d26m00s",
        "constellation": "Cassiopeia"
    }
}


def get_location_by_city():
    """Get coordinates from city and country name using geocoding."""
    geolocator = Nominatim(user_agent="nebula_locator_v1.0")

    print("\nEnter your location (you can be specific):")
    print("Examples: 'New York, USA', 'Tokyo, Japan', 'London, UK'")
    print("          'Paris, France', 'Sydney, Australia'")

    while True:
        try:
            location_str = input("Location: ").strip()
            if not location_str:
                print("Using default location: New York, USA")
                return 40.7128, -74.0060

            print("Geocoding your location...")
            location = geolocator.geocode(location_str, timeout=10)

            if location:
                print(f"Found: {location.address}")
                return location.latitude, location.longitude
            else:
                print("Location not found. Please try again.")
                print("Try being more specific (add country name)")

        except (GeocoderTimedOut, GeocoderServiceError):
            print("Geocoding service error. Using default location: New York, USA")
            return 40.7128, -74.0060
        except Exception as e:
            print(f"Error: {e}. Using default location: New York, USA")
            return 40.7128, -74.0060


def get_location_by_coordinates():
    """Get coordinates directly from user input."""
    print("\nEnter your coordinates:")
    try:
        lat = float(input("Latitude (degrees, + for North, - for South): "))
        lon = float(input("Longitude (degrees, + for East, - for West): "))
        return lat, lon
    except ValueError:
        print("Invalid input. Using default location.")
        return 40.7128, -74.0060


def get_user_location():
    """Let user choose how to enter their location."""
    print("\nHow would you like to enter your location?")
    print("1. City and Country (e.g., 'Tokyo, Japan')")
    print("2. Coordinates (latitude and longitude)")

    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1" or choice == "2":
            break
        print("Please enter 1 or 2.")

    if choice == "2":
        return get_location_by_coordinates()
    else:
        return get_location_by_city()


def get_user_time():
    """Get the observation time from the user or use the current time."""
    print("\n" + "=" * 40)
    print("TIME SELECTION")
    print("=" * 40)
    print("1. Use current system time")
    print("2. Enter a specific date and time")
    print("3. Use tonight's observing time (8 PM local)")

    while True:
        choice = input("Your choice (1, 2, or 3): ").strip()
        if choice in ["1", "2", "3"]:
            break
        print("Please enter 1, 2, or 3.")

    if choice == "2":
        while True:
            try:
                date_str = input("Enter date and time (YYYY-MM-DD HH:MM:SS): ")
                naive_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                aware_dt = naive_dt.replace(tzinfo=pytz.UTC)
                obs_time = Time(aware_dt)
                print(f"Using specified time: {obs_time.iso}")
                break
            except ValueError:
                print("Invalid format. Please use YYYY-MM-DD HH:MM:SS format.")
            except Exception as e:
                print(f"Error: {e}. Please try again.")

    elif choice == "3":
        print("Using 8 PM local time for optimal night sky viewing...")
        obs_time = Time.now()
        obs_time = obs_time + 12 * u.hour
        print(f"Approximate evening time: {obs_time.iso}")

    else:
        obs_time = Time.now()
        print(f"Using current time: {obs_time.iso}")

    return obs_time


def display_nebula_info(nebula):
    """Display information about the selected nebula."""
    print("\n" + "=" * 60)
    print(f"NEBULA INFORMATION: {nebula['name']}")
    print("=" * 60)
    print(f"Constellation: {nebula['constellation']}")
    print(f"Coordinates (J2000): RA {nebula['ra']}, Dec {nebula['dec']}")

    # Additional info based on nebula type
    if "Orion" in nebula['name']:
        print("\nVisibility: Brightest nebula, visible to naked eye!")
        print("Best viewing: Winter months")
    elif "Ring" in nebula['name'] or "Dumbbell" in nebula['name']:
        print("\nType: Planetary nebula (remains of a dead star)")
        print("Best viewed with: Telescope")
    elif "Crab" in nebula['name']:
        print("\nType: Supernova remnant (observed in 1054 AD)")
        print("Contains: Pulsar at its center")
    elif "Lagoon" in nebula['name'] or "Trifid" in nebula['name']:
        print("\nBest viewing: Summer months")
        print("Location: In the Milky Way's center direction")
    elif "Helix" in nebula['name']:
        print("\nType: Closest planetary nebula to Earth")
        print("Nickname: 'Eye of God'")
    print("=" * 60)


def calculate_visibility(altitude):
    """Calculate and return visibility assessment."""
    if altitude > 30:
        return "Excellent - High in the sky, ideal for observation"
    elif altitude > 15:
        return "Good - Reasonably high for observation"
    elif altitude > 5:
        return "Fair - Low in the sky, atmospheric effects noticeable"
    elif altitude > 0:
        return "Poor - Very low, near horizon. Wait for better time."
    else:
        return "Not visible - Below horizon"


def get_compass_direction(azimuth):
    """Convert azimuth to compass direction."""
    compass_points = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                      'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    compass_idx = round(azimuth / 22.5) % 16
    return compass_points[compass_idx]


def main():
    print("=" * 70)
    print("NEBULA LOCATION FINDER")
    print("=" * 70)
    print("Find where nebulas are in your sky right now!")
    print()

    try:
        # Get observer's location
        lat, lon = get_user_location()
        print(f"\nYour location: {lat:.4f} N, {lon:.4f} E")

        # Handle longitude sign convention
        if lon < 0:
            lon_display = f"{-lon:.4f} W" if lon < 0 else f"{lon:.4f} E"
        else:
            lon_display = f"{lon:.4f} E"

        print(f"Coordinates: {lat:.4f} N, {lon_display}")

        location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=0 * u.m)

        # Get observation time
        obs_time = get_user_time()

        # Display the list of nebulae
        print("\n" + "=" * 70)
        print("AVAILABLE NEBULAS")
        print("=" * 70)

        print("\nWINTER/SPRING NEBULAS:")
        winter_nebulae = [1, 4, 11]  # Orion, Crab, Owl
        for key in winter_nebulae:
            neb = NEBULAE[key]
            print(f"  {key:2d}. {neb['name']:30} ({neb['constellation']})")

        print("\nSUMMER NEBULAS:")
        summer_nebulae = [2, 5, 6, 7, 9, 10]  # Ring, N.America, Pelican, Veil, Lagoon, Trifid
        for key in summer_nebulae:
            neb = NEBULAE[key]
            print(f"  {key:2d}. {neb['name']:30} ({neb['constellation']})")

        print("\nAUTUMN NEBULAS:")
        autumn_nebulae = [3, 8, 12, 13]  # Dumbbell, Helix, Heart, Soul
        for key in autumn_nebulae:
            neb = NEBULAE[key]
            print(f"  {key:2d}. {neb['name']:30} ({neb['constellation']})")

        # Get user's choice
        while True:
            try:
                choice = int(input("\nEnter the number of the nebula (1-13): "))
                if 1 <= choice <= 13:
                    break
                else:
                    print("Please enter a number between 1 and 13.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        selected = NEBULAE[choice]

        # Display nebula information
        display_nebula_info(selected)

        # Create a SkyCoord object for the nebula
        nebula_coord = SkyCoord(ra=selected['ra'], dec=selected['dec'], frame='icrs')

        # Convert to AltAz frame
        altaz_frame = AltAz(obstime=obs_time, location=location)
        nebula_altaz = nebula_coord.transform_to(altaz_frame)

        # Extract altitude and azimuth
        alt = nebula_altaz.alt.degree
        az = nebula_altaz.az.degree

        # Display results
        print("\n" + "=" * 70)
        print("CURRENT POSITION IN YOUR SKY")
        print("=" * 70)
        print(f"Nebula: {selected['name']}")
        print(f"Time: {obs_time.iso}")
        print(f"Your Location: {lat:.4f} N, {lon_display}")
        print("\n" + "-" * 40)
        print(f"Altitude: {alt:.1f} degrees")
        print(f"Azimuth:  {az:.1f} degrees")
        print("-" * 40)

        # Convert azimuth to compass direction
        compass_dir = get_compass_direction(az)

        # Enhanced visibility assessment
        visibility = calculate_visibility(alt)

        print(f"\nDirection: {compass_dir} ({az:.0f} degrees)")
        print(f"Visibility: {visibility}")

        if alt > 0:
            if alt > 30:
                print("   * Perfect time for observation!")
            elif alt > 15:
                print("   * Good time to observe")
            else:
                print("   * Consider observing when it's higher in the sky")

            # Suggest better time if currently low
            if 0 < alt < 20:
                print("\nTip: This nebula would be better observed when")
                print("     it's higher in the sky (above 30 degrees altitude).")
        else:
            print("\nThis nebula is currently below the horizon.")
            # Calculate approximate rise time
            hours_till_rise = max((0 - alt) / 15, 0.1)  # Approximate: 15° per hour
            if hours_till_rise > 0:
                rise_time = obs_time + hours_till_rise * u.hour
                print(f"It will rise at approximately: {rise_time.iso.split()[1][:5]} UTC")
            print("Check again in a few hours!")

        # Add constellation information
        print(f"\nLook in the constellation: {selected['constellation']}")

        # Save results option
        save = input("\nSave these results to a file? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"nebula_position_{selected['name'].split()[0]}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Nebula: {selected['name']}\n")
                f.write(f"Time: {obs_time.iso}\n")
                f.write(f"Location: {lat:.4f} N, {lon_display}\n")
                f.write(f"Altitude: {alt:.1f} degrees\n")
                f.write(f"Azimuth: {az:.1f} degrees ({compass_dir})\n")
                f.write(f"Visibility: {visibility}\n")
                f.write(f"Constellation: {selected['constellation']}\n")
            print(f"Results saved to {filename}")

        print("\n" + "=" * 70)
        print("Happy stargazing!")
        print("=" * 70)

        # Ask if user wants to check another nebula
        another = input("\nCheck another nebula? (y/n): ").strip().lower()
        if another == 'y':
            print("\n" * 3)
            main()

    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please check your inputs and try again.")


if __name__ == "__main__":
    # Check for required libraries
    try:
        import astropy
        import geopy
        import pytz
    except ImportError as e:
        print("Missing required libraries. Please install them using:")
        print("pip install astropy geopy pytz")
        print(f"\nError details: {e}")
        sys.exit(1)

    main()