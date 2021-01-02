# Out of Stock
A application to notify the user if the url for an item that they have requested is now in stock.
As of right now the following stores are suported :  
- www.amazon.ca (may have captcha issues)
- www.newegg.ca
- www.bestbuy.ca
- www.canadacomputers.com

## Methods of Notification
The methods of notification are as follows. All methods have terminal output as well by default:
- Email(TODO)
- Terminal
- System Notifacations (Linux only)
- SMS(TODO)

## Requirments
### Dependencies
Most of the dependencies for this project are very commmon and if you use python regularlyly you should 
already have most installed. A ```requierments.txt`` can be found here. They can be installed with ```pip3 install -r requirements.txt``` The depencies are:
- [python 3.9.1](https://www.python.org/downloads/)
- [numpy](https://pypi.org/project/numpy/)
- [requests](https://pypi.org/project/requests/)
- [urlibs](https://pypi.org/project/urllib3/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

### Email
#### Gmail
As of right now the only method of emailing that is suported is Gmail through the official Gmail api. More email services wil be supported in the future. To Use the email and sms notification features please turn on the Gmail api for your account. Steps can be found [here](https://developers.google.com/gmail/api/quickstart/python). Please place the ```credentials.json``` in this project root directory. The gmail dependencies are included included in a seperate ```gmail_requirments.txt``` file found here. They can be installed with ```pip3 install -r gmail_requirments.txt```.

## SMS
Sms is being implemented by piggybacking off of email, so an email is required for sms notifacation.


## How to use
