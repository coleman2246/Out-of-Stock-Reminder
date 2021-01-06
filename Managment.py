from abc import ABC, abstractmethod
import time

import os.path
import base64
from email.mime.text import MIMEText
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import Utils

class EmailManagment(ABC):
    '''

    Args:
        send_email : str - email adress to send from 
        receive_emails : [str] - a list of emails to send to 
        subject : str - subject of the emails
        message : str - message of email
    '''

    def __init__(self,send_email,receive_emails,message,subject):
        self.send_email = send_email
        
        self.receive_emails = receive_emails

        self.message = message
        
        self.subject = subject

        Utils.EmailUtils(send_email).validate_email()
        
        for i in self.receive_emails:
            Utils.EmailUtils(i).validate_email()

    @abstractmethod
    def generate_credentials(self):
        pass

    @abstractmethod
    def create_message(self,message):
        pass


    def send_messages(self):
        pass 


class GmailEmailManagment(EmailManagment):
    '''
    Imports are in this class so if you dont have an gmail email you dont have to install the depencies to use the 
    gmail api.
    '''



    def __init__(self,send_email,receive_emails,message,subject):


        super().__init__(send_email,receive_emails,message,subject)

        self.scopes = ['https://www.googleapis.com/auth/gmail.send'] 
        self.credentials = self.generate_credentials()

    def generate_credentials(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
    
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('gmail', 'v1', credentials=creds)
        return service

    # (sender, to, subject, message_text
    def create_message(self,receiver):

        message = MIMEText(self.message)
        message['to'] = receiver
        message['from'] = self.send_email
        message['subject'] = self.subject

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()   }

    #service, user_id, message
    def send_messages(self):
        for i in self.receive_emails:
            time.sleep(.5)
            self.credentials.users().messages().send(userId="me", body=self.create_message(i)).execute()







