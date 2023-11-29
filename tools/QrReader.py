''' 
    
    QrReader captures ONE SINGLE frame, looks for a QR code
    
    Needs to be put in a loop in the main function

    Methods:
    classify() returns (type,value) tuple of QR
        args: cap which is cv.VideoCapture(0)
    get_type() | PRIVATE FUNCTION | returns the type of the QR ex: location, row/rack, item
        args: qr_value string from classify

    NOTE: type refers to row/rack, item or position 

'''

import zxingcpp
from datetime import datetime

class QrReader: 

    def get_type(self, qr_value):       # parses string and returns type
        if qr_value[:1] == "l":
            return "location"
        elif qr_value[:1] == "r":
            return "row"
        elif qr_value[:1] == "c":
            return "column"
        elif qr_value[:1] == "i":
            return "item"


    def classify(self, img):

        results = zxingcpp.read_barcodes(img)   # calls the barcode reader fn.

        for result in results:  # might return multiple readings, uses o/p from FIRST one
            return (self.get_type(result.text), result.text, datetime.now())      # returns type, value
            
        if len(results) == 0:       # returs none type if qr not found
            return

