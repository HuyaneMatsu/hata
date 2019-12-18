# -*- coding: utf-8 -*-
import ssl, functools
import socket as module_socket
from http.cookies import SimpleCookie
from collections import defaultdict,deque
from time import monotonic
from itertools import cycle, islice

from .py_hdrs import HOST, METH_GET, AUTHORIZATION, PROXY_AUTHORIZATION, METH_CONNECT
from .py_reqrep import ClientRequest,Fingerprint,merge_ssl_params
from .py_exceptions import CertificateError,SSLError,ProxyError
from .py_helpers import is_ip_address,CeilTimeout,EventResultOrError
from .py_protocol import ResponseHandler
from .dereaddons_local import multidict_titled
from .futures import shield,Future
    
class TransportPlaceholder(object):
    __slots__=()
    def close(self):
        pass
    
class Connection(object):
    __slots__=('callbacks', 'connector', 'key', 'loop', 'protocol',)
    def __init__(self,connector,key,protocol,loop):
        self.connector  = connector
        self.key        = key
        self.protocol   = protocol
        self.loop       = loop
        self.callbacks  = []

    def __repr__(self):
        return f'Connection<{self.key}>'

    def __del__(self):
        if self.loop.running:
            protocol=self.protocol
            if protocol is not None:
                self.connector.release(self.key,protocol,should_close=True)

    @property
    def transport(self):
        return self.protocol.transport

    @property
    def writer(self):
        return self.protocol.writer

    def add_callback(self,callback):
        if callback is not None:
            self.callbacks.append(callback)

    def _notifyrelease(self):
        callbacks=self.callbacks.copy()
        self.callbacks=[]

        for callback in callbacks:
            try:
                callback()
            except Exception:
                pass
                
    def close(self):
        self._notifyrelease()
        
        protocol=self.protocol
        if protocol is not None:
            self.connector.release(self.key,protocol,should_close=True)
            self.protocol=None

    def release(self):
        self._notifyrelease()
        
        protocol=self.protocol
        if protocol is not None:
            self.connector.release(self.key,protocol,should_close=protocol.should_close)
            self.protocol=None

    def detach(self):
        self._notifyrelease()
        
        protocol=self.protocol
        if protocol is not None:
            self.connector.release_acquired(protocol)
            self.protocol=None

    @property
    def closed(self):
        protocol=self.protocol
        return (protocol.transport is None) or (not protocol.is_connected())


class BaseConnector(object):
    __slots__=('acquired', 'acquired_per_host', 'closed',
        'connections', 'cookies', 'force_close', 'loop', 'waiters',)
    #Base connector class.
    #conn_timeout - (optional) Connect timeout.
    #force_close - Set to True to force close and do reconnect
    #    after each request (and between redirects).

    def __new__(cls,loop,force_close=False,):

        self=object.__new__(cls)
        self.loop               = loop
        self.closed             = False # prevent AttributeError in __del__ if ctor was failed
        self.connections        = {}
        self.acquired           = set()
        self.acquired_per_host  = defaultdict(set)
        self.force_close        = force_close
        self.waiters            = defaultdict(deque)
        self.cookies            = SimpleCookie()
        return self

    def __del__(self):
        if (not self.closed) and self.connections:
            self.close()

    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.close()

    def _cleanup(self):
        #Cleanup unused transports.
        now = self.loop.time()

        if self.connections:
            new_connections={}
            
            for key,connections in self.connections.items():
                alive=[]
                for protocol,use_time in connections:
                    if protocol.is_connected():
                        if use_time<now:
                            protocol.close()
                        else:
                            alive.append((protocol,use_time))
                    
                if alive:
                    new_connections[key]=alive
            
            self.connections=new_connections

    def drop_acquired_per_host(self,key,val):
        acquired_per_host=self.acquired_per_host
        try:
            connections=acquired_per_host[key]
        except KeyError:
            return
        connections.remove(val)
        if not connections:
            del self.acquired_per_host[key]
            
    def close(self):
        #Close all opened transports.
        result=Future(self.loop)
        result.set_result(None)
        if self.closed:
            return result
        self.closed=True

        try:
            if not self.loop.running:
                return result

            for key,data in self.connections.items():
                for transport,times in data:
                    if transport is None:
                        continue
                    transport.close()
            
            for transport in self.acquired:
                transport.close()

        finally:
            self.connections.clear()
            self.acquired.clear()
        return result
    
    async def connect(self,request,timeout):
        #Get from pool or create new connection.
        key=request.connection_key

        placeholder=TransportPlaceholder()
        self.acquired.add(placeholder)
        self.acquired_per_host[key].add(placeholder)

        try:
            protocol = await self.create_connection(request,timeout)
            if self.closed:
                protocol.close()
                raise ConnectionError('Connector is closed.')

        except BaseException:
            if not self.closed:
                self.acquired.remove(placeholder)
                self.drop_acquired_per_host(key,placeholder)
            raise

        self.acquired.remove(placeholder)
        self.drop_acquired_per_host(key,placeholder)
            
        self.acquired.add(protocol)
        self.acquired_per_host[key].add(protocol)
        return Connection(self,key,protocol,self.loop)
        return Connection(self,key,protocol,self.loop)

    def release_acquired(self,key,protocol):
        if self.closed:
            # acquired connection is already released on connector closing
            return
        
        try:
            self.acquired.remove(protocol)
            self.drop_acquired_per_host(key,protocol)
        except KeyError:
            # this may be result of undetermenistic order of objects
            # finalization due garbage collection.
            pass

    def release(self,key,protocol,should_close=False):
        if self.closed:
            return
        self.release_acquired(key,protocol)

        if should_close or self.force_close or protocol.should_close:
            transport = protocol.transport
            protocol.close()
            if key.is_ssl and transport is not None:
                transport.abort()
        else:
            connections=self.connections.get(key,None)
            if connections is None:
                connections=self.connections[key]=[]
            connections.append((protocol,self.loop.time()))
            
            self._cleanup()

    async def create_connection(self,request,timeout):
        #not implemented
        pass
    
class DNSCacheTable:
    __slots__=('addrs_rr', 'timestamps', 'ttl',)
    def __init__(self,ttl=None):
        self.addrs_rr   = {}
        self.timestamps = {}
        self.ttl        = ttl

    def __contains__(self, host):
        return host in self.addrs_rr

    def add(self, host, addrs):
        self.addrs_rr[host]=(cycle(addrs),len(addrs))

        if self.ttl:
            self.timestamps[host]=monotonic()

    def remove(self, host):
        self.addrs_rr.pop(host,None)

        if self.ttl:
            self.timestamps.pop(host,None)

    def clear(self):
        self.addrs_rr.clear()
        self.timestamps.clear()

    def next_addrs(self,host):
        loop,length=self.addrs_rr[host]
        addrs=list(islice(loop,length))
        # Consume one more element to shift internal state of `cycle`
        next(loop)
        return addrs

    def expired(self, host):
        if self.ttl is None:
            return False
        
        return self.timestamps[host]+self.ttl<monotonic()
    
class TCPConnector(BaseConnector):
    __slots__=('acquired', 'acquired_per_host', 'cached_hosts',
        'closed', 'force_close', 'connections', 'cookies',
        'dns_events', 'family', 'local_addr', 'loop',
        'ssl', 'use_dns_cache', 'waiters',)
    #TCP connector.
    #verify_ssl - Set to True to check ssl certifications.
    #fingerprint - Pass the binary md5, sha1, or sha256
    #    digest of the expected certificate in DER format to verify
    #    that the certificate the server presents matches. See also
    #    https://en.wikipedia.org/wiki/Transport_Layer_Security#Certificate_pinning
    #use_dns_cache - Use memory cache for DNS lookups.
    #ttl_dns_cache - Max seconds having cached a DNS entry, None forever
    #family - socket address family
    #local_addr - local tuple of (host, port) to bind socket to
    #conn_timeout - (optional) Connect timeout.
    #force_close - Set to True to force close and do reconnect
    #    after each request (and between redirects).


    def __new__(cls,loop, verify_ssl=True, fingerprint=None, ttl_dns_cache=10,
                 family=0, ssl_context=None, ssl=None, local_addr=None,
                 force_close=False,):

        self=BaseConnector.__new__(cls,loop,force_close,)

        self.ssl            = merge_ssl_params(ssl,verify_ssl,ssl_context,fingerprint)
        self.cached_hosts   = DNSCacheTable(ttl=ttl_dns_cache)
        self.dns_events     = {}
        self.family         = family
        self.local_addr     = local_addr

        return self

    def close(self):
        for event in self.dns_events.values():
            event.cancel()

        BaseConnector.close(self)


    def clear_dns_cache(self,host=None,port=None):
        if host and port:
            self.cached_hosts.remove((host,port),)
        else:
            self.cached_hosts.clear()
    
    async def resolve(self,host,port=0,family=module_socket.AF_INET):
        infos = await self.loop.getaddrinfo(host,port,type=module_socket.SOCK_STREAM,family=family)
        
        hosts = []
        for family, _, proto, _, address in infos:
            hosts.append({
                'hostname'  : host,
                'host'      : address[0],
                'port'      : address[1],
                'family'    : family,
                'proto'     : proto,
                'flags'     : module_socket.AI_NUMERICHOST})

        return hosts

    async def resolve_host(self,host,port):
        if is_ip_address(host):
            return [{
                'hostname'  : host,
                'host'      : host,
                'port'      : port,
                'family'    : self.family,
                'proto'     : 0,
                'flags'     : 0,
                    }]

        key=(host,port)

        if (key in self.cached_hosts) and (not self.cached_hosts.expired(key)):
            return self.cached_hosts.next_addrs(key)

        if key in self.dns_events:
            await self.dns_events[key].wait()
        else:
            self.dns_events[key]=EventResultOrError(self.loop)
            try:
                addrs = await self.resolve(host,port,family=self.family)
                
                self.cached_hosts.add(key,addrs)
                self.dns_events[key].set()
                
            except BaseException as err:
                # any DNS exception, independently of the implementation
                # is set for the waiters to raise the same exception.
                self.dns_events[key].set(err)
                raise
            finally:
                self.dns_events.pop(key)

        return self.cached_hosts.next_addrs(key)

    async def create_connection(self,request,timeout):
        #Has same keyword arguments as BaseEventLoop.create_connection.
        
        if request.proxy_url:
            _,protocol = await self.create_proxy_connection(request,timeout)
        else:
            _,protocol = await self.create_direct_connection(request,timeout)

        return protocol

    @staticmethod
    @functools.lru_cache(None)
    def make_ssl_context(verified):
        if verified:
            return ssl.create_default_context()
        else:
            sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            sslcontext.options|=ssl.OP_NO_SSLv2
            sslcontext.options|=ssl.OP_NO_SSLv3
            sslcontext.options|=ssl.OP_NO_COMPRESSION
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
        
        sslcontext=request.ssl
        if isinstance(sslcontext,ssl.SSLContext):
            return sslcontext
        
        if sslcontext:
            return self.make_ssl_context(False) #not verified or fingerprinted
                                    
        sslcontext=self.ssl
                                    
        if isinstance(sslcontext,ssl.SSLContext):
            return sslcontext
        
        if sslcontext:
            return self.make_ssl_context(False) #not verified or fingerprinted
        
        return self.make_ssl_context(True)

    def get_fingerprint(self,request):
        if isinstance(request.ssl,Fingerprint):
            return request.ssl
        
        if isinstance(self.ssl,Fingerprint):
            return self.ssl

    async def wrapcreate_connection(self,*args,request,timeout,**kwargs):
        try:
            with CeilTimeout(self.loop,timeout):
                return await self.loop.create_connection(*args,**kwargs)
        except (CertificateError,SSLError) as err:
            err.key=request.connection_key
            raise
        except OSError as err:
            raise OSError(request.connection_key,err) from err
        
    async def create_direct_connection(self,request,timeout):
        
        sslcontext  = self.get_ssl_context(request)
        fingerprint = self.get_fingerprint(request)

        try:
            # Cancelling this lookup should not cancel the underlying lookup
            # or else the cancel event will get broadcast to all the waiters
            # across all connections.
            hosts = await shield(self.resolve_host(request.url.raw_host,request.port),self.loop)
        except OSError as err:
            # in case of proxy it is not ProxyError
            # it is problem of resolving proxy ip itself
            raise ConnectionError(request.connection_key,err) from err
        
        last_error = None

        for hinfo in hosts:
            host = hinfo['host']
            port = hinfo['port']

            try:
                transport,protocol = await self.wrapcreate_connection(
                    ResponseHandler(self.loop),host,port,timeout=timeout,
                    ssl=sslcontext,family=hinfo['family'],
                    proto=hinfo['proto'],
                    flags=hinfo['flags'],
                    server_hostname=hinfo['hostname'] if sslcontext else None,
                    local_addr=self.local_addr,request=request)
            except (ConnectionError,OSError) as err:
                last_error=err
                continue
            except BaseException as err:
                raise

            if request.is_ssl() and fingerprint:
                try:
                    fingerprint.check(transport)
                except ValueError as err:
                    transport.close()
                    transport.abort()
                    last_error=err
                    continue

            return transport,protocol
        else:
            raise last_error
        
    async def create_proxy_connection(self,request,timeout):
        headers=multidict_titled()

        headers[HOST]=request.headers[HOST]

        proxy_request=ClientRequest(METH_GET,request.proxy_url,self.loop,headers=headers,auth=request.proxy_auth,ssl=request.ssl)

        # create connection to proxy server
        transport,protocol = await self.create_direct_connection(proxy_request,timeout)

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

                transport,protocol=await self.wrapcreate_connection(
                    ResponseHandler(self.loop),timeout=timeout,
                    ssl=sslcontext,sock=rawsock,
                    server_hostname=request.host,
                    request=request)
            finally:
                proxy_response.close()

        return transport,protocol
