# -*- coding: utf-8 -*-
import base64, binascii, json, os, re, mimetypes as mime_types, uuid, zlib
from io import StringIO, TextIOBase, BytesIO, BufferedRandom, IOBase, BufferedReader
from collections import deque
from urllib.parse import parse_qsl as parse_query_string_list, urlencode, urlencode as url_encode
from .quote import unquote

from .utils import imultidict, multidict
from .ios import AsyncIO

from .headers import CONTENT_DISPOSITION, CONTENT_ENCODING, CONTENT_LENGTH, CONTENT_TRANSFER_ENCODING, CONTENT_TYPE
from .helpers import content_disposition_header, CHAR, TOKEN
from .protocol import ZLIB_COMPRESSOR, BROTLI_COMPRESSOR
from .exceptions import ContentEncodingError

BIG_CHUNK_LIMIT = 1<<16
DEFAULT_CONTENT_TYPE = 'application/octet-stream'
    
VALID_TCHAR_RP = re.compile(br'\A[!#$%&\'*+\-.^_`|~\w]+\Z')
INVALID_QDTEXT_CHAR_RP = re.compile(br'[\x00-\x08\x0A-\x1F\x7F]')

def create_payload(data, kwargs):
    """
    Creates a new ``PayloadBase`` instance with the given parameters.
    
    Parameters
    ----------
    data : (`list` of ``PayloadBase`` instances), ``BodyPartReader``, `bytes`, `bytearray`, `memoryview`, `str`, \
            `BytesIO`, `StringIO`, `TextIOBase`, `BufferedReader`, `BufferedRandom`, `IOBase`, ``AsyncIO``, \
            `async-iterable` instance
    kwargs : `dict` of (`str`, (`None` or `str`)) items
        Keyword arguments for the payload.
    
    Returns
    -------
    payload : ``PayloadBase``
    
    Raises
    ------
    LookupError
        `payload` is not serializable.
    """
    data_type = data.__class__
    if issubclass(data_type, BodyPartReader):
        type_ = BodyPartReaderPayload
    elif issubclass(data_type, (bytes, bytearray, memoryview)):
        type_ = BytesPayload
    elif issubclass(data_type, str):
        type_ = StringPayload
    elif issubclass(data_type, BytesIO):
        type_ = BytesIOPayload
    elif issubclass(data_type, StringIO):
        type_ = StringIOPayload
    elif issubclass(data_type, TextIOBase):
        type_ = TextIOPayload
    elif issubclass(data_type, (BufferedReader, BufferedRandom)):
        type_ = BufferedReaderPayload
    elif issubclass(data_type, IOBase):
        type_ = IOBasePayload
    elif issubclass(data_type, AsyncIO):
        type_ = AsyncIOPayload
    elif hasattr(data_type, '__aiter__'):
        type_ = AsyncIterablePayload
    else:
        raise LookupError(data_type)
    
    return type_(data, kwargs)


class PayloadBase(object):
    """
    Base class for payloads.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data : (`list` of ``PayloadBase`` instances), ``BodyPartReader``, `bytes`, `bytearray`, `memoryview`, `str`, \
            `BytesIO`, `StringIO`, `TextIOBase`, `BufferedReader`, `BufferedRandom`, `IOBase`, ``AsyncIO``, \
            `async-iterable` instance
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : `imultidict` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    __slots__ = ('content_type', 'data', 'encoding', 'filename', 'headers', 'size', )
    def __init__(self, data, kwargs):
        """
        Creates a new ``PayloadBase`` instance.
        
        Parameters
        ----------
        data : (`list` of ``PayloadBase`` instances), ``BodyPartReader``, `bytes`, `bytearray`, `memoryview`, `str`, \
                `BytesIO`, `StringIO`, `TextIOBase`, `BufferedReader`, `BufferedRandom`, `IOBase`, ``AsyncIO``, \
                `async-iterable` instance
            The payload's data.
        kwargs : `dict` of (`str`, `Any`) items
            Additional keyword arguments.
        """
        self.data = data
        self.encoding = kwargs.get('encoding')
        self.filename = filename = kwargs.get('filename')
        self.size = None
        
        headers = imultidict()
        
        content_type = kwargs.get('content_type')
        if content_type is None:
            if filename is None:
                content_type = DEFAULT_CONTENT_TYPE
            else:
                mime = mime_types.guess_type(self.filename)[0]
                if mime is None:
                    content_type = DEFAULT_CONTENT_TYPE
                else:
                    content_type = mime
        
        headers[CONTENT_TYPE] = content_type
        
        headers_parameter = kwargs.get('headers')
        if (headers_parameter is not None) or  headers_parameter:
            headers.update(headers_parameter)
        
        self.headers = headers
        self.content_type = content_type
    
    def set_content_disposition(self, disposition_type, params, quote_fields=True):
        """
        Sets content disposition header to the payload.
        
        Parameters
        ----------
        disposition_type : `str`
            The disposition's type.
        params : `dict` of (`str`, `str`) items
            Additional parameters.
        quote_fields : `bool`
            Whether field values should be quoted.
        """
        headers = self.headers
        headers.pop_all(CONTENT_DISPOSITION, None)
        headers[CONTENT_DISPOSITION] = content_disposition_header(disposition_type, params, quote_fields=quote_fields)
    
    async def write(self, writer):
        """
        Writes the payload to the given http writer.
        
        This method is a coroutine.
        
        Parameters
        ----------
        writer : ``HTTPStreamWriter``
            Http writer to write the payload's data to.
        """
        pass

class BytesPayload(PayloadBase):
    """
    Payload class for `bytes-like` objects.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data : `bytes`, `bytearray`, `memoryview` instance
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    __slots__ = ()
    
    def __init__(self, data, kwargs):
        """
        Creates a new ``BytesPayload`` instance.
        
        Parameters
        ----------
        data : `bytes`, `bytearray`, `memoryview` instance
            The payload's data.
        kwargs : `dict` of (`str`, `Any`) items
            Additional keyword arguments.
        """
        kwargs.setdefault('content_type', DEFAULT_CONTENT_TYPE)
        
        PayloadBase.__init__(self, data, kwargs)
        
        self.size = len(data)
    
    async def write(self, writer):
        """
        Writes the payload to the given http writer.
        
        This method is a coroutine.
        
        Parameters
        ----------
        writer : ``HTTPStreamWriter``
            Http writer to write the payload's data to.
        """
        await writer.write(self.data)


class StringPayload(BytesPayload):
    """
    Payload class for `bytes-like` objects.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data : `bytes`
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    __slots__ = ()
    def __init__(self, data, kwargs):
        """
        Creates a new ``StringPayload`` instance.
        
        Parameters
        ----------
        data : `str` instance
            The payload's data.
        kwargs : `dict` of (`str`, `Any`) items
            Additional keyword arguments.
        """
        encoding = kwargs.get('encoding')
        content_type = kwargs.get('content_type')
        if encoding is None:
            if content_type is None:
                encoding = 'utf-8'
                content_type = 'text/plain; charset=utf-8'
                
                kwargs['content_type'] = content_type
            else:
                mime_type = MimeType(content_type)
                encoding = mime_type.params.get('charset', 'utf-8')
            
            kwargs['encoding'] = encoding
        
        else:
            if content_type is None:
                content_type = f'text/plain; charset={encoding}'
                kwargs['content_type'] = content_type
        
        data = data.encode(encoding)
        
        BytesPayload.__init__(self, data, kwargs)


class StringIOPayload(StringPayload):
    """
    Payload class for string io objects.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data : `bytes`
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    __slots__ = ()
    def __init__(self, data, kwargs):
        """
        Creates a new ``StringIOPayload`` instance.
        
        Parameters
        ----------
        data : `StringIO` instance
            The payload's data.
        kwargs : `dict` of (`str`, `Any`) items
            Additional keyword arguments.
        """
        data = data.read()
        StringPayload.__init__(self, data, kwargs)


class IOBasePayload(PayloadBase):
    """
    Payload class for `IOBase` instances.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data : `IOBase` instance
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    __slots__ = ()
    def __init__(self, data, kwargs):
        """
        Creates a new ``IOBasePayload`` instance.
        
        Parameters
        ----------
        data : `IOBase` instance
            The payload's data.
        kwargs : `dict` of (`str`, `Any`) items
            Additional keyword arguments.
        """
        if 'filename' not in kwargs:
            kwargs['filename'] = getattr(data, 'name', None)
        
        PayloadBase.__init__(self, data, kwargs)
        
        try:
            disposition  = kwargs['disposition']
        except KeyError:
            disposition = 'attachment'
        else:
            disposition = None
        
        if (disposition is not None):
            filename = self.filename
            if (filename is not None):
                self.set_content_disposition(disposition, {'filename': filename})
    
    async def write(self, writer):
        """
        Writes the payload to the given http writer.
        
        This method is a coroutine.
        
        Parameters
        ----------
        writer : ``HTTPStreamWriter``
            Http writer to write the payload's data to.
        """
        data = self.data
        try:
            while True:
                chunk = data.read(BIG_CHUNK_LIMIT)
                if chunk:
                    await writer.write(chunk)
                else:
                    break
        finally:
            data.close()


class TextIOPayload(IOBasePayload):
    """
    Payload class for `TextIOBase` instances.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data : `TextIOBase` instance
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    __slots__ = ()
    
    def __init__(self, data, kwargs):
        """
        Creates a new ``TextIOPayload`` instance.
        
        Parameters
        ----------
        data : `TextIOBase` instance
            The payload's data.
        kwargs : `dict` of (`str`, `Any`) items
            Additional keyword arguments.
        """
        encoding = kwargs.get('encoding')
        content_type = kwargs.get('content_type')
        if encoding is None:
            if content_type is None:
                encoding = 'utf-8'
                content_type = 'text/plain; charset=utf-8'
                
                kwargs['content_type'] = content_type
            else:
                mime_type = MimeType(content_type)
                encoding = mime_type.params.get('charset', 'utf-8')
            
            kwargs['encoding'] = encoding
        else:
            if content_type is None:
                content_type = f'text/plain; charset={encoding}'
                kwargs['content_type'] = content_type
        
        IOBasePayload.__init__(self, data, kwargs)
        
        try:
            size = os.fstat(data.fileno()).st_size - data.tell()
        except OSError:
            # `data.fileno()` is not supported. Example: `io.BufferedReader(io.BytesIO(b'data'))`
            size = None
        
        self.size = size
    
    async def write(self, writer):
        """
        Writes the payload to the given http writer.
        
        This method is a coroutine.
        
        Parameters
        ----------
        writer : ``HTTPStreamWriter``
            Http writer to write the payload's data to.
        """
        data = self.data
        try:
            while True:
                chunk = data.read(BIG_CHUNK_LIMIT)
                if chunk:
                    await writer.write(chunk.encode(self.encoding))
                else:
                    break
        finally:
            data.close()


class BytesIOPayload(IOBasePayload):
    """
    Payload class for `BytesIO` instances.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data : `BytesIO` instance
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    def __init__(self, data, kwargs):
        """
        Creates a new ``BytesIOPayload`` instance.
        
        Parameters
        ----------
        data : `BytesIO` instance
            The payload's data.
        kwargs : ``imultidict`` of (`str`, `str`) items
            Additional keyword arguments.
        """
        IOBasePayload.__init__(self, data, kwargs)
        
        position = data.tell()
        end = data.seek(0, os.SEEK_END)
        data.seek(position)
        self.size = end-position


class BufferedReaderPayload(IOBasePayload):
    """
    Payload class for `BufferedReader` and for `BufferedRandom` instances.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data : `BufferedReader`, `BufferedRandom` instance
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    __slots__ = ()
    def __init__(self, data, kwargs):
        """
        Creates a new ``BufferedReaderPayload`` instance.
        
        Parameters
        ----------
        data : `BufferedReader`, `BufferedRandom` instance
            The payload's data.
        kwargs : `dict` of (`str`, `Any`) items
            Additional keyword arguments.
        """
        IOBasePayload.__init__(self, data, kwargs)
        try:
            size = os.fstat(data.fileno()).st_size - data.tell()
        except OSError:
            # `data.fileno()` is not supported. Example: `io.BufferedReader(io.BytesIO(b'data'))`
            size = None
        
        self.size = size


class JsonPayload(BytesPayload):
    """
    Payload class for `json` data.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data :`bytes`
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    __slots__ = ()
    def __init__(self, data, kwargs):
        """
        Creates a new ``AsyncIterablePayload`` instance.
        
        Parameters
        ----------
        data : `None`, `str`, `int`, `float`, `list` of repeat, `dict` of (`str`, repeat) items
            The payload's data.
        kwargs : `dict` of (`str`, `Any`) items
            Additional keyword arguments.
        """
        encoding = kwargs.get('encoding')
        if (encoding is None):
            kwargs['encoding'] = encoding = 'utf-8'
        
        data = json.dumps(data).encode(encoding)
        
        kwargs.setdefault('content_type', 'application/json')
        BytesPayload.__init__(self, data, kwargs)


class AsyncIterablePayload(PayloadBase):
    """
    Payload class for `async-iterable`-s.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data :`async-iterable`
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    __slots__ = ('_iterator')
    
    def __init__(self, data, kwargs):
        """
        Creates a new ``AsyncIterablePayload`` instance.
        
        Parameters
        ----------
        data : `async-iterable`
            The payload's data.
        kwargs : `dict` of (`str`, `Any`) items
            Additional keyword arguments.
        """
        kwargs.setdefault('content_type', DEFAULT_CONTENT_TYPE)
        
        PayloadBase.__init__(self, data, kwargs)
        self._iterator = data.__class__.__aiter__(data)
    
    async def write(self, writer):
        """
        Writes the payload to the given http writer.
        
        This method is a coroutine.
        
        Parameters
        ----------
        writer : ``HTTPStreamWriter``
            Http writer to write the payload's data to.
        """
        iterator = self._iterator
        anext = iterator.__class__.__anext__
        try:
            while True:
                chunk = await anext(iterator)
                await writer.write(chunk)
        except StopAsyncIteration:
            self._iterator = None


class AsyncIOPayload(IOBasePayload):
    """
    Payload class for ``AsyncIO`` instances.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data :`async-iterable`
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    async def write(self, writer):
        """
        Writes the payload to the given http writer.
        
        This method is a coroutine.
        
        Parameters
        ----------
        writer : ``HTTPStreamWriter``
            Http writer to write the payload's data to.
        """
        data = self.data
        try:
            while True:
                chunk = await data.read(BIG_CHUNK_LIMIT)
                await writer.write(chunk)
                if len(chunk) < BIG_CHUNK_LIMIT:
                    break
        finally:
            data.close()


class BodyPartReaderPayload(PayloadBase):
    """
    Payload class for ``BodyPartReader``.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data :``BodyPartReader``
        The payload itself.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    """
    def __init__(self, data, kwargs):
        """
        Creates a new ``BodyPartReaderPayload`` instance.
        
        Parameters
        ----------
        data : ``BodyPartReader``
            The payload's data.
        kwargs : `dict` of (`str`, `Any`) items
            Additional keyword arguments.
        """
        PayloadBase.__init__(self, data, kwargs)
        
        params = {}
        name = data.name
        if (name is not None):
            params['name'] = name
        
        filename = data.filename
        if (filename is not None):
            params['filename'] = filename
        
        if params:
            self.set_content_disposition('attachment', params)
    
    async def write(self, writer):
        """
        Writes the payload to the given http writer.
        
        This method is a coroutine.
        
        Parameters
        ----------
        writer : ``HTTPStreamWriter``
            Http writer to write the payload's data to.
        """
        field = self.data
        while True:
            chunk = await field.read_chunk(size=65536)
            if chunk:
                await writer.write(field.decode(chunk))
            else:
                break

class MimeType(object):
    # Parses a MIME type into its components
    
    __slots__ = ('params', 'sub_type', 'suffix', 'type', )
    def __init__(self, mime_type):
        
        if (mime_type is None) or (not mime_type):
            self.type = ''
            self.sub_type = ''
            self.suffix = ''
            self.params = {}
            return
        
        parts = mime_type.split(';')
        params = multidict()
        for item in parts[1:]:
            if not item:
                continue
            if '=' in item:
                key, value = item.split('=', 1)
            else:
                key = item
                value = ''
            
            params[key.strip().lower()] = value.strip(' "')
        
        
        full_type = parts[0].strip().lower()
        if full_type == '*':
            full_type = '*/*'
        
        if '/' in full_type:
            type_, sub_type = full_type.split('/', 1)
        else:
            type_ = full_type
            sub_type = ''

        if '+' in sub_type:
            sub_type, suffix = sub_type.split('+', 1)
        else:
            suffix = ''
            
        self.type = type_
        self.sub_type = sub_type
        self.suffix = suffix
        self.params = params
    
    def __repr__(self):
        return (f'<{self.__class__.__name__} type={self.type!r} sub_type={self.sub_type!r} suffix={self.suffix!r} '
            f'params={self.params!r}>')

    __str__ = __repr__


def parse_content_disposition(header):
    def is_token(string):
        return string and TOKEN >= set(string)

    def is_quoted(string):
        return string[0] == string[-1] == '"'

    def is_rfc5987(string):
        return is_token(string) and string.count("'") == 2

    def is_extended_param(string):
        return string.endswith('*')

    def is_continuous_param(string):
        pos = string.find('*') + 1
        if not pos:
            return False
        substring = string[pos:-1] if string.endswith('*') else string[pos:]
        return substring.isdigit()

    def unescape(text, *, chars=''.join(map(re.escape, CHAR))):
        return re.sub(f'\\\\([{chars}])', '\\1', text)

    if not header:
        return None, {}

    disposition_type, *parts = header.split(';')
    if not is_token(disposition_type):
        return None, {}

    params = {}
    while parts:
        item = parts.pop(0)
        
        if '=' not in item:
            return None, {}
        
        key, value = item.split('=', 1)
        key = key.lower().strip()
        value = value.lstrip()
        
        if key in params:
            return None, {}
        
        if not is_token(key):
            continue
        
        elif is_continuous_param(key):
            if is_quoted(value):
                value = unescape(value[1:-1])
            elif not is_token(value):
                continue
        
        elif is_extended_param(key):
            if is_rfc5987(value):
                encoding, _, value = value.split("'", 2)
                encoding = encoding or 'utf-8'
            else:
                continue
            
            try:
                value = unquote(value, encoding, 'strict')
            except UnicodeDecodeError:
                continue
        
        else:
            failed = True
            
            if is_quoted(value):
                value = unescape(value[1:-1].lstrip('\\/'))
            elif is_token(value):
                failed = False
            elif parts:
                value_ = f'{value};{parts[0]}'
                if is_quoted(value_):
                    parts.pop(0)
                    value = unescape(value_[1:-1].lstrip('\\/'))
                    failed = False
            
            if failed:
                return None, {}
        
        params[key] = value
    
    return disposition_type.lower(), params


def content_disposition_filename(params,name='filename'):
    name_suf = f'{name}*'
    if not params:
        return None
    elif name_suf in params:
        return params[name_suf]
    elif name in params:
        return params[name]
    else:
        parts = []
        file_name_params = sorted((key, value) for key, value in params.items() if key.startswith('filename*'))
        for index, (key, value) in enumerate(file_name_params):
            _, tail = key.split('*', 1)
            if tail.endswith('*'):
                tail = tail[:-1]
            if tail == str(index):
                parts.append(value)
            else:
                break
        if not parts:
            return None
        value = ''.join(parts)
        if "'" in value:
            encoding, _, value = value.split("'", 2)
            encoding = encoding or 'utf-8'
            return unquote(value, encoding, 'strict')
        return value

# TODO
class BodyPartReader(object):
    # Multipart reader for single body part.
    __slots__ = ('headers', '_boundary', '_content', '_at_eof', '_length', '_read_bytes', '_unread', '_prev_chunk',
        '_content_eof', '_cache',)
    
    chunk_size = 8192
    
    def __init__(self, boundary, headers, content):
        self.headers = headers
        self._boundary = boundary
        self._content = content
        self._at_eof = False
        length = self.headers.get(CONTENT_LENGTH)
        self._length = None  if length is None else int(length)
        self._read_bytes = 0
        self._unread = deque()
        self._prev_chunk = None
        self._content_eof = 0
        self._cache = {}
        
    def __aiter__(self):
        return self

    async def __anext__(self):
        item = await self.read()
        if item:
            return item
        raise StopAsyncIteration

    async def next(self):
        item = await self.read()
        if not item:
            return None
        return item

    async def read(self, *, decode=False):
        # Reads body part data.
        #decode : `bool`, Optional : should decode data following by encoding method from `Content-Encoding` header.
        #     Defaults to `False`.
        if self._at_eof:
            return b''
        data = bytearray()
        while not self._at_eof:
            data.extend((await self.read_chunk(self.chunk_size)))
        if decode:
            return self.decode(data)
        return data
    
    async def read_chunk(self, size=chunk_size):
        # Reads body part content chunk of the specified size.
        if self._at_eof:
            return b''
        if self._length:
            chunk = await self._read_chunk_from_length(size)
        else:
            chunk = await self._read_chunk_from_stream(size)
        
        self._read_bytes += len(chunk)
        if self._read_bytes == self._length:
            self._at_eof = True
        if self._at_eof:
            await self._content.read_line()
        
        return chunk

    async def _read_chunk_from_length(self, size):
        # Reads body part content chunk of the specified size.
        chunk_size = min(size,self._length-self._read_bytes)
        chunk = await self._content.read(chunk_size)
        return chunk
    
    async def _read_chunk_from_stream(self, size):
        # Reads content chunk of body part with unknown length.
        first_chunk = self._prev_chunk is None
        if first_chunk:
            self._prev_chunk = await self._content.read(size)
        
        chunk = await self._content.read(size)
        self._content_eof += int(self._content.at_eof())
        
        window = self._prev_chunk + chunk
        sub = b'\r\n' + self._boundary
        
        if first_chunk:
            idx = window.find(sub)
        else:
            idx = window.find(sub, max(0, len(self._prev_chunk)-len(sub)))
        if idx >= 0:
            # pushing boundary back to content
            self._content.unread_data(window[idx:])
            if size > idx:
                self._prev_chunk = self._prev_chunk[:idx]
            chunk = window[len(self._prev_chunk):idx]
            if not chunk:
                self._at_eof = True
        result = self._prev_chunk
        self._prev_chunk = chunk
        return result
    
    async def read_line(self):
        if self._at_eof:
            return b''
        
        if self._unread:
            line = self._unread.popleft()
        else:
            line = await self._content.read_line()
        
        if line.startswith(self._boundary):
            # the very last boundary may not come with \r\n,
            # so set single rules for everyone
            separator_line = line.rstrip(b'\r\n')
            boundary = self._boundary
            last_boundary = self._boundary + b'--'
            #make sure that we read exactly the boundary, not something alike
            if separator_line == boundary or separator_line == last_boundary:
                self._at_eof = True
                self._unread.append(line)
                return b''
        else:
            next_line = await self._content.read_line()
            if next_line.startswith(self._boundary):
                line = line[:-2]  # strip CRLF but only once
            self._unread.append(next_line)
        
        return line

    async def release(self):
        # Like `.read`, but reads all the data.
        if self._at_eof:
            return
        
        while not self._at_eof:
            await self.read_chunk(self.chunk_size)
    
    async def text(self, *, encoding=None):
        # Like `.read`, but assumes that body part contains text data.
        # encoding : `str`, Optional : Custom text encoding. Overrides specified in charset param of `Content-Type`
        #     header
        
        data = await self.read(decode=True)
        # see https://www.w3.org/TR/html5/forms.html#multipart/form-data-encoding-algorithm
        # and https://dvcs.w3.org/hg/xhr/raw-file/tip/Overview.html#dom-xmlhttprequest-send
        encoding = encoding or self.get_charset(default='utf-8')
        return data.decode(encoding)

    async def json(self, *, encoding=None):
        # Like `.read`, but assumes that body parts contains JSON data.
        # encoding :`str`, Optional : Custom JSON encoding. Overrides specified in charset param of `Content-Type`
        #     header
        
        data = await self.read(decode=True)
        if not data:
            return None
        encoding = encoding or self.get_charset(default='utf-8')
        return json.loads(data.decode(encoding))
    
    async def form(self, *, encoding=None):
        # Like `.read`, but assumes that body parts contains form url_encoded data.
        # encoding : `str`, Optional : Custom form encoding. Overrides specified in charset param of `Content-Type`
        #     header
        data = await self.read(decode=True)
        if not data:
            return None
        encoding = encoding or self.get_charset(default='utf-8')
        return parse_query_string_list(data.rstrip().decode(encoding), keep_blank_values=True, encoding=encoding)

    def at_eof(self):
        #Returns True if the boundary was reached or False otherwise.

        return self._at_eof

    def decode(self, data):
        #Decodes data according the specified Content-Encoding
        #or Content-Transfer-Encoding headers value.
        
        #arguments: data=bytearray
        #raises RuntimeError if encoding is unknown.
        #returns bytes

        if CONTENT_TRANSFER_ENCODING in self.headers:
            data = self._decode_content_transfer(data)
        if CONTENT_ENCODING in self.headers:
            return self._decode_content(data)
        return data

    def _decode_content(self, data):
        encoding = self.headers[CONTENT_ENCODING].lower()

        if encoding == 'deflate':
            return zlib.decompress(data, -zlib.MAX_WBITS)
        elif encoding == 'gzip':
            return zlib.decompress(data, 16 + zlib.MAX_WBITS)
        elif encoding == 'identity':
            return data
        else:
            raise RuntimeError(f'unknown content encoding: {encoding}')

    def _decode_content_transfer(self, data):
        encoding = self.headers[CONTENT_TRANSFER_ENCODING].lower()

        if encoding == 'base64':
            return base64.b64decode(data)
        elif encoding == 'quoted-printable':
            return binascii.a2b_qp(data)
        elif encoding in ('binary', '8bit', '7bit'):
            return data
        else:
            raise RuntimeError(f'unknown content transfer encoding: {encoding}')

    def get_charset(self, default=None):
        #Returns charset parameter from Content-Type header or default.

        content_type = self.headers.get(CONTENT_TYPE, '')
        mime_type = MimeType(content_type)
        return mime_type.params.get('charset', default)

    @property
    def name(self):
        #Returns name specified in Content-Disposition header or None
        #if missed or header is malformed.
        _, params = parse_content_disposition(self.headers.get(CONTENT_DISPOSITION))
        return content_disposition_filename(params, 'name')
    
    @property
    def filename(self):
        #Returns filename specified in Content-Disposition header or None
        #if missed or header is malformed
        _, params = parse_content_disposition(self.headers.get(CONTENT_DISPOSITION))
        return content_disposition_filename(params, 'filename')


class MultipartWriter(PayloadBase):
    """
    Multipart body writer.
    
    Attributes
    ----------
    content_type : `None` or `str`
        The payload's content type.
    data : `list` of ``PayloadBase`` instances
        The contained payloads.
    filename : `None` or `str`
        The payload's file's name if applicable.
    encoding : `None` or`str`
        Encoding used to encode the payload's data.
    headers : ``imultidict`` of (`str`, `str`) items
        Payload specific headers.
    size : `None` or `int`
        The payload's size if applicable.
    _boundary : `bytes`
        Boundary to mark the payload's start and end.
    """
    __slots__ = ('_boundary', )
    
    def __init__(self, subtype='mixed', boundary=None):
        """
        Creates a new ``MultipartWriter`` instance with the given parameters.
        
        Parameters
        ----------
        subtype : `str`, Optional
            The subtype of the multipart writer. Defaults to `'mixed'`, but also can `'form-data'` for example.
        boundary : `Nome` or `str`, Optional
            Boundary to mark the payload's start and end. If not given or given as `None`, then is autogenerated.
        
        Raises
        ------
        UnicodeEncodeError
            `boundary` is given as `str`, but is not `ascii` encodable.
        ValueError
            `boundary` contains invalid character.
        """
        if (boundary is None):
            boundary = uuid.uuid4().hex.encode('ascii')
        else:
            try:
                boundary = boundary.encode('ascii')
            except UnicodeEncodeError as err:
                raise ValueError('boundary should contains ASCII only chars') from err
        
        # Refer to RFCs 7231, 7230, 5234.
        #
        # parameter      = token "=" ( token / quoted-string )
        # token          = 1*tchar
        # quoted-string  = DQUOTE *( qdtext / quoted-pair ) DQUOTE
        # qdtext         = HTAB / SP / %x21 / %x23-5B / %x5D-7E / obs-text
        # obs-text       = %x80-FF
        # quoted-pair    = "\" ( HTAB / SP / VCHAR / obs-text )
        # tchar          = "!" / "#" / "$" / "%" / "&" / "'" / "*"
        #                  / "+" / "-" / "." / "^" / "_" / "`" / "|" / "~"
        #                  / DIGIT / ALPHA
        #                  ; any VCHAR, except delimiters
        # VCHAR          = %x21-7E
        
        if VALID_TCHAR_RP.match(boundary) is None:
            if INVALID_QDTEXT_CHAR_RP.search(boundary) is not None:
                raise ValueError('Boundary value contains invalid characters.')
            
            # escape %x5C and %x22
            quoted_boundary = boundary.replace(b'\\', b'\\\\')
            quoted_boundary = quoted_boundary.replace(b'"', b'\\"')
            quoted_boundary = quoted_boundary.decode('ascii')
            quoted_boundary = f'"{quoted_boundary}"'
        else:
            quoted_boundary = boundary.decode('ascii')
        
        kwargs = {'content_type': f'multipart/{subtype}; boundary={quoted_boundary}'}
        
        PayloadBase.__init__(self, [], kwargs)
        
        self._boundary = boundary
        self.headers[CONTENT_TYPE] = self.content_type
    
    @property
    def boundary(self):
        """
        Returns the multipart writer's boundary as string.
        
        Returns
        -------
        boundary : `str`
        """
        return self._boundary.decode('ascii')
    
    def append(self, body_part, headers=None):
        """
        Adds a new body part to the ``MultipartWriter``.
        
        Parameters
        ----------
        body_part : ``PayloadBase``, ``BodyPartReader``, `bytes`, `bytearray`, `memoryview`, `BytesIO`, `StringIO`, \
            `TextIOBase`, `BufferedReader`, `BufferedRandom`, `IOBase`, ``AsyncIO``, `async-iterable` instance
        headers : `None` or ``imultidict`` of (`str`, `str`) items, Optional
            Optional headers for the field.
        
        Returns
        -------
        payload : ``PayloadBase``
            The created payload.
        
        Raises
        ------
        TypeError
            Cannot create payload from the given `body_part`.
        RuntimeError
            - The `payload`'s content has unknown content-encoding.
            - The `payload`'s content has unknown content-transfer-encoding.
        """
        if headers is None:
            headers = imultidict()
        
        if isinstance(body_part, PayloadBase):
            if (headers is not None):
                body_part.headers.update(headers)
            
            payload = body_part
        else:
            kwargs = {}
            if (headers is not None):
                kwargs['headers'] = headers
            
            try:
                payload = create_payload(body_part, kwargs)
            except LookupError as err:
                raise TypeError(f'Cannot create payload from: {body_part!r}') from err
        
        self.append_payload(payload)
        return payload
    
    def append_payload(self, payload):
        """
        Adds a payload to the multipart writer.
        
        Parameters
        ----------
        payload : ``PayloadBase`` instance
            The payload to add to the body.
        
        Raises
        ------
        RuntimeError
            - The `payload`'s content has unknown content-encoding.
            - The `payload`'s content has unknown content-transfer-encoding.
        """
        # content-type
        payload_headers = payload.headers
        if CONTENT_TYPE not in payload_headers:
            payload_headers[CONTENT_TYPE] = payload.content_type
        
        # content-encoding or compression
        try:
            content_encoding = payload_headers[CONTENT_ENCODING].lower()
        except KeyError:
            content_encoding = None
        else:
            if content_encoding in ('deflate', 'gzip', 'br', ):
                pass
            elif content_encoding in ('', 'identity'):
                content_encoding = None
            else:
                raise RuntimeError(f'Unknown content-encoding: {content_encoding!r}.')
        
        # te-encoding
        try:
            transfer_encoding = payload_headers[CONTENT_TRANSFER_ENCODING].lower()
        except KeyError:
            transfer_encoding = None
        else:
            if transfer_encoding == '':
                transfer_encoding = None
            elif transfer_encoding in ('base64', 'quoted-printable'):
                pass
            elif transfer_encoding == 'binary':
                transfer_encoding = None
            else:
                raise RuntimeError(f'Unknown content transfer encoding: {transfer_encoding!r}.')
        
        # Set size to payload headers if applicable.
        size = payload.size
        if (size is not None) and (content_encoding is None) and (transfer_encoding is None):
            payload_headers[CONTENT_LENGTH] = str(size)
        
        # Render headers.
        result = []
        extend = result.extend
        for k, v in payload_headers.items():
            extend((k, ': ', v, '\r\n'))
        
        result.append('\r\n')
        
        headers = ''.join(result).encode('utf-8')
        
        # Calculate new size.
        data = self.data
        if data:
            size = self.size
        else:
            size = 6+len(self._boundary)
            # b'--'+self._boundary+b'--\r\n'
        
        if (size is not None):
            if (content_encoding is not None) or (transfer_encoding is not None) or (payload.size is None):
                size = None
            else:
                size += 6+len(self._boundary)+payload.size+len(headers)
                # b'--'+self._boundary+b'\r\n' ... data ... b'\r\n'
            
            self.size = size
        
        # Add part.
        data.append((payload, headers, content_encoding, transfer_encoding))
    
    
    def append_json(self, obj, headers=None):
        """
        Helper method to add a json field.
        
        Parameters
        ----------
        obj : `None`, `str`, `int`, `float`, `list` of repeat, `dict` of (`str`, repeat) items
            The payload's data.
        headers : `None` or ``imultidict`` of (`str`, `str`) items, Optional
            Optional headers for the json field.

        Returns
        -------
        payload : ``JsonPayload``
            The created json payload.
        
        Raises
        ------
        RuntimeError
            - The `payload`'s content has unknown content-encoding.
            - The `payload`'s content has unknown content-transfer-encoding.
        """
        kwargs = {}
        if (headers is not None):
            kwargs['headers'] = headers
        
        payload = JsonPayload(obj, kwargs)
        self.append_payload(payload)
        return payload
    
    
    def append_form(self, obj, headers=None):
        """
        Helper method to add url_encoded field.
        
        Parameters
        ----------
        obj : `mapping` of (`str`, `Any`) items, `sequence` of `tuple` (`str`, `Any`) items
            The object, what should be percent encoded for a post request.
        headers : `None` or ``imultidict`` of (`str`, `str`) items, Optional
            Optional headers for the url_encoded field.
        
        Returns
        -------
        payload : ``StringPayload``
            The created string payload.
        
        Raises
        ------
        RuntimeError
            - The `payload`'s content has unknown content-encoding.
            - The `payload`'s content has unknown content-transfer-encoding.
        """
        if hasattr(obj.__class__, 'items'): # mapping type
            obj = list(obj.items())
        
        data = url_encode(obj, doseq=True)
        
        kwargs = {'content_type': 'application/x-www-form-url_encoded'}
        
        if (headers is not None):
            kwargs['headers'] = headers
        
        payload = StringPayload(data, kwargs)
        self.append_payload(payload)
        return payload
    
    
    async def write(self, writer, close_boundary=True):
        """
        Writes the payloads of the multipart writer to the given http writer.
        
        This method is a coroutine.
        
        Parameters
        ----------
        writer : ``HTTPStreamWriter``
            Http writer to write the payload's data to.
        close_boundary : `bool`, Optional
            Whether the multipart's payload should be closed with it's boundary.
        """
        data = self.data
        if not data:
            return
        
        for part, headers, content_encoding, transfer_encoding in data:
            await writer.write(b'--' + self._boundary + b'\r\n') # fb strings pls!
            await writer.write(headers)
            
            if (content_encoding is not None) or (transfer_encoding is not None):
                multipart_payload_writer = MultipartPayloadWriter(writer, content_encoding, transfer_encoding)
                
                await part.write(multipart_payload_writer)
                await multipart_payload_writer.write_eof()
            else:
                await part.write(writer)
            await writer.write(b'\r\n')
        
        if close_boundary:
            await writer.write(b'--'+self._boundary+b'--\r\n')


class MultipartPayloadWriter(object):
    __slots__ = ('compressor', 'encoding_buffer', 'transfer_encoding', 'writer',)
    
    def __init__(self, writer, content_encoding, transfer_encoding):
        
        if content_encoding == 'gzip':
            compressor = ZLIB_COMPRESSOR(wbits=16+zlib.MAX_WBITS)
        elif content_encoding == 'deflate':
            compressor = ZLIB_COMPRESSOR(wbits=-zlib.MAX_WBITS)
        elif content_encoding == 'br':
            if BROTLI_COMPRESSOR is None:
                raise ContentEncodingError('Can not decode content-encoding: brotli (br). Please install `brotlipy`.')
            compressor = BROTLI_COMPRESSOR()
        elif content_encoding == 'identity':
            # I assume this is no encoding
            compressor = None
        else:
            raise ContentEncodingError(f'Can not decode content-encoding: {content_encoding!r}.')
        
        if transfer_encoding == 'base64':
            transfer_encoding = transfer_encoding
            encoding_buffer = bytearray()
        else:
            if transfer_encoding == 'quoted-printable':
                transfer_encoding = transfer_encoding
            else:
                transfer_encoding = None
            encoding_buffer = None
        
        self.writer = writer
        self.transfer_encoding = transfer_encoding
        self.compressor = compressor
        self.encoding_buffer = encoding_buffer
    
    async def write_eof(self):
        compressor = self.compressor
        if (compressor is not None):
            self.compressor = None
            chunk = compressor.flush()
                
            if chunk:
                await self.write(chunk)
        
        if self.transfer_encoding == 'base64':
            encoding_buffer = self.encoding_buffer
            if encoding_buffer:
                await self.writer.write(base64.b64encode(encoding_buffer))
    
    async def write(self, chunk):
        compressor = self.compressor
        if (compressor is not None):
            if chunk:
                chunk = compressor.compress(chunk)
                if not chunk:
                    return
        
        transfer_encoding = self.transfer_encoding
        if transfer_encoding == 'base64':
            encoding_buffer = self.encoding_buffer
            encoding_buffer.extend(chunk)
            
            if encoding_buffer:
                barrier = (len(encoding_buffer)//3)*3
                if barrier:
                    encoding_chunk = encoding_buffer[:barrier]
                    del encoding_buffer[:barrier]
                    encoding_chunk = base64.b64encode(encoding_chunk)
                    await self.writer.write(encoding_chunk)
        
        elif transfer_encoding == 'quoted-printable':
            await self.writer.write(binascii.b2a_qp(chunk))
            
        else:
            await self.writer.write(chunk)


