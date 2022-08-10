class CommonPageLoaderException(Exception):
    pass


class CommonRequestsError(CommonPageLoaderException):
    def __init__(self, url=None, error=None):
        self.url = url
        self.error = error
