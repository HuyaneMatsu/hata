__all__ = ('URL', )

from ipaddress import ip_address
from urllib.parse import SplitResult, parse_qsl as parse_query_string_list, urljoin as url_join, \
    urlsplit as url_split, urlunsplit as url_unsplit
from math import isinf, isnan
from datetime import datetime

from .utils import multidict, cached_property
from .quote import quote, unquote

NoneType = type(None)

DEFAULT_PORTS = {
    'http': 80,
    'https': 443,
    'ws': 80,
    'wss': 443,
}

class URL:
    """
    Represents an URL (Uniform Resource Locator)
    
    Attributes
    ----------
    _cache : `dict` of (`str`, `str`) items
        Internal cache used by ``cached_property``-s.
    _value : `urllib.parse.SplitResult`
        Internal value of the ``URL``.
    """
    # Don't derive from str follow pathlib.Path design probably URL will not suffer from pathlib problems: it's
    # intended for libraries, not to be passed into standard library functions like os.open etc.

    # URL grammar (RFC 3986)
    # pct-encoded = "%" HEXDIG HEXDIG
    # reserved = gen-delims / sub-delims
    # gen-delims = ":" / "/" / "?" / "#" / "[" / "]" / "@"
    # sub-delims = "!" / "$" / "&" / "'" / "(" / ")"
    #             / "*" / "+" / "," / ";" / "="
    # unreserved = ALPHA / DIGIT / "-" / "." / "_" / "~"
    # URI = scheme ":" hier-part [ "?" query ] [ "#" fragment ]
    # hier-part = "//" authority path-abempty
    #             / path-absolute
    #             / path-rootless
    #             / path-empty
    # scheme = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )
    # authority = [ userinfo "@" ] host [ ":" port ]
    # userinfo = *( unreserved / pct-encoded / sub-delims / ":" )
    # host = IP-literal / IPv4address / reg-name
    # IP-literal = "[" ( IPv6address / IPvFuture  ) "]"
    # IPvFuture = "v" 1*HEXDIG "." 1*( unreserved / sub-delims / ":" )
    # IPv6address = 6( h16 ":" ) ls32
    #             /                       "::" 5( h16 ":" ) ls32
    #             / [               h16 ] "::" 4( h16 ":" ) ls32
    #             / [ *1( h16 ":" ) h16 ] "::" 3( h16 ":" ) ls32
    #             / [ *2( h16 ":" ) h16 ] "::" 2( h16 ":" ) ls32
    #             / [ *3( h16 ":" ) h16 ] "::"    h16 ":"   ls32
    #             / [ *4( h16 ":" ) h16 ] "::"              ls32
    #             / [ *5( h16 ":" ) h16 ] "::"              h16
    #             / [ *6( h16 ":" ) h16 ] "::"
    # ls32 = ( h16 ":" h16 ) / IPv4address
    #             ; least-significant 32 bits of address
    # h16 = 1*4HEXDIG
    #             ; 16 bits of address represented in hexadecimal
    # IPv4address = dec-octet "." dec-octet "." dec-octet "." dec-octet
    # dec-octet = DIGIT                 ; 0-9
    #             / %x31-39 DIGIT         ; 10-99
    #             / "1" 2DIGIT            ; 100-199
    #             / "2" %x30-34 DIGIT     ; 200-249
    #             / "25" %x30-35          ; 250-255
    # reg-name = *( unreserved / pct-encoded / sub-delims )
    # port = *DIGIT
    # path = path-abempty    ; begins with "/" or is empty
    #               / path-absolute   ; begins with "/" but not "//"
    #               / path-noscheme   ; begins with a non-colon segment
    #               / path-rootless   ; begins with a segment
    #               / path-empty      ; zero characters
    # path-abempty = *( "/" segment )
    # path-absolute = "/" [ segment-nz *( "/" segment ) ]
    # path-noscheme = segment-nz-nc *( "/" segment )
    # path-rootless = segment-nz *( "/" segment )
    # path-empty = 0<pchar>
    # segment = *pchar
    # segment-nz = 1*pchar
    # segment-nz-nc = 1*( unreserved / pct-encoded / sub-delims / "@" )
    #               ; non-zero-length segment without any colon ":"
    # pchar = unreserved / pct-encoded / sub-delims / ":" / "@"
    # query = *( pchar / "/" / "?" )
    # fragment = *( pchar / "/" / "?" )
    # URI-reference = URI / relative-ref
    # relative-ref = relative-part [ "?" query ] [ "#" fragment ]
    # relative-part = "//" authority path-abempty
    #               / path-absolute
    #               / path-noscheme
    #               / path-empty
    # absolute-URI = scheme ":" hier-part [ "?" query ]
    
    __slots__ = ('_cache', '_value', )

    def __new__(cls, value='', encoded=False):
        """
        Creates a new ``URL`` instance from the given `value`
        
        Parameters
        ----------
        value : ``URL``, `str`, `urllib.parse.SplitResult`, Optional
            The value to create ``URL`` from. Defaults to empty string.
        encoded : `bool`, Optional
            Whether the given `value` is already encoded. Defaults to `False`.

        Raises
        -------
        ValueError
            - If `value` is given as `urllib.parse.SplitResult` instance, but `encoded` was given as `False`.
            - If `value` is not `encoded` and the URL is absolute, but `host` is not given.
        TypeError
            If `value` was not given neither as ``URL``, `str` nor `urllib.parse.SplitResult` instance.
        """
        if isinstance(value, cls):
            return value
        
        if isinstance(value, str):
            value = url_split(value)
        elif isinstance(value, SplitResult):
            if not encoded:
                raise ValueError(f'Cannot apply decoding to `{SplitResult.__name__}`.')
        else:
            raise TypeError(f'`value` should have be given as `{cls.__name__}`, `str` or `{SplitResult.__name__}` '
                f'instance, got {value.__class__.__name__}.')
        
        if not encoded:
            if value.netloc:
                netloc = value.hostname
                if netloc is None:
                    raise ValueError('Invalid URL: host is required for absolute urls.')
                
                try:
                    netloc.encode('ascii')
                except UnicodeEncodeError:
                    netloc = netloc.encode('idna').decode('ascii')
                else:
                    try:
                        ip = ip_address(netloc)
                    except:
                        pass
                    else:
                        if ip.version == 6:
                            netloc = f'[{netloc}]'
                
                value_port = value.port
                if value_port:
                    netloc = f'{netloc}:{value_port}'
                
                value_username = value.username
                if value_username:
                    user = quote(value_username)
                    value_password = value.password
                    if value_password:
                        user = f'{user}:{quote(value_password)}'
                    
                    netloc = f'{user}@{netloc}'
            else:
                netloc = ''
            
            value = SplitResult(value.scheme, netloc,
                quote(value.path, safe='@:', protected='/'),
                quote(value.query, safe='=+&?/:@', protected='=+&', query_string=True),
                quote(value.fragment, safe='?/:@'),
            )
        
        self = object.__new__(cls)
        self._value = value
        self._cache = {}
        return self
    
    def __str__(self):
        """Returns str(self)."""
        value = self._value
        if not value.path and self.is_absolute() and (value.query or value.fragment):
            value = value._replace(path='/')
        
        return url_unsplit(value)
    
    def __repr__(self):
        """Returns repr(self)."""
        return f'{self.__class__.__name__}({str(self)!r})'

    def __hash__(self):
        """Returns hash(self)."""
        try:
            hash_value = self._cache['hash']
        except KeyError:
            hash_value = self._cache['hash'] = hash(self._value)
        return hash_value
    
    def __gt__(self, other):
        """Returns (self > other)."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            other = type(self)(other)
        else:
            return NotImplemented
        
        return self._value > other._value
        
    def __ge__(self, other):
        """Returns (self >= other)."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            other = type(self)(other)
        else:
            return NotImplemented
        
        return self._value >= other._value
        
    def __eq__(self, other):
        """Returns (self == other)."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            other = type(self)(other)
        else:
            return NotImplemented
        
        return self._value == other._value
        
    def __ne__(self, other):
        """Returns (self != other)."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            other = type(self)(other)
        else:
            return NotImplemented
        
        return self._value != other._value
    
    def __le__(self, other):
        """Returns (self <= other)."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            other = type(self)(other)
        else:
            return NotImplemented
        
        return self._value <= other._value
        
    def __lt__(self, other):
        """Returns (self < other)."""
        if type(self) is type(other):
            pass
        elif isinstance(other, str):
            other = type(self)(other)
        else:
            return NotImplemented
        
        return self._value < other._value
    
    def __truediv__(self, name):
        """Returns self / other"""
        name = quote(name, safe=':@', protected='/')
        if name.startswith('/'):
            raise ValueError('Appending path starting from slash is forbidden')
        path = self._value.path
        if path == '/':
            new_path = f'/{name}' 
        elif not path and not self.is_absolute():
            new_path = name
        else:
            parts = path.rstrip('/').split('/')
            parts.append(name)
            new_path = '/'.join(parts)
        return URL(self._value._replace(path=new_path, query='', fragment=''), encoded=True)
    
    def is_absolute(self):
        """
        Returns whether the URL is absolute (having scheme or starting with //).
        
        Returns
        -------
        is_absolute : `bool`
        """
        return (self.raw_host is not None)
    
    def is_default_port(self):
        """
        Returns whether the URL's port is default, like: 'http://python.org' or 'http://python.org:80'.
        
        Returns
        -------
        is_default_port : `bool`
        """
        if self.port is None:
            return False
        
        default = DEFAULT_PORTS.get(self.scheme, None)
        if default is None:
            return False
        
        if self.port == default:
            return True
        
        return False
    
    def origin(self):
        """
        Returns an URL with scheme, host and port parts only, user, password, path, query and fragment are removed.
        
        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        ValueError
            - If the URL is not absolute.
            - If the URL has no scheme.
        """
        if not self.is_absolute():
            raise ValueError('URL should be absolute.')
        
        value = self._value
        if not value.scheme:
            raise ValueError('URL should have scheme.')
        
        netloc = self._make_netloc(None, None, value.hostname, value.port)
        new_value = value._replace(netloc=netloc, path='', query='', fragment='')
        return URL(new_value, encoded=True)
    
    def relative(self):
        """
        Returns a relative part of the URL, scheme, user, password, host and port are removed.
        
        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        ValueError
            If URL is not absolute.
        """
        if not self.is_absolute():
            raise ValueError('URL should be absolute.')
        
        value = self._value._replace(scheme='', netloc='')
        return URL(value, encoded=True)
    
    @property
    def scheme(self):
        """
        Returns the scheme for absolute URL-s. Returns empty string for relative URL-s and for URL-s starting with //.
        
        Returns
        -------
        scheme : `str`
        """
        return self._value.scheme
    
    @property
    def raw_user(self):
        """
        Returns the encoded user part of the URL. `None` is returned if the user part is missing.
        
        Returns
        -------
        raw_user : `None` or `str`
        """
        return self._value.username
    
    @cached_property
    def user(self):
        """
        Returns the decoded user part of the URL. `None` is returned if the user part is missing.
        
        Returns
        -------
        user : `None` or `str`
        """
        return unquote(self.raw_user)
    
    @property
    def raw_password(self):
        """
        Returns the encoded password part of the URL. Returns `None` if password is missing.
        
        Returns
        -------
        raw_password : `None` or `str`
        """
        return self._value.password
    
    @cached_property
    def password(self):
        """
        Returns the decoded password part of the URL. Returns `None` if password is missing.
        
        Returns
        -------
        password : `None` or `str`
        """
        return unquote(self.raw_password)
    
    @property
    def raw_host(self):
        """
        Returns the encoded host part of the URL. Returns `None` if the host part is missing or if the URL is relative.
        
        Returns
        -------
        raw_host : `None` or `str`
        """
        return self._value.hostname
    
    @cached_property
    def host(self):
        """
        Returns the decoded host part of the URL. Returns `None` if the host part is missing or if the URL is relative.
        
        Returns
        -------
        host : `None` or `str`
        """
        raw_host = self.raw_host
        if raw_host is None:
            host = None
        else:
            host = raw_host.encode('ascii').decode('idna')
        
        return host
    
    @property
    def raw_subdomain(self):
        """
        Returns the encoded subdomain part of the URL if it has. Als returns `None` if the host part is missing or if
        the URL is relative.
        
        Returns
        -------
        raw_subdomain : `None` or `str`
        """
        host_name = self._value.hostname
        if host_name is None:
            subdomain = None
        else:
            back_index = host_name.rfind('.')
            if back_index == -1:
                subdomain = None
            else:
                back_index = host_name.rfind('.', back_index)
                if back_index == -1:
                    subdomain = None
                else:
                    subdomain = host_name[:back_index]
        
        return subdomain
        
    @cached_property
    def subdomain(self):
        """
        Returns the decoded subdomain of the URL if it has. Also returns `None` if the host part is missing or if the
        Url is relative.
        
        Returns
        -------
        subdomain : `None` or `str`
        """
        raw_subdomain = self.raw_subdomain
        if raw_subdomain is None:
            subdomain = None
        else:
            subdomain = raw_subdomain.encode('ascii').decode('idna')
        
        return subdomain
    
    @property
    def port(self):
        """
        Returns the port part of URL. Returns `None` if the URL is relative, if the URL not contains port part and if
        the port can's be detected from the URL's scheme.
        
        Returns
        -------
        port : `None` or `int`
        """
        value = self._value
        port = value.port
        if port is None:
            port = DEFAULT_PORTS.get(value.scheme, None)
        
        return port
    
    @property
    def raw_path(self):
        """
        Returns the encoded path part of the URL. Returns `'/'` for absolute URL-s without any path parts.
        
        Returns
        -------
        raw_path : `str`
        """
        raw_path = self._value.path
        if (not raw_path) and self.is_absolute():
            raw_path = '/'
        
        return raw_path
    
    @cached_property
    def path(self):
        """
        Returns the decoded path part of the URL. Returns `'/'` for absolute URL-s without any path parts.
        
        Returns
        -------
        path : `str`
        """
        return unquote(self.raw_path)
    
    @cached_property
    def query(self):
        """
        A multidict representing parsed query parameters in decoded representation.
        
        An empty multidict is returned if the url has no query parts.
        
        Returns
        -------
        query : `multidict` of (`str`, `Any`) items
        """
        return multidict(parse_query_string_list(self.query_string, keep_blank_values=True))
    
    @property
    def raw_query_string(self):
        """
        Returns the encoded query string part of URL. Returns an empty string if the query part is missing.
        
        Returns
        -------
        raw_query_string : `str`
        """
        return self._value.query
    
    @cached_property
    def query_string(self):
        """
        Returns the decoded query string part of URL. Returns an empty string if the query part is missing.
        
        Returns
        -------
        query_string : `str`
        """
        return unquote(self.raw_query_string, query_string=True)
    
    @property
    def raw_fragment(self):
        """
        Returns the encoded fragment part of the URL. Returns an empty string if the fragment part is missing.
        
        Returns
        -------
        raw_fragment : `str`
        """
        return self._value.fragment

    @cached_property
    def fragment(self):
        """
        Returns the decoded fragment part of the URL. Returns an empty string if the fragment part is missing.
        
        Returns
        -------
        raw_fragment : `str`
        """
        return unquote(self.raw_fragment)
    
    @cached_property
    def raw_parts(self):
        """
        Returns a `tuple` containing encoded path parts.
        
        If the URL is absolute, or if path is missing, it's first element always will be `'/'`.

        Returns
        -------
        raw_parts : `tuple` of `str`
        """
        path = self._value.path
        
        parts = []
        if self.is_absolute():
            parts.append('/')
            if path:
                parts.extend(path[1:].split('/'))
        else:
            if path.startswith('/'):
                parts.append('/')
                parts.extend(path[1:].split('/'))
            else:
                parts.extend(path.split('/'))
        
        return tuple(parts)
    
    @cached_property
    def parts(self):
        """
        Returns a `tuple` containing decoded path parts.
        
        If the URL is absolute, or if path is missing, it's first element always will be `'/'`.

        Returns
        -------
        raw_parts : `tuple` of `str`
        """
        return tuple(unquote(part) for part in self.raw_parts)
    
    @cached_property
    def parent(self):
        """
        Returns a new URL with last part of path removed without query and fragment.
        
        Returns
        -------
        parent : ``URL``
        """
        path = self.raw_path
        if path == '/':
            if self.raw_fragment or self.raw_query_string:
                parent = URL(self._value._replace(query='', fragment=''), encoded=True)
            else:
                parent = self
        else:
            parts = path.split('/')
            value = self._value._replace(path='/'.join(parts[:-1]), query='', fragment='')
            parent = URL(value, encoded=True)
        
        return parent
    
    @cached_property
    def raw_name(self):
        """
        Returns the last part of ``.raw_parts``. If there are no parts, returns an empty string.
        
        Returns
        -------
        raw_name : `str`
        """
        parts = self.raw_parts
        if self.is_absolute() and (len(parts) < 2):
            raw_name = ''
        else:
            raw_name = parts[-1]
        
        return raw_name
    
    @cached_property
    def name(self):
        """
        Returns the last part of ``.parts``. If there are no parts, returns an empty string.
        
        Returns
        -------
        raw_name : `str`
        """
        return unquote(self.raw_name)
    
    @classmethod
    def _make_netloc(cls, user, password, host, port):
        """
        Makes netloc from the given parameters
        
        Parameters
        ----------
        user : `None` or `str`
            User part of an URL.
        password : `None` or `str`
            Password part of an URL.
        host : `None` or `str`
            The host part of an URL.
        port : `None` or `int`
            The ort part of an URL:
        
        Returns
        -------
        netloc : `str`
        
        Raises
        ------
        ValueError
            If password is not empty, `user` parameter should not be empty either.
        """
        if (password is not None) and password:
            if (user is None) or (not user):
                raise ValueError('Non-empty password requires non-empty user.')
            
            user = f'{user}:{password}'
        
        if host is None:
            netloc = ''
        else:
            netloc = host
        
        if (port is not None) and port:
            netloc = f'{netloc}:{port!s}'
        
        if (user is not None) and user:
            netloc = f'{user}@{netloc}'
        
        return netloc
    
    def with_scheme(self, scheme):
        """
        Returns a new URL with `scheme` replaced.
        
        Parameters
        ----------
        scheme : `str`
            Scheme part for the new url.

        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        TypeError
            If `scheme` was not given as `str` instance.
        ValueError
            If the source URL is relative; Scheme replacement is not allowed for relative URL-s.
        
        Notes
        -----
        The returned URL's `query` and `fragment` will be same as the source one's.
        """
        if not isinstance(scheme, str):
            raise TypeError(f'`scheme` can be given as `str` instance, got {scheme.__class__.__name__}.')
        
        if not self.is_absolute():
            raise ValueError('`scheme` replacement is not allowed for relative URL-s.')
        
        return URL(self._value._replace(scheme=scheme.lower()), encoded=True)
    
    def with_user(self, user):
        """
        Returns a new URL with `user` replaced.
        
        Give `user` as `None` to clear `user` and `password` from the source URL.
        
        Parameters
        ----------
        user : `None` or `str`
            User part for the new url.

        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        TypeError
            If `user` was not given neither as `None` nor `str` instance.
        ValueError
            If the source URL is relative; User replacement is not allowed for relative URL-s.
        
        Notes
        -----
        The returned URL's `query` and `fragment` will be same as the source one's.
        """
        value = self._value
        if user is None:
            password = None
        elif isinstance(user, str):
            user = quote(user)
            password = value.password
        else:
            raise TypeError(f'`user` can be given as `None` or `str` instance, got  {user.__class__.__name__}.')
        
        if not self.is_absolute():
            raise ValueError('`user` replacement is not allowed for relative URL-s.')
        
        return URL(value._replace(netloc=self._make_netloc(user, password, value.hostname, value.port)), encoded=True)
    
    def with_password(self, password):
        """
        Returns a new URL with `password` replaced.
        
        Give `password` as `None` to clear it from the source URL.
        
        Parameters
        ----------
        password : `None` or `str`
            Password part for the new url.

        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        TypeError
            If `password` was not given neither as `None` nor `str` instance.
        ValueError
            If the source URL is relative; Password replacement is not allowed for relative URL-s.
        
        Notes
        -----
        The returned URL's `query` and `fragment` will be same as the source one's.
        """
        if password is None:
            pass
        elif isinstance(password, str):
            password = quote(password)
        else:
            raise TypeError(f'`password` can be given as `None` or `str` instance, got {password.__class__.__name__}.')
        
        if not self.is_absolute():
            raise ValueError('Password replacement is not allowed for relative URL-s.')
        
        value = self._value
        return URL( value._replace(netloc=self._make_netloc(value.username, password, value.hostname, value.port)),
            encoded=True)
    
    def with_host(self, host):
        """
        Returns a new URL with `host` replaced.
        
        Parameters
        ----------
        host : `str`
            Host part for the new url.

        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        TypeError
            If `host` was not given as `str` instance.
        ValueError
            - If the source URL is relative; Host replacement is not allowed for relative URL-s.
            - If `host` was given as empty string; Removing `host` is not allowed.
        
        Notes
        -----
        The returned URL's `query` and `fragment` will be same as the source one's.
        """
        if not isinstance(host, str):
            raise TypeError(f'`host` can be given as `str` instance, got {host.__class__.__name__}.')
        
        if not self.is_absolute():
            raise ValueError('`host` replacement is not allowed for relative URL-s.')
        
        if not host:
            raise ValueError('`host` was given as empty string, but removing host is not allowed.')
        
        try:
            ip = ip_address(host)
        except:
            host = host.encode('idna').decode('ascii')
        else:
            if ip.version == 6:
                host = f'[{host}]'
        
        value = self._value
        return URL(value._replace(netloc=self._make_netloc(value.username, value.password, host, value.port)),
            encoded=True)
    
    def with_port(self, port):
        """
        Returns a new URL with `port` replaced. Give `port` as None` to clear it to default.
        
        Parameters
        ----------
        port : `None` or `int`
            Port part of the new url.

        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        TypeError
            If `port` was not given neither as `None` nor `int` instance.
        ValueError
            If the source URL is relative; Port replacement is not allowed for relative URL-s.
        
        Notes
        -----
        The returned URL's `query` and `fragment` will be same as the source one's.
        """
        if (port is not None) and (not isinstance(port, int)):
            raise TypeError(f'`port` can be given as `None` or `int` instance, got {port.__class__.__name__}.')
        
        if not self.is_absolute():
            raise ValueError('`port` replacement is not allowed for relative URL-s.')
        
        value = self._value
        
        return URL(value._replace(netloc=self._make_netloc(value.username, value.password, value.hostname, port)),
            encoded=True)
    
    def with_query(self, query):
        """
        Returns a new url with query part replaced. By giving `None` you can clear the actual query.
        
        Parameters
        ----------
        query : `None`, `str`, (`dict`, `list`, `set`) of \
                (`str`, (`str`, `int`, `bool`, `NoneType`, `float`, (`list`, `set`, `tuple`) of repeat value)) items
            The query to use.
        
        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        TypeError
            - If `query` was given as an invalid type.
            - If `query` was given as `set` or `list`, but `1` of it's elements cannot be unpacked correctly.
            - If a query key was not given as `str` instance.
            - If a query value was not given as any of the expected types.
        ValueError
            - If a query value was given as `float`, but as `inf`.
            - If a query value was given as `float`, but as `nan`.
        
        Notes
        -----
        The returned URL's `fragment` will be same as the source one's.
        """
        if query is None:
            query = ''
        elif isinstance(query, dict):
            query = build_query_from_dict(query)
        elif isinstance(query, (list, set)):
            query = build_query_from_list(query)
        elif isinstance(query, str):
            query = quote(query, safe='/?:@', protected='=&+', query_string=True)
        elif isinstance(query, (bytes, bytearray, memoryview)):
            raise TypeError(f'Query type cannot be `bytes`, `bytearray` and `memoryview`, got '
                f'{query.__class__.__name__}')
        else:
            raise TypeError(f'Invalid query type: {query.__class__.__name__}.')
        
        value = self._value
        
        path = value.path
        if not path:
            path = '/'
        
        return URL(value._replace(path=path, query=query), encoded=True)
    
    def with_fragment(self, fragment):
        """
        Returns a new URL with `fragment` replaced. Give `fragment` as None` to clear it.
        
        Parameters
        ----------
        fragment : `None` or `str`
            Fragment part of the new url.

        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        TypeError
            If `fragment` was not given neither as `None` nor `str` instance.
        
        Notes
        -----
        The returned URL's `query` will be same as the source one's.
        """
        if fragment is None:
            fragment = ''
        elif not isinstance(fragment, str):
            raise TypeError(f'`fragment` can be given as `None` or `str` instance, got {fragment.__class__.__name__}.')
        
        return URL(self._value._replace(fragment=quote(fragment, safe='?/:@')), encoded=True)
    
    def with_name(self, name):
        """
        Returns a new URL with `name` (last part of path) replaced.
        
        Parameters
        ----------
        name : `str`
            name part of the new url.

        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        TypeError
            If `name` was not given as `str` instance.
        ValueError
            If `name` contains `'/'` character.
        
        Notes
        -----
        The returned URL's `fragment` and `query` will be REMOVED.
        """
        if not isinstance(name, str):
            raise TypeError(f'`name` can be given as `str` instance, got {name.__class__.__name__}.')
        
        if '/' in name:
            raise ValueError(f'`name` contains `\'/\'` character, got {name!r}.')
        
        name = quote(name, safe='@:', protected='/')
        
        parts = list(self.raw_parts)
        if self.is_absolute():
            if len(parts) == 1:
                parts.append(name)
            else:
                parts[-1] = name
            parts[0] = '' # replace leading '/'
        else:
            parts[-1] = name
            if parts[0] == '/':
                parts[0] = '' # replace leading '/'
        
        return URL(self._value._replace(path='/'.join(parts), query='', fragment=''), encoded=True)
    
    def join(self, other):
        """
        Joins two urls.
        
        Construct a full ('absolute') URL by combining a 'base URL' (self) with another one (other).
        
        Informally, this uses components of the base URL, in particular the addressing scheme, the network location and
        (part of) the path, to provide missing components in the relative URL.
        
        Parameters
        ----------
        other : ``URL``
            The other url to join to self.
        
        Raises
        ------
        TypeError
            If `other` was not given as ``URL`` instance.
        
        See Also
        -----
        `urllib.parse.url_join` for more information.
        """
        if not isinstance(other, URL):
            raise TypeError(f'`url` can be given as `{URL.__name__}` instance, got {other.__class__.__name__}.')
        
        return URL(url_join(str(self), str(other)), encoded=True)
    
    def human_repr(self):
        """
        Returns a hooman readable string representing the URL.
        
        Returns
        -------
        human_repr : `str`
        """
        return url_unsplit(SplitResult(self.scheme, self._make_netloc(self.user, self.password, self.host,
            self._value.port), self.path, self.query_string, self.fragment))
    
    def extend_query(self, params):
        """
        Returns a new URL with it's query parameters extended.
        
        Parameters
        ----------
        params : `None`, `str`, (`dict`, `list`, `set`) of \
                (`str`, (`str`, `int`, `bool`, `NoneType`, `float`, (`list`, `set`, `tuple`) of repeat value)) items
            The query parameters to extend the actual.
        
        Returns
        -------
        new_url : ``URL``
        
        Raises
        ------
        TypeError
            - If `query` was given as an invalid type.
            - If `query` was given as `set` or `list`, but `1` of it's elements cannot be unpacked correctly.
            - If a query key was not given as `str` instance.
            - If a query value was not given as any of the expected types.
        ValueError
            - If a query value was given as `float`, but as `inf`.
            - If a query value was given as `float`, but as `nan`.
        
        Notes
        -----
        The returned URL's `fragment` will be same as the source one's.
        """
        if (params is None) or (not params):
            new_url = self
        else:
            query = self.query.copy()
            if isinstance(params, str):
                params = parse_query_string_list(params, keep_blank_values=True)
            
            query.extend(params)
            
            new_url = self.with_query(query)
        
        return new_url


def build_query_from_dict(query):
    """
    Builds a query string and adds the parts of it to the given `build_to` list.
    
    Parameters
    ----------
    query : `dict` of (`str`, (`str`, `int`, `bool`, `NoneType`, `float`, (`list`, `tuple`, `set`) of repeat value)) items
        The query to serialize.
    
    Returns
    -------
    query_string : `str`
        The built query string.
    
    Raises
    ------
    TypeError
        - If `1` of `query`'s keys is not `str` instance.
        - If a query value is not any of the expected types.
    ValueError
        - If a query value was given as `float` and it is `inf`.
        - If a query value was given as `float` and it is `nan`.
    """
    build_to = []
    
    for key, value in query.items():
        query_key = quote(key, safe="/?:@", query_string=True)
        build_query_element_to(build_to, query_key, value)
    
    return ''.join(build_to)


def build_query_from_list(query):
    """
    Builds a query string and adds the parts of it to the given `build_to` list.
    
    Parameters
    ----------
    query : (`list` or `set`) of `tuple` \
            (`str`, (`str`, `int`, `bool`, `NoneType`, `float`, (`list`, `tuple`, `set`) of repeat value))
        The query to serialize.
    
    Returns
    -------
    query_string : `str`
        The built query string.
    
    Raises
    ------
    TypeError
        - If `1` of `query`'s elements cannot be unpacked to a `key` - `value` pair.
        - If `1` of `query`'s keys is not `str` instance.
        - If a query value is not any of the expected types.
    ValueError
        - If a query value was given as `float` and it is `inf`.
        - If a query value was given as `float` and it is `nan`.
    """
    build_to = []
    
    for key, value in query:
        query_key = quote(key, safe="/?:@", query_string=True)
        build_query_element_to(build_to, query_key, value)
    
    return ''.join(build_to)


def build_query_element_to(build_to, query_key, value):
    """
    Builds a query string element to the given `build_to` list.
    
    Parameters
    ----------
    build_to : `list`
        A list to build the query element to.
    query_key : `str`
        An already escaped query key.
    value : `str`, `int`, `bool`, `NoneType`, `float`, (`list`, `tuple`,  `set`) of repeat
        The query string value.
    
    Raises
    ------
    TypeError
        - If `value` was not given as any of the expected types.
    ValueError
        - If `value` is a `float`, but it is `inf`.
        - If `value` is a `float`, but it is `nan`.
    """
    if isinstance(value, str):
        query_value = value
    elif isinstance(value, bool):
        query_value = 'true' if value else 'false'
    elif isinstance(value, int):
        query_value = str(value)
    elif isinstance(value, NoneType):
        query_value = 'null'
    elif isinstance(value, datetime):
        query_value = value.isoformat()
    elif isinstance(value, float):
        if isinf(value):
             raise ValueError('`inf` is not a supported query string parameter value.')
        
        if isnan(value):
            raise ValueError('`nan` is not a supported query string parameter value.')
        
        query_value = str(value)
    
    elif isinstance(value, (list, tuple, set)):
        build_query_list_to(build_to, query_key, value)
        return
    
    else:
        raise TypeError(f'Unexpected value type received when serializing query string, got '
            f'{value.__class__.__name__}; {value!r}.')
    
    query_value = quote(query_value, safe="/?:@", query_string=True)
    
    if build_to:
        build_to.append('&')
    build_to.append(query_key)
    build_to.append('=')
    build_to.append(query_value)


def build_query_list_to(build_to, query_key, query_list):
    """
    Builds a query element from a `list` or `set`.
    
    Parameters
    ----------
    build_to : `list`
        A list to build the query element to.
    query_key : `str`
        An already escaped query key.
    query_list : (`list`, `tuple`, `set`) of (`str`, `int`, `bool`, `NoneType`, `float`, repeat)
        The query string value.
    
    Raises
    -----
    TypeError
        - If `query_list` contains a value with an unexpected type.
    ValueError
        - If `query_list` contains a value as a `float` what it is `inf`.
        - If `query_list` contains a value as a `float` what it is `nan`.
    """
    for value in query_list:
        build_query_element_to(build_to, query_key, value)
