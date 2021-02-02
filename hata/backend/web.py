# -*- coding: utf-8 -*-
# Experimenting with web servers, nothing worthy
# WORK IN PROGRESS
import functools, http, re
from uuid import UUID

from .utils import imultidict
from .futures import WaitTillAll, Future, Task, CancelledError
from .protocol import ProtocolBase
from .exceptions import PayloadError
from .helpers import HttpVersion11

INTERNAL_SERVER_ERROR      = http.HTTPStatus.INTERNAL_SERVER_ERROR
BAD_REQUEST                = http.HTTPStatus.BAD_REQUEST
HTTP_VERSION_NOT_SUPPORTED = http.HTTPStatus.HTTP_VERSION_NOT_SUPPORTED
METHOD_NOT_ALLOWED         = http.HTTPStatus.METHOD_NOT_ALLOWED
NOT_FOUND                  = http.HTTPStatus.METHOD_NOT_ALLOWED

class HTTPRequestHandler(ProtocolBase):
    """
    Request handler of an ``HTTPServer``.
    
    Attributes
    ----------
    _at_eof : `bool`
        Whether the protocol received end of file.
    _chunks : `deque` of `bytes`
        Right feed, left pop queue, used to store the received data chunks.
    _offset : `int`
        Byte offset, of the used up data of the most-left chunk.
    _paused : `bool`
        Whether the protocol's respective transport's reading is paused. Defaults to `False`.
        
        Also note, that not every transport supports pausing.
    exception : `None` or `BaseException`
        Exception set by ``.set_exception``, when an unexpected exception occur meanwhile reading from socket.
    loop : ``EventThread``
        The event loop to what the protocol is bound to.
    payload_reader : `None` or `generator`
        Payload reader generator, what gets the control back, when data, eof or any exception is received.
    payload_waiter : `None` of ``Future``
        Payload waiter of the protocol, what's result is set, when the ``.payload_reader`` generator returns.
        
        If cancelled or marked by done or any other methods, the payload reader will not be cancelled.
    transport : `None` or `Any`
        Asynchronous transport implementation. Is set meanwhile the protocol is alive.
    _drain_waiter : `None` or ``Future``
        A future, what is used to block the writing task, till it's writen data is drained.
    handler_task : `None` or ``Task`` of ``.lifetime_handler``
        Handles the connected http request meanwhile it is alive.
    server : ``HTTPServer``
        The http server of the handler.
    """
    __slots__ = ('handler_task', 'server',)
    def __init__(self, server):
        """
        Creates a new ``HTTPRequestHandler`` instance bound to it's server.
        
        Parameters
        ----------
        server : ``HTTPServer``
            The http server of the handler.
        """
        self.server = server
        ProtocolBase.__init__(self, server.loop)
    
    def connection_made(self, transport):
        """
        Called when a connection is made.
        
        Parameters
        ----------
        transport : `Any`
            Asynchronous transport implementation, what calls the protocol's ``.data_received`` when data is
            received.
        """
        ProtocolBase.connection_made(self, transport)
        self.server.register(self)
        self.handler_task = Task(self.lifetime_handler(), self.loop)
    
    async def lifetime_handler(self):
        try:
            request_message = await self._try_receive_request()
            if request_message is None:
                return
        
        except:
            # We will let Task.__del__ to render the exception...
            
            transport = self.transport
            if transport is None:
                raise
                
            transport.close()
            transport.abort()
            raise
        
        finally:
            self.handler_task = None
            self.server.unregister(self)
    
    async def _try_receive_request(self):
        """
        Tries to receive the http request.
        
        This method is a coroutine.
        
        Returns
        -------
        request_message : ``RawRequestMessage`` or `None`
            Returns `None` if reading teh request fails.
        """
        try:
            request_message = await self.set_payload_reader(self._read_http_request())
        except (CancelledError, ConnectionError) as err:
            await self.loop.render_exc_async(err, before = [
                'Unhandled exception occurred at `',
                self.__class__.__name__,
                '._try_receive_request`, when reading request.:\n'])
            return None
        except BaseException as err:
            if isinstance(err, PayloadError):
                status = BAD_REQUEST
                headers = imultidict()
                body = f'Invalid request body: {err}.\n'.encode()
            else:
                status = INTERNAL_SERVER_ERROR
                headers = imultidict()
                body = b'Failed to open a WebSocket connection.\n'
        else:
            version = request_message.version
            if version == HttpVersion11:
                return request_message
            
            status = HTTP_VERSION_NOT_SUPPORTED
            headers = imultidict()
            body = f'Http version: {version[0]}.{version[1]} is not supported.\n'.encode()
        
        try:
            self.write_http_response(status, headers, body=body)
            
            transport = self.transport
            if (transport is not None):
                transport.close()
                # Abort the TCP connection
                transport.abort()
        except BaseException as err2:
            await self.loop.render_exc_async(err2, before=[
                'Unhandled exception occurred at `',
                self.__class__.__name__,
                '._try_receive_request`, when handling an other exception;',
                repr(err), ':'])
        
        return None


class HTTPServer(object):
    """
    Http web-server implementation.
    
    Attributes
    ----------
    close_connection_task : `None` or ``Task`` of ``_close``
        Close connection task, what's result is set, when closing of the websocket is done.
        
        Should not be cancelled.
        
        Set, when ``.close`` is called.
    handlers : `set` of ``HTTPRequestHandler`` instances
        Active request handlers of the server.
    loop : ``EventThread``
        The event loop of the http server.
    server : `None` or ``Server``
        Asynchronous server instance. Set meanwhile the websocket server is running.
    """
    __slots__ = ('close_connection_task', 'handlers', 'loop', 'server')
    async def __new__(cls, loop, host, port, *, ssl=None, **server_kwargs):
        """
        Creates a new ``HTTPServer`` instance with the given parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        loop : ``EventThread``
            The event loop to what the http server server is bound to.
        host : `None` or `str`, `iterable` of (`None` or `str`), Optional
            To what network interfaces should the server be bound.
        port : `None` or `int`, Optional
            The port to use by the `host`(s).
        ssl : `None` or ``SSLContext``, Optional
            Whether and what ssl is enabled for the connections.
        **server_kwargs : Keyword arguments
            Additional keyword arguments to create the websocket server with.
        
        Other Parameters
        ----------------
        family : `AddressFamily` or `int`
            Can be given either as `socket.AF_INET` or `socket.AF_INET6` to force the socket to use `IPv4` or `IPv6`.
            If not given, then  will be determined from host name.
        backlog : `int`
            The maximum number of queued connections passed to `listen()` (defaults to 100).
        reuse_address : `bool`, Optional
            Tells the kernel to reuse a local socket in `TIME_WAIT` state, without waiting for its natural timeout to
            expire. If not specified will automatically be set to True on Unix.
        reuse_port : `bool`, Optional
            Tells to the kernel to allow this endpoint to be bound to the same port as an other existing endpoint
            already might be bound to.
            
            Not supported on Windows.
        """
        self = object.__new__(cls)
        self.loop = loop
        self.handlers = set()
        self.close_connection_task = None
        self.server = None
        
        factory = functools.partial(HTTPRequestHandler, self,)
        server = await loop.create_server(factory, host, port, ssl=ssl, **server_kwargs)
        
        self.server = server
        await server.start()
        
        return self


    def register(self, protocol):
        """
        Registers a newly created HTTP request handler to the HTTP server itself.
        
        Parameters
        ----------
        protocol : ``HTTPRequestHandler`` or `Any`
            The connected server side http request handler.
        """
        self.handlers.add(protocol)
    
    def unregister(self, protocol):
        """
        Unregisters a newly created server side HTTP request handler from the HTTP server itself.
        
        Parameters
        ----------
        protocol : ``HTTPRequestHandler`` or `Any`
            The connected server side http request handler.
        """
        self.handlers.discard(protocol)
    
    def is_serving(self):
        """
        Returns whether the HTTP server is serving.
        
        Returns
        -------
        is_serving : `bool`
        """
        server = self.server
        if server is None:
            return False
        
        if server.sockets is None:
            return False
        
        return True
    
    def close(self):
        """
        Closes the websocket server. Returns a closing task, what can be awaited.
        
        Returns
        -------
        close_connection_task : ``Task`` of ``_close``
            Close connection task, what's result is set, when closing of the HTTP server is done.
            
            Should not be cancelled.
        """
        close_connection_task = self.close_connection_task
        if close_connection_task is None:
            close_connection_task = Task(self._close(), self.loop)
            self.close_connection_task = close_connection_task
        
        return close_connection_task
    
    async def _close(self):
        """
        Closes the HTTP server. If the websocket task is already closed does nothing.
        
        This method is a coroutine.
        """
        server = self.server
        if server is None:
            return
        
        server.close()
        await server.wait_closed()
        
        loop = self.loop
        
        # Skip 1 full loop
        future = Future(loop)
        loop.call_at(0.0, Future.set_result_if_pending, future, None)
        await future
        
        handlers = self.handlers
        if handlers:
            tasks = []
            for request_handler in handlers:
                tasks.append(request_handler.close(1001))
            
            future = WaitTillAll(tasks, loop)
            tasks = None
            await future
            
        if handlers:
            tasks = []
            for request_handler in handlers:
                task = request_handler.handler_task
                if task is None:
                    continue
                
                tasks.append(task)
            
            task = None
            if tasks:
                future = WaitTillAll(tasks, loop)
                tasks = None
                await future


class Route(object):
    """
    Represents a route found by ``PathRouter``.
    
    Attributes
    ----------
    func : `None` or `callable`
        Function found by the route or `None` if nothing found.
    parameters : `None` or `dict` of (`str`, `str`) items
        Dynamic parameter queried from the urls.
    """
    __slots__ = ('func', 'parameters', 'state')
    def __init__(self, func):
        """
        Creates a new ``Route`` instance with the given `func`.
        
        Parameters
        ----------
        func : `None` or `callable`
            Function found by the route or `None` if nothing found.
        """
        self.func = func
        self.parameters = None
    
    def add_parameter(self, name, value):
        """
        Adds a new parameter to the route.
        
        Parameters
        ----------
        name : `str`
            The parameter's name.
        value : `str`
            The parameter's value.
        """
        parameters = self.parameters
        if parameters is None:
            self.parameters = parameters = {}
        
        parameters[name] = value


MAYBE_REGEX_PATH_PART_RP = re.compile('<(?:(string|int|float|uuid)\:)?([a-zA-Z_][a-zA-Z_0-9]*)>')

PARAMETER_TYPE_STATIC = 0

PARAMETER_TYPE_PATH = 1

PARAMETER_TYPE_INT = 2
PARAMETER_TYPE_FLOAT = 3
PARAMETER_TYPE_UUID = 4
PARAMETER_TYPE_STRING = 5


PARAMETER_TYPE_DEFAULT = PARAMETER_TYPE_STRING

PARAMETER_NAME_TYPE_RELATION = {
    'string': PARAMETER_TYPE_STRING ,
    'int'   : PARAMETER_TYPE_INT    ,
    'float' : PARAMETER_TYPE_FLOAT  ,
    'path'  : PARAMETER_TYPE_PATH   ,
    'uuid'  : PARAMETER_TYPE_UUID   ,
        }

def maybe_type_part(part):
    """
    Checks whether the given url part is maybe a dynamic one.
    
    Parameters
    ----------
    part : `str`
        Url part to process
    
    Returns
    -------
    parameter_type : `int`
        The parameter's type.
        
        Can be any of the following values:
        
        +---------------------------+-------+
        | Respective name           | Value |
        +===========================+=======+
        | PARAMETER_TYPE_STATIC     | 0     |
        +---------------------------+-------+
        | PARAMETER_TYPE_PATH       | 1     |
        +---------------------------+-------+
        | PARAMETER_TYPE_INT        | 2     |
        +---------------------------+-------+
        | PARAMETER_TYPE_FLOAT      | 3     |
        +---------------------------+-------+
        | PARAMETER_TYPE_UUID       | 4     |
        +---------------------------+-------+
        | PARAMETER_TYPE_STRING     | 5     |
        +---------------------------+-------+
    
    parameter_name : `str`
        The parameter's name if applicable.
    """
    matched = MAYBE_REGEX_PATH_PART_RP.fullmatch(part)
    if matched is None:
        parameter_type = PARAMETER_TYPE_STATIC
        parameter_name = part
    else:
        parameter_type_name, parameter_name = matched.groups()
        if parameter_type_name is None:
            parameter_type = PARAMETER_TYPE_DEFAULT
        else:
            parameter_type = PARAMETER_NAME_TYPE_RELATION[parameter_type_name]
    
    return parameter_type, parameter_name

def validate_int(value):
    """
    Parses the given value whether it is integer. If it is, returns it.
    
    Parameters
    ----------
    value : `str`
        The value to validate.
    
    Returns
    -------
    value : `None` or `int`
    """
    if value.isdigit:
        return int(value)

def validate_float(value):
    """
    Parses the given value whether it is float. If it is, returns it.
    
    Parameters
    ----------
    value : `str`
        The value to validate.
    
    Returns
    -------
    value : `None` or `float`
    """
    if value.isnumeric():
        return float(value)
    
def validate_uuid(value):
    """
    Parses the given value whether it is uuid. If it is returns it.
    
    Parameters
    ----------
    value : `str`
        The value to validate.
    
    Returns
    -------
    value : `None` or `uuid.UUID`
    """
    try:
        value = UUID(value)
    except ValueError:
        value = None
    
    return value

def validate_string(value):
    """
    Parses the given string value. Always returns value itself.
    
    Parameters
    ----------
    value : `str`
        The value to validate.

    Returns
    -------
    value : `str`
    """
    return value


PARAMETER_TYPE_TO_VALIDATOR = {
    PARAMETER_TYPE_INT    : validate_int    ,
    PARAMETER_TYPE_FLOAT  : validate_float  ,
    PARAMETER_TYPE_UUID   : validate_uuid   ,
    PARAMETER_TYPE_STRING : validate_string ,
        }


class ParameterValidatorPathStep(object):
    """
    Represents a path dispatching step, here validation is used.
    
    Attributes
    ----------
    path_routers : `list` of `tuple` (`str`, ``PathRouter``)
        A list of `parameter-name`, `path-router` combination to route to.
    parameter_type : `int`
        Identifier value representing the validator.
        
        Can be one of following:

        +---------------------------+-------+
        | Respective name           | Value |
        +===========================+=======+
        | PARAMETER_TYPE_INT        | 2     |
        +---------------------------+-------+
        | PARAMETER_TYPE_FLOAT      | 3     |
        +---------------------------+-------+
        | PARAMETER_TYPE_UUID       | 4     |
        +---------------------------+-------+
        | PARAMETER_TYPE_STRING     | 5     |
        +---------------------------+-------+
        
    validator : `function`
        The respective validator.
    """
    __slots__ = ('path_routers', 'parameter_type', 'validator',)
    def __new__(cls, parameter_type, parameter_name):
        """
        Creates a new ``ParameterValidatorPathStep`` instance with teh given parameters.
        
        Parameters
        ----------
        parameter_type : `int`
            Identifier value representing the validator.
            
            Can be one of following:
    
            +---------------------------+-------+
            | Respective name           | Value |
            +===========================+=======+
            | PARAMETER_TYPE_INT        | 2     |
            +---------------------------+-------+
            | PARAMETER_TYPE_FLOAT      | 3     |
            +---------------------------+-------+
            | PARAMETER_TYPE_UUID       | 4     |
            +---------------------------+-------+
            | PARAMETER_TYPE_STRING     | 5     |
            +---------------------------+-------+
        parameter_name : `str`
            The parameter's name.
        
        Returns
        -------
        self :
        """
        self = object.__new__(cls)
        self.parameter_type = parameter_type
        self.validator = PARAMETER_TYPE_TO_VALIDATOR[parameter_type]
        path_router = PathRouter()
        self.path_routers = [(parameter_name, path_router)]
        return self, path_router
    
    def get_path_router(self, parameter_name):
        """
        Gets path router for the defined path.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.

        Returns
        -------
        path_router : ``PathRouter``
            The matched or created router.
        """
        path_routers = self.path_routers
        for maybe_parameter_name, path_router in path_routers:
            if maybe_parameter_name == parameter_name:
                break
        else:
            path_router = PathRouter()
            path_routers.append((parameter_name, path_router))
        
        return path_router
    
    def __ge__(self, other):
        """Returns whether self should be tested later or at the same time as the other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.parameter_type >= other.parameter_type:
            return True
        
        return False
    
    def __gt__(self, other):
        """Returns whether self should be tested later than other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.parameter_type > other.parameter_type:
            return True
        
        return False
    
    def __eq__(self, other):
        """Returns whether self should be tested at the same time as the other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.parameter_type == other.parameter_type:
            return True
        
        return False
        
    def __ne__(self, other):
        """Returns whether self not should be tested at the same time as the other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.parameter_type != other.parameter_type:
            return True
        
        return False
    
    def __lt__(self, other):
        """Returns whether self should be tested at the same time as the other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.parameter_type < other.parameter_type:
            return True
        
        return False
    
    def __le__(self, other):
        """Returns whether self should be tested earlier or at the same time as the other."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.parameter_type <= other.parameter_type:
            return True
        
        return False


class PathRouter(object):
    """
    Path router for getting which handler function should run for a pre-defined route.
    
    Attributes
    ----------
    route_step_paths : `None` or `dict` of (`str`, ``PathRouter``) items
        Generic string paths to route to. Set as `None` if empty.
    route_step_validated : `None` or `list` of ``ParameterValidatorPathStep``
        Contains `parameter-name`, `validator`, `router` elements to route dynamic names.
    route_end : `None` or `dict` of (`str`, `Any`) items
        If the url ends at the point of this router, then the handler function from ``.route_ends`` is chosen if
        applicable. The functions are stored in `method` - `handler` relation.
    route_end_path : `None` or `dict` of  (`str`, `tuple` (`str`, `async-callable`)) items
        Paths, which have dynamic route ends.
    """
    __slots__ = ('route_end', 'route_end_path', 'route_step_paths', 'route_step_validated')
    def __init__(self):
        """
        Creates a new ``PathRouter`` instance.
        """
        self.route_step_paths = None
        self.route_step_validated = None
        self.route_end = None
        self.route_end_path = None
    
    def dispatch_url(self, path, index, request_method):
        """
        Dispatches the given url, getting it's router.
        
        Parameters
        ----------
        path : `tuple` of `str`
            The request's url's parts.
        index : `int`
            The next index of `path` to inspect.
        request_method : `str`
            The method's request.
        
        Returns
        -------
        route : `None` or ``Route``
            The found route if any.
        """
        if index == len(path):
            route_end = self.route_end
            if route_end is None:
                return None
            
            return Route(route_end.get(request_method, _handler_method_not_allowed))
        
        path_part = path[index]
        index += 1
        
        route_step_paths = self.route_step_paths
        if (route_step_paths is not None):
            try:
                path_router = route_step_paths[path_part]
            except KeyError:
                pass
            else:
                route = path_router.dispatch_url(path, index, request_method)
                if (route is not None):
                    return route
        
        route_step_validated = self.route_step_validated
        if (route_step_validated is not None):
            for parameter_validator_path_step in route_step_validated:
                value = parameter_validator_path_step.validator(path_part)
                if value is None:
                    continue
                
                for parameter_name, path_router in parameter_validator_path_step.path_routers:
                    route = path_router.dispatch_url(path, index, request_method)
                    if (route is None):
                        continue
                    
                    route.add_parameter(parameter_name, value)
                    return route
        
        route_end_path = self.route_end_path
        if (route_end_path is not None):
            parameter_name_and_handler = route_end_path.get(request_method, None)
            if parameter_name_and_handler is None:
                handler = _handler_method_not_allowed
            else:
                handler = parameter_name_and_handler[1]
            
            route = Route(handler)
            
            if (parameter_name_and_handler is not None):
                route.add_parameter(parameter_name_and_handler[0], '/'.join(path[index:]))
            
            return route
        
        return None
    
    def register_url(self, path_type_and_url, index, request_method, handler):
        """
        Registers a new handler to the path router.
        
        Parameters
        ----------
        path_type_and_url : `tuple` of (`int`, `str`)
            The path to register.
        index : `int`
            The index of the part of the path to process by this router.
        request_method : `str`
            The method of the request to register.
        handler : `async-callable`
            The handler to register.
        """
        if index == len(path_type_and_url):
            route_end = self.route_end
            if route_end is None:
                route_end = self.route_end = {}
            
            route_end[request_method] = handler
            
            return
        
        path_part_type, path_part = path_type_and_url[index]
        index += 1
        
        if path_part_type == PARAMETER_TYPE_STATIC:
            route_step_paths = self.route_step_paths
            if route_step_paths is None:
                route_step_paths = self.route_step_paths = {}
            
            try:
                path_router = route_step_paths[path_part]
            except KeyError:
                path_router = route_step_paths[path_part] = PathRouter()
            
            path_router.register_url(path_type_and_url, index, request_method, handler)
            return
        
        if path_part_type == PARAMETER_TYPE_PATH:
            route_end_path = self.route_end_path
            if route_end_path is None:
                route_end_path = self.route_end_path = {}
            
            route_end_path[request_method] = (path_part, handler)
            return
        
        route_step_validated = self.route_step_validated
        if route_step_validated is None:
            route_step_validated = self.route_step_validated = []
            
            parameter_validator_path_step, path_router = ParameterValidatorPathStep(path_part_type, path_part)
            path_router.register_url(path_type_and_url, index, request_method, handler)
            
            route_step_validated.append(parameter_validator_path_step)
            return
        
        for parameter_validator_path_step in route_step_validated:
            if parameter_validator_path_step.parameter_type == path_part_type:
                path_router = parameter_validator_path_step.get_path_router(path_part)
                path_router.register_url(path_type_and_url, index, request_method, handler)
                return
        
        parameter_validator_path_step, path_router = ParameterValidatorPathStep(path_part_type, path_part)
        path_router.register_url(path_type_and_url, index, request_method, handler)
        
        route_step_validated.append(parameter_validator_path_step)


class AbortRequest(BaseException):
    """
    Exception raised when ``abort`` is called.
    
    Attributes
    ----------
    response_code : `int`
        The request abortion code.
    message : `None` or `str`
        Abortion message to send.
    """
    def __init__(self, response_code, message=None):
        
        self.response_code = response_code
        self.message = message
        BaseException.__init__(self)


async def _handler_method_not_allowed():
    """
    Aborts the request with error code 405.
    
    Raises
    ------
    AbortRequest
        With response code of `405`.
    """
    raise AbortRequest(METHOD_NOT_ALLOWED)

async def _handler_not_found():
    """
    Aborts the request with error code 404.
    
    Raises
    ------
    AbortRequest
        With response code of `404`.
    """
    raise AbortRequest(NOT_FOUND)


class WebApp(object):
    """
    _server : `None` or ``WebServer``
    
    _router : ``PathRouter``
        Path router to decide which function should be called when receiving a request.
    """
    __slots__ = ('_server', '_router')
    def __init__(self):
        self._server = None
        self._router = PathRouter()
    
    def _dispatch_url(self, url, request_method):
        """
        Gets handler for the given `url` and `request_method` combination.
        
        Parameters
        ----------
        url : ``URL`` instance
            The received request url.
        request_method : `str`
            The method to request.
        """
        path = url.path
        route = self._router.dispatch_url(path, 0, request_method)
        if route is None:
            route = Route(_handler_not_found)
        
        return route
    
    def _register_url(self, url, request_method, handler):
        """
        Registers an url and handler to the http server.
        
        Parameters
        ----------
        url : ``URL`` instance
            The url to register.
        request_method : `str`
            The method to request.
        handler : `async-callable`
            The handler to call when the given url and method I requested.
        """
        path_type_and_value = tuple(maybe_type_part(path_part) for path_part in url.path)
        self._router.register_url(path_type_and_value, 0, request_method, handler)
