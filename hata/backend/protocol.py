# -*- coding: utf-8 -*-
import re, zlib
from random import getrandbits
from struct import Struct
from collections import deque

from .dereaddons_local import multidict_titled
from .futures import Future, CancelledError, Task, future_or_timeout

from .hdrs import CONNECTION, CONTENT_ENCODING, CONTENT_LENGTH, TRANSFER_ENCODING, METH_CONNECT
from .exceptions import PayloadError, WebSocketProtocolError, ContentEncodingError
from .helpers import HttpVersion, HttpVersion11

try:
    import brotli
except ImportError:
    brotli = None
    COMPRESSION_ERRORS = zlib.error
    BROTLI_DECOMPRESSOR = None
    BROTLI_COMPRESSOR = None
else:
    COMPRESSION_ERRORS = (zlib.error, brotli.error)
    
    if hasattr(brotli, 'Error'):
        # brotlipy case
        BROTLI_DECOMPRESSOR = brotli.Decompressor
        BROTLI_COMPRESSOR = brotli.Compressor
    else:
        # brotli case
        class BROTLI_DECOMPRESSOR(object):
            __slots__ = ('_decompressor', )
            def __init__(self):
                self._decompressor = brotli.Decompressor()
            
            def decompress(self, value):
                return self._decompressor.process(value)
        
        class BROTLI_COMPRESSOR(object):
            __slots__ = ('_compressor', )
            def __init__(self):
                self._compressor = brotli.Compressor()
            
            def compress(self, value):
                return self._compressor.process(value)

ZLIB_DECOMPRESSOR = zlib.decompressobj
ZLIB_COMPRESSOR = zlib.compressobj

WS_OP_CONT   = 0
WS_OP_TEXT   = 1
WS_OP_BINARY = 2

WS_OP_CLOSE  = 8
WS_OP_PING   = 9
WS_OP_PONG   = 10

WS_DATA_OPCODES = (WS_OP_CONT,  WS_OP_TEXT, WS_OP_BINARY)
WS_CTRL_OPCODES = (WS_OP_CLOSE, WS_OP_PING, WS_OP_PONG)

UNPACK_LEN2 = Struct('!H').unpack_from
UNPACK_LEN3 = Struct('!Q').unpack_from

PACK_LEN1   = Struct('!BB').pack
PACK_LEN2   = Struct('!BBH').pack
PACK_LEN3   = Struct('!BBQ').pack

HTTP_STATUS_RP = re.compile(b'HTTP/(\d)\.(\d) (\d\d\d)(?: (.*?))?\r\n')
HTTP_REQUEST_RP = re.compile(b'([^ ]+) ([^ ]+) HTTP/(\d)\.(\d)\r\n')

HTTP_STATUS_LINE_RP = re.compile(b'HTTP/(\d)\.(\d) (\d\d\d)(?: (.*?))?')
HTTP_REQUEST_LINE_RP = re.compile(b'([^ ]+) ([^ ]+) HTTP/(\d)\.(\d)')

CHUNK_LIMIT = 32
MAX_LINE_LENGTH = 8190

WRITE_CHUNK_LIMIT = 65536

CONNECTION_ERROR_EOF_NO_HTTP_HEADER = (
    'Stream closed before any data was received. (Might be caused by bad connection on your side, like the other side '
    'might have closed the stream before receiving the full payload.)'
        )

PAYLOAD_ERROR_EOF_AT_HTTP_HEADER = (
    'EOF received meanwhile reading http headers.'
        )

class RawMessage(object):
    __slots__ = ('_upgraded', 'headers', )
    
    @property
    def close_connection(self):
        try:
            connection = self.headers[CONNECTION]
        except KeyError:
            pass
        else:
            connection = connection.lower()
            if connection.lower() == 'keep-alive':
                return True
            
            if connection == 'close':
                return False
        
        return False # deside?
    
    def _get_upgraded(self):
        upgraded = self._upgraded
        if upgraded == 2:
            try:
                connection = self.headers[CONNECTION]
            except KeyError:
                upgraded = 0
            else:
                upgraded = (connection.lower() == 'upgrade')
            
            self._upgraded = upgraded
        
        return upgraded
    
    def _set_upgraded(self, value):
        self._upgraded = value
    
    upgraded = property(_get_upgraded, _set_upgraded)
    del _get_upgraded, _set_upgraded
    
    def set_upgraded(self, upgraded):
        self._upgraded = upgraded
    
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
        
        return encoding.lower()

class RawResponseMessage(RawMessage):
    __slots__ = ('version', 'status', 'reason',)
    
    def __init__(self, version, status, reason, headers):
        self.version = version
        self.status = status
        self.reason = reason
        self.headers = headers
        self._upgraded = 2

class RawRequestMessage(RawMessage):
    __slots__ = ('version', 'meth', 'path',)
    
    def __init__(self, version, meth, path, headers):
        self.version = version
        self.meth = meth
        self.path = path
        self.headers = headers
        self._upgraded = 2

#TODO: whats the fastest way on pypy ? casting 64 bit ints -> xor -> replace?
_XOR_TABLE = [bytes(a^b for a in range(256)) for b in range(256)]
def apply_mask(mask, data):
    data_bytes = bytearray(data)
    for index in range(4):
        data_bytes[index::4] = data_bytes[index::4].translate(_XOR_TABLE[mask[index]])
    return data_bytes

class Frame(object):
    __slots__ = ('data', 'head1',)
    def __init__(self, fin, opcode, data):
        self.data = data
        self.head1 = (fin<<7)|opcode
    
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
    
    def check(self):
        #check that this frame contains acceptable values.
        if self.head1&0b01110000:
            raise WebSocketProtocolError('Reserved bits must be 0')
        
        opcode = self.head1&0b00001111
        if opcode in WS_DATA_OPCODES:
            return
        
        if opcode in WS_CTRL_OPCODES:
            if len(self.data) > 125:
                raise WebSocketProtocolError('Control frame too long')
            if not self.head1&0b10000000:
                raise WebSocketProtocolError('Fragmented control frame')
            return
        
        raise WebSocketProtocolError(f'Invalid opcode: {opcode}')

class HTTPStreamWriter(object):
    __slots__ = ('size', 'chunked', 'compresser', 'eof', 'length', 'loop', 'protocol', 'transport', )
    def __init__(self, loop, protocol, compression, chunked):
        
        if (compression is None):
            compresser = None
        elif compression == 'gzip':
            compresser = zlib.compressobj(wbits=16+zlib.MAX_WBITS)
        elif compression == 'deflate':
            compresser = zlib.compressobj(wbits=zlib.MAX_WBITS)
        else:
            compresser = None
        
        self.compresser = compresser
        
        self.protocol = protocol
        self.transport = protocol.transport
        
        self.loop = loop
        self.length = None
        self.chunked = chunked
        self.size = 0
        
        self.eof = False
        self.compresser = None
    
    def _write(self, chunk):
        size = len(chunk)
        self.size += size
        
        transport = self.transport
        if (transport is None) or transport.is_closing():
            raise ConnectionResetError('Cannot write to closing transport')
        
        transport.write(chunk)
    
    async def write(self, chunk,):
        #Writes chunk of data to a stream.
        #
        #write_eof() indicates end of stream.
        #writer can't be used after write_eof() method being called.
        #write() return drain future.
        
        compresser = self.compresser
        if (compresser is not None):
            chunk = compresser.compress(chunk)
            if not chunk:
                return
        
        length = self.length
        if (length is not None):
            chunk_len = len(chunk)
            if length >= chunk_len:
                self.length = length-chunk_len
            else:
                chunk = chunk[:length]
                self.length=0
                if not chunk:
                    return
        
        if chunk:
            if self.chunked:
                chunk = b''.join([len(chunk).__format__('x').encode('ascii'), b'\r\n', chunk, b'\r\n'])
            
            self._write(chunk)
            
            if self.size > WRITE_CHUNK_LIMIT:
                self.size = 0
                protocol = self.protocol
                if protocol.transport is not None:
                    await protocol._drain_helper()
    
    async def write_eof(self, chunk=b''):
        if self.eof:
            return
        
        compresser = self.compresser
        if compresser is None:
            if self.chunked:
                if chunk:
                    chunk = b''.join([len(chunk).__format__('x').encode('ascii'), b'\r\n', chunk, b'\r\n0\r\n\r\n'])
                else:
                    chunk = b'0\r\n\r\n'
        else:
            if chunk:
                chunk = compresser.compress(chunk)
            
            chunk = chunk+compresser.flush()
            if chunk and self.chunked:
                chunk = b''.join([len(chunk).__format__('x').encode('ascii'), b'\r\n', chunk, b'\r\n0\r\n\r\n'])
        
        if chunk:
            self._write(chunk)
        
        protocol = self.protocol
        if protocol.transport is not None:
            await protocol._drain_helper()
        
        self.eof = True
        self.transport = None
    
    async def drain(self):
        #Flush the write buffer.
        #
        #The intended use is to write
        #
        #await w.write(data)
        #await w.drain()
        protocol = self.protocol
        if (protocol.transport is not None):
            await protocol._drain_helper()

class ReadProtocolBase(object):
    __slots__ = ('_chunks', '_eof', '_offset', '_paused', 'exception', 'loop', 'payload_reader',  'payload_waiter',
        'transport', )
    
    def __init__(self, loop):
        self.loop = loop
        self.transport = None
        self.exception = None
        self._chunks = deque()
        self._offset = 0
        self._eof = False
        self.payload_reader = None
        self.payload_waiter = None
        self._paused = False
    
    def __repr__(self):
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        if self._eof:
            result.append(' at eof')
            add_comma = True
        else:
            add_comma = False
        
        transport = self.transport
        if (transport is not None):
            if add_comma:
                result.append(', ')
            else:
                add_comma = True
            
            result.append(' transport=')
            result.append(repr(transport))
        
        exception = self.exception
        if (exception is not None):
            if add_comma:
                result.append(', ')
            else:
                add_comma = True
            
            result.append(' exception=')
            result.append(repr(exception))
        
        payload_reader = self.payload_reader
        if (payload_reader is not None):
            if add_comma:
                result.append(', ')
            
            result.append(' payload_reader=')
            result.append(repr(payload_reader))
        
        result.append('>')
        
        return ''.join(result)
    
    def should_close(self):
        if (self.payload_waiter is not None):
            return True
        
        if (self.exception is not None):
            return True
        
        if (not self._eof) and (self._offset or self._chunks):
            return True
        
        return False
    
    # compability method
    def connection_made(self, transport):
        self.transport = transport
    
    # compability method
    def connection_lost(self, exception):
        if exception is None:
            self.eof_received()
        else:
            self.set_exception(exception)
    
    def close(self):
        transport = self.transport
        if (transport is not None):
            transport.close()
    
    def get_extra_info(self, name, default=None):
        transport = self.transport
        if (transport is not None):
            return transport.get_extra_info(name, default)
    
    # read related
    @property
    def size(self):
        result = - self._offset
        for chunk in self._chunks:
            result += len(chunk)
        
        return result
    
    def _maybe_resume_tranport(self):
        if self._paused and len(self._chunks) < CHUNK_LIMIT:
            self._paused = False
            self.transport.resume_reading()
    
    def at_eof(self):
        if not self._eof:
            return False
        
        if (self.payload_reader is not None):
            return False
        
        if self.size:
            return False
    
        return True
    
    def set_exception(self, exception):
        self.exception = exception
        
        payload_waiter = self.payload_waiter
        if (payload_waiter is None):
            return
        
        self.payload_waiter = None
        payload_waiter.set_exception_if_pending(exception)
        
        self.payload_reader.close()
        self.payload_reader = None
    
    # compability method
    def eof_received(self):
        self._eof = True
        
        payload_reader = self.payload_reader
        if payload_reader is None:
            return
        
        try:
             payload_reader.throw(CancelledError())
        except CancelledError as err:
            new_exception = ConnectionError('Connection closed unexpectedly with EOF.')
            new_exception.__cause__ = err
            payload_waiter = self.payload_waiter
            self.payload_reader = None
            self.payload_waiter = None
            payload_waiter.set_exception_if_pending(new_exception)
        
        except StopIteration as err:
            args = err.args
            if not args:
                result = None
            elif len(args) == 1:
                result = args[0]
            else:
                result = args
            
            payload_waiter = self.payload_waiter
            self.payload_reader = None
            self.payload_waiter = None
            payload_waiter.set_result_if_pending(result)
        except GeneratorExit as err:
            payload_waiter = self.payload_waiter
            self.payload_reader = None
            self.payload_waiter = None
            exception = CancelledError()
            exception.__cause__ = err
            payload_waiter.set_exception_if_pending(exception)
        except BaseException as err:
            payload_waiter = self.payload_waiter
            self.payload_reader = None
            self.payload_waiter = None
            payload_waiter.set_exception_if_pending(err)
        
        return False
    
    # compability method
    def data_received(self, data):
        if not data:
            return
        
        payload_reader = self.payload_reader
        if (payload_reader is None):
            chunks = self._chunks
            chunks.append(data)
            if (len(chunks) > CHUNK_LIMIT) and (not self._paused):
                transport = self.transport
                if (transport is not None):
                    try:
                        transport.pause_reading()
                    except (AttributeError, NotImplementedError):
                        #cant be paused
                        self.transport = None
                    else:
                        self._paused = True
        else:
            try:
                payload_reader.send(data)
            except StopIteration as err:
                args = err.args
                if not args:
                    result = None
                elif len(args) == 1:
                    result = args[0]
                else:
                    result = args
                
                payload_waiter = self.payload_waiter
                self.payload_reader = None
                self.payload_waiter = None
                payload_waiter.set_result_if_pending(result)
            except GeneratorExit as err:
                payload_waiter = self.payload_waiter
                self.payload_reader = None
                self.payload_waiter = None
                exception = CancelledError()
                exception.__cause__ = err
                payload_waiter.set_exception_if_pending(exception)
            except BaseException as err:
                payload_waiter = self.payload_waiter
                self.payload_reader = None
                self.payload_waiter = None
                payload_waiter.set_exception_if_pending(err)
    
    # If you expect that the payload waiter will be cancelled from outside, call this method.
    def handle_payload_waiter_cancellation(self):
        payload_waiter = self.payload_waiter
        if (payload_waiter is not None):
            payload_waiter.add_done_callback(self._payload_waiter_cancellation_cb)
    
    def _payload_waiter_cancellation_cb(self, future):
        if future.cancelled():
            self.eof_received()
    
    def cancel_current_reader(self):
        """
        Cancels the current reader task of the protocol.
        """
        payload_reader = self.payload_reader
        if payload_reader is None:
            return
        
        self.payload_reader = None
        payload_reader.close()
        
        payload_waiter = self.payload_waiter
        self.payload_waiter = None
        payload_waiter.cancel()
    
    def set_payload_reader(self, payload_reader):
        assert self.payload_reader is None, 'Payload reader already set!'
        
        payload_waiter = Future(self.loop)
        exception = self.exception
        
        if (exception is None):
            try:
                payload_reader.send(None)
            except StopIteration as err:
                args = err.args
                if not args:
                    result = None
                elif len(args) == 1:
                    result = args[0]
                else:
                    result = args
                
                payload_waiter.set_result_if_pending(result)
            except GeneratorExit as err:
                exception = CancelledError()
                exception.__cause__ = err
                payload_waiter.set_exception_if_pending(exception)
            except BaseException as err:
                payload_waiter.set_exception_if_pending(err)
            
            else:
                self.payload_waiter = payload_waiter
                self.payload_reader = payload_reader
        else:
            payload_waiter.set_exception(exception)
        
        return payload_waiter
    
    async def read(self, n=-1):
        try:
            return await self.set_payload_reader(self._read_until_eof() if n < 0 else self._read_exactly(n))
        except EOFError as err:
            return err.args[0]
    
    async def readexactly(self, n):
        exception = self.exception
        if (exception is not None):
            raise exception
        
        if n < 1:
            if n == 0:
                return b''
            
            raise ValueError(f'`.readexactly` size can not be less than zero, got {n}.')
        
        return await self.set_payload_reader(self._read_exactly(n))
    
    async def readline(self):
        raise NotImplementedError
    
    async def readuntil(self):
        raise NotImplementedError
    
    async def readonce(self):
        """
        Waits till exactly one chunk is of data is received.
        
        Returns
        -------
        data : `bytes`
        
        Raises
        ------
        Any
            Connection lost exception if applicable.
        """
        exception = self.exception
        if (exception is not None):
            raise exception
        
        return await self.set_payload_reader(self._read_once())
    
    def _wait_for_data(self):
        if self._paused:
            self._paused = False
            self.transport.resume_reading()
        
        chunk = yield
        self._chunks.append(chunk)
        return chunk
    
    def _readtill_CRLF(self):
        exception = self.exception
        if (exception is not None):
            raise exception
        
        chunks = self._chunks
        
        if chunks:
            chunk = chunks[0]
        else:
            if self._eof:
                raise EOFError(b'')
            
            chunk = yield from self._wait_for_data()
        
        # Do first search outside, because we operate with offset
        offset = self._offset
        
        position = chunk.find(b'\r\n', offset)
        
        if position != -1:
            # We found!
            # Because the result must be bytes, we slice it
            collected = chunk[offset:position]
            # Add 2 to position to compensate CRLF
            position += 2
            
            # If the chunk is exhausted, remove it
            if len(chunk) == position:
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
                    if self._eof:
                        chunks.clear()
                        self._offset = 0
                        raise EOFError(b''.join(collected))
                    
                    chunk = yield from self._wait_for_data()
                
                if chunk[0] == b'\n'[0]:
                    # If size is 1, we delete it
                    if len(chunk) == 1:
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
                    if self._eof:
                        chunks.clear()
                        self._offset = 0
                        raise EOFError(b''.join(collected))
                    
                    chunk = yield from self._wait_for_data()
            
            # no offset search
            position = chunk.find(b'\r\n')
            
            # case 1: found in middle
            if position != -1:
                # cast memoryview
                collected.append(memoryview(chunk)[:position])
                
                # Add 2 position to ompensate CRLF
                position += 2
                # If the chunk is fully exhausted remove it
                if len(chunk) == position:
                    del chunks[0]
                    self._offset = 0
                # Fast slice the rest of the chunk with offset
                else:
                    self._offset = position
                
                return b''.join(collected)
            
            # collected the data
            collected.append(chunk)
            del chunks[0]
            n -= len(chunk)
            if n < 0:
                raise PayloadError(f'Header line exceeds max line length: {MAX_LINE_LENGTH!r} by {-n!r} and CRLF still '
                    f'not found.')
            
            continue
        
    def _read_exactly(self, n):
        if n < 1:
            if n < 0:
                raise ValueError(f'.readexactly called with negative `n`: {n!r}')
            else:
                return b''
        
        chunks = self._chunks
        if chunks:
            chunk = chunks[0]
            offset = self._offset
        else:
            if self._eof:
                raise EOFError(b'')
            
            chunk = yield from self._wait_for_data()
            offset = 0
        
        chunk_size = len(chunk)
        if offset == 0:
            if chunk_size > n:
                self._offset = n
                return chunk[:n]
            # chunk same size as the requested?
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
            # chunksize + offset end when the requested's end is.
            elif chunk_size == end:
                del chunks[0]
                self._offset = 0
                return chunk[offset:]
            
            else:
                n -= (chunk_size - offset)
                collected = [memoryview(chunk)[offset:]]
                del chunks[0]
        
        while True:
            if chunks:
                chunk = chunks[0]
            else:
                if self._eof:
                    self._offset = 0
                    raise EOFError(b''.join(collected))
                
                chunk = yield from self._wait_for_data()
            
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
    
    def _read_http_helper(self):
        chunks = self._chunks
        if chunks:
            chunk = chunks[0]
            offset = self._offset
        else:
            if self._eof:
                raise EOFError(b'')
            
            chunk = yield from self._wait_for_data()
            offset = 0
        
        return chunk, offset
    
    def _read_http_response(self):
        try:
            try:
                chunk, offset = yield from self._read_http_helper()
            except EOFError as err:
                args = err.args
                if (args is None) or (not args) or (not args[0]):
                    raise ConnectionError(CONNECTION_ERROR_EOF_NO_HTTP_HEADER)
                
                raise
            
            parsed = HTTP_STATUS_RP.match(chunk, offset)
            if parsed is None:
                # stupid fallback
                line = yield from self._readtill_CRLF()
                parsed = HTTP_STATUS_LINE_RP.fullmatch(line)
                if parsed is None:
                    raise PayloadError(f'Invalid status line: {line!r}.')
                
                chunk, offset = yield from self._read_http_helper()
            else:
                offset = parsed.end()
                
            major, minor, status, reason = parsed.groups()
            
            headers = yield from self._read_http_headers(chunk, offset)
            return RawResponseMessage(HttpVersion(int(major), int(minor)), int(status), reason, headers)
        except EOFError as err:
            raise PayloadError(PAYLOAD_ERROR_EOF_AT_HTTP_HEADER) from err
    
    def _read_http_request(self):
        try:
            try:
                chunk, offset = yield from self._read_http_helper()
            except EOFError as err:
                args = err.args
                if (args is None) or (not args) or (not args[0]):
                    raise ConnectionError(CONNECTION_ERROR_EOF_NO_HTTP_HEADER)
                
                raise
            
            parsed = HTTP_REQUEST_RP.match(chunk, offset)
            if parsed is None:
                # stupid fallback
                line = yield from self._readtill_CRLF()
                parsed = HTTP_REQUEST_LINE_RP.fullmatch(line)
                if parsed is None:
                    raise PayloadError(f'invalid request line: {line!r}')
                
                chunk, offset = yield from self._read_http_helper()
            else:
                offset = parsed.end()
            
            meth, path, major, minor = parsed.groups()
            
            headers = yield from self._read_http_headers(chunk, offset)
            path = path.decode('ascii', 'surrogateescape')
            return RawRequestMessage(HttpVersion(int(major), int(minor)), meth.upper().decode(), path, headers)
        except EOFError as err:
            raise PayloadError(PAYLOAD_ERROR_EOF_AT_HTTP_HEADER) from err
    
    def _read_http_headers(self, chunk, offset):
        headers = multidict_titled()
        chunks = self._chunks
        
        end = chunk.find(b'\r\n', offset)
        if end > offset:
            middle = chunk.find(b':', offset, end)
            if middle <= offset:
                raise PayloadError(f'Invalid header line: {chunk[offset:end]!r}')
            name = chunk[offset:middle].lstrip()
            value = chunk[middle+1:end].strip()
            offset = end+2
        
        # Found \r\n instantly, we done!
        elif end == offset:
            # If we are at the end of a chunk, remove it and save the offset.
            offset +=2
            if offset == len(chunk):
                del chunks[0]
                offset = 0
            
            self._offset = offset
            return headers
        else:
            # This aint a real `while True`, just a Python GOTO
            while True:
                # we are at the end?
                if len(chunk) == offset:
                    del chunks[0]
                    
                    # read a new chunk, because thats pretty simple
                    if chunks:
                        chunk = chunks[0]
                    else:
                        if self._eof:
                            raise EOFError(b'')
                        
                        chunk = yield from self._wait_for_data()
                    
                    end = chunk.find(b'\r\n')
                    # If we are at the end now, we get end as 0 and offset is 0, beause we just started a new chunk
                    if end == 0:
                        self._offset = 2
                        return headers
                    
                    middle = chunk.find(b':', 0, end)
                    if middle <= 0:
                        raise PayloadError(f'Invalid header line: {chunk[offset:end]!r}')
                    else:
                        name = chunk[:middle].lstrip()
                        value = chunk[middle+1:end].strip()
                        offset = end+2
                else:
                    # Store offset
                    self._offset = offset
                    #  try getting a full line
                    line = yield from self._readtill_CRLF()
                    # no headers at all? OK, I guess
                    if not line:
                        # because ._readtill_CRLF updates the chunk and the offset state for us, not needed to store it.
                        return headers
                    
                    middle = line.find(b':')
                    if middle <= 0:
                        #Nothing to do, no more case
                        raise PayloadError(f'Invalid header line: {line!r}')
                    
                    name = line[:middle]
                    value = line[middle+1:]
                
                # Jump on this part at the if not done, we will need this for checking continous lines.
                if chunks:
                    chunk = chunks[0]
                    offset = self._offset
                else:
                    if self._eof:
                        raise EOFError(b'')
                    
                    chunk = yield from self._wait_for_data()
                    offset = 0
                
                break
        
        name = name.decode('utf-8', 'surrogateescape')
        
        while True:
            if chunk[offset] in (b'\t'[0], b' '[0]):
                # continous
                value = [value]
                while True:
                    end = chunk.find(b'\r\n', offset)
                    # most likely case if we find \r\n
                    if end > offset:
                        value.append(chunk[offset:end].strip())
                        # andd \r\n shift
                        offset = end+2
                        
                        # if we are at the en of the chunk, we need again a new one for continous check
                        if offset == len(chunk):
                            del chunks[0]
                            if chunks:
                                chunk = chunks[0]
                            else:
                                if self._eof:
                                    raise EOFError(b'')
                                    
                                chunk = yield from self._wait_for_data()
                            
                            offset = 0
                        
                        # If next line is continous as well, continue loop
                        if chunk[offset] in (b'\t'[0], b' '[0]):
                            continue
                        
                        # Not continous, join lines and break
                        value = b' '.join(value)
                        break
                    
                    # We cannot be at the end now, because we just checked continous above >.> at least 1 char
                    
                    # We did not find \r\n
                    # Store offset and get a full line
                    self._offset = offset
                    line = yield from self._readtill_CRLF()
                    
                    # We cannot get empty line, because we just checked continous above <.< at least 1 char
                    
                    # Tho it can be an empty line. At that case we dont want to add it to the values, because
                    # we join them with b' '.
                    line = line.strip()
                    if line:
                        value.append(line)
                    
                    # Update chunk data after _readtill_CRLF, becase we want to check continous.
                    if chunks:
                        chunk = chunks[0]
                        offset = self._offset
                    else:
                        if self._eof:
                            raise EOFError(b'')
                        
                        chunk = yield from self._wait_for_data()
                        offset = 0
                    
                    # If continous, continue
                    if chunk[offset] in (b'\t'[0], b' '[0]):
                        continue
                    
                    # Not continous, leave loop
                    value = b' '.join(value)
                    break
            
            # Store, nice!
            headers[name] = value.decode('utf-8', 'surrogateescape')
            
            # Find end again
            end = chunk.find(b'\r\n', offset)
            # If we found and we arent at the end yet.
            if end > offset:
                middle = chunk.find(b':', offset, end)
                # New header line always must have b':', leave if not found, or if it is at the start.
                if middle <= offset:
                    raise PayloadError(f'Invalid header line: {chunk[offset:end]!r}')
                
                name = chunk[offset:middle].lstrip().decode('utf-8', 'surrogateescape')
                value = chunk[middle+1:end].strip()
                
                # Add 2 to the offset, to apply \r\n
                offset = end+2
                # if we are at the end of the cgunk, remove it and reset the offset
                if offset == len(chunk):
                    del chunks[0]
                    
                    if chunks:
                        chunk = chunks[0]
                    else:
                        if self._eof:
                            raise EOFError(b'')
                        
                        chunk = yield from self._wait_for_data()
                    
                    offset = 0
                continue
            
            # Next case, if we are at the end.
            if end == offset:
                # Update offset to include \r\n
                offset +=2
                # If we are at the of the chunk, remove it
                if offset == len(chunk):
                    del chunks[0]
                    offset = 0
                # Store new offset and return headers
                self._offset = offset
                return headers
            
            # Last case, no \r\n found.
            # If we are at the end of a chunk, ofc none was found.
            if len(chunk) == offset:
                # Go on the next chunk and try again.
                del chunks[0]
                if chunks:
                    chunk = chunks[0]
                else:
                    if self._eof:
                        raise EOFError(b'')
                    
                    chunk = yield from self._wait_for_data()
                
                offset = 0
                
                # No need to apply offset, because it is a completely new chunk.
                end = chunk.find(b'\r\n')
                # Best case scenario, if we found \r\n.
                if end > offset:
                    middle = chunk.find(b':', 0, end)
                    # middle must be found and cannot be first character either.
                    if middle <= 0:
                        raise PayloadError(f'Invalid header line: {chunk[offset:end]!r}')
                    
                    name = chunk[:middle].lstrip().decode('utf-8', 'surrogateescape')
                    value = chunk[middle+1:end].strip()
                    
                    #Apply offset and update chunk data if needed.
                    offset = end+2
                    if offset == len(chunk):
                        del chunks[0]
                        if chunks:
                            chunk = chunks[0]
                        else:
                            if self._eof:
                                raise EOFError(b'')
                        
                            chunk = yield from self._wait_for_data()
                        
                        offset = 0
                    
                    continue
                
                # Second case, when we are at the end.
                elif end == offset:
                    # Increase offset by 2 to include \r\n
                    offset +=2
                    # If we are at the end remove the chunk and store offset, return
                    if offset == len(chunk):
                        del chunks[0]
                        offset = 0
                    
                    self._offset = offset
                    return headers
                
                # Last case, not at end an no line break at the current chunk
                else:
                    # Save offset and get a new line
                    self._offset = offset
                    line = yield from self._readtill_CRLF()
                    if not line:
                        # If the line is empty, we can leave.
                        # Offset and chunk state is updated by the _readtill_CRLF method already.
                        return headers
                    
                    # Find middle
                    middle = line.find(b':')
                    # if middle is not found or the first character is the middle, we have a bad line
                    if middle <= 0:
                        raise PayloadError(f'Invalid header line: {line!r}')
                    
                    name = line[:middle].lstrip().decode('utf-8', 'surrogateescape')
                    value = line[middle+1:].strip()
                    
                    # Update the current chunk and offset state
                    if chunks:
                        chunk = chunks[0]
                        offset = self._offset
                    else:
                        if self._eof:
                            raise EOFError(b'')
                        
                        chunk = yield from self._wait_for_data()
                        offset = 0
                    
                    continue
            # We are not at the end case
            else:
                # Store offset and read a line
                self._offset = offset
                line = yield from self._readtill_CRLF()
                # If the line is empty we leave.
                # Offset and chunk state is updated by the _readtill_CRLF method already.
                if not line:
                    return headers
                
                # Find the middle
                middle = line.find(b':')
                # If the middle was not found, or it is the first character, bad line
                if middle <= 0:
                    raise PayloadError(f'Invalid header line: {line!r}')
                
                name = line[:middle].lstrip().decode('utf-8', 'surrogateescape')
                value = line[middle+1:].strip()
                
                # Update the current chunk and offset state
                if chunks:
                    chunk = chunks[0]
                    offset = self._offset
                else:
                    if self._eof:
                        raise EOFError(b'')
                    
                    chunk = yield from self._wait_for_data()
                    offset = 0
                
                continue
            continue
    
    def _read_websocket_frame(self, is_client, max_size):
        
        head1, head2 = yield from self._read_exactly(2)
        
        if ((head2&0b10000000)>>7) == is_client:
            raise WebSocketProtocolError('Incorrect masking')
        
        length = head2&0b01111111
        
        if length == 126:
            data = yield from self._read_exactly(2)
            length, = UNPACK_LEN2(data)
        elif length == 127:
            data = yield from self._read_exactly(8)
            length, = UNPACK_LEN3(data)
        
        if (max_size is not None) and length>max_size:
            raise PayloadError(f'Payload length exceeds size limit ({length} > {max_size} bytes)')
        
        #Read the data.
        if is_client:
            data = yield from self._read_exactly(length)
        else:
            mask = yield from self._read_exactly(4)
            data = yield from self._read_exactly(length)
            data = apply_mask(mask,data)
        
        frame = object.__new__(Frame)
        frame.data = data
        frame.head1 = head1
        
        return frame
    
    def get_payload_reader_task(self, message):
        length = message.headers.get(CONTENT_LENGTH)
        if (length is not None):
            if length.isdigit():
                length = int(length)
            else:
                raise PayloadError(f'{CONTENT_LENGTH} must be a non negative int, got: {length!r}')
        
        if (not message.upgraded):
            if message.chunked:
                decompresser = self._decompresser_for(message.encoding)
                if decompresser is None:
                    return self._read_chunked()
                else:
                    return self._read_chunked_encoded(decompresser)
            
            if (length is not None) and (length > 0):
                decompresser = self._decompresser_for(message.encoding)
                if decompresser is None:
                    return self._read_exactly(length)
                else:
                    return self._read_exactly_encoded(length, decompresser)
        
        if (type(message) is RawRequestMessage) and (message.meth == METH_CONNECT):
            message.upgraded = True
            return self._read_until_eof()
        
        if (type(message) is RawResponseMessage) and message.status >= 199 and (length is None):
            if message.chunked:
                decompresser = self._decompresser_for(message.encoding)
                if decompresser is None:
                    return self._read_chunked()
                else:
                    return self._read_chunked_encoded(decompresser)
            
            return self._read_until_eof()
        
        return None
    
    @staticmethod
    def _decompresser_for(encoding):
        if (encoding is None):
            decompressor = None
        elif encoding == 'gzip':
            decompressor=ZLIB_DECOMPRESSOR(wbits=16+zlib.MAX_WBITS)
        elif encoding == 'deflate':
            decompressor=ZLIB_DECOMPRESSOR(wbits=-zlib.MAX_WBITS)
        elif encoding == 'br':
            if BROTLI_DECOMPRESSOR is None:
                raise ContentEncodingError('Can not decode content-encoding: brotli (br). Please install `brotlipy`.')
            decompressor = BROTLI_DECOMPRESSOR()
        elif encoding == 'identity':
            # I asume this is no encoding
            decompressor = None
        else:
            raise ContentEncodingError(f'Can not decode content-encoding: {encoding!r}.')
        
        return decompressor
    
    def _read_chunked(self):
        collected = []
        while True:
            chunk_length = yield from self._readtill_CRLF()
            # strip chunk extension
            index = chunk_length.find(b';')
            if index != -1:
                chunk_length = chunk_length[:index]
            
            try:
                chunk_length = int(chunk_length,16)
            except ValueError:
                raise PayloadError(f'Not hexadecimal chunk size: {chunk_length!r}') from None
            
            if chunk_length == 0:
                end = yield from self._read_exactly(2)
                if end != b'\r\n':
                    raise PayloadError(f'Recevied chunk does not end with b\'\\r\\n\', instead with: {end}')
                break
            
            chunk = yield from self._read_exactly(chunk_length)
            end = yield from self._read_exactly(2)
            if end != b'\r\n':
                raise PayloadError(f'Recevied chunk does not end with b\'\\r\\n\', instead with: {end}')
            
            collected.append(chunk)
        
        return b''.join(collected)
    
    def _read_until_eof(self):
        chunks = self._chunks
        
        if not self._eof:
            while True:
                try:
                    yield from self._wait_for_data()
                except (CancelledError, GeneratorExit):
                    if self._eof:
                        break
                    
                    raise
        
        if not chunks:
            return b''
        
        offset = self._offset
        if offset:
            chunks[0] = memoryview(chunks[0])[offset:]
        
        result = b''.join(chunks)
        chunks.clear()
        return result
    
    def _read_exactly_encoded(self, length, decompressobj):
        chunk = yield from self._read_exactly(length)
        return decompressobj.decompress(chunk)
    
    def _read_chunked_encoded(self, decompressobj):
        collected = []
        while True:
            chunk_length = yield from self._readtill_CRLF()
            # strip chunk extension
            index = chunk_length.find(b';')
            if index != -1:
                chunk_length = chunk_length[:index]
            
            try:
                chunk_length = int(chunk_length,16)
            except ValueError:
                raise PayloadError(f'Not hexadecimal chunk size: {chunk_length!r}') from None
            
            if chunk_length == 0:
                end = yield from self._read_exactly(2)
                if end != b'\r\n':
                    raise PayloadError(f'Recevied chunk does not end with b\'\\r\\n\', instead with: {end}')
                break
            
            chunk = yield from self._read_exactly(chunk_length)
            end = yield from self._read_exactly(2)
            if end != b'\r\n':
                raise PayloadError(f'Recevied chunk does not end with b\'\\r\\n\', instead with: {end}')
            
            try:
                chunk = decompressobj.decompress(chunk)
            except COMPRESSION_ERRORS:
                raise PayloadError('Cannot decompress chunk') from None
            
            collected.append(chunk)
        
        return b''.join(collected)
    
    def _read_once(self):
        """
        Reader task for reading exactly one chunk out.
        
        Returns
        -------
        chunk : `bytes`
            The read chunk. Returns empty `bytes` on eof.
        
        Raises
        ------
        CancelledError
            If the reader task is cancelled not by receiving eof.
        """
        chunks = self._chunks
        if not chunks:
            try:
                yield from self._wait_for_data()
            except (CancelledError, GeneratorExit):
                if self._eof:
                    return b''
                
                raise
        
        chunk = chunks.popleft()
        offset = self._offset
        if offset:
            self._offset = 0
            chunk = chunk[offset:]
        
        return chunk
    
    def __call__(self):
        return self


class DatagramAddressedReadProtocol(object):
    """
    Datagram reader protocool for reading from payloads form multiple addresses.
    
    ``DatagramAddressedReadProtocol`` can also be used as a factory of itself, because when called, returns itself.
    
    Attributes
    ----------
    by_address : `dict` of (`tuple` (`str`, `int`), ``ReadProtocolBase``) items
        Dictionary to store the alive readers by address.
    loop : ``EventThread``
        The loop to what the protocol is bound to.
    transport : `Any`
        Asynchronous transport implementation, what calls the protocol's ``.datagram_received`` when data is
        received.
    waiters : `None`, `list` of `Future`
        Waiters for any payload receive if applicable.
    """
    __slots__ = ('by_address', 'loop', 'transport', 'waiters',)
    def __init__(self, loop):
        """
        Creates a new ``DatagramAddressedReadProtocol`` instance bound to the given loop.
        
        Parameters
        ----------
        loop : ``EventThread``
            The loop to what the protocol gonna be bound to.
        """
        self.loop = loop
        self.by_address = {}
        self.transport = None
        self.waiters = None
    
    def __call__(self):
        """
        Returns the protocol itself allowing ``DatagramAddressedReadProtocol`` to be it's own factory.
        
        Returns
        -------
        self : ``DatagramAddressedReadProtocol``
        """
        return self
    
    def connection_made(self, transport):
        """
        Called when a connection is made.
        
        Parameters
        ----------
        transport : `Any`
            Asynchronous transport implementation, what calls the protocol's ``.datagram_received`` when data is
            received.
        """
        self.transport = transport
        for reader_protocol in self.by_address.values():
            reader_protocol.connection_made(transport)
    
    def connection_lost(self, exception):
        """
        Called when the connection is lost or closed.
        
        Parameters
        ----------
        exception : `None` or `BaseException` instance
            Defines whether the connection is closed, or except was received.
            
            If the connection was closed, then `err` is given as `None`. This can happen at the case, when eof is
            received as well.
        """
        for reader_protocol in self.by_address.values():
            if exception is None:
                reader_protocol.eof_received()
            else:
                reader_protocol.set_exception(exception)
    
    def pause_writing(self):
        """
        Called when the transport's buffer goes over the high-water mark.
        
        ``.pause_writing`` is called when the buffer goes over the high-water mark, and eventually
        ``.resume_writing`` is called when the buffer size reaches the low-water mark.
        """
    
    def resume_writing(self):
        """
        Called when the transport's buffer drains below the low-water mark.
        
        See ``.pause_writing`` for details.
        """
    
    def datagram_received(self, data, address):
        """
        Called when some datagram is received.
        
        Parameters
        ----------
        data : `bytes`
            The received data.
        address : `tuple` (`str`, `int`)
            The address from where the data was received.
        """
        by_address = self.by_address
        try:
            protocol = by_address[address]
        except KeyError:
            protocol = ReadProtocolBase(self.loop)
            protocol.connection_made(self.transport)
            by_address[address] = protocol
        
        protocol.data_received(data)
        
        waiters = self.waiters
        if (waiters is not None):
            self.waiters = None
            result = (address, protocol)
            for waiter in waiters:
                waiter.set_result_if_pending(result)
    
    def error_received(self, exception):
        """
        Called when a send or receive operation raises an `OSError`, but not `BlockingIOError`, nor `InterruptedError`.
        
        Parameteres
        -----------
        exception : `OSError`
            The catched exception.
        """
    
    async def wait_for_receive(self, address=None, timeout=None):
        """
        Can be used to wait for payload to receive. Note, that this method should be used onyl initially, because the
        reader protocols implement the reading.
        
        
        This method is a corotuine.
        
        Parameters
        ----------
        address : `None`, `tuple` (`str`, `int`), Optional
            The address of which payload is waiter for.
        timeout : `None` or `
        
        Returns
        -------
        result : `None` or ``ReadProtocolBase`` or (`tuple` (`str`, `int`), ``ReadProtocolBase``)
            - If `timeout` is given and timeot occures, then returns `None`.
            - if `address` is given and data is received from ir, then returns the respective ``ReadProtocolBase``.
            - If `address` is not given, then returns a `tuple` of the respective `address` and protocol.
        """
        if timeout is None:
            if address is None:
                waiters = self.waiters
                if waiters is None:
                    self.waiters = waiters = []
                
                waiter = Future(self.loop)
                waiters.append(waiter)
                
                return await waiter
            else:
                while True:
                    waiters = self.waiters
                    if waiters is None:
                        self.waiters = waiters = []
                    
                    waiter = Future(self.loop)
                    waiters.append(waiter)
                    
                    address, protocol = await waiter
                    if address == address:
                        return protocol
                    
                    continue
        
        else:
            waiter = Task(self.wait_for_receive(address))
            future_or_timeout(waiter, timeout)
            
            try:
                result = await waiter
            except TimeoutError:
                result = None
            
            return result
    
    def close(self):
        """
        Closes the protocol by closing it's transport if applicable.
        """
        transport = self.transport
        if (transport is not None):
            transport.close()


class DatagramMergerReadProtocol(ReadProtocolBase):
    """
    Datagram protocol, which merges all the data received from any address.
    
    Attributes
    ----------
    _chunks : `dequeue` of `bytes`
        The received data chunks.
    _eof : `bool`
        Whether the protocol received end of file.
    _offset : `int`
        The index till the oldest not yet fully exhausted data chunk is used up.
    _paused : `bool`
        Whether the transport is paused reading.
    exception : `None` or `BaseException` instance
        The exception with what the respective connection is lost, if any.
    loop : ``EventThread``
        The eventloop to what the protocol is bound to.
    payload_reader : `generator`
        Payloader reader generator, what is continued when data, eof or any exception is received.
    payload_waiter : ``Future``
        Payload waiter future, what can be awaited to receive the ``.payload_reader``'s result if done.
        
        If cancelled or marked by done or any other methods, the payload reader will not be cancelled.
    transport : `Any`
        Asynchonous transport implementation.
    """
    __slots__ = ()
    
    def pause_writing(self):
        """
        Called when the transport's buffer goes over the high-water mark.
        
        ``.pause_writing`` is called when the buffer goes over the high-water mark, and eventually
        ``.resume_writing`` is called when the buffer size reaches the low-water mark.
        """
    
    def resume_writing(self):
        """
        Called when the transport's buffer drains below the low-water mark.
        
        See ``.pause_writing`` for details.
        """
    
    def datagram_received(self, data, address):
        """
        Called when some datagram is received.
        
        Parameters
        ----------
        data : `bytes`
            The received data.
        address : `tuple` (`str`, `int`)
            The address from where the data was received.
        """
        self.data_received(data)


class ProtocolBase(ReadProtocolBase):
    __slots__ = ('_drain_waiter', )
    
    def __init__(self, loop):
        self.loop = loop
        self.transport = None
        self.exception = None
        self._chunks = deque()
        self._offset = 0
        self._eof = False
        self.payload_reader = None
        self.payload_waiter = None
        self._paused = False
        
        self._drain_waiter = None
    
    def _copy_attrs_to(self, other):
        other.transport = self.transport
        other.exception = self.exception
        other._chunks = self._chunks
        other._offset = self._offset
        other._eof = self._eof
        other.payload_reader = self.payload_reader
        other.payload_waiter = self.payload_waiter
        other._paused = self._paused
        other._drain_waiter = self._drain_waiter
    
    # compability method
    def pause_writing(self):
        self._paused = True
    
    # compability method
    def resume_writing(self):
        self._paused = False
        
        drain_waiter = self._drain_waiter
        if drain_waiter is None:
            return
        
        self._drain_waiter = None
        drain_waiter.set_result_if_pending(None)
    
    # compability method
    async def _drain_helper(self):
        if not self._paused:
            return
        drain_waiter = Future(self.loop)
        self._drain_waiter = drain_waiter
        await drain_waiter
    
    # compability method
    def connection_lost(self, exception):
        if exception is None:
            self.eof_received()
        else:
            self.set_exception(exception)
        
        #wake up the writer if currently paused.
        if not self._paused:
            return
        
        drain_waiter = self._drain_waiter
        if drain_waiter is None:
            return
        
        self._drain_waiter = None
        if drain_waiter.done():
            return
        
        if exception is None:
            drain_waiter.set_result(None)
        else:
            drain_waiter.set_exception(exception)
    
    # Basic writing
    def write(self, data):
        transport = self.transport
        if transport is None:
            raise RuntimeError('Protocol has no attached transport.')
        
        transport.write(data)
    
    def writelines(self, data):
        transport = self.transport
        if transport is None:
            raise RuntimeError('Protocol has no attached transport.')
        
        transport.writelines(data)
    
    # Specific writings
    def write_http_request(self, meth, path, headers, version = HttpVersion11):
        transport = self.transport
        if transport is None:
            raise RuntimeError('Protocol has no attached transport.')
        
        result = [f'{meth} {path} HTTP/{version.major}.{version.major}\r\n']
        extend = result.extend
        for k, v in headers.items():
            extend((k, ': ', v, '\r\n'))
        
        result.append('\r\n')
        
        transport.write(''.join(result).encode())
    
    def write_http_response(self, status, headers, version = HttpVersion11, body = None):
        transport = self.transport
        if transport is None:
            raise RuntimeError('Protocol has no attached transport.')
        
        result = [f'HTTP/{version.major}.{version.minor} {status.value} {status.phrase}\r\n']
        extend = result.extend
        for k, v in headers.items():
            extend((k, ': ', v, '\r\n'))
        
        result.append('\r\n')
        
        transport.write(''.join(result).encode())
        if (body is not None) and body:
            transport.write(body)
    
    def write_websocket_frame(self, frame, is_client):
        transport = self.transport
        if transport is None:
            raise RuntimeError('Protocol has no attached transport.')
        
        # Prepare the header.
        head1 = frame.head1
        head2 = is_client<<7
        
        length = len(frame.data)
        if length < 126:
            header = PACK_LEN1(head1, head2|length)
        elif length < 65536:
            header = PACK_LEN2(head1, head2|126,length)
        else:
            header = PACK_LEN3(head1, head2|127,length)
        transport.write(header)
        
        #prepare the data.
        if is_client:
            mask = getrandbits(32).to_bytes(4, 'big')
            transport.write(mask)
            data = apply_mask(mask, frame.data,)
        else:
            data = frame.data
        
        transport.write(data)
    
    def write_eof(self):
        transport = self.transport
        if (transport is not None):
            transport.write_eof()
    
    def can_write_eof(self):
        transport = self.transport
        if (transport is None):
            return False
        
        return transport.can_write_eof()
    
    async def drain(self):
        #use after writing
        exception = self.exception
        if (exception is not None):
            raise exception
        
        transport = self.transport
        if (transport is not None):
            if transport.is_closing():
                #skip 1 loop, so connection_lost() will be called
                future=Future(self.loop)
                future.set_result(None)
                await future
        
        await self._drain_helper()

del re, Struct
