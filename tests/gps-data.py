import json
import os
import subprocess
from colorama import Fore, Style

def parse_gps_data(data):
    if "class" in data and data["class"] == "TPV":
        print(f"=== GPS Data ===")
        print(f"Timestamp: {data['time']}")
        print(f"Lat: {data['lat']:.6f}°")
        print(f"Lon: {data['lon']:.6f}°")
        print(f"Alt: {data['alt']:.1f} metros")
        print(f"Speed: {data['speed']:.2f} m/s")
        print(f"Rumbo: {data['track']:.2f}°")
    elif "class" in data and data["class"] == "SKY":
        print(f"=== Setellite data ===")
        print(f"Num visible sattelites: {data['nSat']}")
        print(f"Num used sattelites: {data['uSat']}")
        for sat in data['satellites']:
            if 'el' in sat and 'az' in sat and 'ss' in sat:
                used_str = Fore.GREEN + "SI" + Style.RESET_ALL if sat['used'] else Fore.RED + "NO" + Style.RESET_ALL
                print(f"PRN: {sat['PRN']}, Elevation: {sat['el']}, Azimuth: {sat['az']}, Signal: {sat['ss']}, Used: {used_str}")
            else:
                print(f">> ERR Incomplete satellite data ..: {sat}")
    else:
        print(f"=== Unknown data ===")
        print(json.dumps(data, indent=4))

def main():
    process = subprocess.Popen(['gpspipe', '-w'], stdout=subprocess.PIPE)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        data = json.loads(line)
        parse_gps_data(data)
        print()


if __name__ == "__main__":
    main()

