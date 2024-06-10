import os
import json
import mysql.connector
from mysql.connector import Error
import random
import math

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print(">> Connected to DB OK :)")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

def create_table(connection):
    cursor = connection.cursor()
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS wifi_networks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            BSSID VARCHAR(255),
            first_time_seen DATETIME,
            last_time_seen DATETIME,
            channel INT,
            speed INT,
            privacy VARCHAR(255),
            cipher VARCHAR(255),
            authentication VARCHAR(255),
            power INT,
            beacons INT,
            iv INT,
            lan_ip VARCHAR(255),
            id_length INT,
            essid VARCHAR(255),
            wifi_key VARCHAR(255),
            latitude DOUBLE,
            longitude DOUBLE
        )
        """
        cursor.execute(create_table_query)
        print(">> Table 'wifi_networks' already exists")
    except Error as e:
        print(f">> Error creating table: '{e}'")
    cursor.close()

def process_json_files(data_input_folder, connection):
    for filename in os.listdir(data_input_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(data_input_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as json_file:
                try:
                    data = json.load(json_file)
                    if 'wifi_data' in data and isinstance(data['wifi_data'], list):
                        for record in data['wifi_data']:
                            insert_data_into_db(record, connection)
                except json.JSONDecodeError as e:
                    print(f">> Error reading JSON file {filename}: {e}")
                except Error as e:
                    print(f">> Error processing data: '{e}'")

def add_randomness_to_coordinates(lat, lon, delta_meters=20):
    delta_lat = delta_meters / 111000  # Degrees per meter lat
    delta_lon = delta_meters / (111000 * math.cos(math.radians(lat)))  # degrees per meter lon

    random_lat = lat + random.uniform(-delta_lat, delta_lat)
    random_lon = lon + random.uniform(-delta_lon, delta_lon)
    
    return random_lat, random_lon

def check_bssid_exists(bssid, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM wifi_networks WHERE BSSID = %s", (bssid,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

def insert_data_into_db(data, connection):
    cursor = connection.cursor()
    try:
        bssid = data.get('BSSID', '')
        if check_bssid_exists(bssid, connection):
            print(f">> BSSID {bssid} already exists, skipping insertion.")
            return
        
        latitude = data.get('Latitude', 0.0)
        longitude = data.get('Longitude', 0.0)
        if latitude and longitude:
            latitude, longitude = add_randomness_to_coordinates(latitude, longitude)

        insert_query = """
        INSERT INTO wifi_networks (
            BSSID, first_time_seen, last_time_seen, channel, speed, privacy,
            cipher, authentication, power, beacons, iv, lan_ip, id_length,
            essid, wifi_key, latitude, longitude
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            bssid,
            data.get('First time seen', ''),
            data.get('Last time seen', ''),
            data.get('Channel', 0),
            data.get('Speed', 0),
            data.get('Privacy', ''),
            data.get('Cipher', ''),
            data.get('Authentication', ''),
            data.get('Power', 0),
            data.get('# beacons', 0),
            data.get('# IV', 0),
            data.get('LAN IP', ''),
            data.get('ID-length', 0),
            data.get('ESSID', ''),
            data.get('Key', ''),
            latitude,
            longitude
        )
        cursor.execute(insert_query, values)
        connection.commit()
        print(">> Data inserted successfully")
    except Error as e:
        print(f">> Error inserting data: '{e}'")
    cursor.close()

def main():
    connection = create_connection("localhost", "geoip", "password", "geoip")
    if connection is not None:
        create_table(connection)
        process_json_files("./data_input/", connection)
        connection.close()
    else:
        print(">> Error connecting to DB")

if __name__ == "__main__":
    main()






### VERSION WITH SOME RANDOMNESS ADDED
###########################################

# import os
# import json
# import mysql.connector
# from mysql.connector import Error
# import random
# import math

# def create_connection(host_name, user_name, user_password, db_name):
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             passwd=user_password,
#             database=db_name
#         )
#         print(">> Connecetd to DB OK :)")
#     except Error as e:
#         print(f"Error: '{e}'")
#     return connection

# def create_table(connection):
#     cursor = connection.cursor()
#     try:
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS wifi_networks (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             BSSID VARCHAR(255),
#             first_time_seen DATETIME,
#             last_time_seen DATETIME,
#             channel INT,
#             speed INT,
#             privacy VARCHAR(255),
#             cipher VARCHAR(255),
#             authentication VARCHAR(255),
#             power INT,
#             beacons INT,
#             iv INT,
#             lan_ip VARCHAR(255),
#             id_length INT,
#             essid VARCHAR(255),
#             wifi_key VARCHAR(255),
#             latitude DOUBLE,
#             longitude DOUBLE
#         )
#         """
#         cursor.execute(create_table_query)
#         print(">> Table 'wifi_networks' already exists")
#     except Error as e:
#         print(f">> Error creating table: '{e}'")
#     cursor.close()

# def process_json_files(data_input_folder, connection):
#     for filename in os.listdir(data_input_folder):
#         if filename.endswith(".json"):
#             file_path = os.path.join(data_input_folder, filename)
#             with open(file_path, 'r', encoding='utf-8') as json_file:
#                 try:
#                     data = json.load(json_file)
#                     if 'wifi_data' in data and isinstance(data['wifi_data'], list):
#                         for record in data['wifi_data']:
#                             insert_data_into_db(record, connection)
#                 except json.JSONDecodeError as e:
#                     print(f">> Error reading JSON file {filename}: {e}")
#                 except Error as e:
#                     print(f">> Error processing data: '{e}'")

# def add_randomness_to_coordinates(lat, lon, delta_meters=20):
#     delta_lat = delta_meters / 111000  # Grados por metro en latitud
#     delta_lon = delta_meters / (111000 * math.cos(math.radians(lat)))  # Grados por metro en longitud

#     random_lat = lat + random.uniform(-delta_lat, delta_lat)
#     random_lon = lon + random.uniform(-delta_lon, delta_lon)
    
#     return random_lat, random_lon

# def insert_data_into_db(data, connection):
#     cursor = connection.cursor()
#     try:
#         latitude = data.get('Latitude', 0.0)
#         longitude = data.get('Longitude', 0.0)
#         if latitude and longitude:
#             latitude, longitude = add_randomness_to_coordinates(latitude, longitude)

#         insert_query = """
#         INSERT INTO wifi_networks (
#             BSSID, first_time_seen, last_time_seen, channel, speed, privacy,
#             cipher, authentication, power, beacons, iv, lan_ip, id_length,
#             essid, wifi_key, latitude, longitude
#         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             data.get('BSSID', ''),
#             data.get('First time seen', ''),
#             data.get('Last time seen', ''),
#             data.get('Channel', 0),
#             data.get('Speed', 0),
#             data.get('Privacy', ''),
#             data.get('Cipher', ''),
#             data.get('Authentication', ''),
#             data.get('Power', 0),
#             data.get('# beacons', 0),
#             data.get('# IV', 0),
#             data.get('LAN IP', ''),
#             data.get('ID-length', 0),
#             data.get('ESSID', ''),
#             data.get('Key', ''),
#             latitude,
#             longitude
#         )
#         cursor.execute(insert_query, values)
#         connection.commit()
#         print(">> Data insertaded successfuly")
#     except Error as e:
#         print(f">> Error inserting data: '{e}'")
#     cursor.close()

# def main():
#     connection = create_connection("localhost", "geoip", "password", "geoip")
#     if connection is not None:
#         create_table(connection)
#         process_json_files("./data_input/", connection)
#         connection.close()
#     else:
#         print(">> Error connecting to DB")

# if __name__ == "__main__":
#     main()




######## OLD CODE #######################
# #####################################
#  
# import os
# import json
# import mysql.connector
# from mysql.connector import Error

# def create_connection(host_name, user_name, user_password, db_name):
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             passwd=user_password,
#             database=db_name
#         )
#         print("Conexión a la base de datos de MariaDB exitosa")
#     except Error as e:
#         print(f"Error: '{e}'")
#     return connection

# def create_table(connection):
#     cursor = connection.cursor()
#     try:
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS wifi_networks (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             BSSID VARCHAR(255),
#             first_time_seen DATETIME,
#             last_time_seen DATETIME,
#             channel INT,
#             speed INT,
#             privacy VARCHAR(255),
#             cipher VARCHAR(255),
#             authentication VARCHAR(255),
#             power INT,
#             beacons INT,
#             iv INT,
#             lan_ip VARCHAR(255),
#             id_length INT,
#             essid VARCHAR(255),
#             wifi_key VARCHAR(255),
#             latitude DOUBLE,
#             longitude DOUBLE
#         )
#         """
#         cursor.execute(create_table_query)
#         print("Tabla 'wifi_networks' creada o ya existe")
#     except Error as e:
#         print(f"Error al crear la tabla: '{e}'")
#     cursor.close()

# def process_json_files(data_input_folder, connection):
#     for filename in os.listdir(data_input_folder):
#         if filename.endswith(".json"):
#             file_path = os.path.join(data_input_folder, filename)
#             with open(file_path, 'r', encoding='utf-8') as json_file:
#                 try:
#                     data = json.load(json_file)
#                     if 'wifi_data' in data and isinstance(data['wifi_data'], list):
#                         for record in data['wifi_data']:
#                             insert_data_into_db(record, connection)
#                 except json.JSONDecodeError as e:
#                     print(f"Error al leer el archivo JSON {filename}: {e}")
#                 except Error as e:
#                     print(f"Error al procesar datos: '{e}'")

# def insert_data_into_db(data, connection):
#     cursor = connection.cursor()
#     try:
#         insert_query = """
#         INSERT INTO wifi_networks (
#             BSSID, first_time_seen, last_time_seen, channel, speed, privacy,
#             cipher, authentication, power, beacons, iv, lan_ip, id_length,
#             essid, wifi_key, latitude, longitude
#         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """
#         values = (
#             data.get('BSSID', ''),
#             data.get('First time seen', ''),
#             data.get('Last time seen', ''),
#             data.get('Channel', 0),
#             data.get('Speed', 0),
#             data.get('Privacy', ''),
#             data.get('Cipher', ''),
#             data.get('Authentication', ''),
#             data.get('Power', 0),
#             data.get('# beacons', 0),
#             data.get('# IV', 0),
#             data.get('LAN IP', ''),
#             data.get('ID-length', 0),
#             data.get('ESSID', ''),
#             data.get('Key', ''),
#             data.get('Latitude', 0.0),
#             data.get('Longitude', 0.0)
#         )
#         cursor.execute(insert_query, values)
#         connection.commit()
#         print("Datos insertados exitosamente")
#     except Error as e:
#         print(f"Error al insertar datos: '{e}'")
#     cursor.close()

# def main():
#     connection = create_connection("localhost", "geoip", "password", "geoip")
#     if connection is not None:
#         create_table(connection)
#         process_json_files("./data_input/", connection)
#         connection.close()
#     else:
#         print("Error al conectar con la base de datos")

# if __name__ == "__main__":
#     main()
