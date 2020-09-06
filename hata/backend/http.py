# -*- coding: utf-8 -*-
__all__ = ('HTTPClient', )
from .dereaddons_local import multidict_titled

from .helpers import Timeout, tcp_nodelay
from .url import URL
from .reqrep import ClientRequest, SSL_ALLOWED_TYPES
from .connector import TCPConnector
from .cookiejar import CookieJar
from .hdrs import CONTENT_LENGTH, AUTHORIZATION, METH_HEAD, LOCATION, URI, METH_GET, METH_POST, METH_OPTIONS, \
    METH_PUT, METH_PATCH, METH_DELETE
from .websocket import WSClient
from . import websocket

DEFAULT_TIMEOUT = 60.

class HTTPClient(object):
    __slots__ = ('loop', 'connector', 'proxy_url', 'proxy_auth', 'cookie_jar')
    def __init__(self, loop, proxy_url=None, proxy_auth=None, *, connector=None):
        self.loop = loop
        
        self.proxy_url = proxy_url
        self.proxy_auth = proxy_auth
        
        if connector is None:
            connector = TCPConnector(loop)
        
        self.connector = connector
        self.cookie_jar = CookieJar(loop)
        
    async def _request(self, method, url, headers, data=None, params=None, redirect=3):
        history = []
        url = URL(url)
        proxy_url = self.proxy_url
        
        with Timeout(self.loop, DEFAULT_TIMEOUT):
            while True:
                cookies = self.cookie_jar.filter_cookies(url)
                
                if (proxy_url is not None):
                    proxy_url = URL(proxy_url)
                
                request = ClientRequest(self.loop, method, url, headers, data, params, cookies, None, proxy_url,
                    self.proxy_auth)
                
                connection = await self.connector.connect(request)
                
                tcp_nodelay(connection.transport, True)
                
                try:
                    response = await request.send(connection)
                    try:
                        await response.start(connection)
                    except:
                        response.close()
                        raise
                except:
                    connection.close()
                    raise
                
                #we do nothing with os error
                
                self.cookie_jar.update_cookies(response.cookies, response.url)
                
                # redirects
                if response.status in (301, 302, 303, 307) and redirect:
                    redirect -=1
                    history.append(response)
                    if not redirect:
                        response.close()
                        raise ConnectionError('Too many redirects', history[0].request_info, tuple(history))
                    
                    if (response.status == 303 and response.method != METH_HEAD) \
                            or (response.status in (301, 302) and response.method == METH_POST):
                        method = METH_GET
                        data = None
                        try:
                            del headers[CONTENT_LENGTH]
                        except KeyError:
                            pass
                    
                    redirect_url = (response.headers.get(LOCATION) or response.headers.get(URI))
                    if redirect_url is None:
                        break
                    else:
                        response.release()
                    
                    redirect_url = URL(redirect_url)
                    
                    scheme = redirect_url.scheme
                    if scheme not in ('http', 'https', ''):
                        response.close()
                        raise ValueError('Can redirect only to http or https')
                    elif not scheme:
                        redirect_url = url.join(redirect_url)
                    
                    if url.origin() != redirect_url.origin():
                        try:
                            del headers[AUTHORIZATION]
                        except KeyError:
                            pass
                    
                    url = redirect_url
                    params = None
                    response.release()
                    continue
                
                break
        
        response.history = tuple(history)
        return response
        
    async def _request2(self, method, url, headers=None, params=None, data=None, auth=None, redirects=10, read_until_eof=True,
            proxy_url=None, proxy_auth=None, timeout=DEFAULT_TIMEOUT, ssl=None):

        # Transform headers to multidict_titled
        headers = multidict_titled(headers)
        
        if (headers and auth is not None and AUTHORIZATION in headers):
            raise ValueError('Can\'t combine \'Authorization\' header with \'auth\' argument')
        
        if (proxy_url is None):
            proxy_url = self.proxy_url
        
        if (proxy_auth is None):
            proxy_auth = self.proxy_auth
        
        if not isinstance(ssl, SSL_ALLOWED_TYPES):
            raise TypeError(f'`ssl` should be one of instance of: {SSL_ALLOWED_TYPES!r}, but got `{ssl!r}` instead.')
        
        history = []
        url = URL(url)
        
        with Timeout(self.loop, timeout):
            while True:
                cookies = self.cookie_jar.filter_cookies(url)

                if (proxy_url is not None):
                    proxy_url = URL(proxy_url)

                request = ClientRequest(self.loop, method, url, headers, data, params, cookies, auth, proxy_url,
                      proxy_auth, ssl)
                
                connection = await self.connector.connect(request)

                tcp_nodelay(connection.transport, True)

                connection.protocol.set_response_params(
                    skip_payload    = (method.upper() == METH_HEAD),
                    read_until_eof  = read_until_eof,
                    auto_decompress = True,
                    read_timeout    = None,)

                try:
                    response = await request.send(connection)
                    try:
                        await response.start(connection)
                    except:
                        response.close()
                        raise
                except:
                    connection.close()
                    raise

                #we do nothing with os error

                self.cookie_jar.update_cookies(response.cookies,response.url)

                # redirects
                if response.status in (301, 302, 303, 307) and redirects:
                    redirects -=1
                    history.append(response)
                    if not redirects:
                        response.close()
                        raise ConnectionError('Too many redirects', history[0].request_info, tuple(history))
                    
                    # For 301 and 302, mimic IE behaviour, now changed in RFC.
                    # Details: https://github.com/kennethreitz/requests/pull/269
                    if (response.status == 303 and response.method != METH_HEAD) \
                            or (response.status in (301, 302) and response.method == METH_POST):
                        
                        method = METH_GET
                        data = None
                        content_ln = headers.get(CONTENT_LENGTH)
                        if (content_ln is not None) and content_ln:
                            del headers[CONTENT_LENGTH]
                    
                    redirect_url = response.headers.get(LOCATION)
                    if redirect_url is None:
                        redirect_url = response.headers.get(URI)
                        if redirect_url is None:
                            break
                    
                    response.release()
                    
                    redirect_url = URL(redirect_url)

                    scheme = redirect_url.scheme
                    if scheme not in ('http', 'https', ''):
                        response.close()
                        raise ValueError('Can redirect only to http or https')
                    elif not scheme:
                        redirect_url = url.join(redirect_url)

                    url = redirect_url
                    params = None
                    await response.release()
                    continue

                break
        
        response.history = tuple(history)
        return response
    
    async def close(self):
        self.__del__()
    
    @property
    def closed(self):
        connector = self.connector
        if connector is None:
            return True
        
        if connector.closed:
            return True
        
        return False
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    def __del__(self):
        connector = self.connector
        if connector is None:
            return
        
        self.connector = None
        
        if not connector.closed:
            connector.close()
    
    def request(self, meth, url, headers=None, **kwargs):
        if headers is None:
            headers = multidict_titled()
        return RequestCM(self._request(meth, url, headers, **kwargs))
    
    def request2(self, meth, url, headers=None, **kwargs):
        if headers is None:
            headers = multidict_titled()
        return RequestCM(self._request2(meth, url, headers, **kwargs))
    
    def get(self, url, headers=None, **kwargs):
        if headers is None:
            headers = multidict_titled()
        return RequestCM(self._request(METH_GET, url, headers, **kwargs))
    
    def options(self, url, headers=None, **kwargs):
        if headers is None:
            headers = multidict_titled()
        return RequestCM(self._request(METH_OPTIONS, url, headers, **kwargs))
    
    def head(self, url, headers=None, **kwargs):
        if headers is None:
            headers = multidict_titled()
        return RequestCM(self._request(METH_HEAD, url, headers, **kwargs))
    
    def port(self, url, headers=None, **kwargs):
        if headers is None:
            headers = multidict_titled()
        return RequestCM(self._request(METH_POST, url, headers, **kwargs))
    
    def put(self, url, headers=None, **kwargs):
        if headers is None:
            headers = multidict_titled()
        return RequestCM(self._request(METH_PUT, url, headers, **kwargs))
    
    def patch(self, url, headers=None, **kwargs):
        if headers is None:
            headers = multidict_titled()
        return RequestCM(self._request(METH_PATCH, url, headers, **kwargs))
    
    def delete(self, url, headers=None, **kwargs):
        if headers is None:
            headers = multidict_titled()
        return RequestCM(self._request(METH_DELETE, url, headers, **kwargs))

    def connect_ws(self, url, **kwargs):
        return WebsocketCM(WSClient(self.loop, url, **kwargs, http_client = self))

class RequestCM(object):
    __slots__ = ('coroutine', 'response', )
    
    def __init__(self, coroutine):
        self.coroutine = coroutine
        self.response = None
    
    def __getattr__(self, name):
        return getattr(self.coroutine, name)
    
    def __iter__(self):
        self.response = response = yield from self.coroutine.__await__()
        return response
    
    __await__ = __iter__
    
    async def __aenter__(self):
        self.response = response = await self.coroutine
        return response
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        response = self.response
        if (response is not None):
            response.release()
            self.response = None
    
class WebsocketCM(object):
    __slots__ = ('coroutine', 'websocket', )
    
    def __init__(self, coroutine):
        self.coroutine = coroutine
        self.websocket = None
    
    def __getattr__(self, name):
        return getattr(self.coroutine, name)
    
    def __iter__(self):
        self.websocket = websocket = yield from self.coroutine.__await__()
        return websocket
    
    __await__ = __iter__
    
    async def __aenter__(self):
        self.websocket = await self.coroutine
        return self.websocket
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        websocket = self.websocket
        if (websocket is not None):
            self.websocket = None
            await websocket.close()

websocket.HTTPClient = HTTPClient

del websocket
