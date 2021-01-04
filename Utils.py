import time
import json as js
import re

from urllib.parse import urlparse
import requests

import Errors
 


class JsonManager():

    def __init__(self,info_path = "info.json"):
        
        self.path = info_path
        self.json = self.get_json()

    def get_json(self):    
        with open(self.path,'r') as f:
            temp = js.load(f)
        self.json = temp
        return temp


    def write_json(self):
        with open(self.path, 'w') as f:
            js.dump(self.json, f,indent=4)

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



class HtmlUtilsRequest:
    def __init__(self,url):
        self.url = url

        urlutil = UrlUtils(self.url)
        urlutil.validate_url()

    
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}    
        
        try:
            self.request = requests.get(url,headers=header)
        except:
            print("Failed to get : "+self.url)

    def download_html(self, name="test.html"):

        f = open(name, "w")
        f.write(str(self.request.text))
        f.close()
    
    def page_status(self):
        if self.request.status_code != 200:
            raise Errors.FailedToValidatePage(self.url)

class EmailUtils:
    def __init__(self,email):
        self.email = email
        self.json = JsonManager().json
    
    def extract_provider(self):
        return self.email.split("@")[-1]

    def is_acceptable_email(self):
        if not self.extract_provider() in self.json["supported_email_providers"].keys():
            raise Errors.UnnacetablEmail(self.extract_provider())

    def validate_email(self):
        regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
        if not re.search(regex,self.email):
            raise Errors.FailedToValidateEmail(self.email)

class PhoneUtils:
    def __init__(self,phone):
        self.phone = phone
        
        self.parse_number()

    def parse_number(self):
    
        copy = self.phone
        self.phone = self.phone.replace("-","")
        regex = "^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"

        if not re.search(regex,self.phone):
            raise Errors.UnableToParsePhone(copy)