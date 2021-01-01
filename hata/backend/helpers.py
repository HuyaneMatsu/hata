# -*- coding: utf-8 -*-
import base64, binascii, re
from collections import namedtuple
from urllib.parse import quote
import socket as module_socket

from .futures import CancelledError

CHAR = {chr(i) for i in range(0, 128)}
CTL = {*(chr(i) for i in range(0, 32)), chr(127)}
SEPARATORS = {'(', ')', '<', '>', '@', ', ', ';', ':', '\\', '"', '/', '[', ']', '?', '=', '{', '}', ' ', chr(9)}
TOKEN = CHAR ^ CTL ^ SEPARATORS

sentinel = object()

HttpVersion = namedtuple('HttpVersion', ('major', 'minor'))
HttpVersion10 = HttpVersion(1,0)
HttpVersion11 = HttpVersion(1,1)

del namedtuple

class BasicAuth(object):
    """
    Http basic authorization implementation.
    
    Attributes
    ----------
    username : `str`
        Authorization login username.
    password : `str`
        Authorization password. Can be empty string.
    encoding : `str`
        Encoding used to encode the authorization headers. Defaults to ``.DEFAULT_ENCODING``.
    
    Class Attributes
    ----------------
    DEFAULT_ENCODING : `str` = `'latin1'`
        Default encoding used to encode and decode the authorization headers.
    """
    DEFAULT_ENCODING = 'latin1'
    __slots__ = ('username', 'password', 'encoding',)
    
    def __new__(cls, username, password='', encoding=DEFAULT_ENCODING):
        """
        Creates a new ``BasicAuth`` instance with the given parameters.
        
        Attributes
        ----------
        username : `str`
            Authorization login name.
        password : `str`, Optional
            Authorization password. Can be empty string.
        encoding : `str`, Optional
            Encoding used to encode the authorization headers. Defaults to `'latin1'`.
        
        Raises
        ------
        ValueError
            If `username` is given as `None`.
            If `username` contains `':'` character.
            If password is given as `None`.
        """
        if username is None:
            raise ValueError('`None` is not allowed as `login` value.')
        
        if ':' in username:
            raise ValueError(f'`\':\'` is not allowed in `login` (RFC 1945#section-11.1), got {username!r}.')
        
        if password is None:
            raise ValueError('`None` is not allowed as `password` value.')
        
        self = object.__new__(cls)
        
        self.username = username
        self.password = password
        self.encoding = encoding
        
        return self
    
    @classmethod
    def decode(cls, auth_header, encoding=DEFAULT_ENCODING):
        """
        Creates a new ``BasicAuth`` instance from the given HTTP header value and.
        
        Parameters
        ----------
        auth_header : `str`
            Authorization header value.
        encoding : `str`, Optional
            Encoding used to encode the authorization headers. Defaults to `'latin1'`.
        
        Returns
        -------
        self : ``BasicAuth``.
        
        Raises
        ------
        ValueError
            If the authorization method is not `'basic'`.
            If cannot parse the authorization headers.
            Cannot decode authorization header.
        """
        split = auth_header.strip().split(' ')
        if len(split) == 2:
            if split[0].strip().lower() != 'basic':
                raise ValueError(f'Unknown authorization method: {split[0]!r}.')
            to_decode = split[1]
        else:
            raise ValueError(f'Could not parse authorization header from: {auth_header!r}.')
        
        try:
            username, _, password = base64.b64decode(to_decode.encode('ascii')).decode(encoding).partition(':')
        except binascii.Error as err:
            raise ValueError('Invalid base64 encoding.') from err
        
        self = object.__new__(cls)
        self.username = username
        self.password = password
        self.encoding = encoding
        return self
    
    def encode(self):
        """
        Encodes the authorization to it's header value.
        
        Returns
        -------
        auth_header : `str`
        """
        credits_ = (f'{self.username}:{self.password}').encode(self.encoding)
        sub_value = base64.b64encode(credits_).decode(self.encoding)
        return f'Basic {sub_value}'
    
    def __repr__(self):
        """Returns the basic auth's representation."""
        result = [
            self.__class__.__name__,
            '(username=',
            repr(self.username),
                ]
        
        password = self.password
        if password:
            result.append(', password=')
            result.append(repr(password))
        
        encoding = self.encoding
        if encoding != self.DEFAULT_ENCODING:
            result.append(' encoding=')
            result.append(repr(encoding))
        
        result.append(')')
        
        return ''.join(result)

_ipv4_pattern = '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
_ipv6_pattern = (
    '^(?:(?:(?:[A-F0-9]{1,4}:){6}|(?=(?:[A-F0-9]{0,4}:){0,6}'
    '(?:[0-9]{1,3}\.){3}[0-9]{1,3}$)(([0-9A-F]{1,4}:){0,5}|:)'
    '((:[0-9A-F]{1,4}){1,5}:|:)|::(?:[A-F0-9]{1,4}:){5})'
    '(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}'
    '(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])|(?:[A-F0-9]{1,4}:){7}'
    '[A-F0-9]{1,4}|(?=(?:[A-F0-9]{0,4}:){0,7}[A-F0-9]{0,4}$)'
    '(([0-9A-F]{1,4}:){1,7}|:)((:[0-9A-F]{1,4}){1,7}|:)|(?:[A-F0-9]{1,4}:){7}'
    ':|:(:[A-F0-9]{1,4}){7})$'
        )

_ipv4_regex = re.compile(_ipv4_pattern)
_ipv6_regex = re.compile(_ipv6_pattern, flags=re.I)
_ipv4_regex_b = re.compile(_ipv4_pattern.encode('ascii'))
_ipv6_regex_b = re.compile(_ipv6_pattern.encode('ascii'), flags=re.I)

del _ipv4_pattern, _ipv6_pattern, re

def is_ip_address(host):
    """
    Returns whether the given `host` is an ip address.
    
    Parameters
    ----------
    host : `str` or `bytes-like`
        Host value.
    
    Returns
    -------
    is_ip_address : `bool`
    
    Raises
    ------
    TypeError
        If `host` was not given neither as `str`, or as `bytes-like`.
    """
    if host is None:
        return False
    
    if isinstance(host, str):
        if _ipv4_regex.match(host) is not None:
            return True
        
        if _ipv6_regex.match(host) is not None:
            return True
        
        return False
        
    if isinstance(host, (bytes, bytearray, memoryview)):
        if _ipv4_regex_b.match(host) is not None:
            return True
        
        if _ipv6_regex_b.match(host) is not None:
            return True
        
        return False
    
    raise TypeError(f'`host` should be given as `str` or as `bytes-like`, got {host.__class__.__name__}.')


TIMEOUT_STATE_NONE = 0
TIMEOUT_STATE_TIMEOUTED = 1
TIMEOUT_STATE_CANCELLED = 2
TIMEOUT_STATE_EXITED = 3

class Timeout(object):
    """
    Implements async timeout feature as a context manager.
    
    Attributes
    ----------
    _handle : `None` or ``TimerHandle``
        Timer handle to cancel the respective task when it occurs. After timeout occurs, or the timeouter is
        cancelled, set as `None`.
    _loop : ``EventThread``
        The event loop to what the timeouter is bound to.
    _task : `None` or ``Task``
        The respective task what will be cancelled. Set as `None` at creation and when cancelled or exited.
    _state : `int`
        The timeouter's state.
        
        Can be one of the following:
        +---------------------------+-------+
        | Respective name           | Value |
        +===========================+=======+
        | TIMEOUT_STATE_NONE        | 0     |
        +---------------------------+-------+
        | TIMEOUT_STATE_TIMEOUTED   | 1     |
        +---------------------------+-------+
        | TIMEOUT_STATE_CANCELLED   | 2     |
        +---------------------------+-------+
        | TIMEOUT_STATE_EXITED      | 3     |
        +---------------------------+-------+
    """
    __slots__ = ('_handle', '_loop', '_task', '_state')
    def __new__(cls, loop, timeout):
        """
        Creates a new timeouter instance bound to the given loop.
        
        The timeout starts when the timeouter is created.
        
        Parameters
        ----------
        loop : ``EventThread``
            The event loop to what the timeouter will be bound to.
        timeout : `float`
            Time in seconds after the task is cancelled. When the cancellation reaches the context manager, raises
            `TimeoutError` instead.
        """
        self = object.__new__(cls)
        self._loop = loop
        self._handle = loop.call_later(timeout, cls._timeout, self)
        self._task = None
        self._state = TIMEOUT_STATE_NONE
        return self
    
    def cancel(self):
        """
        Cancels the timeouter.
        
        If already cancelled, does nothing.
        """
        if self._state == TIMEOUT_STATE_CANCELLED:
            return
        
        self._state = TIMEOUT_STATE_CANCELLED
        
        handle = self._handle
        if (handle is not None):
            self._handle = None
            handle.cancel()
        
        self._task = None
    
    def __enter__(self):
        """
        Enters the timeouter as a context manager.
        
        Returns
        -------
        self : ``Timeout``
        
        Raises
        ------
        RuntimeError
            ``Timeout`` entered outside of a ``Task``.
        TimeoutError
            Timeout already occurred.
        """
        task = self._loop.current_task
        if (task is None):
            raise RuntimeError('`Timeout` entered outside of a `Task`!')
        
        state = self._state
        if state == TIMEOUT_STATE_NONE:
            self._task = task
        elif state == TIMEOUT_STATE_TIMEOUTED:
            raise TimeoutError
        elif state == TIMEOUT_STATE_CANCELLED:
            pass
        else:
            raise RuntimeError('`Timeout` already used up.')
        
        return self
    
    def _timeout(self):
        """
        Timeouts the timeouter if not yet timeouted nor cancelled.
        """
        if self._state != TIMEOUT_STATE_NONE:
            return
        
        self._state = TIMEOUT_STATE_TIMEOUTED
        
        handle = self._handle
        if (handle is not None):
            self._handle = None
        
        task = self._task
        if (task is not None):
            task.cancel()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits from the timeouter. If the timeout occurs, then raises ``TimeoutError`` from the received cancellation.
        """
        handle = self._handle
        if (handle is not None):
            self._handle = None
            handle.cancel()
        
        self._task = None
        
        state = self._state
        self._state = TIMEOUT_STATE_EXITED
        if (state == TIMEOUT_STATE_TIMEOUTED) and (exc_type is CancelledError):
            raise TimeoutError from None
        
        return False
    
    def __repr__(self):
        return f'<{self.__class__.__name__}>'


def content_disposition_header(disposition_type, parameters, quote_fields=True):
    """
    Creates Content-Disposition header value.
    
    Parameters
    ----------
    disposition_type : `str`
        Disposition type. Can be one of following: `'inline'`, `'attachment'`, '`form-data`'.
    parameters : `dict` of (`str`, `str`) items
        Disposition parameters.
    quote_fields : `bool`
        Whether field values should be quoted.
    
    Returns
    -------
    value : `str`
    """
    if not disposition_type or not (TOKEN > set(disposition_type)):
        raise ValueError(f'Bad content disposition type {disposition_type!r}.')
    
    if parameters:
        parameter_parts = [disposition_type]
        for key, value in parameters.items():
            if (not key) or (not (TOKEN > set(key))):
                raise ValueError(f'Bad content disposition parameter {key!r}={value!r}.')
            
            if quote_fields:
                value = quote(value, '')
            
            parameter_parts.append(f'{key}="{value}"')
            
            if key == 'filename':
                parameter_parts.append(f'filename*=utf-8\'\'{value}')
        
        value = '; '.join(parameter_parts)
    else:
        value = disposition_type
    
    return value

def tcp_nodelay(transport, value):
    """
    Sets or removes tcp nodelay socket option to the given transport's socket if applicable.
    
    Parameters
    ----------
    transport : `Any`
        Asynchronous transport implementation.
    value : `bool`
        Value to set tcp nodelay to.
    """
    socket = transport.get_extra_info('socket')
    
    if socket is None:
        return
    
    if socket.family not in (module_socket.AF_INET, module_socket.AF_INET6):
        return
    
    # socket may be closed already, on windows OSError get raised
    try:
        socket.setsockopt(module_socket.IPPROTO_TCP, module_socket.TCP_NODELAY, value)
    except OSError:
        pass
