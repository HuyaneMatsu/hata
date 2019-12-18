from .py_exceptions import PayloadError
from .py_parsers import HttpResponseParser
from .py_streams import EMPTY_PAYLOAD,DataQueue
from .futures import Future

class Disconnected(Exception):
    pass

class BaseProtocol(object):
    #slot config on inheriting
    #__slots__=('_connection_lost', 'drain_waiter', 'loop', 'paused', 'transport')
    #should be empty
    __slots__=()
    def __init__(self,loop):
        self.loop               = loop
        self.paused             = False
        self.drain_waiter       = None
        self._connection_lost   = False
        self.transport          = None

    def pause_writing(self):
        self.paused=True

    def resume_writing(self):
        self.paused=False

        waiter=self.drain_waiter
        if waiter is None:
            return
        self.drain_waiter=None
        if not waiter.done():
            waiter.set_result(None)

    def connection_made(self,transport):
        self.transport=transport

    def connection_lost(self,exception):
        self._connection_lost=True
        # Wake up the writer if currently paused.
        self.transport=None
        if not self.paused:
            return
        waiter=self.drain_waiter
        if waiter is None:
            return
        self.drain_waiter=None
        if waiter.done():
            return
        if exception is None:
            waiter.set_result(None)
        else:
            waiter.set_exception(exception)

    async def _drain_helper(self):
        if self._connection_lost:
            raise ConnectionResetError('Connection lost')
        if not self.paused:
            return
        waiter=Future(self.loop)
        self.drain_waiter=waiter
        await waiter

    def __call__(self):
        return self

class ResponseHandler(BaseProtocol,DataQueue):
    __slots__=('_connection_lost', '_should_close', 'buffer', 'drain_waiter',
        'eof', 'exception', 'loop', 'parser', 'paused', 'payload',
        'payload_parser', 'reading_paused', 'read_timeout',
        'read_timeout_handle', 'size', 'skip_payload', 'tail', 'timer',
        'transport', 'upgraded', 'waiter')
    #Helper class to adapt between Protocol and StreamReader.

    def __init__(self,loop):
        BaseProtocol.__init__(self,loop)
        DataQueue.__init__(self,loop)

        self._should_close      = False
        self.payload            = None
        self.skip_payload       = False
        self.payload_parser     = None
        self.reading_paused     = False

        self.timer              = None
        self.tail               = b''
        self.upgraded           = False
        self.parser             = None

        self.read_timeout       = None
        self.read_timeout_handle= None


    @property
    def should_close(self):
        if (self.payload is not None and not self.payload.is_eof() or self.upgraded):
            return True
        
        return (self._should_close or self.upgraded or
                self.exception is not None or
                self.payload_parser is not None or
                len(self) or self.tail)

    def force_close(self):
        self._should_close=True

    def close(self):
        transport=self.transport
        if transport is not None:
            transport.close()
            self.transport=None
            self.payload=None
            self.drop_timeout()

    def is_connected(self):
        return (self.transport is not None)
            
    def connection_lost(self,exception):
        self.drop_timeout()

        if self.payload_parser is not None:
            #with suppress(Exception):
            self.payload_parser.feed_eof()

        try:
            uncompleted=self.parser.feed_eof()
        except Exception:
            uncompleted=None
            payload=self.payload
            if payload is not None:
                payload.set_exception(PayloadError('Response payload is not completed'))

        if not self.is_eof():
            if exception is None:
                exception=ConnectionError(uncompleted)
            # assigns self._should_close to True as side effect,
            # we do it anyway below
            self.exception=exception

        self._should_close      = True
        self.parser             = None
        self.payload            = None
        self.payload_parser     = None
        self.reading_paused     = False

        BaseProtocol.connection_lost(self,exception)

    def eof_received(self):
        #should call parser.feed_eof() most likely
        self.drop_timeout()

    def pause_reading(self):
        if self.reading_paused:
            return
        try:
            self.transport.pause_reading()
        except RuntimeError:
            pass
        self.reading_paused = True
        self.drop_timeout()

    def resume_reading(self):
        if self.reading_paused:
            pass
        try:
            self.transport.resume_reading()
        except RuntimeError:
            pass
        self.reading_paused=False
        self.reschedule_timeout()

    def set_exception(self,exception):
        self._should_close=True
        self.drop_timeout()
        DataQueue.set_exception(self,exception)

    def set_parser(self,parser,payload):
        self.payload        = payload
        self.payload_parser = parser

        self.drop_timeout()

        if self.tail:
            data=self.tail
            self.tail=b''
            self.data_received(data)

    def set_response_params(self,timer=None,skip_payload=False,read_until_eof=False,auto_decompress=True,read_timeout=None):
        self.skip_payload   = skip_payload
        self.read_timeout   = read_timeout
        
        self.reschedule_timeout()

        self.parser=HttpResponseParser(
            self, self.loop, timer=timer,
            payload_error=PayloadError,
            read_until_eof=read_until_eof,
            auto_decompress=auto_decompress)

        if self.tail:
            data=self.tail
            self.tail=b''
            self.data_received(data)

    def drop_timeout(self):
        if self.read_timeout_handle is not None:
            self.read_timeout_handle.cancel()
            self.read_timeout_handle=None

    def reschedule_timeout(self):
        timeout=self.read_timeout
        if self.read_timeout_handle:
            self.read_timeout_handle.cancel()

        if timeout:
            self.read_timeout_handle=self.loop.call_later(timeout,self._on_read_timeout)
        else:
            self.read_timeout_handle=None

    def _on_read_timeout(self):
        exception=TimeoutError('Timeout on reading data from socket')
        self.set_exception(exception)
        if self.payload is not None:
            self.payload.set_exception(exception)

    def data_received(self,data):
        if not data:
            return

        # custom payload parser
        if self.payload_parser is not None:
            eof,tail=self.payload_parser.feed_data(data)
            if eof:
                self.payload=None
                self.payload_parser=None

                if tail:
                    self.data_received(tail)

            return
        if self.upgraded or self.parser is None:
            # i.e. websocket connection, websocket parser is not set yet
            self.tail+=data
            return

        # parse http messages
        try:
            messages,upgraded,tail=self.parser.feed_data(data)
        except (AttributeError,NameError) as err:
            if self.transport is not None:
                self.transport.close()
            self.set_exception(err)
            raise #for testing
        except BaseException as err:
            if self.transport is not None:
                # connection.release() could be called BEFORE
                # data_received(), the transport is already
                # closed in this case
                self.transport.close()
            # should_close is True after the call
            self.set_exception(err)
            return

        self.upgraded=upgraded

        payload=None
        for message,payload in messages:
            if message.should_close:
                self._should_close=True

            self.payload=payload

            if self.skip_payload or message.code in (204,304):
                self.feed_data((message,EMPTY_PAYLOAD),0)
            else:
                self.feed_data((message,payload),0)
        if payload is not None:
            # new message(s) was processed
            # register timeout handler unsubscribing
            # either on end-of-stream or immediatelly for
            # EMPTY_PAYLOAD
            if payload is EMPTY_PAYLOAD:
                self.drop_timeout()
            else:
                payload.on_eof(self.drop_timeout)
                
        if tail:
            if upgraded:
                self.data_received(tail)
            else:
                self.tail=tail
