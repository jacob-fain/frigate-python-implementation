import PIL
import numpy
import time

from FrigateCam import *

def testRead():

    # Initializes camera object
    c1 = FrigateCamera("http://10.0.0.165:5000", "/home/jacob/frigate-v3/frigate.db", "cam1")

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


def testRetrieveRecording():


    c1 = FrigateCamera("http://10.0.0.165:5000", "/home/jacob/frigate-v3/frigate.db", "cam1")

    success, path = c1.retrieveRecording(1698338489)

    if success:
        # Plays the recording in vlc
        os.system("cvlc " + path)


def testStats():
    c1 = FrigateCamera("http://10.0.0.165:5000", "/home/jacob/frigate-v3/frigate.db", "cam1")
    c1.stats()



#testRead()
#testRetrieveRecording()
testStats()