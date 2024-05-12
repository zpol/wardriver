import csv
import json
import subprocess
import random 
import string
import os
from colorama import init, Fore

init(autoreset=True)

def parse_csv_to_json(file_path, latitude, longitude):
    wifi_data = []
    print(f"[++] - Parsing wifi data .....")
    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)  # read headers

        for row in csv_reader:
            if len(row) < 15:  # check row items #
                continue

            if row[0].strip() == "BSSID":  # skip headers
                continue

            try:
                channel = int(row[3])  
            except ValueError:
                continue  

            wifi_data.append({
                "BSSID": row[0],
                "First time seen": row[1],
                "Last time seen": row[2],
                "Channel": channel,
                "Speed": int(row[4]),
                "Privacy": row[5],
                "Cipher": row[6],
                "Authentication": row[7],
                "Power": int(row[8]),
                "# beacons": int(row[9]),
                "# IV": int(row[10]),
                "LAN IP": row[11],
                "ID-length": int(row[12]),
                "ESSID": row[13],
                "Key": row[14],
                "Latitude": latitude,
                "Longitude": longitude
            })

    return {
        "wifi_data": wifi_data
    }


def get_gps_data():
    try:
        gpspipe_output = subprocess.run(["gpspipe", "-w", "-x3"], stdout=subprocess.PIPE, text=True)
        lines = gpspipe_output.stdout.strip().split('\n')  # Split the stdout string into individual lines
        for line in lines:
            parsed_data = json.loads(line)
            if "lat" in parsed_data and "lon" in parsed_data:
                latitude = parsed_data["lat"]
                longitude = parsed_data["lon"]
                return latitude, longitude
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        print("[ERR] - Error obtaining GPS data.")


def delete_file(wifi_data_file):

    file2del = wifi_data_file

    try:
        os.remove(file2del)
        print(f"[+] - File '{file2del}' deleted successfully")
    except FileNotFoundError:
        print(f"[ERR] - File '{file2del}' not found")
    except Exception as e:
        print(f"[ERR] - Error deleting '{file2del}': {e} ")

def generate_random_script(length=8):
    characters = string.ascii_lowercase + string.digits 
    random_script = ''.join(random.choice(characters) for _ in range(length))
    return random_script


def process_wifi_data_from_file(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    
    num_bssid = len(data["wifi_data"])
    unique_latitudes = set(entry["Latitude"] for entry in data["wifi_data"])
    unique_longitudes = set(entry["Longitude"] for entry in data["wifi_data"])

    
    essids = [entry["ESSID"] for entry in data["wifi_data"]]
    privacies = [entry["Privacy"] for entry in data["wifi_data"]]

    
    essids_combined = ", ".join(filter(None, essids))  # Filtrar y unir solo los ESSID no vacíos
    privacies_combined = ", ".join([Fore.RED + privacy if "WPA" in privacy else privacy for privacy in privacies])

    return num_bssid, unique_latitudes, unique_longitudes, essids_combined, privacies_combined


def find_latest_csv(directory="data/"):
    try:
        
        files = os.listdir(directory)
        csv_files = [file for file in files if file.endswith(".csv")]
        latest_csv = max(csv_files, key=lambda file: os.path.getctime(os.path.join(directory, file)))

        return latest_csv
    except OSError as e:
        print(f"Error al intentar encontrar el último archivo CSV: {e}")
        return None


if __name__ == "__main__":
    latest_csv_file = find_latest_csv()
    csv_file_path = "./data/" + latest_csv_file  
    latitude, longitude = get_gps_data()
    print(f" [+] Checking file path: {csv_file_path}")
    parsed_data = parse_csv_to_json(csv_file_path, latitude, longitude)

    random_value= generate_random_script()
    random_filename_path="data/wifi_data-" + random_value + ".json"
    with open(random_filename_path, "w") as outfile:
        json.dump(parsed_data, outfile, indent=2)

    print("[++] Data parsed and saved into: data/wifi_data" + random_value + ".json")
    print("[++] Deleting file: data/wifi_data.json")
    delete_file('data/wifi_data-01.csv')

    # get live report
    file_path = random_filename_path
    num_bssid, latitudes, longitudes, essids_combined, privacies_combined = process_wifi_data_from_file(file_path)

    print(f"Num BSSID detected: {num_bssid}")
    print(f"Lat: {latitudes}")
    print(f"Lon: {longitudes}")
    print(f"ESSIDs: {essids_combined}")
    print(f"Privacy: {privacies_combined}")


