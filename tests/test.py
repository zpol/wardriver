import subprocess
import json

def get_gps_data():
    try:
        gpspipe_output = subprocess.Popen(["gpspipe", "-w"], stdout=subprocess.PIPE, text=True)
        for line in gpspipe_output.stdout:
            parsed_data = json.loads(line)
            if "lat" in parsed_data and "lon" in parsed_data:
                latitude = parsed_data["lat"]
                longitude = parsed_data["lon"]
                print(f"[+] Latitude: {latitude}, Longitude: {longitude}")
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        print(">> Err obtaining GPS data.")

if __name__ == "__main__":
    get_gps_data()

