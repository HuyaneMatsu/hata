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
        message = ('chardet (or cchardet) is not installed, please make sure it is installed before importing '
            f'{__spec__.parent}')
        
        err.args = (message,)
        err.msg = message
        raise err from None

from .utils import imultidict
from .futures import Task, CancelledError
from .headers import METHOD_POST_ALL, METHOD_CONNECT, SET_COOKIE, CONTENT_LENGTH, CONNECTION, ACCEPT, ACCEPT_ENCODING, \
    HOST, TRANSFER_ENCODING, COOKIE, CONTENT_ENCODING, AUTHORIZATION, CONTENT_TYPE
from .helpers import BasicAuth
from .multipart import MimeType, create_payload
from .formdata import Formdata
from .protocol import HTTPStreamWriter

json_re = re.compile(r'^application/(?:[\w.+-]+?\+)?json')

class Fingerprint(object):
    """
    HTTP fingerprinting can be used to automate information systems and security audits. Automated security testing
    tools can use HTTP fingerprinting to narrow down the set of tests required, based on the specific platform or the
    specific web server being audited.
    
    Attributes
    ----------
    fingerprint : `bytes`
        The fingerprint's value.
    hash_function : `function`
        Hash function used by the fingerprint.
    
    Class Attributes
    ----------------
    HASH_FUNCTION_BY_DIGEST_LENGTH : `dict` of (`int`, `function`) items
        `fingerprint`'s length - `hash-function` relation mapping.
    """
    __slots__ = ('fingerprint', 'hash_function',)
    
    HASH_FUNCTION_BY_DIGEST_LENGTH = {
        16: md5,
        20: sha1,
        32: sha256,
            }
    
    def __new__(cls, fingerprint):
        """
        Creates a new ``Fingerprint`` instance with the given parameters.
        
        Parameters
        ----------
        fingerprint : `bytes`
            Fingerprint value.
        
        Raises
        ------
        ValueError
            - If `fingerprint`'s length is not any of the expected ones.
            - If the detected `hash_function` is `md5` or `sha1`.
        """
        fingerprint_length = len(fingerprint)
        
        try:
            hash_function = cls.HASH_FUNCTION_BY_DIGEST_LENGTH[fingerprint_length]
        except KeyError:
            raise ValueError(f'`fingerprint` has invalid length, got {fingerprint_length!r}, {fingerprint!r}') from None
        
        if hash_function is md5 or hash_function is sha1:
            raise ValueError('`md5` and `sha1` are insecure and not supported, use `sha256`.')
        
        self = object.__new__(cls)
        self.hash_function = hash_function
        self.fingerprint = fingerprint
        return self

    def check(self, transport):
        """
        Checks whether the given transport's ssl data matches the fingerprint.
        
        Parameters
        ----------
        transport : `Any`
            Asynchronous transport implementation.
        
        Raises
        ------
        ValueError
            If the fingerprint don't match.
        """
        if transport.get_extra_info('sslcontext') is None:
            return
        
        ssl_object = transport.get_extra_info('ssl_object')
        cert = ssl_object.getpeercert(binary_form=True)
        received = self.hash_function(cert).digest()
        fingerprint = self.fingerprint
        if received == fingerprint:
            return
            
        host, port, *_ = transport.get_extra_info('peername')
        raise ValueError(f'The expected fingerprint: {fingerprint!r} not matches the received; received={received!r}, '
            f'host={host!r}, port={port!r}.')

if module_ssl is None:
    SSL_ALLOWED_TYPES = (type(None), )
else:
    SSL_ALLOWED_TYPES = (module_ssl.SSLContext, bool, Fingerprint, type(None))


class ConnectionKey(object):
    """
    Contains information about a host, like proxy, TLS to prevent reusing wrong connections from the pool.
    
    Attributes
    ----------
    host : `str`
        The host's ip address.
    is_ssl : `bool`
        Whether the connection is secure.
    port : `int`
        The host's port.
    proxy_auth : `None` or ``BasicAuth``
        Proxy authorization.
    proxy_url : `None` or ``URL``
        Proxy's url.
    ssl : `None`, ``SSLContext``, `bool`, ``Fingerprint``
        The connection's ssl type.
    """
    __slots__  = ('host', 'is_ssl', 'port', 'proxy_auth',  'proxy_url', 'ssl',) # + 'proxy_header_hash',
    
    def __init__(self, request):
        # proxy_headers = request.proxy_headers
        # if request.proxy_headers is not None:
        #     proxy_header_hash = hash(tuple(proxy_headers.items()))
        # else:
        #     proxy_header_hash = None
        
        self.host = request.host
        self.port = request.port
        self.is_ssl = request.is_ssl()
        self.ssl = request.ssl
        self.proxy_auth = request.proxy_auth
        self.proxy_url = request.proxy_url
        # self.proxy_header_hash = proxy_header_hash
    
    def __repr__(self):
        """Returns the connection key's representation."""
        return f'<{self.__class__.__name__} host={self.host!r}, port={self.port!r}>'
    
    def __eq__(self, other):
        """Returns whether the two connection keys are equal."""
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
        """Returns the connection key's hash value."""
        return hash(self.host) ^ (self.port << 17) ^ hash(self.is_ssl) ^ hash(self.ssl) ^ hash(self.proxy_auth) ^ \
               hash(self.proxy_url)

class RequestInfo(object):
    """
    Base information representing a request.
    
    Attributes
    ----------
    headers : ``imultidict``
        The respective request's headers.
    method : `str`
        The respective request's method.
    real_url : ``URL``
        The url given to request.
    url : ``URL``
        The requested url without fragments. Can be same as ``.real_url``.
    """
    __slots__ = ('headers', 'method', 'real_url', 'url',)
    def __init__(self, request):
        """
        Creates a new ``RequestInfo`` instance representing the given request.
        
        Parameters
        ----------
        request : ``ClientRequest``
            The represented request.
        """
        self.url = request.url
        self.method = request.method
        self.headers = request.headers
        self.real_url = request.original_url
    
    def __repr__(self):
        """Returns the request info's representation."""
        return f'<{self.__class__.__name__} url={self.url!r}>'


DEFAULT_HEADERS = (
    (ACCEPT, '*/*'),
    (ACCEPT_ENCODING, 'gzip, deflate'),
        )

class ClientRequest(object):
    """
    Http request class used by ``HTTPClient``.
    
    Attributes
    ----------
    auth : `None` or ``BasicAuth``
        Authorization sent with the request.
    body : `None`, ``PayloadBase`` instance
        The request's body.
    chunked : `bool`
        Whether the request is sent chunked.
    compression : `None` or `str`
        Compression used when sending the request.
    headers : `imultidict`
        The headers of the request.
    loop : ``EventThread``
        The event loop, trough what the request is executed.
    method : `str`
        The request's method.
    original_url : ``URL``
        The original url, what was asked to request.
    proxy_auth : `None` or ``BasicAuth``
        Proxy authorization sent with the request.
    proxy_url : `None` or ``URL``
        Proxy url to use if applicable.
    response : `None` or ``ClientResponse``
        Object representing the received response. Set as `None` till ``.send`` finishes.
    ssl : `None` `None`, ``SSLContext``, `bool`, ``Fingerprint``
        The connection's ssl type.
    url : ``URL``
        The url, what will be requested.
    writer : `None` or ``Task`` of ``.write_bytes``
        Payload writer task, what is present meanwhile the request's payload is sending.
    """
    __slots__ = ('auth', 'body', 'chunked', 'compression', 'headers', 'loop', 'method', 'original_url', 'proxy_auth',
        'proxy_url', 'response', 'ssl', 'url', 'writer',)
    
    def __new__(cls, loop, method, url, headers, data, params, cookies, auth, proxy_url, proxy_auth, ssl):
        """
        Creates a new ``ClientRequest`` instance with the given parameters.
        
        Parameters
        ----------
        loop : ``EventThread``
            The event loop, trough what the request is executed.
        method : `str`
            The request's method.
        url : ``URL``
            The url to request.
        headers : `None`, `dict` or ``imultidict``, Optional
            Headers of the request.
        data : `None`, `bytes-like`, `io-like`, ``FormData`, Optional
            Data to send as the request's body.
        params : `dict` of (`str`, (`str`, `int`, `float`, `bool`)) items
            Query string parameters.
        cookies : `None` or ``CookieJar``
            Cookies OwO.
        auth : `None` or ``BasicAuth``
            Authorization sent with the request.
        proxy_url : `None` or ``URL``
            Proxy url to use if applicable.
        proxy_auth : `None` or ``BasicAuth``
            Proxy authorization sent with the request.
        ssl : `None` `None`, ``SSLContext``, `bool`, ``Fingerprint``
            The connection's ssl type.
        
        Raises
        ------
        TypeError
            - `proxy_auth`'s type is incorrect.
            - ˙Cannot serialize a field of the given `data`.
        ValueError
            - Host could not be detected from `url`.
            - The `proxy_url`'s scheme is not `http`.
            - `compression` and `Content-Encoding` would be set at the same time.
            - `chunked` cannot be set, because `Transfer-Encoding: chunked` is already set.
            - `chunked` cannot be set, because `Content-Length` header is already present.
        RuntimeError
            - If one of `data`'s field's content has unknown content-encoding.
            - If one of `data`'s field's content has unknown content-transfer-encoding.
        """
        # Convert headers
        headers = imultidict(headers)
        
        # Add extra query parameters to the url and remove fragments
        url = url.extend_query(params)
        request_url = url.with_fragment(None)
        
        if not url.host:
            raise ValueError('Host could not be detected.')
        
        # Check authorization
        if auth is None:
            # If authorization is given, try to detect from url.
            username = url.user
            password = url.password
            
            if (username is not None) and username:
                if password is None:
                    password = ''
                
                auth = BasicAuth(username, password)
        
        # Store auth in headers is applicable.
        if (auth is not None):
            headers[AUTHORIZATION] = auth.encode()
        
        for key, value in DEFAULT_HEADERS:
            headers.setdefault(key, value)
        
        # Add host to headers if not present.
        if HOST not in headers:
            netloc = request_url.raw_host
            if not request_url.is_default_port():
                netloc = f'{netloc}:{request_url.port}'
            
            headers[HOST] = netloc
        
        # Update cookies
        if (cookies is not None) and cookies:
            cookie = SimpleCookie()
            if COOKIE in headers:
                cookie.load(headers.get(COOKIE, ''))
                del headers[COOKIE]
            
            for key, value in cookies.items():
                if isinstance(key, Morsel):
                    # Preserve coded_value
                    try:
                        morsel_value = value.get(value.key)
                    except KeyError:
                        morsel_value = Morsel()
                    
                    morsel_value.set(value.key, value.value, value.coded_value)
                    value = morsel_value
                
                cookie[key] = value
            
            headers[COOKIE] = cookie.output(header='', sep=';').strip()
        
        # Check proxy settings.
        if proxy_url is not None:
            if proxy_auth.scheme != 'http':
                raise ValueError(f'Only http proxies are supported, got {proxy_url!r}.')
            
            if (proxy_auth is not None):
                proxy_auth_type = proxy_auth.__class__
                if proxy_auth_type is not BasicAuth:
                    raise TypeError(f'`proxy_auth` must be `None` or `{BasicAuth.__name__}`, got '
                        f'{proxy_auth_type.__name__}.')
        
        # Needed for transfer data checks
        chunked = True
        compression = headers.get(CONTENT_ENCODING)
        
        # Get request content encoding.
        if (data is not None):
            if data:
                if (compression is not None):
                    if headers.get(CONTENT_ENCODING, ''):
                        raise ValueError('Compression can not be set if `Content-Encoding` header is set.')
                    
                    chunked = True
                
                # formdata
                if isinstance(data, Formdata):
                    data = data()
                else:
                    try:
                        data = create_payload(data, {'disposition': None})
                    except LookupError:
                        data = Formdata.from_fields(data)()
                
                if not chunked:
                    if CONTENT_LENGTH not in headers:
                        size = data.size
                        if size is None:
                            chunked = True
                        else:
                            if CONTENT_LENGTH not in headers:
                                headers[CONTENT_LENGTH] = str(size)
                
                if CONTENT_TYPE not in headers:
                    headers[CONTENT_TYPE] = data.content_type
                
                if data.headers:
                    for key, value in data.headers.items():
                        headers.setdefault(key, value)
            else:
                data = None
        
        # Analyze transfer-encoding header.
        transfer_encoding = headers.get(TRANSFER_ENCODING, '').lower()
        
        if 'chunked' in transfer_encoding:
            if chunked:
                raise ValueError('Chunked can not be set if `Transfer-Encoding: chunked` header is already set.')
        
        elif chunked:
            if CONTENT_LENGTH in headers:
                raise ValueError('Chunked can not be set if `Content-Length` header is set.')
            headers[TRANSFER_ENCODING] = 'chunked'
        
        else:
            if CONTENT_LENGTH not in headers:
                headers[CONTENT_LENGTH] = '0' if data is None else str(len(data))
        
        # Set default content-type.
        if (method in METHOD_POST_ALL) and (CONTENT_TYPE not in headers):
            headers[CONTENT_TYPE] = 'application/octet-stream'
        
        # Everything seems correct, create the object.
        self = object.__new__(cls)
        
        self.original_url = url
        self.url = request_url
        self.method = method
        self.loop = loop
        self.ssl = ssl
        self.chunked = chunked
        self.compression = compression
        self.body = data
        self.auth = auth
        self.writer = None
        self.response = None
        self.headers = headers
        self.proxy_url = proxy_url
        self.proxy_auth = proxy_auth
        
        return self
    
    def is_ssl(self):
        """
        Returns whether the request is ssl.
        
        Returns
        -------
        is_ssl : `bool`
        """
        return self.url.scheme in ('https', 'wss')
    
    @property
    def connection_key(self):
        """
        Returns the connection key of request.
        
        Returns
        -------
        connection_key : ``ConnectionKey``
        """
        return ConnectionKey(self)
    
    @property
    def request_info(self):
        """
        Returns base information representing the request.
        
        Returns
        -------
        request_info : ``RequestInfo``
        """
        return RequestInfo(self)
    
    @property
    def host(self):
        """
        Returns the request's host.
        
        Returns
        -------
        host : `str`
        """
        return self.url.host
    
    @property
    def port(self):
        """
        Returns the request's port.
        
        Returns
        -------
        port : `int`
        """
        return self.url.port
    
    async def write_bytes(self, writer, connection):
        """
        Writes the request's body..
        
        This method is a coroutine.
        
        Parameters
        ----------
        writer : ``HTTPStreamWriter``
            Writer used to write the request's body into the connection's transport.
        connection : ``Connection``
            Connection of the request with what the payload is sent.
        """
        # Support coroutines that yields bytes objects.
        try:
            body = self.body
            if (body is not None):
                await self.body.write(writer)
            await writer.write_eof()
        except OSError as err:
            new_err = OSError(err.errno, f'Can not write request body for {self.url!r}.')
            new_err.__context__ = err
            new_err.__cause__ = err
            connection.protocol.set_exception(new_err)
        except CancelledError as err:
            if not connection.closed:
               connection.protocol.set_exception(err)
        except BaseException as err:
            connection.protocol.set_exception(err)
            raise
        finally:
            self.writer = None
    
    def send(self, connection):
        """
        Sends the request.
        
        Parameters
        ----------
        connection : ``Connection``
            Connection, what is used to send the request.
        
        Returns
        -------
        response : `coroutine` of ``ClientResponse.start`` ->
        """
        try:
            url = self.url
            if self.method == METHOD_CONNECT:
                path = f'{url.raw_host}:{url.port}'
            elif (self.proxy_url is not None) and (not self.is_ssl()):
                path = str(url)
            else:
                path = url.raw_path
                if url.raw_query_string:
                    path = f'{path}?{url.raw_query_string}'
            
            protocol = connection.protocol
            writer = HTTPStreamWriter(protocol, self.compression, self.chunked)
            
            protocol.write_http_request(self.method, path, self.headers)
            
            self.writer = Task(self.write_bytes(writer, connection), self.loop)
            
            self.response = response = ClientResponse(self, connection)
            
            return response.start()
        
        except:
            connection.close()
            raise
    
    def terminate(self):
        """
        Terminates the request's writing task if applicable.
        """
        writer = self.writer
        if (writer is not None):
            self.writer = None
            writer.cancel()


class ClientResponse(object):
    """
    Http response class used by ``HTTPClient``.
    
    Attributes
    ----------
    _released : `bool`
        Whether the connection is released.
    body : `None` or `bytes`
        The received response body. Set as `None` if the response body is not yet received, or if it is empty.
    closed : `bool`
        Whether the response is closed.
    connection : `None` or ``Connection``
        Connection used to receive the request response. Set as `None` if the response is ``.close``-d or
        ``.release``-d.
    payload_waiter : `None` or ``Future``
        Future used to retrieve the response's body. It's result is set, when the respective protocol's reader task
        finished.
    cookies : `http.cookies.SimpleCookie`
        Received cookies with the response.
    headers : `None` or ``imultidict``
        Headers of the response. Set when the http response is successfully received.
    history : `None` or `tuple` of ``ClientResponse``
        Response history. Set as `tuple` of responses from outside.
    loop : ``EventThread``
        The event loop, trough what the request is executed.
    method : `str`
        Method of the respective request.
    status : `None` or `int`
        Received status code. Set as `0` by default.
    url : ``URL``
        The requested url.
    writer : ``Task`` of ``ClientRequest.write_bytes``
        Payload writer task of the respective request.
    raw_message : `None` or ``RawResponseMessage``
        Raw received http response.
    """
    __slots__ = ('_released', 'body', 'closed', 'connection', 'payload_waiter', 'cookies', 'headers', 'history', 'loop',
        'method', 'status', 'url', 'writer', 'raw_message')
       
    def __new__(cls, request, connection):
        """
        Crates a new ``ClientResponse`` instance from the given request and connection.
        
        Parameters
        ----------
        request : ``ClientRequest``
            The respective request.
        connection : ``Connection``
            The connection used to send the request and receive the response.
        """
        self = object.__new__(cls)
        self.loop = request.loop
        self.method = request.method
        self.url = request.original_url
        
        self.writer = request.writer
        self.closed = False
        self.cookies = SimpleCookie()
        self._released = False
        
        self.body = None
        self.status = 0
        self.payload_waiter = None
        self.headers = None
        self.connection = connection
        
        self.raw_message = None
        self.history = None  # will be added later
        
        return self
    
    @property
    def reason(self):
        """
        Returns the server response reason.
        
        reason : `str` or `None`
        """
        message = self.raw_message
        if (message is not None):
            reason = message.reason
            if (reason is not None):
                return reason.decode()
    
    def __del__(self):
        """releases the response if not yet closed."""
        if self.closed:
            return
        
        self._release_connection()
    
    def __repr__(self):
        """Returns the response's representation."""
        ascii_encodable_url = str(self.url)
        
        return f'<{self.__class__.__name__}({ascii_encodable_url}) [{self.status} {self.reason!r}]>'
    
    async def start(self,):
        """
        Starts response processing.
        
        This method is a coroutine.
        
        Returns
        -------
        self : ``ClientResponse``
        """
        try:
            protocol = self.connection.protocol
            
            payload_waiter = protocol.set_payload_reader(protocol._read_http_response())
            self.raw_message = message = await payload_waiter
            protocol.handle_payload_waiter_cancellation()
            payload_reader = protocol.get_payload_reader_task(message)
            if (payload_reader is None):
                payload_waiter = None
                self._response_eof(None)
            else:
                payload_waiter = protocol.set_payload_reader(payload_reader)
                payload_waiter.add_done_callback(self._response_eof)
            
            # response status
            self.status = message.status
            # headers
            self.headers = message.headers
            # OwO
            self.payload_waiter = payload_waiter
            
            # cookies
            for header in self.headers.get_all(SET_COOKIE, ()):
                try:
                    self.cookies.load(header)
                except CookieError: # so sad
                    pass
        except:
            self.close()
            raise
        
        return self
    
    def _response_eof(self, future):
        """
        Future callback added to the payload waiter future, to release the used connection.
        
        Parameters
        ----------
        future : ``Future``
            ``.payload_waiter`` future.
        """
        if self.closed:
            return
        
        self.payload_waiter = None
        
        connection = self.connection
        if (connection is not None):
            # Websocket, protocol could be `None`, because connection could be detached.
            if (connection.protocol is not None) and self.raw_message.upgraded:
                return
            
            self._release_connection()
        
        self.closed = True
        self._cleanup_writer()
    
    def _release_connection(self):
        """
        Releases the response's connection.
        
        If the connection type is "close", closes the protocol as well.
        """
        connection = self.connection
        if connection is None:
            return
        
        headers = self.headers
        if (headers is not None):
            try:
                connection_type = headers[CONNECTION]
            except KeyError:
                pass
            else:
                if connection_type == 'close':
                    protocol = connection.protocol
                    if (protocol is not None):
                        protocol.close()
        
        connection.release()
        self.connection = None
    
    def _notify_content(self):
        """
        Called when response reading is cancelled or released. Sets `ConnectionError` to the respective protocol if
        the payload is still reading.
        """
        payload_waiter = self.payload_waiter
        if (payload_waiter is not None):
            connection = self.connection
            if (connection is not None):
                connection.protocol.set_exception(ConnectionError('Connection closed.'))
        
        self._released = True
    
    def _cleanup_writer(self):
        """
        Cancels the writer task of the respective request. Called when the response is cancelled or released, or if
        reading the whole response is done.
        """
        writer = self.writer
        if (writer is not None):
            self.writer = None
            writer.cancel()
    
    async def read(self):
        """
        Reads the response's body.
        
        This method is a coroutine.
        
        Returns
        -------
        body : `bytes`
        """
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
        """
        Gets the encoding of the response's body.
        
        Returns
        -------
        encoding : `str`
            Defaults to `'utf-8'`.
        """
        content_type = self.headers.get(CONTENT_TYPE, '').lower()
        mime_type = MimeType(content_type)
        
        encoding = mime_type.params.get('charset')
        if encoding is not None:
            try:
                codecs.lookup(encoding)
            except LookupError:
                encoding = None
        
        if encoding is None:
            if mime_type.type == 'application' and mime_type.sub_type == 'json':
                encoding = 'utf-8' # RFC 7159 states that the default encoding is UTF-8.
            else:
                encoding = chardet.detect(self.body)['encoding']
        
        if not encoding:
            encoding = 'utf-8'
        
        return encoding
    
    async def text(self, encoding=None, errors='strict'):
        """
        Loads the response's content as text.
        
        This method is a coroutine.
        
        Parameters
        ----------
        encoding : `None` or `str`, Optional
            If no encoding is given, then detects it from the payload-
        errors : `str`, Optional
            May be given to set a different error handling scheme. The default `errors` value is `'strict'`, meaning
            that encoding errors raise a `UnicodeError`. Other possible values are `'ignore'`, `'replace'`,
            `'xmlcharrefreplace'`, `'backslashreplace'` and any other name registered via `codecs.register_error()`.
        
        Returns
        -------
        text : `str`
        """
        body = await self.read()
        if body is None:
            return
        
        if encoding is None:
            encoding = self.get_encoding()
        
        return body.decode(encoding, errors)
    
    async def json(self, encoding=None, loader=json.loads, content_type='application/json'):
        """
        Loads the response's content as a json.
        
        This method is a coroutine.
        
        Parameters
        ----------
        encoding : None` or `str`, Optional
            Encoding to use instead of the response's. If given as `None` (so by default), then will use the response's
            own encoding.
        loader : `callable`, Optional
            Json loader. Defaults to json.loads`.
        content_type : `str`, Optional
            Content type to use instead of the default one. Defaults to `'application/json'`.
        
        Returns
        -------
        json : `Any`
        
        Raises
        ------
        TypeError
            If the response's mime_type do not match.
        """
        body = await self.read()
        if body is None:
            return
        
        if content_type is not None:
            received_content_type = self.headers.get(CONTENT_TYPE, '').lower()
            
            if (json_re.match(received_content_type) is None) if (content_type == 'application/json') else \
                    (content_type not in received_content_type):
                raise TypeError(f'Attempt to decode JSON with unexpected mime_type: {received_content_type!r}.')
        
        stripped = body.strip()
        if not stripped:
            return None
        
        if encoding is None:
            encoding = self.get_encoding()
        
        return loader(stripped.decode(encoding))
    
    async def __aenter__(self):
        """
        Enters the client response as an asynchronous context manager.
        
        This method is a coroutine.
        """
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the response if not yet closed.
        
        This method is a coroutine.
        """
        self.release()
        return False

    def close(self):
        """
        Closes the response and it's connection. The used connection will not be reused after.
        """
        if not self._released:
            self._notify_content()
        
        if self.closed:
            return
        
        self.closed = True
        
        connection = self.connection
        if (connection is not None):
            self.connection = None
            connection.close()
        
        self._cleanup_writer()
    
    def release(self):
        """
        Releases the response and it's connection. The used connection might be reused after.
        """
        if not self._released:
            self._notify_content()
        
        if self.closed:
            return
        
        self.closed = True
        
        self._release_connection()
        self._cleanup_writer()
