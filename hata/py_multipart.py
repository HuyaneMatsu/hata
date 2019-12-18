# -*- coding: utf-8 -*-
import base64
import binascii
from io import StringIO,TextIOBase,BytesIO,BufferedRandom,IOBase,BufferedReader
import json
import mimetypes
import os
import re
import uuid
import zlib
from collections import deque
from urllib.parse import parse_qsl, unquote, urlencode

from .dereaddons_local import multidict_titled, multidict
from .ios import AsyncIO
from .py_hdrs import CONTENT_DISPOSITION,CONTENT_ENCODING,CONTENT_LENGTH,CONTENT_TRANSFER_ENCODING,CONTENT_TYPE
from .py_parsers import HttpParser
from .py_streams import DEFAULT_LIMIT, StreamReader
from .py_helpers import content_disposition_header,CHAR,TOKEN,sentinel

################X#X   py payload X#X################
#thesse both need to be at the same file, because of the scopes

BIG_CHUNK_LIMIT=1<<16

def create_payload(data,*args,**kwargs):
    if isinstance(data,BodyPartReader):
        type_=BodyPartReaderPayload
    elif isinstance(data,(bytes, bytearray, memoryview)):
        type_=BytesPayload
    elif isinstance(data,str):
        type_=StringPayload
    elif isinstance(data,BytesIO):
        type_=BytesIOPayload
    elif isinstance(data,StringIO):
        type_=StringIOPayload
    elif isinstance(data,TextIOBase):
        type_=TextIOPayload
    elif isinstance(data,(BufferedReader,BufferedRandom)):
        type_=BufferedReaderPayload
    elif isinstance(data,IOBase):
        type_=IOBasePayload
    elif isinstance(data,AsyncIO):
        type_=AsyncIOPayload
    elif isinstance(data,StreamReader):
        type_=StreamReaderPayload
    elif hasattr(data,'__aiter__'):
        type_=AsyncIterablePayload
    else:
        raise LookupError

    return type_(data,*args,**kwargs)


class payload_superclass:
    _default_content_type='application/octet-stream'
    def __init__(self, value, *, headers=None, content_type=sentinel,
                 filename=None, encoding=None, **kwargs):
        self.value      = value
        self.encoding   = encoding
        self.filename   = filename
        if (headers is not None) and headers:
            headers = multidict_titled(headers)
            self.headrs=headers
            if content_type is sentinel and CONTENT_TYPE in headers:
                content_type = headers[CONTENT_TYPE]
        else:
            self.headers=None
            
        if content_type is sentinel:
            content_type = None

        self._content_type = content_type
        self._size=None

    #at some places (1 at least) it is porperty so must change everywhere)
    @property
    def size(self):
        return self._size
        
    @property
    def content_type(self):
        if self._content_type is not None:
            return self._content_type
        elif (self.filename is not None):
            mime = mimetypes.guess_type(self.filename)[0]
            return 'application/octet-stream' if mime is None else mime
        else:
            return payload_superclass._default_content_type

    def set_content_disposition(self, disptype, params, quote_fields=True):
        headers=self.headers
        if headers is None:
            headers = multidict_titled()
            self.headers=headers
        else:
            headers.popall(CONTENT_DISPOSITION,None)
        
        headers[CONTENT_DISPOSITION] = content_disposition_header(
            disptype, params, quote_fields=quote_fields)


class BytesPayload(payload_superclass):

    def __init__(self,value,*args,**kwargs):
        if 'content_type' not in kwargs:
            kwargs['content_type']='application/octet-stream'

        payload_superclass.__init__(self,value,*args,**kwargs)

        self._size = len(value)

    async def write(self,writer):
        await writer.write(self.value)


class StringPayload(BytesPayload):

    def __init__(self,value,*args,encoding=None,content_type=None,**kwargs):
        if encoding is None:
            if content_type is None:
                encoding = 'utf-8'
                content_type = 'text/plain; charset=utf-8'
            else:
                mimetype = MimeType(content_type)
                encoding = mimetype.params.get('charset', 'utf-8')
        else:
            if content_type is None:
                content_type = f'text/plain; charset={encoding}'

        BytesPayload.__init__(self,value.encode(encoding),encoding=encoding,content_type=content_type,*args,**kwargs)


class StringIOPayload(StringPayload):

    def __init__(self,value,*args,**kwargs):
        StringPayload.__init__(self,value.read() *args,**kwargs)


class IOBasePayload(payload_superclass):

    def __init__(self,value,disposition='attachment',*args,**kwargs):
        if 'filename' not in kwargs:
            kwargs['filename']=getattr(value,'name',None)

        payload_superclass.__init__(self,value,*args,**kwargs)

        if (self.filename is not None) and (disposition is not None):
            self.set_content_disposition(disposition,{'filename':self.filename})

    async def write(self,writer):
        try:
            while True:
                chunk=self.value.read(DEFAULT_LIMIT)
                if chunk:
                    await writer.write(chunk)
                else:
                    break
        finally:
            self.value.close()


class TextIOPayload(IOBasePayload):

    def __init__(self,value,*args,encoding=None,content_type=None,**kwargs):

        if encoding is None:
            if content_type is None:
                encoding = 'utf-8'
                content_type = 'text/plain; charset=utf-8'
            else:
                mimetype = MimeType(content_type)
                encoding = mimetype.params.get('charset','utf-8')
        else:
            if content_type is None:
                content_type = f'text/plain; charset={encoding}'

        IOBasePayload.__init__(self,value,content_type=content_type, encoding=encoding, *args, **kwargs)

    @property
    def size(self):
        try:
            return os.fstat(self.value.fileno()).st_size - self.value.tell()
        except OSError:
            return None

    async def write(self,writer):
        try:
            while True:
                chunk=self.value.read(DEFAULT_LIMIT)
                if chunk:
                    await writer.write(chunk.encode(self.encoding))
                else:
                    break
        finally:
            self.value.close()


class BytesIOPayload(IOBasePayload):

    @property
    def size(self):
        position=self.value.tell()
        end=self.value.seek(0,os.SEEK_END)
        self.value.seek(position)
        return end-position


class BufferedReaderPayload(IOBasePayload):

    @property
    def size(self):
        try:
            return os.fstat(self.value.fileno()).st_size - self.value.tell()
        except OSError:
            # data.fileno() is not supported, e.g.
            # io.BufferedReader(io.BytesIO(b'data'))
            return None


class JsonPayload(BytesPayload):

    def __init__(self, value,
                 encoding='utf-8', content_type='application/json',
                 dumps=json.dumps, *args, **kwargs):

        BytesPayload.__init__(self,dumps(value).encode(encoding),
            content_type=content_type,encoding=encoding, *args, **kwargs)


class AsyncIterablePayload(payload_superclass):

    def __init__(self, value, *args, **kwargs):
        if 'content_type' not in kwargs:
            kwargs['content_type'] = 'application/octet-stream'

        payload_superclass.__init__(self,value, *args, **kwargs)

        self._iter = value.__aiter__()

    async def write(self, writer):
        try:
            while True:
                chunk = await self._iter.__anext__()
                await writer.write(chunk)
        except StopAsyncIteration:
            self._iter = None


class StreamReaderPayload(AsyncIterablePayload):

    def __init__(self, value, *args, **kwargs):
        AsyncIterablePayload.__init__(self,value.iter_any(), *args, **kwargs)

class AsyncIOPayload(IOBasePayload):
    async def write(self,writer):
        try:
            while True:
                chunk = await self.value.read(BIG_CHUNK_LIMIT)
                await writer.write(chunk)
                if len(chunk)<BIG_CHUNK_LIMIT:
                    break
        finally:
            self.value.close()


class BodyPartReaderPayload(payload_superclass):

    def __init__(self,value,*args,**kwargs):
        payload_superclass.__init__(self,value,*args,**kwargs)

        params = {}
        if value.name is not None:
            params['name']=value.name
        if value.filename is not None:
            params['filename']=value.filename

        if params:
            self.set_content_disposition('attachment',**params)

    async def write(self,writer):
        field=self.value
        while True:
            chunk=await field.read_chunk(size=65536)
            if chunk:
                await writer.write(field.decode(chunk))
            else:
                break


################X#X   py multipart X#X################




class MimeType(object):
    #Parses a MIME type into its components.
    #:param str mimetype: MIME type
    #:returns: 4 element tuple for MIME type, subtype, suffix and parameters
    #:rtype: tuple
    #Example:
    #>>> MimeType('text/html; charset=utf-8')
    #<MimeType type='text', subtype='html',suffix= '', parameters={'charset': 'utf-8'})>

    __slots__=('mtype', 'params', 'stype', 'suffix',)
    def __init__(self,mimetype):

        if not mimetype:
            self.mtype  = ''
            self.stype  = ''
            self.suffix = ''
            self.params = {}
            return
            
        parts = mimetype.split(';')
        params = multidict()
        for item in parts[1:]:
            if not item:
                continue
            if '=' in item:
                key,value=item.split('=', 1)
            else:
                key=item
                value=''
            
            params[key.lower().strip()]=value.strip(' "')


        fulltype = parts[0].strip().lower()
        if fulltype == '*':
            fulltype = '*/*'

        if '/' in fulltype:
            mtype,stype = fulltype.split('/', 1)
        else:
            mtype=fulltype
            stype=''

        if '+' in stype:
            stype,suffix=stype.split('+', 1)
        else:
            suffix=''
            
        self.mtype  = mtype
        self.stype  = stype
        self.suffix = suffix
        self.params = params
        
    def __repr__(self):
        return f'<{self.__class__.__name__} mtype={self.mtype!r} stype={self.stype!r} suffix={self.suffix!r} params={self.params!r}>'

    __str__=__repr__



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

    disptype, *parts = header.split(';')
    if not is_token(disptype):
        return None, {}

    params = {}
    while parts:
        item=parts.pop(0)
        
        if '=' not in item:
            return None, {}

        key,value = item.split('=', 1)
        key       = key.lower().strip()
        value     = value.lstrip()

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
            failed=True
            
            if is_quoted(value):
                value = unescape(value[1:-1].lstrip('\\/'))
            elif is_token(value):
                failed=False
            elif parts:
                value_=f'{value};{parts[0]}'
                if is_quoted(value_):
                    parts.pop(0)
                    value = unescape(value_[1:-1].lstrip('\\/'))
                    failed=False

            if failed:
                return None, {}

        params[key] = value

    return disptype.lower(),params


def content_disposition_filename(params,name='filename'):
    name_suf=f'{name}*'
    if not params:
        return None
    elif name_suf in params:
        return params[name_suf]
    elif name in params:
        return params[name]
    else:
        parts = []
        fnparams = sorted((key, value)
                          for key, value in params.items()
                          if key.startswith('filename*'))
        for num, (key, value) in enumerate(fnparams):
            _, tail = key.split('*', 1)
            if tail.endswith('*'):
                tail = tail[:-1]
            if tail == str(num):
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


class MultipartResponseWrapper:
    __slots__=('resp', 'stream',)
    #Wrapper around the :class:`MultipartBodyReader` to take care about
    #underlying connection and close it when it needs in.

    def __init__(self,resp,stream):
        self.resp   = resp
        self.stream = stream

    def __aiter__(self):
        return self

    async def __anext__(self):
        part = await self.next()
        if part is None:
            raise StopAsyncIteration
        return part

    def at_eof(self):
        #Returns True when all response data had been read.
        return self.resp.content.at_eof()

    async def next(self):
        #Emits next multipart reader object
        item = await self.stream.next()
        if self.stream.at_eof():
            await self.release()
        return item

    async def release(self):
        #Releases the connection gracefully, reading all the content to the void.
        await self.resp.release()


class BodyPartReader(object):
    __slots__=('headers','_boundary','_content','_at_eof','_length',
               '_read_bytes','_unread','_prev_chunk','_content_eof',
               '_cache',)
    #Multipart reader for single body part.

    chunk_size = 8192

    def __init__(self, boundary, headers, content):
        self.headers        = headers
        self._boundary      = boundary
        self._content       = content
        self._at_eof        = False
        length=self.headers.get(CONTENT_LENGTH,None)
        self._length        = None  if length is None else int(length)
        self._read_bytes    = 0
        self._unread        = deque()
        self._prev_chunk    = None
        self._content_eof   = 0
        self._cache         = {}
        
    def __aiter__(self):
        return self

    async def __anext__(self):
        item = await self.read()
        if item:
            return item
        raise StopAsyncIteration  # NOQA

    async def next(self):
        item = await self.read()
        if not item:
            return None
        return item

    async def read(self, *, decode=False):
        #Reads body part data.
        #param bool decode: Decodes data following by encoding
        #                   method from `Content-Encoding` header. If it missed
        #                   data remains untouched
        #rtype: bytearray
        if self._at_eof:
            return b''
        data = bytearray()
        while not self._at_eof:
            data.extend((await self.read_chunk(self.chunk_size)))
        if decode:
            return self.decode(data)
        return data

    async def read_chunk(self, size=chunk_size):
        #Reads body part content chunk of the specified size.
        #param int size: chunk size
        #:type bytearray

        if self._at_eof:
            return b''
        if self._length:
            chunk = await self._read_chunk_from_length(size)
        else:
            chunk = await self._read_chunk_from_stream(size)

        self._read_bytes += len(chunk)
        if self._read_bytes==self._length:
            self._at_eof = True
        if self._at_eof:
            await self._content.readline()
        
        return chunk

    async def _read_chunk_from_length(self, size):
        #Reads body part content chunk of the specified size.
        #The body part must has `Content-Length` header with proper value.
        #:param int size: chunk size
        #:rtype: bytearray

        chunk_size=min(size,self._length-self._read_bytes)
        chunk = await self._content.read(chunk_size)
        return chunk

    async def _read_chunk_from_stream(self, size):
        #Reads content chunk of body part with unknown length.
        #The `Content-Length` header for body part is not necessary.
        #:param int size: chunk size
        #:rtype: bytearray

        first_chunk = self._prev_chunk is None
        if first_chunk:
            self._prev_chunk = await self._content.read(size)

        chunk = await self._content.read(size)
        self._content_eof += int(self._content.at_eof())

        window = self._prev_chunk + chunk
        sub=b'\r\n' + self._boundary
        
        if first_chunk:
            idx=window.find(sub)
        else:
            idx=window.find(sub,max(0,len(self._prev_chunk)-len(sub)))
        if idx>=0:
            # pushing boundary back to content
            self._content.unread_data(window[idx:])
            if size>idx:
                self._prev_chunk=self._prev_chunk[:idx]
            chunk = window[len(self._prev_chunk):idx]
            if not chunk:
                self._at_eof = True
        result = self._prev_chunk
        self._prev_chunk = chunk
        return result

    async def readline(self):
        #Reads body part by line by line.
        #returns bytearray

        if self._at_eof:
            return b''

        if self._unread:
            line = self._unread.popleft()
        else:
            line = await self._content.readline()

        if line.startswith(self._boundary):
            # the very last boundary may not come with \r\n,
            # so set single rules for everyone
            sline = line.rstrip(b'\r\n')
            boundary = self._boundary
            last_boundary = self._boundary + b'--'
            #make sure that we read exactly the boundary, not something alike
            if sline == boundary or sline == last_boundary:
                self._at_eof = True
                self._unread.append(line)
                return b''
        else:
            next_line = await self._content.readline()
            if next_line.startswith(self._boundary):
                line = line[:-2]  # strip CRLF but only once
            self._unread.append(next_line)

        return line

    async def release(self):
        #Like :meth:`read`, but reads all the data to the void.
        #:rtype: None

        if self._at_eof:
            return

        while not self._at_eof:
            await self.read_chunk(self.chunk_size)

    async def text(self, *, encoding=None):
        #Like :meth:`read`, but assumes that body part contains text data.
        #:param str encoding: Custom text encoding. Overrides specified
        #                     in charset param of `Content-Type` header
        #returns str

        data = await self.read(decode=True)
        # see https://www.w3.org/TR/html5/forms.html#multipart/form-data-encoding-algorithm # NOQA
        # and https://dvcs.w3.org/hg/xhr/raw-file/tip/Overview.html#dom-xmlhttprequest-send # NOQA
        encoding = encoding or self.get_charset(default='utf-8')
        return data.decode(encoding)

    async def json(self, *, encoding=None):
        #Like :meth:`read`, but assumes that body parts contains JSON data.
        #:param str encoding: Custom JSON encoding. Overrides specified
        #                     in charset param of `Content-Type` header

        data = await self.read(decode=True)
        if not data:
            return None
        encoding = encoding or self.get_charset(default='utf-8')
        return json.loads(data.decode(encoding))

    async def form(self, *, encoding=None):
        #Like :meth:`read`, but assumes that body parts contains form
        #urlencoded data.
        #:param str encoding: Custom form encoding. Overrides specified
        #                     in charset param of `Content-Type` header

        data = await self.read(decode=True)
        if not data:
            return None
        encoding = encoding or self.get_charset(default='utf-8')
        return parse_qsl(data.rstrip().decode(encoding),keep_blank_values=True,encoding=encoding)

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

        ctype = self.headers.get(CONTENT_TYPE, '')
        mimetype=MimeType(ctype)
        return mimetype.params.get('charset', default)

    @property
    def name(self):
        #Returns name specified in Content-Disposition header or None
        #if missed or header is malformed.
        _,params=parse_content_disposition(self.headers.get(CONTENT_DISPOSITION))
        return content_disposition_filename(params,'name')
    
    @property
    def filename(self):
        #Returns filename specified in Content-Disposition header or None
        #if missed or header is malformed
        _,params=parse_content_disposition(self.headers.get(CONTENT_DISPOSITION))
        return content_disposition_filename(params,'filename')

class MultipartReader:
    __slots__=('headers','_boundary','_content','_last_part','_at_eof',
               '_at_bof','_unread',)
    
    #Multipart body reader.

    def __init__(self, headers, content):
        self.headers    = headers
        self._boundary  = ('--' + self._get_boundary()).encode()
        self._content   = content
        self._last_part = None
        self._at_eof    = False
        self._at_bof    = True
        self._unread    = []

    def __aiter__(self):
        return self

    async def __anext__(self):
        part = await self.next()
        if part is None:
            raise StopAsyncIteration
        return part

    @classmethod
    def from_response(cls, response):
        #Constructs reader instance from HTTP response.
        #response = ClientResponse
        
        return MultipartResponseWrapper(response,cls(response.headers,response.content))


    def at_eof(self):
        #Returns True if the final boundary was reached or False otherwise.
        
        return self._at_eof

    async def next(self):
        #Emits the next multipart body part.
        # So, if we're at BOF, we need to skip till the boundary.
        if self._at_eof:
            return
        
        await self._maybe_release_last_part()
        if self._at_bof:
            await self._read_until_first_boundary()
            self._at_bof = False
        else:
            await self._read_boundary()
        if self._at_eof:  # we just read the last boundary, nothing to do there
            return
        self._last_part = await self.fetch_next_part()
        return self._last_part

    async def release(self):
        #Reads all the body parts to the void till the final boundary.
        while not self._at_eof:
            item = await self.next()
            if item is None:
                break
            await item.release()

    async def fetch_next_part(self):
        #Returns the next body part reader.
        
        headers=await self._read_headers()
        return self._get_part_reader(headers)

    def _get_part_reader(self, headers):
        #Dispatches the response by the Content-Type header, returning uitable reader instance.
        #headers = dict

        ctype = headers.get(CONTENT_TYPE, '')
        mimetype=MimeType(ctype)
        if mimetype.mtype == 'multipart':
            return type(self)(headers, self._content)

        else:
            return BodyPartReader(self._boundary, headers, self._content)

    def _get_boundary(self):
        mimetype=MimeType(self.headers[CONTENT_TYPE])

        if 'boundary' not in mimetype.params:
            raise ValueError(f'boundary missed for Content-Type: {self.headers[CONTENT_TYPE]}')

        boundary = mimetype.params['boundary']
        if len(boundary)>70:
            raise ValueError(f'boundary {boundary!r} is too long (70 chars max)')

        return boundary

    async def _readline(self):
        if self._unread:
            return self._unread.pop()
        return (await self._content.readline())

    async def _read_until_first_boundary(self):
        while True:
            chunk = await self._readline()
            if chunk == b'':
                raise ValueError(f'Could not find starting boundary {self._boundary!r}')

            chunk=chunk.rstrip()
            
            if chunk==self._boundary:
                return
            
            elif chunk==self._boundary+b'--':
                self._at_eof=True
                return

    async def _read_boundary(self):
        chunk = (await self._readline()).rstrip()
        if chunk==self._boundary:
            pass
        
        elif chunk==self._boundary+b'--':
            self._at_eof=True
            
            epilogue  = await self._readline()
            next_line = await self._readline()

            # the epilogue is expected and then either the end of input or the
            # parent multipart boundary, if the parent boundary is found then
            # it should be marked as unread and handed to the parent for
            # processing
            if next_line.startswith(b'--'):
                self._unread.append(next_line)
            # otherwise the request is likely missing an epilogue and both
            # lines should be passed to the parent for processing
            # (this handles the old behavior gracefully)
            else:
                self._unread.extend([next_line, epilogue])
                
        else:
            raise ValueError('Invalid boundary {chunk!r}, expected {self._boundary!r}')

    async def _read_headers(self):
        lines = [b'']
        while True:
            chunk = await self._content.readline()
            chunk = chunk.strip()
            lines.append(chunk)
            if not chunk:
                break
        parser = HttpParser()
        headers, *_ = parser.parse_headers(lines)
        return headers

    async def _maybe_release_last_part(self):
        #makes sure that the last read body part is read completely.
        if self._last_part is not None:
            if not self._last_part.at_eof():
                await self._last_part.release()
            self._unread.extend(self._last_part._unread)
            self._last_part = None

        
class MultipartWriter(payload_superclass):
    __slots__=('_boundary', '_content_type', '_size', 'encoding', 'filename',
        'haders', 'parts', 'value')
    
    def __init__(self,subtype='mixed',boundary=None):
        if boundary:
            try:
                self._boundary=boundary.encode('ascii')
            except UnicodeEncodeError:
                raise ValueError('boundary should contains ASCII only chars')
        else:
            self._boundary=uuid.uuid4().hex.encode('ascii')
            
        payload_superclass.__init__(self,None,content_type=f'multipart/{subtype}; boundary={self.boundary_value}')

        self.parts=[]
        self.headers=multidict_titled()
        self.headers[CONTENT_TYPE]=self.content_type

    @property
    def boundary(self):
        return self._boundary.decode('ascii')
    
    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        pass

    def __iter__(self):
        return iter(self.parts)

    def __len__(self):
        return len(self.parts)

    _valid_tchar_regex          = re.compile(br"\A[!#$%&'*+\-.^_`|~\w]+\Z")
    _invalid_qdtext_char_regex  = re.compile(br"[\x00-\x08\x0A-\x1F\x7F]")

    @property
    def boundary_value(self):
        #Wrap boundary parameter value in quotes, if necessary.
        #Reads self.boundary and returns a unicode sting.
        
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
        value=self._boundary
        if self._valid_tchar_regex.match(value) is not None:
            return value.decode('ascii')

        if self._invalid_qdtext_char_regex.search(value) is not None:
            raise ValueError('boundary value contains invalid characters')

        # escape %x5C and %x22
        quoted_value_content = value.replace(b'\\',b'\\\\')
        quoted_value_content = quoted_value_content.replace(b'"', b'\\"')

        return f'"{quoted_value_content.decode("ascii")}"'

    def append(self,obj,headers=None):
        #Adds a new body part to multipart writer.
        if headers is None:
            headers=multidict_titled()
            
        if isinstance(obj,payload_superclass):
            if obj.headers is None:
                obj.headers=headers
            else:
                obj.headers.update(headers)
        else:
            try:
                return self.append_payload(create_payload(obj,headers=headers))
            except LookupError:
                raise TypeError

    def append_payload(self,payload):
        #Adds a new body part to multipart writer.
        
        # content-type
        if CONTENT_TYPE not in payload.headers:
            payload.headers[CONTENT_TYPE]=payload.content_type

        # compression
        try:
            encoding=payload.headers[CONTENT_ENCODING].lower()
        except KeyError:
            encoding=''
        else:
            if encoding and encoding not in ('deflate', 'gzip', 'identity'):
                raise RuntimeError(f'unknown content encoding: {encoding}')
            if encoding=='identity':
                encoding=None

        # te encoding
        try:
            te_encoding = payload.headers[CONTENT_TRANSFER_ENCODING].lower()
        except KeyError:
            te_encoding=''
        else:
            if te_encoding not in ('', 'base64', 'quoted-printable', 'binary'):
                raise RuntimeError(f'unknown content transfer encoding: {te_encoding}')

            if te_encoding=='binary':
                te_encoding=None

        # size
        size=payload.size
        
        if size is not None and not (encoding or te_encoding):
            payload.headers[CONTENT_LENGTH]=str(size)

        # render headers
        headers=''.join([f'{k}: {v}\r\n' for k, v in payload.headers.items()]).encode('utf-8') + b'\r\n'

        self.parts.append((payload,headers,encoding,te_encoding))

        return payload

    
    def append_json(self,obj,headers=None):
        #Helper to append JSON part.
        if headers is None:
            headers=multidict_titled()
            
        return self.append_payload(JsonPayload(obj,headers=headers))

    def append_form(self, obj, headers=None):
        #Helper to append form urlencoded part.
        
        if headers is None:
            headers=multidict_titled()
        
        if hasattr(obj,'keys') and hasattr(obj,'__getitem__'): #mapping type
            obj=list(obj.items())
            
        data = urlencode(obj,doseq=True)

        return self.append_payload(
            StringPayload(data,headers=headers,content_type='application/x-www-form-urlencoded'))

    @property
    def size(self):
        if not self.parts:
            return 0

        total=0
        for part,headers,encoding,te_encoding in self.parts:
            if encoding or te_encoding or part.size is None:
                return None
            total+=6+len(self._boundary)+part.size+len(headers)
            # b'--'+self._boundary+b'\r\n' # b'\r\n'

        total+=6+len(self._boundary) 
        # b'--'+self._boundary+b'--\r\n'
        
        return total

    async def write(self,writer,close_boundary=True):
        #Writes body
        if not self.parts:
            return

        for part,headers,encoding,te_encoding in self.parts:
            await writer.write(b'--'+self._boundary+b'\r\n') #fb strings pls!
            await writer.write(headers)
            
            if encoding or te_encoding:
                w = MultipartPayloadWriter(writer)
                if encoding:
                    w.enable_compression(encoding)
                if te_encoding:
                    w.enable_encoding(te_encoding)
                await part.write(w)
                await w.write_eof()
            else:
                await part.write(writer)
            await writer.write(b'\r\n')

        if close_boundary:
            await writer.write(b'--'+self._boundary+b'--\r\n')


class MultipartPayloadWriter:
    __slots__=('compress', 'encoding', 'encoding_buffer', 'writer',)

    def __init__(self,writer):
        self.writer    = writer
        self.encoding  = None
        self.compress  = None

    def enable_encoding(self,encoding):
        if encoding=='base64':
            self.encoding          = encoding
            self.encoding_buffer   = bytearray()
        
        elif encoding=='quoted-printable':
            self.encoding          = 'quoted-printable'

    def enable_compression(self,encoding='deflate'):
        if encoding=='gzip':
            zlib_mode=16+zlib.MAX_WBITS
        else:
            zlib_mode=-zlib.MAX_WBITS
            
        self.compress=zlib.compressobj(wbits=zlib_mode)

    async def write_eof(self):
        if self.compress is not None:
            chunk=self.compress.flush()
            if chunk:
                self.compress=None
                await self.write(chunk)

        if self.encoding=='base64':
            if self.encoding_buffer:
                await self.writer.write(base64.b64encode(self.encoding_buffer))

    async def write(self, chunk):
        if self.compress is not None:
            if chunk:
                chunk=self.compress.compress(chunk)
                if not chunk:
                    return

        if self.encoding=='base64':
            self.encoding_buffer.extend(chunk)

            if self.encoding_buffer:
                buffer=self.encoding_buffer
                div,mod=divmod(len(buffer),3)
                
                encoding_chunk         = buffer[:div*3]
                self.encoding_buffer   = buffer[div*3:]
                
                if encoding_chunk:
                    encoding_chunk=base64.b64encode(encoding_chunk)
                    await self.writer.write(encoding_chunk)
                    
        elif self.encoding=='quoted-printable':
            await self.writer.write(binascii.b2a_qp(chunk))
            
        else:
            await self.writer.write(chunk)


