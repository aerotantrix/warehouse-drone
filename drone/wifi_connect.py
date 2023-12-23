import subprocess

from typing import List

class WiFi:
    def get_wifi_networks(self) -> List[str]:
        try:
            # Run nmcli command to list available Wi-Fi networks
            cmd = "nmcli -f 'SSID' device wifi list"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            output = result.stdout
            
            # Split the output by newlines and filter out empty lines
            networks = output.split('\n')[1:]
            for i in range(len(networks)):
                 networks[i] = networks[i].strip()
            return networks
        except subprocess.CalledProcessError as e:
            print(f"Error: {str(e)}")
            return []
        
    def get_current_network(self) -> str | None:
        try:
            # Run nmcli command to list available Wi-Fi networks
            cmd = "nmcli -t -f active,ssid dev wifi"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            output = result.stdout
            
            # Split the output by newlines and filter out empty lines
            networks = output.split('\n')
            for network in networks:
                if network[0:3] == 'yes':
                    return network[4:]
        except subprocess.CalledProcessError as e:
            print(f"Error: {str(e)}")
            return None

    def connect_to_wifi(self, network_name, password) -> None:
        try:
            if password:
                # Connect to the Wi-Fi network with password
                cmd = f"nmcli device wifi connect '{network_name}' password '{password}'"
            else:
                # Connect to the Wi-Fi network without password
                cmd = f"nmcli device wifi connect '{network_name}'"

            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error: {str(e)}")

wifi = WiFi()
networks = wifi.get_wifi_networks()
print(wifi.get_current_network())
    
