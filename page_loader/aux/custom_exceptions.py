class CommonPageLoaderException(Exception):
    pass


class CommonRequestsError(CommonPageLoaderException):
    def __init__(self, s_code=None, url=None, error=None):
        self.code = s_code
        self.url = url
        self.error = error
