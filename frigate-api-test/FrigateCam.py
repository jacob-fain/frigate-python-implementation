import requests
import requests
from PIL import Image
import numpy as np
from io import BytesIO
import cv2
class FrigateCam:

# ----------------------------------------------------------------------------------------------------------------------

    def __init__(self, frigate_server: str, camera_name: str, params:dict = None):

        """
        :param frigate_server: the url of the frigate server. EX: http://10.0.0.165:5000
        :param camera_name: the name of the camera specified in the frigate config
        :param params: camera specifications stored in a dictionary. set my default as {'fps': 10, 'h': 1080}
        """

        self.server = frigate_server
        self.name = camera_name


        if params is None:
            self.params = {'fps': 1, 'h': 1080}
        else:
            self.params = params

# ----------------------------------------------------------------------------------------------------------------------
    def stream(self):

        api_url = f'{self.server}/api/{self.name}'
        try:
            # Send an HTTP GET request to the API endpoint
            response = requests.get(api_url, params=self.params, stream=True)

            # Process the MJPEG stream
            if response.status_code == 200:
                currentC = None
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk != currentC:
                        print(str(chunk))
                        currentC = chunk

            else:
                print(f'Error: {response.status_code} - {response.text}')

        except Exception as e:
            print(f'Error: {e}')

# ----------------------------------------------------------------------------------------------------------------------

    def stream2(self):
        api_url = f'{self.server}/api/{self.name}'
        try:
            # API Request
            response = requests.get(api_url, params=self.params, stream=True)

            # Stores the current frame, so as not to output it repeatedly
            current_frame = b''

            for chunk in response.iter_content(chunk_size=1024):
                current_frame += chunk

                # Checks if the chunk is in fact a frame
                if b'--frame' in current_frame:

                    # Find the start and end markers
                    start_marker = current_frame.find(b'\xff\xd8')
                    end_marker = current_frame.find(b'\xff\xd9')


                    if start_marker != -1 and end_marker != -1:
                        # This is where the frame needs to be decoded


                        # Extract the JPEG frame
                        frame_data = current_frame[start_marker:end_marker + 2]

                        # Decode the JPEG frame
                        frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

                        # Display the frame
                        cv2.imshow('Frame', frame)
                        cv2.waitKey(1)

                    # Reset the current frame for the next frame
                    current_frame = b''

        except Exception as e:
            print(f'Error: {e}')
