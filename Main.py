#!/usr/bin/python3
import argparse, os,sys

import Remind
import Utils
import Errors
parser = argparse.ArgumentParser(description='Checks onliine retail stores for stock and notifies the user when in stock. ')

parser.add_argument('-phone', help='the phone number to send to. Expected in the form of 555-555-5555', type=str , required=False)
parser.add_argument('-sender', help='email to send notification from  ', type=str , required=False)
parser.add_argument('-receiver', help='email to send notification to', type=str , required=False)
parser.add_argument('-system_notify', help='should system notifications be shown', required=False,action='store_true')
parser.add_argument('-silent', help='should the terminal be silent', required=False, action='store_true')


args = vars(parser.parse_args())


class Parse:

    def __init__(self,args):
        self.args = args
        self.find_function().assign_tasks()

    def all_none(self,check_args,exclude_keys = []):
        all_none = True
        
        for i in check_args.keys():
            if check_args[i] and i not in  exclude_keys:
                all_none = False
        return all_none

    def find_function(self):
        
        # if user puts not arguments in 
        if self.all_none(self.args):
            print("first checked")
            return Remind.TerminalNotify()

        # if user uses -system_notify and optional -silent
        if self.args["system_notify"] and self.all_none(self.args, ["system_notify","silent"] ):
            return Remind.DesktopNotify(self.args["silent"])


        if self.args["sender"]:
            emails = []

            if args["phone"]:
                emails.append(Utils.PhoneUtils(args['phone']).phone+"@txt.bell.ca")

            if args["receiver"]:
                emails.append(args["receiver"])

            if len(emails) == 0:
                raise Errors.InvalidReceiveArgument
            #    def __init__(self,sender_email, receive_emails, silent = False, desktop_notify = True):

            return Remind.EmailNotify(self.args["sender"],emails,silent=args["silent"],desktop_notify=args["system_notify"])
        print("Run python Main.py -h")
        raise Errors.InvalidArgumentSet

Parse(args)
