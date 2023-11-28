'''
all imports go here, group according to module
'''

# general
import sys      # used to import folders containing classfiles
sys.path.insert(0, 'flight/')
sys.path.insert(0, 'network/')
sys.path.insert(0, 'tools/')
import threading

# camera
from tools.QrReader import QrReader



'''
All function defnintions, group according to module
'''

# camera
def camera_runner(camera_output):
    ''' To be placed in a thread with camera_output list as arg
        will always be running and writes non empty results into the list
        REMEMBER TO CLEAR THE LIST
    '''
    camera = QrReader()
    while True:
        result = camera.classify()
        if result is not None:
            camera_output.append(result)




def main():
    print("still empty")


if __name__ =="__main__":
    main()
