import socket
import threading
import time
import cv2
import time
import numpy as np
import zxingcpp

from datetime import datetime
from djitellopy import Tello

tello_ip = "192.168.10.1"
tello_port = 8889

tello_address = (tello_ip, tello_port)


# Receiving from tello
VS_UDP_IP = "0.0.0.0"
VS_UDP_PORT = 11111

# Preparing Objects for VideoCapture
cap = None
# Object preparation for data receiving
response = None

drone_instance = Tello()
time.sleep(2)
drone_instance.connect()
# drone_instance.takeoff()
drone_instance.streamon()


# # Create sockets for communication
# # Address family: AF_INET (IPv4), Socket type: SOCK_DGRAM (UDP)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def socketclose():
    serversocket.close()


# Functions for receiving data
def run_udp_receiver():
    while True:
        try:
            response, _ = serversocket.recvfrom(1024)
            print(response.decode(encoding="utf-8"))

        except Exception as e:
            # socketclose()
            print("**** Exit recv_****")
            print(e)
            break


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


thread = threading.Thread(target=run_udp_receiver, args=())
thread.daemon = True
thread.start()

# # Start of video streaming
# serversocket.sendto('streamon'.encode('utf-8'), tello_address)

udp_video_address = "udp://@" + VS_UDP_IP + ":" + str(VS_UDP_PORT)

if cap is None:
    cap = cv2.VideoCapture(udp_video_address)
if not cap.isOpened():
    cap.open(udp_video_address)

print(f"Battery: {drone_instance.get_battery()}%")


qr_results = {}
while True:
    ret, img = cap.read()
    if ret:
        start_time = time.time()  # testing speed
        results = zxingcpp.read_barcodes(img)  # calls the barcode reader fn.
        end_time = time.time()

        for result in results:
            positions = str(result.position)
            positions = parse_zxcpp_pos(positions)
            bbox = cv2.boundingRect(positions)

            # Draw a bounding box around the QR code
            cv2.rectangle(
                img,
                (int(bbox[0]), int(bbox[1])),
                (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])),
                (0, 255, 0),
                2,
            )

            # Get the text content of the QR code
            qr_text = result.text
            if qr_text not in qr_results:
                qr_results[qr_text] = datetime.now()

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
        print(qr_results)
        break

cap.release()
cv2.destroyAllWindows()
socket.sendto("streamoff".encode("utf-8"), tello_address)

socket.sendto("land".encode("utf-8"), tello_address)
