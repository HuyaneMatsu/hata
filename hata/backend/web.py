# -*- coding: utf-8 -*-
# Experimenting with web servers, nothing worthy
# WORK IN PROGRESS
import functools, http, re, sys, os, ntpath
from threading import current_thread

from uuid import UUID
from importlib.util import find_spec

from .utils import imultidict
from .futures import WaitTillAll, Future, Task, CancelledError
from .protocol import ProtocolBase
from .exceptions import PayloadError
from .helpers import HttpVersion11
from .headers import METHOD_ALL, METHOD_GET
from .url import URL
from .analyzer import CallableAnalyzer
from .event_loop import EventThread

INTERNAL_SERVER_ERROR = http.HTTPStatus.INTERNAL_SERVER_ERROR
BAD_REQUEST = http.HTTPStatus.BAD_REQUEST
HTTP_VERSION_NOT_SUPPORTED = http.HTTPStatus.HTTP_VERSION_NOT_SUPPORTED
METHOD_NOT_ALLOWED = http.HTTPStatus.METHOD_NOT_ALLOWED
NOT_FOUND = http.HTTPStatus.METHOD_NOT_ALLOWED

TASK_LOCALS = {}

class TaskLocal:
    """
    Allows instances's attributes to be accessed from the task where the ``TaskLocal`` is entered from.
    
    Attributes
    ----------
    _kwargs : `dict` of (`str`, `Any`) items
        `name` - `object` pairs to add as task local.
    _task : `None` or ``Task``
        The entered task.
    """
    __slots__ = ('_kwargs', '_task', )
    def __new__(cls, **kwargs):
        """
        Creates a new ``TaskLocal`` instance.
        
        Parameters
        ----------
        **kwargs : `Any`
            `name` - `object` pairs to add as task local.
        """
        self = object.__new__(cls)
        self._kwargs = kwargs
        self._task = None
        return self
    
    def __enter__(self):
        """
        Enables the task local on the current task.
        
        Raises
        ------
        RuntimeError
            - If called from outside of an ``EventThread``.
            - If called from outside of a ``Task``.
            - If already entered.
        """
        task = self._task
        if task is not None:
            raise RuntimeError(f'{self.__class__.__name__} is already entered inside of {task!r}.')
        
        thread = current_thread()
        if not isinstance(thread, EventThread):
            raise RuntimeError(f'{self.__class__.__name__} used outside of {EventThread.__name__}, at {thread!r}.')
        
        task = thread.current_task
        if task is None:
            raise RuntimeError(f'{self.__class__.__name__} used outside of a {Task.__name__}.')
        
        self._task = task
        
        kwargs = self._kwargs
        try:
            locals_ = TASK_LOCALS[task]
        except KeyError:
            TASK_LOCALS[task] = kwargs.copy()
        else:
            locals_.update(kwargs)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Disables the task local on the current task.
        """
        thread = current_thread()
        if not isinstance(thread, EventThread):
            return
        
        task = thread.current_task
        if task is None:
            return
        
        if task is self._task:
            self._task = None
        
        kwargs = self._kwargs
        try:
            locals_ = TASK_LOCALS[task]
        except KeyError:
            return
        
        for key, value in kwargs.items():
            try:
                local_value = locals_[key]
            except KeyError:
                continue
            
            if local_value is not value:
                continue
            
            del locals_[key]
            continue



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
            Returns `None` if reading the request fails.
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
                repr(err2), ':'])
        
        return None


class HTTPServer:
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
        ssl : `None` or ``SSLContext``, Optional (Keyword only)
            Whether and what ssl is enabled for the connections.
        **server_kwargs : Keyword parameters
            Additional keyword parameters to create the websocket server with.
        
        Other Parameters
        ----------------
        family : `AddressFamily` or `int`, Optional (Keyword only)
            Can be given either as `socket.AF_INET` or `socket.AF_INET6` to force the socket to use `IPv4` or `IPv6`.
            If not given, then  will be determined from host name.
        backlog : `int`, Optional (Keyword only)
            The maximum number of queued connections passed to `listen()` (defaults to 100).
        reuse_address : `bool`, Optional (Keyword only)
            Tells the kernel to reuse a local socket in `TIME_WAIT` state, without waiting for its natural timeout to
            expire. If not specified will automatically be set to True on Unix.
        reuse_port : `bool`, Optional (Keyword only)
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


class Route:
    """
    Represents a route found by ``PathRouter``.
    
    Attributes
    ----------
    rule : ``Rule``
        Rule object found by a route.
    parameters : `None` or `dict` of (`str`, `str`) items
        Dynamic parameter queried from the urls.
    """
    __slots__ = ('parameters', 'rule', )
    def __init__(self, rule):
        """
        Creates a new ``Route`` instance with the given `func`.
        
        Parameters
        ----------
        rule : ``Rule``
            Function found by the router.
        """
        self.rule = rule
        parameters = rule.parameters
        if (parameters is not None):
            parameters = dict(parameters)
        self.parameters = parameters
        
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
    
    def __repr__(self):
        """Returns the routes representation."""
        result = ['<', self.__class__.__name__]
        
        parameters = self.parameters
        if (parameters is not None):
            result.append(' parameters=')
            result.append(repr(parameters))
            result.append(', ')
        
        result.append(' rule=')
        result.append(repr(self.rule))
        
        result.append('>')
        
        return ''.join(result)
    
    def __call__(self):
        """
        Calls the route.
        
        Returns
        -------
        coroutine : `CoroutineType` or `GeneratorType`
            The ``.rule``'s `view_func`.
        """
        rule = self.rule
        parameters = self.parameters.copy()
        
        positional_parameter_names = rule.positional_parameter_names
        if positional_parameter_names is None:
            positional_parameters = None
        else:
            positional_parameters = []
            for parameter_name in positional_parameter_names:
                positional_parameters.append(parameters.pop(parameter_name))
        
        if rule.kwargs_parameter_supported:
            keyword_parameters = parameters
        else:
            keyword_parameter_names = rule.keyword_parameter_names
            if keyword_parameter_names is None:
                keyword_parameters = None
            else:
                keyword_parameters = {}
                for parameter_name in keyword_parameter_names:
                    keyword_parameters[parameter_name] = parameters[parameter_name]
        
        view_func = rule.view_func
        if positional_parameters is None:
            if keyword_parameters is None:
                coroutine = view_func()
            else:
                coroutine = view_func(**keyword_parameters)
        else:
            if keyword_parameters is None:
                coroutine = view_func(*positional_parameters)
            else:
                coroutine = view_func(*positional_parameters, **keyword_parameters)
        
        return coroutine




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

def maybe_typed_rule_part(part):
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

PARAMETER_TYPE_TO_NAME = {
    PARAMETER_TYPE_PATH   : 'path'   ,
    PARAMETER_TYPE_INT    : 'int'    ,
    PARAMETER_TYPE_FLOAT  : 'float'  ,
    PARAMETER_TYPE_UUID   : 'uuid'   ,
    PARAMETER_TYPE_STRING : 'string' ,
        }

class ParameterValidatorPathStep:
    """
    Represents a path dispatching step, here validation is used.
    
    Attributes
    ----------
    path_routers : `list` of `tuple` (``PathRouter``, `str`)
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
        Creates a new ``ParameterValidatorPathStep`` instance with the given parameters.
        
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
        self.path_routers = [(path_router, parameter_name)]
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
        for path_router, maybe_parameter_name in path_routers:
            if maybe_parameter_name == parameter_name:
                break
        else:
            path_router = PathRouter()
            path_routers.append((path_router, parameter_name))
        
        return path_router
    
    def render_structure(self, route_prefix_parts, parts):
        """
        Renders the path router's structure to the given `parts` list.
        
        Parameters
        ----------
        route_prefix_parts : `list` of `str`
            Prefix parts to th route to render.
        parts : `list` of `str`
            Rendered path parts.
        """
        parameter_type = self.parameter_type
        for path_router, parameter_name in self.path_routers:
            path_part = _rebuild_path_parameter(parameter_type, parameter_name)
            route_prefix_parts.append(path_part)
            path_router.render_structure(route_prefix_parts, parts)
            del route_prefix_parts[-1]
    
    def validate_parameters(self):
        """
        Validates the parameters of the rules registered into the parameter validator path step.
        
        Raises
        ------
        RuntimeError
            If a `view_func` might not receive a parameter in runtime.
        """
        for router, parameter_name in self.path_routers:
            router.validate_parameters()
    
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

def _render_route_prefix_into(route_prefix_parts, parts):
    """
    Renders the given route route prefix parts into the given `parts` list.
    
    Parameters
    ----------
    route_prefix_parts : `list` of `str`
        Prefix parts to the route to render.
    parts : `list` of `str`
        Rendered path parts.
    """
    limit = len(route_prefix_parts)
    if limit:
        index = 0
        while True:
            element = route_prefix_parts[index]
            parts.append(element)
            
            index += 1
            if index == limit:
                break
            
            parts.append('/')
            continue


def _rebuild_path_parameter(parameter_type, parameter_name):
    """
    Rebuilds a typed path part from it's type identifier and from it's name.
    
    Parameters
    ----------
    parameter_type : `int`
        Parameter type identifier.
    parameter_name : `str`
        The parameter's name.
    
    Returns
    -------
    path_parameter : `str`
    """
    parameter_type_name = PARAMETER_TYPE_TO_NAME[parameter_type]
    return f'<{parameter_type_name}:{parameter_name}>'


class PathRouter:
    """
    Path router for getting which handler function should run for a pre-defined route.
    
    Attributes
    ----------
    route_step_paths : `None` or `dict` of (`str`, ``PathRouter``) items
        Generic string paths to route to. Set as `None` if empty.
    route_step_validated : `None` or `list` of ``ParameterValidatorPathStep``
        Contains `parameter-name`, `validator`, `router` elements to route dynamic names.
    route_end : `None` or `dict` of (`str`, ``Rule``) items
        If the url ends at the point of this router, then the handler function from ``.route_ends`` is chosen if
        applicable. The functions are stored in `method` - `handler` relation.
    route_end_all : `None` or ``Rule``
        If the url ends at this point of the router and non of the `route-end`-s were matched, the the view function
        of this slot is chosen.
    route_end_path : `None` or `dict` of (`str`, `tuple` (``Rule``, `str`)) items
        Paths, which have dynamic route ends.
    route_end_path_all : `None` or `tuple` (``Rule``, `str`)
        ``.route_end_path`` version, what accepts accepts all type of request methods.
    """
    __slots__ = ('route_end', 'route_end_all', 'route_end_path', 'route_end_path_all', 'route_step_paths',
        'route_step_validated')
    def __init__(self):
        """
        Creates a new ``PathRouter`` instance.
        """
        self.route_step_paths = None
        self.route_step_validated = None
        self.route_end = None
        self.route_end_all = None
        self.route_end_path = None
        self.route_end_path_all = None
    
    def dispatch_route(self, path, index, request_method):
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
            
            try:
                rule = route_end[request_method]
            except KeyError:
                pass
            else:
                return Route(rule)
            
            route_end_all = self.route_end_all
            if route_end_all is None:
                return Route(ROUTE_METHOD_NOT_ALLOWED)
            
            rule = route_end_all
            return Route(rule)
        
        rule_part = path[index]
        index += 1
        
        route_step_paths = self.route_step_paths
        if (route_step_paths is not None):
            try:
                path_router = route_step_paths[rule_part]
            except KeyError:
                pass
            else:
                route = path_router.dispatch_route(path, index, request_method)
                if (route is not None):
                    return route
        
        route_step_validated = self.route_step_validated
        if (route_step_validated is not None):
            for parameter_validator_path_step in route_step_validated:
                value = parameter_validator_path_step.validator(rule_part)
                if value is None:
                    continue
                
                for parameter_name, path_router in parameter_validator_path_step.path_routers:
                    route = path_router.dispatch_route(path, index, request_method)
                    if (route is None):
                        continue
                    
                    route.add_parameter(parameter_name, value)
                    return route
        
        route_end_path = self.route_end_path
        route_end_path_all = self.route_end_path_all
        if (route_end_path is not None) or (route_end_path_all is not None):
            if (route_end_path is not None):
                try:
                    rule, parameter_name = route_end_path[request_method]
                except KeyError:
                    pass
                else:
                    route = Route(rule)
                    route.add_parameter(parameter_name, '/'.join(path[index:]))
                    return route
            
            if route_end_path_all is None:
                return Route(ROUTE_METHOD_NOT_ALLOWED)
            
            rule, parameter_name = route_end_path_all
            route = Route(rule)
            route.add_parameter(parameter_name, '/'.join(path[index:]))
            return route
        
        return None
    
    def register_route(self, rule, index):
        """
        Registers a new handler to the path router.
        
        Parameters
        ----------
        rule : ``Rule``
            The rule of the endpoint
        index : `int`
            The index of the part of the path to process by this router.
        """
        url_rule = rule.rule
        if index == len(url_rule):
            request_methods = rule.request_methods
            if request_methods is None:
                self.route_end_all = rule
            else:
                route_end = self.route_end
                if route_end is None:
                    route_end = self.route_end = {}
                
                for request_method in request_methods:
                    route_end[request_method] = rule
            
            return
        
        rule_part_type, rule_part = url_rule[index]
        index += 1
        
        if rule_part_type == PARAMETER_TYPE_STATIC:
            route_step_paths = self.route_step_paths
            if route_step_paths is None:
                route_step_paths = self.route_step_paths = {}
            
            try:
                path_router = route_step_paths[rule_part]
            except KeyError:
                path_router = route_step_paths[rule_part] = PathRouter()
            
            path_router.register_route(rule, index)
            return
        
        if rule_part_type == PARAMETER_TYPE_PATH:
            rule_rule_part_tuple = (rule, rule_part)
            request_methods = rule.request_methods
            if request_methods is None:
                self.route_end_path_all = rule_rule_part_tuple
            else:
                route_end_path = self.route_end_path
                if route_end_path is None:
                    route_end_path = self.route_end_path = {}
                
                for request_method in request_methods:
                    route_end_path[request_method] = rule_rule_part_tuple
            return
        
        route_step_validated = self.route_step_validated
        if route_step_validated is None:
            route_step_validated = self.route_step_validated = []
            
            parameter_validator_path_step, path_router = ParameterValidatorPathStep(rule_part_type, rule_part)
            path_router.register_route(rule, index)
            
            route_step_validated.append(parameter_validator_path_step)
            return
        
        for parameter_validator_path_step in route_step_validated:
            if parameter_validator_path_step.parameter_type == rule_part_type:
                path_router = parameter_validator_path_step.get_path_router(rule_part)
                path_router.register_route(rule, index)
                return
        
        parameter_validator_path_step, path_router = ParameterValidatorPathStep(rule_part_type, rule_part)
        path_router.register_route(rule, index)
        
        route_step_validated.append(parameter_validator_path_step)
    
    def render_structure(self, route_prefix_parts, parts):
        """
        Renders the path router's structure to the given `parts` list.
        
        Parameters
        ----------
        route_prefix_parts : `list` of `str`
            Prefix parts to the route to render.
        parts : `list` of `str`
            Rendered path parts.
        """
        route_step_paths = self.route_step_paths
        if (route_step_paths is not None):
            for path_part, path_router in route_step_paths.items():
                route_prefix_parts.append(path_part)
                path_router.render_structure(route_prefix_parts, parts)
                del route_prefix_parts[-1]
        
        route_step_validated = self.route_step_validated
        if (route_step_validated is not None):
            for parameter_validator_path_step in route_step_validated:
                parameter_validator_path_step.render_structure(route_prefix_parts, parts)
        
        route_end = self.route_end
        if (route_end is not None):
            _render_route_prefix_into(route_prefix_parts, parts)
            parts.append(' ')
            
            methods = sorted(route_end.keys())
            if len(methods) != 1:
                methods_repr = repr(methods)
            else:
                methods_repr = methods[0]
            
            parts.append(methods_repr)
            parts.append('\n')
        
        route_end_all = self.route_end_all
        if (route_end_all is not None):
            _render_route_prefix_into(route_prefix_parts, parts)
            parts.append(' *\n')
        
        route_end_path = self.route_end_path
        if (route_end_path is not None):
            combinations = {}
            
            for request_method, (rule, parameter_name) in route_end_path.items():
                try:
                    methods = combinations[parameter_name]
                except KeyError:
                    combinations[parameter_name] = methods = []
                
                methods.append(request_method)
            
            for parameter_name, methods in combinations.items():
                path_part = _rebuild_path_parameter(PARAMETER_TYPE_PATH, parameter_name)
                route_prefix_parts.append(path_part)
                _render_route_prefix_into(route_prefix_parts, parts)
                del route_prefix_parts[-1]
                parts.append(' ')
                
                methods = sorted(route_end.keys())
                if len(methods) != 1:
                    methods_repr = repr(methods)
                else:
                    methods_repr = methods[0]
                
                parts.append(methods_repr)
                parts.append('\n')
        
        route_end_path_all = self.route_end_path_all
        if (route_end_path_all is not None):
            parameter_name = route_end_path_all[1]
            
            path_part = _rebuild_path_parameter(PARAMETER_TYPE_PATH, parameter_name)
            route_prefix_parts.append(path_part)
            _render_route_prefix_into(route_prefix_parts, parts)
            del route_prefix_parts[-1]
            parts.append(' *\n')
    
    def validate_parameters(self):
        """
        Validates the parameters of the rules registered into the router.
        
        Raises
        ------
        RuntimeError
            If a `view_func` might not receive a parameter in runtime.
        """
        route_step_paths = self.route_step_paths
        if (route_step_paths is not None):
            for path_router in route_step_paths.values():
                path_router.validate_parameters()
        
        route_step_validated = self.route_step_validated
        if (route_step_validated is not None):
            for parameter_validator_path_step in route_step_validated:
                parameter_validator_path_step.validate_parameters()
        
        route_end = self.route_end
        if (route_end is not None):
            for rule in route_end.values():
                rule.validate_parameters()
        
        route_end_all = self.route_end_all
        if (route_end_all is not None):
            route_end_all.validate_parameters()
        
        route_end_path = self.route_end_path
        if (route_end_path is not None):
            for rule, parameter_name in route_end_path.values():
                rule.validate_parameters()
        
        route_end_path_all = self.route_end_path_all
        if (route_end_path_all is not None):
            rule, parameter_name = route_end_path_all
            rule.validate_parameters()

class AbortRequest(BaseException):
    """
    Exception raised when ``abort`` is called.
    
    Attributes
    ----------
    response_code : `int`
        The request abortion code.
    reason : `None` or `str`
        Abortion reason to send.
    """
    def __init__(self, response_code, reason=None):
        
        self.response_code = response_code
        self.reason = reason
        BaseException.__init__(self)

def abort(response_code, reason=None):
    """
    Aborts the request when.
    
    Attributes
    ----------
    response_code : `int`
        The request abortion code.
    reason : `None` or `str`
        Abortion reason to send.
    """
    raise AbortRequest(response_code, reason)


async def _handler_method_not_allowed():
    """
    Aborts the request with error code 405.
    
    This function is a coroutine.
    
    Raises
    ------
    AbortRequest
        With response code of `405`.
    """
    raise AbortRequest(METHOD_NOT_ALLOWED)

async def _handler_not_found():
    """
    Aborts the request with error code 404.
    
    This function is a coroutine.
    
    Raises
    ------
    AbortRequest
        With response code of `404`.
    """
    raise AbortRequest(NOT_FOUND)


class _RouteAdder:
    """
    Route adder returned by ``WebBase.route`` to add a route to it as a decorator.
    
    Attributes
    ----------
    endpoint  : `None` or `str`
        The internal endpoint of the url. Defaults to the name of the added function.
    options : `dict` of (`str`, `Any`) items.
        Additional options to be forward to the underlying ``Rule`` object.
    parent : ``AppBase``
        The parent webapp.
    rule : `str`
        The url rule as string.
    """
    __slots__ = ('endpoint', 'options', 'parent', 'rule')
    def __new__(cls, parent, rule, endpoint, options):
        """
        Creates a new ``_RouteAdder object with the given parameters.
        
        Parameters
        ----------
        parent : ``AppBase``
            The parent webapp.
        rule : `str`
            The url rule as string.
        endpoint  : `None` or `str`
            The internal endpoint of the url. Defaults to the name of the added function.
        options : `dict` of (`str`, `Any`) items.
            Additional options to be forward to the underlying ``Rule`` object.
        """
        self = object.__new__(cls)
        self.parent = parent
        self.rule = rule
        self.endpoint = endpoint
        self.options = options
        return self
    
    def __call__(self, view_func):
        """
        Adds the given `view_func` and the stored parameters to the parent ``AppBase`` calling it's `.add_url_rule`
        method.
        
        Parameters
        ----------
        view_func : `async-callable`
            The function to call when serving a request to the provided endpoint.
        
        Returns
        -------
        rule : ``Rule``
            The added rule object.
        """
        return self.parent.add_url_rule(self.rule, self.endpoint, view_func,
            provide_automatic_options=None, **self.options)


class _ErrorHandlerAdder:
    """
    Error handler adder returned by ``WebBase.error_handler`` to add an error handler to it as a decorator.
    
    Attributes
    ----------
    error_code : `int`
        Respective http error code for th/e request.
    parent : ``AppBase``
        The parent webapp.
    """
    __slots__ = ('error_code', 'parent',)
    
    def __new__(cls, parent, error_code):
        """
        Creates a new ``_ErrorHandlerAdder`` instance with the given parameters.
        
        Parameters
        ----------
        parent : ``AppBase``
            The parent webapp.
        error_code : `int`
            Respective http error code for th/e request.
        """
        self = object.__new__(cls)
        self.parent = parent
        self.error_code = error_code
        return self
    
    def __call__(self, error_handler_function):
        """
        Adds an `error_handler` with the stored parent ``AppBase`` to it.
        
        Parameters
        ----------
        error_handler_function : `async-callable`
            An async function to call when an http exception is raised.
            
            Should accept following parameters:
            +-------------------+-------------------+---------------------------+
            | Respective name   | Type              | Description               |
            +===================+===================+===========================+
            | exception         | ``AbortRequest``  | The occurred exception.   |
            +-------------------+-------------------+---------------------------+
        
        Returns
        -------
        error_handler_function : `async-callable`
        """
        return self.parent._error_handler(self.error_code, error_handler_function)

def _validate_subdomain(subdomain):
    """
    Validates the given subdomain.
    
    Parameters
    ----------
    subdomain : `None` or `str`
        Subdomain value.
    
    Returns
    -------
    subdomain : `None` or `str`
        The validated subdomain.
    
    Raises
    ------
    TypeError
        If `subdomain` was not given neither as `None` or `str` instance.
    """
    if (subdomain is not None):
        if type(subdomain) is str:
            pass
        elif isinstance(subdomain, str):
            subdomain = str(subdomain)
        else:
            raise TypeError(f'`subdomain` can be as `None` or as `str` instance, got {subdomain.__class__.__name__}.')
        
        if not subdomain:
            subdomain = None
    
    return subdomain

def _validate_parameters(parameters, parameters_name):
    """
    Validates the given subdomain.
    
    Parameters
    ----------
    parameters : `None` or `dict` of (`str`, `Any`) items or (`set`, `tuple`, `list`) of `tuple` (`str`, `Any`)
        Initial parameters to add to the route.
    
    Returns
    -------
    parameters : `None` or `tuple` of `tuple` (`str`, `int`)
        The validated parameters.
    
    Raises
    ------
    TypeError
        - If `parameters` is neither `None`, `dict`, `list`, `set` or `tuple`.
        - If `parameters` contains a non `tuple` element.
    ValueError
        If `parameters` contains an element with length of not `2`.
    """
    if parameters is None:
        parameters_validated = None
    else:
        if isinstance(parameters, dict):
            parameters = list(parameters.items())
        elif type(parameters) is list:
            pass
        elif isinstance(parameters, (list, set, tuple)):
            parameters = list(parameters)
        else:
            raise TypeError(f'`{parameters_name}` should have be given as `dict`, `list`, `set` or `tuple`, got '
                f'{parameters.__class__.__name__}.')
        
        parameters_validated = []
        
        for index, item in enumerate(parameters):
            if not isinstance(item, tuple):
                raise TypeError(f'`{parameters_name}` element `{index}` should have be `tuple` instance, got '
                    f'{item.__class__.__name__}.')
            
            item_length = len(item)
            if item_length != 2:
                raise ValueError(f'`{parameters_name}` element `{index}` length is not the expected `2`, got '
                    f'{item_length}; {item!r}.')
            
            parameter_name, parameter_value = item
            
            if type(parameter_name) is str:
                pass
            elif isinstance(parameter_name, str):
                parameter_name = str(parameter_name)
            else:
                raise TypeError(f'`{parameters_name}` element `{index}`\'s 0th element can be only `str` instance, '
                    f'got {parameter_name.__class__.__name__}.')
            
            parameters_validated.append((parameter_name, parameter_value))
        
        if parameters_validated:
            # Check for dupe parameters.
            parameter_names = set()
            for item in parameters_validated:
                parameter_names.add(item[0])
            
            if len(parameter_names) != len(parameters_validated):
                # There are dupe parameters, remove them
                index = 0
                limit = len(parameters_validated)
                
                while index < limit:
                    item = parameters_validated[index]
                    try:
                        parameter_names.remove(item[0])
                    except KeyError:
                        del parameters_validated[index]
                        limit -= 1
                    else:
                        index += 1
            
            parameters_validated = tuple(parameters_validated)
        else:
            parameters_validated = None
    
    return parameters_validated

def _validate_method(method):
    """
    Validates the given method.
    
    Parameters
    ----------
    method : `None` or `str`
        Request method to validate.
    
    Returns
    -------
    method : `None` or `str`
        The validated request method.
    
    Raises
    ------
    TypeError
        - If `method` is neither `None` nor `str`.
    ValueError
        If `method` is not  a request method.
    """
    if (method is not None):
        if type(method) is str:
            pass
        elif isinstance(method, str):
            method = str(method)
        else:
            raise TypeError(f'`method` can be given as `None` or `str` instance, got {method.__class__.__name__}.')
        
        method = method.upper()
        if method not in METHOD_ALL:
            raise ValueError(f'`method` can be given any of `{METHOD_ALL!r}`, got {method!r}.')
    
    return method

def _validate_methods(methods):
    """
    Validates the given methods.
    
    Parameters
    ----------
    methods : `None` or (`tuple`, `list`, `set`) of `str`
        Request method to validate.
    
    Returns
    -------
    methods : `None` or `list`
        The validated request methods.
    
    Raises
    ------
    TypeError
        - If `methods` is neither `None`, `list`, `set` nor `tuple`.
        - If `methods` contains a non `str` element.
    ValueError
        If `methods` contains a non request method element.
    """
    if (methods is None):
        methods_validated = None
    else:
        methods_validated = []
        
        if not isinstance(methods, (list, tuple, set)):
            raise TypeError(f'`methods` can be either given as `None`, `list`, `tuple`, `set` instance, got '
                f'{methods.__class__.__name__}.')
        
        for index, method in enumerate(methods):
            if type(method) is str:
                pass
            elif isinstance(method, str):
                method = str(method)
            else:
                raise TypeError(f'`methods` element `{index}` should have be given as `None` or `str` instance, got '
                    f'{method.__class__.__name__}.')
            
            method = method.upper()
            if method not in METHOD_ALL:
                raise ValueError(f'`method` element `{index}` should have be given any of `{METHOD_ALL!r}`, got '
                    f'{method!r}.')
            
            methods_validated.append(method)
        
        if not methods_validated:
            methods_validated = None
    
    return methods_validated


def _validate_options(options):
    """
    Validates the given options.
    
    Parameters
    ----------
    options : `dict` of (`str`, `Any`) items.
        Additional options forward to the underlying ``Rule`` object.
    
    Returns
    -------
    request_methods : `set` of `str`
        A set of the validated http methods. If none is given, `'GET'` is auto added to it.
    parameters : `None` or `list` of `tuple` (`str`, `Any`)
        Defaults parameters to the dispatched router.
    subdomain : `None` or `str`
        Whether the respective route should match the specified subdomain.
    
    Raises
    ------
    TypeError
        - If `method` element is neither `None` or `str` instance.
        - Extra option was given.
        - If `methods` is neither `None`, `list`, `tuple` or `set` instance.
        - If `methods` contains a non `str` element.
        - If `defaults` is neither `None`, `dict`, `list`, `set` or `tuple`.
        - If `defaults` contains a non `tuple` element.
        - If 0th element of an element of `defaults` is not `str` instance.
        - If `subdomain` was not given neither as `None` or `str` instance.
    ValueError
        - If `method` is not an http request method.
        - If `methods` contains a non http request method element.
        - If `defaults` contains an element with length of not `2`.
    """
    request_methods = None
    
    method = options.pop('method', None)
    method = _validate_method(method)
    if (method is not None):
        if (request_methods is None):
            request_methods = set()
        request_methods.add(method)
    
    methods = options.pop('methods', None)
    if (methods is not None):
        if (request_methods is None):
            request_methods = set()
        request_methods.union(methods)
    
    parameters = options.pop('defaults', None)
    parameters = _validate_parameters(parameters, 'defaults')
    
    subdomain = options.pop('subdomain', None)
    subdomain = _validate_subdomain(subdomain)
    
    if options:
        raise TypeError(f'`options` contains unused parameters: {options!r}.')
    
    if request_methods:
        request_methods.add(METHOD_GET)
    
    return request_methods, parameters, subdomain

def _validate_import_name(import_name):
    """
    Validates the given `import_name` value.
    
    Parameters
    ----------
    import_name : `str`
        The import name's value.
    
    Returns
    -------
    import_name : `str`
        The validated import name.
    
    Raises
    ------
    TypeError
        If `import_name` was not given as `str` instance.
    ValueError
        If `import_name` is an empty string.
    """
    if type(import_name) is str:
        pass
    elif isinstance(import_name, str):
        import_name = str(import_name)
    else:
        raise TypeError(f'`import_name` can be given as `str` instance, got {import_name.__class__.__name__}.')
    
    if not import_name:
        raise ValueError(f'`import_name` cannot be given as empty string.')
    
    return import_name

def _validate_template_folder(template_folder):
    """
    Validates the given `template_folder` value.
    
    Parameters
    ----------
    template_folder : `None` or `str`
        The template folder's value.
    
    Returns
    -------
    template_folder : `None` or `str`
        The template folder's validated value.
    
    Raises
    ------
    TypeError
        If `template_folder` was not given neither as `None` or `str` instance.
    """
    if (template_folder is not None):
        if type(template_folder) is str:
            pass
        elif isinstance(template_folder, str):
            template_folder = str(template_folder)
        else:
            raise TypeError(f'`template_folder` can be given as `str` instance, got '
                f'{template_folder.__class__.__name__}.')
        
        if not template_folder:
            template_folder = None
    
    return template_folder

def _validate_root_path(root_path, import_name):
    """
    Validates the given `root_path` value. If `root_oath` is `None`, will try to detect it from `import_name`.
    
    Parameters
    ----------
    root_path : `None` or `str`
        The given root path.
    
    Returns
    -------
    root_path : `None` or `str`
        The validated root path.
    
    Raises
    ------
    ImportError
        If `route_path` refers to a module, but error occurred meanwhile importing it.
    TypeError
        If `root_path` was not given neither as `None` or `str` instance.
    ValueError
        If `root_path` was given as empty string.
    """
    if root_path is None:
        try:
            maybe_module = sys.modules[import_name]
        except KeyError:
            pass
        else:
            maybe_file_name = getattr(maybe_module, '__file__')
            if (maybe_file_name is not None):
                return os.path.dirname(os.path.abspath(maybe_file_name))
        
        # Find importable file if applicable.
        try:
            spec = find_spec(import_name)
        except BaseException as err:
            raise ImportError(f'Exception occurred while finding loader for {import_name!r} ({type(err)}{err})') \
                from err
        
        if spec is None:
            loader = None
        else:
            loader = spec.loader
        
        # Not found, probably the main file?
        if (loader is None) or (import_name == '__main__'):
            return os.getcwd()
       
        # Get file name from loader.
        path = loader.get_filename(import_name)
        return os.path.dirname(os.path.abspath(path))
        
    else:
        if type(root_path) is str:
            pass
        elif isinstance(root_path, str):
            root_path = str(root_path)
        else:
            raise TypeError(f'`root_path` can be given as `str` instance, got {root_path.__class__.__name__}.')
        
        if not root_path:
            raise ValueError(f'`root_path` cannot be given as empty string.')
    
    return root_path

def _validate_static_folder(static_folder):
    """
    Validates the given static folder value.
    
    Parameters
    ----------
    static_folder : `None` or `str`
        Static folder value to validate.
    
    Returns
    -------
    static_folder : `None` or `str`
        The validated static folder value.
    
    Raises
    ------
    TypeError
        If `static_folder` was not given neither as `None` nor `str` instance.
    ValueError
        If `static_folder` was given as empty string.
    """
    if (static_folder is not None):
        if type(static_folder) is str:
            pass
        elif isinstance(static_folder, str):
            static_folder = str(static_folder)
        else:
            raise TypeError(f'`static_folder` can be given as `str` instance, got {static_folder.__class__.__name__}.')
        
        if not static_folder:
            raise ValueError(f'`static_folder` cannot be given as empty string.')
    
    return static_folder

def _validate_static_url_path(static_url_path):
    """
    Validates the given static folder value.
    
    Parameters
    ----------
    static_url_path : `str`
        Static url path value to validate.
    
    Returns
    -------
    static_url_path : `None` or `str`
        The validated static url path value.
    
    Raises
    ------
    TypeError
        If `static_url_path` was not given either as `None` or `str` instance.
    """
    if (static_url_path is not None):
        if type(static_url_path) is str:
            pass
        elif isinstance(static_url_path, str):
            static_url_path = str(static_url_path)
        else:
            raise TypeError(f'`static_url_path` can be given as `str` instance, got '
                f'{static_url_path.__class__.__name__}.')
    
    return static_url_path

def _validate_url_prefix(url_prefix):
    """
    Validates the given url prefix converting it into url route parts.
    
    Parameters
    ---------
    url_prefix : `None` or `str`
        Url prefix for a blueprint.
    
    Returns
    -------
    url_prefix_processed : `None` or `tuple` of `tuple` (`str`, `int`)
        The processed url prefix.
    
    Raises
    ------
    TypeError
        - If `url_prefix` was neither given as `None` or as `str` instance.
        - If `url_prefix` contains a `path` rule part.
    """
    if url_prefix is None:
        url_prefix_processed = None
    else:
        if type(url_prefix) is str:
            pass
        elif isinstance(url_prefix, str):
            url_prefix = str(url_prefix)
        else:
            raise TypeError(f'`url_prefix` can be given as `str` instance, got {url_prefix.__class__.__name__}.')
        
        url_prefix_processed = tuple(maybe_typed_rule_part(rule_part) for rule_part in URL(url_prefix).path)
        if url_prefix_processed:
            for parameter_type, parameter_name in url_prefix_processed:
                if parameter_type == PARAMETER_TYPE_PATH:
                    raise TypeError(f'Only last rule part can be `path` type, got {url_prefix!r}.')
        else:
            url_prefix_processed = None
    
    return url_prefix_processed

DUMMY_RULE_PART = (PARAMETER_TYPE_STATIC, '/')

def _merge_url_rule(rule_before, rule_after):
    """
    Merges two url rule parts.
    
    Parameters
    ----------
    rule_before : `None` or `tuple` of `tuple` (`int`, `str`)
        First url part if any to join `rule_after` to.
    rule_after : `None` or `tuple` of `tuple` (`int`, `str`)
        Second url part what's start is extended by `rule_before`.
    
    Returns
    -------
    merged_rule : `None` or `tuple` of `tuple` (`int`, `str`)
        The merged rule.
    """
    if rule_before is None:
        return rule_after
    
    if rule_after is None:
        return rule_before
    
    if rule_after[0] == DUMMY_RULE_PART:
        rule_after = rule_after[1:]
    
    return (*rule_before, *rule_after)

def _merge_parameters(primary_parameters, secondary_parameters):
    """
    Merges two default parameters list,
    
    Parameters
    ----------
    primary_parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        Priority parameters, which element's wont be removed.
    secondary_parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        Secondary parameters, which will be merged to `primary_parameters`.
    
    Returns
    -------
    merged_parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        The merged parameters.
    """
    if primary_parameters is None:
        return secondary_parameters
    
    if secondary_parameters is None:
        return primary_parameters
    
    extend_parameters = []
    for secondary_item in secondary_parameters:
        parameter_name = secondary_item[0]
        for priority_item in primary_parameters:
            if priority_item[0] == parameter_name:
                break
        else:
            extend_parameters.append(secondary_item)
    
    if not extend_parameters:
        return primary_parameters
    
    return (*primary_parameters, *extend_parameters)

class RuleFolder:
    """
    Rule folder, which contains more rules enabling adding them at once.
    
    Attributes
    ----------
    endpoint : `str`
        The endpoint's internal name.
    keyword_parameter_names : `None` or `tuple` of `str`
        Keyword only parameter names accepted by `view_func`.
    kwargs_parameter_supported : `bool`
        Whether `view_func` accepts `**kwargs` parameter.
    positional_parameter_names : `None` or `tuple` of `str`
        Positional only parameter names accepted by `view_func`.
    rules : `list` of ``Rule``
        Rules added.
    view_func : `async-callable`
        The function to call when serving a request to the provided endpoint.
    """
    __slots__ = ('endpoint', 'keyword_parameter_names', 'kwargs_parameter_supported', 'positional_parameter_names',
        'rules', 'view_func')
    def __init__(self, view_func, positional_parameter_names, keyword_parameter_names, kwargs_parameter_supported,
            endpoint):
        """
        Creates a new ``RuleFolder`` instance.
        
        Parameters
        ----------
        view_func : `async-callable`
            The function to call when serving a request to the provided endpoint.
        positional_parameter_names : `None` or `tuple` of `str`
            Positional only parameter names accepted by `view_func`.
        keyword_parameter_names : `None` or `tuple` of `str`
            Keyword only parameter names accepted by `view_func`.
        kwargs_parameter_supported : `bool`
            Whether `view_func` accepts `**kwargs` parameter.
        endpoint : `str`
            The endpoint's internal name.
        """
        self.view_func = view_func
        self.endpoint = endpoint
        self.rules = []
        self.positional_parameter_names = positional_parameter_names
        self.keyword_parameter_names = keyword_parameter_names
        self.kwargs_parameter_supported = kwargs_parameter_supported
    
    @classmethod
    def from_rule(cls, rule):
        """
        Creates a rule folder from a rule.
        
        Parameters
        ----------
        rule : ``Rule``
            The rule to create the folder from.

        Returns
        -------
        self : ``RuleFolder``
        """
        self = object.__new__(cls)
        
        self.view_func = rule.view_func
        self.endpoint = rule.endpoint
        self.rules = [rule]
        self.positional_parameter_names = rule.positional_parameter_names
        self.keyword_parameter_names = rule.keyword_parameter_names
        self.kwargs_parameter_supported = rule.kwargs_parameter_supported
        
        return self
    
    def add_rule(self, rule, request_methods, parameters, subdomain):
        """
        Adds a rule to the rule folder.
        
        Parameters
        ----------
        rule : `tuple` of `tuple` (`int`, `str`)
            The url rule to register.
        request_methods : `None` or `set` of `str`
            Request methods to call `view_func` when received.
        parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
            Default parameters to pass to the `view_func`.
        subdomain : `None` or `str`
            Whether the route should match the specified subdomain.
        """
        self.rules.append(Rule(rule, self.view_func, self.positional_parameter_names, self.keyword_parameter_names,
            self.kwargs_parameter_supported, self.endpoint, request_methods, parameters, subdomain))
    
    def copy(self):
        """
        Copies the rule folder.
        
        Returns
        -------
        new : ``RuleFolder``
        """
        new = object.__new__(type(self))
        
        new.rules = [rule.copy() for rule in self.rules]
        new.view_func = self.view_func
        new.endpoint = self.endpoint
        new.positional_parameter_names = self.positional_parameter_names
        new.keyword_parameter_names = self.keyword_parameter_names
        new.kwargs_parameter_supported = self.kwargs_parameter_supported
        
        return new
    
    def set_subdomain(self, subdomain):
        """
        Sets subdomain to each rule of the rule folder.
        
        Parameters
        ----------
        subdomain : `None` or `str`
            Subdomain, what the rule of the blueprint gonna match.
        """
        for rule in self.rules:
            rule.set_subdomain(subdomain)
        
    def set_parameters(self, parameters):
        """
        Sets parameters to each rule of the rule folder.
        
        Parameters
        ----------
        parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        """
        for rule in self.rules:
            rule.set_parameters(parameters)
    
    def set_rule_prefix(self, rule):
        """
        Extends the rule parts of the rules of the rule folder.
        
        Parameters
        ----------
        rule : `None` or `tuple` of `tuple` (`str`, `int`)
            The rule parts to extend the ``Rule``'s with.
        """
        for rule in self.rules:
            rule.set_rule_prefix(rule)
    
    def set_application(self, application):
        """
        Sets the rule folder's rules' application inside of the rule folder
        
        Parameters
        ----------
        application : ``WebApp``
        """
        for rule in self.rules:
            rule.set_application(application)
    
    def set_blueprint_state_stack(self, blueprint_state_stack):
        """
        Sets the rule folder's rules' blueprint stack.
        
        Parameters
        ----------
        blueprint_state_stack : `None` or `tuple` of ``BlueprintState``
        """
        for rule in self.rules:
            rule.set_blueprint_state_stack(blueprint_state_stack)
    
    def __repr__(self):
        """Returns the rule folder's representation."""
        return f'<{self.__class__.__name__} rules={self.rules!r}>'
    
    def iter_rules(self):
        """
        Iterates over the rules of the rule folder.
        
        This method is a generator.
        
        Yields
        ------
        rule :``Rule``
        """
        for rule in self.rules:
            yield from rule.iter_rules()


class Rule:
    """
    A registered rule.
    
    Attributes
    ----------
    application : `None` or ``WebApp``
        The parent application.
        
        Only added when the rule is registered.
    blueprint_state_stack : `None` or `tuple` of ``Blueprint``
        Blueprint stack for the rule.
        
        Only added when the rule is registered.
    endpoint : `str`
        The endpoint's internal name.
    keyword_parameter_names : `None` or `tuple` of `str`
        Keyword only parameter names accepted by `view_func`.
    kwargs_parameter_supported : `bool`
        Whether `view_func` accepts `**kwargs` parameter.
    parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        Default parameters to pass to the `view_func`.
    positional_parameter_names : `None` or `tuple` of `str`
        Positional only parameter names accepted by `view_func`.
    request_methods : `None` or `set` of `str`
        Request methods to call `view_func` when received.
    rule : `tuple` or `tuple` of (`int`, `str`)
        The url's path part.
    subdomain : `None` or `str`
        Whether the route should match the specified subdomain.
    view_func : `async-callable`
        The function to call when serving a request to the provided endpoint.
    """
    __slots__ = ('application', 'blueprint_state_stack', 'endpoint', 'keyword_parameter_names',
        'kwargs_parameter_supported', 'parameters', 'positional_parameter_names', 'request_methods', 'rule',
        'subdomain', 'view_func')
    
    def __init__(self, rule, view_func, positional_parameter_names, keyword_parameter_names,
            kwargs_parameter_supported, endpoint, request_methods, parameters, subdomain):
        """
        Creates a new ``Rule`` instance.
        
        Parameters
        ----------
        rule : `tuple` of `tuple` (`int`, `str`)
            The url rule to register.
        view_func : `async-callable`
            The function to call when serving a request to the provided endpoint.
        positional_parameter_names : `None` or `tuple` of `str`
            Positional only parameter names accepted by `view_func`.
        keyword_parameter_names : `None` or `tuple` of `str`
            Keyword only parameter names accepted by `view_func`.
        kwargs_parameter_supported : `bool`
            Whether `view_func` accepts `**kwargs` parameter.
        endpoint : `str`
            The endpoint's internal name.
        request_methods : `None` or `set` of `str`
            Request methods to call `view_func` when received.
        parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
            Default parameters to pass to the `view_func`.
        subdomain : `None` or `str`
            Whether the route should match the specified subdomain.
        """
        self.rule = rule
        self.view_func = view_func
        self.endpoint = endpoint
        self.request_methods = request_methods
        self.parameters = parameters
        self.subdomain = subdomain
        self.application = None
        self.blueprint_state_stack = None
        self.positional_parameter_names = positional_parameter_names
        self.keyword_parameter_names = keyword_parameter_names
        self.kwargs_parameter_supported = kwargs_parameter_supported
    
    def copy(self):
        """
        Copies the rule.
        
        Returns
        -------
        new : ``Rule``
        """
        new = object.__new__(type(self))
        
        new.endpoint = self.endpoint
        new.parameters = self.parameters
        new.request_methods = self.request_methods
        new.rule = self.rule
        new.subdomain = self.subdomain
        new.view_func = self.view_func
        new.positional_parameter_names = self.positional_parameter_names
        new.keyword_parameter_names = self.keyword_parameter_names
        new.kwargs_parameter_supported = self.kwargs_parameter_supported
        
        return new
    
    def validate_parameters(self):
        """
        Validates the parameters of the ``Rule``. Raises `RuntimeError` if the rule's ``.view_func`` might not receive
        a parameter in runtime.
        
        Raises
        ------
        RuntimeError
            If ``.view_func`` might not receive a parameter in runtime.
        """
        excepted_parameter_names = set()
        
        positional_parameter_names = self.positional_parameter_names
        if (positional_parameter_names is not None):
            excepted_parameter_names.update(positional_parameter_names)
        
        keyword_parameter_names = self.keyword_parameter_names
        if (keyword_parameter_names is not None):
            excepted_parameter_names.update(keyword_parameter_names)
        
        parameters = self.parameters
        if (parameters is not None):
            for parameter_name, parameter_value in parameters:
                excepted_parameter_names.discard(parameter_name)
        
        for rule_part_type, rule_part_name in self.rule:
            if rule_part_type != PARAMETER_TYPE_STATIC:
                excepted_parameter_names.discard(rule_part_name)
        
        if excepted_parameter_names:
            raise RuntimeError(f'{self.__class__.__name__}: {self!r} might be called without all of it\'s expected '
                f'parameters. The following might be missing: {", ".join(excepted_parameter_names)}')
    
    def set_subdomain(self, subdomain):
        """
        Sets subdomain to the rule if it has non set yet.
        
        Parameters
        ----------
        subdomain : `None` or `str`
            Subdomain, what the rule of the blueprint gonna match.
        """
        if (subdomain is not None) and (self.subdomain is None):
            self.subdomain = subdomain

    def set_parameters(self, parameters):
        """
        Sets parameters to the rule.
        
        Parameters
        ----------
        parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        """
        self.parameters = _merge_parameters(self.parameters, parameters)
    
    def set_rule_prefix(self, rule):
        """
        Extends the rule parts of the rule.
        
        Parameters
        ----------
        rule : `None` or `tuple` of `tuple` (`str`, `int`)
            The rule parts to extend the ``Rule``'s with.
        """
        self.rule = _merge_url_rule(rule, self.rule)
    
    def set_application(self, application):
        """
        Sets the rule's application.
        
        Parameters
        ----------
        application : ``WebApp``
        """
        self.application = application
    
    def set_blueprint_state_stack(self, blueprint_state_stack):
        """
        Sets the rule's blueprint stack.
        
        Parameters
        ----------
        blueprint_state_stack : `None` or `tuple` of ``BlueprintState``
        """
        self.blueprint_state_stack = blueprint_state_stack
    
    def __repr__(self):
        """Returns the rule's representation."""
        result = ['<', self.__class__.__name__, ' endpoint=', repr(self.endpoint)]
        parameters = self.parameters
        if (parameters is not None):
            result.append(', parameters=')
            result.append(repr(parameters))
        
        request_methods = self.request_methods
        if request_methods is None:
            request_method_repr = '*'
        else:
            request_method_repr_parts = ['[']
            for request_method in request_methods:
                request_method_repr_parts.append(request_method)
                request_method_repr_parts.append(', ')
            
            request_method_repr_parts[-1] = ']'
            
            request_method_repr = ''.join(request_method_repr_parts)
        
        result.append(', request_methods=')
        result.append(request_method_repr)
        
        rule = self.rule
        if (rule is not None):
            result.append(', rule=')
            result.append(repr(rule))
        
        subdomain = self.subdomain
        if (subdomain is not None):
            result.append(', subdomain=')
            result.append(repr(subdomain))
        
        result.append(', view_func=')
        result.append(repr(self.view_func))
        
        result.append('>')
        
        return ''.join(result)
    
    def iter_rules(self):
        """
        Iterates over the rules of ``Rule``.
        
        A ``Rule`` is a standalone rule, so just yield itself.
        
        This method is a generator.
        
        Yields
        ------
        rule : ``Rule``
        """
        yield self

    @property
    def before_request_functions(self):
        """
        Returns the functions which should run before a request is started.
        
        Returns
        -------
        before_request_functions : `None` or `list` of `async-callable`
        """
        before_request_functions = None
        blueprint_state_stack = self.blueprint_state_stack
        if (blueprint_state_stack is not None):
            for blueprint in reversed(blueprint_state_stack):
                before_request_functions_chunk = blueprint.before_request_functions
                if (before_request_functions_chunk is not None):
                    if before_request_functions is None:
                        before_request_functions = []
                    
                    before_request_functions.extend(before_request_functions_chunk)
        
        application = self.application
        if (application is not None):
            before_request_functions_chunk = application.before_request_functions
            if (before_request_functions_chunk is not None):
                if before_request_functions is None:
                    before_request_functions = []
                
                before_request_functions.extend(before_request_functions_chunk)
        
        return before_request_functions
    
    @property
    def after_request_functions(self):
        """
        Functions which are ensured to modify the response object.
         
        Returns
        -------
        after_request_functions : `None` or `list` of `async-callable`
        """
        after_request_functions = None
        blueprint_state_stack = self.blueprint_state_stack
        if (blueprint_state_stack is not None):
            for blueprint in reversed(blueprint_state_stack):
                after_request_functions_chunk = blueprint.after_request_functions
                if (after_request_functions_chunk is not None):
                    if (after_request_functions is None):
                        after_request_functions = []
                    
                    after_request_functions.extend(after_request_functions_chunk)
        
        application = self.application
        if (application is not None):
            after_request_functions_chunk = application.after_request_functions
            if (after_request_functions_chunk is not None):
                if (after_request_functions is None):
                    after_request_functions = []
                
                after_request_functions.extend(after_request_functions_chunk)
        
        return after_request_functions
    
    @property
    def teardown_request_functions(self):
        """
        Functions which should run after a request's view func is done, even if exception occurs.
        
        Returns
        -------
        teardown_request_functions : `None` or `list` of `async-callable`
        """
        teardown_request_functions = None
        blueprint_state_stack = self.blueprint_state_stack
        if (blueprint_state_stack is not None):
            for blueprint in reversed(blueprint_state_stack):
                teardown_request_functions_chunk = blueprint.teardown_request_functions
                if (teardown_request_functions_chunk is not None):
                    if teardown_request_functions is None:
                        teardown_request_functions = []
                    
                    teardown_request_functions.extend(teardown_request_functions_chunk)
        
        application = self.application
        if (application is None):
            teardown_request_functions_chunk = application.teardown_request_functions
            if (teardown_request_functions_chunk is not None):
                if teardown_request_functions is None:
                    teardown_request_functions = []
                
                teardown_request_functions.extend(teardown_request_functions_chunk)
        
        return teardown_request_functions


ROUTE_METHOD_NOT_ALLOWED = Rule((), _handler_method_not_allowed, None, None, False, 'method_not_allowed', None, None,
    None)
ROUTE_NOT_FOUND_NOT_ALLOWED = Rule((), _handler_not_found, None, None, False, 'not found', None, None, None)


def _analyze_handler(handler, handler_name, expected_parameter_count):
    """
    Analyzes a handler.
    
    Parameters
    ----------
    handler : `async-callable`
        The handler to analyze.
    handler_name : `str`
        The handler's name.
    expected_parameter_count : `int`
        The parameter amount what the handler
    
    Raises
    ------
    TypeError
        - If `handler` is not `callable`.
        - If `handler` is not `async-callable`.
        - If `handler` accepts bad amount of parameters.
    """
    analyzed = CallableAnalyzer(handler)
    if not analyzed.is_async():
        raise TypeError(f'`{handler_name}` can be given as `async-callable`, got {analyzed.__class__.__name__}; '
            f'{analyzed!r}.')
    
    non_reserved_positional_parameter_count = analyzed.get_non_reserved_positional_parameter_count()
    if non_reserved_positional_parameter_count != expected_parameter_count:
        raise TypeError(f'`{handler_name}` should accept `{expected_parameter_count}` non reserved positional '
            f'parameters, meanwhile it expects {non_reserved_positional_parameter_count}.')
    
    if analyzed.accepts_args():
        raise TypeError(f'`{handler_name}` should accept not expect args, meanwhile it does.')
    
    if analyzed.accepts_kwargs():
        raise TypeError(f'`{handler_name}` should accept not expect kwargs, meanwhile it does.')
    
    non_default_keyword_only_parameter_count = analyzed.get_non_default_keyword_only_parameter_count()
    if non_default_keyword_only_parameter_count:
        raise TypeError(f'`{handler_name}` should accept `0` keyword only parameters, meanwhile it expects '
            f'{non_default_keyword_only_parameter_count}.')


class AppBase:
    """
    Base class for ``Blueprint``-s and for ``WebApp``-s.
    
    Attributes
    ----------
    after_request_functions : `None` or `list` of `async-callable`
        Functions which are ensured to modify the response object.
        
        To register an after request function use the ``.after_request`` decorator.
        
        The following parameters are passed to each after request function:
        +-------------------+-----------------------+-----------------------+
        | Respective name   | Type                  | Description           |
        +===================+=======================+=======================+
        | response          | ``ServerResponse``    | The response object.  |
        +-------------------+-----------------------+-----------------------+
    
    before_request_functions : `None` or `list` of `async-callable`
        Functions which should run before a request' view-func  is started.
        
        To register a before request function use the ``.before_request`` decorator.
        
        If any before request processor returns a non `None` value, then the request processing will stop and that
        return will be sent as response.
        
        No parameters are passed to before request functions.
    
    blueprints : `None` or `dict` of (`str`, `tuple` (``BlueprintState``, ``Blueprint``)
        Registered blueprints to the app.
    
    error_handler_functions : `None` or `dict` of (`int`, `async-callable`) items
        Error handlers which run when an http exception is raised from a view.
        
        To register an error handler use the ``.error_handler`` decorator.
    
        The following parameters are passed to each error handler:
        +-------------------+-------------------+---------------------------+
        | Respective name   | Type              | Description               |
        +===================+===================+===========================+
        | exception         | ``AbortRequest``  | The occurred exception.   |
        +-------------------+-------------------+---------------------------+
    
    import_name : `str`
        The name of the package or module that this app belongs to.
    root_path : `str`
        Absolute path to the package on the filesystem.
    rules : `dict` of (`str`, `Any`)
        The added rules to the application or blueprint. The keys are their endpoint name.
    static_folder : `None` or `str`
        Absolute path to the static file's folder.
    static_url_path : `None` or `str`
        Url path to static files. By defaults relates to `static_folder`.
    
    teardown_request_functions : `None` or `list` of `async-callable`
        Functions which should run after a request's view func is done, even if exception occurs.
        
        To register a teardown request function use the ``.teardown_request`` decorator.
        
        The following parameters are passed to each teardown request:
        +-------------------+---------------------------+-----------------------------------+
        | Respective name   | Type                      | Description                       |
        +===================+===========================+===================================+
        | exception         | `None` or `BaseException` | The occurred exception if any.    |
        +-------------------+---------------------------+-----------------------------------+
        
    template_context_processors : `None` or `list of `async-callable`
        Functions which are called to populate template context. Each should return a dictionary with what the template
        dictionary is updated with.
        
        To register template context processor, use the ``.context_processor`` decorator.
        
        No parameters are passed to template context processors.
    
    template_folder : `None` or `str`
        The folder from where the templates should be loaded from.
    
    url_default_functions : `None` or `list` of `async-callable`
        Keyword parameter preprocessors for ``url_for``.
        
        To register them use the ``.url_defaults`` method.
        
        The following parameters are passed to the url default functions:
        +-------------------+---------------------------+-------------------------------------------------------+
        | Respective name   | type                      | Description                                           |
        +===================+===========================+=======================================================+
        | endpoint          | `None` or `str`           | The endpoint what matched the request url.            |
        +-------------------+---------------------------+-------------------------------------------------------+
        | kwargs            | `dict` of (`str`, `Any`)  | Additional keyword parameters passed to ``url_for``.  |
        +-------------------+---------------------------+-------------------------------------------------------+
    
    url_value_preprocessors : `None` or `list` of `async-callable`
        Preprocessors which can modify the parameters matched from the url.
        
        To registered them use the ``.url_value_preprocessor`` decorator.
        
        The following parameters are passed to each url value preprocessor:
        +-------------------+---------------------------+-----------------------------------------------+
        | Respective name   | Type                      | Description                                   |
        +===================+===========================+===============================================+
        | endpoint          | `None` or `str`           | The endpoint what matched the request url.    |
        |                   |                           | Set as `None` if exception occurred.          |
        +-------------------+---------------------------+-----------------------------------------------+
        | parameters        | `dict` of (`str`, `Any`)  | Parameters parsed from the request url.       |
        +-------------------+---------------------------+-----------------------------------------------+
    """
    __slots__ = ('after_request_functions', 'before_request_functions', 'blueprints', 'error_handler_functions',
        'import_name', 'root_path', 'rules', 'static_folder', 'static_url_path', 'teardown_request_functions',
        'template_context_processors', 'template_folder', 'url_default_functions', 'url_value_preprocessors',)
    
    def __new__(cls, import_name, template_folder, root_path, static_folder, static_url_path):
        """
        Parameters
        ----------
        import_name : `str`
            The name of the package or module that this app belongs to.
        template_folder : `None` or `str`
            The folder from where the templates should be loaded from.
        root_path : `None` or `str`
            Absolute path to the package on the filesystem.
        static_folder : `None` or `str`
            Path on top of the application route path for static files, which can be accessed trough the
            `static_url_path`.
        static_url_path : `None` or `str`
            Url path to static files. Defaults to `static_folder`'s value.
        
        Raises
        ------
        ImportError
            Exception occurred meanwhile finding route path from import name.
        TypeError
            - If `import_name` was not given as `st` instance.
            - If `template_folder` was not given neither as `None` or `str` instance.
            - If `root_path` was not given neither as `None` or `str` instance.
            - If `static_folder` was not given neither as `None` nor `str` instance.
            - If `static_url_path` was not given either as `None` or `str` instance.
        ValueError
            - If `import_name` was given as an empty string.
            - If `root_path` was given as an empty string.
        """
        import_name = _validate_import_name(import_name)
        template_folder = _validate_template_folder(template_folder)
        static_folder = _validate_static_folder(static_folder)
        static_url_path = _validate_static_url_path(static_url_path)
        
        root_path = _validate_root_path(root_path, import_name)
        if (static_url_path is None) and (static_folder is not None):
            if os.path.isabs(static_folder):
                static_folder_head, static_folder_tail = ntpath.split(static_folder)
                if not static_folder_tail:
                    static_folder_tail = ntpath.basename(static_folder_head)
                
                static_url_path = static_folder_tail
            else:
                static_url_path = '/'.join(os.path.normpath(static_folder).split(os.path.sep))
        
        if (template_folder is not None) and (not os.path.isabs(template_folder)):
            template_folder = os.path.join(root_path, template_folder)
            
        if (static_folder is not None) and (not os.path.isabs(static_folder)):
            static_folder = os.path.join(root_path, static_folder)
        
        self = object.__new__(cls)
        self.import_name = import_name
        self.template_folder = template_folder
        self.root_path = root_path
        self.static_folder = static_folder
        self.static_url_path = static_url_path
        
        self.rules = {}
        self.blueprints = None
        
        self.error_handler_functions = None
        self.before_request_functions = None
        self.after_request_functions = None
        self.teardown_request_functions = None
        self.template_context_processors = None
        self.url_value_preprocessors = None
        self.url_default_functions = None
        
        return self
    
    def route(self, rule, endpoint=None, **options):
        """
        A decorator, what can be used to registers rules. Does the same thing as ``.add_url_rule``, but it is intended
        to be used as a decorator.
        
        Parameters
        ----------
        rule : `str`
            The url rule as string.
        endpoint  : `None` or `str`, Optional
            The internal endpoint of the url. Defaults to the name of the added function.
        **options : keyword parameters
            Additional options to be forward to the underlying ``Rule`` object.
        
        Returns
        -------
        route_adder : ``_RouteAdder``
        """
        return _RouteAdder(self, rule, endpoint, options)
    
    def add_url_rule(self, rule, *args, provide_automatic_options=None, **options):
        """
        Method to add a route to the application.
        
        If you want to subclass the type, subclassing this method is enough, because ``.route`` calls ``.add_url_rule``.
        
        Parameters
        ----------
        rule : `str`
            The url rule as string.
        *args : parameters
            `endpoint` and `view_func` depending 1 or 2 parameters were given.
        endpoint  : `None` or `str`, Optional
            The internal endpoint of the url. Defaults to the name of the added function.
        view_func : `async-callable`
            The function to call when serving a request to the provided endpoint.
        provide_automatic_options : `None` or `bool`, Optional (Keyword only)
            Controls whether `options` should be handled manually.
        **options : keyword parameters
            Additional options to be forward to the underlying ``Rule`` object.
        
        Returns
        -------
        rule : ``Rule``
            The added rule object.
        
        Raises
        ------
        TypeError
            - If `provide_automatic_options` was not given neither as `None` or `bool`.
            - If `view_func` was not given as `async-callable`
            - If `rule` was not given as `str` instance.
            - If `endpoint` was not given as `str` instance.
            - If `view_func` parameter is missing from `*args`.
            - Extra positional only parameter.
            - If `method` element is neither `None` or `str` instance.
            - Extra option was given.
            - If `methods` is neither `None`, `list`, `tuple` or `set` instance.
            - If `methods` contains a non `str` element.
            - If `defaults` is neither `None`, `dict`, `list`, `set` or `tuple`.
            - If `defaults` contains a non `tuple` element.
            - If 0th element of an element of `defaults` is not `str` instance.
            - If `subdomain` was not given neither as `None` or `str` instance.
            - If `view_func` is not ``Rule``, ``RuleFolder``, neither `async-callable` instance.
        ValueError
            - If `method` is not an http request method.
            - If `methods` contains a non http request method element.
            - If `defaults` contains an element with length of not `2`.
        """
        args_length = len(args)
        if args_length == 0:
            raise TypeError(f'`view_func` positional only parameter is missing.')
        elif args_length == 1:
            endpoint = None
            view_func = args[0]
        elif args_length == 2:
            endpoint = args[0]
            view_func = args[1]
        else:
            raise TypeError(f'`Extra positional parameters: {args[2:]!r}.')
        
        if view_func is None:
            raise TypeError(f'`view_func` can be `async-callable`, `{Rule.__name__}` or `{RuleFolder.__name__}` '
                f'instance, got `None`.')
        
        if isinstance(view_func, (Rule, RuleFolder)):
            real_func = view_func.view_func
            analyzed = CallableAnalyzer(real_func)
            
            view_func_positional_parameter_names = view_func.positional_parameter_names
            view_func_keyword_parameter_names = view_func.keyword_parameter_names
            view_func_kwargs_parameter_supported = view_func.kwargs_parameter_supported
        else:
            real_func = view_func
            analyzed = CallableAnalyzer(view_func)
            if not analyzed.is_async():
                raise TypeError(f'`view_func` can be given as `async-callable`, got {view_func.__class__.__name__}; '
                    f'{view_func!r}.')
            
            if analyzed.accepts_args():
                raise TypeError(f'`view_func` should not accept `*args` meanwhile it does, got {view_func!r}.')
            
            view_func_positional_parameter_names = None
            view_func_keyword_parameter_names = None
            view_func_kwargs_parameter_supported = analyzed.accepts_kwargs()
            
            for parameter in analyzed.parameters:
                if parameter.reserved:
                    continue
                
                if parameter.is_kwargs():
                    continue
                
                if parameter.is_positional():
                    if view_func_positional_parameter_names is None:
                        view_func_positional_parameter_names = []
                    view_func_positional_parameter_names.append(parameter.name)
                else:
                    if view_func_keyword_parameter_names is None:
                        view_func_keyword_parameter_names = []
                    view_func_keyword_parameter_names.append(parameter.name)
            
            if (view_func_positional_parameter_names is not None):
                view_func_positional_parameter_names = tuple(view_func_positional_parameter_names)
            
            if (view_func_keyword_parameter_names is not None):
                view_func_keyword_parameter_names = tuple(view_func_keyword_parameter_names)
        
        view_func_parameters = None
        for parameter in analyzed.parameters:
            if parameter.has_default:
                if view_func_parameters is None:
                    view_func_parameters = []
                
                view_func_parameters.append((parameter.name, parameter.default))
        
        if (view_func_parameters is not None):
            view_func_parameters = tuple(view_func_parameters)
        
        for parameter_name in ('method', 'methods', 'defaults'):
            if options.get(parameter_name, None) is None:
                parameter_value = getattr(endpoint, parameter_name, None)
                if (parameter_value is not None):
                    options[parameter_name] = parameter_value
        
        if provide_automatic_options is None:
            provide_automatic_options = getattr(view_func, 'provide_automatic_options', None)
        
        if provide_automatic_options is None:
            provide_automatic_options = True
        else:
            if not isinstance(provide_automatic_options, bool):
                raise TypeError(f'`provide_automatic_options` can be given either as `None` or `bool` instance, got '
                    f'{provide_automatic_options.__class__.__name__}.`')
        
        if endpoint is None:
            if isinstance(view_func, (Rule, RuleFolder)):
                endpoint = view_func.endpoint
            else:
                try:
                    endpoint = view_func.__name__
                except AttributeError:
                    endpoint = view_func.__class__.__name__
        
        if type(endpoint) is str:
            pass
        elif isinstance(endpoint, str):
            endpoint = str(endpoint)
        else:
            raise TypeError(f'`endpoint` can be given as `str` instance, got {endpoint.__class__.__name__}.')
        
        if type(rule) is str:
            pass
        elif isinstance(rule, str):
            rule = str(rule)
        else:
            raise TypeError(f'`rule` can be given as `str` instance, got {rule.__class__.__name__}.')
        
        rule_processed = tuple(maybe_typed_rule_part(rule_part) for rule_part in URL(rule).parts)
        if rule_processed and (rule_processed[0] == DUMMY_RULE_PART):
            rule_processed = rule_processed[1:]
        
        for parameter_type, parameter_name in rule_processed[:-1]:
            if parameter_type == PARAMETER_TYPE_PATH:
                raise TypeError(f'Only last rule part can be `path` type, got {rule!r}.')
        
        if provide_automatic_options:
            request_methods, parameters, subdomain = _validate_options(options)
            if request_methods is None:
                request_methods = set()
                request_methods.add(METHOD_GET)
        
        else:
            request_methods = None
            parameters = None
            subdomain = None
        
        parameters = _merge_parameters(parameters, view_func_parameters)
        
        actual_rule = self.rules.get(endpoint, None)
        
        if actual_rule is None:
            rule = Rule(rule_processed, real_func, view_func_positional_parameter_names,
                view_func_keyword_parameter_names, view_func_kwargs_parameter_supported, endpoint, request_methods,
                parameters, subdomain)
            self.rules[endpoint] = rule
            return rule
        
        if isinstance(actual_rule, Rule):
            folder = RuleFolder.from_rule(actual_rule)
            folder.add_rule(rule_processed, request_methods, parameters, subdomain)
            self.rules[endpoint] = folder
            return folder
        
        # if isinstance(actual_rule, RuleFolder):
        actual_rule.add_rule(rule_processed, request_methods, parameters, subdomain)
        return actual_rule
    
    
    def after_request(self, after_request_function):
        """
        Registers an after request function. After request functions are ensured to modify the response object.
        
        Parameters
        ----------
        after_request_function : `async-callable`
            Should accept the following parameters
            +-------------------+-----------------------+-----------------------+
            | Respective name   | Type                  | Description           |
            +===================+=======================+=======================+
            | response          | ``ServerResponse``    | The response object.  |
            +-------------------+-----------------------+-----------------------+
        
        Returns
        -------
        after_request_function : `async-callable`
        
        Raises
        ------
        TypeError
            - If `after_request_function` was not given as `callable`.
            - If `after_request_function` was not given as `async-callable`.
            - If `after_request_function` accepts less or more than 1 positional parameters.
        """
        _analyze_handler(after_request_function, 'after_request_function', 1)
        after_request_functions = self.after_request_functions
        if after_request_functions is None:
            self.after_request_functions = after_request_functions = []
        
        after_request_functions.append(after_request_function)
        
        return after_request_function
    
    def before_request(self, before_request_function):
        """
        Registers a function which should run before a request is done.
        
        If any before request processor returns a non `None` value, then the request processing will stop and that
        return will be sent as response.
        
        Parameters
        ----------
        before_request_function : `async-callable`
            No parameters are passed to before request functions.
        
        Returns
        -------
        before_request_function : `async-callable`
        
        Raises
        ------
        TypeError
            - If `before_request_function` was not given as `callable`.
            - If `before_request_function` was not given as `async-callable`.
            - If `before_request_function` accepts less or more than 1 positional parameters.
        """
        _analyze_handler(before_request_function, 'before_request_function', 0)
        before_request_functions = self.before_request_functions
        if before_request_functions is None:
            self.after_request_functions = before_request_functions = []
        
        before_request_functions.append(before_request_function)
        
        return before_request_function
    
    def error_handler(self, error_code):
        """
        Registers an error handler which run when an http exception is raised from a view.
        
        Parameters
        ----------
        error_code : `int`
            Http error code.
        
        Raises
        ------
        TypeError
            If `error_code` was not given as `int` instance.
        
        Returns
        -------
        route_adder : ``_ErrorHandlerAdder``
        """
        if type(error_code) is int:
            pass
        elif isinstance(error_code, int):
            error_code = int(error_code)
        else:
            raise TypeError(f'`error_code` can be given as `int` instance, got {error_code.__class__.__name__}.')
        
        return _ErrorHandlerAdder(self, error_code)
    
    def _error_handler(self, error_code, error_handler_function):
        """
        Registers an error handler to the webapp. Called by ``_ErrorHandlerAdder``, what is returned by
        ``.error_handler``.
        
        Parameters
        ----------
        error_code : `int`
            Http error code. Should be already validated.
        error_handler_function : `async-callable`
            An async function to call when an http exception is raised.
            
            Should accept following parameters:
            +-------------------+-------------------+---------------------------+
            | Respective name   | Type              | Description               |
            +===================+===================+===========================+
            | exception         | ``AbortRequest``  | The occurred exception.   |
            +-------------------+-------------------+---------------------------+
        
        Returns
        -------
        error_handler_function : `async-callable`
        
        Raises
        ------
        TypeError
            - If `error_handler_function` was not given as `callable`.
            - If `error_handler_function` was not given as `async-callable`.
            - If `error_handler_function` accepts less or more than 1 positional parameters.
        """
        _analyze_handler(error_handler_function, 'error_handler_function', 0)
        error_handler_functions = self.error_handler_functions
        if error_handler_functions is None:
            self.error_handler_functions = error_handler_functions = {}
        
        error_handler_functions[error_code] = error_handler_function
        
        return error_handler_function
    
    def url_defaults(self, url_default_function):
        """
        Registers a keyword parameter processor for ``url_for``.
        
        Parameters
        ----------
        url_default_function : `async-callable`
            Should accept the following parameters
            +-------------------+---------------------------+-------------------------------------------------------+
            | Respective name   | type                      | Description                                           |
            +===================+===========================+=======================================================+
            | endpoint          | `None` or `str`           | The endpoint what matched the request url.            |
            +-------------------+---------------------------+-------------------------------------------------------+
            | kwargs            | `dict` of (`str`, `Any`)  | Additional keyword parameters passed to ``url_for``.  |
            +-------------------+---------------------------+-------------------------------------------------------+
        
        Returns
        -------
        url_default_function : `async-callable`
        
        Raises
        ------
        TypeError
            - If `url_default_function` was not given as `callable`.
            - If `url_default_function` was not given as `async-callable`.
            - If `url_default_function` accepts less or more than 2 positional parameters.
        """
        _analyze_handler(url_default_function, 'url_default_function', 2)
        url_default_functions = self.url_default_functions
        if url_default_functions is None:
            self.url_default_functions = url_default_functions = []
        
        url_default_functions.append(url_default_function)
        
        return url_default_function
    
    def url_value_preprocessor(self, url_value_preprocessor):
        """
        Registers a preprocessor which can modify the parameters matched from the url.
        
        Parameters
        ----------
        url_value_preprocessor : `async-callable`
            Should accept the following parameters
            +-------------------+---------------------------+-----------------------------------------------+
            | Respective name   | Type                      | Description                                   |
            +===================+===========================+===============================================+
            | endpoint          | `None` or `str`           | The endpoint what matched the request url.    |
            |                   |                           | Set as `None` if exception occurred.          |
            +-------------------+---------------------------+-----------------------------------------------+
            | parameters        | `dict` of (`str`, `Any`)  | Parameters parsed from the request url.       |
            +-------------------+---------------------------+-----------------------------------------------+
        
        Returns
        -------
        url_value_preprocessor : `async-callable`
        
        Raises
        ------
        TypeError
            - If `url_value_preprocessor` was not given as `callable`.
            - If `url_value_preprocessor` was not given as `async-callable`.
            - If `url_value_preprocessor` accepts less or more than 2 positional parameters.
        """
        _analyze_handler(url_value_preprocessor, 'url_value_preprocessor', 2)
        url_value_preprocessors = self.url_value_preprocessors
        if url_value_preprocessors is None:
            self.url_value_preprocessors = url_value_preprocessors = []
        
        url_value_preprocessors.append(url_value_preprocessor)
        
        return url_value_preprocessor
    
    def register_blueprint(self, blueprint, **options):
        """
        Registers a blueprint into the application.
        
        Parameters
        ----------
        parent : ``Blueprint``
            The parent blueprint or webapp to register self to.
        **options : Keyword parameters
            Extra options to overwrite the blueprint's.
        
        Other Parameters
        ----------------
        url_prefix : `None` or `str`
            Url prefix for a blueprint.
        subdomain : `None` or `str`
            Subdomain for the blueprint.
        url_defaults : `None`, `dict` of (`str`, `Any`) items or (`set`, `list`, `tuple`) of (`str`, `Any`) items
            Parameters which the routes of the blueprint will get by default.
        
        Raises
        ------
        TypeError
            - If `blueprint was not given as ``Blueprint`` instance.
            - If `url_prefix` was neither given as `None` or as `str` instance.
            - If `url_prefix` contains a `path` rule part.
            - If `subdomain` was not given neither as `None` or `str` instance.
            - If `parameters` is neither `None`, `dict`, `list`, `set` or `tuple`.
            - If `parameters` contains a non `tuple` element.
            - If `options` contains extra parameters.
        ValueError
            If `parameters` contains an element with length of not `2`.
        """
        blueprint_state = BlueprintState(blueprint, options)
        
        blueprints = self.blueprints
        if blueprints is None:
            self.blueprints = blueprints = []
        
        blueprints.append(blueprint_state)


class BlueprintState:
    """
    Represents options with what an a blueprint is added, since a blueprint's options can be overwritten.
    
    Attributes
    ----------
    blueprint : ``blueprint``
        The wrapped blueprint.
    url_prefix : `None` or `tuple` of `tuple` (`str`, `int`)
        Url prefix for all the routes of the blueprint. Set as `None` if not applicable.
    subdomain : `None` or `str`
        Subdomain, what the routes of the blueprint gonna match.
    parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        Parameters which the routes of the blueprint will get by default.
    """
    __slots__ = ('blueprint', 'url_prefix', 'subdomain', 'parameters')
    def __new__(cls, blueprint, options):
        """
        Creates a new blueprint state form the given blueprint and extra options.
        
        Parameters
        ----------
        blueprint : ``AppBase``
            The blueprint create overwrite state from.
        options : `None` or `dict` of (`str`, `Any`) items
            Extra options
        
        Raises
        ------
        TypeError
            - If `blueprint was not given as ``Blueprint`` instance.
            - If `url_prefix` was neither given as `None` or as `str` instance.
            - If `url_prefix` contains a `path` rule part.
            - If `subdomain` was not given neither as `None` or `str` instance.
            - If `parameters` is neither `None`, `dict`, `list`, `set` or `tuple`.
            - If `parameters` contains a non `tuple` element.
            - If `options` contains extra parameters.
        ValueError
            If `parameters` contains an element with length of not `2`.
        """
        if not isinstance(blueprint, Blueprint):
            raise TypeError(f'`blueprint` can be only as `{Blueprint.__name__}` instance, got '
                f'{blueprint.__class__.__name__}.')
        
        if options is None:
            subdomain = None
            url_prefix = None
            parameters = None
        else:
            subdomain = options.pop('subdomain', None)
            subdomain = _validate_subdomain(subdomain)
            
            url_prefix = options.pop('url_prefix', None)
            url_prefix = _validate_url_prefix(url_prefix)
            
            parameters = options.pop('url_defaults', None)
            parameters = _validate_parameters(parameters, 'url_defaults')
            
            if options:
                raise TypeError(f'`options` contains unexpected parameters: {options!r}.')
        
        self = object.__new__(cls)
        self.blueprint = blueprint
        self.subdomain = subdomain
        self.url_prefix = url_prefix
        self.parameters = parameters
        return self


class Blueprint(AppBase):
    """
    Represents a blueprint, a collection of routes and other app-related functions that can be registered on a real
    application later.
    
    Attributes
    ----------
    after_request_functions : `None` or `list` of `async-callable`
        Functions which are ensured to modify the response object.
        
        To register a after request function use the ``.after_request`` decorator.
        
        The following parameters are passed to each after request function:
        +-------------------+-----------------------+-----------------------+
        | Respective name   | Type                  | Description           |
        +===================+=======================+=======================+
        | response          | ``ServerResponse``    | The response object.  |
        +-------------------+-----------------------+-----------------------+
    
    before_request_functions : `None` or `list` of `async-callable`
        Functions which should run before a request is done.
        
        To register a before request function use the ``.before_request`` decorator.
        
        If any before request processor returns a non `None` value, then the request processing will stop and that
        return will be sent as response.
        
        No parameters are passed to before request functions.
    
    blueprints : `None` or `list` of ``BlueprintState``
        Registered blueprints to the app.
    
    error_handler_functions : `None` or `dict` of (`int`, `async-callable`) items
        Error handlers which run when an http exception is raised from a view.
        
        To register an error handler use the ``.error_handler`` decorator.
    
        The following parameters are passed to each error handler:
        +-------------------+-------------------+---------------------------+
        | Respective name   | Type              | Description               |
        +===================+===================+===========================+
        | exception         | ``AbortRequest``  | The occurred exception.   |
        +-------------------+-------------------+---------------------------+
    
    import_name : `str`
        The name of the package or module that this app belongs to.
    root_path : `str`
        Absolute path to the package on the filesystem.
    rules : `dict` of (`str`, `Any`)
        The added rules to the application or blueprint. The keys are their endpoint name.
    static_folder : `None` or `str`
        Absolute path to the static file's folder.
    static_url_path : `None` or `str`
        Url path to static files. By defaults relates to `static_folder`.
    
    teardown_request_functions : `None` or `list` of `async-callable`
        Functions which should run after a request is done even if exception occurs.
        
        To register a teardown request function use the ``.teardown_request`` decorator.
        
        The following parameters are passed to each teardown request:
        +-------------------+---------------------------+-----------------------------------+
        | Respective name   | Type                      | Description                       |
        +===================+===========================+===================================+
        | exception         | `None` or `BaseException` | The occurred exception if any.    |
        +-------------------+---------------------------+-----------------------------------+
        
    template_context_processors : `None` or `list of `async-callable`
        Functions which are called to populate template context. Each should return a dictionary with what the template
        dictionary is updated with.
        
        To register template context processor, use the ``.context_processor`` decorator.
        
        No parameters are passed to template context processors.
    
    template_folder : `None` or `str`
        The folder from where the templates should be loaded from.
    
    url_default_functions : `None` or `list` of `async-callable`
        Keyword parameter preprocessors for ``url_for``.
        
        To register them use the ``.url_defaults`` method.
        
        The following parameters are passed to the url default functions:
        +-------------------+---------------------------+-------------------------------------------------------+
        | Respective name   | type                      | Description                                           |
        +===================+===========================+=======================================================+
        | endpoint          | `None` or `str`           | The endpoint what matched the request url.            |
        +-------------------+---------------------------+-------------------------------------------------------+
        | kwargs            | `dict` of (`str`, `Any`)  | Additional keyword parameters passed to ``url_for``.  |
        +-------------------+---------------------------+-------------------------------------------------------+
    
    url_value_preprocessors : `None` or `list` of `async-callable`
        Preprocessors which can modify the parameters matched from the url.
        
        To registered them use the ``.url_value_preprocessor`` decorator.
        
        The following parameters are passed to each url value preprocessor:
        +-------------------+---------------------------+-----------------------------------------------+
        | Respective name   | Type                      | Description                                   |
        +===================+===========================+===============================================+
        | endpoint          | `None` or `str`           | The endpoint what matched the request url.    |
        |                   |                           | Set as `None` if exception occurred.          |
        +-------------------+---------------------------+-----------------------------------------------+
        | parameters        | `dict` of (`str`, `Any`)  | Parameters parsed from the request url.       |
        +-------------------+---------------------------+-----------------------------------------------+
    
    url_prefix : `None` or `tuple` of `tuple` (`str`, `int`)
        Url prefix for all the routes of the blueprint. Set as `None` if not applicable.
    subdomain : `None` or `str`
        Subdomain, what the routes of the blueprint gonna match.
    parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        Parameters which the routes of the blueprint will get by default.
    """
    __slots__ = ('url_prefix', 'subdomain', 'parameters')
    def __new__(cls, import_name, *, template_folder=None, root_path=None, static_folder=None,
            static_url_path=None, url_prefix=None, subdomain=None, url_defaults=None):
        """
        Creates a new ``Blueprint`` instance.
        
        Parameters
        ----------
        import_name : `str`
            The name of the package or module that this app belongs to.
        template_folder : `None` or `str`, Optional (Keyword only)
            The folder from where the templates should be loaded from.
        root_path : `None` or `str`, Optional (Keyword only)
            Absolute path to the package on the filesystem.
        static_folder : `None` or `str`, Optional (Keyword only)
            Path on top of the application route path for static files, which can be accessed trough the
            `static_url_path`. Defaults to `None`.
        static_url_path : `None` or `str`, Optional (Keyword only)
            Url path to static files. Defaults to `static_folder`'s value.
        url_prefix : `None` or `str`, Optional (Keyword only)
            Url prefix for all the routes registered to the blueprint.
        subdomain : `None` or `str`, Optional (Keyword only)
            Subdomain, what the routes of the blueprint gonna match.
        url_defaults : `None`, `dict` of (`str`, `Any`) items or (`set`, `list`, `tuple`) of (`str`, `Any`) items
                , Optional (Keyword only)
            Parameters which the routes of the blueprint will get by default.
        
        Raises
        ------
        ImportError
            Exception occurred meanwhile finding route path from import name.
        TypeError
            - If `import_name` was not given as `st` instance.
            - If `template_folder` was not given neither as `None` or `str` instance.
            - If `root_path` was not given neither as `None` or `str` instance.
            - If `static_folder` was not given neither as `None` nor `str` instance.
            - If `static_url_path` was not given either as `None` or `str` instance.
            - If `url_prefix` was neither given as `None` or as `str` instance.
            - If `url_prefix` contains a `path` rule part.
            - If `subdomain` was not given neither as `None` or `str` instance.
            - If `defaults` is neither `None`, `dict`, `list`, `set` or `tuple`.
            - If `defaults` contains a non `tuple` element.
        ValueError
            - If `import_name` was given as an empty string.
            - If `root_path` was given as an empty string.
            - If `defaults` contains an element with length of not `2`.
        """
        url_prefix = _validate_url_prefix(url_prefix)
        subdomain = _validate_subdomain(subdomain)
        parameters = _validate_parameters(url_defaults, 'url_defaults')
        
        self = AppBase.__new__(cls, import_name, template_folder, root_path, static_folder, static_url_path)
        self.url_prefix = url_prefix
        self.subdomain = subdomain
        self.parameters = parameters
        return self


class WebApp(AppBase):
    """
    Central registry for the view functions, the URL rules, and for blueprints.
    
    Attributes
    ----------
    after_request_functions : `None` or `list` of `async-callable`
        Functions which are ensured to modify the response object.
        
        To register a after request function use the ``.after_request`` decorator.
        
        The following parameters are passed to each after request function:
        +-------------------+-----------------------+-----------------------+
        | Respective name   | Type                  | Description           |
        +===================+=======================+=======================+
        | response          | ``ServerResponse``    | The response object.  |
        +-------------------+-----------------------+-----------------------+
    
    before_request_functions : `None` or `list` of `async-callable`
        Functions which should run before a request is done.
        
        To register a before request function use the ``.before_request`` decorator.
        
        If any before request processor returns a non `None` value, then the request processing will stop and that
        return will be sent as response.
        
        No parameters are passed to before request functions.
    
    blueprints : `None` or `dict` of (`str`, `tuple` (``BlueprintState``, ``Blueprint``)
        Registered blueprints to the app.
    
    error_handler_functions : `None` or `dict` of (`int`, `async-callable`) items
        Error handlers which run when an http exception is raised from a view.
        
        To register an error handler use the ``.error_handler`` decorator.
    
        The following parameters are passed to each error handler:
        +-------------------+-------------------+---------------------------+
        | Respective name   | Type              | Description               |
        +===================+===================+===========================+
        | exception         | ``AbortRequest``  | The occurred exception.   |
        +-------------------+-------------------+---------------------------+
    
    import_name : `str`
        The name of the package or module that this app belongs to.
    root_path : `str`
        Absolute path to the package on the filesystem.
    rules : `dict` of (`str`, `Any`)
        The added rules to the application or blueprint. The keys are their endpoint name.
    static_folder : `None` or `str`
        Absolute path to the static file's folder.
    static_url_path : `None` or `str`
        Url path to static files. By defaults relates to `static_folder`.
    
    teardown_request_functions : `None` or `list` of `async-callable`
        Functions which should run after a request is done even if exception occurs.
        
        To register a teardown request function use the ``.teardown_request`` decorator.
        
        The following parameters are passed to each teardown request:
        +-------------------+---------------------------+-----------------------------------+
        | Respective name   | Type                      | Description                       |
        +===================+===========================+===================================+
        | exception         | `None` or `BaseException` | The occurred exception if any.    |
        +-------------------+---------------------------+-----------------------------------+
        
    template_context_processors : `None` or `list of `async-callable`
        Functions which are called to populate template context. Each should return a dictionary with what the template
        dictionary is updated with.
        
        To register template context processor, use the ``.context_processor`` decorator.
        
        No parameters are passed to template context processors.
    
    template_folder : `None` or `str`
        The folder from where the templates should be loaded from.
    
    url_default_functions : `None` or `list` of `async-callable`
        Keyword parameter preprocessors for ``url_for``.
        
        To register them use the ``.url_defaults`` method.
        
        The following parameters are passed to the url default functions:
        +-------------------+---------------------------+-------------------------------------------------------+
        | Respective name   | type                      | Description                                           |
        +===================+===========================+=======================================================+
        | endpoint          | `None` or `str`           | The endpoint what matched the request url.            |
        +-------------------+---------------------------+-------------------------------------------------------+
        | kwargs            | `dict` of (`str`, `Any`)  | Additional keyword parameters passed to ``url_for``.  |
        +-------------------+---------------------------+-------------------------------------------------------+
    
    url_value_preprocessors : `None` or `list` of `async-callable`
        Preprocessors which can modify the parameters matched from the url.
        
        To registered them use the ``.url_value_preprocessor`` decorator.
        
        The following parameters are passed to each url value preprocessor:
        +-------------------+---------------------------+-----------------------------------------------+
        | Respective name   | Type                      | Description                                   |
        +===================+===========================+===============================================+
        | endpoint          | `None` or `str`           | The endpoint what matched the request url.    |
        |                   |                           | Set as `None` if exception occurred.          |
        +-------------------+---------------------------+-----------------------------------------------+
        | parameters        | `dict` of (`str`, `Any`)  | Parameters parsed from the request url.       |
        +-------------------+---------------------------+-----------------------------------------------+
    
    _server : `None` or ``WebServer``
        The running web-server of the webapp.
    """
    __slots__ = ('_server',)
    def __new__(cls, import_name, *, template_folder=None, root_path=None, static_folder='static',
            static_url_path=None):
        """
        Creates a new ``WebApp`` instance.
        
        Parameters
        ----------
        import_name : `str`
            The name of the package or module that this app belongs to.
        template_folder : `None` or `str`, Optional (Keyword only)
            The folder from where the templates should be loaded from.
        root_path : `None` or `str`, Optional (Keyword only)
            Absolute path to the package on the filesystem.
        static_folder : `None` or `str`, Optional (Keyword only)
            Path on top of the application route path for static files, which can be accessed trough the
            `static_url_path`. Defaults to `'static'`.
        static_url_path : `None` or `str`, Optional (Keyword only)
            Url path to static files. Defaults to `static_folder`'s value.
        
        Raises
        ------
        ImportError
            Exception occurred meanwhile finding route path from import name.
        TypeError
            - If `import_name` was not given as `st` instance.
            - If `template_folder` was not given neither as `None` or `str` instance.
            - If `root_path` was not given neither as `None` or `str` instance.
            - If `static_folder` was not given neither as `None` nor `str` instance.
            - If `static_url_path` was not given either as `None` or `str` instance.
        ValueError
            - If `import_name` was given as an empty string.
            - If `root_path` was given as an empty string.
        """
        self = AppBase.__new__(cls, import_name, template_folder, root_path, static_folder, static_url_path)
        
        
        self._server = None
        
        return self

def _register_rules(application, blueprint_state_stack, rules, router, router_by_subdomain, subdomain, url_prefix,
        parameters):
    """
    Registers more rules paths.
    
    Parameters
    ----------
    application : ``WebApp``
        The parent application.
    blueprint_state_stack : `None` or `tuple` of ``BluePrintState``
        Blueprint stack of the rule.
    rules : `list` of (``Rule``, ``RuleFolder``)
        Rules of a blueprint or of an application to register.
    router : ``PathRouter``
        Router where rules are registered without subdomain
    router_by_subdomain : `dict` of (`str`, ``PathRouter``) items
        Routers by subdomain name.
    subdomain : `None` or `str`
        Subdomain to overwrite the rules'.
    url_prefix : `None` or `tuple` of `None` or `tuple` of `tuple` (`str`, `int`)
        Additional url prefix for the rules.
    parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        Parameters which the routes of the blueprint will get by default.
    """
    for rule in rules:
        for rule in rule.iter_rules():
            rule = rule.copy()
            rule.set_subdomain(subdomain)
            rule.set_rule_prefix(url_prefix)
            rule.set_parameters(parameters)
            rule.set_application(application)
            rule.set_blueprint_state_stack(blueprint_state_stack)
            _register_route(rule, router, router_by_subdomain)

def _register_route(rule, router, router_by_subdomain):
    """
    Registers an rule to the paths.
    
    Parameters
    ----------
    rule : ``Rule``
        The url rule to register.
    router : ``PathRouter``
        Router where rules are registered without subdomain
    router_by_subdomain : `dict` of (`str`, ``PathRouter``) items
        Routers by subdomain name.
    """
    subdomain = rule.subdomain
    if subdomain is None:
        target_router = router
    else:
        try:
            target_router = router_by_subdomain[subdomain]
        except KeyError:
            target_router = router_by_subdomain[subdomain] = PathRouter()
    
    target_router.register_route(rule, 0)

def _register_rules_from_state_stack(application, blueprint_state_stack, router, router_by_subdomain):
    """
    Registers the
    
    Parameters
    ----------
    application : ``WebApp``
        The parent web application.
    blueprint_state_stack : `list` of ``BlueprintState``
        A list of blueprint stack.
    router : ``PathRouter``
        Router where rules are registered without subdomain
    router_by_subdomain : `dict` of (`str`, ``PathRouter``) items
        Routers by subdomain name.
    """
    blueprint_state_stack = tuple(blueprint_state_stack)
    rules = list(blueprint_state_stack[-1].blueprint.rules.values())
    
    subdomain_final = None
    url_prefix_final = None
    parameters_final = None
    
    for blueprint_state in reversed(blueprint_state_stack):
        blueprint = blueprint_state.blueprint
        subdomain_overwrite = blueprint_state.subdomain
        if subdomain_overwrite is None:
            subdomain_overwrite = blueprint.subdomain
        
        if (subdomain_overwrite is not None):
            subdomain_final = subdomain_overwrite
        
        url_prefix_overwrite = blueprint_state.url_prefix
        if url_prefix_overwrite is None:
            url_prefix_overwrite = blueprint.url_prefix
        
        if (url_prefix_overwrite is not None):
            url_prefix_final = _merge_url_rule(url_prefix_overwrite, url_prefix_final)
        
        parameters_overwrite = blueprint_state.parameters
        if parameters_overwrite is None:
            parameters_overwrite = blueprint.parameters
        
        if (parameters_overwrite is not None):
            parameters_final = _merge_parameters(parameters_final, parameters_overwrite)
    
    _register_rules(application, blueprint_state_stack, rules, router, router_by_subdomain, subdomain_final,
        url_prefix_final, subdomain_final)


class RequestHandler:
    """
    Dispatches a request.
    
    _router : ``PathRouter``
        Path router to decide which function should be called when receiving a request.
    _router_by_subdomain : `dict` of (`str`, ``PathRouter``)
        Routers for each subdomain.
    """
    __slots__ = ('_router', '_router_by_subdomain')
    def __new__(cls, application):
        """
        Creates a new ``RequestHandler`` instance.
        
        Parameters
        ----------
        application : ``WebApp``
            The parent application.
        
        Raises
        ------
        RuntimeError
            - If recursive blueprint hook was found.
        """
        # First scan for blueprints for recursive hooks and raise RuntimeError if any found.
        # Do not use recursion when checking for recursion, lol.
        blueprint_state_generator_stack = []
        blueprint_stack = []
        
        next_stack_blueprints = application.blueprints
        if (next_stack_blueprints is not None):
            blueprint_state_generator_stack.append(iter(next_stack_blueprints))
        
        while blueprint_state_generator_stack:
            blue_print_state_generator = blueprint_state_generator_stack[-1]
            
            try:
                blueprint_state = next(blue_print_state_generator)
            except StopIteration:
                del blueprint_state_generator_stack[-1]
                del blueprint_stack[-1]
                continue
            
            blueprint = blueprint_state.blueprint
            if blueprint in blueprint_stack:
                raise RuntimeError(f'Recursive blueprint hook found: {blueprint_stack!r} is followed by {blueprint!r}.')
            
            next_stack_blueprints = blueprint.blueprints
            if next_stack_blueprints is None:
                continue
            
            blueprint_stack.append(blueprint)
            blueprint_state_generator_stack.append(iter(next_stack_blueprints))
            continue
        
        # No recursive blueprints found.
        # Now we can add the rules.
        router = PathRouter()
        router_by_subdomain = {}
        
        blueprint_state_stack = []
        
        next_stack_blueprints = application.blueprints
        if (next_stack_blueprints is not None):
            blueprint_state_generator_stack.append(iter(next_stack_blueprints))
        
        _register_rules(application, None, list(application.rules.values()), router, router_by_subdomain, None, None, None)
        
        while blueprint_state_generator_stack:
            blue_print_state_generator = blueprint_state_generator_stack[-1]
            
            try:
                blueprint_state = next(blue_print_state_generator)
            except StopIteration:
                _register_rules_from_state_stack(application, blueprint_state_stack, router, router_by_subdomain)
                
                del blueprint_state_generator_stack[-1]
                del blueprint_state_stack[-1]
                continue
            
            blueprint_state_stack.append(blueprint_state)
            continue
        
        router.validate_parameters()
        
        self = object.__new__(cls)
        self._router = router
        self._router_by_subdomain = router_by_subdomain
        return self
    
    def render_structure(self):
        """
        Renders the ``RequestHandler``'s routing structure.
        
        Returns
        -------
        routing_structure : `str`
        """
        route_prefix_parts = ['.']
        parts = []
        
        self._router.render_structure(route_prefix_parts, parts)
        
        for subdomain, router in self._router_by_subdomain:
            route_prefix_parts.append(subdomain)
            router.render_structure(route_prefix_parts, parts)
            del route_prefix_parts[-1]
        
        return ''.join(parts)
    
    async def __call__(self, raw_request_message):
        """
        Handles a request.
        
        This method is a coroutine.
        
        Parameters
        ----------
        raw_request_message : ``RawRequestMessage``
            Received raw request.
        """
        url = URL(raw_request_message.path)
        route = self._dispatch_route(url, raw_request_message.method)
        rule = route.rule
        
        before_request_functions = rule.before_request_functions
        if (before_request_functions is None):
            answered = False
        else:
            for before_request_function in before_request_functions:
                try:
                    response_result = await before_request_function()
                except BaseException as err:
                    response_exception = err
                    # TODO
                    # Answer
                    answered = True
                    break
                else:
                    if (response_result is not None):
                        # TODO
                        # Answer
                        answered = True
                        break
            else:
                answered = False
        
        if not answered:
            # TODO
            pass
        
    def _dispatch_route(self, url, request_method):
        """
        Gets handler for the given `url` and `request_method` combination.
        
        Parameters
        ----------
        url : ``URL`` instance
            The received request url.
        request_method : `str`
            The method to request.
        
        Returns
        -------
        route : ``Route``
            The found route if any.
        """
        subdomain = url.subdomain
        if subdomain is None:
            router = self._router
        else:
            try:
                router = self._router_by_subdomain[subdomain]
            except KeyError:
                return Route(ROUTE_NOT_FOUND_NOT_ALLOWED)
        
        path = url.parts
        
        route = router.dispatch_route(path, 1, request_method)
        if route is None:
            route = Route(ROUTE_NOT_FOUND_NOT_ALLOWED)
        
        return route
