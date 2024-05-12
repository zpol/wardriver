# Function to test GET GPS data
get_gps_data() {
    gpspipe -w | while read -r line; do
        if echo "$line" | grep -q '"lat":' && echo "$line" | grep -q '"lon":'; then
            latitude=$(echo "$line" | grep -oP '(?<="lat":)[^,]+')
            longitude=$(echo "$line" | grep -oP '(?<="lon":)[^,]+')
            echo "[+] Latitude: $latitude, Longitude: $longitude"
        fi
    done
}


get_gps_data
