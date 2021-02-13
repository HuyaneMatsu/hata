# -*- coding: utf-8 -*-
# Experimenting with web servers, nothing worthy
# WORK IN PROGRESS
import functools, http, re, sys, os, ntpath

from uuid import UUID
from importlib.util import find_spec

from .utils import imultidict, methodize
from .futures import WaitTillAll, Future, Task, CancelledError
from .protocol import ProtocolBase
from .exceptions import PayloadError
from .helpers import HttpVersion11
from .headers import METHOD_ALL, METHOD_GET
from .url import URL
from .analyzer import CallableAnalyzer

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
    route_end : `None` or `dict` of (`str`, ``Rule``) items
        If the url ends at the point of this router, then the handler function from ``.route_ends`` is chosen if
        applicable. The functions are stored in `method` - `handler` relation.
    route_end_all : `None` or ``Rule``)
        If the url ends at this point of the router and non of the `route-end`-s were matched, the the view function
        of this slot is chosen.
    route_end_path : `None` or `dict` of (`str`, ``Rule``) items
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
    
    def register_route(self, rule, index, request_methods):
        """
        Registers a new handler to the path router.
        
        Parameters
        ----------
        rule : ``rule``
            The rule of the endpoint
        index : `int`
            The index of the part of the path to process by this router.
        request_methods : `None` or `set` of `str`
            The methods of the request to registered `rule`. Can be given as `None` to handle all type of requests.
        """
        url_rule = rule.rule
        if index == len(url_rule):
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
            
            path_router.register_route(rule, index, request_methods)
            return
        
        if rule_part_type == PARAMETER_TYPE_PATH:
            rule_rule_part_tuple = (rule, rule_part)
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
            path_router.register_route(rule, index, request_methods)
            
            route_step_validated.append(parameter_validator_path_step)
            return
        
        for parameter_validator_path_step in route_step_validated:
            if parameter_validator_path_step.parameter_type == rule_part_type:
                path_router = parameter_validator_path_step.get_path_router(rule_part)
                path_router.register_route(rule, index, request_methods)
                return
        
        parameter_validator_path_step, path_router = ParameterValidatorPathStep(rule_part_type, rule_part)
        path_router.register_route(rule, index, request_methods)
        
        route_step_validated.append(parameter_validator_path_step)


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


class _RouteAdder(object):
    """
    Route adder returned by ``WebApp.route`` to add a route to it as a decorator.
    
    Attributes
    ----------
    parent : ``WebApp``
        The parent webapp.
    rule : `str`
        The url rule as string.
    endpoint  : `None` or `str`
        The internal endpoint of the url. Defaults to the name of the added function.
    options : `dict` of (`str`, `Any`) items.
        Additional options to be forward to the underlying ``Rule`` object.
    """
    def __new__(cls, parent, rule, endpoint, options):
        """
        Creates a new ``_RouteAdder object with the given parameters.
        
        Parameters
        ----------
        parent : ``WebApp``
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
        Adds the given `view_func` and the stored parameters to the parent ``WebApp`` calling it's `.add_url_rule`
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
        return self.parent.add_url_rule(rule=self.rule, endpoint=self.endpoint, view_func=view_func,
            provide_automatic_options=None, **self.options)

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
        A set of teh validated http methods. If none is given, `'GET'` is auto added to it.
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
    template_folder : `str` or `None`
        The template folder's value.
    
    Returns
    -------
    template_folder : `str` or `None`
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
    root_path : `str` or `None`
        The given root path.
    
    Returns
    -------
    root_path : `str` or `None`
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
    static_folder : `str` or `None`
        Static folder value to validate.
    
    Returns
    -------
    static_folder : `str` or `None`
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
    static_url_path : `str` or `None`
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
    url_prefix : `str` or `None`
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

DUMMY_RULE_PART = ('/', PARAMETER_TYPE_STATIC)

class Rule(object):
    """
    A registered rule.
    
    Attributes
    ----------
    endpoint : `str`
        The endpoint's internal name.
    parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        Default parameters to pass to the `view_func`.
    request_methods : `None` or `set` of `str`
        Request methods to call `view_func` when received.
    rule : `tuple` or `tuple` of (`int`, `str`)
        The url's path part.
    subdomain : `None` or `str`
        Whether the route should match the specified subdomain.
    view_func : `async-callable`
        The function to call when serving a request to the provided endpoint.
    """
    __slots__ = ('endpoint', 'parameters', 'request_methods', 'rule', 'subdomain', 'view_func')
    
    def __init__(self, rule, view_func, endpoint, request_methods, parameters, subdomain):
        """
        Creates a new ``Rule`` instance.
        
        Parameters
        ----------
        rule : `tuple` of `tuple` (`int`, `str`)
            The url rule to register.
        view_func : `async-callable`
            The function to call when serving a request to the provided endpoint.
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
        
        return new
    
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
        if (parameters is not None):
            self_parameters = self.parameters
            if self_parameters is None:
                self.parameters = parameters.copy()
            else:
                to_add = []
                for item in parameters:
                    parameter_name = item[0]
                    for self_item in self_parameters:
                        if self_item[0] == parameter_name:
                            break
                    else:
                        to_add.append(item)
                
                if to_add:
                    self.parameters = (*self_parameters, *to_add)
    
    def set_rule_prefix(self, rule):
        """
        Extends the rule parts of the rule.
        
        Parameters
        ----------
        rule : `None` or `tuple` of `tuple` (`str`, `int`)
            The rule parts to extend the ``Rule``'s with.
        """
        if (rule is not None):
            self_rule = self.rule
            if self_rule[0] == DUMMY_RULE_PART:
                self_rule = self_rule[1:]
            
            self.rule = (*rule, *self_rule)

ROUTE_METHOD_NOT_ALLOWED = Rule((), _handler_method_not_allowed, 'method_not_allowed', None, None, None)
ROUTE_NOT_FOUND_NOT_ALLOWED = Rule((), _handler_not_found, 'not found', None, None, None)


class AppBase(object):
    """
    Base class for ``BluePrint``-s and for ``WebApp``-s.
    
    Attributes
    ----------
    import_name : `str`
        The name of the package or module that this app belongs to.
    template_folder : `None` or `str`
        The folder from where the templates should be loaded from.
    root_path : `str`
        Absolute path to the package on the filesystem.
    static_folder : `str` or `None`
        Absolute path to the static file's folder.
    static_url_path : `str` or `None`
        Url path to static files. By defaults relates to `static_folder`.
    rules : `dict` of (`str`, `Any`)
        The added rules to the application or blueprint. The keys are their endpoint name.
    error_handler_functions : `None` or `dict` of (`int`, `async-callable`)
        Global error handlers of the application or blueprint.
        
        To register an error handler use the ``.errorhandler`` decorator.
    error_handler_functions_by_blueprint : `None` or `dict` of (`str`, `dict` of (`int`, `async-callable`))
        Error handlers for each blue print fo teh application.
        
        To register an error handler use the ``.errorhandler`` decorator.
    before_request_functions : `None` or `list` of `async-callable`
        Functions which should run before a request is done.
        
        To register a before request function use the ``.before_request`` decorator.
    before_request_functions_by_blueprint : `None` or `dict` of (`str`, `list` of `async-callable`)
        Functions which should be called before a respective blue print's request is dispatched.
        
        To register a before request function use the ``.before_request`` decorator.
    
    after_request_functions : `None` or `list` of `async-callable`
        Functions which should run after a request is done.
        
        To register a after request function use the ``.after_request`` decorator.
    after_request_functions_by_blueprint : `None` or `dict` of (`str`, `list` of `async-callable`)
        Functions which should be called before a respective blue print's request is dispatched.
        
        To register a before request function use the ``.after_request`` decorator.
    
    teardown_request_functions : `None` or `list` of `async-callable`
        Functions which should run after a request is done even if exception occurs.
        
        To register a teardown request function use the ``.teardown_request`` decorator.
    teardown_request_functions_by_blueprint : `None` or `dict` of (`str`, `list` of `async_callable`)
        Functions which should be called before a respective blue print's request is dispatched even if exception
        occurs.
        
        To register a teardown request function use the ``.teardown_request`` decorator.
    template_context_processors : `None` or `list of `async-callable`
        Functions which are called to populate template context without passing them any parameter. Each should return
        a dictionary with what the template dictionary is updated with.
        
        To register template context processor, use the ``.context_processor`` decorator.
    template_context_processors_by_blueprint : `None` or `dict` of (`str`, `Any`)
        A dictionary of functions for each template which are called to populate template context without passing them
        any parameter. Each should return a dictionary with what the template dictionary is updated with.
        
        To register template context processor, use the ``.context_processor`` decorator.
    url_value_preprocessors : `None` or `list` of `async-callable`
        Preprocessors, which can modify the parameters matched from the url.
        
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
        
    url_value_preprocessors_by_blueprint : `None` or `dict` of (`str`, list` of `async-callable`) items
        Preprocessors by blueprint which can modify the parameters matched from the url.
        
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
    url_default_functions : `None` or `dict` of (`str` of `callable`)
        Keyword argument preprocessors when calling ``url_for`` on it's parameters.
        
        To register them use the ``.url_defaults`` method.
        
        The following parameters are passed to the url default functions:
        +-------------------+---------------------------+-------------------------------------------------------+
        | Respective name   | type                      | Description                                           |
        +===================+===========================+=======================================================+
        | endpoint          | `None` or `str`           | The endpoint what matched the request url.            |
        +-------------------+---------------------------+-------------------------------------------------------+
        | kwargs            | `dict` of (`str`, `Any`)  | Additional keyword parameters passed to ``url_for``.  |
        +-------------------+---------------------------+-------------------------------------------------------+
    url_default_functions_by_blueprint : `None` or `dict` of (`str`, `list` of `callable`) items
        Keyword argument preprocessors by blueprint name when calling ``url_for`` on it's parameters.
        
        To register them use the ``.url_defaults`` method.
        
        The following parameters are passed to the url default functions:
        +-------------------+---------------------------+-------------------------------------------------------+
        | Respective name   | type                      | Description                                           |
        +===================+===========================+=======================================================+
        | endpoint          | `None` or `str`           | The endpoint what matched the request url.            |
        +-------------------+---------------------------+-------------------------------------------------------+
        | kwargs            | `dict` of (`str`, `Any`)  | Additional keyword parameters passed to ``url_for``.  |
        +-------------------+---------------------------+-------------------------------------------------------+
    """
    __slots__ = ('import_name', 'template_folder', 'root_path', 'static_folder', 'static_url_path', 'rules',
        'error_handler_functions', 'error_handler_functions_by_blueprint', 'before_request_functions',
        'before_request_functions_by_blueprint', 'after_request_functions', 'after_request_functions_by_blueprint',
        'teardown_request_functions', 'teardown_request_functions_by_blueprint', 'template_context_processors',
        'template_context_processors_by_blueprint', 'url_value_preprocessors', 'url_value_preprocessors_by_blueprint',
        'url_default_functions', 'url_default_functions_by_blueprint')
    
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
        
        self.error_handler_functions = None
        self.error_handler_functions_by_blueprint = None
        
        self.before_request_functions = None
        self.before_request_functions_by_blueprint = None
        
        self.after_request_functions = None
        self.after_request_functions_by_blueprint = None
        
        self.teardown_request_functions = None
        self.teardown_request_functions_by_blueprint = None
        
        self.template_context_processors = None
        self.template_context_processors_by_blueprint = None
        
        self.url_value_preprocessors = None
        self.url_value_preprocessors_by_blueprint = None
        
        self.url_default_functions = None
        self.url_default_functions_by_blueprint = None
        return self

class BluePrint(AppBase):
    """
    Represents a blueprint, a collection of routes and other app-related functions that can be registered on a real
    application later.
    
    Attributes
    ----------
    import_name : `str`
        The name of the package or module that this app belongs to.
    template_folder : `None` or `str`
        The folder from where the templates should be loaded from.
    root_path : `str`
        Absolute path to the package on the filesystem.
    static_folder : `str` or `None`
        Absolute path to the static file's folder.
    static_url_path : `str` or `None`
        Url path to static files. By defaults relates to `static_folder`.
    url_prefix : `None` or `tuple` of `tuple` (`str`, `int`)
        Url prefix for all the routes of the blueprint. Set as `None` if not applicable.
    subdomain : `str` or `None`
        Subdomain, what the routes of the blueprint gonna match.
    parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
        Parameters which the routes of the blueprint will get by default.
    """
    __slots__ = ('url_prefix', 'subdomain', 'parameters')
    def __new__(cls, import_name, *, template_folder=None, root_path=None, static_folder=None,
            static_url_path=None, url_prefix=None, subdomain=None, url_defaults=None):
        """
        Creates a new ``BluePrint`` instance.
        
        Parameters
        ----------
        import_name : `str`
            The name of the package or module that this app belongs to.
        template_folder : `None` or `str`, Optional
            The folder from where the templates should be loaded from.
        root_path : `None` or `str`, Optional
            Absolute path to the package on the filesystem.
        static_folder : `None` or `str`, Optional
            Path on top of the application route path for static files, which can be accessed trough the
            `static_url_path`. Defaults to `None`.
        static_url_path : `None` or `str`, Optional
            Url path to static files. Defaults to `static_folder`'s value.
        url_prefix : `str` or `None`, Optional
            Url prefix for all the routes registered to teh blueprint.
        subdomain : `str` or `None`
            Subdomain, what the routes of the blueprint gonna match.
        url_defaults : `None`, `dict` of (`str`, `Any`) items or (`set`, `list`, `tuple`) of (`str`, `Any`) items
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
        ValueError
            - If `import_name` was given as an empty string.
            - If `root_path` was given as an empty string.
        """
        url_prefix = _validate_url_prefix(url_prefix)
        subdomain = _validate_subdomain(subdomain)
        parameters = _validate_parameters(url_defaults, 'url_defaults')
        
        self = AppBase.__new__(cls, import_name, template_folder, root_path, static_folder, static_url_path)
        self.url_prefix = url_prefix
        self.subdomain = subdomain
        self.parameters = parameters
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
        **options : keyword arguments
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
        *args : arguments
            `endpoint` and `view_func` depending 1 or 2 parameters were given.
        endpoint  : `None` or `str`, Optional
            The internal endpoint of the url. Defaults to the name of the added function.
        view_func : `async-callable`
            The function to call when serving a request to the provided endpoint.
        provide_automatic_options : `None` or `bool`, Optional
            Controls whether `options` should be handled manually.
        **options : keyword arguments
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
            raise TypeError('`view_func` can be `async-callable`, got `None`.')
        
        analyzed = CallableAnalyzer(view_func)
        if not analyzed.is_async():
            raise TypeError(f'`view_func` can be given as `async-callable`, got {analyzed.__class__.__name__}; '
                f'{analyzed!r}.')
        
        for parameter_name in ('method', 'methods', 'defaults'):
            if options.get(parameter_name) is None:
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
            endpoint = analyzed.__name__
        
        if type(endpoint) is str:
            pass
        elif isinstance(endpoint, str):
            endpoint = str(endpoint)
        else:
            raise TypeError(f'`endpoint` can be given as `str` instance, got {endpoint.__class__.__name__}.')
        
        
        rule_processed = tuple(maybe_typed_rule_part(rule_part) for rule_part in URL(rule).path)
        
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
        
        rule = Rule(rule_processed, view_func, endpoint, request_methods, parameters, subdomain)
        self._add_rule(rule)
        return rule

class WebApp(AppBase):
    """
    Central registry for the view functions, the URL rules, and for blueprints.
    
    Attributes
    ----------
    import_name : `str`
        The name of the package or module that this app belongs to.
    template_folder : `None` or `str`
        The folder from where the templates should be loaded from.
    root_path : `str`
        Absolute path to the package on the filesystem.
    static_folder : `str` or `None`
        Absolute path to the static file's folder.
    static_url_path : `str` or `None`
        Url path to static files. By defaults relates to `static_folder`.
    
    _server : `None` or ``WebServer``
        The running web-server of the webapp.
    _router : ``PathRouter``
        Path router to decide which function should be called when receiving a request.
    """
    __slots__ = ('_server', '_router')
    def __new__(cls, import_name, *, template_folder=None, root_path=None, static_folder='static',
            static_url_path=None):
        """
        Creates a new ``WebApp`` instance.
        
        Parameters
        ----------
        import_name : `str`
            The name of the package or module that this app belongs to.
        template_folder : `None` or `str`, Optional
            The folder from where the templates should be loaded from.
        root_path : `None` or `str`, Optional
            Absolute path to the package on the filesystem.
        static_folder : `None` or `str`, Optional
            Path on top of the application route path for static files, which can be accessed trough the
            `static_url_path`. Defaults to `'static'`.
        static_url_path : `None` or `str`, Optional
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
        self._router = PathRouter()
        return self
    
    def _dispatch_route(self, url, request_method):
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
        route = self._router.dispatch_route(path, 0, request_method)
        if route is None:
            route = Route(ROUTE_NOT_FOUND_NOT_ALLOWED)
        
        return route
    
    def _register_route(self, rule, request_methods, parameters):
        """
        Registers an url and handler to the http server.
        
        Parameters
        ----------
        rule : ``Rule``
            The url rule to register.
        request_methods : `None` or `set of `str`
            The method to request.
        parameters : `None` or `tuple` of `tuple` (`str`, `Any`)
            Default parameters to call `view_func` with.
        """
        self._router.register_route(rule, 0, request_methods, parameters)
