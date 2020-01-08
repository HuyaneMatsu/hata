# -*- coding: utf-8 -*-
from ssl import SSLError,CertificateError
from .futures import CancelledError

class PayloadError(Exception):
    pass

class HttpProcessingError(Exception):
    #pass Shortcut for raising HTTP errors with custom code, message and headers.
    
    def __init__(self,code=0,message='',headers=None):
        self.code   = code
        self.headers= headers
        self.message= message

        Exception.__init__(self,f'{self.code}, message=\'{message}\'')


class RequestError(HttpProcessingError):
    #Connection error during sending request."""
    pass

class ResponseError(HttpProcessingError):
    #Connection error during reading response."""
    pass

class InvalidHandshake(Exception):
    pass

class AbortHandshake(InvalidHandshake):
    def __init__(self,status,headers,body):
        self.status=status
        self.headers=headers
        self.body=body
        
        InvalidHandshake.__init__(self,f'HTTP {status}, {len(headers)} headers, {len(body)} bytes')
    
class ProxyError(HttpProcessingError):
    #if proxy responds with status other than "200 OK"
    pass

class InvalidOrigin(InvalidHandshake):
    pass

class InvalidUpgrade(InvalidHandshake):
    pass

class ContentEncodingError(HttpProcessingError):
    def __init__(self,message='Bad Request',headers=None):
        HttpProcessingError.__init__(self,400,message,headers)

class ConnectionClosed(Exception):
    _close_reasons= {
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
    def _get_close_reason(cls,code):
        if code<1000:
            return '`unused`'
        if code<2000:
            try:
                return cls._close_reasons[code]
            except KeyError:
                return '`reserved`'
        if code<3000:
            return '`reserved for extensions`'
        if code<4000:
            return '`registered`'
        if code<500:
            return '`private use`'

        return '`unknown`'

    def __init__(self,code,exception,reason=''):
        self.code=code
        self.exception=exception
        self._reason=reason
        Exception.__init__(self)

    @property
    def reason(self):
        reason=self._reason
        if reason:
            return reason
        return self._get_close_reason(self.code)
        
    def __str__(self):
        return f'{self.__class__.__name__}, code={self.code}, reason={self.reason!r}, exception={self.exception!r}'

class WebSocketProtocolError(Exception):
    pass
