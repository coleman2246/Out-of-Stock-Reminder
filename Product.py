from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


from Utils import UrlUtils,HtmlUtilsRequest
import Errors

class ProductPage(ABC):
    '''
    A parent class that all product pages will extend that takes care of 
    things that all websites will have in common. It will validate
    the url to make sure it is a valid url, make that the url passed
    is a supported page, and make sure that the webpage doesnt
    return any unexpecte codes.

    Getting the HTML is left up to the children class because some
    websites may need javascript to get the full html and something
    like selenium will be needed.

    Args:
        url : str - url of webpage to check
    '''        
    
    def __init__(self,url,selenium = False):
        self.url = url

        urlutil = UrlUtils(self.url)
        urlutil.validate_url()
        urlutil.is_acceptable_store()

        self.domain = urlutil.extract_domain()
        if not selenium:
            self.valid_webpage()

    @abstractmethod
    def in_stock(self):
        self.update_page()
        '''
        All children of this function will be implemented to follow this pattern:
        check if out of stock indicator exists. If out of stock indicator 
        exists return False, if it doesnt check if in stock button exists. If it
        does exists than return True, otherwise UnableToParseStock
        '''
        pass 

    @abstractmethod
    def get_item_name(self):
        pass 

    @abstractmethod
    def valid_webpage(self):
        pass 

    @abstractmethod
    def get_price(self):
        self.update_page() 
        '''
        All children of this function will be implemented to follow this pattern:
        check if price exists. If price exists return its name, otherwise 
        it raises UnableToParseName
        '''
        pass

    @abstractmethod
    def update_page(self):
        '''
        Updates the page html from the internet.
        '''

        pass

class StandardProductPage(ProductPage,ABC):
    '''
        A slightly less generic product page abstract class that is meant for pages
        that dont require javascript and can be parsed following with a simple 
        soup.find(). all args with _args in the name will be used in soup.find methods.
        They are all optional because some children may want to implement
        a specific function.
        Args:
            in_stock_args: [str,{str : str}] - finding the in stock parameter in the method in_stock()
            out_stock_args: [str,{str : str}] - finding the out stock parameter in the method in_stock()
            price_args: [[str,{str : str}]] - finding the in price parameter in the method get_price(),must be 2d because some pages have sale prices as well
            name_args: [str,{str : str}] -  finding the in name parameter in the get_item_name() method
    '''

    def __init__(self, url, out_of_stock_args = None, in_stock_args = None, price_args = None, name_args = None,selenium = False):
        if not selenium:
            self.html = HtmlUtilsRequest(url)
            self.soup = BeautifulSoup(self.html.request.text,"html.parser")


        super().__init__(url,selenium)


        self.out_of_stock_args = out_of_stock_args
        self.in_stock_args = in_stock_args

        self.price_args = price_args

        self.name_args = name_args       

    def update_page(self):
        self.html = HtmlUtilsRequest(self.url)
        self.soup = BeautifulSoup(self.html.request.text,"html.parser")
        

    def in_stock(self):
        super().in_stock()
        no_stock = self.soup.find(self.out_of_stock_args[0],self.out_of_stock_args[1])

        if no_stock:
            return False
        else:
            
            #looking for in stock button
            stock = self.soup.find(self.in_stock_args[0],self.in_stock_args[1])
            if stock:
                return True
            else:
                raise Errors.UnableToParseStock(self.url)
        
    def get_price(self):
        super().get_price()
        if self.in_stock():
            for i in self.price_args:
                price = self.soup.find(i[0], i[1])
                if price:
                    return price.text.strip()
            
            raise Errors.UnableToParsePrice(self.url)
        else:
            return -1

    def get_item_name(self):
        name = self.soup.find(self.name_args[0], self.name_args[1])
        if name:
            return name.text.strip()
        else:
            raise Errors.UnableToParseName(self.url)
        
    
    def valid_webpage(self):
       self.html.page_status()

class SeleniumProductPage(StandardProductPage,ABC):

    def __init__(self, url, out_of_stock_args = None, in_stock_args = None, price_args = None, name_args = None):
  
        
        super().__init__(url, out_of_stock_args , in_stock_args, price_args, name_args,selenium=True)


        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=options)
        self.update_page()


    def update_page(self):
        self.driver.refresh()
        self.driver.get(self.url)

        self.soup = BeautifulSoup(self.driver.page_source,"html.parser")
        




class NeweggProductPageCA(StandardProductPage):
    """
    Will make sure that a valid page has been requested. It will check to make sure that the page given is
    expected (a product page) by looking for varous properites that are specific 
    to www.newegg.ca product pages. All functions are inherited from StandarProductPage because newegg
    requires no special functions. All validation is handled by the parent

    Args: 
        url: str - url of website to check
    """
    def __init__(self,url):
        out_stock_args = ['span',{'class' : 'btn btn-message btn-wide'}]
        in_stock_args = ['button',{'class' : 'btn btn-primary btn-wide'}]
        price_args = [['li', {'class': "price-current"}]]
        name_args = ['h1', {'class': "product-title"}]

        super().__init__(url,out_stock_args,in_stock_args,price_args,name_args)

class BhphotovideoProductPage(StandardProductPage):

    def __init__(self,url):
        out_stock_args = ['button',{'class' : 'notifyBtn_2u4cU097e899btC11lCxuW buttonTheme_1mBX7Kocn_Oq_wzW6ri7s5 tertiary_3fLAKfyXQQMUL4ZSxgfZGx'}]
        in_stock_args = ['button',{'class' : 'toCartBtn_2C85cCSy-imVSRqkpuNDT2 buttonTheme_1mBX7Kocn_Oq_wzW6ri7s5'}]
        price_args = [['div', {'class': "price_1DPoToKrLP8uWvruGqgtaY"}]]
        name_args = ['h1', {'class': "title1_17KKS47kFEQb7ynVBsRb_5 reset_gKJdXkYBaMDV-W3ignvsP primary_ELb2ysditdCtk24iMBTUs"}]
        
        super().__init__(url,out_stock_args,in_stock_args,price_args,name_args)

class VuugoProductPageCA(StandardProductPage):
    def __init__(self,url):
        out_stock_args = ['span',{'class' : 'red'}]
        in_stock_args = ['span',{'class' : 'green'}]
        price_args = [['span', {'class': "price-new"}],["span",{"class": "text-price"}]]
        
        super().__init__(url,out_stock_args,in_stock_args,price_args)

    def get_item_name(self):
        name = self.soup.find(self.name_args[0], self.name_args[1])
        if name:
            return name.text.strip()
        else:
            raise Errors.UnableToParseName(self.url)
                

    def get_item_name(self):
        div =  self.soup.find("div",{"class":"extra-wrap"})
        h1 = div.find("h1")
        
        
        return h1.text.strip()
    

        
class AmazonProductPageCA(SeleniumProductPage):
    def __init__(self,url):
        in_stock_args = ['span', {"class" : "a-size-medium a-color-success"}] 
        out_stock_args = ["a", {"id" : "buybox-see-all-buying-choices-announce", "class": "a-button-text"}]
        price_args = [["span", {'id': "price_inside_buybox" , "class" : "a-size-medium a-color-price"}]]
        name_args = ['span', {'class': "a-size-large product-title-word-break" , 'id': 'productTitle' }]

        super().__init__(url,out_stock_args,in_stock_args,price_args,name_args)

        


class BestBuyProductPageCA(StandardProductPage):
    def __init__(self,url):
        name_args = ['h1', {'class': "productName_19xJx"}]

        super().__init__(url,name_args=name_args)

       
    def in_stock(self):
        super.update_page()

        #looking for out of stock indicator
        out_stock = self.soup.find('span', {"class" : "availabilityMessage_1MO75 container_3LC03"})
        if out_stock and out_stock.text.strip() == "Coming soon":
            return False
        else:
            
            #looking for in stock indicator
            stock = self.soup.find("button", {"class" : "button_2Xgu4 primary_oeAKs addToCartButton_1DQ8z addToCartButton regular_cDhX6", "type": "submit" })
            if stock and out_stock and out_stock.text.strip() == "Available to ship":
                return True
            else:
                raise Errors.UnableToParseStock(self.url)
        
    def get_price(self):
        if self.in_stock():
            price = self.soup.find("span", {"class" : "screenReaderOnly_3anTj large_3aP7Z"}).text.strip()
            return price
        else:
            return -1

class CanadaComputersProductPage(StandardProductPage):
    def __init__(self,url):
        name_args = ['h1', {'class': "h3 mb-0"}]
        super().__init__(url,name_args=name_args)

 
    def in_stock(self):
        super().update_page()

        root = self.soup.find('div', {'class': 'pi-prod-availability'})
        span = root.findAll("span")

        for i in span:
            bad_indiactors =  i.find("i",{"class" : "fas fa-ban red text-danger"} )
            good_indiactors =  i.find("i",{"class" : "fas fa-check green text-success"} )
            
            if bad_indiactors and "ONLINE" in i.text.upper() and "NOT" in i.text.upper():
                return False

            if good_indiactors and "ONLINE" in i.text.upper():
                return True
        raise Errors.UnableToParseStock(self.url)

    def get_price(self):
        if self.in_stock():
            
            price = self.soup.find('span', {'class': 'h2-big'}).text.strip()
        
            if price:
                return price
            else:
                raise Errors.UnableToParsePrice(self.url)
        else:
            return -1

