
import cv2
import zxingcpp
import time
import numpy as np
from djitellopy import Tello

# img = cv2.imread("qr.png")
# tello = Tello()
# tello.connect()
# tello.streamon()
# print(f"Battery: {tello.get_battery()}%")

#cap = cv2.VideoCapture("udp://@0.0.0.0:11111")
cap = cv2.VideoCapture(0)


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



while True:
    success, img = cap.read()  # image as array
    start_time = time.time()  # testing speed
    results = zxingcpp.read_barcodes(img)  # calls the barcode reader fn.
    end_time = time.time()

    for result in results:  # needed for multiple readings, prints o/p for all of them
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

        # Place text under the bounding box
        cv2.putText(
            img,
            qr_text,
            (int(bbox[0]), int(bbox[1] + bbox[3] + 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2,
        )

    print(f"processing time = {(end_time-start_time):.3f}ms")  # testing speed

    cv2.imshow("result", img)  # video preview
    if cv2.waitKey(1) == ord("q"):  # kill preview with "q"
        break

cap.release()  # close object
cv2.destroyAllWindows()  # close all running cv2 instances

