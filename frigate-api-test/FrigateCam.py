import datetime
import os
import sqlite3
import time

import numpy
import pytz
import requests
import requests
from PIL import Image
import numpy as np
from io import BytesIO
import cv2
class FrigateCamera:

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
            self.params = {'fps': 1, 'h': 300}
        else:
            self.params = params

# ----------------------------------------------------------------------------------------------------------------------

    def read(self):


        api_url = f'{self.server}/api/{self.name}/latest.jpg'

        try:
            # API Request
            response = requests.get(api_url, params=self.params)

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

    def recording(self, target_time: float):

        # Connects to the database
        conn = sqlite3.connect("/home/jacob/frigate-v3/frigate.db")

        # Query Database
        cur = conn.cursor()
        cur.execute("SELECT * FROM recordings")
        rows = cur.fetchall()


        print("RECORDINGS:")
        for row in rows:
            print(row)


        print("\nTARGET TIME:")
        print(target_time)
        print(datetime.datetime.utcfromtimestamp(target_time))


        for row in rows:

            # If the clip contains the target_time
            if -9 <= (row[3] - target_time) <= 0:

                print("\nPATH TO THE RECORDING WHICH STORES THE TARGET TIME:")
                print(row[2])
                print("\n\n")

                # Fix recording path
                filename = row[2].replace('/media/frigate/', '/home/jacob/frigate-v3/')

                # Open MP4 in VLC
                os.system("cvlc " + filename)
                break


        



