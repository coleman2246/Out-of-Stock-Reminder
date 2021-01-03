
class Error(Exception):
    """Base class for other exceptions"""
    pass

class FailedToValidateUrl(Error):
    """The url requested is not of valid formating"""
    def __init__(self,url):
        self.message = 'The request URL: "'+url+ '" formating could not be verified'
        super().__init__(self.message)

class FailedToValidatePage(Error):
    """
        The url requested was either denied by the host or is not a valid product page.
        It is expecting to have the code of 200
    """
    def __init__(self,url):
        self.message = 'The request URL: "'+url+ '" did not return the expected code'
        super().__init__(self.message)

class FailedToValidateEmail(Error):
    def __init__(self,email):
        self.message = 'The request Email: "'+email+ '" formating could not be verified'
        super().__init__(self.message)

class UnnacetablEmail(Error):
    """The email that was requested was not found in Utils.is_acceptable_store while parsing the json """
    def __init__(self,email):
        self.message = 'The request Email: "'+email+ '" is not a supported email type. Check info.json for more list of acceptable email providers'
        super().__init__(self.message)



class UnnacetablePage(Error):
    """The url that was requested was not found in Utils.is_acceptable_store while parsing the json """
    def __init__(self,url):
        self.message = 'The request Store: "'+url+ '" is not a supported store. Check info.json for more list of acceptable stores'
        super().__init__(self.message)


class UnableToParse(Error):
    '''
    This is a parent class for errors that are caused by 
    not being able to parse for a expected attribute
    '''

    def __init__(self,url,attribute):
        self.message = 'The request URL: "'+url+ '" was unable to be parsed for '+attribute+ ' \
. This may be beacuse of site changes or you did not request a standard item page (special page)'
        super().__init__(self.message)

class UnableToParseStock(UnableToParse):
    """This class is for errors that are caused beacuse of being unable to parse stock levels"""
    def __init__(self,url):
        self.attribute = "Stock"
        super().__init__(url,self.attribute)


class UnableToParseName(UnableToParse):
    """This class is for errors that are caused beacuse of being unable to prase the product name """
    def __init__(self,url):
        self.attribute = "Name"
        super().__init__(url,self.attribute)


class UnableToParsePrice(UnableToParse):
    """This class is for errors that are caused beacuse of being unable to prase the product price """
    def __init__(self,url):
        self.attribute = "Price"
        super().__init__(url,self.attribute)

class UnableToParsePhone(Error):
    def __init__(self,phone):
        msg = "The following phone number: "+ phone + "could not be parsed. The expected format is 555-555-555."
        super().__init__(msg)

class InvalidReceiveArgument(Error):
    def __init__(self):
        msg = "You've entered an email to send a notifacation with, but have not specified either a phone number or an email"
        super().__init__(msg)


class InvalidArgumentSet(Error):
    def __init__(self):
        msg = "You've entered an argument configuartion that is not supported"
        super().__init__(msg)
