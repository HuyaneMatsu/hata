from re import compile as re_compile

from scarletio.http_client import HTTPClient


# out_websocket uses `__init__` instead of `__new__`.
assert HTTPClient.__init__ is not object.__init__

GATEWAY_URL_RP = re_compile('https\\://discord\\.com/api/v\\d+/gateway/bot')


class TestClientResponse:
    __slots__ = ('response_value',)
    def __new__(cls, response_value):
        self = object.__new__(cls)
        self.response_value = response_value
        return self
    
    
    def __await__(self):
        return self
        yield
    
    
    async def text(self, encoding = None):
        return self.response_value
    
    
    def release(self):
        pass
    
    @property
    def headers(self):
        return {'content-type': 'application/json'}
    
    
    @property
    def status(self):
        return 200


class TestHTTPClient(HTTPClient):
    """
    `out_operations` is a list of `tuple<str, object>` -> operation name and parameter(s).
    `in_operations` is a list of `tuple<str, bool, object>` -> operation name, raise and value.
    """
    __slots__ = ('out_websocket',)
    
    def __init__(self, loop, *, out_websocket = None):
        HTTPClient.__init__(self, loop)
        self.out_websocket = out_websocket
        
    
    async def _request(self, method, url, headers, data, query_parameters):
        if method == 'GET' and GATEWAY_URL_RP.fullmatch(url) is not None:
            return TestClientResponse('{"url": "orin"}')
        
        raise RuntimeError('Unexpected request', method, url, headers, data, query_parameters)

    
    async def connect_websocket(self, url):
        out_websocket = self.out_websocket
        if out_websocket is None:
            raise RuntimeError('websocket is null.')
        
        out_websocket.url = url
        return out_websocket
