# -*- coding: utf-8 -*-
#HTTP Headers constants and some parsing
from .dereaddons_local import titledstr
import re
from base64 import b64encode

METH_ANY    = '*'
METH_CONNECT= 'CONNECT'
METH_HEAD   = 'HEAD'
METH_GET    = 'GET'
METH_DELETE = 'DELETE'
METH_OPTIONS= 'OPTIONS'
METH_PATCH  = 'PATCH'
METH_POST   = 'POST'
METH_PUT    = 'PUT'
METH_TRACE  = 'TRACE'

METH_ALL = {METH_CONNECT, METH_HEAD, METH_GET, METH_DELETE,
            METH_OPTIONS, METH_PATCH, METH_POST, METH_PUT, METH_TRACE}


ACCEPT = titledstr('Accept')
ACCEPT_CHARSET = titledstr('Accept-Charset')
ACCEPT_ENCODING = titledstr('Accept-Encoding')
ACCEPT_LANGUAGE = titledstr('Accept-Language')
ACCEPT_RANGES = titledstr('Accept-Ranges')
ACCESS_CONTROL_MAX_AGE = titledstr('Access-Control-Max-Age')
ACCESS_CONTROL_ALLOW_CREDENTIALS = titledstr('Access-Control-Allow-Credentials')
ACCESS_CONTROL_ALLOW_HEADERS = titledstr('Access-Control-Allow-Headers')
ACCESS_CONTROL_ALLOW_METHODS = titledstr('Access-Control-Allow-Methods')
ACCESS_CONTROL_ALLOW_ORIGIN = titledstr('Access-Control-Allow-Origin')
ACCESS_CONTROL_EXPOSE_HEADERS = titledstr('Access-Control-Expose-Headers')
ACCESS_CONTROL_REQUEST_HEADERS = titledstr('Access-Control-Request-Headers')
ACCESS_CONTROL_REQUEST_METHOD = titledstr('Access-Control-Request-Method')
AGE = titledstr('Age')
ALLOW = titledstr('Allow')
AUTHORIZATION = titledstr('Authorization')
CACHE_CONTROL = titledstr('Cache-Control')
CONNECTION = titledstr('Connection')
CONTENT_DISPOSITION = titledstr('Content-Disposition')
CONTENT_ENCODING = titledstr('Content-Encoding')
CONTENT_LANGUAGE = titledstr('Content-Language')
CONTENT_LENGTH = titledstr('Content-Length')
CONTENT_LOCATION = titledstr('Content-Location')
CONTENT_MD5 = titledstr('Content-MD5')
CONTENT_RANGE = titledstr('Content-Range')
CONTENT_TRANSFER_ENCODING = titledstr('Content-Transfer-Encoding')
CONTENT_TYPE = titledstr('Content-Type')
COOKIE = titledstr('Cookie')
DATE = titledstr('Date')
DESTINATION = titledstr('Destination')
DIGEST = titledstr('Digest')
ETAG = titledstr('Etag')
EXPECT = titledstr('Expect')
EXPIRES = titledstr('Expires')
FORWARDED = titledstr('Forwarded')
FROM = titledstr('From')
HOST = titledstr('Host')
IF_MATCH = titledstr('If-Match')
IF_MODIFIED_SINCE = titledstr('If-Modified-Since')
IF_NONE_MATCH = titledstr('If-None-Match')
IF_RANGE = titledstr('If-Range')
IF_UNMODIFIED_SINCE = titledstr('If-Unmodified-Since')
KEEP_ALIVE = titledstr('Keep-Alive')
LAST_EVENT_ID = titledstr('Last-Event-ID')
LAST_MODIFIED = titledstr('Last-Modified')
LINK = titledstr('Link')
LOCATION = titledstr('Location')
MAX_FORWARDS = titledstr('Max-Forwards')
ORIGIN = titledstr('Origin')
PRAGMA = titledstr('Pragma')
PROXY_AUTHENTICATE = titledstr('Proxy-Authenticate')
PROXY_AUTHORIZATION = titledstr('Proxy-Authorization')
RANGE = titledstr('Range')
REFERER = titledstr('Referer')
RETRY_AFTER = titledstr('Retry-After')
SEC_WEBSOCKET_ACCEPT = titledstr('Sec-WebSocket-Accept')
SEC_WEBSOCKET_VERSION = titledstr('Sec-WebSocket-Version')
SEC_WEBSOCKET_PROTOCOL = titledstr('Sec-WebSocket-Protocol')
SEC_WEBSOCKET_EXTENSIONS = titledstr('Sec-WebSocket-Extensions')
SEC_WEBSOCKET_KEY = titledstr('Sec-WebSocket-Key')
SEC_WEBSOCKET_KEY1 = titledstr('Sec-WebSocket-Key1')
SERVER = titledstr('Server')
SET_COOKIE = titledstr('Set-Cookie')
TE = titledstr('TE')
TRAILER = titledstr('Trailer')
TRANSFER_ENCODING = titledstr('Transfer-Encoding')
UPGRADE = titledstr('Upgrade')
WEBSOCKET = titledstr('WebSocket')
URI = titledstr('URI')
USER_AGENT = titledstr('User-Agent')
VARY = titledstr('Vary')
VIA = titledstr('Via')
WANT_DIGEST = titledstr('Want-Digest')
WARNING = titledstr('Warning')
WWW_AUTHENTICATE = titledstr('WWW-Authenticate')
X_FORWARDED_FOR = titledstr('X-Forwarded-For')
X_FORWARDED_HOST = titledstr('X-Forwarded-Host')
X_FORWARDED_PROTO = titledstr('X-Forwarded-Proto')

_TOKEN_RP       = re.compile(r'[-!#$%&\'*+.^_`|~0-9a-zA-Z]+')
_LIST_START_RP  = re.compile('[\t ,]*')
_SPACE_RP       = re.compile('[\t ]*')
_PROTOCOL_RP    = re.compile(r'[-!#$%&\'*+.^_`|~0-9a-zA-Z]+(?:/[-!#$%&\'*+.^_`|~0-9a-zA-Z]+)?')

del re
del titledstr

def build_extensions(available_extensions):
    main_parts=[]
    sub_parts=[]
    
    for available_extension in available_extensions:
        name=available_extension.name
        parameters=available_extension.request_params

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
    result=[]
    limit=len(data)
    index=0

    check_start=True
    
    while True:
        #parse till 1st element
        matched=_LIST_START_RP.match(data,index)
        index=matched.end()
        
        #are we at the end?
        if index==limit:
            return result
        
        #now lets parse the extension's name
        matched=_TOKEN_RP.match(data,index)
        if matched is None:
            raise ValueError(f'expected extension name since index {index}')
        name=matched.group(0)
        index=matched.end()
        
        #nice, we have a name, we can make our item now!
        sub_parts=[]
        result.append((name,sub_parts,),)

        #should we parse a sublist?
        while True:
            
            #after half item we skip this part
            if check_start:
                #are we at the end?
                if index==limit:
                    return result
                
                #lets parse till next character
                matched=_SPACE_RP.match(data,index)
                index=matched.end()
                
                #are we at the end?
                if index==limit:
                    return result
            
                #no sublist?
                if data[index]==',':
                    index=index+1
                    break

                #invalid character
                if data[index]!=';':
                    raise ValueError(f'exptected \';\' at index {index}')

                #we have a sublist
                index=index+1
                
            else:
                check_start=True
            
            #parse space
            matched=_SPACE_RP.match(data,index)
            index=matched.end()

            #are we at the end?
            if index==limit:
                break

            #lets parse the key now
            matched=_TOKEN_RP.match(data,index)
            if matched is None:
                raise ValueError(f'expected parameter name since index {index}')
            key=matched.group(0)
            index=matched.end()
            
            #are we at the end?
            if index==limit:
                sub_parts.append((key,None,),)
                break
            
            #parse space
            matched=_SPACE_RP.match(data,index)
            index=matched.end()

            #are we at the end?
            if index==limit:
                sub_parts.append((key,None,),)
                break

            #is it a full item or a half?
            
            #next extension
            if data[index]==',':
                sub_parts.append((key,None,),)
                index=index+1
                break

            #next item
            if data[index]==';':
                sub_parts.append((key,None,),)
                index=index+1
                check_start=False
                continue

            #invalid character
            if data[index]!='=':
                raise ValueError(f'expetced \',\' or \';\' or \'=\' at index {index}')
            
            index=index+1

            #parse space
            matched=_SPACE_RP.match(data,index)
            index=matched.end()

            #are we at the end?
            if index==limit:
                raise ValueError('expected a parameter value, but string ended')

            #is it '"stuff"' ?
            if data[index]=='"':
                index=index+1

                #are we at the end?
                if index==limit:
                    raise ValueError('expected a parameter value, but string ended')
            
                matched=_TOKEN_RP.match(data,index)
                if matched is None:
                    raise ValueError(f'expected parameter value since index {index}')
                value=matched.group(0)
                index=matched.end()

                #are we at the end? or did we finish the string normally?
                if index==limit or data[index]!='"':
                    raise ValueError('expected a \'"\' after starting a value with \'"\'')
                index=index+1
            
            #is it 'stuff' ?
            else:
                matched=_TOKEN_RP.match(data,index)
                if matched is None:
                    raise ValueError(f'expected parameter value since index {index}')
                value=matched.group(0)
                index=matched.end()

            #we got a full item
            sub_parts.append((key,value,),)

def parse_connections(data):
    result=[]
    limit=len(data)
    index=0

    while True:
        #parse till 1st element
        matched=_LIST_START_RP.match(data,index)
        index=matched.end()
        
        #are we at the end?
        if index==limit:
            return result
        
        #now lets parse the upgrade's name
        matched=_TOKEN_RP.match(data,index)
        if matched is None:
            raise ValueError(f'expected upgrade type since index {index}')
        name=matched.group(0)
        index=matched.end()

        #nice
        result.append(name)
        
        #are we at the end?
        if index==limit:
            return result

        #lets parse till next character
        matched=_SPACE_RP.match(data,index)
        index=matched.end()

        #are we at the end?
        if index==limit:
            return result
    
        #no sublist?
        if data[index]==',':
            index=index+1
            continue

        raise ValueError(f'exptected \',\' at index {index}')

def build_basic_auth(name,password):
    user_pass=f'{name}:{password}'
    credentials=b64encode(user_pass.encode()).decode()
    return f'Basic {credentials}'

def build_subprotocols(subprotocols):
    return ', '.join(subprotocols)

parse_subprotocols=parse_connections #yes, these are the same

def parse_upgrades(data):
    result=[]
    limit=len(data)
    index=0

    while True:
        #parse till 1st element
        matched=_LIST_START_RP.match(data,index)
        index=matched.end()
        
        #are we at the end?
        if index==limit:
            return result
        
        #now lets parse the upgrade's name
        matched=_PROTOCOL_RP.match(data,index)
        if matched is None:
            raise ValueError(f'expected upgrade type since index {index}')
        name=matched.group(0)
        index=matched.end()

        #nice
        result.append(name)
        
        #are we at the end?
        if index==limit:
            return result

        #lets parse till next character
        matched=_SPACE_RP.match(data,index)
        index=matched.end()

        #are we at the end?
        if index==limit:
            return result
    
        #no sublist?
        if data[index]==',':
            index=index+1
            continue

        raise ValueError(f'exptected \',\' at index {index}')
