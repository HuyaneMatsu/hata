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
    # Http basic authentication helper.
    # login      = str
    # password   = str
    # encoding   = str ('latin1' by default)
    __slots__ = ('login', 'password', 'encoding',)
    
    def __new__(cls, login, password='', encoding='latin1'):
        if login is None:
            raise ValueError('None is not allowed as login value')
        
        if password is None:
            raise ValueError('None is not allowed as password value')
        
        if ':' in login:
            raise ValueError('A ":" is not allowed in login (RFC 1945#section-11.1)')
        
        self = object.__new__(cls)
        
        self.login = login
        self.password = password
        self.encoding = encoding
        
        return self
    
    @classmethod
    def decode(cls, auth_header, encoding='latin1'):
        # Create a BasicAuth object from an Authorization HTTP header.
        split = auth_header.strip().split(' ')
        if len(split) == 2:
            if split[0].strip().lower() != 'basic':
                raise ValueError(f'Unknown authorization method {split[0]}')
            to_decode = split[1]
        else:
            raise ValueError('Could not parse authorization header.')
        
        try:
            username, _, password = base64.b64decode(to_decode.encode('ascii')).decode(encoding).partition(':')
        except binascii.Error:
            raise ValueError('Invalid base64 encoding.')
        
        self = object.__new__(cls)
        self.login = username
        self.password = password
        self.encoding = encoding
        return self
    
    def encode(self):
        # Encode credentials.
        credits_ = (f'{self.login}:{self.password}').encode(self.encoding)
        subv = base64.b64encode(credits_).decode(self.encoding)
        return f'Basic {subv}'
    
    def __repr__(self):
        return f'{self.__class__.__name__}(login={self.login}, password={self.password}, encoding={self.encoding})'

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
_ipv6_regex = re.compile(_ipv6_pattern, flags=re.IGNORECASE)
_ipv4_regexb = re.compile(_ipv4_pattern.encode('ascii'))
_ipv6_regexb = re.compile(_ipv6_pattern.encode('ascii'), flags=re.IGNORECASE)

del _ipv4_pattern,_ipv6_pattern,re

def is_ip_address(host):
    if host is None:
        return False
    
    if isinstance(host, str):
        if _ipv4_regex.match(host) or _ipv6_regex.match(host):
            return True
        else:
            return False
        
    if isinstance(host, (bytes,bytearray,memoryview)):
        if _ipv4_regexb.match(host) or _ipv6_regexb.match(host):
            return True
        else:
            return False
    
    raise TypeError(f'{host} [{type(host)}] is not a str or bytes')


class Timeout(object):
    __slots__ = ('_handle', '_loop', '_task', '_timeouted')
    def __new__(cls, loop, timeout):
        self = object.__new__(cls)
        self._loop = loop
        self._handle = loop.call_later(timeout, cls._cancel, self)
        self._task = None
        self._timeouted = False
        return self
    
    def cancel(self):
        handle = self._handle
        if handle is None:
            return
        
        handle.cancel()
        self._handle = None
        self._task = None
    
    def __enter__(self):
        if (self._handle is None):
            raise TimeoutError from None
        
        task = self._loop.current_task
        if (task is None):
            raise RuntimeError('Timeout should be used inside a task!')
        
        self._task = task
        return self
    
    def _cancel(self):
        handle = self._handle
        if handle is None:
            return
        
        self._handle = None
        
        self._timeouted = True
        
        task = self._task
        if task is None:
            return
        
        task.cancel()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        handle = self._handle
        if (handle is not None):
            self._handle = None
            handle.cancel()
        
        self._task = None
        
        if self._timeouted and (exc_type is CancelledError):
            raise TimeoutError from None
        
        return False
    
    def __repr__(self):
        return f'<{self.__class__.__name__}>'


def content_disposition_header(disptype, params, quote_fields=True):
    # Sets Content-Disposition header.
    #
    # disptype is a disposition type: inline, attachment, form-data.
    # Should be valid extension token (see RFC 2183)
    #
    # params is a dict with disposition params.

    if not disptype or not (TOKEN > set(disptype)):
        raise ValueError(f'bad content disposition type {disptype!r}')
    value = disptype
    if params:
        param_parts = [value]
        for key, val in params.items():
            if not key or not (TOKEN > set(key)):
                raise ValueError(f'bad content disposition parameter {key!r}={val!r}')
            if quote_fields:
                val = quote(val, '')
            
            param_parts.append(f'{key}="{val}"')
            
            if key == 'filename':
                param_parts.append(f'filename*=utf-8\'\'{val}')
                
        value = '; '.join(param_parts)
    return value

def tcp_nodelay(transport, value):
    socket = transport.get_extra_info('socket')
    
    if socket is None:
        return
    
    if socket.family not in (module_socket.AF_INET, module_socket.AF_INET6):
        return
    
    value = bool(value)
    
    # socket may be closed already, on windows OSError get raised
    try:
        socket.setsockopt(module_socket.IPPROTO_TCP, module_socket.TCP_NODELAY, value)
    except OSError:
        pass
