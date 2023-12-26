import subprocess

def add_wifi_profile(ssid, password):
    try:
        # Create the command to add WiFi profile
        command = f'netsh wlan add profile filename=nul user={ssid} keyMaterial={password}'

        # Run the command using subprocess
        subprocess.run(command, check=True, shell=True)

        print(f"WiFi profile added for network: {ssid}")

    except subprocess.CalledProcessError as e:
        print(f"Error adding WiFi profile for network: {ssid}")
        print(f"Error message: {e}")

def connect_to_wifi(ssid):
    try:
        # Create the command to connect to WiFi
        command = f'netsh wlan connect name="{ssid}"'

        # Run the command using subprocess
        subprocess.run(command, check=True, shell=True)

        print(f"Connected to WiFi network: {ssid}")

    except subprocess.CalledProcessError as e:
        print(f"Error connecting to WiFi network: {ssid}")
        print(f"Error message: {e}")

# Replace 'YourWiFiSSID' and 'YourWiFiPassword' with your actual WiFi credentials
wifi_ssid = 'Mi10i'
wifi_password = 'ORROR123'

add_wifi_profile(wifi_ssid, wifi_password)
connect_to_wifi(wifi_ssid)
