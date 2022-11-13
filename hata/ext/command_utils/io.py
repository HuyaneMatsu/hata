__all__ = ('get_channel_stdin', 'get_channel_stdout',)

import reprlib
from collections import deque
from datetime import datetime, timedelta

from scarletio import CancelledError, Future, LOOP_TIME, Task, future_or_timeout, shield, sleep

from ...discord.core import KOKORO
from ...discord.utils import sanitize_content


MESSAGE_EDIT_TIMEDELTA = timedelta(seconds=10)
REQUEST_RATE_LIMIT = 1.2


class ChannelOutputStream:
    """
    Attributes
    ----------
    _channel : ``Channel``
        The target channel of the stream.
    _chunk_size : `int`
        The maximal chunk size to send in one message.
    _client : ``Client``
        The client who send the stream to the channel.
    _close_waiter : `None`, ``Future``
        Waiter future set to wait for closing.
    _closed : `bool`
        Whether the stream is closed.
    _chunks : `str`
        The data queue.
    _last_chunk : `None`, `str`
        The last send raw chunk.
    _last_message : `None`, ``Message``
        The last sent message.
    _sanitize : `bool`
        Whether the output stream should be sanitized.
    _transfer_task : `None`, ``Task``
        Transfer task set meanwhile data is transferred to ``._channel``.
    """
    __slots__ = (
        '_channel', '_chunk_size', '_client', '_close_waiter', '_closed', '_chunks', '_last_chunk', '_last_message',
        '_sanitize', '_transfer_task'
    )
    
    def __init__(self, client, channel, chunk_size, sanitize):
        """
        Creates a new ``ChannelOutputStream`` with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The client who send the stream to the channel.
        channel : ``Channel``
            The target channel of the stream.
        chunk_size : `int`
            The maximal chunk size to send in one message.
        sanitize : `bool`
            Whether the output stream should be sanitized.
        """
        self._client = client
        self._channel = channel
        self._chunks = deque()
        self._transfer_task = None
        self._chunk_size = chunk_size
        self._sanitize = sanitize
        self._last_message = None
        self._last_chunk = None
        self._closed = False
        self._close_waiter = None
    
    def write(self, data):
        """
        Writes the given data to the buffer.
        
        Parameters
        ----------
        data : `str`
            The data to write.
        
        Raises
        ------
        TypeError
            Only string can be written to the output stream.
        ValueError
            I/O operation on closed or on a detached file.
        """
        if self._closed:
            raise ValueError('I/O operation on closed or on a detached file.')
        
        if not isinstance(data, str):
            raise TypeError(
                f'Only `str` can be written into `{self.__class__.__name__}`, got '
                f'{data.__class__.__name__}; {reprlib.repr(data)}.'
            )
        
        if not data:
            return
        
        self._chunks.append(data)
        
        transfer_task = self._transfer_task
        if (transfer_task is None):
            self._transfer_task = Task(self._do_transfer(), KOKORO)
    
    
    async def flush(self):
        """
        Force the text in the buffer into the raw stream.
        
        After flushing the newly written content will be forced to new message as well.
        
        This method is a coroutine.
        
        Raises
        ------
        BlockingIOError
            If the raw stream blocks.
        ValueError
            I/O operation on closed or on a detached file.
        """
        transfer_task = self._transfer_task
        if (transfer_task is not None):
            await transfer_task
        
        self._last_message = None
        self._last_chunk = None
    
    
    async def _do_transfer(self):
        """
        Sends the data written to the stream to the respective channel.
        
        This method is a coroutine.
        """
        try:
            client = self._client
            while True:
                try:
                    message = self._last_message
                    if (message is None):
                        un_poll = None
                        should_edit = False
                    else:
                        last_action = message.edited_at
                        if last_action is None:
                            last_action = message.created_at
                        
                        if (last_action + MESSAGE_EDIT_TIMEDELTA > datetime.utcnow()):
                            un_poll = self._last_chunk
                            should_edit = True
                        else:
                            un_poll = None
                            should_edit = False
                    
                    raw_data = self._poll(un_poll)
                    if raw_data is None:
                        break
                    
                    if len(raw_data) < (self._chunk_size >> 1):
                        maybe_update_next = True
                    else:
                        maybe_update_next = False
                    
                    if self._sanitize:
                        data = sanitize_content(raw_data, guild=self._channel.guild)
                    else:
                        data = raw_data
                    
                    request_start = LOOP_TIME()
                    if should_edit:
                        await client.message_edit(message, data)
                    else:
                        message = await client.message_create(self._channel, data)
                    
                    if maybe_update_next:
                        self._last_message = message
                        self._last_chunk = raw_data
                    else:
                        self._last_message = None
                        self._last_chunk = None
                    
                    sleep_time = request_start - LOOP_TIME() + REQUEST_RATE_LIMIT
                    
                    if sleep_time > 0.0:
                        await sleep(sleep_time, KOKORO)
                
                except BaseException as err:
                    self._last_message = None
                    self._last_chunk = None
                    await client.events.error(client, f'{self!r}._do_transfer', err)
        finally:
            self._transfer_task = None
    
    
    def _poll(self, un_poll):
        """
        Polls a chunk of data from the stream.
        
        Parameters
        ----------
        un_poll : `None`, `str`
            Data to un-poll.
        
        Returns
        -------
        data : `None`, `str`
            The data to send if any.
        """
        chunks = self._chunks
        
        if not chunks:
            return None
        
        data_parts = []
        data_parts_size = self._chunk_size
        
        if (un_poll is not None):
            chunks.appendleft(un_poll)
        
        while chunks:
            part = chunks[0]
            data_parts_size -= len(part)
            if data_parts_size > 0:
                data_parts.append(part)
                del chunks[0]
                continue
            
            if data_parts_size == 0:
                data_parts.append(part)
                del chunks[0]
                break
            
            data_parts.append(part[:data_parts_size])
            chunks[0] = part[data_parts_size:]
            break
        
        if data_parts:
            return ''.join(data_parts)
    
    
    def __repr__(self):
        """Returns the stream's representation."""
        repr_parts = [
            '<', self.__class__.__name__, ' client = ', repr(self._client), ', channel = ', repr(self._channel)
        ]
        
        chunks_size = 0
        for data in self._chunks:
            chunks_size += len(data)
        
        if chunks_size:
            repr_parts.append(' size = ')
            repr_parts.append(repr(chunks_size))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    def close(self):
        """
        Closes the output.
        """
        if self._closed:
            return
        
        self._closed = True
        
        close_waiter = self._close_waiter
        if (close_waiter is not None):
            close_waiter.set_result_if_pending(None)
    
    async def wait_for_close(self, timeout = None):
        """
        Waits till the stream is closed.
        
        Parameters
        ----------
        timeout : `None`, `float` = `None`, Optional
            Maximal timeout to wait.
        
        Raises
        ------
        TimeoutError
            Timeout occurred.
        """
        if self._closed:
            return
        
        close_waiter = self._close_waiter
        if (close_waiter is None):
            close_waiter = self._close_waiter = Future(KOKORO)
        
        waiter = shield(close_waiter, KOKORO)
        
        if (timeout is not None):
            future_or_timeout(waiter, timeout)
        
        return waiter
    
    def __enter__(self):
        """Enters the stream returning itself."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exists the stream by closing it."""
        self.close()
        return False

class ChannelInputStream:
    """
    Attributes
    ----------
    _channel : ``Channel``
        The source channel of the stream.
    _check : `None`, `callable`
        Optional check to call to check whether a received message should be passed to the stream.
        
        Should accept the following parameters:
        
        +-----------+---------------+
        | Name      | Type          |
        +===========+===============+
        | message   | ``Message``   |
        +-----------+---------------+
        
        Should return the following values:
        
        +-------------------+---------------+
        | Name              | Type          |
        +===================+===============+
        | should_redirect   | `bool`        |
        +-------------------+---------------+
    
    _client : ``Client``
        The client who send the stream to the channel.
    _close_waiter : `None`, ``Future``
        Waiter future set to wait for closing.
    _closed : `bool`
        Whether the stream is closed.
    _chunks : `str`
        The data queue.
    _payload_reader : `None`, `GeneratorType`
        Payload reader generator, what gets the control back, when data, eof or any exception is received.
    _payload_waiter : `None` of ``Future``
        Payload waiter of the protocol, what's result is set, when the ``._payload_reader`` generator returns.
        
        If cancelled or marked by done or any other methods, the payload reader will not be cancelled.
    """
    __slots__ = (
        '_channel', '_check', '_client', '_close_waiter', '_closed', '_chunks', '_payload_reader', '_payload_waiter'
    )
    
    def __init__(self, client, channel, check):
        """
        Creates a new ``ChannelInputStream`` with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The client who send the stream to the channel.
        channel : ``Channel``
            The target channel of the stream.
        check : `None`, `callable`
            Optional check to call to check whether a received message should be passed to the stream.
        """
        self._client = client
        self._channel = channel
        self._chunks = deque()
        self._check = check
        self._closed = False
        self._close_waiter = None
        self._payload_reader = None
        self._payload_waiter = None
        
        client.events.message_create.append(channel, self)
    
    
    async def __call__(self, client, message):
        """
        Feeds a message to the input.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            the received message.
        """
        check = self._check
        if (check is not None):
            should_redirect = check(message)
            if (not isinstance(should_redirect, int)) or (not should_redirect):
                return
        
        data = message.content
        if not data:
            return
        
        
        chunks = self._chunks
        for data in (data, '\n'):
            payload_reader = self._payload_reader
            if payload_reader is None:
                chunks.append(data)
                continue
            
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
                
                payload_waiter = self._payload_waiter
                self._payload_reader = None
                self._payload_waiter = None
                payload_waiter.set_result_if_pending(result)
            except GeneratorExit as err:
                payload_waiter = self._payload_waiter
                self._payload_reader = None
                self._payload_waiter = None
                exception = CancelledError()
                exception.__cause__ = err
                payload_waiter.set_exception_if_pending(exception)
            except BaseException as err:
                payload_waiter = self._payload_waiter
                self._payload_reader = None
                self._payload_waiter = None
                payload_waiter.set_exception_if_pending(err)
    
    def close(self):
        """
        Closes the input.
        """
        if self._closed:
            return
        
        self._closed = True
        self._client.events.message_create.remove(self._channel, self)
    
        close_waiter = self._close_waiter
        if (close_waiter is not None):
            close_waiter.set_result_if_pending(None)
    
        payload_reader = self._payload_reader
        if payload_reader is None:
            return False
        
        try:
             payload_reader.throw(CancelledError())
        except CancelledError as err:
            new_exception = ConnectionError('Connection closed unexpectedly with EOF.')
            new_exception.__cause__ = err
            payload_waiter = self._payload_waiter
            self._payload_reader = None
            self._payload_waiter = None
            payload_waiter.set_exception_if_pending(new_exception)
        
        except StopIteration as err:
            args = err.args
            if not args:
                result = None
            elif len(args) == 1:
                result = args[0]
            else:
                result = args
            
            payload_waiter = self._payload_waiter
            self._payload_reader = None
            self._payload_waiter = None
            payload_waiter.set_result_if_pending(result)
        except GeneratorExit as err:
            payload_waiter = self._payload_waiter
            self._payload_reader = None
            self._payload_waiter = None
            exception = CancelledError()
            exception.__cause__ = err
            payload_waiter.set_exception_if_pending(exception)
        except BaseException as err:
            payload_waiter = self._payload_waiter
            self._payload_reader = None
            self._payload_waiter = None
            payload_waiter.set_exception_if_pending(err)
    
    
    async def wait_for_close(self, timeout = None):
        """
        Waits till the stream is closed.
        
        Parameters
        ----------
        timeout : `None`, `float` = `None`, Optional
            Maximal timeout to wait.
        
        Raises
        ------
        TimeoutError
            Timeout occurred.
        """
        if self._closed:
            return
        
        close_waiter = self._close_waiter
        if (close_waiter is None):
            close_waiter = self._close_waiter = Future(KOKORO)
        
        waiter = shield(close_waiter, KOKORO)
        
        if (timeout is not None):
            future_or_timeout(waiter, timeout)
        
        return waiter
    
    
    def _set_payload_reader(self, payload_reader):
        """
        Sets payload reader to the stream.
        
        Parameters
        ----------
        payload_reader : `GeneratorType`
            A generator, what gets control, every time a chunk is received, till it returns or raises.
        
        Returns
        -------
        payload_waiter : ``Future``
            Waiter, to what the result of the `payload_reader` is set.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        assert self._payload_reader is None, 'Payload reader already set!'
        
        if self._closed and (not self._chunks):
            raise ValueError('I/O operation on closed or on a detached file.')
        
        payload_waiter = Future(KOKORO)
        
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
            self._payload_waiter = payload_waiter
            self._payload_reader = payload_reader
        
        return payload_waiter
    
    
    def _read_all(self):
        """
        Reads all the data from the stream.
        
        This method is a generator.
        
        Returns
        -------
        data : `str`
            The read data.
        """
        chunks = []
        self_chunks = self._chunks
        chunks.extend(self_chunks)
        self_chunks.clear()
        
        while True:
            try:
                chunk = yield
            except CancelledError:
                break
            else:
                chunks.append(chunk)
        
        return ''.join(chunks)
    
    
    def _read_exactly(self, size):
        """
        Reads the exact amount of data form the stream.
        
        This method is a generator.
        
        Returns
        -------
        data : `str`
            The read data.
        """
        if size == 0:
            return b''
        
        chunks = []
        self_chunks = self._chunks
        
        while self_chunks:
            chunk = self_chunks[0]
            chunk_length = len(chunk)
            size -= chunk_length
            if size > 0:
                del self_chunks[0]
                chunks.append(chunk)
                continue
            
            if size == 0:
                del self_chunks[0]
                chunks.append(chunk)
                break
            
            self_chunks[0] = chunk[-size:]
            chunks.append(chunk[:-size])
            break
        
        if (size > 0) and (not self._closed):
            while True:
                try:
                    chunk = yield
                except CancelledError:
                    break
                else:
                    chunk_length = len(chunk)
                    size -= chunk_length
                    if size > 0:
                        chunks.append(chunk)
                        continue
                    
                    if size == 0:
                        chunks.append(chunk)
                        break
                    
                    self_chunks.appendleft(chunk[-size:])
                    chunks.append(chunk[:-size])
                    break
        
        return ''.join(chunks)
    
    
    def _read_line(self):
        """
        Reads a line from the stream.
        
        This method is a generator
        
        Returns
        -------
        data : `str`
            The read data.
        """
        chunks = []
        self_chunks = self._chunks
        
        while self_chunks:
            chunk = self_chunks[0]
            index = chunk.find('\n')
            if index == -1:
                del self_chunks[0]
                chunks.append(chunk)
                continue
            
            index += 1
            if index == len(chunk):
                del self_chunks[0]
                chunks.append(chunk)
                line_break_found = True
                break
            
            self_chunks[0] = chunk[index:]
            chunks.append(chunk[:index])
            line_break_found = True
            break
        else:
            line_break_found = False
        
        if (not line_break_found) and (not self._closed):
            while True:
                try:
                    chunk = yield
                except CancelledError:
                    break
                else:
                    index = chunk.find('\n')
                    if index == -1:
                        chunks.append(chunk)
                        continue
                    
                    index += 1
                    if index == len(chunk):
                        chunks.append(chunk)
                        break
                    
                    self_chunks.appendleft(chunk[index:])
                    chunks.append(chunk[:index])
                    break
        
        return ''.join(chunks)
    
    
    def _read_lines(self, limit):
        """
        Reads a line from the stream.
        
        This method is a generator
        
        Parameters
        ----------
        limit : `int`
            The upper limit if lines to read.
            
            If given as negative `int`, then all the data till eof is read from the stream.
        
        Returns
        -------
        lines : `list` of `str`
            The read lines.
        """
        lines = []
        
        while limit:
            line = yield from self._read_line()
            if not line:
                break
            
            lines.append(line)
            limit -= 1
            continue
        
        return lines
    
    
    async def read(self, size=-1):
        """
        Reads from the underlying stream.
        
        This method is a coroutine.
        
        Parameters
        ----------
        size : `int` = `-1`. Optional
            The upper limit to read from the underlying stream. If eof is received meanwhile reading, the already read
            data is returned.
            
            If given as negative `int`, then all the data till eof is read.
        
        Returns
        -------
        data : `str`
            The read data.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        return await self._set_payload_reader(self._read_all() if size<0 else self._read_exactly(size))
    
    
    async def read_line(self):
        """
        Reads a line from the underlying stream.
        
        This method is a coroutine.
        
        Returns
        -------
        data : `str`
            The read data.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        return await self._set_payload_reader(self._read_line())
    
    readline = read_line

    async def read_lines(self, hint=-1):
        """
        Read and return a list of lines from the stream.
        
        This method is a coroutine.
        
        Parameters
        ----------
        hint : `int` = `-1`, Optional
            The upper limit if lines to read.
            
            If given as negative `int`, then all the data till eof is read from the stream.
        
        Returns
        -------
        lines : `list` of (`bytes`, `str`)
            The red lines.
        
        Raises
        ------
        ValueError
            I/O operation on closed or on a detached file.
        """
        return await self._set_payload_reader(self._read_lines(hint))
    
    readlines = read_lines
    
    def __enter__(self):
        """Enters the stream returning itself."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exists the stream by closing it."""
        self.close()
        return False


def get_channel_stdout(client, channel, *, chunk_size=1000, sanitize=False):
    """
    Gets output stream towards the given channel.
    
    Parameters
    ----------
    client : ``Client``
        The client who redirects the stream.
    channel : ``Channel``
        The channel where the stream is redirected from.
    chunk_size : `int` = `1000`, Optional (Keyword only)
        The maximal size of a raw chunk to output.
    sanitize : `bool` = `False`, Optional (Keyword only)
        Whether the output stream should be sanitized.
        
        > Sanitization is only applied after an output chunk is cut to size, so it is recommended to not set
        > `chunk_size` over `1000` if `sanitize` is given as `True`.
    
    Returns
    -------
    output_stream : ``ChannelOutputStream``
    """
    return ChannelOutputStream(client, channel, chunk_size, sanitize)


def get_channel_stdin(client, channel, *, check = None):
    """
    Gets an input stream from the given channel.
    
    Parameters
    ----------
    client : ``Client``
        The client who redirects the stream.
    channel : ``Channel``
        The channel from where the stream will be redirected form.
    check : `None`, `callable` = `None`, Optional (Keyword only)
        Check which message's content should be feed to the input. Defaults to `None`.
        
        Should accept the following parameters:
        
        +-----------+---------------+
        | Name      | Type          |
        +===========+===============+
        | message   | ``Message``   |
        +-----------+---------------+
        
        Should return the following values:
        
        +-------------------+---------------+
        | Name              | Type          |
        +===================+===============+
        | should_redirect   | ``bool``      |
        +-------------------+---------------+
    
    Returns
    -------
    input_stream : ``ChannelInputStream``
    """
    return ChannelInputStream(client, channel, check)
