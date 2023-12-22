from csv import reader
import cv2
import zxing
import time
from datetime import datetime, timedelta
from PIL import Image

telloVideo = cv2.VideoCapture("udp://@0.0.0.0:11111")
telloVideo.set(cv2.CAP_PROP_FOURCC, 0x00000021)

# wait for frame
ret = False
# scale down
scale = 3
qrs = set()
reader = zxing.BarCodeReader()

t_start = datetime.now()
out = cv2.VideoWriter('output.avi', 0x00000021, 20.0, (640, 480))

while((datetime.now() - t_start).seconds < 75):
    # Capture frame-by-framestreamon
    ret, frame = telloVideo.read()
    if(ret):
    # Our operations on the frame come here# <- resize for improved performance
        # Display the resulting frame
        cv2.imshow('Tello',frame)
        try:
            frame = cv2.resize(frame, (1280, 720))
            out.write(frame)
            res = reader.decode(Image.fromarray(frame)).parsed
            qrs.add(res)
        except Exception as e:
            print(e)

# When everything done, release the capture
print(qrs)
telloVideo.release()
out.release()
cv2.destroyAllWindows()