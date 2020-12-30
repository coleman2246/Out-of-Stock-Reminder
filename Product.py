from abc import ABC, abstractmethod
import requests

from bs4 import BeautifulSoup

from Utils import UrlUtils,HtmlUtils
    

class ProductPage(ABC):
        
    def __init__(self,url):
        self.url = url

        urlutil = UrlUtils(self.url)
        urlutil.validate_url()
        urlutil.is_acceptable_store()

        self.domain = urlutil.extract_domain()
        self.valid_webpage()

    @abstractmethod
    def in_stock(self):
        pass 

    @abstractmethod
    def get_item_name(self):
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
        self.html = HtmlUtils(url)

        super().__init__(url)

        self.soup = BeautifulSoup(self.html.request.text,"html.parser") 
    
    def in_stock(self):
        cart_button = {}
        for div in self.soup.findAll('div', {'class': 'nav-col'}):
            try:
                cart_button[div.find('span').attrs['class'][0]] = div.text.strip()
            except:
                return True
        return not cart_button["btn"] == "Sold Out"
        
    def get_price(self):
        if self.in_stock():
            price = self.soup.find('li', {'class': "price-current"}).text
            return price
        else:
            return -1

    def get_item_name(self):
        name = self.soup.find('h1', {'class': "product-title"}).text
        return  name
    
    def valid_webpage(self):
       self.html.page_status()

       # todo check to see if item# at the top of the screen is present 


    
        

url = "https://www.newegg.ca/asus-va27ehe-27-full-hd/p/N82E16824281014?Description=montiro&cm_re=montiro-_-24-281-014-_-Product"
test = NeweggProductPage(url)
print(test.get_item_name())