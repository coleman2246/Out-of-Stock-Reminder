import sys
import threading
import os
from abc import ABC, abstractmethod
from time import localtime, strftime, sleep

import numpy as np

import Product
import Errors
import Utils
import Managment


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
    def __init__(self):
        self.json_obj = Utils.JsonManager()
        self.json = self.json_obj.json
        self.thread_count = self.json["threads"]
        self.urls = sorted(self.json["watch_list"])
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
        instances = []

        for i in products:
            instances.append(self.identify_url(i))
        
        while True:
            for instance in instances:    
                if instance.url in self.json_obj.get_json()["notified_lists"]:
                    continue

                status = instance.in_stock()
                if status:
                    self.in_stock_action(instance)
                    
                    self.lock.acquire()

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
    '''
    Outputs the stock updates in the terminal. Inhereits from Notify so it gets the assignments 
    of tasks and checking for free.

    Args:
        silent : bool - if to show terminal output
    '''
    def __init__(self,silent = False):
        self.silent = silent
        super().__init__()


    def no_stock_action(self,instance):

        name = instance.get_item_name()

        message = "[ " +strftime("%Y-%m-%d %H:%M:%S", localtime()) + " ]: "

        message += instance.get_item_name()[:160] + " - "+ bcolors.OKCYAN + instance.domain + bcolors.ENDC
        

        message += bcolors.WARNING + " - No Stock" + bcolors.ENDC
        
        if not self.silent:
            print(message)

    def in_stock_action(self,instance):
       
        name = instance.get_item_name()

        message = "[ " +strftime("%Y-%m-%d %H:%M:%S", localtime()) + " ]: "

        message += instance.get_item_name()[:160] + " - "+ bcolors.OKCYAN + instance.domain + bcolors.ENDC
        

        message += bcolors.OKGREEN + " - In Stock" + bcolors.ENDC
        
        if not self.silent:
            print(message)

class DesktopNotify(TerminalNotify):
    '''
    Sends a system notify when in stock. Inhereits from TerminalNotify so it gets terminal output for free.  
    of tasks and checking for free.

    Args:
        silent : bool - if to show terminal output
    '''


    def __init__(self,silent = False):
        super().__init__(silent)


    def no_stock_action(self,instance):
        super().no_stock_action(instance)

    def in_stock_action(self,instance):
        super().in_stock_action(instance)
        os.system('notify-send "'+self.strip_illegal_chars(instance.get_item_name()) +" - "+ instance.domain+'"' ) 

    def strip_illegal_chars(self,string):
        illegal_chars = ['"',"'",]
        clean = string

        for i in illegal_chars:
            clean = clean.replace(i,"")

        return clean
class EmailNotify(DesktopNotify):
    '''
    Will send a email to a list of emails from a source email

    Args:
        send_email : str - if none will not send email or text, email to send emails from
        receive_emails : [str] -  emails to message
        silent : bool - if to show terminal output
        desktop_notify : bool - if system notify should happen
    '''
    def __init__(self,sender_email, receive_emails, silent = False, desktop_notify = True):
        
        self.sender_email = sender_email
        Utils.EmailUtils(self.sender_email).is_acceptable_email()

        self.json = Utils.JsonManager().json

        self.email_obj = self.id_email()(self.sender_email,receive_emails,"","")

        self.desktop_notify = desktop_notify

        
        super().__init__(silent)
    

    def id_email(self):

        provider_domain = Utils.EmailUtils(self.sender_email).extract_provider()

        email = getattr(Managment, self.json["supported_email_providers"][provider_domain])
        
        return email

    def no_stock_action(self,instance):
        super().no_stock_action(instance)

    def in_stock_action(self,instance):
        if self.desktop_notify:
            super().in_stock_action(instance)

        message = "New item in stock " + instance.get_item_name()+" " + instance.get_price() + "- " + instance.url
        title = instance.domain + " - " + instance.get_item_name()

        self.email_obj.subject = title
        self.email_obj.message = message
        self.email_obj.send_messages()
        







