# -*- coding: utf-8 -*-
import re

from .utils import istr

METHOD_ANY = '*'
METHOD_CONNECT = 'CONNECT'
METHOD_HEAD = 'HEAD'
METHOD_GET = 'GET'
METHOD_DELETE = 'DELETE'
METHOD_OPTIONS = 'OPTIONS'
METHOD_PATCH = 'PATCH'
METHOD_POST = 'POST'
METHOD_PUT = 'PUT'
METHOD_TRACE = 'TRACE'

METHOD_GET_ALL = {METHOD_GET, METHOD_HEAD, METHOD_OPTIONS}
METHOD_POST_ALL = {METHOD_PATCH, METHOD_POST, METHOD_PUT}

METHOD_ALL = {METHOD_CONNECT, METHOD_HEAD, METHOD_GET, METHOD_DELETE, METHOD_OPTIONS, METHOD_PATCH, METHOD_POST,
    METHOD_PUT, METHOD_TRACE}


ACCEPT = istr('Accept')
ACCEPT_CHARSET = istr('Accept-Charset')
ACCEPT_ENCODING = istr('Accept-Encoding')
ACCEPT_LANGUAGE = istr('Accept-Language')
ACCEPT_RANGES = istr('Accept-Ranges')
ACCESS_CONTROL_MAX_AGE = istr('Access-Control-Max-Age')
ACCESS_CONTROL_ALLOW_CREDENTIALS = istr('Access-Control-Allow-Credentials')
ACCESS_CONTROL_ALLOW_HEADERS = istr('Access-Control-Allow-Headers')
ACCESS_CONTROL_ALLOW_METHODS = istr('Access-Control-Allow-Methods')
ACCESS_CONTROL_ALLOW_ORIGIN = istr('Access-Control-Allow-Origin')
ACCESS_CONTROL_EXPOSE_HEADERS = istr('Access-Control-Expose-Headers')
ACCESS_CONTROL_REQUEST_HEADERS = istr('Access-Control-Request-Headers')
ACCESS_CONTROL_REQUEST_METHOD = istr('Access-Control-Request-Method')
AGE = istr('Age')
ALLOW = istr('Allow')
AUTHORIZATION = istr('Authorization')
CACHE_CONTROL = istr('Cache-Control')
CONNECTION = istr('Connection')
CONTENT_DISPOSITION = istr('Content-Disposition')
CONTENT_ENCODING = istr('Content-Encoding')
CONTENT_LANGUAGE = istr('Content-Language')
CONTENT_LENGTH = istr('Content-Length')
CONTENT_LOCATION = istr('Content-Location')
CONTENT_MD5 = istr('Content-MD5')
CONTENT_RANGE = istr('Content-Range')
CONTENT_TRANSFER_ENCODING = istr('Content-Transfer-Encoding')
CONTENT_TYPE = istr('Content-Type')
COOKIE = istr('Cookie')
DATE = istr('Date')
DESTINATION = istr('Destination')
DIGEST = istr('Digest')
ETAG = istr('Etag')
EXPECT = istr('Expect')
EXPIRES = istr('Expires')
FORWARDED = istr('Forwarded')
FROM = istr('From')
HOST = istr('Host')
IF_MATCH = istr('If-Match')
IF_MODIFIED_SINCE = istr('If-Modified-Since')
IF_NONE_MATCH = istr('If-None-Match')
IF_RANGE = istr('If-Range')
IF_UNMODIFIED_SINCE = istr('If-Unmodified-Since')
KEEP_ALIVE = istr('Keep-Alive')
LAST_EVENT_ID = istr('Last-Event-ID')
LAST_MODIFIED = istr('Last-Modified')
LINK = istr('Link')
LOCATION = istr('Location')
MAX_FORWARDS = istr('Max-Forwards')
ORIGIN = istr('Origin')
PRAGMA = istr('Pragma')
PROXY_AUTHENTICATE = istr('Proxy-Authenticate')
PROXY_AUTHORIZATION = istr('Proxy-Authorization')
RANGE = istr('Range')
REFERER = istr('Referer')
RETRY_AFTER = istr('Retry-After')
SEC_WEBSOCKET_ACCEPT = istr('Sec-WebSocket-Accept')
SEC_WEBSOCKET_VERSION = istr('Sec-WebSocket-Version')
SEC_WEBSOCKET_PROTOCOL = istr('Sec-WebSocket-Protocol')
SEC_WEBSOCKET_EXTENSIONS = istr('Sec-WebSocket-Extensions')
SEC_WEBSOCKET_KEY = istr('Sec-WebSocket-Key')
SEC_WEBSOCKET_KEY1 = istr('Sec-WebSocket-Key1')
SERVER = istr('Server')
SET_COOKIE = istr('Set-Cookie')
TE = istr('TE')
TRAILER = istr('Trailer')
TRANSFER_ENCODING = istr('Transfer-Encoding')
UPGRADE = istr('Upgrade')
WEBSOCKET = istr('WebSocket')
URI = istr('URI')
USER_AGENT = istr('User-Agent')
VARY = istr('Vary')
VIA = istr('Via')
WANT_DIGEST = istr('Want-Digest')
WARNING = istr('Warning')
WWW_AUTHENTICATE = istr('WWW-Authenticate')
X_FORWARDED_FOR = istr('X-Forwarded-For')
X_FORWARDED_HOST = istr('X-Forwarded-Host')
X_FORWARDED_PROTO = istr('X-Forwarded-Proto')

_TOKEN_RP = re.compile(r'[-!#$%&\'*+.^_`|~0-9a-zA-Z]+')
_LIST_START_RP = re.compile('[\t ,]*')
_SPACE_RP = re.compile('[\t ]*')
_PROTOCOL_RP = re.compile(r'[-!#$%&\'*+.^_`|~0-9a-zA-Z]+(?:/[-!#$%&\'*+.^_`|~0-9a-zA-Z]+)?')

del re
del istr

def build_extensions(available_extensions):
    """
    Builds websocket extensions header from the given extension values.
    
    Parameters
    ----------
    available_extensions : `list` of `Any`
        Each websocket extension should have the following `4` attributes / methods:
        - `name`, type `str`. The extension's name.
        - `request_params` : `list` of `tuple` (`str`, `str`). Additional header parameters of the extension.
        - `decode` : `callable`. Decoder method, what processes a received websocket frame. Should accept `2`
            parameters: The respective websocket ``Frame``, and the ˙max_size` as `int`, what decides the
            maximal size of a received frame. If it is passed, ``PayloadError`` is raised.
        - `encode` : `callable`. Encoder method, what processes the websocket frames to send. Should accept `1`
            parameter, the respective websocket ``Frame``.
    
    Returns
    -------
    header_value : `str`
    """
    main_parts = []
    sub_parts = []
    
    for available_extension in available_extensions:
        name = available_extension.name
        parameters = available_extension.request_params
        
        sub_parts.append(name)
        for key, value in parameters:
            if value is None:
                sub_parts.append(key)
            else:
                sub_parts.append(f'{key}={value}')
        
        main_parts.append('; '.join(sub_parts))
        sub_parts.clear()
    
    return ', '.join(main_parts)

def parse_extensions(header_value):
    """
    Parses extension header.
    
    Parameters
    ----------
    header_value : `str`
        Received extension header.

    Returns
    -------
    result : `list` of `tuple` (`str`, `list` of `tuple` (`str`, `str`))
        The parsed out extensions as `name` - `parameters` pairs. The `parameters` are in `list` storing
        `key` - `value` pairs.
    
    Raises
    ------
    ValueError
        Extension header value is incorrect.
    """
    result = []
    limit = len(header_value)
    index = 0
    
    check_start = True
    
    while True:
        # parse till 1st element
        matched = _LIST_START_RP.match(header_value, index)
        index = matched.end()
        
        # are we at the end?
        if index == limit:
            return result
        
        # now lets parse the extension's name
        matched = _TOKEN_RP.match(header_value, index)
        if matched is None:
            raise ValueError(f'Expected extension name since index {index}.')
        name = matched.group(0)
        index = matched.end()
        
        # nice, we have a name, we can make our item now!
        sub_parts = []
        result.append((name, sub_parts,),)
        
        # should we parse a sublist?
        while True:
            
            # after half item we skip this part
            if check_start:
                # are we at the end?
                if index == limit:
                    return result
                
                # lets parse till next character
                matched = _SPACE_RP.match(header_value, index)
                index = matched.end()
                
                # are we at the end?
                if index == limit:
                    return result
                
                # no sublist?
                if header_value[index] == ',':
                    index += 1
                    break

                # invalid character
                if header_value[index] != ';':
                    raise ValueError(f'Expected \';\' at index {index}.')
                
                # we have a sublist
                index += 1
                
            else:
                check_start = True
            
            # parse space
            matched = _SPACE_RP.match(header_value, index)
            index = matched.end()
            
            # are we at the end?
            if index == limit:
                break
            
            # lets parse the key now
            matched = _TOKEN_RP.match(header_value, index)
            if matched is None:
                raise ValueError(f'Expected parameter name since index {index}.')
            key = matched.group(0)
            index = matched.end()
            
            # are we at the end?
            if index == limit:
                sub_parts.append((key, None,),)
                break
            
            # parse space
            matched = _SPACE_RP.match(header_value, index)
            index = matched.end()
            
            # are we at the end?
            if index == limit:
                sub_parts.append((key, None,),)
                break

            #is it a full item or a half?
            
            #next extension
            if header_value[index] == ',':
                sub_parts.append((key, None,),)
                index += 1
                break

            # next item
            if header_value[index] == ';':
                sub_parts.append((key, None,),)
                index += 1
                check_start = False
                continue

            #invalid character
            if header_value[index] != '=':
                raise ValueError(f'Expected \',\' or \';\' or \'=\' at index {index}.')
            
            index += 1
            
            # parse space
            matched = _SPACE_RP.match(header_value, index)
            index = matched.end()
            
            # are we at the end?
            if index == limit:
                raise ValueError('Expected a parameter value, but string ended.')
            
            # is it '"stuff"' ?
            if header_value[index] == '"':
                index += 1
                
                # are we at the end?
                if index == limit:
                    raise ValueError('Expected a parameter value, but string ended.')
                
                matched = _TOKEN_RP.match(header_value, index)
                if matched is None:
                    raise ValueError(f'Expected parameter value since index {index}.')
                value = matched.group(0)
                index = matched.end()
                
                # are we at the end? or did we finish the string normally?
                if index == limit or header_value[index] != '"':
                    raise ValueError('Expected a \'"\' after starting a value with \'"\'.')
                index += 1
            
            # is it 'stuff' ?
            else:
                matched = _TOKEN_RP.match(header_value, index)
                if matched is None:
                    raise ValueError(f'Expected parameter value since index {index}.')
                value = matched.group(0)
                index = matched.end()
            
            # we got a full item
            sub_parts.append((key, value,),)

def parse_connections(header_value):
    """
    Parses subprotocol or connection headers.
    
    Parameters
    ----------
    header_value : `str`
        Received subprotocol or connection header.
    
    Returns
    -------
    result : `list` of `str`
        The parsed subprotocol or connection headers.
    
    Raises
    ------
    ValueError
        Subprotocol or connection header value is incorrect.
    """
    result = []
    limit = len(header_value)
    index = 0
    
    while True:
        #parse till 1st element
        matched = _LIST_START_RP.match(header_value, index)
        index = matched.end()
        
        #are we at the end?
        if index == limit:
            return result
        
        #now lets parse the upgrade's name
        matched = _TOKEN_RP.match(header_value, index)
        if matched is None:
            raise ValueError(f'Expected upgrade type since index {index}.')
        name = matched.group(0)
        index = matched.end()

        #nice
        result.append(name)
        
        #are we at the end?
        if index == limit:
            return result

        #lets parse till next character
        matched = _SPACE_RP.match(header_value, index)
        index = matched.end()

        #are we at the end?
        if index == limit:
            return result
    
        #no sublist?
        if header_value[index] == ',':
            index += 1
            continue
        
        raise ValueError(f'Expected \',\' at index {index}.')

def build_subprotocols(subprotocols):
    """
    Builds websocket subprotocol headers from the given subprotocol values.
    
    Parameters
    ----------
    subprotocols : `list` of `str`
        A list of supported subprotocols.
    
    Returns
    -------
    header_value : `str`
    """
    return ', '.join(subprotocols)

parse_subprotocols = parse_connections # yes, these are the same

def parse_upgrades(header_value):
    """
    Parses upgrade headers.
    
    Parameters
    ----------
    header_value : `str`
        Received upgrade header.
    
    Returns
    -------
    result : `list` of `str`
        The parsed upgrade headers.
    
    Raises
    ------
    ValueError
        Upgrade header value is incorrect.
    """
    result = []
    limit = len(header_value)
    index = 0
    
    while True:
        # parse till 1st element
        matched = _LIST_START_RP.match(header_value, index)
        index = matched.end()
        
        # are we at the end?
        if index == limit:
            return result
        
        # now lets parse the upgrade's name
        matched = _PROTOCOL_RP.match(header_value, index)
        if matched is None:
            raise ValueError(f'Expected upgrade type since index {index}.')
        name = matched.group(0)
        index = matched.end()
        
        # nice
        result.append(name)
        
        # are we at the end?
        if index == limit:
            return result
        
        # lets parse till next character
        matched = _SPACE_RP.match(header_value, index)
        index = matched.end()
        
        # are we at the end?
        if index == limit:
            return result
        
        # no sublist?
        if header_value[index] == ',':
            index += 1
            continue
        
        raise ValueError(f'Expected \',\' at index {index}.')
