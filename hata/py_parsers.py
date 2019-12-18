# -*- coding: utf-8 -*-
from .dereaddons_local import multidict_titled
from .py_exceptions import PayloadError,ContentEncodingError,PayloadError
from . import py_hdrs as hdrs
from .py_streams import StreamReader,EMPTY_PAYLOAD
from collections import namedtuple
from .py_url import URL
import re
import string
from .py_helpers import HttpVersion
import zlib

CONTENT_LENGTH=hdrs.CONTENT_LENGTH

try:
    import brotli
except ImportError:
    brotli=None

RawRequestMessage=namedtuple('RawRequestMessage',
    ['method', 'path', 'version', 'headers', 'raw_headers',
     'should_close', 'compression', 'upgrade', 'chunked', 'url'])

RawResponseMessage = namedtuple('RawResponseMessage',
    ['version', 'code', 'reason', 'headers', 'raw_headers',
     'should_close', 'compression', 'upgrade', 'chunked'])

ASCIISET= set(string.printable)
METHRE  = re.compile('[A-Z0-9$-_.]+')
VERSRE  = re.compile(r'HTTP/(\d+).(\d+)')
HDRRE   = re.compile(rb'[\x00-\x1F\x7F()<>@,;:\[\]={} \t\\\\\"]')

PARSESTATE_NONE              = 'a'
PARSESTATE_LENGTH            = 'b'
PARSESTATE_CHUNKED           = 'c'
PARSESTATE_UNTIL_EOF         = 'd'

PARSESTATE_CHUNKED_SIZE      = 'e'
PARSESTATE_CHUNKED_CHUNK     = 'f'
PARSESTATE_CHUNKED_CHUNK_EOF = 'g'
PARSESTATE_MAYBE_TRAILERS    = 'h'
PARSESTATE_TRAILERS          = 'i'

del namedtuple, re

class HttpParser:
    __slots__=['auto_decompress', 'code', 'lines', 'loop', 'max_field_size',
        'max_headers', 'max_line_size', 'method', 'payload', 'payload_error',
        'payload_parser', 'protocol', 'readall', 'read_until_eof',
        'response_w_body', 'tail', 'timer', 'upgraded']

    def __init__(self,protocol=None,loop=None, max_line_size=8190,
            max_headers=32768, max_field_size=8190, timer=None, code=None,
            method=None, readall=False, payload_error=None,
            response_w_body=True, read_until_eof=False,auto_decompress=True):

        self.loop           = loop        
        self.protocol       = protocol
        self.max_line_size  = max_line_size
        self.max_headers    = max_headers
        self.max_field_size = max_field_size
        self.timer          = timer
        self.code           = code
        self.method         = method
        self.readall        = readall
        self.payload_error  = payload_error
        self.response_w_body= response_w_body
        self.read_until_eof = read_until_eof

        self.lines          = []
        self.tail           = b''
        self.upgraded       = False
        self.payload        = None
        self.payload_parser = None
        self.auto_decompress= auto_decompress

    def feed_eof(self):
        if self.payload_parser is None:
            # try to extract partial message
            if self.tail:
                self.lines.append(self.tail)

            if self.lines:
                if self.lines[-1]!='\r\n':
                    self.lines.append(b'')
                try:
                    return self.parse_message(self.lines)
                except (AttributeError,NameError):
                    raise #for testing
                except Exception:
                    return None
        else:
            self.payload_parser.feed_eof()
            self.payload_parser = None
            
    def feed_data(self,data,
                  SEP=b'\r\n',EMPTY=b'',
                  SEC_WEBSOCKET_KEY1=hdrs.SEC_WEBSOCKET_KEY1):

        if self.tail:
            data=self.tail+data
            self.tail=b''
        
        messages    = []
        data_len    = len(data)
        start_pos   = 0
        loop        = self.loop

        while start_pos<data_len:

            # read HTTP message (request/response line + headers), \r\n\r\n
            # and split by lines
            if self.payload_parser is None and not self.upgraded:
                pos=data.find(SEP,start_pos)
                # consume \r\n
                if pos==start_pos and not self.lines:
                    start_pos=pos+2
                    continue

                if pos>=start_pos:
                    # line found
                    self.lines.append(data[start_pos:pos])
                    start_pos=pos+2

                    # \r\n\r\n found
                    if self.lines[-1]==EMPTY:
                        try:
                            message=self.parse_message(self.lines)
                        finally:
                            self.lines.clear()

                        # payload length
                        length = message.headers.get(CONTENT_LENGTH)
                        if length is not None:
                            try:
                                length = int(length)
                            except ValueError:
                                raise ValueError(CONTENT_LENGTH)
                            if length < 0:
                                raise ValueError(CONTENT_LENGTH)

                        # do not support old websocket spec
                        if SEC_WEBSOCKET_KEY1 in message.headers:
                            raise ValueError(SEC_WEBSOCKET_KEY1)

                        self.upgraded=message.upgrade
                        method=getattr(message,'method',self.method)

                        # calculate payload
                        if ((length is not None and length>0) or
                                message.chunked and not message.upgrade):
                            payload=StreamReader(self.protocol,loop,timer=self.timer)
                            payload_parser=HttpPayloadParser(
                                payload,length=length,
                                chunked=message.chunked,method=method,
                                compression=message.compression,
                                code=self.code,readall=self.readall,
                                response_w_body=self.response_w_body,
                                auto_decompress=self.auto_decompress)
                            if not payload_parser.done:
                                self.payload_parser=payload_parser
                        elif method==hdrs.METH_CONNECT:
                            payload=StreamReader(self.protocol,loop,timer=self.timer)
                            self.upgraded = True
                            self.payload_parser=HttpPayloadParser(
                                payload,method=message.method,
                                compression=message.compression,readall=True,
                                auto_decompress=self.auto_decompress)
                        else:
                            if (getattr(message,'code',100)>=199 and
                                    length is None and self.read_until_eof):
                                payload=StreamReader(self.protocol,loop,timer=self.timer)
                                payload_parser=HttpPayloadParser(
                                    payload, length=length,
                                    chunked=message.chunked, method=method,
                                    compression=message.compression,
                                    code=self.code,readall=True,
                                    response_w_body=self.response_w_body,
                                    auto_decompress=self.auto_decompress)
                                if not payload_parser.done:
                                    self.payload_parser=payload_parser
                            else:
                                payload=EMPTY_PAYLOAD

                        messages.append((message,payload))
                else:
                    self.tail=data[start_pos:]
                    data=EMPTY
                    break

            # no parser, just store
            elif self.payload_parser is None and self.upgraded:
                break

            # feed payload
            elif data and start_pos<data_len:
                try:
                    eof,data = self.payload_parser.feed_data(data[start_pos:])
                except BaseException as err:
                    if self.payload_error is None:
                        self.payload_parser.payload.set_exception(err)
                    else:
                        self.payload_parser.payload.set_exception(self.payload_error(str(err)))

                    eof  = True
                    data = b''

                if eof:
                    start_pos = 0
                    data_len  = len(data)
                    self.payload_parser = None
                    continue
            else:
                break

        if data and start_pos<data_len:
            data=data[start_pos:]
        else:
            data=EMPTY

        return messages,self.upgraded,data

    def parse_headers(self,lines):
        #Parses RFC 5322 headers from a stream.
        #
        #Line continuations are supported. Returns list of header name
        #and value pairs. Header name is in upper case.

        headers     = multidict_titled()
        raw_headers = []

        line_index  = 1
        line        = lines[1]
        line_count  = len(lines)

        while line:
            # Parse initial header name : value pair.
            try:
                bname, bvalue = line.split(b':', 1)
            except ValueError:
                raise ValueError(line) from None

            bname = bname.strip(b' \t')
            bvalue = bvalue.lstrip()
            if HDRRE.search(bname):
                raise ValueError(bname)
            if len(bname) > self.max_field_size:
                raise PayloadError(f'request header name {bname.decode("utf8", "xmlcharrefreplace")}',
                    self.max_field_size,len(bname))
            header_length=len(bvalue)

            # next line
            line_index  = line_index+1
            line        = lines[line_index]

            # consume continuation lines
            continuation = line and line[0] in (32,9)  # (' ', '\t')

            if continuation:
                bvalue = [bvalue]
                while continuation:
                    header_length+=len(line)
                    if header_length > self.max_field_size:
                        raise PayloadError(f'request header field {bname.decode("utf8", "xmlcharrefreplace")}',
                            self.max_field_size,header_length)
                    bvalue.append(line)

                    # next line
                    line_index+=1
                    if line_index<line_count:
                        line = lines[line_index]
                        if line:
                            continuation=line[0] in (32,9)  # (' ', '\t')
                    else:
                        line=b''
                        break
                bvalue = b''.join(bvalue)
            else:
                if header_length > self.max_field_size:
                    raise PayloadError(f'request header field {bname.decode("utf8", "xmlcharrefreplace")}',
                        self.max_field_size,header_length)

            bvalue  = bvalue.strip()
            name    = bname.decode('utf-8','surrogateescape')
            value   = bvalue.decode('utf-8','surrogateescape')

            headers[name]=value
            raw_headers.append((bname,bvalue),)

        close_conn  = None
        encoding    = None
        upgrade     = False
        chunked     = False
        raw_headers = tuple(raw_headers)

        # keep-alive
        connnection=headers.get(hdrs.CONNECTION)
        if connnection:
            v=connnection.lower()
            if v=='close':
                close_conn=True
            elif v=='keep-alive':
                close_conn=False
            elif v=='upgrade':
                upgrade=True

        # encoding
        enc=headers.get(hdrs.CONTENT_ENCODING)
        if enc:
            enc = enc.lower()
            if enc in ('gzip', 'deflate', 'br'):
                encoding = enc

        # chunking
        te = headers.get(hdrs.TRANSFER_ENCODING)
        if te and 'chunked' in te.lower():
            chunked = True

        return headers, raw_headers, close_conn, encoding, upgrade, chunked

    def parse_message(self,lines):
        pass
    
class HttpPayloadParser:
    __slots__=['auto_decompress', 'chunk', 'chunk_size', 'chunk_tail', 'done',
        'length', 'payload', 'type']
    def __init__(self, payload,
                 length=None, chunked=False, compression=None,code=None, method=None,
                 readall=False, response_w_body=True, auto_decompress=True):
        
        self.payload        = payload
        self.length         = 0
        self.type           = PARSESTATE_NONE
        self.chunk          = PARSESTATE_CHUNKED_SIZE
        self.chunk_size     = 0
        self.chunk_tail     = b''
        self.auto_decompress= auto_decompress
        self.done           = False

        # payload decompression wrapper
        if response_w_body and compression and self.auto_decompress:
            payload=DeflateBuffer(payload,compression)

        # payload parser
        if not response_w_body:
            # don't parse payload if it's not expected to be received
            self.type=PARSESTATE_NONE
            payload.feed_eof()
            self.done=True

        elif chunked:
            self.type=PARSESTATE_CHUNKED
        elif length is not None:
            self.type=PARSESTATE_LENGTH
            self.length=length
            if self.length==0:
                payload.feed_eof()
                self.done=True
        else:
            if readall and code!=204:
                self.type=PARSESTATE_UNTIL_EOF
            elif method in ('PUT','POST'):
                self.type=PARSESTATE_NONE
                payload.feed_eof()
                self.done=True

        self.payload=payload

    def feed_eof(self):
        if self.type is PARSESTATE_UNTIL_EOF:
            self.payload.feed_eof()
        elif self.type is PARSESTATE_LENGTH:
            raise PayloadError('Not enough data for satisfy content length header.')
        elif self.type is PARSESTATE_CHUNKED:
            raise ContentEncodingError('Not enough data for satisfy transfer length header.')

    def feed_data(self,chunk,SEP=b'\r\n',CHUNK_EXT=b';'):
        #Read specified amount of bytes
        if self.type is PARSESTATE_LENGTH:
            required=self.length
            chunk_len=len(chunk)

            if required>=chunk_len:
                self.length=required-chunk_len
                self.payload.feed_data(chunk,chunk_len)
                if self.length==0:
                    self.payload.feed_eof()
                    return True,b''
            else:
                self.length=0
                self.payload.feed_data(chunk[:required],required)
                self.payload.feed_eof()
                return True,chunk[required:]

        #Chunked transfer encoding parser
        elif self.type is PARSESTATE_CHUNKED:
            if self.chunk_tail:
                chunk=self.chunk_tail+chunk
                self.chunk_tail=b''

            while chunk:
                # read next chunk size
                if self.chunk is PARSESTATE_CHUNKED_SIZE:
                    pos=chunk.find(SEP)
                    if pos>=0:
                        i=chunk.find(CHUNK_EXT,0,pos)
                        if i>=0:
                            size_b=chunk[:i]  #strip chunk-extensions
                        else:
                            size_b=chunk[:pos]

                        try:
                            size=int(bytes(size_b),16)
                        except ValueError:
                            exception=ContentEncodingError(chunk[:pos])
                            self.payload.set_exception(exception)
                            raise exception from None

                        chunk=chunk[pos+2:]
                        if size:
                            self.chunk=PARSESTATE_CHUNKED_CHUNK
                            self.chunk_size=size
                            self.payload.begin_http_chunk_receiving()
                        else:#eof marker
                            self.chunk=PARSESTATE_MAYBE_TRAILERS

                    else:
                        self.chunk_tail=chunk
                        return False,b''

                #read chunk and feed buffer
                if self.chunk is PARSESTATE_CHUNKED_CHUNK:
                    required=self.chunk_size
                    chunk_len=len(chunk)

                    if required>chunk_len:
                        self.chunk_size=required-chunk_len
                        self.payload.feed_data(chunk,chunk_len)
                        return False,b''
                    else:
                        self.chunk_size=0
                        self.payload.feed_data(chunk[:required],required)
                        chunk=chunk[required:]
                        self.chunk=PARSESTATE_CHUNKED_CHUNK_EOF
                        self.payload.end_http_chunk_receiving()

                #toss the CRLF at the end of the chunk
                if self.chunk is PARSESTATE_CHUNKED_CHUNK_EOF:
                    if chunk[:2]==SEP:
                        chunk=chunk[2:]
                        self.chunk=PARSESTATE_CHUNKED_SIZE
                    else:
                        self.chunk_tail=chunk
                        return False,b''

                #if stream does not contain trailer, after 0\r\n
                #we should get another \r\n otherwise
                #trailers needs to be skiped until \r\n\r\n
                if self.chunk is PARSESTATE_MAYBE_TRAILERS:
                    if chunk[:2]==SEP:
                        # end of stream
                        self.payload.feed_eof()
                        return True,chunk[2:]
                    else:
                        self.chunk=PARSESTATE_TRAILERS

                #read and discard trailer up to the CRLF terminator
                if self.chunk is PARSESTATE_TRAILERS:
                    pos=chunk.find(SEP)
                    if pos>=0:
                        chunk=chunk[pos+2:]
                        self.chunk=PARSESTATE_MAYBE_TRAILERS
                    else:
                        self.chunk_tail=chunk
                        return False,b''

        #Read all bytes until eof
        elif self.type is PARSESTATE_UNTIL_EOF:
            self.payload.feed_data(chunk,len(chunk))

        return False,b''
    
class DeflateBuffer:
    __slots__=['decompressor', 'encoding', 'out', 'size', 'started']
    #DeflateStream decompress stream and feed data into specified stream.
    
    def __init__(self, out, encoding):
        self.out        = out
        self.size       = 0
        self.encoding   = encoding
        self.started    = False

        if encoding=='br':
            if brotli is None:
                raise ContentEncodingError('Can not decode content-encoding: brotli (br). Please install `brotlipy')
            self.decompressor = brotli.Decompressor()
        else:
            if encoding=='gzip':
                zlib_mode=16+zlib.MAX_WBITS
            else:
                zlib_mode=-zlib.MAX_WBITS

            self.decompressor=zlib.decompressobj(wbits=zlib_mode)

    def set_exception(self,exception):
        self.out.set_exception(exception)

    def feed_data(self,chunk,size):
        self.size+=size
        try:
            chunk=self.decompressor.decompress(chunk)
        except (AttributeError,NameError):
            raise #for testing
        except Exception:
            if not self.started and self.encoding=='deflate':
                self.decompressor = zlib.decompressobj()
                try:
                    chunk = self.decompressor.decompress(chunk)
                except (AttributeError,NameError):
                    raise #for testing
                except Exception:
                    raise ContentEncodingError(f'Can not decode content-encoding: {self.encoding}')
            else:
                raise ContentEncodingError(f'Can not decode content-encoding: {self.encoding}')

        if chunk:
            self.started = True
            self.out.feed_data(chunk, len(chunk))

    def feed_eof(self):
        chunk = self.decompressor.flush()

        if chunk or self.size > 0:
            self.out.feed_data(chunk, len(chunk))
            if self.encoding == 'deflate' and not self.decompressor.eof:
                raise ContentEncodingError('deflate')

        self.out.feed_eof()

    def begin_http_chunk_receiving(self):
        self.out.begin_http_chunk_receiving()

    def end_http_chunk_receiving(self):
        self.out.end_http_chunk_receiving()


class HttpRequestParser(HttpParser):
    def parse_message(self,lines):
        # request line
        line=lines[0].decode('utf-8','surrogateescape')
        try:
            method,path,version=line.split(None,2)
        except ValueError:
            raise ValueError(line) from None

        if len(path)>self.max_line_size:
            raise PayloadError('Status line is too long',self.max_line_size,len(path))

        # method
        method=method.upper()
        if not METHRE.match(method):
            raise ValueError(method)

        # version
        try:
            if version.startswith('HTTP/'):
                n1,n2=version[5:].split('.',1)
                version=HttpVersion(int(n1),int(n2))
            else:
                raise ValueError(version)
        except ValueError:
            raise
        except (AttributeError,NameError):
            raise #for testing
        except Exception:
            raise ValueError(version)

        # read headers
        headers,raw_headers,close,compression,upgrade,chunked=self.parse_headers(lines)
        
        if close is None:  # then the headers weren't set in the request
            close=False

        return RawRequestMessage(
            method,path,version,headers,raw_headers,
            close,compression,upgrade,chunked,URL(path))


class HttpResponseParser(HttpParser):
    def parse_message(self,lines):
        line=lines[0].decode('utf-8','surrogateescape')
        try:
            version,status=line.split(None,1)
        except ValueError:
            raise ValueError(line) from None

        try:
            status,reason=status.split(None,1)
        except ValueError:
            reason=''

        if len(reason)>self.max_line_size:
            raise ValueError('Status line is too long',self.max_line_size,len(reason))

        # version
        match=VERSRE.match(version)
        if match is None:
            raise ValueError(line)
        
        version=HttpVersion(int(match.group(1)),int(match.group(2)))

        # The status code is a three-digit number
        try:
            status=int(status)
        except ValueError:
            raise ValueError(line) from None

        if status>999:
            raise ValueError(line)

        # read headers
        headers,raw_headers,close,compression,upgrade,chunked=self.parse_headers(lines)

        if close is None:
            close=False

        return RawResponseMessage(
            version,status,reason.strip(),
            headers,raw_headers,close,compression,upgrade,chunked)
