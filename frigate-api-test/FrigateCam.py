import datetime
import json
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

    def retrieveRecording(self, target_time: float) -> tuple:
        """
        Queries the frigate database with and identifies the path to the recording which contains a specific time.
        :param target_time: The targeted time in UNIX timestamp format. EX: 169frigate.db8338489
        :return: A tuple containing the results. Either (True, path_to_recording) or (False, None)
        """

        # Connects to the database
        conn = sqlite3.connect(self.db_path + "frigate.db")

        # Query Database
        cur = conn.cursor()
        cur.execute("SELECT * FROM recordings")
        rows = cur.fetchall()


        print("\nRECORDINGS:")
        for row in rows:
            print(row)

        print("\nTARGET TIME:")
        print(target_time)
        print(datetime.datetime.utcfromtimestamp(target_time))


        for row in rows:

            recording_start_time = row[3]

            # If the clip contains the target_time
            if -9 <= (recording_start_time - target_time) <= 0:

                print("\nPATH TO THE RECORDING WHICH STORES THE TARGET TIME:")
                print(row[2])
                print("\n\n")

                # Fix recording path
                path_to_recording = self.db_path + row[2].replace('/media/frigate/', '')

                # Returns path
                return True, path_to_recording

        # If a recording containing the targeted time could not be found
        return False, None

# ----------------------------------------------------------------------------------------------------------------------

    def retrieveRecordingContinued(self, target_time: float) -> tuple:
        """
        Queries the frigate database with and identifies the path to the recording which contains a specific time.
        :param target_time: The targeted time in UNIX timestamp format. EX: 1698338489
        :return: A tuple containing the results. Either (True, path_to_recording) or (False, None)
        """

        # Connects to the database
        conn = sqlite3.connect(self.db_path)

        # Query Database
        cur = conn.cursor()
        cur.execute("SELECT * FROM recordings")
        rows = cur.fetchall()


        print("\nRECORDINGS:")
        for row in rows:
            print(row)

        print("\nTARGET TIME:")
        print(target_time)
        print(datetime.datetime.utcfromtimestamp(target_time))


        for row in rows:

            recording_start_time = row[3]

            # If the clip contains the target_time
            if -9 <= (recording_start_time - target_time) <= 0:

                print("\nPATH TO THE RECORDING WHICH STORES THE TARGET TIME:")
                print(row[2])
                print("\n\n")

                # Fix recording path
                path_to_recording = row[2].replace('/media/frigate/', '/home/jacob/frigate-v3/')

                # Returns path
                return True, path_to_recording

        # If a recording containing the targeted time could not be found
        return False, None

# ----------------------------------------------------------------------------------------------------------------------

    def stats(self):
        """
        Retrieves stats regarding Frigate and it's cameras
        :return: A JSON containing the stats
        """


        api_url = f'{self.server}/api/stats'

        try:

            # API Request
            response = requests.get(api_url, params=self.params)

            if response.status_code == 200:
                return response.content

        except Exception as e:
            print(f'Error: {e}')

# ----------------------------------------------------------------------------------------------------------------------



