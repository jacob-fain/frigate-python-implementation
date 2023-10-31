import PIL
import numpy
import time

from FrigateCam import *

c1 = FrigateCamera("http://10.0.0.165:5000", "cam1")
cv2.namedWindow("Display", cv2.WINDOW_AUTOSIZE)

prev_frame = None
while True:
    start_time = time.time()
    success, frame = c1.read()
    print(time.time()-start_time)
    if not numpy.array_equal(frame,prev_frame):

        # using cv2.imshow() to display the image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('Display', frame)

        # Waiting 0ms for user to press any key
        cv2.waitKey(20)

        # Using cv2.destroyAllWindows() to destroy
        # all created windows open on screen
        prev_frame = frame







    #c1.showRecordings()


