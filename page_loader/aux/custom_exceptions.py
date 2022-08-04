class CommonPageLoaderException(Exception):
    pass


class CommonRequestsError(CommonPageLoaderException):
    def __init__(self, code=None, url=None, error=None):
        self.code = code
        self.url = url
        self.error = error

