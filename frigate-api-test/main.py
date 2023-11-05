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
    frameNum = 0
    clipNum = 0
    start_time = time.time()

    while True:

        # retrieves the video clip
        success, path = c1.retrieveRecording(timestamp)
        if success:

            timestamp += 10
            clipNum += 1

            cap = cv2.VideoCapture(path)

            # Loops through each frame of the video
            while True:

                ret, frame = cap.read()
                if not ret:
                    break

                # Update Text
                frameNum += 1
                elapsed_time = round(time.time() - start_time, 1)
                cv2.putText(frame, f"Clip: {clipNum}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Frame: {frameNum}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                cv2.putText(frame, f"Time: {elapsed_time}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                try:
                    cv2.putText(frame, f"FPS: {round(frameNum / elapsed_time)}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 0, 255), 2)
                except: pass


                # Display the frame
                cv2.imshow("Display", frame)

                # Adjusts the framerate / playback speed.
                cv2.waitKey(30)

            cap.release()
        # Stops when reaching the end of the recordings
        else:
            break

#-----------------------------------------------------------------------------------------------------------------------

def testStats():
    c1 = FrigateCamera("http://10.0.0.165:5000",
                       "/home/jacob/Ubihere/Frigate/",
                       "cam1")
    c1.stats()



#testRead()
testRetrieveRecording()
#testStats()