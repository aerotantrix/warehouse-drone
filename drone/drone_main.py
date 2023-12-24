import cv2
import time
import socket
import requests
import zxingcpp
import threading
import numpy as np

from typing import Dict
from queue import Queue
from djitellopy import Tello
from wifi_connect import WiFi
from datetime import datetime


class TelloMain:
    def __init__(
        self,
        wifi_connect_tries: int = 5,
        row_size: int = 5,
        column_size: int = 5,
        box_height: int = 52,
        box_width: int = 72,
        speed: int = 20,
        shelf: int = 1,
    ) -> None:
        self.__tello_ip = "192.168.10.1"
        self.__tello_port = 8889
        self.__tello_address = (self.__tello_ip, self.__tello_port)

        self.__server = "http://192.168.1.100:8000/"
        self.__access_token = ""

        # Receiving from tello
        self.__VS_UDP_IP = "0.0.0.0"
        self.__VS_UDP_PORT = 11111
        self.__udp_video_address = (
            "udp://@" + self.__VS_UDP_IP + ":" + str(self.__VS_UDP_PORT)
        )

        self.__wifi = WiFi()

        self.__drone_wifi_name = "TELLO-C3A55B"
        self.__drone_wifi_password = None

        self.drone_instance = Tello()
        try:
            self.connect_to_tello(tries=wifi_connect_tries)
        except Exception as e:
            print(e)

        self.__serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.__udp_thread = threading.Thread(target=self.run_udp_receiver)
        self.__udp_thread.daemon = True
        self.__udp_thread.start()

        print(f"Battery: {self.drone_instance.get_battery()}%")

        # image processing
        self.__cap = cv2.VideoCapture(self.__udp_video_address)
        if not self.__cap.isOpened():
            self.__cap.open(self.__udp_video_address)

        # self.__response = None
        # flight params
        self.pattern_done = False
        self.__row_size, self.__column_size = row_size, column_size
        self.__box_height, self.__box_width = box_height, box_width
        self.__shelf = shelf
        self.__speed = speed

        self.__flight_q = Queue()

    def connect_to_tello(self, tries: int) -> None:
        # First connect to drone's Wifi
        if self.__wifi.get_current_network() != self.__drone_wifi_name:
            print(
                f"Not connected to {self.__drone_wifi_name}, trying to connect to it now"
            )
            for i in range(tries):
                print(f"TRY {i}:", sep=" ")
                self.__wifi.connect_to_wifi(
                    self.__drone_wifi_name,
                    self.__drone_wifi_password,
                    print_output=True,
                )
                if self.__wifi.get_current_network() == self.__drone_wifi_name:
                    print(f"Connected to {self.__drone_wifi_name}")
                    break
            if self.__wifi.get_current_network() != self.__drone_wifi_name:
                raise Exception(
                    f"Failed to Connect to the drone's WiFi {self.__drone_wifi_name}"
                )

        time.sleep(2)
        self.drone_instance.connect()
        self.drone_instance.streamon()

    def socketclose(self):
        self.__serversocket.close()

    def run_udp_receiver(self):
        while True:
            try:
                response, _ = self.__serversocket.recvfrom(1024)
                print(response.decode(encoding="utf-8"))

            except Exception as e:
                self.socketclose()
                print("**** Exit recv_****")
                print(e)
                break

    def move_to_target_location(self) -> None:
        try:
            if self.drone_instance.get_battery() <= 10:
                raise Exception(f"Low Battery: {self.drone_instance.get_battery()}")
            else:
                print(f"Battery: {self.drone_instance.get_battery()}%")
            self.drone_instance.takeoff()
            #correct z
            self.drone_instance.move_up(
                self.__column_size * (self.__box_height - 1) - 40
            )
        except Exception as e:
            print("Error in move_to_target_location(): ", e)

    def move_to_initial_location(self) -> None:
        if self.__row_size % 2 == 0:
            self.drone_instance.land()
        else:
            self.drone_instance.move_left(self.__row_size * self.__box_height)
            self.drone_instance.land()

    def pattern(self) -> None:
        self.pattern_done = False
        self.move_to_target_location()
        try:
            self.drone_instance.set_speed(self.__speed)
            bin_key = 0
            for i in range(self.__row_size):
                for j in range(self.__column_size):
                    if i % 2 == 0:
                        self.drone_instance.move_right(self.__box_height)
                    elif i % 2 != 0:
                        self.drone_instance.move_left(self.__box_height)
                    bin_key += 1  # Bin values starting from left
                    if bin_key == self.__row_size * self.__column_size - 1:
                        break
                    self.__flight_q.put([i, j, self.__shelf, time.time()])
                if (self.__row_size - i) != 1:
                    self.drone_instance.move_down(self.__box_width)
                else:
                    self.move_to_initial_location()
        except:
            pass
        finally:
            self.pattern_done = True

    @staticmethod
    def parse_zxcpp_pos(position: str) -> np.ndarray:
        points = position.split(" ")
        points[-1] = points[-1].removesuffix("\x00")
        point_tuples = []
        for point in points:
            point_tuples.append(point.split("x"))

        for i in range(len(point_tuples)):
            for j in range(len(point_tuples[i])):
                point_tuples[i][j] = int(point_tuples[i][j])
        return np.array(point_tuples)

    def run(self, draw_bbox: bool = True) -> None:
        self.__flight_thread = threading.Thread(target=self.pattern)
        self.__flight_thread.daemon = True
        self.__flight_thread.start()

        while not self.pattern_done:
            success, img = self.__cap.read()

            if success:
                start_time = time.time()  # testing speed
                results = zxingcpp.read_barcodes(img)
                end_time = time.time()

                for result in results:
                    positions = str(result.position)
                    positions = TelloMain.parse_zxcpp_pos(positions)
                    qr_text = result.text

                    if draw_bbox:
                        bbox = cv2.boundingRect(positions)
                        cv2.rectangle(
                            img,
                            (int(bbox[0]), int(bbox[1])),
                            (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])),
                            (0, 255, 0),
                            2,
                        )
                        # Place text under the bounding box
                        cv2.putText(
                            img,
                            f"{qr_text} {(end_time-start_time):.3f}ms",
                            (int(bbox[0]), int(bbox[1] + bbox[3] + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            2,
                        )
                cv2.imshow("tello", img)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    def update_server(self) -> None:
        pass

    def login_to_server(self) -> None:
        url = self.__server + "login-station"
        payload = {
            "username": "eagleEye",
            "password": "12345",
        }
        response = requests.post(url, json=payload)

        try:
            if response.status_code == 200:
                self.__access_token = response.json()["access_token"]
            else:
                raise Exception("Login Failed")
        except Exception as e:
            print(e)

    def __del__(self):
        self.__cap.release()
        cv2.destroyAllWindows()


tello = TelloMain(row_size=4,column_size=4)
tello.run()
 