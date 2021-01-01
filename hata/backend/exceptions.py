# -*- coding: utf-8 -*-
class PayloadError(Exception):
    """
    Raised when http payload processing fails.
    """
    pass


class InvalidHandshake(Exception):
    """
    Raised when websocket handshake fails.
    """
    pass


class HttpProcessingError(Exception):
    """
    Base class for http content specific errors.
    
    Attributes
    ----------
    code : `int`
        Http error code. Defaults to `0`.
    message : `str`
        Error message. Defaults to empty string.
    headers : `None` or ``imultidict`` of (`str`, `str`) items
        Respective headers.
    """
    def __init__(self, code=0, message='', headers=None):
        self.code = code
        self.headers = headers
        self.message = message
        
        Exception.__init__(self, f'HTTP {self.code}, message={message!r}, headers={self.headers!r}')


class AbortHandshake(HttpProcessingError, InvalidHandshake):
    """
    Raised when websocket handshake is aborted on server side.
    
    Attributes
    ----------
    code : `int`
        Http error code. Defaults to `0`.
    message : `str`
        Error message. Defaults to empty string.
    headers : `None` or ``imultidict`` of (`str`, `str`) items
        Respective headers.
    """


class ProxyError(HttpProcessingError):
    """
    Raised when a proxy request responds with status other than "200 OK".
    
    Attributes
    ----------
    code : `int`
        Http error code. Defaults to `0`.
    message : `str`
        Error message. Defaults to empty string.
    headers : `None` or ``imultidict`` of (`str`, `str`) items
        Respective headers.
    """
    pass


class InvalidOrigin(InvalidHandshake):
    """
    Raised when a websocket handshake received invalid origin header.
    """
    pass


class InvalidUpgrade(InvalidHandshake):
    """
    Raised when a websocket was not correctly upgraded.
    """
    pass


class ContentEncodingError(HttpProcessingError, PayloadError):
    """
    Raised when http content decoding fails.
    
    Attributes
    ----------
    code : `int`
        Http error code. Defaults to `0`.
    message : `str`
        Error message. Defaults to empty string.
    headers : `None` or ``imultidict`` of (`str`, `str`) items
        Respective headers.
    """
    def __init__(self, message='Bad Request', headers=None):
        HttpProcessingError.__init__(self, 400, message, headers)


class ConnectionClosed(Exception):
    """
    Connection closed exception raised when a websocket is closed.
    
    Attributes
    ----------
    code : `int`
        Websocket close code.
    exception : `None` or `BaseException`
        Source exception if applicable.
    reason : `None or `str`
        Websocket close reason if any.
    
    Class Attributes
    ----------------
    _close_reasons : `dict` of (`int`, `str`) items
        Predefined close reasons used if the respective close frame did not include one.
    """
    _close_reasons = {
        1000: 'OK',
        1001: 'going away',
        1002: 'protocol error',
        1003: 'unsupported type',
        1004: '`reserved`',
        1005: 'no status code [internal]',
        1006: 'connection closed abnormally [internal]',
        1007: 'invalid data',
        1008: 'policy violation',
        1009: 'message too big',
        1010: 'extension required',
        1011: 'unexpected error',
        1013: 'Try again later',
        1014: 'Bad gateway',
        1015: 'TLS failure [internal]',
            }

    @classmethod
    def _get_close_reason(cls, code):
        """
        Classmethod to get close for any websocket close code.
        
        Parameters
        ----------
        code : `int`
            Websocket close code.
        
        Returns
        -------
        reason : `str`
        """
        try:
            return cls._close_reasons[code]
        except KeyError:
            pass
        
        if code < 1000:
            return '`unused`'
        if code < 2000:
            return '`reserved`'
        if code < 3000:
            return '`reserved for extensions`'
        if code < 4000:
            return '`registered`'
        if code < 5000:
            return '`private use`'
        
        return '`unknown`'
    
    def __init__(self, code, exception, reason=None):
        """
        Creates a new ``ConnectionClosed`` exception from the given parameters.
        
        Parameters
        ----------
        code : `int`
            The websocket close code.
        exception : `None` or `BaseException`
            Source exception if applicable.
        reason : `None or `str`, Optional
            Websocket close reason if any. Defaults to `None`.
        """
        self.code = code
        self.exception = exception
        self._reason = reason
        Exception.__init__(self)
    
    @property
    def reason(self):
        """
        Returns the websocket close reason.
        
        Returns
        -------
        reason : `str`
        """
        reason = self._reason
        if (reason is None):
            reason = self._get_close_reason(self.code)
        
        return reason
    
    def __repr__(self):
        """Returns the exception's representation."""
        return f'<{self.__class__.__name__}, code={self.code!r}, reason={self.reason!r}, exception={self.exception!r}>'
    
    __str__ = __repr__


class WebSocketProtocolError(Exception):
    """
    Exception raised by websocket when receiving invalid payload.
    """
    pass
