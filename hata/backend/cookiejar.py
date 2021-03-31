# -*- coding: utf-8 -*-
import re
from datetime import datetime, timezone
from collections import defaultdict
from http.cookies import Morsel, SimpleCookie
from math import ceil

from .url import URL
from .helpers import is_ip_address
from .event_loop import LOOP_TIME

class CookieJar:
    """
    Implements cookie storage adhering to RFC 6265.
    
    Attributes
    ----------
    cookies : `defaultdict` of (`str`, `http.cookies.SimpleCookie`) items
        Dictionary containing the stored cookies.
    expirations : `dict` of (`tuple` (`str`, `str`), `float`) item
        Cookie expirations. The keys are a domain, name pairs, meanwhile the values are their expirations.
    host_only_cookies : `set` of `tuple` (`str`, `str`)
        Reference of hosts only cookies in tuples as `host-name`, `host` pairs.
    next_expiration : `float`
        The next expiration's monotonic time.
    unsafe : `bool`
        Whether the jar accepts unsafe cookies as well.
    """
    DATE_TOKENS_RE = re.compile(
        '[\x09\x20-\x2F\x3B-\x40\x5B-\x60\x7B-\x7E]*(?P<token>[\x00-\x08\x0A-\x1F\d:a-zA-Z\x7F-\xFF]+)')
    DATE_HMS_TIME_RE = re.compile('(\d{1,2}):(\d{1,2}):(\d{1,2})')
    DATE_DAY_OF_MONTH_RE = re.compile('(\d{1,2})')
    DATE_MONTH_RE = re.compile('(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)', re.I)
    DATE_YEAR_RE = re.compile('(\d{2,4})')
    MAX_TIME = 2051215261.0 # (2035-01-01)
    
    __slots__ = ('cookies', 'expirations', 'host_only_cookies', 'next_expiration', 'unsafe', )
    
    def __init__(self, unsafe=False):
        """
        Creates a new cookie-jar.
        
        Parameters
        ----------
        unsafe : `bool`
            Whether unsafe cookies are added to the jar as well. Defaults to `False`.
        """
        self.cookies = defaultdict(SimpleCookie)
        self.host_only_cookies = set()
        self.unsafe = unsafe
        self.next_expiration = ceil(LOOP_TIME())
        self.expirations = {}
    
    def __getstate__(self):
        return (list(self.cookies.values()), self.host_only_cookies, self.unsafe)
    
    def __setstate__(self, state):
        cookies, host_only_cookies, unsafe = state
        
        self.cookies = defaultdict(SimpleCookie)
        self.host_only_cookies = host_only_cookies
        self.unsafe = False
        self.next_expiration = 0.0
        self.expirations = {}
        
        for cookie in cookies:
            self.update_cookies(cookie)
        
        self.unsafe = unsafe
        self._do_expiration()
    
    def clear(self):
        """
        Clears the cookie-jar.
        """
        self.cookies.clear()
        self.host_only_cookies.clear()
        self.next_expiration = ceil(LOOP_TIME())
        self.expirations.clear()
        
    def __iter__(self):
        """
        Iterates over the jar's cookies' values.
        
        This method is a generator.
        
        Returns
        -------
        value : `str`
        """
        self._do_expiration()
        for val in self.cookies.values():
            yield from val.values()
    
    def __len__(self):
        """Returns the length of the cookie-jar."""
        length = 0
        for cookie in self.cookies.values():
            length += len(cookie)
        
        return length
    
    def _do_expiration(self):
        """
        Removes the expired cookies from the jar.
        """
        now = LOOP_TIME()
        if self.next_expiration > now:
            return
        
        expirations = self.expirations
        if not expirations:
            return
        
        next_expiration = self.MAX_TIME
        to_del = []
        cookies = self.cookies
        
        for key, when in expirations.items():
            if when < now:
                cookies[key[0]].pop(key[1], None)
                to_del.append(key)
                self.host_only_cookies.discard(key)
            else:
                next_expiration = min(next_expiration, when)
        
        for key in to_del:
            del expirations[key]
        
        self.next_expiration = ceil(next_expiration)
    
    def _expire_cookie(self, when, domain, name):
        """
        Sets the expiration of the cookie jar and of the given `domain`, `name` relation.
        
        Parameters
        ----------
        when : `int`
            Posix timestamp of the cookie's expiration.
        domain : `str`
            The cookie's domain.
        name : `str`
            The cookie's name.
        """
        self.next_expiration = min(self.next_expiration, when)
        self.expirations[(domain, name)] = when
    
    def update_cookies(self, cookies, response_url=URL()):
        """
        Updates the cookies of the.
        
        Parameters
        ----------
        cookies : `http.cookies.SimpleCookie`
            A cookie to update the
        response_url : ``URL``
            Respective response's url.
        """
        hostname = response_url.raw_host
        
        if not self.unsafe and is_ip_address(hostname):
            # Don't accept cookies from IPs
            return
        
        for name, cookie in cookies.items():
            if not isinstance(cookie, Morsel):
                temporary = SimpleCookie()
                temporary[name] = cookie
                cookie = temporary[name]
            
            domain = cookie['domain']
            
            # ignore domains with trailing dots
            if domain.endswith('.'):
                domain = ''
                del cookie['domain']
            
            if not domain and hostname is not None:
                # Set the cookie's domain to the response hostname and set its host-only-flag
                self.host_only_cookies.add((hostname, name))
                domain = cookie['domain'] = hostname
            
            if domain.startswith('.'):
                # Remove leading dot
                domain = domain[1:]
                cookie['domain'] = domain
            
            if hostname and not self._is_domain_match(domain, hostname):
                # Setting cookies for different domains is not allowed
                continue
            
            path = cookie['path']
            if not path or not path.startswith('/'):
                # Set the cookie's path to the response path
                path = response_url.path
                if not path.startswith('/'):
                    path = '/'
                else:
                    # Cut everything from the last slash to the end
                    path = f'/{path[1:path.rfind("/")]}'
                cookie['path'] = path
            
            max_age = cookie['max-age']
            if max_age:
                try:
                    delta_seconds = int(max_age)
                    self._expire_cookie(LOOP_TIME()+delta_seconds, domain, name)
                except ValueError:
                    cookie['max-age'] = ''
            
            else:
                expires = cookie['expires']
                if expires:
                    expire_time = self._parse_date(expires)
                    if expire_time is None:
                        cookie['expires'] = ''
                    else:
                        self._expire_cookie(expire_time.timestamp(), domain, name)
            
            self.cookies[domain][name] = cookie
        
        self._do_expiration()
    
    def filter_cookies(self, request_url=URL()):
        """
        Returns this jar's cookies filtered by their attributes
        
        Parameters
        ----------
        request_url : ``URL``
            The url to filter the cookies by.
        
        Returns
        -------
        filtered : ``SimpleCookie``
            Filtered out cookies.
        """
        self._do_expiration()
        
        filtered = SimpleCookie()
        hostname = request_url.raw_host
        if hostname is None:
            hostname = ''
        
        is_not_secure = (request_url.scheme not in ('https', 'wss'))
        
        for cookie in self:
            name = cookie.key
            domain = cookie['domain']
            
            # Send shared cookies
            if not domain:
                filtered[name] = cookie.value
                continue
            
            if not self.unsafe and is_ip_address(hostname):
                continue
            
            if (domain, name) in self.host_only_cookies:
                if domain != hostname:
                    continue
            
            elif not self._is_domain_match(domain, hostname):
                continue
            
            if not self._is_path_match(request_url.path, cookie['path']):
                continue
            
            if is_not_secure and cookie['secure']:
                continue
            
            # It's critical we use the Morsel so the coded_value (based on cookie version) is preserved
            morsel_value = cookie.get(cookie.key, Morsel())
            morsel_value.set(cookie.key, cookie.value, cookie.coded_value)
            filtered[name] = morsel_value
        
        return filtered
    
    @staticmethod
    def _is_domain_match(domain, hostname):
        """
        Implements domain matching adhering to RFC 6265.
        
        Parameters
        ----------
        domain : `str`
            The domain's name to match.
        hostname : `str`
            The hostname to match.
        
        Returns
        -------
        domain_matching : `bool`
        """
        if hostname == domain:
            return True

        if not hostname.endswith(domain):
            return False

        non_matching = hostname[:-len(domain)]

        if not non_matching.endswith('.'):
            return False

        return not is_ip_address(hostname)

    @staticmethod
    def _is_path_match(request_path, cookie_path):
        """
        Implements path matching adhering to RFC 6265.
        
        Parameters
        ----------
        request_path : `str`
            The request's path.
        cookie_path : `str`
            The cookie's path.
        
        Returns
        -------
        path_matching : `bool`
        """
        if not request_path.startswith('/'):
            request_path = '/'
        
        if request_path == cookie_path:
            return True
        
        if not request_path.startswith(cookie_path):
            return False

        if cookie_path.endswith('/'):
            return True
        
        cookie_path_ln = len(cookie_path)
        if cookie_path_ln >= len(request_path):
            return False
        
        if request_path[cookie_path_ln] == '/':
            return True
        
        return False
    
    @classmethod
    def _parse_date(cls, date_str):
        """
        Implements date string parsing adhering to RFC 6265.
        
        Parameters
        ----------
        date_str : `str`
            Datetime string.
        
        Returns
        -------
        date : `None` or `datetime`
            The parsed date. If no date is given or if the `date_str` is invalid, returns `None`,
        """
        if not date_str:
            return
        
        found_time = found_day = found_month = found_year = False
        
        hour = minute = second = day = month = year = 0
        
        for token_match in cls.DATE_TOKENS_RE.finditer(date_str):
            
            token = token_match.group('token')
            
            if not found_time:
                time_match = cls.DATE_HMS_TIME_RE.match(token)
                if time_match:
                    found_time = True
                    hour, minute, second = time_match.groups()
                    hour = int(hour)
                    minute = int(minute)
                    second = int(second)
                    continue
            
            if not found_day:
                day_match = cls.DATE_DAY_OF_MONTH_RE.match(token)
                if day_match:
                    found_day = True
                    day = int(day_match.group())
                    continue
            
            if not found_month:
                month_match = cls.DATE_MONTH_RE.match(token)
                if month_match:
                    found_month = True
                    month = month_match.lastindex
                    continue
            
            if not found_year:
                year_match = cls.DATE_YEAR_RE.match(token)
                if year_match:
                    found_year = True
                    year = int(year_match.group())
        
        if 70 <= year <= 99:
            year += 1900
        elif 0 <= year <= 69:
            year += 2000
        
        if (not found_day) or (not found_month) or (not found_year) or (not found_time) or (year < 1601) or (day < 1) \
                or (day > 31) or (hour > 23) or (minute > 59) or (second > 59):
            return None
        
        return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
