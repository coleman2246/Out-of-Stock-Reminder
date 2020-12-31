import sys
import threading
from abc import ABC, abstractmethod
from time import gmtime, strftime, sleep

import numpy as np

import Product
import Errors
import Utils




class Task(ABC):

    def __init__(self):
        self.json = Utils.JsonManager().json
        self.thread_count = self.json["threads"]
        self.urls = self.json["watch_list"]
        self.update_time = self.json["update_time"]

    def identify_url(self,url):
        
        domain = Utils.UrlUtils(url).extract_domain()

        product = getattr(Product, self.json["supported_sites"][domain])
        
        return product(url)

    @abstractmethod
    def notify(self):
        pass

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



class TerminalView(Task):
    def __init__(self):
        super().__init__()

        self.threads = []

    def draw_update(self,products):
        
        while True:
            for i in products:    
                instance = self.identify_url(i)
                status = instance.in_stock()
                name = instance.get_item_name()

                message = "[ " +strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ]: "

                message += instance.get_item_name()[:160] + " - "+ bcolors.OKCYAN + Utils.UrlUtils(i).extract_domain() + bcolors.ENDC



                if status:
                    message += bcolors.OKGREEN + " - In Stock" + bcolors.ENDC
                else:
                    message += bcolors.WARNING +" - Not In Stock" + bcolors.ENDC 

                print(message)
            sleep(self.update_time)

    def notify(self):
        divided_tasks = np.array_split(self.urls,self.thread_count)
        
        for i in range(self.thread_count):
            sleep(4)
            t = threading.Thread(target=self.draw_update, args=(divided_tasks[i],))
            self.threads.append(t)
            t.start()
        
        for i in self.threads:
            i.join()

t = TerminalView()
t.notify()