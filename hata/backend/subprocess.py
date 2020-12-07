# -*- coding: utf-8 -*-
import os, sys, errno
from stat import S_ISCHR, S_ISFIFO, S_ISSOCK
from subprocess import TimeoutExpired, PIPE, Popen
from socket import socketpair as create_socketpair

from .futures import Task, Future, WaitTillAll, future_or_timeout
from .protocol import ReadProtocolBase

IS_AIX = sys.platform.startswith('aix')
LIMIT = 1<<16
MAX_READ_SIZE = 262144

PROCESS_EXIT_DELAY_LIMIT = 10

class UnixReadPipeTransport(object):
    
    __slots__ = ('_extra', 'closing', 'fileno', 'loop', '_paused', 'pipe', 'protocol')
    async def __new__(cls, loop, pipe, protocol, extra=None):
        fileno = pipe.fileno()
        mode = os.fstat(fileno).st_mode
        if not (S_ISFIFO(mode) or S_ISSOCK(mode) or S_ISCHR(mode)):
            raise ValueError('Pipe transport is only for pipes, sockets and character devices.')
        
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
        return self._extra.get(name, default)
    
    def __repr__(self):
        return f'<{self.__class__.__name__} fd={self.fileno}>'
    
    def _read_ready(self):
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
        if self.closing or self._paused:
            return
        
        self._paused = True
        self.loop.remove_reader(self.fileno)
    
    def resume_reading(self):
        if self.closing or not self._paused:
            return
        
        self._paused = False
        self.loop.add_reader(self.fileno, self._read_ready)
    
    def set_protocol(self, protocol):
        self.protocol = protocol
    
    def get_protocol(self):
        return self.protocol
    
    def is_closing(self):
        return self.closing
    
    def close(self):
        if not self.closing:
            self._close(None)
    
    def __del__(self):
        pipe = self.pipe
        if (pipe is not None):
            pipe.close()
    
    def _fatal_error(self, exception, message='Fatal error on pipe transport'):
        if not (isinstance(exception, OSError) and (exception.errno == errno.EIO)):
            self.loop.render_exc_async(exception, [message, '\non: ', repr(self), '\n'])
        
        self._close(exception)
    
    def _close(self, exception):
        self.closing = True
        loop = self.loop
        loop.remove_reader(self.fileno)
        loop.call_soon(self.__class__._call_connection_lost, self, exception)
    
    def _call_connection_lost(self, exception):
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
    
    __slots__ = ('_buffer', '_connection_lost', '_extra', '_high_water', '_low_water', 'closing', 'fileno', 'loop',
        'pipe', 'protocol', 'protocol_paused')
    
    async def __new__(cls, loop, pipe, protocol, extra=None):
        fileno = pipe.fileno()
        mode = os.fstat(fileno).st_mode
        is_char = S_ISCHR(mode)
        is_fifo = S_ISFIFO(mode)
        is_socket = S_ISSOCK(mode)
        if not (is_char or is_fifo or is_socket):
            raise ValueError('Pipe transport is only for pipes, sockets and character devices.')
        
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
        self._connection_lost = 0
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
        return f'<{self.__class__.__name__} fd={self.fileno}>'
    
    def get_extra_info(self, name, default=None):
        return self._extra.get(name, default)
    
    def get_write_buffer_size(self):
        return len(self._buffer)
    
    def _read_ready(self):
        # Pipe was closed by peer.
        if self._buffer:
            exception = BrokenPipeError()
        else:
            exception = None
            
        self._close(exception)
    
    def write(self, data):
        if not data:
            return
        
        if isinstance(data, bytearray):
            data = memoryview(data)
        
        if self._connection_lost or self.closing:
            self._connection_lost += 1
            return
        
        buffer = self._buffer
        if not buffer:
            try:
                n = os.write(self.fileno, data)
            except (BlockingIOError, InterruptedError):
                n = 0
            except BaseException as err:
                self._connection_lost += 1
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
        buffer = self._buffer
        
        try:
            n = os.write(self.fileno, buffer)
        except (BlockingIOError, InterruptedError):
            pass
        except BaseException as err:
            buffer.clear()
            self._connection_lost += 1
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
        return True
    
    def write_eof(self):
        if self.closing:
            return
        
        self.closing = True
        if not self._buffer:
            loop = self.loop
            loop.remove_reader(self.fileno)
            loop.call_soon(self.__class__._call_connection_lost, self, None)
    
    def set_protocol(self, protocol):
        self.protocol = protocol
    
    def get_protocol(self):
        return self.protocol
    
    def is_closing(self):
        return self.closing
    
    def close(self):
        if (self.pipe is not None) and (not self.closing):
            self.write_eof()
    
    def __del__(self):
        pipe = self.pipe
        if (pipe is not None):
            pipe.close()
    
    def abort(self):
        self._close(None)
    
    def _fatal_error(self, exception, message='Fatal error on pipe transport'):
        if not isinstance(exception, OSError):
            self.loop.render_exc_async(exception, [message, '\non: ', repr(self), '\n'])
        
        self._close(exception)
    
    def _close(self, exception):
        self.closing = True
        
        loop = self.loop
        buffer = self._buffer
        if buffer:
            self.loop.remove_writer(self.fileno)
            buffer.clear()
        
        loop.remove_reader(self.fileno)
        loop.call_soon(self.__class__._call_connection_lost, self, exception)
    
    def _call_connection_lost(self, exception):
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
                repr(self), '._maybe_pause_protocol() failed\n'
                'On: ', repr(protocol), '.pause_writing()\n'])
    
    def _maybe_resume_protocol(self):
        if (self.protocol_paused and self.get_write_buffer_size() <= self._low_water):
            self.protocol_paused = False
            protocol = self.protocol
            if (protocol is not None):
                try:
                    protocol.resume_writing()
                except BaseException as err:
                    self.loop.render_exc_async(err, [
                        repr(self), '._maybe_resume_protocol() failed\n'
                        'on: ', repr(protocol), '.resume_writing()\n'])
    
    def get_write_buffer_limits(self):
        return self._low_water, self._high_water
    
    def _set_write_buffer_limits(self, low=None, high=None):
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
            raise ValueError(f'high ({high!r}) must be >= low ({low!r}) must be >= 0')
        
        self._high_water = high
        self._low_water = low
    
    def set_write_buffer_limits(self, low=None, high=None):
        self._set_write_buffer_limits(low=low, high=high)
        self._maybe_pause_protocol()

class SubprocessStreamWriter(object):
    __slots__ = ('loop', 'transport', 'protocol', )
    def __init__(self, loop, transport, protocol):
        self.transport = transport
        self.protocol = protocol
        self.loop = loop
    
    def write(self, data):
        self.transport.write(data)
    
    def writelines(self, data):
        self.transport.writelines(data)
    
    def write_eof(self):
        return self.transport.write_eof()
    
    def can_write_eof(self):
        return self.transport.can_write_eof()
    
    def close(self):
        return self.transport.close()
    
    def is_closing(self):
        return self.transport.is_closing()
    
    async def wait_closed(self):
        await self.protocol._get_close_waiter(self)
    
    def get_extra_info(self, name, default=None):
        return self.transport.get_extra_info(name, default)
    
    async def drain(self):
        if self.transport.is_closing():
            loop = self.loop
            future = Future(loop)
            loop.call_soon(Future.set_result_if_pending, future, None)
            await future
        
        await self.protocol._drain_helper()

class SubprocessWritePipeProtocol(object):
    __slots__ = ('disconnected', 'fd', 'transport', 'process', )
    
    def __init__(self, process, fd):
        self.process = process
        self.fd = fd
        self.transport = None
        self.disconnected = False
    
    def __call__(self):
        return self
    
    def connection_made(self, transport):
        self.transport = transport
    
    def __repr__(self):
        return f'<{self.__class__.__name__} fd={self.fd} pipe={self.transport!r}>'
    
    def connection_lost(self, exception):
        process = self.process
        if (process is not None):
            self.process = None
            process._pipe_connection_lost(self.fd, exception)
            self.disconnected = True
    
    def pause_writing(self):
        self.process._protocol.pause_writing()
    
    def resume_writing(self):
        self.process._protocol.resume_writing()

class SubprocessReadPipeProtocol(SubprocessWritePipeProtocol):
    __slots__ = ()
    def data_received(self, data):
        self.process._pipe_data_received(self.fd, data)
    
    def eof_received(self):
        # connection_lost is received anyways after eof, and connection_lost without exception will cause eof.
        pass

class AsyncProcess(object):
    __slots__ = ('_alive_fds', '_connection_lost', '_drain_waiter', '_exit_waiters', '_extra', '_finished', '_paused',
    '_pending_calls', '_stdin_closed', '_subprocess_stderr_protocol', '_subprocess_stdin_protocol',
    '_subprocess_stdout_protocol', 'closed', 'loop', 'pid', 'process', 'returncode', 'stderr', 'stdin', 'stdout', )
    
    async def __new__(cls, loop, args, shell, stdin, stdout, stderr, bufsize, extra, popen_kwargs):
        if stdin == PIPE:
            # Use a socket pair for stdin, since not all platforms support selecting read events on the write end of a
            # socket (which we use in order to detect closing of the other end).  Notably this is needed on AIX, and
            # works just fine on other platforms.
            stdin_r, stdin_w = create_socketpair()
        else:
            stdin_r = stdin
            stdin_w = None
        
        process = None
        
        try:
            process = Popen(args, shell=shell, stdin=stdin_r, stdout=stdout, stderr=stderr, universal_newlines=False,
                bufsize=bufsize, **popen_kwargs)
            
            if (stdin_w is not None):
                stdin_r.close()
                process.stdin = open(stdin_w.detach(), 'wb', buffering=bufsize)
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
        self.pid = process.pid
        self.returncode = None
        self._exit_waiters = None
        self._pending_calls = []
        self._subprocess_stdin_protocol = None
        self._subprocess_stdout_protocol = None
        self._subprocess_stderr_protocol = None
        self._finished = False
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self._paused = False
        self._drain_waiter = None
        self._connection_lost = False
        self._alive_fds = []
        self._stdin_closed = Future(loop)
        
        try:
            stdin = process.stdin
            if (stdin is not None):
                subprocess_stdin_protocol = SubprocessWritePipeProtocol(self, 0)
                await loop.connect_write_pipe(subprocess_stdin_protocol, stdin)
                self._subprocess_stdin_protocol = subprocess_stdin_protocol
                stdin_transport = subprocess_stdin_protocol.transport
                if (stdin_transport is not None):
                    self.stdin = SubprocessStreamWriter(loop, stdin_transport, protocol=self)
            
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
        return self._extra.get(name, default)
    
    def is_closing(self):
        return self.closed
    
    def close(self):
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
            if (self.returncode is None) and (process.poll() is None):
                try:
                    process.kill()
                except ProcessLookupError:
                    pass
        
        self.loop.call_soon(self.__class__._process_exited, self, 0)
    
    __del__ = close
    
    def send_signal(self, signal):
        process = self.process
        if process is None:
            raise ProcessLookupError()
        
        process.send_signal(signal)
    
    def terminate(self):
        process = self.process
        if process is None:
            raise ProcessLookupError()
        
        process.terminate()
    
    async def kill(self):
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
        pending_calls = self._pending_calls
        if (pending_calls is None):
            self._do_pipe_connection_lost(fd, exception)
        else:
            pending_calls.append((self.__class__._do_pipe_connection_lost, (fd, exception)))
        
        self._try_finish()
    
    def _do_pipe_connection_lost(self, fd, exception):
        if fd == 0:
            pipe = self.stdin
            if pipe is not None:
                pipe.close()
            self._do_connection_lost(exception)
            stdin_closed = self._stdin_closed
            if exception is None:
                stdin_closed.set_result_if_pending(None)
            else:
                stdin_closed.set_exception_if_pending(exception)
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
        pending_calls = self._pending_calls
        if (pending_calls is None):
            self._do_pipe_data_received(fd, data)
        else:
            pending_calls.append((self.__class__._do_pipe_data_received, (fd, data)))
    
    def _do_pipe_data_received(self, fd, data):
        if fd == 1:
            reader = self.stdout
        elif fd == 2:
            reader = self.stderr
        else:
            return
        
        if (reader is not None):
            reader.data_received(data)
    
    def _process_exited(self, delayed):
        returncode = self.process.poll()
        if returncode is None:
            if delayed == PROCESS_EXIT_DELAY_LIMIT:
                # do not wait more
                returncode = 255
            else:
                # not yet exited, delay a little bit.
                delayed += 1
                
                self.loop.call_later(0.01*delayed, self.__class__._process_exited, self, delayed)
                return
        
        self.returncode = returncode
        
        pending_calls = self._pending_calls
        if (pending_calls is None):
            self._maybe_process_exited()
        else:
            pending_calls.append((self.__class__._maybe_process_exited, ()))
        
        self._try_finish()
        
        # wake up futures waiting for wait()
        exit_waiters = self._exit_waiters
        if (exit_waiters is not None):
            for waiter in self._exit_waiters:
                if not waiter.cancelled():
                    waiter.set_result(returncode)
        
        self._exit_waiters = None
    
    def _maybe_process_exited(self):
        if self._alive_fds:
            return
        
        self.close()
    
    async def wait(self, timeout=None):
        returncode = self.returncode
        if (returncode is not None):
            return returncode
        
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
            try:
                exit_waiters.remove(waiter)
            except ValueError:
                pass
            
            process = self.process
            if process is None:
                args = None
            else:
                args = process.args
            
            raise TimeoutExpired(args, timeout) from None
    
    def _try_finish(self):
        if self.returncode is None:
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
        
        self._finished = True
        
        pending_calls = self._pending_calls
        if (pending_calls is None):
            self._call_connection_lost(None)
        else:
            pending_calls.append((self.__class__._call_connection_lost, (self, None,)))
    
    def _call_connection_lost(self, exception):
        try:
            self._do_connection_lost(exception)
        finally:
            self.process = None
    
    # Used by .communicate
    async def _feed_stdin(self, input_):
        stdin = self.stdin
        if stdin is None:
            return
        
        stdin.write(input_)
        
        try:
            await stdin.drain()
        except (BrokenPipeError, ConnectionResetError):
            # communicate() ignores BrokenPipeError and ConnectionResetError
            pass
        
        stdin.close()
    
    # Used by .communicate
    async def _read_close_stdout_stream(self):
        stream = self.stdout
        if stream is None:
            return b''
        
        transport = self._subprocess_stdout_protocol.transport
        result = await stream.read()
        transport.close()
        return result
    
    # Used by .communicate
    async def _read_close_stderr_stream(self):
        stream = self.stderr
        if stream is None:
            return b''
        
        transport = self._subprocess_stderr_protocol.transport
        result = await stream.read()
        transport.close()
        return result
    
    async def communicate(self, input_=None, timeout=None):
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
            
            _, pending = await future
            
            if pending:
                # timeout occured, cancel the read tasks and raise TimeoutExpired.
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
        returncode = self.returncode
        if (returncode is not None):
            return returncode
    
    def pause_writing(self):
        self._paused = True
    
    def resume_writing(self):
        self._paused = False
        
        drain_waiter = self._drain_waiter
        if drain_waiter is None:
            return
        
        self._drain_waiter = None
        drain_waiter.set_result_if_pending(None)
    
    def _do_connection_lost(self, exception):
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
        if self._connection_lost:
            raise ConnectionResetError('Connection lost')
        
        if not self._paused:
            return
        
        self._drain_waiter = drain_waiter = Future(self)
        await drain_waiter
