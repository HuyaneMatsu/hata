# -*- coding: utf-8 -*-
import socket as module_socket
from functools import lru_cache
from http.cookies import SimpleCookie
from collections import defaultdict
from time import monotonic
from threading import current_thread

try:
    import ssl as module_ssl
except ImportError:
    module_ssl = None
    ssl_errors = ()
else:
    ssl_errors = (module_ssl.SSLError, module_ssl.CertificateError)

from .dereaddons_local import multidict_titled
from .futures import shield, Task

from .hdrs import HOST, METH_GET, AUTHORIZATION, PROXY_AUTHORIZATION, METH_CONNECT
from .reqrep import ClientRequest, Fingerprint, SSL_ALLOWED_TYPES
from .exceptions import ProxyError
from .helpers import is_ip_address, CeilTimeout
from .websocket import ProtocolBase

KEEP_ALIVE_TIMEOUT = 15.0
    
class Connection(object):
    __slots__=('callbacks', 'connector', 'key', 'loop', 'protocol',)
    def __init__(self,connector,key,protocol,loop):
        self.connector  = connector
        self.key        = key
        self.protocol   = protocol
        self.loop       = loop
        self.callbacks  = []
    
    def __repr__(self):
        return f'<{self.__class__.__name__} to {self.key}>'
    
    def __del__(self):
        if self.loop.running:
            protocol = self.protocol
            if (protocol is not None):
                self.connector.release(self.key, protocol, should_close=True)
    
    @property
    def transport(self):
        return self.protocol.transport
    
    @property
    def writer(self):
        return self.protocol.writer
    
    def add_callback(self,callback):
        if callback is None:
            return
        
        if not self.closed:
            self.callbacks.append(callback)
            return
        
        try:
            callback()
        except BaseException as err:
            current_thread().render_exc_async(err,[
                'Exception occured at ',
                repr(self),
                '.add_callback\nAt running ',
                repr(callback),
                '\n',
                    ])
    
    def _run_callbacks(self):
        callbacks = self.callbacks
        while callbacks:
            callback = callbacks.pop()
            
            try:
                callback()
            except BaseException as err:
                current_thread().render_exc_async(err,[
                    'Exception occured at ',
                    repr(self),
                    '._run_callbacks\nAt running ',
                    repr(callback),
                    '\n',
                        ])
    
    def close(self):
        self._run_callbacks()
        
        protocol=self.protocol
        if (protocol is not None):
            self.connector.release(self.key,protocol,should_close=True)
            self.protocol=None
    
    def release(self):
        self._run_callbacks()
        
        protocol=self.protocol
        if (protocol is not None):
            self.connector.release(self.key,protocol,should_close=protocol.should_close())
            self.protocol=None
    
    def detach(self):
        self._run_callbacks()
        
        protocol=self.protocol
        if (protocol is not None):
            self.connector.release_acquired(self.key,protocol)
            self.protocol=None
    
    @property
    def closed(self):
        protocol = self.protocol
        if protocol is None:
            return True
        
        return (protocol.transport is None)


class ConnectorBase(object):
    __slots__=('__weakref__', 'acquired', 'acquired_per_host', 'cleanup_handle', 'closed', 'connections', 'cookies',
        'force_close', 'loop', )
    #Base connector class.
    #force_close - Set to True to force close and do reconnect
    #    after each request (and between redirects).
    
    def __new__(cls, loop, force_close=False,):
        
        self=object.__new__(cls)
        self.loop               = loop
        self.closed             = False
        self.connections        = {}
        self.acquired           = set()
        self.acquired_per_host  = defaultdict(set)
        self.force_close        = force_close
        self.cookies            = SimpleCookie()
        self.cleanup_handle     = None
        return self
    
    def __del__(self):
        if (not self.closed) and self.connections:
            self.close()
    
    def _cleanup(self):
        handle = self.cleanup_handle
        if (handle is not None):
            # Cancelling the currently running handle does nothing.
            handle.cancel()
            self.cleanup_handle = None
        
        #Cleanup unused transports.
        connections = self.connections
        if not connections:
            return
        
        now = monotonic()
        to_remove_keys = []
        
        for key, connections_ in connections.items():
            for index in reversed(range(len(connections_))):
                protocol, time = connections_[index]
                
                if time + KEEP_ALIVE_TIMEOUT < now:
                    continue
                
                del connections_[index]
                transport = protocol.transport
                if key.is_ssl and (transport is not None):
                    transport.abort()
            
            if not connections_:
                to_remove_keys.append(key)
        
        for key in to_remove_keys:
            del connections[key]
        
        if connections:
            self.cleanup_handle = self.loop.call_later_weak(KEEP_ALIVE_TIMEOUT, self._cleanup,)
    
    def drop_acquired_per_host(self, key, val):
        acquired_per_host=self.acquired_per_host
        try:
            connections=acquired_per_host[key]
        except KeyError:
            return
        
        connections.remove(val)
        
        if not connections:
            del acquired_per_host[key]
    
    def close(self):
        #Close all opened transports.
        if self.closed:
            return
        
        self.closed=True

        try:
            if not self.loop.running:
                return
            
            for connections in self.connections.values():
                for transport, time in connections:
                    transport.close()
            
            for transport in self.acquired:
                transport.close()

        finally:
            self.connections.clear()
            self.acquired.clear()
    
    async def connect(self,request,timeout):
        #Get from pool or create new connection.
        key=request.connection_key
        
        protocol = self.get_protocol(key)
        if protocol is None:
            protocol = await self.create_connection(request,timeout)
            if self.closed:
                protocol.close()
                raise ConnectionError('Connector is closed.')
        
        self.acquired.add(protocol)
        self.acquired_per_host[key].add(protocol)
        
        return Connection(self, key, protocol, self.loop)
    
    def get_protocol(self, key):
        try:
            connections = self.connections[key]
        except KeyError:
            return None
        
        now = monotonic()
        while connections:
            protocol, time = connections.pop()
            if (protocol.transport is None):
                continue
            
            if (now - time) > KEEP_ALIVE_TIMEOUT:
                transport = protocol.transport
                protocol.close()
                if key.is_ssl and (transport is not None):
                    transport.abort()
            else:
                if not connections:
                    del self.connections[key]
                
                return protocol
        
        del self.connections[key]
    
    def release_acquired(self,key,protocol):
        if self.closed:
            return
        
        try:
            self.acquired.remove(protocol)
            self.drop_acquired_per_host(key,protocol)
        except KeyError:
            pass
    
    def release(self, key, protocol, should_close=False):
        if self.closed:
            return
        
        self.release_acquired(key,protocol)
        
        if should_close or self.force_close or protocol.should_close():
            transport = protocol.transport
            protocol.close()
            if key.is_ssl and (transport is not None):
                transport.abort()
        else:
            try:
                connections=self.connections[key]
            except KeyError:
                connections=self.connections[key]=[]
            
            connections.append((protocol,monotonic()))
            
            if self.cleanup_handle is None:
                self.cleanup_handle = self.loop.call_later_weak(KEEP_ALIVE_TIMEOUT, self._cleanup,)
    
    async def create_connection(self,request,timeout):
        #not implemented
        pass

DNS_CACHE_TIMEOUT = 10.0

class HostInfo(object):
    __slots__ = ('hostname', 'host', 'port', 'family', 'proto', 'flags', )
    
    def __repr__(self):
        return f'<{self.__class__.__name__}, hostname={self.hostname!r}, host={self.host!r}, port={self.port!r}, ' \
               f'family={self.family!r}, proto={self.proto!r}, flags={self.flags!r}>'
    
    @classmethod
    def from_ip(cls, host, port, family):
        self = object.__new__(cls)
        self.hostname = host
        self.host = host
        self.port = port
        self.family = family
        self.proto = 0
        self.flags = 0
        
        return self

    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.hostname!=other.hostname:
            return False
        
        if self.host!=other.host:
            return False
        
        if self.port!=other.port:
            return False
        
        if self.family!=other.family:
            return False
        
        if self.proto!=other.proto:
            return False
        
        if self.flags!=other.flags:
            return False
        
        return True

    def __hash__(self):
        return hash(self.hostname) ^ hash(self.host) ^ (self.port << 17 ) ^ hash(self.family) ^ hash(self.proto) ^ hash(self.flags)

class HostInfoCont(object):
    __slots__ = ('addrs', 'index', 'timestamp')
    
    def __new__(cls, host, infos):
        addrs = []
        for element in infos:
            unit = HostInfo()
            unit.hostname = host
            adress = element[4]
            unit.host = adress[0]
            unit.port = adress[1]
            unit.family = element[0]
            unit.proto = element[2]
            unit.flags = module_socket.AI_NUMERICHOST
            
            addrs.append(unit)
    
        self = object.__new__(cls)
        self.index = 0
        self.timestamp = monotonic()
        self.addrs = addrs
        
        return self
    
    @property
    def expired(self):
        return ((self.timestamp+DNS_CACHE_TIMEOUT) < monotonic())
    
    def next_addrs(self):
        result = []
        
        addrs = self.addrs
        index = self.index
        limit = len(addrs)
        left = limit
        
        while True:
            value = addrs[index]
            result.append(value)
            index +=1
            if index == limit:
                index = 0
            
            left -=1
            if left:
                continue
            
            break
        
        self.index = index
        return result

    def __repr__(self):
        return f'<{self.__class__.__name__} addrs={self.addrs!r}, index={self.index!r}, timestamp={self.timestamp!r}>'
    
class TCPConnector(ConnectorBase):
    __slots__=('acquired', 'acquired_per_host', 'cached_hosts',
        'closed', 'force_close', 'connections', 'cookies',
        'dns_events', 'family', 'local_addr', 'loop',
        'ssl', 'use_dns_cache', 'waiters',)
    #TCP connector.
    #fingerprint - Pass the binary md5, sha1, or sha256
    #    digest of the expected certificate in DER format to verify
    #    that the certificate the server presents matches. See also
    #    https://en.wikipedia.org/wiki/Transport_Layer_Security#Certificate_pinning
    #family - socket address family
    #local_addr - local tuple of (host, port) to bind socket to
    #conn_timeout - (optional) Connect timeout.
    #force_close - Set to True to force close and do reconnect
    #    after each request (and between redirects).


    def __new__(cls, loop, fingerprint=None, family=0, ssl_context=None, ssl=None, local_addr=None,
            force_close=False, ):
        
        if not isinstance(ssl, SSL_ALLOWED_TYPES):
            raise TypeError(f'`ssl` should be one of instance of: {SSL_ALLOWED_TYPES!r}, but got `{ssl!r}` instead.')
        
        self = ConnectorBase.__new__(cls,loop,force_close,)
        
        self.ssl            = ssl
        self.cached_hosts   = {}
        self.dns_events     = {}
        self.family         = family
        self.local_addr     = local_addr
        
        return self

    def close(self):
        for event in self.dns_events.values():
            event.cancel()
        
        ConnectorBase.close(self)
    
    def clear_dns_cache(self,host=None,port=None):
        if (host is not None) and (port is not None):
            try:
                del self.cached_hosts[(host,port)]
            except KeyError:
                pass
        else:
            self.cached_hosts.clear()
    
    async def resolve(self, host, port=0, family=module_socket.AF_INET):
        infos = await self.loop.getaddrinfo(host,port,type=module_socket.SOCK_STREAM,family=family)
        return HostInfoCont(host, infos,)
    
    async def resolver_task(self, key,):
        
        try:
            event = self.dns_events[key]
        except KeyError:
            event = Task(self.resolve(*key, family=self.family), self.loop)
            self.dns_events[key]= event
            try:
                hostinfo = await event
            except:
                raise
            else:
                self.cached_hosts[key] = hostinfo
            finally:
                del self.dns_events[key]
        else:
            hostinfo = await event
        
        return hostinfo
    
    async def resolve_host_iterator(self, request):
        host = request.url.raw_host
        port = request.port
        
        if is_ip_address(host):
            yield HostInfo.from_ip(host, port, self.family)
            return
        
        key = (host, port)
        try:
            value = self.cached_hosts[key]
        except KeyError:
            pass
        else:
            expired = value.expired
            if expired:
                task = shield(self.resolver_task(key), self.loop)
            
            addrs = value.next_addrs()
            for hostinfo in addrs:
                yield hostinfo
            
            if expired:
                try:
                    value = await task
                except OSError as err:
                    raise ConnectionError(request.connection_key,err) from err
                
                new_addrs = value.next_addrs()
                for hostinfo in new_addrs:
                    if hostinfo in addrs:
                        continue
                    
                    yield hostinfo
            
            return
        
        task = shield(self.resolver_task(key), self.loop)
        
        try:
            value = await task
        except OSError as err:
            raise ConnectionError(request.connection_key,err) from err
        
        for hostinfo in value.next_addrs():
            yield hostinfo
    
    async def create_connection(self,request,timeout):
        #Has same keyword arguments as BaseEventLoop.create_connection.
        
        if request.proxy_url:
            _,protocol = await self.create_proxy_connection(request,timeout)
        else:
            _,protocol = await self.create_direct_connection(request,timeout)

        return protocol
    
    @staticmethod
    @lru_cache(None)
    def make_ssl_context(verified):
        if verified:
            return module_ssl.create_default_context()
        else:
            sslcontext = module_ssl.SSLContext(module_ssl.PROTOCOL_SSLv23)
            sslcontext.options|=module_ssl.OP_NO_SSLv2
            sslcontext.options|=module_ssl.OP_NO_SSLv3
            sslcontext.options|=module_ssl.OP_NO_COMPRESSION
            sslcontext.set_default_verify_paths()
            return sslcontext
    
    def get_ssl_context(self,request):
        #Logic to get the correct SSL context
        
        #0. if request.ssl is False, return None
        
        #1. if ssl_context is specified in request, use it
        #2. if _ssl_context is specified in self, use it
        #3. otherwise:
        #    1. if verify_ssl is not specified in request, use self.ssl_context
        #       (will generate a default context according to self.verify_ssl)
        #    2. if verify_ssl is True in request, generate a default SSL context
        #    3. if verify_ssl is False in request, generate a SSL context that
        #       won't verify

        if not request.is_ssl():
            return
        
        if module_ssl is None:
            raise RuntimeError('SSL is not supported')
        
        sslcontext=request.ssl
        if isinstance(sslcontext, module_ssl.SSLContext):
            return sslcontext
        
        if (sslcontext is not None):
            return self.make_ssl_context(False) #not verified or fingerprinted
                        
        sslcontext=self.ssl
                                    
        if isinstance(sslcontext, module_ssl.SSLContext):
            return sslcontext
        
        return self.make_ssl_context((sslcontext is None), )

    def get_fingerprint(self,request):
        if isinstance(request.ssl,Fingerprint):
            return request.ssl
        
        if isinstance(self.ssl,Fingerprint):
            return self.ssl
    
    async def create_direct_connection(self,request,timeout):
        
        sslcontext  = self.get_ssl_context(request)
        fingerprint = self.get_fingerprint(request)
        
        last_error = None
        
        async for host_info in self.resolve_host_iterator(request):
            try:
                with CeilTimeout(self.loop,timeout):
                    transport, protocol = await self.loop.create_connection(ProtocolBase(self.loop),
                        host_info.host, host_info.port,
                        ssl = sslcontext,
                        family = host_info.family,
                        proto = host_info.proto,
                        flags = host_info.flags,
                        local_addr = self.local_addr,
                        server_hostname = (host_info.hostname if sslcontext else None),
                            )
            except ssl_errors as err:
                err.key=request.connection_key
                raise
            except OSError as err:
                last_error = OSError(request.connection_key,err)
                last_error.__cause__ = err
                continue
            
            if request.is_ssl() and fingerprint:
                try:
                    fingerprint.check(transport)
                except ValueError as err:
                    transport.close()
                    transport.abort()
                    last_error=err
                    continue
            
            return transport, protocol
        
        raise last_error
    

    async def create_proxy_connection(self,request,timeout):
        headers=multidict_titled()
        
        headers[HOST]=request.headers[HOST]
        
        proxy_request=ClientRequest(METH_GET,request.proxy_url,self.loop,headers=headers,auth=request.proxy_auth,ssl=request.ssl)
        
        # create connection to proxy server
        transport, protocol = await self.create_direct_connection(proxy_request,timeout)
        
        # Many HTTP proxies has buggy keepalive support.  Let's not
        # reuse connection but close it after processing every
        # response.
        protocol.force_close()
        
        auth=proxy_request.headers.pop(AUTHORIZATION,None)
        if auth is not None:
            if not request.is_ssl():
                request.headers[PROXY_AUTHORIZATION]=auth
            else:
                proxy_request.headers[PROXY_AUTHORIZATION]=auth
        
        if request.is_ssl():
            sslcontext          = self.get_ssl_context(request)
            proxy_request.method= METH_CONNECT
            proxy_request.url   = request.url
            key                 = (request.connection_key,None,None)
            connection          = Connection(self,key,protocol,self.loop)
            proxy_response      = await proxy_request.send(connection)
            try:
                connection.protocol.set_response_params()
                response = await proxy_response.start(connection)
            except BaseException:
                proxy_response.close()
                connection.close()
                raise
            else:
                connection.protocol  = None
                connection.protocol.transport = None
                try:
                    if response.status != 200:
                        raise ProxyError(response.status,response.reason,response.headers)
                    rawsock = transport.get_extra_info('socket',None)
                    if rawsock is None:
                        raise RuntimeError('Transport does not expose socket instance')
                    # Duplicate the socket, so now we can close proxy transport
                    rawsock=rawsock.dup()
                finally:
                    transport.close()

                try:
                    with CeilTimeout(self.loop,timeout):
                        transport, protocol= await self.loop.create_connection(ProtocolBase(self.loop),
                            ssl=sslcontext,
                            sock=rawsock,
                            server_hostname=request.host,)
                except ssl_errors as err:
                    err.key=request.connection_key
                    raise
                except OSError as err:
                    raise OSError(request.connection_key,err) from err
            
            finally:
                proxy_response.close()

        return transport,protocol

del lru_cache
