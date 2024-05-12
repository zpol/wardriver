import csv
import json
import subprocess

def parse_csv_to_json(file_path):
    wifi_data = []

    with open(file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)  

        print("[+] Reading data...")
        for row in csv_reader:
            if len(row) < 15:  
                continue

            if row[0].strip() == "BSSID":  
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
                "Key": row[14]
            })

    return {
        "wifi_data": wifi_data
    }

if __name__ == "__main__":
    csv_file_path = "data/wifi_data-01.csv"  
    parsed_data = parse_csv_to_json(csv_file_path)

    with open("data/wifi_data.json", "w") as outfile:
        json.dump(parsed_data, outfile, indent=2)

    print("[+] Data parsed and saved into: data/wifi_data.json")

