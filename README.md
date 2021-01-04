# Out of Stock
An application to notify the user if the url for an item that they have requested is now in stock.
As of right now the following stores are suported:  
- www.amazon.ca (slowest store due to selenium requirment)
- www.newegg.ca
- www.bestbuy.ca
- www.canadacomputers.com  
- www.bhphotovideo.com (some items will get rate limited and you will receive error 429)
- 

The functions may work on other non-canadian versions of these webistes, but if you wish to test them put the corresponding website and its
function in the ``supported_sites`` list in that ``info.json``. 

## Methods of Notification
The methods of notification are as follows. All methods have terminal output by default:
- Email
- Terminal
- System Notifacations (Linux only)
- SMS

## Requirments
### Dependencies
Most of the dependencies for this project are common python libraries . A `requierments.txt` can be found [here](https://raw.githubusercontent.com/coleman2246/Out-of-Stock-Reminder/master/Dependencies/requirements.txt). They can be installed with `pip3 install -r requirements.txt` The dependencies are:
- [python 3.9.1](https://www.python.org/downloads/)
- [numpy](https://pypi.org/project/numpy/)
- [requests](https://pypi.org/project/requests/)
- [urlibs](https://pypi.org/project/urllib3/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [selenium](https://pypi.org/project/selenium/)
#### Selenium
Due to Amazon not playing nicely, you are going to be required to setup the
selenium geckodriver which can be found [here](https://github.com/mozilla/geckodriver/releases).


### Email
#### Gmail
As of right now the only method of emailing that is suported is Gmail through the official Gmail api. More email services wil be supported in the future. To use the email and SMS notification features please turn on the Gmail api for your account. Steps can be found [here](https://developers.google.com/gmail/api/quickstart/python). Please place the ```credentials.json``` in this project root directory. The gmail dependencies are included included in a seperate ```gmail_requirments.txt``` file 
found [here](https://raw.githubusercontent.com/coleman2246/Out-of-Stock-Reminder/master/Dependencies/gmail_requirments.txt). They can be installed with ```pip3 install -r gmail_requirments.txt```.

## SMS
SMS is being implemented by piggybacking off of email, so an email is required for SMS notification.


## How to use
Put the product urls you wish to be notified for in  ``watch_list`` in ``info.json``. When an item has been confirmed to be in stock you will be notified 
and the product url will be placed in the ``notified_lists`` in the ``info.json`` file. You will not be notified about this url again until you remove it from the ``notified_list``. Options like the thread count and update time can also be configured in this json file.


### Usage
```
Main.py [-h] [-phone PHONE] [-sender SENDER] [-receiver RECEIVER] [-system_notify] [-silent]
Checks onliine retail stores for stock and notifies the user when in stock.

optional arguments:
- h, --help          show this help message and exit
- phone PHONE        the phone number to send to. Expected in the form of 555-555-5555
- sender SENDER      email to send notification from
- receiver RECEIVER  email to send notification to
- system_notify      should system notifications be shown.
- silent             should the terminal be silent
```

By default the notification method is just by terminal. Which is equivalent to:
```
python3 Main.py
```
### Example Usage
```bash
python3 Main.py -phone 555-555-555 -receiver email@gmail.com -sender email12@gmail.com
```
This command will send SMS notifications to the phone number ``555-555-555`` and email notifications to ``email@gmail.com`` from the email ``email12@gmail.com``. This
command will also have terminal output
## Future
- In the future using selenium, a auto-buy option maybe be implemented
- Better/more consistent documentation