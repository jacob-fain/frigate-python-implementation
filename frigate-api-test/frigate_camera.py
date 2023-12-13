
import sqlite3
import time
import numpy
import requests
from PIL import Image
from io import BytesIO
import cv2


class Frigate_Camera:

# ----------------------------------------------------------------------------------------------------------------------

    def __init__(self, frigate_server: str, frigate_db_path: str, camera_name: str, params: dict = None):
        """
        :param frigate_server: the url of the frigate server. EX: http://10.0.0.165:5000
        :param camera_name: the name of the camera specified in the frigate config
        :param frigate_db_path: The path to the frigate folder which contains the frigate.db
        """

        self.server = frigate_server
        self.name = camera_name
        self.db_path = frigate_db_path
        self.db_connection = sqlite3.connect(self.db_path + "frigate.db")

# ----------------------------------------------------------------------------------------------------------------------

    def read(self) -> tuple:
        """
        Queries the Frigate API and retrieves the camera's most recent frame, converting it to a numpy array.

        :return: A tuple containing the results. Either (True, np_array_image) or (False, None).
        """

        api_url = f'{self.server}/api/{self.name}/latest.jpg'

        try:
            response = requests.get(api_url)
            if response.status_code == 200:

                # Converts the frame to a numpy array
                img_data = BytesIO(response.content)
                img = Image.open(img_data)
                np_img = numpy.array(img)

                return True, np_img

            else:
                print(f"API Request Error: {response.status_code}")
                return False, None

        except requests.exceptions.RequestException as e:
            print(f"read encountered an error: {e}")
            return False, None

#-----------------------------------------------------------------------------------------------------------------------

    def retrieve_recording(self, target_time: float, skip_count: int = 0) -> tuple:
        """
        Queries the frigate database with and identifies the path to the recording which contains a specific time.

        :param target_time: The targeted time in UNIX timestamp format. EX: 1698338489
        :param skip_count: The number of recordings to skip after the one containing the target_time.
        :return: A tuple containing the results. Either (True, cap) or (False, None). Cap is a CV2 video capture object
        """

        # TODO MOVE CURSOR TO INSTANCE VARIABLES

        # TODO UPDATE METHOD SO THAT INSTEAD OF RETRIEVING ALL OF THE RECORDINGS JUST RETRIEVES THE CORRECT ONE

        db_cursor = None
        try:

            # Queries the database
            db_cursor = self.db_connection.execute("SELECT * FROM recordings")
            recordings = db_cursor.fetchall()

            row_number = len(recordings) - 1
            while row_number >= 0: # Loop through each tuple starting with the most recent recording

                recording_start_time = recordings[row_number][3]
                if recording_start_time <= target_time: # locates the recording containing the target_time

                    # pens the correct recording as an OpenCV Capture object
                    index_after_skip = row_number + skip_count
                    path_to_recording = self.db_path + recordings[index_after_skip][2].replace('/media/frigate/', '')
                    cap = cv2.VideoCapture(path_to_recording)

                    # clo
                    db_cursor.close()

                    return True, cap, recording_start_time

                row_number -= 1

        except Exception as e:
            print(f"retrieve_volume encountered an error: {e}")
            return False, None, None

        finally:
            if db_cursor is not None:
                db_cursor.close()



# ----------------------------------------------------------------------------------------------------------------------

    def create_volume(self, target_time: float, num_of_recordings: int = 1, target_fps: float = None, skip_count: int = 0):
        """
        Creates a volume of frames from a camera recording. Allows for custom duration and framerate

        :param target_time: The targeted time in UNIX timestamp format. EX: 1698338489
        :param num_of_recordings: The number of recording to use in the volume. 3 recordings would be roughly 30 seconds.
        :param target_fps: The FPS to convert the volume to. Defaults as the recordings FPS
        :param skip_count: The number of recordings to skip
        :return: A list of frames. The frames are stored as numpy arrays.
        """

        # Initialize variables
        volume = []                 # List to store frames
        used_recordings = 0         # Counter for used recordings
        video_fps = None            # Variable to store the FPS of the video
        capture = None              # Video capture object
        volume_start_time = None    # Start time of the generated volume

        try:
            while used_recordings < num_of_recordings:

                # Releases the previous capture if it exists
                if capture is not None:
                    capture.release()

                success, capture, recording_start_time = self.retrieve_recording(target_time, skip_count)

                # Set the start time of the volume if not set
                if volume_start_time is None:
                    volume_start_time = recording_start_time

                # Set FPS variables
                if not video_fps:
                    video_fps = round(capture.get(cv2.CAP_PROP_FPS))
                if target_fps > video_fps or target_fps is None:
                    target_fps = video_fps

                if success:
                    used_recordings += 1
                    skip_count += 1

                    frame_index_in = -1
                    frame_index_out = -1

                    # Process frames to achieve target FPS
                    while True:
                        success = capture.grab()
                        if not success: break
                        frame_index_in += 1
                        out_due = int(frame_index_in / video_fps * target_fps)
                        if out_due > frame_index_out:
                            success, frame = capture.retrieve()
                            if not success: break
                            frame_index_out += 1
                            volume.append(frame)

            return True, volume, used_recordings, volume_start_time


        except Exception as e:
            print(f"create_volume encountered an error: {e}")
            return False, None, None, None

        finally:
            if capture is not None:
                capture.release()




# ----------------------------------------------------------------------------------------------------------------------
