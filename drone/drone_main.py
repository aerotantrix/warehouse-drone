import cv2
import zxing
import time
from djitellopy import Tello
from queue import Queue
import threading
import requests
import numpy as np
#import json

from wifi_connect import WiFi

class Inv:
    def __init__(self) -> None:
        self.reader = zxing.BarCodeReader()
        self.connector = WiFi()
        self.desired_network = "TELLO-C3A55B"
        self.password = ''
        self.initialize_connection()
        self.tello = Tello()
        self.Q = Queue()
        self.Dictionary={}
        self.ServerUrl = "http://192.168.1.100"
        #self.__JsonFilePath="data.json"
        self.row_size,self.column_size=4,4
        self.box_height,self.box_width=46,72
        self.speed=20
        self.Sleep_time=0.1
        self.ProductData=""
        self.Status=-1
        print("HI ",self)
        # Choose a network to connect (replace 'YourNetworkName' with the desired network name)

        # Create an instance of connect2wifi class
        self.networks = self.connector.get_wifi_networks()
        self.wifi_connect=self.connector.connect_to_wifi(self.desired_network,self.password)
        #connect to tello
        self.tello.connect()
        
    def initialize_connection(self):
        if self.connector.get_current_network() != self.desired_network:
            self.connector.connect_to_wifi(self.desired_network, self.password)
            if self.connector.get_current_network() != self.desired_network:
                raise Exception(f'Cannot connect to {self.desired_network}')
        
    def move_to_target_location(self) -> None:
        try:
            if self.tello.get_battery() <= 10:
                raise Exception(f'Low Battery: {self.tello.get_battery()}')
            else:
                print(f'Battery: {self.tello.get_battery()}%')
            self.tello.takeoff()
            self.tello.streamon()
            self.tello.move_up(self.column_size*(self.box_height - 1)-40)
        except Exception as e:
            print('Error in move_to_target_location(): ', e)
        
        
        
    def move_to_initial_location(self) -> None:
        if self.row_size % 2 == 0:
            self.tello.land()
        else:
            self.tello.move_left(self.row_size*self.box_height)
            self.tello.land()
    
    
    
    def pattern(self) -> None:
        self.tello.set_speed(20)
        bin_key =0
        for i in range(self.row_size):
            for j in range(self.column_size):
                if i % 2 == 0:
                    self.tello.move_right(self.box_height)
                elif i % 2 != 0:
                    self.tello.move_left(self.box_height)
                time.sleep(self.Sleep_time)
                #rack_key = chr(ord('A') + j)    # Convert ASCII to get 'A', 'B', 'C', ...
                #self.ProductData=self.qr_process(i, j)
                if self.ProductData=="Not available":
                    self.Status=0
                self.Status=1
                self.Dictionary={"BIN ID:":bin_key,
                                 "RACK NO:":j,
                                 "SHELF ":1,
                                 "ProductData":self.ProductData,
                                 "Status":self.Status}
                
                #self.send_data_to_server()
                bin_key +=1   # Bin values starting from 1eft
            if (self.row_size-i) != 1:
                self.tello.move_down(self.box_width)
            else:
                self.move_to_initial_location()
                
                
    def qr_process(self, i: int, j: int) -> str:
        while True:
            try:
                image: np.ndarray = self.tello.get_frame_read().frame
                image = cv2.resize(image, (1280,720))
                cv2.imshow("Tello Video Feed", image)
                cv2.imwrite(f'img{i}{j}.png', image)
                result: str = self.reader.decode(f'img{i}{j}'.png).parsed
                if result not in self.Q:
                    self.Q.put(result)
                    return result.text
                else:
                    return "Not available"
            except Exception as e:
                print("Error at qr_process(): ", e)
                return "Not available"
        
        
        
    def send_data_to_server(self):
        try:
            response = requests.post(self.ServerUrl,data=self.Dictionary)
            if response.status_code == 400:
                print("Data sent successfully.")
            else:
                print("Failed to send data. Status code:", response.status_code)

        except (FileNotFoundError) as e:
            print("Error handling data:", e)
        except requests.RequestException as e:
            print("Error sending data:", e)
            
            
    def register_station(self,username, password, stationname, battery):
        url = "http://192.168.1.100:8000/register-station"  # Replace with the actual server IP and port

        # Payload with login credentials
        payload = {
            "username": "eagleEye",
            "password": 12345,
            "stationname": "eagleEye",
            "battery": self.tello.get_battery()
        }

        try:
            # Send POST request to the FastAPI endpoint
            response = requests.post(url, json=payload)

            # Check the response status code
            if response.status_code == 200:
                print("Station registration successful.")
            else:
                print("Failed to register station. Status code:", response.status_code)

        except requests.RequestException as e:
            print("Error sending request:", e)
            
            
def main():
    include=Inv()
    include.move_to_target_location()
    include.pattern()
    include.move_to_initial_location()
    
if __name__=="__main__":
    main()
