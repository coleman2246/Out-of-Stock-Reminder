import sys
import threading
import os
from abc import ABC, abstractmethod
from time import gmtime, strftime, sleep

import numpy as np

import Product
import Errors
import Utils



class Notify(ABC):

    '''
    This is the class that will check if all the products on the list are in stock. Parameters
    such as thread_count,watchi_list, and update_time are all from the info.json file.

    The check_updates() will call in_stock_action if the item is said to be in stock and 
    no_stock_action() if the item is said not to be in stock. Both of these action functions
    are requierd to be implemented by their children.

    when the item is in stockall other threads are to be locked so that the 
    info.json objet can be updated so no duplicates of the notifacations are sent

    '''



    def __init__(self,silent =  False):
        self.json_obj = Utils.JsonManager()
        self.json = self.json_obj.json
        self.thread_count = self.json["threads"]
        self.urls = self.json["watch_list"]
        self.update_time = self.json["update_time"]
        self.threads = []
        self.lock = threading.Lock()

    def identify_url(self,url):
        
        domain = Utils.UrlUtils(url).extract_domain()

        product = getattr(Product, self.json["supported_sites"][domain])
        
        return product(url)


    @abstractmethod
    def in_stock_action(self,product):
        pass

    @abstractmethod
    def no_stock_action(self,product):
        pass

    def check_products(self,products):
        
        while True:
            for i in products:    
                instance = self.identify_url(i)
                status = instance.in_stock()

                if status and instance.url not in self.json_obj.get_json()["notified_lists"]:
                    self.lock.acquire()
                    self.in_stock_action(instance)
                    
                    self.json_obj.get_json()
                    self.json_obj.json["notified_lists"].append(instance.url)
                    self.json_obj.write_json()
                    
                    self.lock.release()
                elif not status:
                    self.no_stock_action(instance)

            sleep(self.update_time)

    def assign_tasks(self):
        divided_tasks = np.array_split(self.urls,self.thread_count)
        
        for i in range(self.thread_count):
        
            t = threading.Thread(target=self.check_products, args=(divided_tasks[i],))
            self.threads.append(t)
            t.start()
        
        for i in self.threads:
            i.join()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TerminalNotify(Notify):
    def __init__(self,silent = False):
        self.silent = silent
        super().__init__()


    def no_stock_action(self,instance):

        name = instance.get_item_name()

        message = "[ " +strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ]: "

        message += instance.get_item_name()[:160] + " - "+ bcolors.OKCYAN + instance.domain + bcolors.ENDC
        

        message += bcolors.WARNING + " - No Stock" + bcolors.ENDC
        
        if not self.silent:
            print(message)

    def in_stock_action(self,instance):
       
        name = instance.get_item_name()

        message = "[ " +strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ]: "

        message += instance.get_item_name()[:160] + " - "+ bcolors.OKCYAN + instance.domain + bcolors.ENDC
        

        message += bcolors.OKGREEN + " - In Stock" + bcolors.ENDC
        
        if not self.silent:
            print(message)

class DesktopNotify(TerminalNotify):
    def __init__(self,silent = False):
        super().__init__(silent)


    def no_stock_action(self,instance):
        super().no_stock_action(instance)

    def in_stock_action(self,instance):
        super().in_stock_action(instance)
        os.system('notify-send "'+instance.get_item_name() +" - "+ instance.domain+'"' ) 

class EmailNotify(Notify):
    def __init__(self):
        super().__init__()
    

    def send_notifacation(self):
        import smtplib, ssl

        port = 465  # For SSL
        send_email = ""
        receive_email = send_email
        password = input("Type your password and press enter: ")

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(send_email, password)
            server.sendmail(send_email, receive_email, "test123")
            # TODO: Send email here


    def notify(self):
        pass


t = DesktopNotify()
t.assign_tasks()














