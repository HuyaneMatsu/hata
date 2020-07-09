# -*- coding: utf-8 -*-
import json, re, codecs
from http.cookies import SimpleCookie, CookieError, Morsel
from hashlib import md5, sha1, sha256

try:
    import ssl as module_ssl
except ImportError:
    module_ssl = None

try:
    import cchardet as chardet
except ImportError:
    try:
        import chardet
    except ImportError as err:
        message=f'chardet (or cchardet) is not installed, please make sure it is installed before importing {__spec__.parent}'
        err.args=(message,)
        err.msg=message
        raise err from None

from .dereaddons_local import multidict_titled
from .futures import Task, CancelledError
from .hdrs import METH_POST_ALL, METH_CONNECT, SET_COOKIE, CONTENT_LENGTH, CONNECTION, ACCEPT, ACCEPT_ENCODING, \
    HOST, TRANSFER_ENCODING, COOKIE, CONTENT_ENCODING, AUTHORIZATION, CONTENT_TYPE
from .helpers import BasicAuth, EmptyTimer
from .multipart import MimeType, create_payload, payload_superclass
from .formdata import Formdata
from .protocol import StreamWriter

json_re = re.compile(r'^application/(?:[\w.+-]+?\+)?json')

class Fingerprint(object):
    __slots__=('fingerprint', 'hashfunc',)
    
    HASHFUNC_BY_DIGESTLEN = {
        16  : md5,
        20  : sha1,
        32  : sha256,
            }
    
    def __init__(self,fingerprint):
        digestlen=len(fingerprint)
        try:
            hashfunc=self.HASHFUNC_BY_DIGESTLEN[digestlen]
        except KeyError as err:
            err.args=('fingerprint has invalid length',)
            raise
        
        if hashfunc is md5 or hashfunc is sha1:
            raise ValueError('md5 and sha1 are insecure and not supported. Use sha256.')
    
        self.hashfunc = hashfunc
        self.fingerprint = fingerprint


    def check(self,transport):
        if not transport.get_extra_info('sslcontext'):
            return
        sslobj=transport.get_extra_info('ssl_object')
        cert= sslobj.getpeercert(binary_form=True)
        got = self.hashfunc(cert).digest()
        if got!=self.fingerprint:
            host,port,*_=transport.get_extra_info('peername')
            raise ValueError(self.fingerprint,got,host,port)

if module_ssl is None:
    SSL_ALLOWED_TYPES = type(None)
else:
    SSL_ALLOWED_TYPES = (module_ssl.SSLContext, bool, Fingerprint, type(None))

#the key should contain an information about used proxy / TLS
#to prevent reusing wrong connections from a pool
class ConnectionKey(object):
    __slots__=('host', 'is_ssl', 'port', 'proxy_auth', #'proxy_header_hash',
        'proxy_url', 'ssl',)

    def __init__(self, request):
        #if request.proxy_headers:
        #    proxy_header_hash=hash(tuple(request.proxy_headers.items()))
        #else:
        #    self.proxy_headers=None
        
        self.host               = request.host          #str
        self.port               = request.port          #int
        self.is_ssl             = request.is_ssl()      #bool
        self.ssl                = request.ssl           #SSLContext / None
        self.proxy_auth         = request.proxy_auth    #BasicAuth / None
        self.proxy_url          = request.proxy_url     #Url / None
        #self.proxy_header_hash  = proxy_header_hash     #int / None
        
    def __repr__(self):
        return f'<{self.__class__.__name__} host={self.host}, port={self.port}>'
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.host != other.host:
            return False
        
        if self.port != other.port:
            return False
        
        if self.is_ssl != other.is_ssl:
            return False
        
        if self.ssl is None:
            if other.ssl is not None:
                return False
        else:
            if other.ssl is None:
                return False
            
            if self.ssl != other.ssl:
                return False
            
        if self.proxy_auth is None:
            if other.proxy_auth is not None:
                return False
        else:
            if other.proxy_auth is None:
                return False
            
            if self.proxy_auth != other.proxy_auth:
                return False

        if self.proxy_url is None:
            if other.proxy_url is not None:
                return False
        else:
            if other.proxy_url is None:
                return False
            
            if self.proxy_url != other.proxy_url:
                return False
        
        return True
    
    def __hash__(self):
        return hash(self.host) ^ (self.port << 17) ^ hash(self.is_ssl) ^ hash(self.ssl) ^ hash(self.proxy_auth) ^ hash(self.proxy_url)

class RequestInfo(object):
    __slots__=('headers', 'method', 'real_url', 'url',)
    def __init__(self,request):
        self.url                = request.url           #URL
        self.method             = request.method        #str
        self.headers            = request.headers       #multidict_titiled
        self.real_url           = request.original_url  #URL #maybe request.url is a default for this if this is None


class ClientRequest(object):


    DEFAULT_HEADERS = (
        (ACCEPT,'*/*'),
        (ACCEPT_ENCODING,'gzip, deflate'),
            )
    
    _default_encoding='utf-8'
    
    __slots__=('auth', 'body', 'chunked', 'compression', 'encoding', 'headers',
        'length', 'loop', 'method', 'original_url', 'proxy_auth', 'proxy_url',
        'response', 'ssl', 'timer', 'url', 'writer',)
    
    def __init__(self,method,url,loop,headers=None,data=None,params=None,
                 cookies=None,auth=None,proxy_url=None,proxy_auth=None,
                 timer=None,ssl=None):
        
        url=url.extend_query(params)
        
        self.original_url   = url
        self.url            = url.with_fragment(None)
        self.method         = method
        self.encoding       = self._default_encoding
        self.loop           = loop
        if timer is None:
            self.timer      = EmptyTimer()
        else:
            self.timer      = timer
        self.ssl            = ssl
         
        #create for later
        self.chunked        = None
        self.compression    = None
        self.body           = b''
        self.auth           = None
        self.response       = None
        self.length         = None
        self.writer         = None
        
        self.update_host(url)
        self.headers = multidict_titled(headers)
        self.update_auto_headers()
        self.update_cookies(cookies)
        self.update_content_encoding(data)
        self.update_auth(auth)
        self.update_proxy(proxy_url,proxy_auth)
        
        self.update_body_from_data(data)
        self.update_transfer_encoding()
    
    def is_ssl(self):
        return self.url.scheme in ('https', 'wss')
    
    @property
    def connection_key(self):
        return ConnectionKey(self)
    
    @property
    def request_info(self):
        return RequestInfo(self)
    
    @property
    def host(self):
        return self.url.host
    
    @property
    def port(self):
        return self.url.port
    
    def update_host(self,url):
        #Update destination host, port and connection type (ssl).
        # get host/port
        if not url.host:
            raise ValueError('Host could not be detected.')
        
        # basic auth info
        username=url.user
        password=url.password
        
        if (username is not None) and username:
            if password is None:
                password=''
            self.auth=BasicAuth(username,password)
    
        # Record entire netloc for usage in host header
    
    def update_auto_headers(self):
        for key,value in self.DEFAULT_HEADERS:
            if key not in self.headers:
                self.headers[key]=value
        
        # add host
        if HOST not in self.headers:
            netloc=self.url.raw_host
            if not self.url.is_default_port():
                netlock=f'{netloc}:{self.url.port}'
            self.headers[HOST]=netloc
                
    def update_cookies(self, cookies):
        #Update request cookies header.
        if not cookies:
            return

        cookie=SimpleCookie()
        if COOKIE in self.headers:
            cookie.load(self.headers.get(COOKIE,''))
            del self.headers[COOKIE]

        for key,value in cookies.items():
            if isinstance(key,Morsel):
                # Preserve coded_value
                mrsl_val=value.get(value.key,Morsel())
                mrsl_val.set(value.key,value.value,value.coded_value)
                cookie[key]=mrsl_val
            else:
                cookie[key]=value

        self.headers[COOKIE] = cookie.output(header='', sep=';').strip()

    def update_content_encoding(self,data):
        #Set request content encoding.
        if not data:
            return

        encoding=self.headers.get(CONTENT_ENCODING,'').lower()
        
        compression = self.compression
        if (compression is not None):
            if encoding:
                raise ValueError('compression can not be set if Content-Encoding header is set')
            
            self.headers[CONTENT_ENCODING] = compression
            #enable chunked, no need to deal with length
            self.chunked = True
    
    def update_auth(self,auth):
        if auth is None:
            auth=self.auth
        if auth is None:
            return
            
        self.headers[AUTHORIZATION]=auth.encode()
    
    def update_body_from_data(self,data):
        if not data:
            return

        #formdata  
        if isinstance(data,Formdata):
            data=data()
        else:
            try:
                data=create_payload(data,disposition=None)
            except LookupError:
                data=Formdata.fromfields(data)()
        
        self.body=data
        
        if not self.chunked:
            if CONTENT_LENGTH not in self.headers:
                size=data.size
                if size is None:
                    self.chunked=True
                else:
                    if CONTENT_LENGTH not in self.headers:
                        self.headers[CONTENT_LENGTH]=str(size)
        
        if CONTENT_TYPE not in self.headers:
            self.headers[CONTENT_TYPE]=data.content_type
        
        if data.headers:
            for key,value in data.headers.items():
                if key not in self.headers:
                    self.headers[key]=value
    
    def update_transfer_encoding(self):
        #Analyze transfer-encoding header
        
        transfer_encoding = self.headers.get(TRANSFER_ENCODING, '').lower()
        
        if 'chunked' in transfer_encoding:
            if self.chunked:
                raise ValueError('Chunked can not be set if "Transfer-Encoding: chunked" header is set.')
        
        elif self.chunked:
            if CONTENT_LENGTH in self.headers:
                raise ValueError('Chunked can not be set if Content-Length header is set.')
            self.headers[TRANSFER_ENCODING]='chunked'

        else:
            if CONTENT_LENGTH not in self.headers:
                self.headers[CONTENT_LENGTH]=str(len(self.body))
    
    
    def update_proxy(self,proxy_url,proxy_auth):
        if proxy_url:
            if proxy_auth.scheme!='http':
                raise ValueError('Only http proxies are supported')
            if not isinstance(proxy_auth,BasicAuth):
                raise ValueError('proxy_auth must be None or BasicAuth')
        self.proxy_url=proxy_url
        self.proxy_auth=proxy_auth
    
    def keep_alive(self):
        return self.headers.get(CONNECTION)!='close'
    
    async def write_bytes(self,writer,connection):
        #Support coroutines that yields bytes objects.
        try:
            if isinstance(self.body,payload_superclass):
                await self.body.write(writer)
            else:
                if isinstance(self.body,(bytes,bytearray)):
                    self.body=(self.body,)

                for chunk in self.body:
                    await writer.write(chunk)
            
            await writer.write_eof()
        except (AttributeError,NameError) as err:
            connection.protocol.set_exception(err)
            raise #for testing
        except OSError as err:
            new_err = OSError(err.errno,f'Can not write request body for {self.url}')
            new_err.__context__ = err
            new_err.__cause__   = err
            connection.protocol.set_exception(new_err)
        except CancelledError as err:
            if not connection.closed:
               connection.protocol.set_exception(err)
        except Exception as err:
            connection.protocol.set_exception(err)
        finally:
            self.writer = None

    async def send(self,connection):
        # Specify request target:
        # - CONNECT request must send authority form URI
        # - not CONNECT proxy must send absolute form URI
        # - most common is origin form URI
        if self.method==METH_CONNECT:
            path = f'{self.url.raw_host}:{self.url.port}'
        elif self.proxy_url and not self.is_ssl():
            path=str(self.url)
        else:
            path=self.url.raw_path
            if self.url.raw_query_string:
                path=f'{path}?{self.url.raw_query_string}'
        
        protocol = connection.protocol
        writer = StreamWriter(protocol,self.loop,self.compression,self.chunked)
        
        # set default content-type
        if (self.method in METH_POST_ALL) and (CONTENT_TYPE not in self.headers):
            self.headers[CONTENT_TYPE]='application/octet-stream'
        
        
        connection_type=self.headers.get(CONNECTION)
           
        if ((connection_type is None) or (not connection_type)) and (not self.keep_alive()):
            connection_type='close'
                
        if (connection_type is not None):
            self.headers[CONNECTION]=connection_type
        
        
        protocol.write_http_request(self.method, path, self.headers)
        
        self.writer = Task(self.write_bytes(writer,connection),self.loop)
        
        self.response=ClientResponse(self.method,self.original_url,self.loop,self.writer,self.timer)
        return self.response

    async def close(self):
        if self.writer:
            try:
                await self.writer
            finally:
                self.writer=None

    def terminate(self):
        if self.writer:
            if self.loop.running:
                self.writer.cancel()
            self.writer=None

class ClientResponse:
    __slots__=('_released', 'body', 'closed', 'connection', 'payload_waiter',
        'cookies', 'headers', 'history', 'loop', 'method', 'status', 'timer', 'url', 'writer', 'raw_message')
       
    def __init__(self,method,url,loop,writer,timer):
        self.method         = method
        self.url            = url
        self.loop           = loop
        
        self.writer         = writer
        self.closed         = False # to allow __del__ for non-initialized properly response
        self.timer          = timer
        self.cookies        = SimpleCookie()
        self._released      = False
        
        self.body           = None
        self.status         = None  # Status-Code
        self.payload_waiter = None  # Data stream
        self.headers        = None  # Response headers, multidict_titled
        self.connection     = None  # current connection
        
        self.raw_message    = None
        self.history        = None  # will be added later
    
    @property
    def reason(self):
        message = self.raw_message
        if (message is not None):
            reason = message.reason
            if (reason is not None):
                return reason.decode()
        
    def __del__(self):
        if self.closed:
            return
        
        connection = self.connection
        if (connection is not None):
            connection.release()
            self._cleanup_writer()                
    
    def __repr__(self):
        ascii_encodable_url=str(self.url)
        
        return f'<{self.__class__.__name__}({ascii_encodable_url}) [{self.status} {self.reason!r}]>'
    
    async def start(self,connection):
        #Start response processing.
        self.closed=False
        self.connection=connection
        protocol=connection.protocol
        
        with self.timer:
            self.raw_message = message = await protocol.set_payload_reader(protocol.read_http_response())
            protocol.handle_payload_waiter_cancellation()
            payload_reader = protocol.get_payload_reader_task(message)
            if (payload_reader is None):
                payload_waiter = None
                self._response_eof(None)
            else:
                payload_waiter = protocol.set_payload_reader(payload_reader)
                payload_waiter.add_done_callback(self._response_eof)
        
        #response status
        self.status     = message.status
        #headers
        self.headers    = message.headers
        #owo
        self.payload_waiter    = payload_waiter
        
        # cookies
        for header in self.headers.getall(SET_COOKIE, ()):
            try:
                self.cookies.load(header)
            except CookieError: #so sad
                pass
        
        return self
    
    def _response_eof(self, future):
        if self.closed:
            return
        
        self.payload_waiter = None
        connection = self.connection
        if (connection is not None):
            # websocket, protocol could be None because connection could be detached
            if (connection.protocol is not None) and self.raw_message.upgraded:
                return
            
            connection.release()
            self.connection=None
        
        self.closed=True
        self._cleanup_writer()
    
    # If content is still present
    def _notify_content(self):
        payload_waiter = self.payload_waiter
        if (payload_waiter is not None):
            self.connection.protocol.set_exception(ConnectionError('Connection closed'))
        
        self._released = True
    
    def _cleanup_writer(self):
        writer = self.writer
        if (writer is not None):
            self.writer=None
            writer.cancel()
    
    async def read(self):
        payload_waiter = self.payload_waiter
        if (payload_waiter is None):
            body = self.body
        else:
            try:
                self.body = body = await payload_waiter
            finally:
                self.payload_waiter = None
        
        return body
    
    def get_encoding(self):
        ctype=self.headers.get(CONTENT_TYPE,'').lower()
        mimetype=MimeType(ctype)
        
        encoding=mimetype.params.get('charset',None)
        if encoding is not None:
            try:
                codecs.lookup(encoding)
            except LookupError:
                encoding=None
        if encoding is None:
            if mimetype.mtype=='application' and mimetype.stype=='json':
                encoding='utf-8' # RFC 7159 states that the default encoding is UTF-8.
            else:
                encoding=chardet.detect(self.body)['encoding']
        if not encoding:
            encoding='utf-8'
        
        return encoding
    
    async def text(self,encoding=None,errors='strict'):
        body = await self.read()
        if body is None:
            return
        
        if encoding is None:
            encoding = self.get_encoding()
        
        return body.decode(encoding,errors)
    
    async def json(self,encoding=None,loader=json.loads,content_type='application/json'):
        body = await self.read()
        if body is None:
            return
        
        if content_type is not None:
            ctype=self.headers.get(CONTENT_TYPE,'').lower()

            if content_type=='application/json':
                failed = (json_re.match(ctype) is None)
            else:
                failed = (content_type not in ctype)
            
            if failed:
                raise TypeError(f'Attempt to decode JSON with unexpected mimetype: {ctype}',self)

        stripped = body.strip()
        if not stripped:
            return None

        if encoding is None:
            encoding=self.get_encoding()

        return loader(stripped.decode(encoding))

    async def __aenter__(self):
        return self

    async def __aexit__(self,exc_type,exc_val,exc_tb):
        # similar to _RequestContextManager, we do not need to check
        # for exceptions, response object can closes connection
        # is state is broken
        self.release()

    def close(self):
        if not self._released:
            self._notify_content()
        
        if self.closed:
            return
        
        self.closed=True
        if not self.loop.running:
            return
        
        connection=self.connection
        if (connection is not None):
            connection.close()
            self.connection=None
        
        self._cleanup_writer()
    
    def release(self):
        if not self._released:
            self._notify_content()
        
        if self.closed:
            return
        self.closed=True
        
        connection=self.connection
        if (connection is not None):
            connection.release()
            self.connection=None
        
        self._cleanup_writer()
