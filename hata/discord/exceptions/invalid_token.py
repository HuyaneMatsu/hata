__all__ = ('InvalidToken',)

INVALID_TOKEN_ERROR_MESSAGE = 'Invalid token, please update it, then start the client again.'

class InvalidToken(BaseException):
    def __init__(self):
        BaseException.__init__(self, INVALID_TOKEN_ERROR_MESSAGE)
