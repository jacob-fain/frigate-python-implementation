
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

    fps = 25
    cam1 = Frigate_Camera("http://10.0.0.112:5000",
                       "/home/jacob/Ubihere/Frigate/",
                       "cam1")

    camera_list = [cam1]
    camera_volume_list = []

    while True:

        video_image_list = []
        camera_n = -1

        for camera in camera_list:
            camera_n += 1

            if camera_volume_list == [[]]: camera_volume_list = []
            # If camera does not have a volume yet or its volume is empty, creates a new volume
            if len(camera_volume_list) == camera_n or not camera_volume_list[camera_n]:

                # Creates a 30 second long volume for each camera from 60 seconds ago at 1fps
                success = False
                while not success:
                    success, volume = camera.create_volume(time.time() - 60, 10, fps)
                    if success:
                        camera_volume_list.append(volume)

            # Assigns the most recent frame from the camera volume to video image then deletes the frame from the volume
            video_image = camera_volume_list[camera_n][0]
            del camera_volume_list[camera_n][0]

            # Appends the image to video_image_list
            video_image = cv2.resize(video_image, (640, 480))
            #video_image = video_image.transpose((2, 0, 1))
            # self.video_image = np.expand_dims(self.video_image, 0)
            video_image_list.append(video_image)

            # Displays the volume for testing
            frame = video_image_list.pop(0)

            cv2.imshow('Display', frame)
            cv2.waitKey(round(1000 / fps))



#-----------------------------------------------------------------------------------------------------------------------

def testPlayRecording():

    c1 = Frigate_Camera("http://192.168.0.108:5000",
                       "/home/jacob/Ubihere/Frigate/",
                       "cam1")

    c1.play_recording(1701209244, 100)

#testRead()
testPlayRecording()
#testCreateVolume()