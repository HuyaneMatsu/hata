__all__ = ('InvalidToken',)


INVALID_TOKEN_ERROR_MESSAGE = 'Invalid token, please update it, then start the client again.'


class InvalidToken(BaseException):
    __slots__ = ()
    
    def __new__(cls):
        return BaseException.__new__(cls, INVALID_TOKEN_ERROR_MESSAGE)
    
    __init__ = object.__init__
