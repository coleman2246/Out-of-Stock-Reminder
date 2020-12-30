import time
import json
import requests

from urllib.parse import urlparse

import Errors
 


class JsonManager():

    def __init__(self,info_path):
        self.json = None
        self.path = info_path

        with open(self.path,'r') as f:
            self.json = json.load(f)



class UrlUtils:
    def __init__(self, url,json_path= "info.json"):
        self.url = url
        self.parsed_url = urlparse(url)
        self.json_mng = JsonManager(json_path)

    def extract_domain(self):
        return self.parsed_url.netloc


    def validate_url(self):
        if not bool(self.parsed_url.scheme):
            raise Errors.FailedToValidateUrl(self.url)


    def is_acceptable_store(self):
        if not self.extract_domain() in self.json_mng.json["supported_sites"].keys():
            raise Errors.UnnacetablePage(self.extract_domain())



class HtmlUtils:
    def __init__(self,url):
        self.url = url

        urlutil = UrlUtils(self.url)
        urlutil.validate_url()

        self.request = requests.get(url)


    def download_html(self, name="test.html"):

        f = open(name, "w")
        f.write(str(self.request.text))
        f.close()
    
    def page_status(self):
        if self.request.status_code != 200:
            raise Errors.FailedToValidatePage(self.url)