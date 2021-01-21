# -*- coding: utf-8 -*-
import os, sys, errno
from stat import S_ISCHR, S_ISFIFO, S_ISSOCK
from subprocess import TimeoutExpired, PIPE, Popen
from socket import socketpair as create_socket_pair

from .futures import Task, Future, WaitTillAll, future_or_timeout
from .protocol import ReadProtocolBase

IS_AIX = sys.platform.startswith('aix')
LIMIT = 1<<16
MAX_READ_SIZE = 262144

PROCESS_EXIT_DELAY_LIMIT = 10

class UnixReadPipeTransport(object):
    """
    Asynchronous read only transport implementation for pipes.
    
    Attributes
    ----------
    _extra : `dict` of (`str`, `Any`) items
        Optional transport information.
    closing : `bool`
        Whether the transport ic closing.
    fileno : `int`
        The used socket's file descriptor number.
    loop : ``EventThread``
        The respective event loop of the transport.
    pipe : `None` or `file-like` object
        The pipe to connect to on read end.
        
        Is set to non-blocking mode.
        
        After closing the transport is set to `None`.
    protocol : `None`, ``SubprocessReadPipeProtocol``, `Any`
        Asynchronous protocol implementation used by the transport.
        
        After closing the transport is set to `None`.
    """
    __slots__ = ('_extra', '_paused', 'closing', 'fileno', 'loop', 'pipe', 'protocol')
    async def __new__(cls, loop, pipe, protocol, extra=None):
        """
        Creates a new ``UnixReadPipeTransport`` instance with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        loop : ``EventThread``
            The respective event loop of the transport.
        pipe : `file-like` object
            The pipe to connect to on read end.
        protocol : ``SubprocessReadPipeProtocol`` or `Any`
            Asynchronous protocol implementation used by the transport.
        extra : `None` or `dict` of (`str`, `Any`) items, Optional
            Optional transport information.
        
        Raises
        ------
        ValueError
            If `pipe` was not given neither as pipe, socket or character device.
        """
        fileno = pipe.fileno()
        mode = os.fstat(fileno).st_mode
        if not (S_ISFIFO(mode) or S_ISSOCK(mode) or S_ISCHR(mode)):
            raise ValueError(f'{cls.__name__} is only for pipes, sockets and character devices, got '
                f'{pipe.__class__.__name__}; {pipe!r}.')
        
        self = object.__new__(cls)
        if extra is None:
            extra = {}
        
        extra['pipe'] = pipe
        
        self._extra = extra
        self.loop = loop
        self.pipe = pipe
        self.fileno = fileno
        self.protocol = protocol
        self.closing = False
        self._paused = False
        
        try:
            os.set_blocking(fileno, False)
            # skip 1 callback loop
            future = Future(loop)
            loop.call_soon(Future.set_result_if_pending, future, None)
            await future
            
            protocol.connection_made(self)
            loop.add_reader(fileno, self._read_ready)
        
        except:
            self.close()
            raise
        
        return self
    
    def get_extra_info(self, name, default=None):
        """
        Gets optional transport information.
        
        Parameters
        ----------
        name : `str`
            The extra information's name to get.
        default : `Any`, Optional
            Default value to return if `name` could not be matched. Defaults to `None`.
        
        Returns
        -------
        info : `default`, `Any`
        """
        return self._extra.get(name, default)
    
    def __repr__(self):
        """Returns the ``UnixReadPipeTransport``'s representation."""
        return f'<{self.__class__.__name__} fd={self.fileno}>'
    
    def _read_ready(self):
        """
        Added as a read callback on the respective event loop to be called when the data is received on the pipe.
        """
        try:
            data = os.read(self.fileno, MAX_READ_SIZE)
        except (BlockingIOError, InterruptedError):
            pass
        except OSError as err:
            self._fatal_error(err, 'Fatal read error on pipe transport')
        else:
            if data:
                self.protocol.data_received(data)
            else:
                self.closing = True
                loop = self.loop
                loop.remove_reader(self.fileno)
                protocol = self.protocol
                loop.call_soon(protocol.__class__.eof_received, protocol)
                loop.call_soon(self.__class__._call_connection_lost, self, None)
    
    def pause_reading(self):
        """
        Pauses the receiving end.
        
        No data will be passed to the respective protocol's ``.data_received`` method until ``.resume_reading`` is
        called.
        """
        if self.closing or self._paused:
            return
        
        self._paused = True
        self.loop.remove_reader(self.fileno)
    
    def resume_reading(self):
        """
        Resumes the receiving end.
        
        Data received will once again be passed to the respective protocol's ``.data_received`` method.
        """
        if self.closing or not self._paused:
            return
        
        self._paused = False
        self.loop.add_reader(self.fileno, self._read_ready)
    
    def set_protocol(self, protocol):
        """
        Sets a new protocol to the transport.
        
        Parameters
        ----------
        protocol : ``SubprocessReadPipeProtocol`` or `Any`
            Asynchronous protocol implementation.
        """
        self.protocol = protocol
    
    def get_protocol(self):
        """
        Gets the read pipe transport's actual protocol.
        
        Returns
        -------
        protocol : `None`, ``SubprocessReadPipeProtocol`` or `Any`
            Asynchronous protocol implementation.
        """
        return self.protocol
    
    def is_closing(self):
        """
        Returns whether the read pipe transport is closing.
        
        Returns
        -------
        is_closing : `bool`
        """
        return self.closing
    
    def close(self):
        """
        Starts the shutdown process of the read pipe transport.
        """
        if not self.closing:
            self._close(None)
    
    def __del__(self):
        """
        Closes the read pipe transport if not yet closed.
        """
        pipe = self.pipe
        if (pipe is not None):
            pipe.close()
    
    def _fatal_error(self, exception, message='Fatal error on pipe transport'):
        """
        If a fatal error occurs on the transport, renders its traceback and closes itself.
        
        Parameters
        ----------
        exception : `BaseException`
            The occurred exception.
        message : `str`, Optional
            Additional error message to render.
        """
        if not (isinstance(exception, OSError) and (exception.errno == errno.EIO)):
            self.loop.render_exc_async(exception, [message, '\non: ', repr(self), '\n'])
        
        self._close(exception)
    
    def _close(self, exception):
        """
        Starts the transport's closing process.
        
        Parameters
        ----------
        exception : `None` or ``BaseException``
            Defines whether the connection is closed, or an exception was received.
            
            If the connection was closed, then `exception` is given as `None`. This can happen at the case, when eof is
            received as well.
        """
        self.closing = True
        loop = self.loop
        loop.remove_reader(self.fileno)
        loop.call_soon(self.__class__._call_connection_lost, self, exception)
    
    def _call_connection_lost(self, exception):
        """
        Calls the read pipe transport's protocol's `.connection_lost` with the given exception and closes the
        transport's pipe.
        
        Parameters
        ----------
        exception : `None` or ``BaseException``
            Exception to call the protocol's ``.connection_lost`` with.
            
            Defines whether the connection is closed, or an exception was received.
            
            If the connection was closed, then `exception` is given as `None`. This can happen at the case, when eof is
            received as well.
        """
        protocol = self.protocol
        if protocol is None:
            return
        
        try:
            protocol.connection_lost(exception)
        finally:
            pipe = self.pipe
            if (pipe is not None):
                self.pipe = None
                pipe.close()
            
            self.protocol = None

class UnixWritePipeTransport(object):
    """
    Asynchronous write only transport implementation for pipes.
    
    Attributes
    ----------
    _buffer : `bytearray`
        Data ensured to be written on the wrapped pipe as it becomes readable again.
    _high_water : `int`
        The ``.protocol`` is paused writing when the buffer size passes the high water mark. Defaults to `65536`.
    _low_water : `int`
        The ``.protocol`` is resumed writing when the buffer size goes under the low water mark. Defaults to `16384`.
    _extra : `dict` of (`str`, `Any`) items
        Optional transport information.
    closing : `bool`
        Whether the transport ic closing.
    fileno : `int`
        The used socket's file descriptor number.
    loop : ``EventThread``
        The respective event loop of the transport.
    pipe : `None` or `file-like` object
        The pipe to connect to on read end.
        
        Is set to non-blocking mode.
        
        After closing the transport is set to `None`.
    protocol : `None`, ``SubprocessWritePipeProtocol`` or `Any`
        Asynchronous protocol implementation used by the transport.
        
        After closing the transport is set to `None`.
    protocol_paused : `bool`
        Whether ``.protocol`` is paused writing.
    """
    __slots__ = ('_buffer', '_extra', '_high_water', '_low_water', 'closing', 'fileno', 'loop', 'pipe', 'protocol',
        'protocol_paused')
    
    async def __new__(cls, loop, pipe, protocol, extra=None):
        """
        Creates a new ``UnixWritePipeTransport`` instance with the given parameters.
        
        Parameters
        ----------
        loop : ``EventThread``
            The respective event loop of the transport.
        pipe `: file-like` object
            The pipe to connect to on read end.
        protocol : ``SubprocessWritePipeProtocol`` or `Any`
            Asynchronous protocol implementation used by the transport.
        extra : `None` or `dict` of (`str`, `Any`) items, Optional
            Optional transport information.

        Raises
        ------
        ValueError
            If `pipe` was not given neither as pipe, socket or character device.
        """
        fileno = pipe.fileno()
        mode = os.fstat(fileno).st_mode
        is_char = S_ISCHR(mode)
        is_fifo = S_ISFIFO(mode)
        is_socket = S_ISSOCK(mode)
        if not (is_char or is_fifo or is_socket):
            raise ValueError('Pipe transport is only for pipes, sockets and character devices, got '
                f'{pipe.__class__.__name__}; {pipe!r}.')
        
        if extra is None:
            extra = {}
        
        extra['pipe'] = pipe
        
        self = object.__new__(cls)
        self._extra = extra
        self.loop = loop
        self.protocol_paused = False
        self.pipe = pipe
        self.fileno = fileno
        self.protocol = protocol
        self._buffer = bytearray()
        self.closing = False  # Set when close() or write_eof() called.
        
        self._high_water = 65536
        self._low_water = 16384
        
        try:
            os.set_blocking(fileno, False)
            # skip 1 callback loop
            future = Future(loop)
            loop.call_soon(Future.set_result_if_pending, future, None)
            await future
            
            protocol.connection_made(self)
            
            # On AIX, the reader trick (to be notified when the read end of the  socket is closed) only works for
            # sockets. On other platforms it works for pipes and sockets.
            if is_socket or (is_fifo and not IS_AIX):
                loop.add_reader(fileno, self._read_ready)
        except:
            self.close()
            raise
        
        return self
    
    def __repr__(self):
        """Returns the ``UnixWritePipeTransport``'s representation."""
        return f'<{self.__class__.__name__} fd={self.fileno}>'
    
    def get_extra_info(self, name, default=None):
        """
        Gets optional transport information.
        
        Parameters
        ----------
        name : `str`
            The extra information's name to get.
        default : `Any`, Optional
            Default value to return if `name` could not be matched. Defaults to `None`.
        
        Returns
        -------
        info : `default`, `Any`
        """
        return self._extra.get(name, default)
    
    def get_write_buffer_size(self):
        """
        Return the current size of the write buffer.
        
        Returns
        -------
        get_write_buffer_size : `int`
        """
        return len(self._buffer)
    
    def _read_ready(self):
        """
        Added as a read callback on the respective event loop to be called when the data is received on the pipe.
        
        If this happens, since it is a write only pipe, means it should be closed, so we do like that.
        """
        # Pipe was closed by peer.
        if self._buffer:
            exception = BrokenPipeError()
        else:
            exception = None
            
        self._close(exception)
    
    def write(self, data):
        """
        Write the given data to the transport.
        
        The method do no blocks, instead arranges the data to be sent asynchronously.
        
        Parameters
        ----------
        data : `bytes-like`
            The bytes data to be sent.
        """
        if not data:
            return
        
        if isinstance(data, bytearray):
            data = memoryview(data)
        
        if self.closing:
            return
        
        buffer = self._buffer
        if not buffer:
            try:
                n = os.write(self.fileno, data)
            except (BlockingIOError, InterruptedError):
                n = 0
            except BaseException as err:
                self._fatal_error(err, 'Fatal write error on pipe transport')
                return
            
            if n == len(data):
                return
            
            if n > 0:
                data = memoryview(data)[n:]
            
            self.loop.add_writer(self.fileno, self._write_ready)
        
        buffer.extend(data)
        self._maybe_pause_protocol()
    
    def _write_ready(self):
        """
        Added as a write callback on the respective event loop when the transport has unsent data. Called when the
        respective socket becomes writable.
        """
        buffer = self._buffer
        
        try:
            n = os.write(self.fileno, buffer)
        except (BlockingIOError, InterruptedError):
            pass
        except BaseException as err:
            buffer.clear()
            self.loop.remove_writer(self.fileno)
            self._fatal_error(err, 'Fatal write error on pipe transport')
        else:
            if n == len(buffer):
                buffer.clear()
                self.loop.remove_writer(self.fileno)
                self._maybe_resume_protocol()  # May append to buffer.
                if self.closing:
                    self.loop.remove_reader(self.fileno)
                    self._call_connection_lost(None)
                return
            
            if n > 0:
                del buffer[:n]
    
    def can_write_eof(self):
        """
        Return whether the transport supports ``.write_eof``.
        
        Returns
        -------
        can_write_eof : `bool`
            ``UnixWritePipeTransport`` instances always return `True`.
        """
        return True
    
    def write_eof(self):
        """
        Writes eof to the transport's protocol if applicable.
        
        If the write transport's buffer is empty, calls connection lost as well.
        """
        if self.closing:
            return
        
        self.closing = True
        if not self._buffer:
            loop = self.loop
            loop.remove_reader(self.fileno)
            loop.call_soon(self.__class__._call_connection_lost, self, None)
    
    def set_protocol(self, protocol):
        """
        Sets a new protocol to the transport.
        
        Parameters
        ----------
        protocol : ``SubprocessWritePipeProtocol`` or `Any`
            Asynchronous protocol implementation.
        """
        self.protocol = protocol
    
    def get_protocol(self):
        """
        Gets the transport's actual protocol.
        
        Returns
        -------
        protocol : `None`, ``SubprocessWritePipeProtocol` or  `Any`
            Asynchronous protocol implementation.
        """
        return self.protocol
    
    def is_closing(self):
        """
        Returns whether the read pipe transport is closing.
        
        Returns
        -------
        is_closing : `bool`
        """
        return self.closing
    
    def close(self):
        """
        Starts the shutdown process of the write pipe transport.
        """
        if (self.pipe is not None) and (not self.closing):
            self.write_eof()
    
    def __del__(self):
        """
        Closes the write pipe transport if not yet closed.
        """
        pipe = self.pipe
        if (pipe is not None):
            pipe.close()
    
    def abort(self):
        """
        Close the transport immediately.
        
        The buffered data will be lost.
        """
        self._close(None)
    
    def _fatal_error(self, exception, message='Fatal error on pipe transport'):
        """
        If a fatal error occurs on the transport, renders its traceback and closes itself.
        
        Parameters
        ----------
        exception : `BaseException`
            The occurred exception.
        message : `str`, Optional
            Additional error message to render.
        """
        if not isinstance(exception, OSError):
            self.loop.render_exc_async(exception, [message, '\non: ', repr(self), '\n'])
        
        self._close(exception)
    
    def _close(self, exception):
        """
        Starts the transport's closing process.
        
        Parameters
        ----------
        exception : `None` or ``BaseException``
            Defines whether the connection is closed, or an exception was received.
            
            If the connection was closed, then `exception` is given as `None`. This can happen at the case, when eof is
            received as well.
        """
        self.closing = True
        
        loop = self.loop
        buffer = self._buffer
        if buffer:
            self.loop.remove_writer(self.fileno)
            buffer.clear()
        
        loop.remove_reader(self.fileno)
        loop.call_soon(self.__class__._call_connection_lost, self, exception)
    
    def _call_connection_lost(self, exception):
        """
        Calls the write pipe transport's protocol's `.connection_lost` with the given exception and closes the
        transport's pipe.
        
        Parameters
        ----------
        exception : `None` or ``BaseException``
            Exception to call the protocol's ``.connection_lost`` with.
            
            Defines whether the connection is closed, or an exception was received.
            
            If the connection was closed, then `exception` is given as `None`. This can happen at the case, when eof is
            received as well.
        """
        protocol = self.protocol
        if protocol is None:
            return
        
        try:
            protocol.connection_lost(exception)
        finally:
            pipe = self.pipe
            if (pipe is not None):
                self.pipe = None
                pipe.close()
            
            self.protocol = None
    
    def _maybe_pause_protocol(self):
        """
        Called after data was ensured to be written into the transfer to check whether it's protocol should be paused.
        """
        size = self.get_write_buffer_size()
        if size <= self._high_water:
            return
        
        if self.protocol_paused:
            return
        
        self.protocol_paused = True
        
        protocol = self.protocol
        if protocol is None:
            return
        
        try:
            protocol.pause_writing()
        except BaseException as err:
            self.loop.render_exc_async(err, [
                repr(self), '`._maybe_pause_protocol` failed\n'
                'On: ', repr(protocol), '.pause_writing()\n'])
    
    def _maybe_resume_protocol(self):
        """
        Called after successful writing to the pipe to check whether the protocol should be resumed.
        """
        if (self.protocol_paused and self.get_write_buffer_size() <= self._low_water):
            self.protocol_paused = False
            protocol = self.protocol
            if (protocol is not None):
                try:
                    protocol.resume_writing()
                except BaseException as err:
                    self.loop.render_exc_async(err, [
                        repr(self), '`._maybe_resume_protocol` failed\n'
                        'on: ', repr(protocol), '.resume_writing()\n'])
    
    def get_write_buffer_limits(self):
        """
        Returns the low and the high water of the transport.
        
        Returns
        -------
        low_water : `int`
            The ``.protocol`` is paused writing when the buffer size passes the high water mark. Defaults to `65536`.
        high_water : `int`
            The ``.protocol`` is resumed writing when the buffer size goes under the low water mark. Defaults to
            `16384`.
        """
        return (self._low_water, self._high_water)
    
    def _set_write_buffer_limits(self, low=None, high=None):
        """
        Sets the write buffer limits of the transport.
        
        Parameters
        ----------
        low : None` or `int`, Optional
            The ``.protocol`` is paused writing when the buffer size passes the high water mark. Defaults to `65536`.
        high : `None` or `int`, Optional
            The ``.protocol`` is resumed writing when the buffer size goes under the low water mark. Defaults to
            `16384`.

        Raises
        ------
        ValueError
            If `high` is lower than `low` or if `low` is lower than `0`.
        """
        if high is None:
            if low is None:
                high = 65536
                low = 16384
            else:
                high = low<<2
        else:
            if low is None:
                low = high>>2
        
        if low < 0 or high < low:
            raise ValueError(f'High water must be greater or equal than low, what must be greater than equal than `0`, '
                f'got high={high!r}; low={low!r}.')
        
        self._high_water = high
        self._low_water = low
    
    def set_write_buffer_limits(self, low=None, high=None):
        """
        Set the high- and low-water limits for write flow control.
        
        These two values control when to call the protocol's ``.pause_writing`` and ``.resume_writing`` methods. If
        specified, the low-water limit must be less than or equal to the high-water limit. Neither value can be
        negative. The defaults are implementation-specific. If only the high-water limit is given, the low-water limit
        defaults to an implementation-specific value less than or equal to the high-water limit. Setting high to zero
        forces low to zero as well, and causes ``.pause_writing`` to be called whenever the buffer becomes non-empty.
        Setting low to zero causes ``.resume_writing`` to be called only once the buffer is empty. Use of zero for
        either limit is generally sub-optimal as it reduces opportunities for doing I/O and computation concurrently.
        
        Parameters
        ----------
        low : None` or `int`, Optional
            The ``.protocol`` is paused writing when the buffer size passes the high water mark. Defaults to `65536`.
        high : `None` or `int`, Optional
            The ``.protocol`` is resumed writing when the buffer size goes under the low water mark. Defaults to
            `16384`.
        
        Raises
        ------
        ValueError
            If `low` is lower than `0` or if `low` is higher than `high`.
        """
        self._set_write_buffer_limits(low=low, high=high)
        self._maybe_pause_protocol()

class SubprocessStreamWriter(object):
    """
    Writer interface for subprocess calls.
    
    Attributes
    ----------
    loop : ``EventThread``
        The respective event loop of the stream.
    transport : ``UnixWritePipeTransport`` or `Any`
        Asynchronous transport implementation.
    protocol : ``AsyncProcess`` or `Any`
        Asynchronous protocol implementation.
    """
    __slots__ = ('loop', 'transport', 'protocol', )
    def __init__(self, loop, transport, protocol):
        """
        Stream-writer used as ``AsyncProcess.stdin``.
        
        Parameters
        ----------
        loop : ``EventThread``
            The respective event loop of the stream.
        transport : ``UnixWritePipeTransport`` or `Any`
            Asynchronous transport implementation.
        protocol : ``AsyncProcess`` or `Any`
            Asynchronous protocol implementation.
        """
        self.transport = transport
        self.protocol = protocol
        self.loop = loop
    
    def write(self, data):
        """
        Write the given data to subprocess pipe's transport.
        
        The method do no blocks, instead arranges the data to be sent asynchronously.
        
        Parameters
        ----------
        data : `bytes-like`
            The bytes data to be sent.
        """
        self.transport.write(data)
    
    def writelines(self, data):
        """
        Writes the given lines to the subprocess pipe's transport.
        
        Parameters
        ----------
        data : `iterable` of `bytes-like`
            The lines to write.
        
        Raises
        ------
        RuntimeError
            Protocol has no attached transport.
        """
        self.transport.writelines(data)
    
    def write_eof(self):
        """
        Writes eof to the subprocess pipe's transport's protocol if applicable.
        
        By default ``SubprocessStreamWriter``'s transport is ``UnixWritePipeTransport``, what will call connection lost
        as well when the write buffer is empty.
        """
        return self.transport.write_eof()
    
    def can_write_eof(self):
        """
        Return whether the pipe's transport supports ``.write_eof``.
        
        Returns
        -------
        can_write_eof : `bool`
            By default ``SubprocessStreamWriter``'s transport is ``UnixWritePipeTransport`` instance, what always
            return `True`.
        """
        return self.transport.can_write_eof()
    
    def close(self):
        """
        Starts the shutdown process of subprocess pipe's transport.
        """
        return self.transport.close()
    
    def is_closing(self):
        """
        Returns whether the subprocess pipe's transport is closing.
        
        Returns
        -------
        is_closing : `bool`
        """
        return self.transport.is_closing()
    
    async def wait_closed(self):
        """
        Blocks till the subprocess pipe's protocol closes.
        
        This method is a coroutine.
        """
        await self.protocol._get_close_waiter(self)
    
    def get_extra_info(self, name, default=None):
        """
        Gets optional transport information.
        
        Parameters
        ----------
        name : `str`
            The extra information's name to get.
        default : `Any`, Optional
            Default value to return if `name` could not be matched. Defaults to `None`.
        
        Returns
        -------
        info : `default`, `Any`
        """
        return self.transport.get_extra_info(name, default)
    
    async def drain(self):
        """
        Blocks till the write buffer is drained.
        
        This method is a coroutine.
        
        Raises
        ------
        BaseException
            Connection lost exception if applicable.
        """
        if self.transport.is_closing():
            loop = self.loop
            future = Future(loop)
            loop.call_soon(Future.set_result_if_pending, future, None)
            await future
        
        await self.protocol._drain_helper()

class SubprocessWritePipeProtocol(object):
    """
    Asynchronous subprocess write pipe protocol.
    
    Attributes
    ----------
    disconnected : `bool`
        Whether the protocol is disconnected.
    fd : `int`
        The used socket's file descriptor number.
    transport : ``UnixWritePipeTransport`` or `Any`
        Asynchronous transport implementation.
    process : ``AsyncProcess``
        The parent process of the pipe protocol.
    """
    __slots__ = ('disconnected', 'fd', 'transport', 'process', )
    
    def __init__(self, process, fd):
        """
        Creates a new ``SubprocessWritePipeProtocol`` instance with the given parameters.
        
        Parameters
        ----------
        process : ``AsyncProcess``
            The parent process of the pipe protocol.
        fd : `int`
            The used socket's file descriptor number.
        """
        self.process = process
        self.fd = fd
        self.transport = None
        self.disconnected = False
    
    def __call__(self):
        """
        ``SubprocessWritePipeProtocol`` instances return themselves allowing using them as their one-time factory.
        
        Returns
        -------
        self : ``SubprocessWritePipeProtocol``
        """
        return self
    
    def connection_made(self, transport):
        """
        Called when the connection is made.
        
        Sets the ``SubprocessWritePipeProtocol``'s ``.transport``.
        
        Parameters
        ----------
        transport : ``UnixWritePipeTransport`` or `Any`
            Asynchronous transport implementation.
        """
        self.transport = transport
    
    def __repr__(self):
        """Returns the subprocess write protocol's representation."""
        return f'<{self.__class__.__name__} fd={self.fd} pipe={self.transport!r}>'
    
    def connection_lost(self, exception):
        """
        Called when the connection is lost or closed.
        
        Parameters
        ----------
        exception : `None` or `BaseException` instance
            Defines whether the connection is closed, or an exception was received.
            
            If the connection was closed, then `exception` is given as `None`. This can happen at the case, when eof is
            received as well.
        """
        process = self.process
        if (process is not None):
            self.process = None
            process._pipe_connection_lost(self.fd, exception)
            self.disconnected = True
    
    def pause_writing(self):
        """
        Called when the transport's buffer goes over the high-water mark.
        
        ``.pause_writing`` is called when the buffer goes over the high-water mark, and eventually
        ``.resume_writing`` is called when the buffer size reaches the low-water mark.
        """
        self.process.pause_writing()
    
    def resume_writing(self):
        """
        Called when the transport's buffer drains below the low-water mark.
        
        See ``.pause_writing`` for details.
        """
        self.process.resume_writing()

class SubprocessReadPipeProtocol(SubprocessWritePipeProtocol):
    """
    Asynchronous subprocess read pipe protocol.
    
    Attributes
    ----------
    disconnected : `bool`
        Whether the protocol is disconnected.
    fd : `int`
        The used socket's file descriptor number.
    transport : ``UnixWritePipeTransport`` or `Any`
        Asynchronous transport implementation.
    process : ``AsyncProcess``
        The parent process of the pipe protocol.
    """
    __slots__ = ()
    def data_received(self, data):
        """
        Called when some data is received on the pipe.
        
        Parameters
        ----------
        data : `bytes`
            The received data.
        """
        self.process._pipe_data_received(self.fd, data)
    
    def eof_received(self):
        # connection_lost is received anyways after eof, and connection_lost without exception will cause eof.
        """
        Calling ``.connection_lost`` without exception causes eof. ``.connection_lost`` is called anyways after
        ``.eof_received``, so this method does nothing.
        
        Returns
        -------
        transport_closes : `bool`
            Returns `False` if the transport will close itself. If it returns `True`, then closing the transport is up
            to the protocol.
            
            Always returns `False`.
        """
        return False


class AsyncProcess(object):
    """
    Asynchronous process implementation.
    
    Attributes
    ----------
    _alive_fds : `list` if `int`
        A list of alive file descriptor's respective internal identifier.
        
        Can have the following elements:
        
        +-------------------+-------+
        | Respective name   | Value |
        +===================+=======+
        | stdin             | `0`   |
        +-------------------+-------+
        | stdout            | `1`   |
        +-------------------+-------+
        | stderr            | `2`   |
        +-------------------+-------+
    
    _connection_lost : `bool`
        Whether all the pipes of the ``AsyncProcess`` lost connection.
    _drain_waiter : `None` or ``Future``
        A future, what is used to block the writing task, till it's writen data is drained.
    _exit_waiters : `None` or `set of ``Future``
        Waiter futures which wait for the subprocess to shutdown.
    _extra : `dict` of (`str`, `Any`) items
        Optional transport information.
    _paused : `bool`
        Whether the subprocess is paused writing because it hit's the high water mark.
    _pending_calls : `None` or `list` of (`callable`, `tuple` of `Any`)
        Meanwhile the subprocess connection is established, this attribute is set as a list to put connection lost
        and related calls it to with their parameters.
    _subprocess_stderr_protocol : `None` or ``SubprocessReadPipeProtocol``
        Protocol of the stderr pipe if applicable.
    _subprocess_stdin_protocol : `None` or ``SubprocessWritePipeProtocol``
        Protocol of the stdin pipe if applicable.
    _subprocess_stdout_protocol : `None` or ``SubprocessReadPipeProtocol``
        Protocol of the stdout pipe if applicable.
    closed : `bool`
        Whether subprocess is closed.
    loop : ``EventThread``
        the respective event loop of the async subprocess to what is bound to.
    process : `subprocess.Process`
        The internal blocking subprocess object.
    process_id : `int`
        The subprocess identifier.
    return_code : `None` or `int`
        The returned exit code of the subprocess. Set as `None` if not yet applicable.
    stderr : ``ReadProtocolBase``
        Asynchronous stderr implementation.
    stdin : ``SubprocessStreamWriter``
        Asynchronous stdin implementation.
    stdout : ``ReadProtocolBase``
        Asynchronous stdout implementation.
    """
    __slots__ = ('_alive_fds', '_connection_lost', '_drain_waiter', '_exit_waiters', '_extra', '_paused',
        '_pending_calls', '_subprocess_stderr_protocol', '_subprocess_stdin_protocol', '_subprocess_stdout_protocol',
        'closed', 'loop', 'process_id', 'process', 'return_code', 'stderr', 'stdin', 'stdout', )
    
    async def __new__(cls, loop, process_arguments, shell, stdin, stdout, stderr, buffer_size, extra,
            process_open_kwargs):
        """
        Creates a new ``AsyncProcess`` instance.
        
        Parameters
        ----------
        loop : ``EventThread``
            The event loop to what the async process is bound to.
        process_arguments : `tuple` of `Any`
            Process arguments to open the subprocess with.
        shell : `bool
            Whether the specified command will be executed through the shell.
        stdin : `file-like`, `subprocess.PIPE`.
            Standard input for the created shell. Defaults to `subprocess.PIPE`.
        stdout : `file-like`, `subprocess.PIPE`, `subprocess.DEVNULL`
            Standard output for the created shell.
        stderr : `file-like`, `subprocess.PIPE`, `subprocess.DEVNULL`, `subprocess.STDOUT`
            Standard error for the created shell.
        buffer_size : `int`
            Will be supplied as the corresponding argument to the open() function when creating the
            stdin/stdout/stderr pipe file objects:
            
            Expected values:
            
            +---------------+-----------+-----------------------------------------------------------------------+
            | Name          | Value     | Description                                                           |
            +===============+===========+=======================================================================+
            | unbuffered    | `0`       | Read and write are one system call and can return short.              |
            +---------------+-----------+-----------------------------------------------------------------------+
            | line buffered | `1`       | Only usable if `universal_newlines=True`, for example in text mode.   |
            +---------------+-----------+-----------------------------------------------------------------------+
            | buffer size   | `>1`      | Use a buffer of approximately to that value.                          |
            +---------------+-----------+-----------------------------------------------------------------------+
            | default       | `<0`      | use the system default: `io.DEFAULT_BUFFER_SIZE`.                     |
            +---------------+-----------+-----------------------------------------------------------------------+
            
        extra : `None` or `dict` of (`str`, `Any`) items
            Optional transport information.
        process_open_kwargs : `dict` of (`str`, `Any`) items
            Additional parameters to open the process with.
        
        Raises
        ------
        TypeError
            If `process_open_kwargs` contains unexpected key.
        """
        if stdin == PIPE:
            # Use a socket pair for stdin, since not all platforms support selecting read events on the write end of a
            # socket (which we use in order to detect closing of the other end).  Notably this is needed on AIX, and
            # works just fine on other platforms.
            stdin_r, stdin_w = create_socket_pair()
        else:
            stdin_r = stdin
            stdin_w = None
        
        process = None
        
        try:
            process = Popen(process_arguments, shell=shell, stdin=stdin_r, stdout=stdout, stderr=stderr,
                universal_newlines=False, bufsize=buffer_size, **process_open_kwargs)
            
            if (stdin_w is not None):
                stdin_r.close()
                process.stdin = open(stdin_w.detach(), 'wb', buffering=buffer_size)
                stdin_w = None
        except:
            if (process is not None) and (process.poll() is None):
                try:
                    process.kill()
                except ProcessLookupError:
                    pass
            
            raise
        finally:
            if (stdin_w is not None):
                stdin_r.close()
                stdin_w.close()
        
        if extra is None:
            extra = {}
        
        extra['subprocess'] = process
        
        self = object.__new__(cls)
        self._extra = extra
        self.closed = False
        self.loop = loop
        self.process = process
        self.process_id = process.pid
        self.return_code = None
        self._exit_waiters = None
        self._pending_calls = []
        self._subprocess_stdin_protocol = None
        self._subprocess_stdout_protocol = None
        self._subprocess_stderr_protocol = None
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self._paused = False
        self._drain_waiter = None
        self._connection_lost = False
        self._alive_fds = []
        
        try:
            stdin = process.stdin
            if (stdin is not None):
                subprocess_stdin_protocol = SubprocessWritePipeProtocol(self, 0)
                await loop.connect_write_pipe(subprocess_stdin_protocol, stdin)
                self._subprocess_stdin_protocol = subprocess_stdin_protocol
                stdin_transport = subprocess_stdin_protocol.transport
                if (stdin_transport is not None):
                    self.stdin = SubprocessStreamWriter(loop, stdin_transport, self)
            
            stdout = process.stdout
            if (stdout is not None):
                subprocess_stdout_protocol = SubprocessReadPipeProtocol(self, 1)
                await loop.connect_read_pipe(subprocess_stdout_protocol, stdout)
                self._subprocess_stdout_protocol = subprocess_stdout_protocol
                stdout_transport = subprocess_stdout_protocol.transport
                if (stdout_transport is not None):
                    self.stdout = stdout_protocol = ReadProtocolBase(loop)
                    stdout_protocol.connection_made(stdout_transport)
                    self._alive_fds.append(1)
            
            stderr = process.stderr
            if (stderr is not None):
                subprocess_stderr_protocol = SubprocessReadPipeProtocol(self, 2)
                await loop.connect_read_pipe(subprocess_stderr_protocol, stderr)
                self._subprocess_stderr_protocol = subprocess_stderr_protocol
                stderr_transport = subprocess_stderr_protocol.transport
                if (stderr_transport is not None):
                    self.stderr = ReadProtocolBase(loop)
                    self.stderr.connection_made(stderr_transport)
                    self._alive_fds.append(2)
            
            for pending_call, args in self._pending_calls:
                pending_call(self, *args)
            
            self._pending_calls = None
        except:
            self.close()
            await self.wait()
            raise
        
        return self
    
    def __repr__(self):
        """Returns the async process's representation."""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        if self.closed:
            result.append(' closed')
            add_comma = True
        else:
            add_comma = False
        
        stdin = self.stdin
        if (stdin is not None):
            if add_comma:
                result.append(',')
            else:
                add_comma = True
            
            result.append(' stdin=')
            result.append(repr(stdin))
        
        stdout = self.stdout
        if (stdout is not None):
            if add_comma:
                result.append(',')
            else:
                add_comma = True
            
            result.append(' stdout=')
            result.append(repr(stdout))
        
        stderr = self.stderr
        if (stderr is not None):
            if add_comma:
                result.append(',')
            
            result.append(' stderr=')
            result.append(repr(stderr))
        
        result.append('>')
        
        return ''.join(result)
    
    def get_extra_info(self, name, default=None):
        """
        Gets optional transport information.
        
        Parameters
        ----------
        name : `str`
            The extra information's name to get.
        default : `Any`, Optional
            Default value to return if `name` could not be matched. Defaults to `None`.
        
        Returns
        -------
        info : `default`, `Any`
        """
        return self._extra.get(name, default)
    
    def is_closing(self):
        """
        Returns whether the async process is closing.
        
        Returns
        -------
        is_closing : `bool`
        """
        return self.closed
    
    def close(self):
        """
        Starts the shutdown process of the async process.
        """
        if self.closed:
            return
        
        self.closed = True
        
        pipe_stdin = self._subprocess_stdin_protocol
        if (pipe_stdin is not None):
            pipe_stdin.transport.close()
        
        pipe_stdout = self._subprocess_stdout_protocol
        if (pipe_stdout is not None):
            pipe_stdout.transport.close()
        
        pipe_stderr = self._subprocess_stderr_protocol
        if (pipe_stderr is not None):
            pipe_stderr.transport.close()
        
        process = self.process
        if (process is not None):
            if (self.return_code is None) and (process.poll() is None):
                try:
                    process.kill()
                except ProcessLookupError:
                    pass
        
        Task(self._process_exited(), self.loop)
    
    __del__ = close
    
    def send_signal(self, signal):
        """
        Sends the signal to the child process.
        
        Parameters
        ----------
        signal : `int`
            The signal to send.
        
        Raises
        ------
        ProcessLookupError
            The underlying process is already dead.
        """
        process = self.process
        if process is None:
            raise ProcessLookupError()
        
        process.send_signal(signal)
    
    def terminate(self):
        """
        Stops the child process.
        
        Raises
        ------
        ProcessLookupError
            The underlying process is already dead.
        """
        process = self.process
        if process is None:
            raise ProcessLookupError()
        
        process.terminate()
    
    async def kill(self):
        """
        Kills the child process.
        
        This method is a coroutine.
        
        Raises
        ------
        ProcessLookupError
            The underlying process is already dead.
        """
        process = self.process
        if process is None:
            raise ProcessLookupError()
        
        process.kill()
        
        self.close()
        
        loop = self.loop
        future = Future(loop)
        loop.call_later(0.0, Future.set_result_if_pending, future, None)
        await future
    
    def _pipe_connection_lost(self, fd, exception):
        """
        Called when a file descriptor of the subprocess lost connection.
        
        Calls ``._do_pipe_connection_lost`` or adds it as a callback if the process is still connecting.
        
        Parameters
        ----------
        fd : `int`
            File descriptor identifier.
            
            It's value can be any of the following:
            
            +-------------------+-------+
            | Respective name   | Value |
            +===================+=======+
            | stdin             | `0`   |
            +-------------------+-------+
            | stdout            | `1`   |
            +-------------------+-------+
            | stderr            | `2`   |
            +-------------------+-------+
        
        exception : `None` or `BaseException` instance
            Defines whether the connection is closed, or an exception was received.
            
            If the connection was closed, then `exception` is given as `None`. This can happen at the case, when eof is
            received as well.
        """
        pending_calls = self._pending_calls
        if (pending_calls is None):
            self._do_pipe_connection_lost(fd, exception)
        else:
            pending_calls.append((self.__class__._do_pipe_connection_lost, (fd, exception)))
        
        self._try_finish()
    
    def _do_pipe_connection_lost(self, fd, exception):
        """
        Called by ``._pipe_connection_lost`` to call the pipe's connection lost method.
        
        Parameters
        ----------
        fd : `int`
            File descriptor identifier.
            
            It's value can be any of the following:
            
            +-------------------+-------+
            | Respective name   | Value |
            +===================+=======+
            | stdin             | `0`   |
            +-------------------+-------+
            | stdout            | `1`   |
            +-------------------+-------+
            | stderr            | `2`   |
            +-------------------+-------+
        
        exception : `None` or `BaseException` instance
            Defines whether the connection is closed, or an exception was received.
            
            If the connection was closed, then `exception` is given as `None`. This can happen at the case, when eof is
            received as well.
        """
        if fd == 0:
            pipe = self.stdin
            if (pipe is not None):
                pipe.close()
            
            self._do_connection_lost(exception)
            return
        
        if fd == 1:
            reader = self.stdout
        elif fd == 2:
            reader = self.stderr
        else:
            reader = None
        
        if (reader is not None):
            reader.connection_lost(exception)
        
        try:
            self._alive_fds.remove(fd)
        except ValueError:
            pass
        
        self._maybe_process_exited()
    
    def _pipe_data_received(self, fd, data):
        """
        Called when one of the subprocess's pipe receives any data.
        
        Calls ``._do_pipe_data_received`` or adds it as a callback if the process is still connecting.
        
        Parameters
        ----------
        fd : `int`
            File descriptor identifier.
            
            It's value can be any of the following:
            
            +-------------------+-------+
            | Respective name   | Value |
            +===================+=======+
            | stdin             | `0`   |
            +-------------------+-------+
            | stdout            | `1`   |
            +-------------------+-------+
            | stderr            | `2`   |
            +-------------------+-------+
        
        data : `bytes`
            The received data.
        """
        pending_calls = self._pending_calls
        if (pending_calls is None):
            self._do_pipe_data_received(fd, data)
        else:
            pending_calls.append((self.__class__._do_pipe_data_received, (fd, data)))
    
    def _do_pipe_data_received(self, fd, data):
        """
        Called by ``._pipe_data_received`` to call the respective protocol' data received method.
        
        Parameters
        ----------
        fd : `int`
            File descriptor identifier.
            
            It's value can be any of the following:
            
            +-------------------+-------+
            | Respective name   | Value |
            +===================+=======+
            | stdin             | `0`   |
            +-------------------+-------+
            | stdout            | `1`   |
            +-------------------+-------+
            | stderr            | `2`   |
            +-------------------+-------+
        
        data : `bytes`
            The received data.
        """
        if fd == 1:
            reader = self.stdout
        elif fd == 2:
            reader = self.stderr
        else:
            return
        
        if (reader is not None):
            reader.data_received(data)
    
    async def _process_exited(self):
        """
        Task created by ``.close``to wait till the sub-process is closed and to set
        
        This method is a coroutine.
        """
        try:
            return_code = self.process.poll()
            if return_code is None:
                return_code = await self.loop.run_in_executor(self.process.wait)
            
            self.return_code = return_code
            
            self._try_finish()
            
            # wake up futures waiting for wait()
            exit_waiters = self._exit_waiters
            if (exit_waiters is not None):
                for waiter in self._exit_waiters:
                    if not waiter.cancelled():
                        waiter.set_result(return_code)
            
            self._exit_waiters = None
        finally:
            self.process = None
    
    def _maybe_process_exited(self):
        """
        Called when a sub-process pipe is closed. When all all pipe is closed, calls ``.close``.
        """
        if self._alive_fds:
            return
        
        self.close()
    
    async def wait(self, timeout=None):
        """
        Wait for child process to terminate.
        
        This method is a coroutine.
        
        Parameters
        ----------
        timeout : `None` or `float`
            The maximal amount of time to wait for teh process to close in seconds.

        Returns
        -------
        return_code : `int`
            The returncode of the subprocess.
        
        Raises
        ------
        TimeoutExpired
            If the process was not closed before timeout.
        """
        return_code = self.return_code
        if (return_code is not None):
            return return_code
        
        waiter = Future(self.loop)
        
        exit_waiters = self._exit_waiters
        if exit_waiters is None:
            self._exit_waiters = exit_waiters = set()
        
        exit_waiters.add(waiter)
        if (timeout is not None):
            future_or_timeout(waiter, timeout)
        
        try:
            return await waiter
        except TimeoutError:
            exit_waiters.discard(waiter)
            
            process = self.process
            if process is None:
                args = None
            else:
                args = process.args
            
            raise TimeoutExpired(args, timeout) from None
    
    def _try_finish(self):
        """
        If the sub-process finished closing, calls ``._do_connection_lost``. If the process is still connecting, adds
        it as a callback instead.
        """
        if self.return_code is None:
            return
        
        stdin_protocol = self._subprocess_stdin_protocol
        if (stdin_protocol is None) or stdin_protocol.disconnected:
            return
        
        stdout_protocol = self._subprocess_stdout_protocol
        if (stdout_protocol is None) or stdout_protocol.disconnected:
            return
        
        stderr_protocol = self._subprocess_stderr_protocol
        if (stderr_protocol is None) or stderr_protocol.disconnected:
            return
        
        pending_calls = self._pending_calls
        if (pending_calls is None):
            self._do_connection_lost(None)
        else:
            pending_calls.append((self.__class__._do_connection_lost, (self, None,)))
    
    async def _feed_stdin(self, input_):
        """
        Feeds the given data to ``.stdin``, waits till it drains and closes it.
        
        Used by ``.communicate``.
        
        This method is a coroutine.
        
        Parameters
        ----------
        input_ : `None` or `bytes-like`
            Optional data to be sent to the sub-process.
        """
        stdin = self.stdin
        if stdin is None:
            return
        
        if (input_ is not None):
            stdin.write(input_)
        
        try:
            await stdin.drain()
        except (BrokenPipeError, ConnectionResetError):
            # communicate() ignores BrokenPipeError and ConnectionResetError
            pass
        
        stdin.close()
    
    async def _read_close_stdout_stream(self):
        """
        Reads every data from ``.stdout``. When reading is done, closes it.
        
        Used by ``.communicate``.
        
        This method is a coroutine.
        
        Returns
        -------
        result :`None` or `bytes`
        """
        stream = self.stdout
        if stream is None:
            return None
        
        transport = self._subprocess_stdout_protocol.transport
        result = await stream.read()
        transport.close()
        return result
    
    async def _read_close_stderr_stream(self):
        """
        Reads every data from ``.stderr``. When reading is done, closes it.
        
        Used by ``.communicate``.
        
        This method is a coroutine.
        
        Returns
        -------
        result : `None` or `bytes`
        """
        stream = self.stderr
        if stream is None:
            return None
        
        transport = self._subprocess_stderr_protocol.transport
        result = await stream.read()
        transport.close()
        return result
    
    async def communicate(self, input_=None, timeout=None):
        """
        Sends data to stdin and reads data from stdout and stderr.
        
        Returns when the process is closed or raises when timeout occurs.
        
        This method is a coroutine.
        
        Parameters
        ----------
        input_ : `None` or `bytes-like`, Optional
            Optional data to be sent to the sub-process.
        timeout : `None` or `float`, Optional
            The maximal amount of time to wait for teh process to close in seconds.
        
        Returns
        -------
        stdout : `None` or `bytes`
            The read data from stdout.
        stderr : `None` or `bytes`
            The read data from stderr.
        
        Raises
        ------
        TimeoutExpired
            If the process was not closed before timeout.
        """
        tasks = []
        
        loop = self.loop
        if input_ is None:
            stdin_task = None
        else:
            stdin_task = Task(self._feed_stdin(input_), loop)
            tasks.append(stdin_task)
        
        if self.stdout is None:
            stdout_task = None
        else:
            stdout_task = Task(self._read_close_stdout_stream(), loop)
            tasks.append(stdout_task)
        
        if self.stderr is None:
            stderr_task = None
        else:
            stderr_task = Task(self._read_close_stderr_stream(), loop)
            tasks.append(stderr_task)
        
        if tasks:
            future = WaitTillAll(tasks, loop)
            if (timeout is not None):
                future_or_timeout(future, timeout)
            
            done, pending = await future
            
            if pending:
                # timeout occurred, cancel the read tasks and raise TimeoutExpired.
                for task in pending:
                    task.cancel()
                
                process = self.process
                if process is None:
                    args = None
                else:
                    args = process.args
                
                raise TimeoutExpired(args, timeout)
            
            if (stdin_task is not None):
                stdin_task.result()
            
            if (stdout_task is None):
                stdout = None
            else:
                stdout = stdout_task.result()
            
            if (stderr_task is None):
                stderr = None
            else:
                stderr = stderr_task.result()
        else:
            stdout = None
            stderr = None
        
        await self.wait()
        
        return stdout, stderr
    
    def poll(self):
        """
        Returns the subprocess's returncode if terminated.
        
        Returns
        -------
        return_code : `None` or `int`
        """
        return self.return_code
    
    def pause_writing(self):
        """
        Called when the write transport's buffer goes over the high-water mark.
        
        ``.pause_writing`` is called when the write buffer goes over the high-water mark, and eventually
        ``.resume_writing`` is called when the write buffer size reaches the low-water mark.
        """
        self._paused = True
    
    def resume_writing(self):
        """
        Called when the transport's write buffer drains below the low-water mark.
        
        See ``.pause_writing`` for details.
        """
        self._paused = False
        
        drain_waiter = self._drain_waiter
        if drain_waiter is None:
            return
        
        self._drain_waiter = None
        drain_waiter.set_result_if_pending(None)
    
    def _do_connection_lost(self, exception):
        """
        Sets ``._connection_lost`` as `True` and set ``._drain_waiter`` result or exception as well.
        
        Parameters
        ----------
        exception : `None` or `BaseException` instance
            Defines whether the connection is closed, or an exception was received.
            
            If the connection was closed, then `exception` is given as `None`. This can happen at the case, when eof is
            received as well.
        """
        self._connection_lost = True
        # Wake up the writer if currently paused.
        if not self._paused:
            return
        
        drain_waiter = self._drain_waiter
        if drain_waiter is None:
            return
        
        self._drain_waiter = None
        if exception is None:
            drain_waiter.set_result_if_pending(None)
        else:
            drain_waiter.set_exception_if_pending(exception)
    
    async def _drain_helper(self):
        """
        Called when the transport buffer after writing goes over the high limit mark to wait till it is drained.
        
        This method is a coroutine.
        """
        if self._connection_lost:
            raise ConnectionResetError('Connection lost')
        
        if not self._paused:
            return
        
        self._drain_waiter = drain_waiter = Future(self)
        await drain_waiter
