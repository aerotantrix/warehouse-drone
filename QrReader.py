''' 
    
    QrReader captures ONE SINGLE frame, looks for a QR code
    
    Needs to be put in a loop in the main function

    Methods:
    classify() returns (type,value) tuple of QR
    get_type() | PRIVATE FUNCTION | returns the type of the QR ex: location, row/rack, item

    NOTE: type refers to row/rack, item or position 

'''

import cv2
import zxingcpp

class QrReader: 

    def get_type(self, qr_value):       # parses string and returs type
        qr_type = qr_value      # to be decided
        return qr_type


    def classify(self):
        cap = cv2.VideoCapture(0) 

        success, img = cap.read()    # image as array
        if success:
            results = zxingcpp.read_barcodes(img)   # calls the barcode reader fn.

            for result in results:  # might return multiple readings, uses o/p from FIRST one
                return (self.get_type(result.text), result.text)      # returns type, value
                
            if len(results) == 0:       # returs none type if qr not found
                return

        cap.release()   # close object
