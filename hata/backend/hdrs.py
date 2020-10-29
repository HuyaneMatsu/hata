# -*- coding: utf-8 -*-
#HTTP Headers constants and some parsing
import re
from base64 import b64encode

from .dereaddons_local import istr

METH_ANY = '*'
METH_CONNECT = 'CONNECT'
METH_HEAD = 'HEAD'
METH_GET = 'GET'
METH_DELETE = 'DELETE'
METH_OPTIONS = 'OPTIONS'
METH_PATCH = 'PATCH'
METH_POST = 'POST'
METH_PUT = 'PUT'
METH_TRACE = 'TRACE'

METH_GET_ALL = {METH_GET, METH_HEAD, METH_OPTIONS}
METH_POST_ALL = {METH_PATCH, METH_POST, METH_PUT}

METH_ALL = {METH_CONNECT, METH_HEAD, METH_GET, METH_DELETE, METH_OPTIONS, METH_PATCH, METH_POST, METH_PUT, METH_TRACE}


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
    main_parts = []
    sub_parts = []
    
    for available_extension in available_extensions:
        name = available_extension.name
        parameters = available_extension.request_params
        
        sub_parts.append(name)
        for key,value in parameters:
            if value is None:
                sub_parts.append(key)
            else:
                sub_parts.append(f'{key}={value}')
        
        main_parts.append('; '.join(sub_parts))
        sub_parts.clear()
    
    return ', '.join(main_parts)

def parse_extensions(data):
    result = []
    limit = len(data)
    index = 0
    
    check_start = True
    
    while True:
        # parse till 1st element
        matched = _LIST_START_RP.match(data, index)
        index = matched.end()
        
        # are we at the end?
        if index == limit:
            return result
        
        # now lets parse the extension's name
        matched = _TOKEN_RP.match(data, index)
        if matched is None:
            raise ValueError(f'expected extension name since index {index}')
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
                matched = _SPACE_RP.match(data, index)
                index = matched.end()
                
                # are we at the end?
                if index == limit:
                    return result
                
                # no sublist?
                if data[index] == ',':
                    index +=1
                    break

                # invalid character
                if data[index] != ';':
                    raise ValueError(f'exptected \';\' at index {index}')
                
                # we have a sublist
                index +=1
                
            else:
                check_start = True
            
            # parse space
            matched = _SPACE_RP.match(data, index)
            index = matched.end()
            
            # are we at the end?
            if index == limit:
                break
            
            # lets parse the key now
            matched = _TOKEN_RP.match(data, index)
            if matched is None:
                raise ValueError(f'expected parameter name since index {index}')
            key = matched.group(0)
            index = matched.end()
            
            # are we at the end?
            if index == limit:
                sub_parts.append((key, None,),)
                break
            
            # parse space
            matched = _SPACE_RP.match(data, index)
            index = matched.end()
            
            # are we at the end?
            if index == limit:
                sub_parts.append((key, None,),)
                break

            #is it a full item or a half?
            
            #next extension
            if data[index] == ',':
                sub_parts.append((key, None,),)
                index +=1
                break

            # next item
            if data[index] == ';':
                sub_parts.append((key, None,),)
                index +=1
                check_start = False
                continue

            #invalid character
            if data[index] != '=':
                raise ValueError(f'expetced \',\' or \';\' or \'=\' at index {index}')
            
            index +=1
            
            # parse space
            matched = _SPACE_RP.match(data, index)
            index = matched.end()
            
            # are we at the end?
            if index == limit:
                raise ValueError('expected a parameter value, but string ended')
            
            # is it '"stuff"' ?
            if data[index] == '"':
                index +=1
                
                # are we at the end?
                if index == limit:
                    raise ValueError('expected a parameter value, but string ended')
                
                matched = _TOKEN_RP.match(data, index)
                if matched is None:
                    raise ValueError(f'expected parameter value since index {index}')
                value = matched.group(0)
                index = matched.end()
                
                # are we at the end? or did we finish the string normally?
                if index == limit or data[index] != '"':
                    raise ValueError('expected a \'"\' after starting a value with \'"\'')
                index +=1
            
            # is it 'stuff' ?
            else:
                matched = _TOKEN_RP.match(data, index)
                if matched is None:
                    raise ValueError(f'expected parameter value since index {index}')
                value = matched.group(0)
                index = matched.end()
            
            # we got a full item
            sub_parts.append((key, value,),)

def parse_connections(data):
    result = []
    limit = len(data)
    index = 0
    
    while True:
        #parse till 1st element
        matched = _LIST_START_RP.match(data, index)
        index = matched.end()
        
        #are we at the end?
        if index == limit:
            return result
        
        #now lets parse the upgrade's name
        matched = _TOKEN_RP.match(data, index)
        if matched is None:
            raise ValueError(f'expected upgrade type since index {index}')
        name = matched.group(0)
        index = matched.end()

        #nice
        result.append(name)
        
        #are we at the end?
        if index == limit:
            return result

        #lets parse till next character
        matched = _SPACE_RP.match(data, index)
        index = matched.end()

        #are we at the end?
        if index == limit:
            return result
    
        #no sublist?
        if data[index] == ',':
            index +=1
            continue
        
        raise ValueError(f'exptected \',\' at index {index}')

def build_basic_auth(name,password):
    user_pass = f'{name}:{password}'
    credentials = b64encode(user_pass.encode()).decode()
    return f'Basic {credentials}'

def build_subprotocols(subprotocols):
    return ', '.join(subprotocols)

parse_subprotocols = parse_connections # yes, these are the same

def parse_upgrades(data):
    result = []
    limit = len(data)
    index = 0
    
    while True:
        # parse till 1st element
        matched = _LIST_START_RP.match(data, index)
        index = matched.end()
        
        # are we at the end?
        if index == limit:
            return result
        
        # now lets parse the upgrade's name
        matched = _PROTOCOL_RP.match(data, index)
        if matched is None:
            raise ValueError(f'expected upgrade type since index {index}')
        name = matched.group(0)
        index = matched.end()
        
        # nice
        result.append(name)
        
        # are we at the end?
        if index == limit:
            return result
        
        # lets parse till next character
        matched = _SPACE_RP.match(data, index)
        index = matched.end()
        
        # are we at the end?
        if index == limit:
            return result
        
        # no sublist?
        if data[index] == ',':
            index +=1
            continue
        
        raise ValueError(f'exptected \',\' at index {index}')
