# -*- coding: utf-8 -*-
__all__ = ('WSClient', 'WSServer', )

import hashlib, codecs, re, functools
from random import getrandbits
from base64 import b64encode, b64decode
from struct import Struct
import urllib.parse
from collections import OrderedDict, deque
from binascii import Error as BinasciiError
from email.utils import formatdate

from .dereaddons_local import multidict_titled
from .futures import Future, Task, AsyncQue, future_or_timeout, shield, CancelledError, WaitTillAll, iscoroutine

from .py_hdrs import CONNECTION, SEC_WEBSOCKET_KEY, AUTHORIZATION, SEC_WEBSOCKET_VERSION, CONTENT_ENCODING, \
    SEC_WEBSOCKET_EXTENSIONS, SEC_WEBSOCKET_PROTOCOL, HOST, ORIGIN, SEC_WEBSOCKET_ACCEPT, UPGRADE, DATE, METH_GET, \
    CONTENT_TYPE, SERVER, CONTENT_LENGTH, build_extensions, build_basic_auth, parse_subprotocols, parse_upgrades, \
    parse_connections, parse_extensions, build_subprotocols, TRANSFER_ENCODING
from .py_exceptions import PayloadError, InvalidUpgrade, AbortHandshake, ConnectionClosed, InvalidHandshake, \
    InvalidOrigin, WebSocketProtocolError
from .py_helpers import HttpVersion, HttpVersion11

import http

FORBIDDEN             = http.HTTPStatus.FORBIDDEN
UPGRADE_REQUIRED      = http.HTTPStatus.UPGRADE_REQUIRED
BAD_REQUEST           = http.HTTPStatus.BAD_REQUEST
INTERNAL_SERVER_ERROR = http.HTTPStatus.INTERNAL_SERVER_ERROR
SERVICE_UNAVAILABLE   = http.HTTPStatus.SERVICE_UNAVAILABLE
SWITCHING_PROTOCOLS   = http.HTTPStatus.SWITCHING_PROTOCOLS

del http

OP_CONT     = 0
OP_TEXT     = 1
OP_BINARY   = 2

OP_CLOSE    = 8
OP_PING     = 9
OP_PONG     = 10

DATA_OPCODES = (OP_CONT,  OP_TEXT, OP_BINARY)
CTRL_OPCODES = (OP_CLOSE, OP_PING, OP_PONG)

EXTERNAL_CLOSE_CODES=(1000,1001,1002,1003,1007,1008,1009,1010,1011,)

UNPACK_LEN2 = Struct('!H').unpack_from
UNPACK_LEN3 = Struct('!Q').unpack_from

PACK_LEN1   = Struct('!BB').pack
PACK_LEN2   = Struct('!BBH').pack
PACK_LEN3   = Struct('!BBQ').pack

CONNECTING  = 'CONNECTING'
OPEN        = 'OPEN'
CLOSING     = 'CLOSING'
CLOSED      = 'CLOSED'

WS_KEY = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

_HEADER_KEY_RP = re.compile(rb'[-!#$%&\'*+.^_`|~0-9a-zA-Z]+')
_HEADER_VALUE_RP = re.compile(rb'[\x09\x20-\x7e\x80-\xff]*')

HTTP_STATUS_RP = re.compile(b'HTTP/(\d)\.(\d) (\d\d\d)(?: (.*?))?\r\n')
HTTP_REQUEST_RP = re.compile(b'([^ ]+) ([^ ]+) HTTP/(\d)\.(\d)\r\n')

HTTP_STATUS_LINE_RP=re.compile(b'HTTP/(\d)\.(\d) (\d\d\d)(?: (.*?))?')
HTTP_REQUEST_LINE_RP = re.compile(b'([^ ]+) ([^ ]+) HTTP/(\d)\.(\d)')

CHUNK_LIMIT = 32
MAX_LINE_LENGTH = 8190

del Struct, re

class RawMessage(object):
    __slots__ = ('headers', )
    
    @property
    def close_connection(self):
        try:
            connection=self.headers[CONNECTION]
        except KeyError:
            pass
        else:
            connection = connection.lower()
            if connection.lower() == 'keep-alive':
                return True
            
            if connection == 'close':
                return False
        
        return False # deside?
    
    @property
    def upgrade(self):
        try:
            connection=self.headers[CONNECTION]
        except KeyError:
            return False
        
        return (connection.lower() == 'upgrade')
    
    @property
    def chunked(self):
        try:
            transfer_encoding = self.headers[TRANSFER_ENCODING]
        except KeyError:
            return False
        
        return ('chunked' in transfer_encoding)
    
    @property
    def encoding(self):
        try:
            encoding = self.headers[CONTENT_ENCODING]
        except KeyError:
            return
       
        encoding = encoding.lower()
        if encoding in ('gzip', 'deflate', 'br'):
            return encoding

class RawResponseMessage(RawMessage):
    __slots__ = ('version', 'status', 'reason')
    
    def __init__(self, version, status, reason, headers):
        self.version=version
        self.status=status
        self.reason=reason
        self.headers=headers

class RawRequestMessage(RawMessage):
    __slots__ = ('version', 'meth', 'path',)
    
    def __init__(self, version, meth, path, headers):
        self.version = version
        self.meth = meth
        self.path = path
        self.headers = headers

#TODO: whats the fastest way on pypy ? casting 64 bit ints -> xor -> replace?
_XOR_TABLE = [bytes(a^b for a in range(256)) for b in range(256)]
def apply_mask(mask,data):
    data_bytes=bytearray(data)
    for index in range(4):
        data_bytes[index::4]=data_bytes[index::4].translate(_XOR_TABLE[mask[index]])
    return data_bytes

class Frame(object):
    __slots__=('data', 'head1',)
    def __init__(self, fin, opcode, data):
        self.data=data
        self.head1=(fin<<7)|opcode
    
    @property
    def fin(self):
        return (self.head1&0b10000000)>>7
    
    @property
    def rsv1(self):
        return (self.head1&0b01000000)>>6

    @property
    def rsv2(self):
        return (self.head1&0b00100000)>>5

    @property
    def rsv3(self):
        return (self.head1&0b00010000)>>4

    @property
    def opcode(self):
        return  self.head1&0b00001111

    @classmethod
    async def read(cls,websocket,max_size):
        #read the header.
        reader=websocket.reader
        
        data = await reader.readexactly(2)
        head1,head2=data
        
        opcode=head1&0b00001111
        
        if ((head2&0b10000000)>>7)==websocket.is_client:
            raise WebSocketProtocolError('Incorrect masking')
        
        length = head2&0b01111111
        
        if length == 126:
            data = await reader.readexactly(2)
            length, = UNPACK_LEN2(data)
        elif length == 127:
            data = await reader.readexactly(8)
            length, = UNPACK_LEN3(data)
        
        if max_size is not None and length>max_size:
            raise PayloadError(f'Payload length exceeds size limit ({length} > {max_size} bytes)')
        
        #Read the data.
        if websocket.is_client:
            data = await reader.readexactly(length)
        else:
            mask = await reader.readexactly(4)
            data = await reader.readexactly(length)
            data=apply_mask(mask,data)
        
        frame=object.__new__(cls)
        frame.data=data
        frame.head1=head1
        
        if websocket.extensions is not None:
            for extension in reversed(websocket.extensions):
                frame=extension.decode(frame,max_size=websocket.max_size)
        
        frame.check()
        
        return frame
    
    def write(frame,websocket):
        #walidates, then writes a websocket frame.
        frame.check()

        if websocket.extensions is not None:
            for extension in websocket.extensions:
                frame = extension.encode(frame)

        writer=websocket.writer
        
        # Prepare the header.
        head1 = frame.head1
        head2 = websocket.is_client<<7

        length=len(frame.data)
        if length<126:
            writer.write(PACK_LEN1(head1,head2|length))
        elif length<65536:
            writer.write(PACK_LEN2(head1,head2|126,length))
        else:
            writer.write(PACK_LEN3(head1,head2|127,length))

        #prepare the data.
        if websocket.is_client:
            mask=getrandbits(32).to_bytes(4,'big')
            writer.write(mask)
            data=apply_mask(mask,frame.data,)
        else:
            data=frame.data
            
        writer.write(data)

    def check(frame):
        #check that this frame contains acceptable values.
        if frame.head1&0b01110000:
            raise WebSocketProtocolError('Reserved bits must be 0')

        opcode=frame.head1&0b00001111
        if opcode in DATA_OPCODES:
            return
        
        if opcode in CTRL_OPCODES:
            if len(frame.data)>125:
                raise WebSocketProtocolError('Control frame too long')
            if not frame.head1&0b10000000:
                raise WebSocketProtocolError('Fragmented control frame')
            return
        
        raise WebSocketProtocolError(f'Invalid opcode: {opcode}')


class StreamWriter(object):
    __slots__=('loop', 'protocol', 'reader', 'transport')
    def __init__(self,loop,transport,protocol,reader):
        self.transport = transport
        self.protocol = protocol
        self.reader = reader
        self.loop = loop

    def __repr__(self):
        return f'<{self.__class__.__name__} transport={self.transport!r} reader={self.reader!r}>'

    def write(self, data):
        self.transport.write(data)
    
    def write_http_request(self, meth, path, headers, version = HttpVersion11):
        result = [f'{meth} {path} HTTP/{version.major}.{version.major}\r\n']
        extend = result.extend
        for k, v in headers.items():
            extend((k,': ',v,'\r\n'))
        
        result.append('\r\n')
    
        self.transport.write(''.join(result).encode())
    
    def write_http_response(self, status, headers, version = HttpVersion11, body = None):
        result = [f'HTTP/{version.major}.{version.minor} {status.value} {status.phrase}\r\n']
        extend = result.extend
        for k, v in headers.items():
            extend((k,': ',v,'\r\n'))
        
        result.append('\r\n')
        
        transport = self.transport
        transport.write(''.join(result).encode())
        if (body is not None) and body:
            transport.write(body)
    
    def writelines(self, data):
        self.transport.writelines(data)

    def write_eof(self):
        return self.transport.write_eof()

    def can_write_eof(self):
        return self.transport.can_write_eof()

    def close(self):
        return self.transport.close()

    def get_extra_info(self, name, default=None):
        return self.transport.get_extra_info(name, default)

    async def drain(self):
        #use after writing
        reader = self.reader
        if reader is not None:
            exception = reader.exception
            if (exception is not None):
                raise exception
        
        transport = self.transport
        if transport is not None:
            if transport.is_closing():
                #skip 1 loop, so connection_lost() will be called
                future=Future(self.loop)
                future.set_result(None)
                await future
        
        await self.protocol._drain_helper()

class StreamReader(object):
    __slots__ = ('chunks', '_waiter', 'loop', 'exception', 'eof', 'transport', '_paused', '_offset')
    
    def __init__(self, loop):
        self.chunks = deque()
        self._waiter = None
        self.loop = loop
        self.exception=None
        self.eof = False
        self.transport = None
        self._paused = False
        self._offset = 0
        
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        add_comma = False
        size = self.size
        if size:
            result.append(' ')
            result.append(repr(size))
            result.append(' bytes')
            add_comma=True
        
        if self.eof:
            if add_comma:
                result.append(',')
            else:
                add_comma = True
            result.append(' at eof')
        
        waiter = self._waiter
        if (waiter is not None):
            if add_comma:
                result.append(',')
            else:
                add_comma = True
            result.append(' waiter=')
            result.append(repr(waiter))
        
        exception = self.exception
        if (exception is not None):
            if add_comma:
                result.append(',')
            else:
                add_comma = True
            result.append(' exception=')
            result.append(repr(exception))
        
        transport = self.transport
        if (transport is not None):
            if add_comma:
                result.append(',')
            else:
                add_comma = True
            result.append(' transport=')
            result.append(repr(transport))
        
        if self._paused:
            if add_comma:
                result.append(',')
            else:
                add_comma = True
            result.append(' paused')
        
        result.append('>')
        
        return ''.join(result)
    
    @property
    def size(self):
        result = - self._offset
        for chunk in self.chunks:
            result += len(chunk)
        
        return result
    
    def set_exception(self, exception):
        self.exception = exception
        waiter = self._waiter
        if waiter is None:
            return
        
        if not waiter.cancelled():
            waiter.set_exception(exception)
    
    def set_transport(self, transport):
        self.transport = transport
    
    def _maybe_resume_tranport(self):
        if self._paused and len(self.chunks) > CHUNK_LIMIT:
            self._paused = False
            self.transport.resume_reading()
        
    def feed_eof(self):
        self.eof = True
        
        waiter = self._waiter
        if (waiter is not None):
            self._waiter = None
            
            if (not waiter.cancelled()):
                waiter.set_result(None)
    
    def at_eof(self):
        return (self.eof and (not self.size))
    
    def feed_data(self, data):
        size = len(data)
        if size == 0:
            return
        
        chunks = self.chunks
        self.chunks.append(data)
        
        waiter = self._waiter
        if (waiter is not None):
            self._waiter = None
            
            if (not waiter.cancelled()):
                waiter.set_result(None)
        
        if (len(chunks) > CHUNK_LIMIT) and (not self._paused):
            transport = self.transport
            if (transport is not None):
                try:
                    transport.pause_reading()
                except (AttributeError,NotImplemented):
                    #cant be paused
                    self.transport = None
                else:
                    self._paused = True
    
    async def _wait_for_data(self):
        if self._paused:
            self._paused = False
            self.transport.resume_reading()
        
        waiter = self._waiter = Future(self.loop)
        await waiter
    
    async def readtill_CRLF(self):
        exception = self.exception
        if (exception is not None):
            raise exception
        
        chunks = self.chunks
        
        chunk = chunks[0]
        
        # Do first search outside, because we operate with offset
        offset = self._offset
        
        position = chunk.find(b'\r\n', offset)
        
        if position != -1:
            # We found!
            # Because the result must be bytes, we slice it
            collected = chunk[offset:position]
            # Add 2 to position to compensate CRLF
            position = position+2
            
            # If the chunk is exhausted, remove it
            if len(chunk)==position:
                del chunks[0]
                self._offset = 0
            # Else, offset it, fast slicing!
            else:
                self._offset = position
            
            return collected
        
        # If first did not succeed, lets go normally.
        collected = []
        n = MAX_LINE_LENGTH - len(chunk)
        # If there is offset, apply it
        if offset:
            collected.append(memoryview(chunk)[offset:])
            n += offset
        else:
            collected.append(chunk)
        del chunks[0]
        
        while True:
            # case 2: found between 2?
            if chunk[-1] == b'\r'[0]:
                if chunks:
                    chunk = chunks[0]
                else:
                    if self.eof:
                        chunks.clear()
                        self._offset = 0
                        raise EOFError(b''.join(collected))
                    
                    await self._wait_for_data()
                    chunk = chunks[0]
                
                if chunk[0] == b'\n'[0]:
                    # If size is 1, we delete it
                    if len(chunk)==1:
                        del chunks[0]
                        self._offset = 0
                    # If more, fast slice it!
                    else:
                        self._offset = 1
                    
                    # cast memory view, so we do not need to create a new immutable
                    collected[-1] = memoryview(collected[-1])[:-1]
                    
                    return b''.join(collected)
                
            else:
                # case 3: not found, go for next chunk
                if chunks:
                    chunk = chunks[0]
                else:
                    if self.eof:
                        chunks.clear()
                        self._offset = 0
                        raise EOFError(b''.join(collected))
                    
                    await self._wait_for_data()
                    chunk = chunks[0]
            
            # no offset search
            position = chunk.find(b'\r\n')
            
            # case 1: found in middle
            if position != -1:
                # cast memoryview
                collected.append(memoryview(chunk)[:position])
                
                # Add 2 position to ompensate CRLF
                position = position+2
                # If the chunk is fully exhausted remove it
                if len(chunk) == position:
                    del chunks[0]
                    self._offset = 0
                # Fast slice the rest of the chunk with offset
                else:
                    self._offset=position
                
                return b''.join(collected)
            
            # collected the data
            collected.append(chunk)
            del chunks[0]
            n -=len(chunk)
            if n < 0:
                raise PayloadError(f'Header line exceeds max line length: {MAX_LINE_LENGTH!r} by {-n!r} and CRLF still not found.')
            
            continue
        
    async def readexactly(self, n):
        exception = self.exception
        if (exception is not None):
            raise exception
        
        if n<1:
            if n<0:
                raise ValueError(f'.readexactly called with negative `n`: {n!r}')
            else:
                return b''
        
        chunks = self.chunks
        if not chunks:
            if not chunks:
                if self.eof:
                    self._offset = 0
                    raise EOFError(b'')
                
                await self._wait_for_data()
            
        chunk = chunks[0]
        offset = self._offset
        chunk_size = len(chunk)
        if offset == 0:
            if chunk_size > n:
                self._offset = n
                result = chunk[:n]
                return chunk[:n]
            #chunk same size as the requested?
            elif chunk_size == n:
                del chunks[0]
                # offset is already 0, nice!
                return chunk
            
            else:
                n -= len(chunk)
                collected = [chunk]
                del chunks[0]
        else:
            end = offset+n
            if chunk_size > end:
                self._offset = end
                return chunk[offset:end]
            #chunksize + offset end when the requested's end is.
            elif chunk_size == end:
                del chunks[0]
                self._offset = 0
                return chunk[offset:]
            
            else:
                n -= (chunk_size - offset)
                collected = [memoryview(chunk)[offset:]]
                del chunks[0]
        
        while True:
            if not chunks:
                if self.eof:
                    self._offset = 0
                    raise EOFError(b''.join(collected))
                
                await self._wait_for_data()
            
            chunk = chunks[0]
            chunk_size = len(chunk)
            
            n -= chunk_size
            
            if n > 0:
                collected.append(chunk)
                del chunks[0]
                continue
            
            if n == 0:
                collected.append(chunk)
                del chunks[0]
                self._offset = 0
                return b''.join(collected)
            
            offset = self._offset = chunk_size+n
            collected.append(memoryview(chunk)[:offset])
            return b''.join(collected)
    
    async def _read_http_helper(self):
        chunks = self.chunks
        if chunks:
            chunk = chunks[0]
            offset = self._offset
        else:
            if self.eof:
                raise EOFError(b'')
            
            await self._wait_for_data()
            chunk = chunks[0]
            offset = 0
        
        return chunk, offset
    
    async def read_http_response(self):
        exception = self.exception
        if (exception is not None):
            raise exception
        
        chunk, offset = await self._read_http_helper()
        
        parsed = HTTP_STATUS_RP.match(chunk, offset)
        if parsed is None:
            # stupid fallback
            line = await self.readtill_CRLF()
            parsed = HTTP_STATUS_LINE_RP.fullmatch(line)
            if parsed is None:
                raise PayloadError(f'Invalid status line: {line!r}.')
            
            chunk, offset = await self._read_http_helper()
        else:
            offset = parsed.end()
            
        major, minor, status, reason = parsed.groups()
        
        headers = await self.read_http_headers(chunk, offset)
        return RawResponseMessage(HttpVersion(int(major), int(minor)), int(status), reason, headers)
    
    async def read_http_request(self):
        exception = self.exception
        if (exception is not None):
            raise exception
        
        chunk, offset = await self._read_http_helper()
        
        parsed = HTTP_REQUEST_RP.match(chunk, offset)
        if parsed is None:
            # stupid fallback
            line = await self.readtill_CRLF()
            parsed = HTTP_REQUEST_LINE_RP.fullmatch(line)
            if parsed is None:
                raise PayloadError(f'invalid request line: {line!r}')
            
            chunk, offset = await self._read_http_helper()
        else:
            offset = parsed.end()
        
        meth, path, major, minor = parsed.groups()
        
        headers = await self.read_http_headers(chunk, offset)
        return RawRequestMessage(HttpVersion(int(major), int(minor)), meth.upper().decode(), path.decode('ascii', 'surrogateescape'), headers)
    
    async def read_http_headers(self, chunk, offset):
        headers = multidict_titled()
        chunks = self.chunks
        
        middle = chunk.find(b':',offset)
        end = chunk.find(b'\r\n',middle)
        
        if end == -1:
            # This aint a real `while True`, just a Python GOTO
            while True:
                # we are at the end?
                if len(chunk) == offset:
                    del chunks[0]
                    
                    # read a new chunk, because thats pretty simple
                    if not chunks:
                        if self.eof:
                            raise EOFError(b'')
                        
                        await self._wait_for_data()
                    
                    chunk = chunks[0]
                    
                    middle = chunk.find(b':')
                    end = chunk.find(b'\r\n')
                    
                    if end == -1:
                        self._offset = 0
                    else:
                        name = chunk[offset:middle].lstrip()
                        value = chunk[middle+1:end].strip()
                        offset = end+2
                
                elif len(chunk) >= (offset - 2) and chunk[offset] == b'\r'[0] and chunk[offset+1] == b'\n'[0]:
                    # No headers at all: Store offset and quit
                    self._offset = offset+2
                    return headers
                
                self._offset = offset
                #  try getting a full line
                line = await self.readtill_CRLF()
                # no headers at all? OK, I guess
                if not line:
                    return headers
                
                middle = line.find(b':')
                if middle == -1:
                    #Nothing to do, no more case
                    raise PayloadError(f'Invalid header line: {line!r}')
                
                name = line[:middle]
                value = line[middle+1:]
                
                # read a chunk again
                if chunks:
                    offset = self._offset
                else:
                    if self.eof:
                        raise EOFError(b'')
                    
                    await self._wait_for_data()
                    offset = 0
                
                chunk = chunks[0]
                break
        
        else:
            name = chunk[offset:middle].lstrip()
            value = chunk[middle+1:end].strip()
            offset = end+2
        
        name = name.decode('utf-8','surrogateescape')
        
        while True:
            if chunk[offset] in (b'\t'[0], b' '[0]):
                # continous, I hate it!
                value = [value]
                while True:
                    end = chunk.find(b'\r\n',offset)
                    if end == -1:
                        self._offset = offset
                        line = await self.readtill_CRLF()
                        if not line:
                            headers[name] = b' '.join(value).decode('utf-8','surrogateescape')
                            return headers
                        
                        value.append(line.strip())
                        
                        if chunks:
                            offset = self._offset
                        else:
                            if self.eof:
                                raise EOFError(b'')
                                
                            await self._wait_for_data()
                            offset = 0
                            
                        chunk = chunks[0]
                        
                        if chunk[offset] in (b'\t'[0], b' '[0]):
                            continue
                        
                        value = b' '.join(value)
                        break
                    
                    value.append(chunk[offset:end].strip())
                    offset = end+2
                    
                    if offset == len(chunk):
                        del chunks[0]
                        if not chunks:
                            if self.eof:
                                raise EOFError(b'')
                                
                            await self._wait_for_data()
                        
                        chunk = chunks[0]
                        offset = 0
                    
                    if chunk[offset] in (b'\t'[0], b' '[0]):
                        continue
                    
                    value = b' '.join(value)
                    break
            
            headers[name] = value.decode('utf-8','surrogateescape')
            
            middle = chunk.find(b':',offset)
            end = chunk.find(b'\r\n',middle)
            
            if end == -1:
                if len(chunk) == offset:
                    del chunks[0]
                    if not chunks:
                        if self.eof:
                            raise EOFError(b'')
                    
                        await self._wait_for_data()
                    
                    chunk = chunks[0]
                    offset = 0
                    
                    middle = chunk.find(b':')
                    end = chunk.find(b'\r\n',middle)
                    if end == -1:
                        self._offset = offset
                        line = await self.readtill_CRLF()
                        if not line:
                            return headers
                        
                        middle = line.find(b':')
                        if middle == -1:
                            raise PayloadError(f'Invalid header line: {line!r}')
                        
                        name = line[:middle].lstrip().decode('utf-8','surrogateescape')
                        value = line[middle+1:].strip()
                        
                        if chunks:
                            offset = self._offset
                        else:
                            if self.eof:
                                raise EOFError(b'')
                            
                            await self._wait_for_data()
                            offset = 0
                        
                        chunk = chunks[0]
                        continue
                    
                    else:
                        name = chunk[:middle].lstrip().decode('utf-8','surrogateescape')
                        value = chunk[middle+1:end].strip()
                        
                        offset = end+2
                        if offset == len(chunk):
                            del chunks[0]
                            if not chunks:
                                if self.eof:
                                    raise EOFError(b'')
                            
                                await self._wait_for_data()
                            
                            chunk = chunks[0]
                            offset = 0
                        
                        continue
                        
                else:
                    self._offset = offset
                    line = await self.readtill_CRLF()
                    if not line:
                        return headers
                    
                    middle = line.find(b':')
                    if middle == -1:
                        raise PayloadError(f'Invalid header line: {line!r}')
                    
                    name = line[:middle].lstrip().decode('utf-8','surrogateescape')
                    value = line[middle+1:].strip()
                    
                    if chunks:
                        offset = self._offset
                    else:
                        if self.eof:
                            raise EOFError(b'')
                        
                        await self._wait_for_data()
                        offset = 0
                    
                    chunk = chunks[0]
                    continue
                
            else:
                name = chunk[offset:middle].lstrip().decode('utf-8','surrogateescape')
                value = chunk[middle+1:end].strip()
            
            offset = end+2
            if offset == len(chunk):
                del chunks[0]
                if not chunks:
                    if self.eof:
                        raise EOFError(b'')
                    
                    await self._wait_for_data()
                
                offset = 0
                chunk = chunks[0]
            
            continue

        
class WebSocketCommonProtocol(object):
    __slots__=('_connection_lost', '_drain_lock', '_drain_waiter', '_paused',
        'close_code', 'close_connection_task', 'close_reason',
        'connection_lost_waiter', 'extensions', 'host', 'legacy_recv', 'loop',
        'max_queue', 'max_size', 'messages', 'over_ssl', 'pings', 'port',
        'read_limit', 'reader', 'secure', 'state', 'subprotocol', 'timeout',
        'transfer_data_exc', 'transfer_data_task', 'write_limit', 'writer')
    
    is_client = True #placeholder for subclasses
    
    def __init__(self, loop, host, port, *, secure=None, timeout=10.,
            max_size=1<<26, max_queue=None, read_limit=1<<16, write_limit=1<<16,
            legacy_recv=False):
        
        self.host = host
        self.port = port
        self.secure = secure
        self.timeout = timeout
        self.max_size = max_size #set it to a BIG number if u wanna ignore max size
        self.max_queue = max_queue
        self.read_limit = read_limit
        self.write_limit = write_limit

        self.loop = loop

        self.legacy_recv = legacy_recv

        self._paused = False
        self._drain_waiter = None
        self._connection_lost = False
        
        self.reader = StreamReader(loop)
        self.writer = None #we will set it later
        self.over_ssl = False #we will set it latet

        self._drain_lock = Future(loop)
        self._drain_lock.set_result(None)

        self.state = CONNECTING

        self.extensions  = None #set from outside
        self.subprotocol = None #set from outside

        self.close_code = 0
        self.close_reason = ''


        self.connection_lost_waiter=Future(loop)
        self.messages = AsyncQue(loop=loop,maxlen=max_queue)

        self.pings = OrderedDict()

        self.transfer_data_task = None
        self.transfer_data_exc = None
        self.close_connection_task = None

    def connection_open(self):
        self.state = OPEN
        self.transfer_data_task     = Task(self.transfer_data(),self.loop)
        self.close_connection_task  = Task(self.close_connection(),self.loop)

    @property
    def local_address(self):
        if self.writer is None:
            return None
        return self.writer.get_extra_info('sockname')

    @property
    def remote_address(self):
        if self.writer is None:
            return None
        return self.writer.get_extra_info('peername')

    @property
    def open(self):
        return self.state is OPEN and not self.transfer_data_task.done()

    @property
    def closed(self):
        return self.state is CLOSED

    #await it
    def recv(self):
        return self.messages.result()

    def recv_no_wait(self):
        return self.messages.result_no_wait()
    
    async def send(self,data):
        await self.ensure_open()

        if isinstance(data,(bytes,bytearray,memoryview)):
            opcode=OP_BINARY
        elif type(data) is str:
            opcode=OP_TEXT
            data=data.encode('utf-8')
        else:
            raise TypeError(f'data must be bytes or str, got: {data.__class__.__name__}')

        await self.write_frame(opcode,data)

    async def close(self, code=1000, reason=''):
        #if no close frame is received within the timeout
        #we cancel the connection
        try:
            task=Task(self.write_close_frame(self._serialize_close(code,reason)),self.loop)
            future_or_timeout(task,self.timeout)
            await task
        except TimeoutError:
            self.fail_connection()

        try:
            #if close() is cancelled during the wait, self.transfer_data_task
            #is cancelled before the timeout elapses
            task=self.transfer_data_task
            future_or_timeout(task,self.timeout)
            await task
        except (TimeoutError,CancelledError):
            pass
        
        #quit for the close connection task to close the TCP connection.
        await shield(self.close_connection_task,self.loop)

    @staticmethod
    def _serialize_close(code,reason):
        if not (code in EXTERNAL_CLOSE_CODES or 2999<code<5000):
            raise WebSocketProtocolError(f'Invalid status code {code}')
        return code.to_bytes(2,'big')+reason.encode('utf-8')
    
    async def ping(self,data=b''):
        await self.ensure_open()

        if type(data) is str:
            data.encode('utf-8')

        # Protect against duplicates if a payload is explicitly set.
        if data in self.pings:
            raise ValueError('Already waiting for a pong with the same data')

        # Generate a unique random payload otherwise.
        while data in self.pings:
            data=getrandbits(32).to_bytes(4,'big')

        self.pings[data]=Future(self.loop)

        await self.write_frame(OP_PING,data)

        return shield(self.pings[data],self.loop)
    
    async def pong(self,data=b''):
        await self.ensure_open()
        if type(data) is str:
            data.encode('utf-8')
        await self.write_frame(OP_PONG,data)
    
    # Private methods - no guarantees.
    
    async def ensure_open(self):
        if self.state is OPEN:
            #if self.transfer_data_task exited without a closing handshake.
            if self.transfer_data_task.done():
                await shield(self.close_connection_task,self.loop)
                raise ConnectionClosed(self.close_code,None,self.close_reason)
            return

        if self.state is CLOSED:
            raise ConnectionClosed(self.close_code,None,self.close_reason) from self.transfer_data_exc

        if self.state is CLOSING:
            if not self.close_code:
                #if we started the closing handshake, wait for its completion
                await shield(self.close_connection_task,self.loop)
            raise ConnectionClosed(self.close_code,None,self.close_reason) from self.transfer_data_exc

        raise Exception('WebSocket connection isn\'t established yet')
    
    async def transfer_data(self):
        try:
            while True:
                message = await self.read_message()
                #exit the loop when receiving a close frame.
                if message is None:
                    break
                
                self.messages.set_result(message)
        except CancelledError as err:
            #we alrady failed connection
            exception=ConnectionClosed(self.close_code or 1000, err, self.close_reason)
        
        except WebSocketProtocolError as err:
            exception=ConnectionClosed(1002,err)
            self.fail_connection(1002)
            
        except (ConnectionError, EOFError) as err:
            exception=ConnectionClosed(1006,err)
            self.fail_connection(1006)

        except UnicodeDecodeError as err:
            exception=ConnectionClosed(1007,err)
            self.fail_connection(1007)

        except PayloadError as err:
            exception=ConnectionClosed(1009,err)
            self.fail_connection(1009)

        except BaseException as err:
            await self.loop.render_exc_async(err, [
                'Unexpected exception occured at ',
                repr(self),
                '.transfer_data\n',
                    ])
            #should not happen
            exception=ConnectionClosed(1011,err)
            self.fail_connection(1011)
        
        else:
            # connection wa closed
            exception = ConnectionClosed(self.close_code or 1000, None, self.close_reason)
            
            # If we are a client and we receive this, we closed our own
            # connection, there is no reason to wait for TCP abort
            if self.is_client:
                self.connection_lost_waiter.set_result_if_pending(None)
            
        if self.transfer_data_exc is None:
            self.transfer_data_exc=exception
            self.messages.set_exception(exception)

    async def read_message(self):
        frame = await self.read_data_frame(max_size=self.max_size)
        if frame is None: #close frame
            return

        if frame.opcode == OP_TEXT:
            text = True
        elif frame.opcode == OP_BINARY:
            text = False
        else: #frame.opcode == OP_CONT:
            raise WebSocketProtocolError('Unexpected opcode')
        
        #we got a whole frame, nice
        if frame.fin:
            return frame.data.decode('utf-8') if text else frame.data
        
        max_size=self.max_size #set max size to BIG number to ignore it
        chunks=[]
        
        if text:
            decoder = codecs.getincrementaldecoder('utf-8')(errors='strict')
            append=lambda frame : chunks.append(decoder.decode(frame.data,frame.fin))
        else:
            append=lambda frame : chunks.append(frame.data)
        
        while True:
            append(frame)
            max_size-=len(frame.data)

            if frame.fin:
                break
            
            frame = await self.read_data_frame(max_size=max_size)
            if frame is None:
                raise WebSocketProtocolError('Incomplete fragmented message')
            if frame.opcode!=OP_CONT:
                raise WebSocketProtocolError('Unexpected opcode')
        
        return ('' if text else b'').join(chunks)

    async def read_data_frame(self,max_size):
        while True:
            frame = await Frame.read(self,max_size)
            
            #most likely
            if frame.opcode in DATA_OPCODES:
                return frame

            if (await self._process_CTRL_frame(frame)):
                continue
            return

    async def _process_CTRL_frame(self,frame):
        opcode=frame.opcode
        if opcode==OP_CLOSE:
            data=frame.data
            length=len(data)
            if length>=2:
                code=int.from_bytes(data[:2],'big')
                if not (code in EXTERNAL_CLOSE_CODES or 2999<code<5000):
                    raise WebSocketProtocolError(f'Invalid status code {code}')
                reason=data[2:].decode('utf-8')
                self.close_code=code
                self.close_reason=reason
            elif length==0:
                self.close_code=1005
            else:
                raise WebSocketProtocolError(f'Close frame too short: {length}')

            await self.write_close_frame(frame.data)
            return False

        if opcode==OP_PING:
            await self.pong(frame.data)
            return True

        #opcode==OP_PONG:
        if frame.data in self.pings:
            #checking all pings up to the one matching this pong.
            ping_id=b''
            while ping_id!=frame.data:
                ping_id,pong_waiter=self.pings.popitem(0)
                pong_waiter.set_result(None)
        return True

    async def write_frame(self,opcode,data,_expected_state=OPEN):
        # Defensive assertion for protocol compliance.
        if self.state is not _expected_state:
            raise Exception(f'Cannot write to a WebSocket in the {self.state} state')

        #we write only 1 frame at a time, so we 'queue' it
        old_lock=self._drain_lock
        new_lock=Future(self.loop)
        self._drain_lock=new_lock
        await old_lock
        try:
            frame=Frame(True,opcode,data)
            frame.write(self)
            await self.writer.drain()
        except ConnectionError:
            self.fail_connection()
            #raise ConnectionClosed with the correct code and reason.
            await self.ensure_open()
        finally:
            new_lock.set_result(None)
            
    def writer_is_closing(self):
        return self.writer.transport.is_closing()

    async def write_close_frame(self, data=b''):
        #check connection before we write
        if self.state is OPEN:
            self.state = CLOSING
            await self.write_frame(OP_CLOSE, data, CLOSING)

    async def close_connection(self):
        try:
            # Wait for the data transfer phase to complete.
            if self.transfer_data_task is not None:
                try:
                    await self.transfer_data_task
                except (CancelledError,TimeoutError):
                    pass
            
            # Cancel all pending pings because they'll never receive a pong.
            for ping in self.pings.values():
                ping.cancel()
            
            # A client should wait for a TCP close from the server.
            if self.is_client and self.transfer_data_task is not None:
                if (await self.wait_for_connection_lost()):
                    return
            
            # If connection goes off meawhile connecting, writer can be set
            # to None.
            writer = self.writer
            if (writer is not None) and writer.can_write_eof():
                writer.write_eof()
                if (await self.wait_for_connection_lost()):
                    return
        finally:
            #finally ensures that the transport never remains open
            if self.connection_lost_waiter.done() and not self.secure:
                return
            
            #Close the TCP connection
            writer = self.writer
            if (writer is not None):
                writer.close()
                if (await self.wait_for_connection_lost()):
                    return
                #Abort the TCP connection
                writer.transport.abort()
            #connection_lost() is called quickly after aborting.
            await self.wait_for_connection_lost()
            
    async def wait_for_connection_lost(self):
        if self.connection_lost_waiter.pending():
            try:
                task=shield(self.connection_lost_waiter,self.loop)
                future_or_timeout(task,self.timeout)
                await task
            except TimeoutError:
                pass
                
        #re-check self.connection_lost_waiter.done() synchronously because
        #connection_lost() could run between the moment the timeout occurs
        #and the moment this coroutine resumes running.
        return self.connection_lost_waiter.done()

    def fail_connection(self, code=1006, reason=''):
        #cancel transfer_data_task if the opening handshake succeeded
        if self.transfer_data_task is not None:
            self.transfer_data_task.cancel()

        #send a close frame when the state is OPEN and the connection is not
        #broken
        if code!=1006 and self.state is OPEN:

            frame_data = self._serialize_close(code,reason)
            #Write the close frame without draining the write buffer.
            self.state = CLOSING
            frame = Frame(True,OP_CLOSE,frame_data)
            frame.write(self)

        #start close_connection_task if the opening handshake didn't succeed.
        close_task=self.close_connection_task
        if close_task is None:
            close_task=Task(self.close_connection(),self.loop)
            self.close_connection_task=close_task
            
        return close_task

    #compability method
    def connection_made(self, transport):
        transport.set_write_buffer_limits(self.write_limit)
        self.reader.set_transport(transport)
        self.over_ssl = (transport.get_extra_info('sslcontext') is not None)
        self.writer = StreamWriter(self.loop,transport,self,self.reader)

    #compability method
    def connection_lost(self,exception):
        self.state = CLOSED
        if not self.close_code:
            self.close_code = 1006
        
        # `self.connection_lost_waiter` should be pending
        self.connection_lost_waiter.set_result_if_pending(None)
        
        if self.reader is not None:
            if exception is None:
                self.reader.feed_eof()
            else:
                self.reader.set_exception(exception)

        self._connection_lost=True
        #wake up the writer if currently paused.
        if not self._paused:
            return
        
        waiter=self._drain_waiter
        if waiter is None:
            return
        
        self._drain_waiter=None
        if waiter.done():
            return
        
        if exception is None:
            waiter.set_result(None)
        else:
            waiter.set_exception(exception)

    #compability method
    def pause_writing(self):
        self._paused = True

    #compability method
    def data_received(self,data):
        self.reader.feed_data(data)

    #compability method
    def eof_received(self):
        self.reader.feed_eof()
        return (not self.over_ssl)

    #compability method
    def resume_writing(self):
        self._paused = False

        waiter = self._drain_waiter
        if waiter is None:
            return
        
        self._drain_waiter = None
        if waiter.pending():
            waiter.set_result(None)

    #compability method
    async def _drain_helper(self):
        if self._connection_lost:
            raise ConnectionResetError('Connection lost')
        if not self._paused:
            return
        waiter = Future(self.loop)
        self._drain_waiter = waiter
        await waiter
        
class WebSocketURI(object):
    __slots__= ('host', 'port', 'resource_name', 'secure', 'user_info',)
    def __init__(self,uri):
        uri = urllib.parse.urlparse(uri)

        self.secure  = (uri.scheme == 'wss')
        self.host    = uri.hostname
        self.port    = uri.port or (443 if self.secure else 80)
        
        resource_name = uri.path or '/'
        if uri.query:
            resource_name=f'{resource_name}?{uri.query}'
        self.resource_name=resource_name
        
        if uri.username or uri.password:
            self.user_info = (uri.username,uri.password)
        else:
            self.user_info = None

class WSClient(WebSocketCommonProtocol):
    is_client = True

    async def __new__(cls, loop, uri, *, origin=None, available_extensions=None,
            available_subprotocols=None, extra_headers=None, compression=None,
            connection_kwargs=None, websocket_kwargs=None):

        if connection_kwargs is None:
            connection_kwargs={}
        if websocket_kwargs is None:
            websocket_kwargs={}
        
        wsuri = WebSocketURI(uri)
        if wsuri.secure:
            connection_kwargs.setdefault('ssl',True)
        elif connection_kwargs.get('ssl',None) is not None:
            raise ValueError(f'{cls.__name__}() received a SSL context for a ws:// URI, use a wss:// URI to enable TLS')
        
        if compression is not None and compression!='deflate':
            raise ValueError(f'Unsupported compression: {compression}')

        if connection_kwargs.get('sock') is None:
            host=wsuri.host
            port=wsuri.port
        else:
            #if sock is given, host and port must be None
            host=None
            port=None

        #init
        self=object.__new__(cls)
        WebSocketCommonProtocol.__init__(self,loop,host,port,**websocket_kwargs)
        
        try:
            await loop.create_connection(self,host,port,**connection_kwargs)
            
            #building headers
            sec_key=b64encode(int.to_bytes(getrandbits(128),length=16,byteorder='big')).decode()
            request_headers = multidict_titled()
            
            request_headers[UPGRADE]='websocket'
            request_headers[CONNECTION]='Upgrade'
            request_headers[SEC_WEBSOCKET_KEY]=sec_key
            request_headers[SEC_WEBSOCKET_VERSION]='13'
            
            if wsuri.port == (443 if wsuri.secure else 80):
                request_headers[HOST] = wsuri.host
            else:
                request_headers[HOST] = f'{wsuri.host}:{wsuri.port}'
            
            if wsuri.user_info is not None:
                request_headers[AUTHORIZATION]=build_basic_auth(*wsuri.user_info)
                
            if origin is not None:
                request_headers[ORIGIN]=origin

            if available_extensions is not None:
                request_headers[SEC_WEBSOCKET_EXTENSIONS]=build_extensions(available_extensions)
                
            if available_subprotocols is not None:
                request_headers[SEC_WEBSOCKET_PROTOCOL]=build_subprotocols(available_subprotocols)

            if extra_headers is not None:
                if isinstance(extra_headers,multidict_titled) or hasattr(extra_headers,'items'): #we use expecially items, so we check that
                    for name,value in extra_headers.items():
                        request_headers[name]=value
                else:
                    raise TypeError(f'extra_headers should be dictlike with \'.items\' method, got {extra_headers.__class__.__name__} instance.')
            
            self.writer.write_http_request(METH_GET, wsuri.resource_name, request_headers)
            
            #parse status line
            message = await self.reader.read_http_response()
           
            if message.version != HttpVersion11:
                raise ValueError(f'Unsupported HTTP version: {message.version}')

            if message.status!=101:
                raise InvalidHandshake(f'Invalid status code: {message.status}')
            
            response_headers = message.headers
            connections=[]
            received_connections=response_headers.getall(CONNECTION,)
            if (received_connections is not None):
                for received_connection in received_connections:
                    connections.extend(parse_connections(received_connection))
            
            if not any(value.lower()=='upgrade' for value in connections):
                raise InvalidHandshake(f'Invalid connection, no upgrade found, got {connections!r}')
            
            upgrade=[]
            received_upgrades=response_headers.getall(UPGRADE)
            if (received_upgrades is not None):
                for received_upgrade in received_upgrades:
                    upgrade.extend(parse_upgrades(received_upgrade))
            
            if len(upgrade)!=1 and upgrade[0].lower()!='websocket': #ignore upper/lover case
                raise InvalidHandshake(f'Expected \'WebSocket\' for \'Upgrade\', but got {upgrade!r}')

            expected_key=b64encode(hashlib.sha1((sec_key+WS_KEY).encode()).digest()).decode()
            received_keys=response_headers.getall(SEC_WEBSOCKET_ACCEPT)
            if received_keys is None:
                raise InvalidHandshake(f'Expected 1 secret key \'{expected_key}\', but received 0')
            if len(received_keys)>1:
                raise InvalidHandshake(f'Expected 1 secret key \'{expected_key}\', but received more : {received_keys}')
            
            received_key=received_keys[0]
            if received_key!=expected_key:
                raise InvalidHandshake(f'Expected secret key \'{expected_key}\', but got \'{received_key}\'')

            #extensions
            accepted_extensions=[]
            received_extensions=response_headers.getall(SEC_WEBSOCKET_EXTENSIONS)
            if (received_extensions is not None):
                if available_extensions is None:
                    raise InvalidHandshake(f'No extensions supported, but received {received_extensions!r}')
                
                parsed_extension_values=[]
                for value in received_extensions:
                    parsed_extension_values.extend(parse_extensions(value))
                
                for name,params in parsed_extension_values:
                    for extension in available_extensions:
                        #do names and params match?
                        if extension.name==name and extension.are_valid_params(params,accepted_extensions):
                            accepted_extensions.append(extension)
                            break
                    else:
                        #no matching extension
                        raise InvalidHandshake(f'Unsupported extension: name = {name}, params = {params}')

            self.extensions=accepted_extensions

            subprotocol = None
            received_subprotocols=response_headers.getall(SEC_WEBSOCKET_PROTOCOL)
            if (received_subprotocols is not None):
                if available_subprotocols is None:
                    raise InvalidHandshake('No subprotocols supported, btu received {received_subprotocol!r}')
                
                parsed_subprotocol_values=[]
                for received_subprotocol in received_subprotocols:
                    parsed_subprotocol_values.extend(parse_subprotocols(received_subprotocol))
                
                if len(parsed_subprotocol_values)>1:
                    raise InvalidHandshake(f'Multiple subprotocols: {parsed_subprotocol_values!r}')
                
                subprotocol=parsed_subprotocol_values[0]
                
                if subprotocol not in available_subprotocols:
                    raise InvalidHandshake(f'Unsupported subprotocol: {subprotocol}')

            self.subprotocol=subprotocol

            self.connection_open()
        except:
            await self.fail_connection()
            raise
        
        return self
    
    def __call__(self):
        return self

class WSServerProtocol(WebSocketCommonProtocol):
    is_client = False
    
    __slots__ = ('available_extensions', 'available_subprotocols',
        'extra_headers', 'handler', 'handler_task', 'origin', 'origins',
        'request_processer', 'server', 'subprotocol_selector',
        'request', 'response_headers')
    
    def __init__(self,server):
        handler, host, port, secure, origins, available_extensions, \
        available_subprotocols , extra_headers, request_processer, \
        subprotocol_selector, websocket_kwargs = server.proto_args
        
        self.handler=handler
        self.server=server
        self.origins=origins
        self.available_extensions=available_extensions
        self.available_subprotocols=available_subprotocols
        self.extra_headers=extra_headers
        self.request_processer=request_processer
        self.subprotocol_selector=subprotocol_selector
        self.handler_task=None
        
        WebSocketCommonProtocol.__init__(self, server.loop, host, port,
            secure=secure, **websocket_kwargs)
        
        self.request=None
        self.response_headers=None
        self.origin=None
        
    def connection_made(self, transpot):
        WebSocketCommonProtocol.connection_made(self,transpot)
        self.server.register(self)
        self.handler_task=Task(self.lifetime_handler(),self.loop)
        
    async def lifetime_handler(self):
        try:
            # handshake returns True if it succeeded
            if not (await self.handshake()):
                return
            
            try:
                await self.handler(self)
            except BaseException as err:
                await self.loop.render_exc_async(err,before = [
                    'Unhandled exception occured at',
                    self.__class__.__name__,
                    '.lifetime_handler meanhile running: ',
                    repr(self.handler),
                    '\n',
                        ])
                return
            
            await self.close()
        except:
            # We will let Task.__del__ to render the exception...
            writer=self.writer
            if writer is None:
                raise
            
            transport=writer.transport
            if transport is None:
                raise
                
            transport.close()
            raise
        
        finally:
            self.server.unregister(self)
    
    async def handshake(self):
        try:
            self.request = request =await self.reader.read_http_request()
            
            request_headers=request.headers
            if self.server.is_serving():
                path=request.path
                
                request_processer=self.request_processer
                if request_processer is None:
                    early_response=None
                else:
                    early_response=request_processer(path, request_headers)
                    if iscoroutine(early_response):
                        early_response=await early_response
                
                if (early_response is not None):
                    raise AbortHandshake(*early_response)
                
            else:
                raise AbortHandshake(SERVICE_UNAVAILABLE,multidict_titled(),b'Server is shutting down.\n',)
            
            connections=[]
            connection_headers=request_headers.getall(CONNECTION)
            if (connection_headers is not None):
                for connection_header in connection_headers:
                    connections.extend(parse_connections(connection_header))
        
            if not any(value.lower()=='upgrade' for value in connections):
                raise InvalidUpgrade(f'Invalid connection, no upgrade found, got {connections!r}')
            
            upgrade=[]
            upgrade_headers=request_headers.getall(UPGRADE)
            if (upgrade_headers is not None):
                for upgrade_header in upgrade_headers:
                    upgrade.extend(parse_upgrades(upgrade_header))
            
            if len(upgrade)!=1 and upgrade[0].lower()!='websocket': #ignore upper/lover case
                raise InvalidUpgrade(f'Expected \'WebSocket\' for \'Upgrade\', but got {upgrade!r}')
            
            received_keys=request_headers.getall(SEC_WEBSOCKET_KEY)
            if received_keys is None:
                raise InvalidHandshake(f'Missing {SEC_WEBSOCKET_KEY!r} from headers')
            
            if len(received_keys)>1:
                raise InvalidHandshake(f'Multiple {SEC_WEBSOCKET_KEY!r} values at headers')
            
            key=received_keys[0]
        
            try:
                raw_key = b64decode(key.encode(),validate=True)
            except BinasciiError:
                raise InvalidHandshake(f'Invalid {SEC_WEBSOCKET_KEY!r}: {key!r}')
            
            if len(raw_key)!=16:
                raise InvalidHandshake(f'Invalid {SEC_WEBSOCKET_KEY!r}, should be length 16; {key!r}')
        
            sw_version=request_headers.getall(SEC_WEBSOCKET_VERSION)
            if sw_version is None:
                raise InvalidHandshake(f'Missing {SEC_WEBSOCKET_VERSION!r} values at headers')
            
            if len(sw_version)>1:
                raise InvalidHandshake(f'Multiple {SEC_WEBSOCKET_VERSION!r} values at headers')
            
            sw_version=sw_version[0]
            if sw_version != "13":
                raise InvalidHandshake(f'Invalid {SEC_WEBSOCKET_VERSION!r}: {sw_version!r}')
            
            while True:
                origins=self.origins
                if (origins is None):
                    origin=None
                    break
                
                origin_headers=request_headers.getall(ORIGIN)
                
                if (origin_headers is None):
                    raise InvalidOrigin('No origin at header.')
                
                if len(origin_headers)>1:
                    raise InvalidOrigin('More than 1 origin at header.')
                
                origin=origin_headers[0]
                
                if origin in origins:
                    break
                    
                raise InvalidOrigin(origin)
            
            self.origin=origin
            
            while True:
                accepted_extensions=[]
                
                available_extensions=self.available_extensions
                if (available_extensions is None):
                    extension_header=None
                    break
                
                extension_headers_=request_headers.getall(SEC_WEBSOCKET_EXTENSIONS)
                if (extension_headers_ is None):
                    extension_header=None
                    break
                
                extension_headers=[]
                parsed_extension_values=[]
                for extension_header_ in extension_headers_:
                    parsed_extension_values.extend(parse_extensions(extension_header_))
                
                for name,params in parsed_extension_values:
                    for extension in available_extensions:
                        #do names and params match?
                        if extension.name==name and extension.are_valid_params(params,accepted_extensions):
                            accepted_extensions.append(extension)
                            extension_headers.append((name,params))
                            break
                    else:
                        #no matching extension
                        raise InvalidHandshake(f'Unsupported extension: name = {name}, params = {params}')
                    
                    # If we didn't break from the loop, no extension in our list
                    # matched what the client sent. The extension is declined.
        
                # Serialize extension header.
                if extension_headers:
                    extension_header=build_extensions(extension_headers)
                    break
                
                extension_header=None
                break
            
            self.extensions=accepted_extensions
            
            
            while True:
                available_subprotocols=self.available_subprotocols
                if (available_subprotocols is None):
                    subprotocol_header=None
                    break
                    
                protocol_headers=request_headers.getall(SEC_WEBSOCKET_PROTOCOL)
                if (protocol_headers is None):
                    subprotocol_header=None
                    break
                
                parsed_header_subprotocols=[]
                for protocol_header in protocol_headers:
                    parsed_header_subprotocols.extend(parse_subprotocols(protocol_header))
                
                subprotocol_selector=self.subprotocol_selector
                if (subprotocol_selector is not None):
                    subprotocol_header=subprotocol_selector(parsed_header_subprotocols,available_subprotocols)
                    break
                    
                subprotocols=set(parsed_header_subprotocols)
                subprotocols.intersection_update(available_subprotocols)
                
                if not subprotocols:
                    subprotocol_header=None
                    break
                    
                subprotocol_header=sorted(subprotocols, key = lambda priority: (parsed_header_subprotocols.index(priority)+available_subprotocols.index(priority)))[0]
                break
            
            self.subprotocol=subprotocol_header
            
            response_headers = multidict_titled()
    
            response_headers[UPGRADE] = 'websocket'
            response_headers[CONNECTION] = 'Upgrade'
            response_headers[SEC_WEBSOCKET_ACCEPT] = b64encode(hashlib.sha1((key+WS_KEY).encode()).digest()).decode()
            
            if (extension_header is not None):
                response_headers[SEC_WEBSOCKET_EXTENSIONS] = extension_header
    
            if (subprotocol_header is not None):
                response_headers[SEC_WEBSOCKET_PROTOCOL] = subprotocol_header
            
            extra_headers=self.extra_headers
            if (extra_headers is not None):
                for key, value in extra_headers.items():
                    response_headers[key] = value
    
            response_headers.setdefault(DATE, formatdate(usegmt=True))
            response_headers.setdefault(SERVER, '')
            
            self.response_headers = response_headers
            self.writer.write_http_response(SWITCHING_PROTOCOLS, response_headers)
            
            self.connection_open()
        except (CancelledError, ConnectionError) as err:
            await self.loop.render_exc_async(err,before = [
                'Unhandled exception occured at ',
                self.__class__.__name__,
                '.handshake, when handshaking:\n'])
            return False
        except BaseException as err:
            if isinstance(err,AbortHandshake):
                status=err.status
                headers=err.headers
                body=err.body
            elif isinstance(err,InvalidOrigin):
                status=FORBIDDEN
                headers=multidict_titled()
                body=f'Failed to open a WebSocket connection: {err}.\n'.encode()
            elif isinstance(err,InvalidUpgrade):
                status=UPGRADE_REQUIRED
                headers=multidict_titled()
                headers[UPGRADE]='websocket'
                body = (
                    f'Failed to open a WebSocket connection: {err}.\n\n'
                    f'You cannot access a WebSocket server directly with a '
                    f'browser. You need a WebSocket client.\n'
                        ).encode()
            elif isinstance(err,InvalidHandshake):
                status=BAD_REQUEST
                headers=multidict_titled()
                body=f'Failed to open a WebSocket connection: {err}.\n'.encode()
            else:
                status=INTERNAL_SERVER_ERROR
                headers=multidict_titled()
                body=b'Failed to open a WebSocket connection.\n'
                
            headers.setdefault(DATE             , formatdate(usegmt=True))
            headers.setdefault(SERVER           , '')
            headers.setdefault(CONTENT_LENGTH   , repr(len(body)))
            headers.setdefault(CONTENT_TYPE     , 'text/plain')
            headers.setdefault(CONNECTION       , 'close')
            
            try:
                self.writer.write_http_response(status, headers, body=body)
                self.fail_connection()
                await self.wait_for_connection_lost()
            except BaseException as err2:
                await self.loop.render_exc_async(err2,before = [
                    'Unhandled exception occured at ',
                    self.__class__.__name__,
                    '.handshake, when handling an other exception;',
                    repr(err),':'])
            return False
        
        return True
        
class WSServer(object):
    __slots__ = ('loop', 'websockets', 'close_connection_task','handler', 'server', 'proto_args')
    async def __new__(cls, loop, host, port, handler, *, protocol=None,
            compression=None, available_extensions=None, extra_headers=None,
            origins=None, available_subprotocols=None, request_processer=None,
            subprotocol_selector=None, websocket_kwargs=None, **kwargs):
        
        if protocol is None:
            protocol=WSServerProtocol
        
        if websocket_kwargs is None:
            websocket_kwargs={}
        
        secure = (kwargs.get("ssl") is not None)
        
        if (compression is not None):
            if compression!='deflate':
                raise ValueError(f'Unsupported compression: {compression}')
        
            if available_extensions is None:
                available_extensions=[]
        
        if (extra_headers is None):
            pass
        elif type(extra_headers) is multidict_titled:
            pass
        elif hasattr(type(extra_headers),'items'):
            extra_headers_local=multidict_titled()
            
            for name,value in extra_headers.items():
                extra_headers_local[name]=value
            
            extra_headers=extra_headers_local
        else:
            raise TypeError(f'extra_headers should be `None` or a dictlike with \'.items\' method, got {extra_headers.__class__.__name__} instance.')
        
        if (extra_headers is not None) and (not extra_headers):
            extra_headers=None
            
        self=object.__new__(cls)
        self.loop=loop
        self.handler=handler
        self.websockets=set()
        self.close_connection_task=None
        self.server = None
        self.proto_args = (handler, host, port, secure, origins,
            available_extensions, available_subprotocols , extra_headers,
            request_processer, subprotocol_selector, websocket_kwargs)
        
        factory = functools.partial(protocol, self,)
        server = await loop.create_server(factory, host, port, **kwargs)
        
        self.server = server
        await server.start()
        
        return self
    
    def register(self,protocol):
        self.websockets.add(protocol)
        
    def is_serving(self):
        server=self.server
        if server is None:
            return False
        
        if server.sockets is None:
            return False
        
        return True
    
    def close(self):
        close_connection_task = self.close_connection_task
        if close_connection_task is None:
            close_connection_task=Task(self._close(),self.loop)
            self.close_connection_task=close_connection_task
        
        return close_connection_task
    
    async def _close(self):
        server=self.server
        if server is None:
            return
        
        server.close()
        await server.wait_closed()
        
        loop=self.loop
        
        # Skip 1 full loop
        future=Future(loop)
        loop.call_at(0.0,future.set_result_if_pending,None)
        await future

        websockets=self.websockets
        if websockets:
            await WaitTillAll([websocket.close(1001) for websocket in websockets],loop)
            
        if websockets:
            await WaitTillAll([websocket.handler_task for websocket in websockets],loop)


