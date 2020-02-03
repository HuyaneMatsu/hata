# -*- coding: utf-8 -*-
import base64
import binascii
import re
from collections import namedtuple
from urllib.parse import quote
from math import ceil
import socket as module_socket
from .futures import CancelledError, Future

CHAR = set(chr(i) for i in range(0, 128))
CTL = set(chr(i) for i in range(0, 32)) | {chr(127), }
SEPARATORS = {'(', ')', '<', '>', '@', ',', ';', ':', '\\', '"', '/', '[', ']',
              '?', '=', '{', '}', ' ', chr(9)}
TOKEN = CHAR ^ CTL ^ SEPARATORS

sentinel = object()

HttpVersion = namedtuple('HttpVersion',['major','minor'])
HttpVersion10 = HttpVersion(1,0)
HttpVersion11 = HttpVersion(1,1)

del namedtuple

class BasicAuth(object):
    #Http basic authentication helper.
    #login      = str
    #password   = str
    #encoding   = str ('latin1' by default)
    __slots__=('login','password','encoding',)
    
    def __new__(cls,login,password='',encoding='latin1'):
        if login is None:
            raise ValueError('None is not allowed as login value')

        if password is None:
            raise ValueError('None is not allowed as password value')

        if ':' in login:
            raise ValueError('A ":" is not allowed in login (RFC 1945#section-11.1)')
        
        self=object.__new__(cls)
        
        self.login=login
        self.password=password
        self.encoding=encoding
        
        return self

    @classmethod
    def decode(cls, auth_header, encoding='latin1'):
        #Create a BasicAuth object from an Authorization HTTP header.
        split=auth_header.strip().split(' ')
        if len(split)==2:
            if split[0].strip().lower()!='basic':
                raise ValueError(f'Unknown authorization method {split[0]}')
            to_decode=split[1]
        else:
            raise ValueError('Could not parse authorization header.')

        try:
            username,_,password=base64.b64decode(to_decode.encode('ascii')).decode(encoding).partition(':')
        except binascii.Error:
            raise ValueError('Invalid base64 encoding.')
        
        self=object.__new__(cls)
        self.login=username
        self.password=password
        self.encoding=encoding
        return self

    def encode(self):
        #Encode credentials.
        credits_=(f'{self.login}:{self.password}').encode(self.encoding)
        subv=base64.b64encode(credits_).decode(self.encoding)
        return f'Basic {subv}'

    def __repr__(self):
        return f'{self.__class__.__name__}(login={self.login}, password={self.password}, encoding={self.encoding})'

_ipv4_pattern = (
    '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
    '(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        )
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
_ipv4_regex     = re.compile(_ipv4_pattern)
_ipv6_regex     = re.compile(_ipv6_pattern, flags=re.IGNORECASE)
_ipv4_regexb    = re.compile(_ipv4_pattern.encode('ascii'))
_ipv6_regexb    = re.compile(_ipv6_pattern.encode('ascii'), flags=re.IGNORECASE)

del _ipv4_pattern,_ipv6_pattern,re

def is_ip_address(host):
    if host is None:
        return False
    if isinstance(host, str):
        if _ipv4_regex.match(host) or _ipv6_regex.match(host):
            return True
        else:
            return False
    elif isinstance(host, (bytes,bytearray,memoryview)):
        if _ipv4_regexb.match(host) or _ipv6_regexb.match(host):
            return True
        else:
            return False
    else:
        raise TypeError(f'{host} [{type(host)}] is not a str or bytes')


class EmptyTimer(object):
    __slots__=()
    def __enter__(self):
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        return False


class TimeoutHandle(object):
    __slots__=('callbacks', 'loop', 'timeout',)
    
    def __init__(self,loop,timeout):
        self.timeout    = timeout
        self.loop       = loop
        self.callbacks  = []

    def register(self,callback,*args,**kwargs):
        self.callbacks.append((callback,args,kwargs))

    def close(self):
        self.callbacks.clear()

    def start(self):
        if self.timeout is not None and self.timeout>0:
            
            at=ceil(self.loop.time()+self.timeout)
            return self.loop.call_at(at,self.__call__)

    def timer(self):
        if self.timeout is not None and self.timeout>0:
            timer=TimerContext(self.loop)
            self.register(timer.timeout)
        else:
            timer=EmptyTimer()
        return timer

    def __call__(self):
        for callback,args,kwargs in self.callbacks:
            try:
                callback(*args,**kwargs)
            except BaseException as err:
                self.loop.render_exc_async(err,[
                    'Exception occured at ',
                    self.__class__.__name__,
                    '.__call__\n'
                        ])

        self.callbacks.clear()

        
class Timeout(object):
    __slots__=('cancel_handler', 'cancelled', 'loop', 'task', 'timeout',)
    def __init__(self,loop,timeout):
        
        self.timeout        = timeout
        self.loop           = loop
        self.task           = None
        self.cancelled      = False
        self.cancel_handler = None

    def __enter__(self):
        self.task=self.loop.current_task
        if self.task is None:
            raise RuntimeError('Timeout context manager should be used inside a task')
        if self.timeout:
            self.cancel_handler=self.loop.call_later(self.timeout,self._cancel_task)
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        if exc_type in (CancelledError, GeneratorExit) and self.cancelled:
            self.cancel_handler=None
            self.task=None
            raise TimeoutError from None
        
        if self.timeout:
            self.cancel_handler.cancel()
            self.cancel_handler=None
        self.task=None

    def _cancel_task(self):
        self.cancelled=self.task.cancel()


class TimerContext(object):
    __slots__=('cancelled', 'loop', 'tasks',)
    #Low resolution timeout context manager

    def __init__(self,loop):
        self.loop       = loop
        self.tasks      = []
        self.cancelled  = False

    def __enter__(self):
        task=self.loop.current_task
        if task is None:
            raise RuntimeError('Timeout context manager should be used inside a task')

        if self.cancelled:
            task.cancel()
            raise TimeoutError from None

        self.tasks.append(task)
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        if self.tasks:
            self.tasks.pop()

        if exc_type in (CancelledError, GeneratorExit) and self.cancelled:
            raise TimeoutError from None

    def timeout(self):
        if not self.cancelled:
            for task in set(self.tasks):
                task.cancel()

            self.cancelled=True

            
class CeilTimeout(Timeout):
    def __enter__(self):
        if self.timeout:
            self.task=self.loop.current_task
            if self.task is None:
                raise RuntimeError('Timeout context manager should be used inside a task')
            self.cancel_handler=self.loop.call_at(ceil(self.loop.time()+self.timeout),self._cancel_task)
        return self

def content_disposition_header(disptype,params,quote_fields=True):
    #Sets Content-Disposition header.
    #
    #disptype is a disposition type: inline, attachment, form-data.
    #Should be valid extension token (see RFC 2183)
    #
    #params is a dict with disposition params.

    if not disptype or not (TOKEN>set(disptype)):
        raise ValueError(f'bad content disposition type {disptype!r}')
    value=disptype
    if params:
        param_parts=[value]
        for key,val in params.items():
            if not key or not (TOKEN>set(key)):
                raise ValueError(f'bad content disposition parameter {key!r}={val!r}')
            if quote_fields:
                val=quote(val,'')
                
            param_parts.append(f'{key}="{val}"')
            
            if key=='filename':
                param_parts.append(f'filename*=utf-8\'\'{val}')
                
        value='; '.join(param_parts)
    return value

def tcp_nodelay(transport,value):
    socket=transport.get_extra_info('socket')

    if socket is None:
        return

    if socket.family not in (module_socket.AF_INET,module_socket.AF_INET6):
        return

    value = bool(value)

    # socket may be closed already, on windows OSError get raised
    try:
        socket.setsockopt(module_socket.IPPROTO_TCP,module_socket.TCP_NODELAY,value)
    except OSError:
        pass

class EventResultOrError(object):
    __slots__=('exception', 'loop', 'waiter',)
    def __init__(self,loop):
        self.loop       = loop
        self.exception  = None
        self.waiter     = Future(loop)

    def set(self,exception=None):
        self.exception=exception
        self.waiter.set_result_if_pending(None)

    async def wait(self):
        value = await self.waiter
        exception=self.exception
        if exception is not None:
            raise exception
        return value

    def cancel(self):
        self.waiter.cancel()
