"""create a function that processes the QRcode image and return the processed string data """

import cv2
import zxingcpp
import time
from djitellopy import Tello

tello=Tello()
tello.connect()

def QRprocess():
    # Set up video stream
    tello.streamon()  
    # Initialize the QRCodeDetector
    #qr_detector = cv2.QRCodeDetector()
    
    
    while True:
        image= tello.get_frame_read().frame

        # Resize frame for better display
        image = cv2.resize(image, (1280,720))

        # Show frame in a window
        cv2.imshow("Tello Video Feed", image)
        
        # Detect and decode QR codes in the frame
        #retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(image)
        #read frame if QRdetected
        results = zxingcpp.read_barcodes(image)      # decodes the frame to get QRinfo
        for result in results:  # needed for multiple readings, prints o/p for all of them
            print("Found barcode:\n Text:    '{}'\n Format:   {}\n Position: {}".format(result.text, result.format, result.position))
            
        # Check for keyboard input to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        '''print(f"while loop time = {(end_time2-start_time2):.3f}ms")  
        print(f"processing time = {(end_time3-start_time3):.3f}ms")  
        print(f"booting time = {(end_time1-start_time1):.3f}ms")  '''
    
    # Close video stream
    tello.streamoff()

    # Disconnect from the drone
    tello.disconnect()
    
if __name__=="__main__":
    QRprocess()
    
   

    

    
