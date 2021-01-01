import sys
import threading
from abc import ABC, abstractmethod
from time import gmtime, strftime, sleep

import numpy as np

import Product
import Errors
import Utils




class Task(ABC):

    def __init__(self,silent =  False):
        self.json = Utils.JsonManager().json
        self.thread_count = self.json["threads"]
        self.urls = self.json["watch_list"]
        self.update_time = self.json["update_time"]
        self.threads = []


    def identify_url(self,url):
        
        domain = Utils.UrlUtils(url).extract_domain()

        product = getattr(Product, self.json["supported_sites"][domain])
        
        return product(url)


    @abstractmethod
    def fire(self,product):
        pass

    def check_produts(self,products):
        
        while True:
            for i in products:    
                instance = self.identify_url(i)
                status = instance.in_stock()
                name = instance.get_item_name()

                message = "[ " +strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ]: "

                message += instance.get_item_name()[:160] + " - "+ bcolors.OKCYAN + Utils.UrlUtils(i).extract_domain() + bcolors.ENDC


                if start:
                    self.fire(instance)


                if status:
                    message += bcolors.OKGREEN + " - In Stock" + bcolors.ENDC
                else:
                    message += bcolors.WARNING +" - Not In Stock" + bcolors.ENDC 

                if not silent:
                    print(message)

            sleep(self.update_time)




    def assign_tasks(self):
        divided_tasks = np.array_split(self.urls,self.thread_count)
        
        for i in range(self.thread_count):
            sleep(4)
            t = threading.Thread(target=self.draw_update, args=(divided_tasks[i],))
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

class TerminalView(Task):
    def __init__(self):
        super().__init__()



    def fire(self,instance):
        

class EmailNotify(Task):
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


t = EmailNotify()
t.send_notifacation()














