'''
all imports go here, group according to module
'''

# general
import sys      # used to import folders containing classfiles
sys.path.insert(0, 'flight/')
sys.path.insert(0, 'network/')
sys.path.insert(0, 'tools/')
import threading
import queue

# camera
from tools.QrReader import QrReader
import cv2
 


'''
All function defnintions, group according to module
'''

# camera
def camera_runner(camera_output):
    ''' To be placed in a thread with camera_output list as arg
        will always be running and writes non empty results into the queue
        REMEMBER TO CLEAR THE QUEUE
    '''
    camera = QrReader()     # creates QrReader object
    cap = cv2.VideoCapture(0)   # calls VideoCapture and stores image in cap
    visited_list = []   # logs all visited QRs, avoids unnecessary operations

    while True:
        success, img = cap.read()       # cap gets converted to numpy array
        if success:     # calls this only if image is retrieved
            result = camera.classify(img)       # calls classify passing the array as arg
            if result is not None and result not in visited_list:
                camera_output.put(result)       # writes to the camera_output queue to be processed later
                visited_list.append(result)         # logs data already retrieved




def main():
    '''
    Processes for each feature have to be created and called here
    '''
    camera_output = queue.Queue()
    camera_thread = threading.Thread(target=camera_runner, args=(camera_output,))
    camera_thread.start()
    print(camera_output.get())

if __name__ =="__main__":
    main()
