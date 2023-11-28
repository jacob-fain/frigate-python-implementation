
import sqlite3
import time
import numpy
import requests
from PIL import Image
from io import BytesIO
import cv2


class Frigate_Camera:
    """
    An object
    """

# ----------------------------------------------------------------------------------------------------------------------

    def __init__(self, frigate_server: str, frigate_db_path: str, camera_name: str, params:dict = None):

        """
        :param frigate_server: the url of the frigate server. EX: http://10.0.0.165:5000
        :param camera_name: the name of the camera specified in the frigate config
        :param params: camera specifications stored in a dictionary. set my default as {'fps': 10, 'h': 1080}
        """

        self.server = frigate_server
        self.name = camera_name
        self.db_path = frigate_db_path

        if params is None:
            self.params = {'fps': 30, 'h': 700}
        else:
            self.params = params

# ----------------------------------------------------------------------------------------------------------------------

    def read(self) -> tuple:
        """
        Queries the Frigate API and retrieves the camera's most recent frame
        :return: A tuple containing the results. Either (True, NP_Array_Image) or (False, None)
        """

        api_url = f'{self.server}/api/{self.name}/latest.jpg'

        try:
            # API Request
            response = requests.get(api_url)

            if response.status_code == 200:

                # Converts to jpeg
                img_data = BytesIO(response.content)
                img = Image.open(img_data)
                np_img = numpy.array(img)

                return True, np_img

            else:
                return False, None

        except Exception as e:
            print(f'Error: {e}')

#-----------------------------------------------------------------------------------------------------------------------

    def retrieve_recording(self, target_time: float) -> tuple:
        """
        Queries the frigate database with and identifies the path to the recording which contains a specific time.
        :param target_time: The targeted time in UNIX timestamp format. EX: 1698338489
        :return: A tuple containing the results. Either (True, cap) or (False, None). Cap is a CV2 video capture object
        """

        # Connects to the database
        conn = sqlite3.connect(self.db_path + "frigate.db")

        # Query Database
        cur = conn.cursor()
        cur.execute("SELECT * FROM recordings")
        rows = cur.fetchall()

        # print("\nRECORDINGS:")
        # for row in rows:
        #     print(row)

        # Loop through each tuple in the recordings relation
        for row in reversed(rows):
            recording_start_time = row[3]

            # If the clip contains the target_time
            if -9 <= (recording_start_time - target_time) <= 0:

                # Fix recording path
                path_to_recording = self.db_path + row[2].replace('/media/frigate/', '')

                # Creates a CV2 video capture object and returns it
                cap = cv2.VideoCapture(path_to_recording)
                return True, cap

        # If a recording containing the targeted time could not be found
        return False, None

# ----------------------------------------------------------------------------------------------------------------------

    def play_recording(self, target_time: float, duration: float = None):
        """
        Plays a recording from the camera in an OpenCV window
        :param target_time: The targeted time in UNIX timestamp format. EX: 1698338489
        :param duration: The amount of seconds to play
        """

        # Accumulators
        frame_num = 0
        clip_num = 0
        start_time = time.time()


        while True:

            # retrieves the video clip
            success, cap = self.retrieve_recording(target_time)
            if success:

                target_time += 10
                clip_num += 1

                # Loops through each frame of the video
                while True:

                    ret, frame = cap.read()
                    if not ret:
                        break

                    frame_num += 1
                    elapsed_time = round(time.time() - start_time, 1)

                    # Closes program if video duration is reached
                    if duration is not None and elapsed_time >= duration:
                        exit()

                    # Appends text to each frame
                    cv2.putText(frame, f"Clip: {clip_num}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Frame: {frame_num}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    cv2.putText(frame, f"Time: {elapsed_time}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    if elapsed_time != 0.0:
                        cv2.putText(frame, f"FPS: {round(frame_num / elapsed_time)}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1,(100, 0, 255), 2)

                    # Display the frame
                    cv2.imshow(f"{self.name} recording", frame)

                    # Adjusts the framerate / playback speed.
                    cv2.waitKey(30)

                cap.release()

            # Stops when reaching the end of the recordings
            else:
                break

# ----------------------------------------------------------------------------------------------------------------------

    def create_volume(self, target_time: float, duration: float, target_fps: float = None):
        """
        Creates a volume of frames from a camera recording. Allows for custom duration and framerate
        :param target_time: The targeted time in UNIX timestamp format. EX: 1698338489
        :param duration: The amount of seconds of the recording to capture
        :param target_fps: The FPS to convert the volume to. Defaults as the recordings FPS
        :return: A list of frames. The frames are stored as numpy arrays.
        """

        try:
            # Initial call which is used to provide information about the stream
            success, cap = self.retrieve_recording(round(target_time))
            video_fps = round(cap.get(cv2.CAP_PROP_FPS))

            if target_fps > video_fps or target_fps is None:
                target_fps = video_fps

            volume = []
            while True:

                # retrieves the video clip
                success, cap = self.retrieve_recording(target_time)

                if success:
                    target_time += 10

                    index_in = -1
                    index_out = -1

                    while True:

                        success = cap.grab()
                        if not success: break
                        index_in += 1

                        # Skips frames to achieve target FPS
                        out_due = int(index_in / video_fps * target_fps)
                        if out_due > index_out:
                            success, frame = cap.retrieve()
                            if not success: break
                            index_out += 1

                            # Append the frame to the new volume
                            volume.append(frame)

                            # Once the total number of frames is reached, returns the volume
                            if len(volume)>= target_fps * duration:
                                return True, volume

        except:
            return False, None
# ----------------------------------------------------------------------------------------------------------------------



