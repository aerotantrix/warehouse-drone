'''
all imports go here, group according to module
'''

# general
import sys      # used to import folders containing classfiles
sys.path.insert(0, 'flight/')
sys.path.insert(0, 'network/')
sys.path.insert(0, 'tools/')
from multiprocessing import Process

# camera
from tools.QrReader import QrReader
import cv2



'''
All function defnintions, group according to module
'''

# camera
def camera_runner(camera_output, cap):
    ''' To be placed in a thread with camera_output list as arg
        will always be running and writes non empty results into the list
        REMEMBER TO CLEAR THE LIST
    '''
    camera = QrReader()     # creates QrReader object
    cap = cv2.VideoCapture(0)   # calls VideoCapture and stores image in cap
    while True:
        success, img = cap.read()   # cap gets converted to numpy array
        if success:     # calls this only if image is retrieved
            result = camera.classify(img)   # calls classify passing the array as arg
            if result is not None:
                camera_output.append(result)    # writes to the camera_output list to be processed later




def main():
    print("still empty")
    '''
    Processes for each feature have to be created and called here
    '''


if __name__ =="__main__":
    main()
