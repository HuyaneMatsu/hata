# -*- coding: utf-8 -*-
import sys
import zlib
from collections import deque
from .futures import Future,CancelledError
from .py_exceptions import PayloadError

DEFAULT_LIMIT=1<<16

class EofStream(Exception):
    #eof stream indication.
    pass

class AS_IT(object):
    __slots__=('func', 'n', 'parent',)
    def __init__(self,parent,func,n=None):
        self.parent = parent
        self.func   = func
        self.n      = n

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            result = await self.func(self.parent,self.n)
            if result:
                return result
        except EofStream:
            pass
        
        raise StopAsyncIteration

class AS_IT_CT(object):
    __slots__=('parent',)
    def __init__(self,parent):
        self.parent=parent

    def __aiter__(self):
        return self

    async def __anext__(self):
        rv = await self.parent.readchunk()
        if rv[0]:
            return rv
        raise StopAsyncIteration

class StreamReader(object):

    def __aiter__(self):
        return AS_IT(self,type(self).readline)

    def iter_chunked(self, n):
        return AS_IT(self,type(self).read,n)

    def iter_any(self):
        return AS_IT(self,type(self).readany)

    def iter_chunks(self):
         return AS_IT_CT(self)

    __slots__=('buffer', 'buffer_offset', 'chunk_splits', 'cursor', 'eof',
        'eof_callbacks', 'eof_waiter', 'exception', 'high_water', 'loop',
        'low_water', 'protocol', 'size', 'timer', 'total_bytes', 'waiter',)

    def __init__(self,protocol,loop,limit=DEFAULT_LIMIT,timer=None):
        self.protocol      = protocol
        self.low_water     = limit
        self.high_water    = limit<<1

        self.loop          = loop
        self.size          = 0
        self.cursor        = 0
        self.chunk_splits  = None
        self.buffer        = deque()
        self.buffer_offset = 0
        self.eof           = False
        self.waiter        = None
        self.eof_waiter    = None
        self.exception     = None
        self.timer         = timer
        self.eof_callbacks = []
        self.total_bytes   = 0
        
    def __repr__(self):
        info=['<',__class__.__name__]
        
        info.append(' size=')
        info.append(self.size.__str__())
        info.append(' bytes')

        eof=self.eof
        if eof:
            info.append(' eof')
        
        info.append(' waiter=')
        info.append(self.waiter.__repr__())
        
        info.append(' exception=')
        info.append(self.exception.__repr__())
        
        info.append('>')
        
        return ''.join(info)

    def set_exception(self,exception):
        self.exception=exception
        self.eof_callbacks.clear()

        waiter=self.waiter
        if waiter is not None:
            self.waiter=None
            if not waiter.done():
                waiter.set_exception(exception)

        waiter=self.eof_waiter
        if waiter is not None:
            if not waiter.done():
                waiter.set_exception(exception)
            self.eof_waiter=None

    def on_eof(self,callback):
        if self.eof:
            try:
                callback()
            except Exception as err:
                self.loop.render_exc_async(err,[
                    'Exception occured at ',
                    self.__class__.__name__,
                    '.on_eof\n',
                          ])
        else:
            self.eof_callbacks.append(callback)

    def feed_eof(self):
        self.eof=True

        waiter=self.waiter
        if waiter is not None:
            self.waiter=None
            if not waiter.done():
                waiter.set_result(True)

        waiter=self.eof_waiter
        if waiter is not None:
            self.eof_waiter=None
            if not waiter.done():
                waiter.set_result(True)

        for callback in self.eof_callbacks:
            try:
                callback()
            except (AttributeError,NameError):
                raise #for testing
            except Exception:
                pass

        self.eof_callbacks.clear()

    def is_eof(self):
        #Return True if  'feed_eof' was called.
        return self.eof

    def at_eof(self):
        #Return True if the buffer is empty and 'feed_eof' was called.
        return self.eof and not self.buffer

    async def wait_eof(self):
        if self.eof:
            return

        self.eof_waiter=Future(self.loop)
        try:
            await self.eof_waiter
        finally:
            self.eof_waiter=None

    def unread_data(self,data):
        #rollback reading some data from stream, inserting it to buffer head.
        if not data:
            return

        if self.buffer_offset:
            self.buffer[0]=self.buffer[0][self.buffer_offset:]
            self.buffer_offset=0
        
        self.size       += len(data)
        self.cursor     -= len(data)
        self.buffer.appendleft(data)

    # TODO: size is ignored, remove the param later
    def feed_data(self,data,size=0):

        if not data:
            return

        self.size+=len(data)
        self.buffer.append(data)
        self.total_bytes+=len(data)

        waiter=self.waiter
        if waiter is not None:
            self.waiter=None
            if not waiter.done():
                waiter.set_result(True)

        if (self.size>self.high_water and not self.protocol.reading_paused):
            self.protocol.pause_reading()

    def begin_http_chunk_receiving(self):
        if self.chunk_splits is None:
            self.chunk_splits=[]

    def end_http_chunk_receiving(self):
        if self.chunk_splits is None:
            raise RuntimeError('Called end_chunk_receiving without calling begin_chunk_receiving first')
        if not self.chunk_splits or self.chunk_splits[-1]!=self.total_bytes:
            self.chunk_splits.append(self.total_bytes)

    async def _wait(self,func_name):
        # StreamReader uses a future to link the protocol feed_data() method
        # to a read coroutine. Running two read coroutines at the same time
        # would have an unexpected behaviour. It would not possible to know
        # which coroutine would get the next data.
        if self.waiter is not None:
            raise RuntimeError(f'{func_name} called while another coroutine is already waiting for incoming data')

        waiter=self.waiter=Future(self.loop)
        try:
            if self.timer is None:
                await waiter
            else:
                with self.timer:
                    await waiter
        finally:
            self.waiter=None

    async def readline(self,n=None): #n is gonna get ignored, but mut for the iterator class
        if self.exception is not None:
            raise self.exception

        line        = []
        line_size   = 0
        not_enough  = True

        while not_enough:
            while self.buffer and not_enough:
                offset = self.buffer_offset
                ichar = self.buffer[0].find(b'\n',offset)+1
                # Read from current offset to found b'\n' or to the end.
                if ichar:
                    amount=ichar-offset
                else:
                    amount=-1
                data=self._read_nowait_chunk(amount)
                
                line.append(data)
                line_size+=len(data)
                if ichar:
                    not_enough = False

                if line_size>self.high_water:
                    raise ValueError('Line is too long')

            if self.eof:
                break

            if not_enough:
                await self._wait('readline')

        return b''.join(line)

    async def read(self, n=-1):
        if self.exception is not None:
            raise self.exception

        if not n:
            return b''

        if n < 0:
            # This used to just loop creating a new waiter hoping to
            # collect everything in self.buffer, but that would
            # deadlock if the subprocess sends more than self.limit
            # bytes.  So just call self.readany() until EOF.
            blocks = []
            while True:
                block = await self.readany()
                if not block:
                    break
                blocks.append(block)
            return b''.join(blocks)

        if not self.buffer and not self.eof:
            await self._wait('read')

        return self._read_nowait(n)

    async def readany(self):
        if self.exception is not None:
            raise self.exception

        if not self.buffer and not self.eof:
            await self._wait('readany')

        return self._read_nowait(-1)

    async def readchunk(self):
        #Returns a tuple of (data, end_of_http_chunk). When chunked transfer
        #encoding is used, end_of_http_chunk is a boolean indicating if the end
        #of the data corresponds to the end of a HTTP chunk , otherwise it is
        #always False.
        if self.exception is not None:
            raise self.exception

        if not self.buffer and not self.eof:
            if (self.chunk_splits and self.cursor==self.chunk_splits[0]):
                # end of http chunk without available data
                self.chunk_splits=self.chunk_splits[1:]
                return b'',True
            await self._wait('readchunk')

        if not self.buffer:
            # end of file
            return b'',False
        elif self.chunk_splits is not None:
            while self.chunk_splits:
                pos=self.chunk_splits[0]
                self.chunk_splits=self.chunk_splits[1:]
                if pos>self.cursor:
                    return (self._read_nowait(pos-self.cursor),True)
            return self._read_nowait(-1),False
        else:
            return self._read_nowait_chunk(-1),False

    async def readexactly(self,n):
        if self.exception is not None:
            raise self.exception

        blocks=[]
        while n>0:
            block = await self.read(n)
            if not block:
                partial = b''.join(blocks)
                raise PayloadError(partial,len(partial)+n)
            blocks.append(block)
            n-=len(block)

        return b''.join(blocks)

    def read_nowait(self,n=-1):
        # default was changed to be consistent with .read(-1)
        #
        # I believe the most users don't know about the method and
        # they are not affected.
        if self.exception is not None:
            raise self.exception

        if self.waiter is not None and not self.waiter.done():
            raise RuntimeError('Called while some coroutine is waiting for incoming data.')

        return self._read_nowait(n)

    def _read_nowait_chunk(self,n):
        first_buffer=self.buffer[0]
        offset=self.buffer_offset
        if n!=-1 and len(first_buffer)-offset>n:
            data=first_buffer[offset:offset+n]
            self.buffer_offset+=n

        elif offset:
            self.buffer.popleft()
            data=first_buffer[offset:]
            self.buffer_offset=0

        else:
            data=self.buffer.popleft()

        self.size-=len(data)
        self.cursor+=len(data)

        if self.size<self.low_water and self.protocol.reading_paused:
            self.protocol.resume_reading()
        return data

    def _read_nowait(self,n):
        chunks=[]

        while self.buffer:
            chunk = self._read_nowait_chunk(n)
            chunks.append(chunk)
            if n!=-1:
                n-=len(chunk)
                if n==0:
                    break
        if chunks:
            return b''.join(chunks)
        return b''


class StreamWriter(object):
    __slots__=('size', 'chunked', 'compress', 'drain_waiter', 'eof',
        'length', 'loop', 'on_chunk_sent', 'output_size', 'protocol',
        'transport',)
    def __init__(self,protocol,loop,on_chunk_sent=None):
        self.protocol       = protocol
        self.transport      = protocol.transport
        
        self.loop           = loop
        self.length         = None
        self.chunked        = False
        self.size           = 0
        self.output_size    = 0

        self.eof            = False
        self.compress       = None
        self.drain_waiter   = None

        self.on_chunk_sent  = on_chunk_sent

    def enable_chunking(self):
        self.chunked=True

    def enable_compression(self,encoding='deflate'):
        if encoding=='gzip':
            zlib_mode=16+zlib.MAX_WBITS
        else:
            zlib_mode=-zlib.MAX_WBITS
        self.compress=zlib.compressobj(wbits=zlib_mode)

    def _write(self,chunk):
        size=len(chunk)
        self.size+=size
        self.output_size+=size
            
        if self.transport is None or self.transport.is_closing():
            raise ConnectionResetError('Cannot write to closing transport')
        self.transport.write(chunk)

    async def write(self,chunk, *,drain=True,LIMIT=0x10000):
        #Writes chunk of data to a stream.
        #
        #write_eof() indicates end of stream.
        #writer can't be used after write_eof() method being called.
        #write() return drain future.

        if self.on_chunk_sent is not None:
            await self.on_chunk_sent(chunk)

        if self.compress is not None:
            chunk=self.compress.compress(chunk)
            if not chunk:
                return

        if self.length is not None:
            chunk_len=len(chunk)
            if self.length>=chunk_len:
                self.length=self.length-chunk_len
            else:
                chunk=chunk[:self.length]
                self.length=0
                if not chunk:
                    return

        if chunk:
            if self.chunked:
                chunk=b''.join([(f'{len(chunk):x}\r\n').encode('ascii'),chunk,b'\r\n'])
            self._write(chunk)

            if self.size>LIMIT and drain:
                self.size=0
                await self.drain()

    async def write_headers(self,status_line,headers):
        #Write request/response status and headers.
        # status + headers
        breaker='\r\n'
        self._write(f'{status_line}\r\n{"".join([f"{k}: {v}{breaker}" for k,v in headers.items()])}\r\n'.encode('ascii'))

        
    async def write_eof(self,chunk=b''):
        if self.eof:
            return

        if chunk and self.on_chunk_sent:
            await self.on_chunk_sent(chunk)

        if self.compress is None:
            if self.chunked:
                if chunk:
                    chunk=b''.join([(f'{len(chunk):x}\r\n').encode('ascii'),chunk,b'\r\n0\r\n\r\n'])
                else:
                    chunk=b'0\r\n\r\n'
        else:
            if chunk:
                chunk=self.compress.compress(chunk)

            chunk=chunk+self.compress.flush()
            if chunk and self.chunked:
                chunk=b''.join([(f'{len(chunk):x}\r\n').encode('ascii'),chunk,b'\r\n0\r\n\r\n'])


        if chunk:
            self._write(chunk)

        await self.drain()

        self.eof=True
        self.transport=None

    async def drain(self):
        #Flush the write buffer.
        #
        #The intended use is to write
        #
        #await w.write(data)
        #await w.drain()
        if self.protocol.transport is not None:
            await self.protocol._drain_helper()


class EmptyStreamReader(object):
    __slots__=()
    #these wont work, but need to put here something too
    def __aiter__(self):
        return AS_IT(self,type(self).readline)

    def iter_chunked(self, n):
        return AS_IT(self,type(self).read,n)

    def iter_any(self):
        return AS_IT(self,type(self).readany)

    def iter_chunks(self):
         return AS_IT_CT(self)

    def get_exception(self):
        return None
    
    def set_exception(self,exception):
        pass

    exception=property(get_exception,set_exception)
    del get_exception
    #the property's set_exception and the Reader's set_eceptions do the same, so they ll be same
    
    def on_eof(self,callback):
        try:
            callback()
        except (AttributeError,NameError):
            raise #for testing
        except Exception:
            pass

    def feed_eof(self):
        pass

    def is_eof(self):
        return True

    def at_eof(self):
        return True

    async def wait_eof(self):
        return

    def feed_data(self,data,size=0):
        pass

    async def readline(self):
        return b''

    async def read(self,n=-1):
        return b''

    async def readany(self):
        return b''

    async def readchunk(self):
        return b'',False

    async def readexactly(self,n):
        raise PayloadError(b'',n)

    def read_nowait(self):
        return b''

EMPTY_PAYLOAD = EmptyStreamReader()


class DataQueue(object):
    #DataQueue is a general-purpose blocking queue with one reader.
    __slots__=('buffer', 'eof', 'exception', 'loop', 'size', 'waiter',)
    def __init__(self,loop):
        self.loop       = loop
        self.eof        = False
        self.waiter     = None
        self.exception  = None
        self.size       = 0
        self.buffer     = deque()

    def __len__(self):
        return len(self.buffer)

    def is_eof(self):
        return self.eof

    def at_eof(self):
        return self.eof and not self.buffer

    def set_exception(self,exception):
        self.eof        = True
        self.exception  = exception
        waiter          = self.waiter
        
        if waiter is None:
            return

        self.waiter=None
        if not waiter.done():
            waiter.set_exception(exception)

    def feed_data(self,data,size=0):
        self.size=size
        self.buffer.append((data,size))

        waiter=self.waiter
        if waiter is None:
            return

        self.waiter=None
        if not waiter.done():
            waiter.set_result(True)

    def feed_eof(self):
        self.eof=True

        waiter=self.waiter
        if waiter is None:
            return
        
        self.waiter=None
        if not waiter.done():
            waiter.set_result(False)

    async def read(self):
        if not self.buffer and not self.eof:
            self.waiter=Future(self.loop)
            try:
                await self.waiter
            except (CancelledError,TimeoutError) as err:
                self.waiter=None
                raise

        if self.buffer:
            data,size=self.buffer.popleft()
            self.size-=size
            return data
        else:
            if self.exception is None:
                raise EofStream
            raise self.exception

    def __aiter__(self):
        return AS_IT(self,type(self).read)
