__all__ = ('HTTPClient', )
from .utils import imultidict

from .helpers import Timeout, tcp_nodelay
from .url import URL
from .reqrep import ClientRequest, SSL_ALLOWED_TYPES
from .connector import TCPConnector
from .cookiejar import CookieJar
from .headers import CONTENT_LENGTH, AUTHORIZATION, METHOD_HEAD, LOCATION, URI, METHOD_GET, METHOD_POST, \
    METHOD_OPTIONS, METHOD_PUT, METHOD_PATCH, METHOD_DELETE
from .websocket import WSClient
from .export import export

DEFAULT_TIMEOUT = 60.0

@export
class HTTPClient:
    """
    HTTP client implementation.
    
    Attributes
    ----------
    loop : ``EventThread``
        The event loop used by the http client.
    connector : ``ConnectorBase`` instance
        Connector of the http client. Defaults to ``TCPConnector`` instance.
    proxy_url : `None`, `str` or ``URL``
        Proxy url to use with all of the requests of the http client.
    proxy_auth : `None` or ``BasicAuth``
        Proxy authorization to send with all the requests of the http client.
    cookie_jar : ``CookieJar``
        Cookies stored by the http client.
    """
    __slots__ = ('loop', 'connector', 'proxy_url', 'proxy_auth', 'cookie_jar')
    def __init__(self, loop, proxy_url=None, proxy_auth=None, *, connector=None):
        """
        Creates a new ``HTTPClient`` instance with the given parameters.
        
        Parameters
        ----------
        loop : ``EventThread``
            The event loop used by the http client.
        proxy_url : `None`, `str` or ``URL``, Optional
            Proxy url to use with all of the requests of the http client. Defaults to `None`.
        proxy_auth : `None` or ``BasicAuth``, Optional
            Proxy authorization to send with all the requests of the http client. Defaults to `None`.
        connector : `None` or ``ConnectorBase`` instance, Optional (Keyword only)
            Connector to be used by the ``HTTPClient``. If not given or given as `None`, a new ``TCPConnector`` is
            created and used.
        """
        self.loop = loop
        
        self.proxy_url = proxy_url
        self.proxy_auth = proxy_auth
        
        if connector is None:
            connector = TCPConnector(loop)
        
        self.connector = connector
        self.cookie_jar = CookieJar()
        
    async def _request(self, method, url, headers, data=None, params=None, redirects=3):
        """
        Internal method for executing an http request.
        
        This method is a coroutine.
        
        Parameters
        ----------
        method : `str`
            The method of the request.
        url : `str` or ``URL``
            The url to request.
        headers : (`dict` or ``imultidict``) of (`str`, `str`) items
            Request headers.
        data : `None` or `Any`, Optional
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional
            The maximal amount of allowed redirects. Defaults to `3`.
        
        Returns
        -------
        response : ``ClientResponse``
        
        Raises
        ------
        ConnectionError
            - Too many redirects.
            - Would be redirected to not `http` or `https`.
            - Connector closed.
        ValueError
            - Host could not be detected from `url`.
            - The `proxy_url`'s scheme is not `http`.
            - `compression` and `Content-Encoding` would be set at the same time.
            - `chunked` cannot be set, because `Transfer-Encoding: chunked` is already set.
            - `chunked` cannot be set, because `Content-Length` header is already present.
        OSError
            If a system function returns a system-related error.
        RuntimeError
            - If one of `data`'s field's content has unknown content-encoding.
            - If one of `data`'s field's content has unknown content-transfer-encoding.
        TimeoutError
            Did not receive answer in time.
        TypeError
            - `proxy_auth`'s type is incorrect.
            - ˙Cannot serialize a field of the given `data`.
        
        See Also
        --------
        - ``.request`` : Executes an http request returning a request context manager.
        - ``.request2`` : Executes an http request with extra parameters returning a request context manager.
        - ``._request2`` : Internal method for executing an http request with extra parameters.
        """
        history = []
        url = URL(url)
        proxy_url = self.proxy_url
        
        with Timeout(self.loop, DEFAULT_TIMEOUT):
            while True:
                cookies = self.cookie_jar.filter_cookies(url)
                
                if (proxy_url is not None):
                    proxy_url = URL(proxy_url)
                
                request = ClientRequest(self.loop, method, url, headers, data, params, cookies, None, proxy_url,
                    self.proxy_auth, None)
                
                connection = await self.connector.connect(request)
                
                tcp_nodelay(connection.transport, True)
                
                response = await request.send(connection)
                
                # we do nothing with os error
                
                self.cookie_jar.update_cookies(response.cookies, response.url)
                
                # redirects
                if response.status in (301, 302, 303, 307) and redirects:
                    redirects -= 1
                    history.append(response)
                    if not redirects:
                        response.close()
                        raise ConnectionError('Too many redirects', history[0].request_info, tuple(history))
                    
                    if (response.status == 303 and response.method != METHOD_HEAD) \
                            or (response.status in (301, 302) and response.method == METHOD_POST):
                        method = METHOD_GET
                        data = None
                        try:
                            del headers[CONTENT_LENGTH]
                        except KeyError:
                            pass
                    
                    redirect_url = response.headers.get(LOCATION, None)
                    if redirect_url is None:
                        redirect_url = response.headers.get(URI, None)
                        if redirect_url is None:
                            break
                    
                    response.release()
                    
                    redirect_url = URL(redirect_url)
                    
                    scheme = redirect_url.scheme
                    if scheme not in ('http', 'https', ''):
                        response.close()
                        raise ConnectionError(f'Can redirect only to http or https, got {scheme!r}',
                            history[0].request_info, tuple(history))
                    
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
        
    async def _request2(self, method, url, headers=None, data=None, params=None, redirects=3, auth=None,
            proxy_url=..., proxy_auth=..., timeout=DEFAULT_TIMEOUT, ssl=None):
        """
        Internal method for executing an http request with extra parameters
        
        This method is a coroutine.
        
        Parameters
        ----------
        method : `str`
            The method of the request.
        url : `str` or ``URL``
            The url to request.
        headers : (`dict` or ``imultidict``) of (`str`, `str`) items
            Request headers.
        data : `None` or `Any`, Optional
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional
            The maximal amount of allowed redirects. Defaults to `3`.
        auth : `None` or ``BasicAuth``, Optional
            Authorization to use.
        proxy_url : `None`, `str` or ``URL``, Optional
            Proxy url to use instead of the client's own.
        proxy_auth : `None` or ``BasicAuth``, Optional
            Proxy authorization to use instead of the client's.
        timeout : `float`, Optional
            The maximal duration to wait for server response. Defaults to `60.0` seconds.
        ssl : `ssl.SSLContext`, `bool`, ``Fingerprint``, `NoneType`
            Whether and what type of ssl should the connector use.
        
        Returns
        -------
        response : ``ClientResponse``
        
        Raises
        ------
        ConnectionError
            - Too many redirects.
            - Would be redirected to not `http` or `https`.
            - Connector closed.
        TypeError
            - `proxy_auth`'s type is incorrect.
            - ˙Cannot serialize a field of the given `data`.
            - `ssl`'s type is unacceptable.
        ValueError
            - Host could not be detected from `url`.
            - The `proxy_url`'s scheme is not `http`.
            - `compression` and `Content-Encoding` would be set at the same time.
            - `chunked` cannot be set, because `Transfer-Encoding: chunked` is already set.
            - `chunked` cannot be set, because `Content-Length` header is already present.
            - `headers` contain authorization headers, but `auth` parameter is given as well.
        RuntimeError
            - If one of `data`'s field's content has unknown content-encoding.
            - If one of `data`'s field's content has unknown content-transfer-encoding.
        TimeoutError
            - Did not receive answer in time.
        
        See Also
        --------
        - ``.request`` : Executes an http request returning a request context manager.
        - ``.request2`` : Executes an http request with extra parameters returning a request context manager.
        - ``._request`` : Internal method for executing an http request without extra parameters.
        """
        # Transform headers to imultidict
        headers = imultidict(headers)
        
        if (headers and (auth is not None) and AUTHORIZATION in headers):
            raise ValueError('Can\'t combine \'Authorization\' header with \'auth\' parameter')
        
        if (proxy_url is ...):
            proxy_url = self.proxy_url
        
        if (proxy_auth is ...):
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
                
                response = await request.send(connection)
                
                # we do nothing with os error
                
                self.cookie_jar.update_cookies(response.cookies, response.url)
                
                # redirects
                if response.status in (301, 302, 303, 307) and redirects:
                    redirects -= 1
                    history.append(response)
                    if not redirects:
                        response.close()
                        raise ConnectionError('Too many redirects', history[0].request_info, tuple(history))
                    
                    # For 301 and 302, mimic IE behaviour, now changed in RFC.
                    # Details: https://github.com/kennethreitz/requests/pull/269
                    if (response.status == 303 and response.method != METHOD_HEAD) \
                            or (response.status in (301, 302) and response.method == METHOD_POST):
                        
                        method = METHOD_GET
                        data = None
                        content_length = headers.get(CONTENT_LENGTH, None)
                        if (content_length is not None) and content_length:
                            del headers[CONTENT_LENGTH]
                    
                    redirect_url = response.headers.get(LOCATION, None)
                    if redirect_url is None:
                        redirect_url = response.headers.get(URI, None)
                        if redirect_url is None:
                            break
                    
                    response.release()
                    
                    redirect_url = URL(redirect_url)
                    
                    scheme = redirect_url.scheme
                    if scheme not in ('http', 'https', ''):
                        response.close()
                        raise ConnectionError(f'Can redirect only to http or https, got {scheme!r}',
                            history[0].request_info, tuple(history))
                    
                    elif not scheme:
                        redirect_url = url.join(redirect_url)
                    
                    url = redirect_url
                    params = None
                    await response.release()
                    continue
                
                break
        
        response.history = tuple(history)
        return response
    
    @property
    def closed(self):
        """
        Returns whether the ``HTTPClient`` is closed.
        
        Returns
        -------
        closed : `bool`
        """
        connector = self.connector
        if connector is None:
            return True
        
        if connector.closed:
            return True
        
        return False
    
    async def __aenter__(self):
        """
        Enters the ``HTTPClient`` as an asynchronous context manager.
        
        This method is a coroutine.
        """
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the ``HTTPClient`` with closing it.
        
        This method is a coroutine.
        """
        self.close()
    
    def __del__(self):
        """
        Closes the ``HTTPClient`` closed.
        """
        connector = self.connector
        if connector is None:
            return
        
        self.connector = None
        
        if not connector.closed:
            connector.close()
    
    close = __del__
    
    def request(self, method, url, headers=None, **kwargs):
        """
        Executes an http request.
        
        Parameters
        ----------
        method : `str`
            The method of the request.
        url : `str` or ``URL``
            The url to request.
        headers : `None` or (`dict` or ``imultidict``) of (`str`, `str`) items, Optional
            Request headers.
        **kwargs : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        data : `None` or `Any`, Optional (Keyword only)
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional (Keyword only)
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional (Keyword only)
            The maximal amount of allowed redirects. Defaults to `3`.
        
        Returns
        -------
        request_context_manager : ``RequestCM``
        
        See Also
        --------
        - ``.request2`` : Executes an http request with extra parameters returning a request context manager.
        - ``.get`` : Shortcut for executing a get request.
        - ``.options`` : Shortcut for executing an options request.
        - ``.head`` : Shortcut for executing a head request.
        - ``.post`` : Shortcut for executing a post request.
        - ``.put`` : Shortcut for executing a put request.
        - ``.patch`` : Shortcut for executing a patch request.
        - ``.delete`` :  Shortcut for executing a delete request.
        """
        if headers is None:
            headers = imultidict()
        
        return RequestCM(self._request(method, url, headers, **kwargs))
    
    def request2(self, method, url, headers=None, **kwargs):
        """
        Executes an http request with extra parameters.
        
        Parameters
        ----------
        method : `str`
            The method of the request.
        url : `str` or ``URL``
            The url to request.
        headers : `None` or (`dict` or ``imultidict``) of (`str`, `str`) items, Optional
            Request headers.
        **kwargs : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        data : `None` or `Any`, Optional (Keyword only)
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional (Keyword only)
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional (Keyword only)
            The maximal amount of allowed redirects. Defaults to `3`.
        auth : `None` or ``BasicAuth``, Optional (Keyword only)
            Authorization to use.
        proxy_url : `None`, `str` or ``URL``, Optional
            Proxy url to use instead of the client's own.
        proxy_auth : `None` or ``BasicAuth``, Optional (Keyword only)
            Proxy authorization to use instead of the client's.
        timeout : `float`, Optional (Keyword only)
            The maximal duration to wait for server response. Defaults to `60.0` seconds.
        ssl : `ssl.SSLContext`, `bool`, ``Fingerprint``, `NoneType`
            Whether and what type of ssl should the connector use.
        
        Returns
        -------
        request_context_manager : ``RequestCM``
        
        See Also
        --------
        - ``.request`` : Executes an http request without extra parameters returning a request context manager.
        - ``.get`` : Shortcut for executing a get request.
        - ``.options`` : Shortcut for executing an options request.
        - ``.head`` : Shortcut for executing a head request.
        - ``.post`` : Shortcut for executing a post request.
        - ``.put`` : Shortcut for executing a put request.
        - ``.patch`` : Shortcut for executing a patch request.
        - ``.delete`` :  Shortcut for executing a delete request.
        """
        if headers is None:
            headers = imultidict()
        
        return RequestCM(self._request2(method, url, headers, **kwargs))
    
    def get(self, url, headers=None, **kwargs):
        """
        Shortcut for executing a get request.
        
        Parameters
        ----------
        url : `str` or ``URL``
            The url to request.
        headers : `None` or (`dict` or ``imultidict``) of (`str`, `str`) items, Optional
            Request headers.
        **kwargs : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        data : `None` or `Any`, Optional (Keyword only)
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional (Keyword only)
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional (Keyword only)
            The maximal amount of allowed redirects. Defaults to `3`.

        Returns
        -------
        request_context_manager : ``RequestCM``
        
        See Also
        --------
        - ``.request`` : Executes an http request without extra parameters returning a request context manager.
        - ``.request2`` : Executes an http request with extra parameters returning a request context manager.
        - ``.options`` : Shortcut for executing an options request.
        - ``.head`` : Shortcut for executing a head request.
        - ``.post`` : Shortcut for executing a post request.
        - ``.put`` : Shortcut for executing a put request.
        - ``.patch`` : Shortcut for executing a patch request.
        - ``.delete`` :  Shortcut for executing a delete request.
        """
        if headers is None:
            headers = imultidict()
        
        return RequestCM(self._request(METHOD_GET, url, headers, **kwargs))
    
    def options(self, url, headers=None, **kwargs):
        """
        Shortcut for executing a get request.
        
        Parameters
        ----------
        url : `str` or ``URL``
            The url to request.
        headers : `None` or (`dict` or ``imultidict``) of (`str`, `str`) items, Optional
            Request headers.
        **kwargs : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        data : `None` or `Any`, Optional (Keyword only)
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional (Keyword only)
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional (Keyword only)
            The maximal amount of allowed redirects. Defaults to `3`.

        Returns
        -------
        request_context_manager : ``RequestCM``
        
        See Also
        --------
        - ``.request`` : Executes an http request without extra parameters returning a request context manager.
        - ``.request2`` : Executes an http request with extra parameters returning a request context manager.
        - ``.get`` : Shortcut for executing a get request.
        - ``.head`` : Shortcut for executing a head request.
        - ``.post`` : Shortcut for executing a post request.
        - ``.put`` : Shortcut for executing a put request.
        - ``.patch`` : Shortcut for executing a patch request.
        - ``.delete`` :  Shortcut for executing a delete request.
        """
        if headers is None:
            headers = imultidict()
        
        return RequestCM(self._request(METHOD_OPTIONS, url, headers, **kwargs))
    
    def head(self, url, headers=None, **kwargs):
        """
        Shortcut for executing a head request.
        
        Parameters
        ----------
        url : `str` or ``URL``
            The url to request.
        headers : `None` or (`dict` or ``imultidict``) of (`str`, `str`) items, Optional
            Request headers.
        **kwargs : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        data : `None` or `Any`, Optional (Keyword only)
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional (Keyword only)
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional (Keyword only)
            The maximal amount of allowed redirects. Defaults to `3`.

        Returns
        -------
        request_context_manager : ``RequestCM``
        
        See Also
        --------
        - ``.request`` : Executes an http request without extra parameters returning a request context manager.
        - ``.request2`` : Executes an http request with extra parameters returning a request context manager.
        - ``.get`` : Shortcut for executing a get request.
        - ``.options`` : Shortcut for executing an options request.
        - ``.post`` : Shortcut for executing a post request.
        - ``.put`` : Shortcut for executing a put request.
        - ``.patch`` : Shortcut for executing a patch request.
        - ``.delete`` :  Shortcut for executing a delete request.
        """
        if headers is None:
            headers = imultidict()
        
        return RequestCM(self._request(METHOD_HEAD, url, headers, **kwargs))
    
    def post(self, url, headers=None, **kwargs):
        """
        Shortcut for executing a post request.
        
        Parameters
        ----------
        url : `str` or ``URL``
            The url to request.
        headers : `None` or (`dict` or ``imultidict``) of (`str`, `str`) items, Optional
            Request headers.
        **kwargs : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        data : `None` or `Any`, Optional (Keyword only)
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional (Keyword only)
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional (Keyword only)
            The maximal amount of allowed redirects. Defaults to `3`.

        Returns
        -------
        request_context_manager : ``RequestCM``
        
        See Also
        --------
        - ``.request`` : Executes an http request without extra parameters returning a request context manager.
        - ``.request2`` : Executes an http request with extra parameters returning a request context manager.
        - ``.get`` : Shortcut for executing a get request.
        - ``.options`` : Shortcut for executing an options request.
        - ``.head`` : Shortcut for executing a head request.
        - ``.put`` : Shortcut for executing a put request.
        - ``.patch`` : Shortcut for executing a patch request.
        - ``.delete`` :  Shortcut for executing a delete request.
        """
        if headers is None:
            headers = imultidict()
        
        return RequestCM(self._request(METHOD_POST, url, headers, **kwargs))
    
    def put(self, url, headers=None, **kwargs):
        """
        Shortcut for executing a put request.
        
        Parameters
        ----------
        url : `str` or ``URL``
            The url to request.
        headers : `None` or (`dict` or ``imultidict``) of (`str`, `str`) items, Optional
            Request headers.
        **kwargs : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        data : `None` or `Any`, Optional (Keyword only)
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional (Keyword only)
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional (Keyword only)
            The maximal amount of allowed redirects. Defaults to `3`.

        Returns
        -------
        request_context_manager : ``RequestCM``
        
        See Also
        --------
        - ``.request`` : Executes an http request without extra parameters returning a request context manager.
        - ``.request2`` : Executes an http request with extra parameters returning a request context manager.
        - ``.get`` : Shortcut for executing a get request.
        - ``.options`` : Shortcut for executing an options request.
        - ``.head`` : Shortcut for executing a head request.
        - ``.post`` : Shortcut for executing a post request.
        - ``.patch`` : Shortcut for executing a patch request.
        - ``.delete`` :  Shortcut for executing a delete request.
        """
        if headers is None:
            headers = imultidict()
        
        return RequestCM(self._request(METHOD_PUT, url, headers, **kwargs))
    
    def patch(self, url, headers=None, **kwargs):
        """
        Shortcut for executing a patch request.
        
        Parameters
        ----------
        url : `str` or ``URL``
            The url to request.
        headers : `None` or (`dict` or ``imultidict``) of (`str`, `str`) items, Optional
            Request headers.
        **kwargs : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        data : `None` or `Any`, Optional (Keyword only)
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional (Keyword only)
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional (Keyword only)
            The maximal amount of allowed redirects. Defaults to `3`.

        Returns
        -------
        request_context_manager : ``RequestCM``
        
        See Also
        --------
        - ``.request`` : Executes an http request without extra parameters returning a request context manager.
        - ``.request2`` : Executes an http request with extra parameters returning a request context manager.
        - ``.get`` : Shortcut for executing a get request.
        - ``.options`` : Shortcut for executing an options request.
        - ``.head`` : Shortcut for executing a head request.
        - ``.post`` : Shortcut for executing a post request.
        - ``.put`` : Shortcut for executing a put request.
        - ``.delete`` :  Shortcut for executing a delete request.
        """
        if headers is None:
            headers = imultidict()
        
        return RequestCM(self._request(METHOD_PATCH, url, headers, **kwargs))
    
    def delete(self, url, headers=None, **kwargs):
        """
        Shortcut for executing a delete request.
        
        Parameters
        ----------
        url : `str` or ``URL``
            The url to request.
        headers : `None` or (`dict` or ``imultidict``) of (`str`, `str`) items, Optional
            Request headers.
        **kwargs : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        data : `None` or `Any`, Optional (Keyword only)
            Data to send a the body of the request. Defaults to `None`.
        params : `None` or `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items, Optional (Keyword only)
            Query string parameters. Defaults to `None`.
        redirects : `int`, Optional (Keyword only)
            The maximal amount of allowed redirects. Defaults to `3`.

        Returns
        -------
        request_context_manager : ``RequestCM``
        
        See Also
        --------
        - ``.request`` : Executes an http request without extra parameters returning a request context manager.
        - ``.request2`` : Executes an http request with extra parameters returning a request context manager.
        - ``.get`` : Shortcut for executing a get request.
        - ``.options`` : Shortcut for executing an options request.
        - ``.head`` : Shortcut for executing a head request.
        - ``.post`` : Shortcut for executing a post request.
        - ``.put`` : Shortcut for executing a put request.
        - ``.patch`` : Shortcut for executing a patch request.
        """
        if headers is None:
            headers = imultidict()
        
        return RequestCM(self._request(METHOD_DELETE, url, headers, **kwargs))

    def connect_ws(self, url, **kwargs):
        """
        Connect a websocket client to the given url.
        
        Parameters
        ----------
        url : `str` or ``URL``
            The url to connect to.
        **kwargs : Keyword Parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        origin : `None` or `str`, Optional (Keyword only)
            Value of the Origin header.
        available_extensions : `None` or (`list` of `Any`), Optional (Keyword only)
            Available websocket extensions. Defaults to `None`.
            
            Each websocket extension should have the following `4` attributes / methods:
            - `name`, type `str`. The extension's name.
            - `request_params` : `list` of `tuple` (`str`, `str`). Additional header parameters of the extension.
            - `decode` : `callable`. Decoder method, what processes a received websocket frame. Should accept `2`
                parameters: The respective websocket ``Frame``, and the ˙max_size` as `int`, what describes the
                maximal size of a received frame. If it is passed, ``PayloadError`` is raised.
            - `encode` : `callable`. Encoder method, what processes the websocket frames to send. Should accept `1`
                parameter, the respective websocket ``Frame``.
        available_subprotocols : `None` or (`list` of `str`), Optional (Keyword only)
            A list of supported subprotocols in order of decreasing preference.
        extra_request_headers : ``imultidict`` or `dict-like` with (`str`, `str`) items, Optional (Keyword only)
            Extra request headers.
        http_client : `None` or ``HTTPClient`` instance, Optional (Keyword only)
            Http client to use to connect the websocket.
        close_timeout : `float`, Optional (Keyword only)
            The maximal duration in seconds what is waited for response after close frame is sent. Defaults to `10.0`.
        max_size : `int`, Optional (Keyword only)
            Max payload size to receive. If a payload exceeds it, ``PayloadError`` is raised. Defaults to `67108864`
            bytes.
        max_queue : `None` or `int`, Optional (Keyword only)
            Max queue size of ``.messages``. If a new payload is added to a full queue, the oldest element of it is
            removed. Defaults to `None`.
        """
        return WebsocketCM(WSClient(self.loop, url, **kwargs, http_client=self))

class RequestCM:
    """
    Asynchronous context manager wrapping a request coroutine.
    
    Examples
    --------
    ``RequestCM`` instances are returned by ``HTTPClient`` request methods. Request context managers can be used as an
    asynchronous context manager or as a simple awaitable.
    
    ```py
    async with http_client.get('http://python.org') as response:
        data = await response.read()
    ```
    
    ```py
    response = await http_client.get('http://python.org')
    data = await response.read()
    ```
    
    Attributes
    ----------
    coroutine : `coroutine` of (``HTTPRequest._request`` or ``HTTPRequest._request2``)
        The wrapped requester coroutine.
    response : `None` or ``ClientResponse``
        Received client response if applicable.
    """
    __slots__ = ('coroutine', 'response', )
    
    def __init__(self, coroutine):
        """
        Creates a new request content manager.
        
        Parameters
        ----------
        coroutine : `coroutine` of (``HTTPRequest._request`` or ``HTTPRequest._request2``)
            Requester coroutine to wrap.
        """
        self.coroutine = coroutine
        self.response = None
    
    def __getattr__(self, name):
        """Returns the mentioned attribute of the wrapped coroutine."""
        return getattr(self.coroutine, name)
    
    def __iter__(self):
        """
        Awaits the wrapped coroutine.
        
        This method is a generator. Should be used with `await` expression.
        
        Returns
        -------
        response : ``ClientResponse``
            Received client response if applicable.
        
        Raises
        ------
        BaseException
            Any exception raised by the request.
        """
        self.response = response = yield from self.coroutine.__await__()
        return response
    
    __await__ = __iter__
    
    async def __aenter__(self):
        """
        Enters the ``RequestCM`` as an asynchronous context manager. Releases the response when the context manager is
        exited.
        
        This method is a coroutine.
        
        Returns
        -------
        response : ``ClientResponse``
            Received client response if applicable.
        
        Raises
        ------
        BaseException
            Any exception raised by the request.
        """
        self.response = response = await self.coroutine
        return response
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the response.
        
        This method is a coroutine.
        """
        response = self.response
        if (response is not None):
            self.response = None
            response.release()


class WebsocketCM:
    """
    Asynchronous context manager wrapping a websocket connecting coroutine.
    
    Examples
    --------
    ``WebsocketCM`` instances are returned by the ``HTTPClient.connect_ws`` method. Websocket context managers can be
    used as an asynchronous context manager or as a simple awaitable.
    
    ```py
    async with http_client.connect_ws('http://ayaya.aya') as websocket:
        await websocket.send('ayaya')
    ```
    
    ```py
    websocket = await http_client.connect_ws('http://ayaya.aya')
    await websocket.send('ayaya')
    ```
    
    Attributes
    ----------
    coroutine : `coroutine` of ``WSClient.__new__``
        The wrapped requester coroutine.
    websocket : `None` or ``WSClient``
        The connected websocket client if applicable
    """
    __slots__ = ('coroutine', 'websocket', )
    
    def __init__(self, coroutine):
        """
        Creates a new websocket content manager.
        
        Parameters
        ----------
        coroutine : `coroutine` of ``WSClient.__new__``
            Websocket connecting coroutine to wrap.
        """
        self.coroutine = coroutine
        self.websocket = None
    
    def __getattr__(self, name):
        """Returns the mentioned attribute of the wrapped coroutine."""
        return getattr(self.coroutine, name)
    
    def __iter__(self):
        """
        Awaits the wrapped coroutine.
        
        This method is a generator. Should be used with `await` expression.
        
        Returns
        -------
        websocket : ``WSClient``
            The connected websocket client.
        
        Raises
        ------
        BaseException
            Any exception raised meanwhile connecting the websocket.
        """
        self.websocket = websocket = yield from self.coroutine.__await__()
        return websocket
    
    __await__ = __iter__
    
    async def __aenter__(self):
        """
        Enters the ``WebsocketCM`` as an asynchronous context manager. Closes the websocket when the context manager is
        exited.
        
        This method is a coroutine.
        
        Returns
        -------
        websocket : ``WSClient``
            The connected websocket client.
        
        Raises
        ------
        BaseException
            Any exception raised meanwhile connecting the websocket.
        """
        self.websocket = websocket = await self.coroutine
        return websocket
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the connected websocket.
        
        This method is a coroutine.
        """
        websocket = self.websocket
        if (websocket is not None):
            self.websocket = None
            await websocket.close()
