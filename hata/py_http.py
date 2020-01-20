# -*- coding: utf-8 -*-
__all__ = ('HTTPClient', )

from .py_helpers import TimeoutHandle,CeilTimeout,tcp_nodelay
from .py_url import URL

from .py_reqrep import ClientRequest,merge_ssl_params,Request_CM
from .py_connector import TCPConnector
from .py_cookiejar import CookieJar

from .py_hdrs import CONTENT_LENGTH, AUTHORIZATION, METH_HEAD, LOCATION,    \
    URI, METH_GET, METH_POST, METH_OPTIONS, METH_PUT, METH_PATCH, METH_DELETE

from .dereaddons_local import multidict_titled

DEFAULT_TIMEOUT=20.

class HTTPClient(object):
    __slots__=('loop','connector','proxy_url','proxy_auth', 'cookie_jar')
    def __init__(self,loop,proxy_url=None,proxy_auth=None):
        self.loop=loop
        
        self.proxy_url=proxy_url
        self.proxy_auth=proxy_auth
        
        self.connector=TCPConnector(loop)
        self.cookie_jar=CookieJar(loop)
        
    async def _request(self, method, url, headers, data=None, params=None, redirect=3):
        history         = []
        url             = URL(url)
        proxy_url       = self.proxy_url
        timer_obj       = TimeoutHandle(self.loop,DEFAULT_TIMEOUT)
        timer_handler   = timer_obj.start()
        timer           = timer_obj.timer()
        
        try:
            with timer:
                while True:
                    cookies=self.cookie_jar.filter_cookies(url)

                    if proxy_url:
                        proxy_url=URL(proxy_url)
            
                    request=ClientRequest(method,url,self.loop,headers,data,params,
                        cookies,None,proxy_url,self.proxy_auth,timer)

                    with CeilTimeout(self.loop,DEFAULT_TIMEOUT):
                        connection = await self.connector.connect(request,DEFAULT_TIMEOUT)

                    tcp_nodelay(connection.transport,True)

                    connection.protocol.set_response_params(
                        timer           =timer,
                        skip_payload    = (method.upper()==METH_HEAD),
                        read_until_eof  =True,
                        auto_decompress =True,
                        read_timeout    =None,)
                    
                    try:
                        response=await request.send(connection)
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
                    if response.status in (301,302,303,307) and redirect:
                        redirect-=1
                        history.append(response)
                        if not redirect:
                            response.close()
                            raise ConnectionError('Too many redirects',history[0].request_info,tuple(history))

                        # For 301 and 302, mimic IE behaviour, now changed in RFC.
                        # Details: https://github.com/kennethreitz/requests/pull/269
                        if (response.status==303 and response.method!=METH_HEAD) \
                           or (response.status in (301,302) and response.method==METH_POST):
                            method=METH_GET
                            data=None
                            headers.pop(CONTENT_LENGTH,None)

                        redirect_url = (response.headers.get(LOCATION) or response.headers.get(URI))
                        if redirect_url is None:
                            break
                        else:
                            response.release()
                        
                        redirect_url=URL(redirect_url)

                        scheme=redirect_url.scheme
                        if scheme not in ('http','https',''):
                            response.close()
                            raise ValueError('Can redirect only to http or https')
                        elif not scheme:
                            redirect_url=url.join(redirect_url)


                        if url.origin()!=redirect_url.origin():
                            headers.pop(AUTHORIZATION,None)
                            
                        url=redirect_url
                        params = None
                        response.release()
                        continue

                    break

            # register connection
            if response.connection is None:
                timer_handler.cancel()
            else:
                response.connection.add_callback(timer_handler.cancel)

            response.history=tuple(history)
            return response
        except BaseException:
            timer_obj.close()
            raise
        
    async def _request2(self, method, url, headers=None, params=None,
            data=None, auth=None, redirects=10, read_until_eof=True,
            proxy_url=None, proxy_auth=None, timeout=DEFAULT_TIMEOUT,
            ssl=None, verify_ssl=None, ssl_context=None, fingerprint=None, ):

        # Transform headers to multidict_titled
        headers = multidict_titled(headers)

        if (headers and auth is not None and AUTHORIZATION in headers):
            raise ValueError('Can\'t combine \'Authorization\' header with \'auth\' argument')

        if (proxy_url is None):
            proxy_url   = self.proxy_url
        if (proxy_auth is None):
            proxy_auth  = self.proxy_auth
        
        ssl             = merge_ssl_params(ssl,verify_ssl,ssl_context,fingerprint)
        history         = []
        url             = URL(url)
        timer_obj       = TimeoutHandle(self.loop,timeout)
        timer_handler   = timer_obj.start()
        timer           = timer_obj.timer()

        try:
            with timer:
                while True:
                    cookies=self.cookie_jar.filter_cookies(url)

                    if proxy_url:
                        proxy_url=URL(proxy_url)

                    request=ClientRequest(method,url,self.loop,headers,data,params,
                        cookies,auth,proxy_url,proxy_auth,timer,ssl)
                    
                    with CeilTimeout(self.loop,timeout):
                        connection=await self.connector.connect(request,timeout)

                    tcp_nodelay(connection.transport,True)

                    connection.protocol.set_response_params(
                        timer           = timer,
                        skip_payload    = (method.upper()==METH_HEAD),
                        read_until_eof  = read_until_eof,
                        auto_decompress = True,
                        read_timeout    = None,)

                    try:
                        response=await request.send(connection)
                        try:
                            await response.start(connection)
                        except BaseException:
                            response.close()
                            raise
                    except BaseException:
                        connection.close()
                        raise
 
                    #we do nothing with os error

                    self.cookie_jar.update_cookies(response.cookies,response.url)

                    # redirects
                    if response.status in (301,302,303,307) and redirects:
                        redirects-=1
                        history.append(response)
                        if not redirects:
                            response.close()
                            raise ConnectionError('Too many redirects',history[0].request_info,tuple(history))

                        # For 301 and 302, mimic IE behaviour, now changed in RFC.
                        # Details: https://github.com/kennethreitz/requests/pull/269
                        if (response.status==303 and response.method!=METH_HEAD) \
                                or (response.status in (301, 302) and response.method==METH_POST):
                            
                            method=METH_GET
                            data=None
                            content_ln=headers.get(CONTENT_LENGTH)
                            if (content_ln is not None) and content_ln:
                                del headers[CONTENT_LENGTH]

                        redirect_url = response.headers.get(LOCATION)
                        if redirect_url is None:
                            redirect_url = response.headers.get(URI)
                            if redirect_url is None:
                                break
                        
                        response.release()
                        
                        redirect_url=URL(redirect_url)

                        scheme=redirect_url.scheme
                        if scheme not in ('http', 'https', ''):
                            response.close()
                            raise ValueError('Can redirect only to http or https')
                        elif not scheme:
                            redirect_url=url.join(redirect_url)

                        url     = redirect_url
                        params  = None
                        await response.release()
                        continue

                    break
            
            # register connection
            if response.connection is not None:
                response.connection.add_callback(timer_handler.cancel)
            else:
                timer_handler.cancel()
            
            response.history=tuple(history)
            return response
        
        except BaseException:
            timer_obj.close()
            raise
    
    async def close(self):
        connector=self.connector
        if connector is None:
            return
        
        if not connector.closed:
            connector.close()
        self.connector=None
        
    async def restart(self):
        connector=self.connector
        if (connector is not None) and (not connector.closed):
            connector.close()
        
        self.connector=TCPConnector(self.loop)
        
    @property
    def closed(self):
        connector=self.connector
        if connector is None:
            return True
        
        if connector.closed:
            return True
        
        return False
        
    async def __aenter__(self):
        return self

    async def __aexit__(self,exc_type,exc_val,exc_tb):
        await self.close()

    def __del__(self):
        connector=self.connector
        if connector is None:
            return
        
        if not connector.closed:
            connector.close()
        
        self.connector=None
    
    def request(self, meth, url, headers=None, **kwargs):
        if headers is None:
            headers=multidict_titled()
        return Request_CM(self._request(meth, url, headers, **kwargs))
    
    def request2(self, meth, url, headers=None, **kwargs):
        if headers is None:
            headers=multidict_titled()
        return Request_CM(self._request2(meth, url, headers, **kwargs))
    
    def get(self, url, headers=None, **kwargs):
        if headers is None:
            headers=multidict_titled()
        return Request_CM(self._request(METH_GET, url, headers, **kwargs))
    
    def options(self, url, headers=None, **kwargs):
        if headers is None:
            headers=multidict_titled()
        return Request_CM(self._request(METH_OPTIONS, url, headers, **kwargs))
    
    def head(self, url, headers=None, **kwargs):
        if headers is None:
            headers=multidict_titled()
        return Request_CM(self._request(METH_HEAD, url, headers, **kwargs))
    
    def port(self, url, headers=None, **kwargs):
        if headers is None:
            headers=multidict_titled()
        return Request_CM(self._request(METH_POST, url, headers, **kwargs))
    
    def put(self, url, headers=None, **kwargs):
        if headers is None:
            headers=multidict_titled()
        return Request_CM(self._request(METH_PUT, url, headers, **kwargs))
    
    def patch(self, url, headers=None, **kwargs):
        if headers is None:
            headers=multidict_titled()
        return Request_CM(self._request(METH_PATCH, url, headers, **kwargs))
    
    def delete(self, url, headers=None, **kwargs):
        if headers is None:
            headers=multidict_titled()
        return Request_CM(self._request(METH_DELETE, url, headers, **kwargs))
