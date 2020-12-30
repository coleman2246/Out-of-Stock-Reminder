
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

class UnnacetablePage(Error):
    """The url that was requested was not found in Utils.is_acceptable_store while parsing the json """
    def __init__(self,url):
        self.message = 'The request Store: "'+url+ '" is not a supported store. Check info.json for more list of acceptable stores'
        super().__init__(self.message)