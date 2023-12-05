
from frigate_camera import *


#-----------------------------------------------------------------------------------------------------------------------

def testRead():

    # Initializes camera object
    c1 = Frigate_Camera("http://10.0.0.112:5000",
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
        #print(F"{round(time.time() - start_time, 4)} seconds")

        # Only displays the frame if it is new
        if not numpy.array_equal(frame,prev_frame):

            # using cv2.imshow() to display the image
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow('Display', frame)
            cv2.waitKey(20)
            prev_frame = frame

#-----------------------------------------------------------------------------------------------------------------------

def testCreateVolume(timestamp, duration, fps):



    camera = Frigate_Camera("http://10.0.0.112:5000",
                       "/home/jacob/Ubihere/Frigate/",
                       "cam1")

    success = None
    volume = []

    while not success:
        success, volume = camera.create_volume(timestamp, duration, fps)

    for frame in volume:

        cv2.imshow('Display', frame)
        cv2.waitKey(round(1000 / fps))


#-----------------------------------------------------------------------------------------------------------------------

def testPlayRecording(timestamp):

    c1 = Frigate_Camera("http://10.0.0.112:5000",
                       "/home/jacob/Ubihere/Frigate/",
                       "cam1")

    c1.play_recording(timestamp)

#-----------------------------------------------------------------------------------------------------------------------


#testRead()

#testPlayRecording(1701366426)

testCreateVolume(1701366428, 20, 1)