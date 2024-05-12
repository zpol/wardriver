import time
from gps3 import gps3

def main():
    # Conncet to gpsd
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()
    gps_socket.connect()

    try:
        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)

                # there is data?
                if data_stream.TPV['mode'] == 3:
                    
                    print(f"Lat: {data_stream.TPV['lat']:.6f} º")
                    print(f"Long: {data_stream.TPV['lon']:.6f} º")
                    print(f"Alt: {data_stream.TPV['alt']:.1f} meters")
                    print(f"Speed: {data_stream.TPV['speed']:.2f} m/s")
                    print(f"Track: {data_stream.TPV['track']:.2f} º")
                    print(f"GPS time: {data_stream.TPV['time']}")
                    print(f"Num de satellites: {data_stream.SKY['satellites']}")
                    print(f"HDOP: {data_stream.TPV['hdop']}")

                else:
                    print(">> Waiting for GPS data ...")

    except KeyboardInterrupt:
        gps_socket.close()

if __name__ == "__main__":
    main()

