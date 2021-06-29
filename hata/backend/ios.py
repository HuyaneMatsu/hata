# -*- coding: utf-8 -*-
__all__ = ('AsyncIO', 'ReuAsyncIO', 'ReuBytesIO', )

import os
from io import BytesIO
from threading import current_thread

from .executor import ExecutorThread
from .utils import alchemy_incendiary
from .event_loop import EventThread

OPERATION_WRITE = 0
OPERATION_READ = 1

IO_CLOSED_OR_DETACHED = 'I/O operation on closed or on a detached file.'

class ReuBytesIO(BytesIO):
    """
    Reusable bytes io, what seeks the cursor at `0`, when calling ``.close``. Use ``.real_close`` to close it for real,
    or use it with the `with` syntax.
    
    Should be used instead of `BytesIO` when sending it with http requests. Since the buffer is closed when a request
    is sent, at the case of received errors repeat could not be executed.
    
    Attributes
    ----------
    _last_op : `int`
        The last called operation of the buffer.
        
        If switching after reading to writing the buffer seeks to `0`.
        
        Can be set as `1` of the following:
        
        +-------------------+-------+
        | Respective name   | Value |
        +===================+=======+
        | OPERATION_WRITE   | 0     |
        +-------------------+-------+
        | OPERATION_READ    | 1     |
        +-------------------+-------+
    _size : `int`
        The position, till the buffer was written by the last reading session and can be read back.
    """
    __slots__ = ('_last_op', '_size')
    
    def __init__(self,):
        """
        Initializes the buffer.
        """
        self._size = 0
        self._last_op = OPERATION_WRITE
    
    def write(self, data):
        """
        Writes the given data to the buffer.
        
        If the buffer is in `read` mode, in seeks back to `0`
        
        Parameters
        ----------
        data : `bytes-like`
            The data to write.
        """
        if self._last_op != OPERATION_WRITE:
            BytesIO.seek(self, 0)
            self._size = 0
            self._last_op = OPERATION_WRITE
        
        amount = BytesIO.write(self, data)
        self._size += amount
        return amount
    
    def read(self, amount=None):
        """
        Reads the given amount of data from the buffer.
        
        Parameters
        ----------
        amount : `None` or `int`, Optional
            The amount of data to read from the buffer. If given as `None`, so by the default, then reads all the data
            out from it.
        
        Returns
        -------
        data : `bytes`
            The red data.
        """
        self._last_op = OPERATION_READ
        
        if amount is None:
            amount = self._size-self.tell()
        else:
            readable = self._size-self.tell()
            if amount > readable:
                amount = readable
        
        return BytesIO.read(self, amount)
    
    def close(self):
        """
        Seeks back to position `0`.
        """
        self.seek(0)
    
    def __len__(self):
        """
        Returns the length till the buffer was written in it's last write session.
        
        Returns
        -------
        length : `int`
        """
        return self._size
    
    def seek(self, offset, whence=os.SEEK_SET):
        """
        Changes the stream position by the given offset. Offset is interpreted relative to the position indicated
        by `whence`.
        
        Parameters
        ----------
        offset : `int`
            Position to move the cursor to.
        whence : `int`, Optional
            How the given `offset` should be interpreted. Default value for whence is `os.SEEK_SET`.
            
            Can be given as:
            
            +-------------------+-------+-----------------------------------------------------------+
            | Respective name   | Value | Description                                               |
            +===================+=======+===========================================================+
            | os.SEEK_SET       | 0     | Start of the stream. Offset should be zero or positive.   |
            +-------------------+-------+-----------------------------------------------------------+
            | os.SEEK_CUR       | 1     | Current stream position. Offset may be negative.          |
            +-------------------+-------+-----------------------------------------------------------+
            | os.SEEK_END       | 2     | End of the stream. Offset is usually negative.            |
            +-------------------+-------+-----------------------------------------------------------+
            
        Returns
        -------
        position : `int`
            The new absolute position.
        """
        if whence == os.SEEK_END:
            return self._size
        
        value = BytesIO.seek(self, offset, whence)
        if value > self._size:
            self._size = value
            
        return value
    
    def real_close(self):
        """
        Closes the buffer.
        """
        BytesIO.close(self)


def get_executor():
    """
    Gets executor from the current event thread if applicable. If not, starts a new one.
    
    Returns
    -------
    executor : ``ExecutorThread`` or ``ClaimedExecutor``
    """
    loop = current_thread()
    if isinstance(loop, EventThread):
        executor = loop.claim_executor()
    else:
        executor = ExecutorThread()
    
    return executor


class _AsyncIOIterator:
    """
    Asynchronous iterator for ``AsyncIO`` objects.
    
    Attributes
    ----------
    _wrapped : ``AsyncIO``
        The ``AsyncIO`` to asynchronous iterate over.
    """
    __slots__ = ('_wrapped',)
    
    def __init__(self, wrapped):
        """
        Creates a mew ``_AsyncIOIterator`` instance with the given parameter.
        
        Parameters
        ----------
        wrapped : ``AsyncIO``
            The ``AsyncIO`` to asynchronous iterate over.
        """
        self._wrapped = wrapped
    
    def __aiter__(self):
        """Asynchronous iterating an ``_AsyncIOIterator`` returns itself."""
        return self
    
    async def __anext__(self):
        """
        Reads a line from the respective file.
        
        This method is a coroutine.
        """
        result = await self._wrapped.readline()
        if result:
            return result
        
        raise StopAsyncIteration


class AsyncIO:
    """
    Asynchronous file-io, what uses an executor for it.
    
    Attributes
    ----------
    _executor : `None`, ``ExecutorThread`` or ``ClaimedExecutor``
        The executor what executes the io waiting. Set as `None` if the respective `file-io` is closed.
    _io : `file-io`
        The wrapped `file-io`.
    """
    __slots__ = ('_executor', '_io',)
    
    async def __new__(cls, *args, **kwargs):
        """
        Creates a new ``AsyncIO`` instance with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        *args : parameters
            Parameters to use when opening the respective file.
        **kwargs : keyword parameters
            Keyword parameters to use when opening the respective file.
        
        Notes
        -----
        Check `https://docs.python.org/3/library/functions.html#open` for parameters.
        """
        self = object.__new__(cls)
        self._executor = executor = get_executor()
        self._io = await executor.execute(alchemy_incendiary(open, args, kwargs))
        return self
    
    @classmethod
    def wrap(cls, io):
        """
        Wraps an already open file.
        
        Parameters
        ----------
        io : `file-io`
            The opened `file-io` to wrap.
        
        Returns
        -------
        self : ``AsyncIO``
        """
        self = object.__new__(cls)
        self._io = io
        if io.closed:
            executor = None
        else:
            executor = get_executor()
        self._executor = executor
        return self
    
    @property
    def buffer(self):
        """
        Returns the buffer of the underlying stream.
        
        Returns
        -------
        buffer : ``_io.BufferedWriter`` or ``_io.BufferedReader``
        """
        return self._io.buffer
    
    def __del__(self):
        """Releases the executor and closes the wrapped `file-io` if not yet done."""
        executor = self._executor
        if executor is None:
            return
        
        self._io.close()
        executor.release()
        self._executor = None
    
    close = __del__
    
    @property
    def closed(self):
        """
        Returns whether the ``AsyncIO`` instance is closed.
        
        Returns
        -------
        closed : `bool`
        """
        return (self._executor is None)
    
    async def detach(self):
        """
        Separates the wrapped `file-io`'s underlying raw stream from the buffer and return it.
        
        After detaching the ``AsyncIO`` becomes unusable.
        
        This method is a coroutine.
        
        Returns
        -------
        buffer : ``_io.BufferedWriter`` or ``_io.BufferedReader``
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        raw = await executor.execute(self._io.detach)
        self._executor = None
        return raw
    
    async def detach_to_self(self):
        """
        Separates the wrapped `file-io`'s underlying raw stream from the buffer and attaches it to the ``AsyncIO``
        
        This method is a coroutine.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        self._io = await executor.execute(self._io.detach)
    
    @property
    def encoding(self):
        """
        Returns the io-s encoding.
        
        Returns
        -------
        encoding : `str`
        """
        return self._io.encoding
    
    @property
    def errors(self):
        """
        Returns the error settings of the io.
        
        Returns
        -------
        errors : `str`
        """
        return self._io.errors
    
    def fileno(self):
        """
        Returns the underlying file descriptor.
        
        Returns
        -------
        fd : `int`
        """
        return self._io.fileno()
    
    async def flush(self):
        """
        Force bytes held in the buffer into the raw stream.
        
        This method is a coroutine.
        
        Raises
        ------
        BlockingIOError
            If the raw stream blocks.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        return await executor.execute(self._io.flush)
        
    def isatty(self):
        """
        Returns whether the stream is interactive.
        
        Returns
        -------
        isatty : `bool`
        """
        return self._io.isatty()
    
    @property
    def line_buffering(self):
        """
        Returns whether line buffering is enabled.
        
        Returns
        -------
        line_buffering : `bool`
        """
        return self._io.line_buffering
    
    @property
    def mode(self):
        """
        Returns the `mode` given to the constructor.
        
        Returns
        -------
        mode : `str`
        """
        return self._io.mode
    
    @property
    def name(self):
        """
        The file's name.
        
        Returns
        -------
        name : `str`
        """
        return self._io.name
    
    @property
    def newlines(self):
        """
        Indicating the newlines translated so far. Depending on the implementation and the initial constructor flags,
        this may not be available.
        
        Returns
        -------
        newlines : `None`, `str` or `tuple` of `str`
        """
        return self._io.newlines
    
    async def read(self, size=-1):
        """
        Reads from the underlying stream.
        
        This method is a coroutine.
        
        Parameters
        ----------
        size : `int`
            The upper limit to read from the underlying stream. If eof is received meanwhile reading, the already read
            data is returned.
            
            If given as negative `int`, then all the data till eof is read from the underlying stream.
        
        Returns
        -------
        data : `bytes` or `str`
            The read data.
        
        Raises
        ------
        BlockingIOError
            Might be raised if the underlying stream is in blocking mode.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        return await executor.execute(alchemy_incendiary(self._io.read, (size,),))
    
    def read1(self, *args):
        """
        Reads from the underlying stream.
        
        This method is a coroutine.
        
        Can be used for implementing your own buffering over ``.read``.
        
        Parameters
        ----------
        size : `int`
            The upper limit to read from the underlying stream. If eof is received meanwhile reading, the already read
            data is returned.
            
            If given as negative `int`, then all the data till eof is read from the underlying stream.
        
        Returns
        -------
        data : `bytes` or `str`
            The read data.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        return executor.execute(alchemy_incendiary(self._io.read1, args,))
    
    @property
    def readable(self):
        """
        Returns whether the underlying stream is readable.
        
        Returns
        -------
        readable : `bool`
        """
        return self._io.readable
    
    async def readinto(self, b):
        """
        Read bytes into a pre-allocated writable `bytes-like` object `b`, and return the number of bytes read.
        
        This method is a coroutine.
        
        Parameters
        ----------
        b : `bytes-like`
            Writable bytes like to write into.
        
        Raises
        ------
        BlockingIOError
            Might be raised if the underlying stream is in blocking mode.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        return await executor.execute(alchemy_incendiary(self._io.readinto, (b,),))
    
    async def readinto1(self, b):
        """
        Read bytes into a pre-allocated writable `bytes-like` object `b`, and return the number of bytes read.
        
        This method is a coroutine.
        
        Can be used for implementing your own buffering over ``.readinto``.
        
        Parameters
        ----------
        b : `bytes-like`
            Writable bytes like to write into.
        
        Raises
        ------
        BlockingIOError
            Might be raised if the underlying stream is in blocking mode.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        return await executor.execute(alchemy_incendiary(self._io.readinto1, (b,),))
    
    async def readline(self, size=-1):
        """
        Read until newline or EOF and return a single `str`. If the buffer is at EOF, returns an empty string.
        
        This method is a coroutine.
        
        Parameters
        ----------
        size : `int`
            The upper limit to read from the underlying stream. If eof is received meanwhile reading, the already read data is
            returned.
            
            If given as negative `int`, then all the data till linebreak or eof is read from the underlying stream.
        
        Returns
        -------
        line : `bytes` or `str`
            The red line.
        
        Raises
        ------
        BlockingIOError
            Might be raised if the underlying stream is in blocking mode.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        return await executor.execute(alchemy_incendiary(self._io.readline, (size,),))
    
    async def readlines(self, hint=-1):
        """
        Read and return a list of lines from the stream.
        
        This method is a coroutine.
        
        Parameters
        ----------
        hint : `int`
            The upper limit if lines to read.
            
            If given as negative `int`, then all the data till eof is read from the underlying stream.
        
        Raises
        ------
        BlockingIOError
            Might be raised if the underlying stream is in blocking mode.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        io = self._io
        return await executor.execute(alchemy_incendiary(io.__class__.readlines, (io, hint,),))
    
    async def seek(self, offset, whence=os.SEEK_SET):
        """
        Changes the stream position by the given offset. Offset is interpreted relative to the position indicated
        by `whence`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        offset : `int`
            Position to move the cursor to.
        whence : `int`, Optional
            How the given `offset` should be interpreted. Default value for whence is `os.SEEK_SET`.
            
            Can be given as:
            
            +-------------------+-------+-----------------------------------------------------------+
            | Respective name   | Value | Description                                               |
            +===================+=======+===========================================================+
            | os.SEEK_SET       | 0     | Start of the stream. Offset should be zero or positive.   |
            +-------------------+-------+-----------------------------------------------------------+
            | os.SEEK_CUR       | 1     | Current stream position. Offset may be negative.          |
            +-------------------+-------+-----------------------------------------------------------+
            | os.SEEK_END       | 2     | End of the stream. Offset is usually negative.            |
            +-------------------+-------+-----------------------------------------------------------+
            
        Returns
        -------
        position : `int`
            The new absolute position.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        io = self._io
        return await executor.execute(alchemy_incendiary(io.__class__.seek, (io, offset, whence),))
    
    def seekable(self):
        """
        Returns whether the stream supports random access. If not, then ``.seek``, ``.tell`` and ``.truncate`` will
        raise `OSError`.
        
        Returns
        -------
        seekable : `bool`
        """
        return self._io.seekable()
    
    async def tell(self):
        """
        Return the current stream position.
        
        This method is a coroutine
        
        Returns
        -------
        position : `int`
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        OSError
            If the underlying stream is not seekable.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        return await executor.execute(self._io.tell)
    
    async def truncate(self, size=None):
        """
        Resize the stream to the given size in bytes (or the current position if size is not specified). The current
        stream position isn’t changed. This resizing can extend or reduce the current file size. In case of extension,
        the contents of the new file area depend on the platform (on most systems, additional bytes are zero-filled).
        
        This method is a coroutine.
        
        Parameters
        ----------
        size : `None` or `int`, Optional
            The stream's new size in bytes.
        
        Returns
        -------
        size : `int`
            The new file size.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        OSError
            If the underlying stream is not seekable or writeable.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        io = self._io
        return await executor.execute(alchemy_incendiary(io.__class__.truncate, (io, size,),))
    
    def writable(self):
        """
        Returns whether the stream supports writing. If not, then, then ``.write``, ``.writelines``  and ``.truncate``
        will raise `OSError`.
        
        Returns
        -------
        writable : `bool`
        """
        return self._io.writable()
    
    async def write(self, b):
        """
        Write the given object, to the underlying raw stream, and return the number of bytes written.
        
        Depending on the implementation the written's data's amount might be less as the given object's length.
        
        This method is a coroutine.
        
        Parameters
        ----------
        b : `bytes-like` or `str`
            The object to write into the underlying stream.
        
        Returns
        -------
        written : `int`
            The amount of bytes written to the underlying stream.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        OSError
            If the underlying stream is not writeable.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        io = self._io
        return await executor.execute(alchemy_incendiary(io.__class__.write, (io, b,),))
    
    async def writelines(self, lines):
        """
        Write a list of lines to the stream. Line separators are not added, so it is usual for each of the lines
        provided to have a line separator at the end.
        
        This method is a coroutine.
        
        Parameters
        ----------
        b : `list` of (`bytes-like` or `str`)
            The lines to write into the underlying stream.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        OSError
            If the underlying stream is not writeable.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        io = self._io
        return await executor.execute(alchemy_incendiary(io.__class__.writelines, (io, lines,),))
    
    def __repr__(self):
        """Returns the io's representation"""
        result = [
            '<',
            self.__class__.__name__,
            ' io=',
            repr(self._io),
        ]
        
        executor = self._executor
        if executor is None:
            result.append(' closed')
        else:
            result.append(', executor=')
            result.append(repr(executor))
        
        result.append('>')
        
        return ''.join(result)
    
    __str__ = __repr__
    
    def __enter__(self):
        """
        Enters the asynchronous io as a context manager, closing it, when exited. Raises `ValueError` if already
        closed.
        """
        if self._executor is None:
            raise ValueError('Can not enter an already closed or detached io.')
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the asynchronous io."""
        self.__del__()
    
    def __aiter__(self):
        """
        Asynchronous iterates the asynchronous file-io.
        
        Returns
        -------
        iterator : ``_AsyncIOIterator``
        """
        return _AsyncIOIterator(self)


class _ReuAsyncIOIterator:
    """
    Asynchronous iterator for ``ReuAsyncIO`` objects.
    
    Attributes
    ----------
    _wrapped : ``ReuAsyncIO``
        The ``ReuAsyncIO`` to asynchronous iterate over.
    """
    __slots__ = ('_wrapped',)
    
    def __init__(self,wrapped):
        """
        Creates a mew ``_ReuAsyncIOIterator`` instance with the given parameter.
        
        Parameters
        ----------
        wrapped : ``ReuAsyncIO``
            The ``ReuAsyncIO`` to asynchronous iterate over.
        """
        self._wrapped = wrapped
    
    def __aiter__(self):
        """Asynchronous iterating an ``_ReuAsyncIOIterator`` returns itself."""
        return self
    
    async def __anext__(self):
        """Reads a line from the respective file."""
        wrapped = self._wrapped
        if wrapped._should_seek:
            await AsyncIO.seek(wrapped, 0)
            wrapped._should_seek = False
        
        result = await wrapped.readline()
        if result:
            return result
        raise StopAsyncIteration


class ReuAsyncIO(AsyncIO):
    """
    Reusable asynchronous file-io, supporting only opening in `read-bytes` mode, what seeks the cursor at `0`, when
    calling ``.close``. Use ``.real_close`` to close it for real, or use it with the `with` syntax.
    
    Should be used instead of `BytesIO` when sending it with http requests. Since the buffer is closed when a request
    is sent, at the case of received errors repeat could not be executed.
    
    Attributes
    ----------
    _executor : `None`, ``ExecutorThread`` or ``ClaimedExecutor``
        The executor what executes the io waiting. Set as `None` if the respective `file-io` is closed.
    _io : `file-io`
        The wrapped `file-io`.
    _should_seek : `bool`
        Whether the buffer was closed with ``.close`` and the next operation should seek back to `0`.
    """
    __slots__ = ('_executor', '_io', '_should_seek',)
    
    async def __new__(cls, path, mode='rb', *args, **kwargs):
        """
        Creates a new ``AsyncIO`` instance with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        path : `bytes` or `str`
            The file's path to open.
        mode : `str`
            The mode to open with the file. Defaults to `'rb'`.
        *args : parameters
            Parameters to use when opening the respective file.
        **kwargs : keyword parameters
            Keyword parameters to use when opening the respective file.
        
        Raises
        ------
        ValueError
            If `mode` is not given as `'rb'`, since ``ReuAsyncIO`` supports only `'rb'` mode.
        
        Notes
        -----
        Check `https://docs.python.org/3/library/functions.html#open` for parameters.
        """
        if mode != 'rb':
            raise ValueError(f'{cls.__name__} supports \'rb\' mode only, got {mode!r}.')
        
        self = object.__new__(cls)
        self._executor = executor = get_executor()
        self._io = await executor.execute(alchemy_incendiary(open, (path, mode, *args), kwargs))
        self._should_seek = False
        return self
    
    def close(self):
        """
        Sets the internal ``._should_seek`` slot to `True`, marking the io to seek back to the start at the next
        operation.
        """
        self._should_seek = True
    
    real_close = AsyncIO.__del__
    
    @classmethod
    def wrap(cls, io):
        """
        Wraps an already open file.
        
        Parameters
        ----------
        io : `file-io`
            The opened `file-io` to wrap.
        
        Returns
        -------
        self : ``ReuAsyncIO``
        """
        self = object.__new__(cls)
        self._io = io
        if io.closed:
            executor = None
        else:
            executor = get_executor()
        self._executor = executor
        self._should_seek = False
        return self
    
    async def detach(self):
        """
        Separates the wrapped `file-io`'s underlying raw stream from the buffer and return it.
        
        After detaching the ``ReuAsyncIO`` becomes unusable.
        
        This method is a coroutine.
        
        Returns
        -------
        buffer : ``_io.BufferedWriter`` or ``_io.BufferedReader``
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        raw = await executor.execute(self._io.detach)
        self._executor = None
        self._should_seek = False
        return raw
    
    @staticmethod
    def _seek_and_call(self, func, *args):
        """
        Staticmethod to seek to the respective stream's  `0` start, then call the given `func`.
        
        Parameters
        ----------
        self : ``ReuAsyncIO``
            The respective asynchronous io instance.
        func : `callable`
            The callable to call after seeking.
        *args : Parameters
            Additional parameters to call the given `func` with.
        
        Returns
        -------
        result : `Any`
            The returned value by the given `func`.
        """
        io = self._io
        io.seek(0)
        self._should_seek = False
        return func(self._io, *args)
    
    async def read(self, size=-1):
        """
        Reads from the underlying stream.
        
        This method is a coroutine.
        
        Parameters
        ----------
        size : `int`
            The upper limit to read from the underlying stream. If eof is received meanwhile reading, the already read
            data is returned.
            
            If given as negative `int`, then all the data till eof is read from the underlying stream.
        
        Returns
        -------
        data : `bytes` or `str`
            The read data.
        
        Raises
        ------
        BlockingIOError
            Might be raised if the underlying stream is in blocking mode.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        func = self._io.__class__.read
        if self._should_seek:
            task = alchemy_incendiary(self._seek_and_call, (self, func, size,),)
        else:
            task = alchemy_incendiary(func, (self._io, size,),)
        
        return await executor.execute(task)
        
    async def read1(self, *args):
        """
        Reads from the underlying stream.
        
        This method is a coroutine.
        
        Can be used for implementing your own buffering over ``.read``.
        
        Parameters
        ----------
        size : `int`
            The upper limit to read from the underlying stream. If eof is received meanwhile reading, the already read
            data is returned.
            
            If given as negative `int`, then all the data till eof is read from the underlying stream.
        
        Returns
        -------
        data : `bytes` or `str`
            The read data.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        func = self._io.__class__.read1
        if self._should_seek:
            task = alchemy_incendiary(self._seek_and_call, (self, func, *args,),)
        else:
            task = alchemy_incendiary(func, (self._io, *args),)
        
        return await executor.execute(task)
    
    async def readinto(self, b):
        """
        Read bytes into a pre-allocated writable `bytes-like` object `b`, and return the number of bytes read.
        
        This method is a coroutine.
        
        Parameters
        ----------
        b : `bytes-like`
            Writable bytes like to write into.
        
        Raises
        ------
        BlockingIOError
            Might be raised if the underlying stream is in blocking mode.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        func = self._io.__class__.readinto
        if self._should_seek:
            task = alchemy_incendiary(self._seek_and_call, (self, func, b,),)
        else:
            task = alchemy_incendiary(func, (self._io, b,),)
        
        return await executor.execute(task)
    
    async def readinto1(self, b):
        """
        Read bytes into a pre-allocated writable `bytes-like` object `b`, and return the number of bytes read.
        
        This method is a coroutine.
        
        Can be used for implementing your own buffering over ``.readinto``.
        
        Parameters
        ----------
        b : `bytes-like`
            Writable bytes like to write into.
        
        Raises
        ------
        BlockingIOError
            Might be raised if the underlying stream is in blocking mode.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        func = self._io.__class__.readinto1
        if self._should_seek:
            task = alchemy_incendiary(self._seek_and_call, (self, func, b,),)
        else:
            task = alchemy_incendiary(func, (self._io, b,),)
        
        return await executor.execute(task)
    
    async def readline(self, size=-1):
        """
        Read until newline or EOF and return a single `str`. If the buffer is at EOF, returns an empty string.
        
        This method is a coroutine.
        
        Parameters
        ----------
        size : `int`
            The upper limit to read from the underlying stream. If eof is received meanwhile reading, the already read data is
            returned.
            
            If given as negative `int`, then all the data till linebreak or eof is read from the underlying stream.
        
        Returns
        -------
        line : `bytes` or `str`
            The red line.
        
        Raises
        ------
        BlockingIOError
            Might be raised if the underlying stream is in blocking mode.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        func = self._io.__class__.readline
        if self._should_seek:
            task = alchemy_incendiary(self._seek_and_call, (self, func, size,),)
        else:
            task = alchemy_incendiary(func, (self._io, size,),)
        
        return await executor.execute(task)
    
    async def readlines(self, hint=-1):
        """
        Read and return a list of lines from the stream.
        
        This method is a coroutine.
        
        Parameters
        ----------
        hint : `int`, Optional
            The upper limit if lines to read. Defaults to `-1`.
            
            If given as negative `int`, then all the data till eof is read from the underlying stream.
        
        Returns
        -------
        lines : `list` of (`bytes` or `str`)
            The red lines.
        
        Raises
        ------
        BlockingIOError
            Might be raised if the underlying stream is in blocking mode.
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        func = self._io.__class__.readlines
        if self._should_seek:
            task = alchemy_incendiary(self._seek_and_call, (self, func, hint,),)
        else:
            task = alchemy_incendiary(func, (self._io, hint,),)
        
        return await executor.execute(task)
    
    async def seek(self, offset, whence=os.SEEK_SET):
        """
        Changes the stream position by the given offset. Offset is interpreted relative to the position indicated
        by `whence`.
        
        This method is a coroutine.
        
        Parameters
        ----------
        offset : `int`
            Position to move the cursor to.
        whence : `int`, Optional
            How the given `offset` should be interpreted. Default value for whence is `os.SEEK_SET`.
            
            Can be given as:
            
            +-------------------+-------+-----------------------------------------------------------+
            | Respective name   | Value | Description                                               |
            +===================+=======+===========================================================+
            | os.SEEK_SET       | 0     | Start of the stream. Offset should be zero or positive.   |
            +-------------------+-------+-----------------------------------------------------------+
            | os.SEEK_CUR       | 1     | Current stream position. Offset may be negative.          |
            +-------------------+-------+-----------------------------------------------------------+
            | os.SEEK_END       | 2     | End of the stream. Offset is usually negative.            |
            +-------------------+-------+-----------------------------------------------------------+
            
        Returns
        -------
        position : `int`
            The new absolute position.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        func = self._io.__class__.seek
        if self._should_seek:
            task = alchemy_incendiary(self._seek_and_call, (self, func, offset, whence,),)
        else:
            task = alchemy_incendiary(func, (self._io, offset, whence),)
        
        return await executor.execute(task)
    
    async def tell(self):
        """
        Return the current stream position.
        
        This method is a coroutine
        
        Returns
        -------
        position : `int`
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        OSError
            If the underlying stream is not seekable.
        """
        executor = self._executor
        if executor is None:
            raise ValueError(IO_CLOSED_OR_DETACHED)
        
        if self._should_seek:
            io = self._io
            await executor.execute(alchemy_incendiary(io.__class__.seek, (io, 0,),))
            self._should_seek = False
            return 0
        
        return await executor.execute(self._io.tell)
    
    def __aiter__(self):
        """
        Asynchronous iterates the asynchronous file-io.
        
        Returns
        -------
        iterator : ``_ReuAsyncIOIterator``
        """
        return _ReuAsyncIOIterator(self)
