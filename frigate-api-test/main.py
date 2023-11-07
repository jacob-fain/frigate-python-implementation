import PIL
import numpy
import time

from FrigateCam import *

#-----------------------------------------------------------------------------------------------------------------------

def testRead():

    # Initializes camera object
    c1 = FrigateCamera("http://192.168.0.108:5000",
                       "/home/jacob/Ubihere/Frigate/",
                       "cam1")

    # Creates OpenCV window for displaying the frames
    cv2.namedWindow("Display", cv2.WINDOW_AUTOSIZE)

    # Stores the previously processed frame
    prev_frame = None
    while True:

        # Reads the frame and outputs how long it took to read
        start_time = time.time()
        success, frame = c1.read()
        print(time.time() - start_time)

        # Only displays the frame if it is new
        if not numpy.array_equal(frame,prev_frame):

            # using cv2.imshow() to display the image
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow('Display', frame)
            cv2.waitKey(20)
            prev_frame = frame

#-----------------------------------------------------------------------------------------------------------------------

def testCreateVolume():


    c1 = FrigateCamera("http://192.168.0.108:5000",
                       "/home/jacob/Ubihere/Frigate/",
                       "cam1")


    fps = 3
    volume = c1.createVolume(1699300816,20, fps)



    # Displays the volume for testing
    for frame in volume:
        cv2.imshow('Display', frame)
        cv2.waitKey(round(1000 / fps))


#-----------------------------------------------------------------------------------------------------------------------

def testPlayRecording():

    c1 = FrigateCamera("http://192.168.0.108:5000",
                       "/home/jacob/Ubihere/Frigate/",
                       "cam1")

    c1.playRecording(1699300816, 15)

# testRead()
# testPlayRecording()
testCreateVolume()