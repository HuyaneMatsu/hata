# -*- coding: utf-8 -*-
import json, ssl, re, codecs
from http.cookies import SimpleCookie, CookieError, Morsel
from hashlib import md5, sha1, sha256

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

NoneType=type(None)

from .dereaddons_local import multidict_titled
from . import py_hdrs as hdrs
from .futures import Task
from .py_helpers import BasicAuth,EmptyTimer
from .py_multipart import MimeType,create_payload,payload_superclass
from .py_streams import StreamWriter
from .py_exceptions import HttpProcessingError,CancelledError,ResponseError
from .py_formdata import Formdata


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

SSL_ALLOWED_TYPES = (ssl.SSLContext, bool, Fingerprint, NoneType)

def merge_ssl_params(ssl,verify_ssl,ssl_context,fingerprint):
    if verify_ssl is not None and not verify_ssl:
        if ssl is not None:
            raise ValueError('verify_ssl, ssl_context, fingerprint and ssl parameters are mutually exclusive')
        else:
            ssl = False
    if ssl_context is not None:
        if ssl is not None:
            raise ValueError('verify_ssl, ssl_context, fingerprint and ssl parameters are mutually exclusive')
        else:
            ssl = ssl_context
    if fingerprint is not None:
        if ssl is not None:
            raise ValueError('verify_ssl, ssl_context, fingerprint and ssl parameters are mutually exclusive')
        else:
            ssl = Fingerprint(fingerprint)
    if not isinstance(ssl, SSL_ALLOWED_TYPES):
        raise TypeError(f'ssl should be SSLContext, bool, Fingerprint or None, \'got {ssl!r} instead.')
    return ssl

#the key should contain an information about used proxy / TLS
#to prevent reusing wrong connections from a pool
class ConnectionKey:
    __slots__=('host', 'is_ssl', 'port', 'proxy_auth', #'proxy_header_hash',
        'proxy_url', 'ssl',)

    def __init__(self,request):
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

class RequestInfo(object):
    __slots__=('headers', 'method', 'real_url', 'url',)
    def __init__(self,request):
        self.url                = request.url           #URL
        self.method             = request.method        #str
        self.headers            = request.headers       #multidict_titiled
        self.real_url           = request.original_url  #URL #maybe request.url is a default for this if this is None

    
class ClientRequest(object):
    GET_METHODS = {hdrs.METH_GET, hdrs.METH_HEAD, hdrs.METH_OPTIONS}
    POST_METHODS = {hdrs.METH_PATCH, hdrs.METH_POST, hdrs.METH_PUT}
    ALL_METHODS = GET_METHODS.union(POST_METHODS).union({hdrs.METH_DELETE, hdrs.METH_TRACE})

    DEFAULT_HEADERS = (
        (hdrs.ACCEPT,'*/*'),
        (hdrs.ACCEPT_ENCODING,'gzip, deflate'),
            )
    
    _default_encoding='utf-8'
    # N.B.
    # Adding __del__ method with self.writer closing doesn't make sense
    # because _writer is instance method, thus it keeps a reference to self.
    # Until writer has finished finalizer will not be called.

    __slots__=('auth', 'body', 'chunked', 'compress', 'encoding', 'headers',
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
        self.compress       = None
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
        if hdrs.HOST not in self.headers:
            netloc=self.url.raw_host
            if not self.url.is_default_port():
                netlock=f'{netloc}:{self.url.port}'
            self.headers[hdrs.HOST]=netloc
                
    def update_cookies(self, cookies):
        #Update request cookies header.
        if not cookies:
            return

        cookie=SimpleCookie()
        if hdrs.COOKIE in self.headers:
            cookie.load(self.headers.get(hdrs.COOKIE,''))
            del self.headers[hdrs.COOKIE]

        for key,value in cookies.items():
            if isinstance(key,Morsel):
                # Preserve coded_value
                mrsl_val=value.get(value.key,Morsel())
                mrsl_val.set(value.key,value.value,value.coded_value)
                cookie[key]=mrsl_val
            else:
                cookie[key]=value

        self.headers[hdrs.COOKIE] = cookie.output(header='', sep=';').strip()

    def update_content_encoding(self,data):
        #Set request content encoding.
        if not data:
            return

        encoding=self.headers.get(hdrs.CONTENT_ENCODING,'').lower()

        if self.compress:
            if encoding:
                raise ValueError('compress can not be set if Content-Encoding header is set')
            
            if not isinstance(self.compress, str):
                self.compress = 'deflate'
            self.headers[hdrs.CONTENT_ENCODING] = self.compress
            #enable chunked, no need to deal with length
            self.chunked = True


    def update_auth(self,auth):
        if auth is None:
            auth=self.auth
        if auth is None:
            return
            
        self.headers[hdrs.AUTHORIZATION]=auth.encode()


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
            if hdrs.CONTENT_LENGTH not in self.headers:
                size=data.size
                if size is None:
                    self.chunked=True
                else:
                    if hdrs.CONTENT_LENGTH not in self.headers:
                        self.headers[hdrs.CONTENT_LENGTH]=str(size)
                        
        if hdrs.CONTENT_TYPE not in self.headers:
            self.headers[hdrs.CONTENT_TYPE]=data.content_type

        if data.headers:
            for key,value in data.headers.items():
                if key not in self.headers:
                    self.headers[key]=value

    def update_transfer_encoding(self):
        #Analyze transfer-encoding header

        transfer_encoding = self.headers.get(hdrs.TRANSFER_ENCODING, '').lower()

        if 'chunked' in transfer_encoding:
            if self.chunked:
                raise ValueError('Chunked can not be set if "Transfer-Encoding: chunked" header is set.')

        elif self.chunked:
            if hdrs.CONTENT_LENGTH in self.headers:
                raise ValueError('Chunked can not be set if Content-Length header is set.')
            self.headers[hdrs.TRANSFER_ENCODING]='chunked'

        else:
            if hdrs.CONTENT_LENGTH not in self.headers:
                self.headers[hdrs.CONTENT_LENGTH]=str(len(self.body))


    def update_proxy(self,proxy_url,proxy_auth):
        if proxy_url:
            if proxy_auth.scheme!='http':
                raise ValueError('Only http proxies are supported')
            if not isinstance(proxy_auth,BasicAuth):
                raise ValueError('proxy_auth must be None or BasicAuth')
        self.proxy_url=proxy_url
        self.proxy_auth=proxy_auth

    def keep_alive(self):
        return self.headers.get(hdrs.CONNECTION)!='close'
    
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
        if self.method==hdrs.METH_CONNECT:
            path = f'{self.url.raw_host}:{self.url.port}'
        elif self.proxy_url and not self.is_ssl():
            path=str(self.url)
        else:
            path=self.url.raw_path
            if self.url.raw_query_string:
                path=f'{path}?{self.url.raw_query_string}'

        writer=StreamWriter(connection.protocol,self.loop)

        if self.compress:
            writer.enable_compression(self.compress)

        if self.chunked is not None:
            writer.enable_chunking()

        # set default content-type
        if (self.method in self.POST_METHODS) and (hdrs.CONTENT_TYPE not in self.headers):
            self.headers[hdrs.CONTENT_TYPE]='application/octet-stream'

        
        connection_type=self.headers.get(hdrs.CONNECTION)
           
        if not connection_type and not self.keep_alive():
            connection_type='close'
                
        if connection_type is not None:
            self.headers[hdrs.CONNECTION]=connection_type


        status_line=f'{self.method} {path} HTTP/1.1'

        
        await writer.write_headers(status_line,self.headers)

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
    __slots__=('_released', 'body', 'closed', 'connection', 'content',
        'cookies', 'headers', 'history', 'loop', 'method', 'raw_headers',
        'reason', 'status', 'timer', 'url', 'writer',)
       
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
        self.reason         = None  # Reason-Phrase
        self.content        = None  # Data stream
        self.headers        = None  # Response headers, multidict_titled
        self.raw_headers    = None  # Response raw headers, a sequence of pairs
        self.connection     = None  # current connection

        self.history        = None  # will be added later

    def __del__(self):
        if self.closed:
            return

        if self.connection is not None:
            self.connection.release()
            self._cleanup_writer()                

    def __repr__(self):
        ascii_encodable_url=str(self.url)
        if self.reason:
            ascii_encodable_reason=self.reason.encode('ascii','backslashreplace').decode('ascii')
        else:
            ascii_encodable_reason=self.reason
        return f'<{self.__class__.__name__}({ascii_encodable_url}) [{self.status} {ascii_encodable_reason}]>\n{self.headers!s}\n'     
        
    async def start(self,connection):
        #Start response processing.
        self.closed=False
        self.connection=connection
        protocol=connection.protocol

        with self.timer:
            while True:
                # read response
                try:
                    message,data = await protocol.read()
                except HttpProcessingError as err:
                    raise ResponseError( message=err.message,headers=err.headers) from err

                if (message.code<100 or message.code>199 or message.code==101):
                    break
        
        data.on_eof(self._response_eof)
        
        #response status
        self.status     = message.code
        self.reason     = message.reason
        #headers
        self.headers    = message.headers
        self.raw_headers= message.raw_headers
        #owo
        self.content    = data
        
        # cookies
        for header in self.headers.getall(hdrs.SET_COOKIE, ()):
            try:
                self.cookies.load(header)
            except CookieError: #so sad
                pass
        return self


    def _response_eof(self):
        if self.closed:
            return
        
        connection=self.connection
        if connection is not None:
            # websocket, protocol could be None because
            # connection could be detached
            if (connection.protocol is not None and connection.protocol.upgraded):
                return
            
            connection.release()
            self.connection=None

        self.closed=True
        self._cleanup_writer()

    def _notify_content(self):
        content = self.content
        if content and content.exception is None:
            content.set_exception(ConnectionError('Connection closed'))
        self._released = True

    def _cleanup_writer(self):
        writer=self.writer
        if writer is not None:
            writer.cancel()
            self.writer=None
        
    async def read(self):
        if self.body is None:
            try:
                self.body = await self.content.read()
            except BaseException:
                self.close()
                raise
        elif self._released:
            raise ConnectionError('Connection closed')

        return self.body


    def get_encoding(self):
        ctype=self.headers.get(hdrs.CONTENT_TYPE,'').lower()
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
        if self.body is None:
            await self.read()

        if encoding is None:
            encoding=self.get_encoding()

        return self.body.decode(encoding,errors)

        
    async def json(self,encoding=None,loader=json.loads,content_type='application/json'):
        if self.body is None:
            await self.read()

        if content_type is not None:
            ctype=self.headers.get(hdrs.CONTENT_TYPE,'').lower()

            if content_type=='application/json':
                failed = (json_re.match(ctype) is None)
            else:
                failed = (content_type not in ctype)
            
            if failed:
                raise TypeError(f'Attempt to decode JSON with unexpected mimetype: {ctype}',self)

        stripped = self.body.strip()
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
        if connection is not None:
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
        if connection is not None:
            connection.release()
            self.connection=None

        self._cleanup_writer()

class Request_CM(object):

    async def __aexit__(self,exc_type,exc_val,exc_tb):
        self.response.release()
    
    __slots__=('coroutine', 'response',)

    def __init__(self,coroutine):
        self.coroutine=coroutine

    def send(self,argument):
        return self.coroutine.send(argument)

    def throw(self,argument):
        return self.coroutine.throw(argument)

    def close(self):
        return self.coroutine.close()

    def __await__(self):
        result=self.coroutine.__await__()
        return result

    def __iter__(self):
        return self.__await__()

    async def __aenter__(self):
        self.response = await self.coroutine
        return self.response

del re
