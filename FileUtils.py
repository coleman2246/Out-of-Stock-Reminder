import time
import json

class FileReader():

    def __init__(self,info_path):
        self.json = None
        self.path = info_path

        with open(self.path,'r') as f:
            self.json = json.load(f)

