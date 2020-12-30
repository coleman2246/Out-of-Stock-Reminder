from abc import ABC, abstractmethod
import requests

from urllib.parse import urlparse

from bs4 import BeautifulSoup

class UrlUtils:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        

    def extract_domain(self):
        return self.parsed_url.netloc


    def validate_url(self):
        return bool(self.parsed_url.scheme)

class ProductPage(ABC):
        
    def __init__(self,url):
        self.url = url

        urlutil = UrlUtils(self.url)
        urlutil.validate_url()

        self.domain = urlutil.extract_domain()
        self.valid_webpage()

    @abstractmethod
    def in_stock(self):
        pass 

    @abstractmethod
    def item_name(self):
        pass 

    @abstractmethod
    def item_name(self):
        pass 

    @abstractmethod
    def valid_webpage(self):
        pass 

    @abstractmethod
    def get_price(self):
        pass

class NeweggProductPage(ProductPage):
    """
    Will make sure that a valid page has been requested. It must be of the domain newegg.* and it must be a valid page
    on newegg.
    """

    def __init__(self,url):
        super().__init__(url)
        self.html = requests.get(self.url)
        self.soup = BeautifulSoup(self.html) 
    
    def in_stock(self):
        r = 

    def item_name(self):
        pass    
    
    def valid_webpage(self):
        pass

url = "https://www.newegg.ca/western-digital-blue-sn550-nvme-1tb/p/N82E16820250135?Item=N82E16820250135&cm_sp=Homepage_dailydeals-_-P0_20-250-135-_-12292020"
test = NeweggProductPage(url)
