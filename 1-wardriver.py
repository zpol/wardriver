import subprocess
import json
import os
import time
import base64


def b():
    t="ICAgICBfLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fX19fX19fX19fX19fX19fX19fX19fX19fX18vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtX19fX19fX19fX19fXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fXwogICAgXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fLxtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV8vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fX19fXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fX18vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fX19fXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fX18vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG0gCiAgIF8vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtX19fX18vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtX19fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV8vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtX19fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV8vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fXyAgCiAgXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV8vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtX19fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fX18vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fX18vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtX19fX18vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtX19fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fX18vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtX19fX19fICAgCiBfLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV8vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fX19fX19fX18vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fX19fX19fLxtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXC8bWzM5OzAwbRtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fLxtbMzg7NTsxMzA7MDFtXF8bWzM5OzAwbV9fX19fX18vG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cLxtbMzk7MDBtG1szODs1OzEzMDswMW1cXxtbMzk7MDBtXy8bWzM4OzU7MTMwOzAxbVwvG1szOTswMG0bWzM4OzU7MTMwOzAxbVxfG1szOTswMG1fX19fX18gICAgCl9fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fX19fdiAbWzM4OzU7MjQxbTAbWzM5bS4zLjBfX19fXyAgIAo="

    decoded_bytes = base64.b64decode(t)
    decoded_text = decoded_bytes.decode('utf-8')
    print(decoded_text)



def enable_monitor_mode(interface):
    try:
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
        subprocess.run(["sudo", "iw", interface, "set", "monitor", "control"], check=True)
        subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], check=True)
        print(f"[+] - Monitor mode enabled for {interface}.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")




def run_airodump():
    # Exec airodump-ng + gather datda into csv
    try:
        print(f"[+] - Starting capturing data packets...")
        subprocess.run(["sudo", "airodump-ng", "--output-format", "csv", "-w", "data/wifi_data", "wlan1"], capture_output=True, timeout=5)
    except subprocess.TimeoutExpired:
        pass
    except subprocess.CalledProcessError as e:
        print(f"[ERR] - Error running airodump-ng: {e}")




def step2():
    print("[+] - Starting to parse CSV data:")
    try:
        resultado = subprocess.run(["python3", "3-coordinates-aggregator.py"], capture_output=True, text=True)

        print("[+] - Output for: [GPS Coordinates Aggregation]:")
        print(resultado.stdout)
        
        if resultado.returncode == 0:
            print("[+] - Coordinate Aggregator executed succesfuly.")
        else:
            print("[ERR] - ERR executing Coordinates Aggregator.")
    except Exception as e:
        print(f"[ERR] - Error executing coordinates aggregator: {e}")
    except subprocess.CalledProcessError as e:
        print(f"[ERR] - Error executing coordinates aggregator: {e}")








def main():
    b()
    wifi_data = []

    # enable monitor mode for iface wlan1
    interface = "wlan1"  
    enable_monitor_mode(interface)

    while True:
        run_airodump()

        print(f"[+] Sleep 7 sec....")
        time.sleep(7)

        step2()






if __name__ == "__main__":
    main()

