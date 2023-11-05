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

def testRetrieveRecording():

    cv2.namedWindow("Display", cv2.WINDOW_AUTOSIZE)


    c1 = FrigateCamera("http://192.168.0.108:5000",
                       "/home/jacob/Ubihere/Frigate/",
                       "cam1")

    timestamp = 1699195704
    while True:
        success, path = c1.retrieveRecording(timestamp)
        timestamp += 10

        if success:

            cap = cv2.VideoCapture(path)

            finished = False
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Display the frame in a cv2 window
                cv2.imshow("Display", frame)
                cv2.waitKey(30)
                # Break the loop if the user presses 'q'
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release the video capture and close the cv2 window

            cap.release()



        # Plays the recording in vlc
        # os.system("cvlc " + path)




#-----------------------------------------------------------------------------------------------------------------------

def testStats():
    c1 = FrigateCamera("http://10.0.0.165:5000",
                       "/home/jacob/Ubihere/Frigate/",
                       "cam1")
    c1.stats()



#testRead()
testRetrieveRecording()
#testStats()