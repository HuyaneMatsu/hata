# -*- coding: utf-8 -*-
import re
from datetime import timedelta


from ...backend.utils import cached_property, copy_docs

from ...env import CACHE_USER

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None


NUMERIC_CONVERSION_LIMIT = 100

CONTENT_ARGUMENT_PARSERS = {}

DEFAULT_ARGUMENT_SEPARATOR = ('"', '"')
DEFAULT_ARGUMENT_ASSIGNER = ':'


class ContentArgumentParserContextBase:
    """
    Parsing context returned by ``ContentArgumentParser``.
    
    Attributes
    ----------
    _cache : `dict` of (`str`, `Any`)
        Cache used by cached properties.
    _parsed : re.Match
        The parsed regex.
    """
    __slots__ = ('_cache', '_parsed')
    def __new__(cls, parsed):
        """
        Creates a new ``ContentArgumentParserContext`` instance with the given match.
        
        Parameters
        ----------
        parsed : re.Match
            The parsed regex.
        """
        self = object.__new__(cls)
        self._parsed = parsed
        self._cache = {}
        return self
    
    @property
    def has_keyword(self):
        """
        Returns whether keyword could be parsed.
        
        Returns
        -------
        has_keyword : `bool`
        """
        return (self.keyword is not None)
    
    @property
    def end(self):
        """
        Returns the end of the parsed region.
        
        Returns
        -------
        end : `str`
        """
        return self._parsed.end()
    
    @cached_property
    def whole(self):
        """
        Gets the whole parsed string part.
        
        Returns
        -------
        whole : `str`
        """
        return ''
    
    @cached_property
    def keyword(self):
        """
        Gets the parsed keyword from the parsed part.
        
        Returns
        -------
        keyword : `None` or `str`
        """
        return None
    
    @cached_property
    def value(self):
        """
        Returns the parsed value.
        
        Returns
        -------
        value : `str`
        """
        return ''

class ContentArgumentParserContextSeparator(ContentArgumentParserContextBase):
    @cached_property
    @copy_docs(ContentArgumentParserContextBase.whole)
    def whole(self):
        return self._parsed.group(1)
    
    @cached_property
    @copy_docs(ContentArgumentParserContextBase.keyword)
    def keyword(self):
        return self._parsed.group(2)
    
    @cached_property
    @copy_docs(ContentArgumentParserContextBase.value)
    def value(self):
        return self._parsed.group(3)

class ContentArgumentParserContextEncapsulator(ContentArgumentParserContextBase):
    @cached_property
    @copy_docs(ContentArgumentParserContextBase.whole)
    def whole(self):
        parsed = self._parsed
        part = parsed.group(3)
        if part is None:
            part = parsed.group(2)
        
        return part
    
    @cached_property
    @copy_docs(ContentArgumentParserContextBase.keyword)
    def keyword(self):
        return self._parsed.group(2)
    
    @cached_property
    @copy_docs(ContentArgumentParserContextBase.value)
    def value(self):
        parsed = self._parsed
        part = parsed.group(3)
        if part is None:
            part = parsed.group(2)
        
        return part


class ContentArgumentParser:
    """
    Content argument parser used inside of a ``ContentParserContext`` and stored by ``CommandContentParser``
    instances.
    
    Attributes
    ----------
    _context_class : ``ContentArgumentParserContextBase``
        Context class to interact with the parsed string.
    _rp : `_sre.SRE_Pattern`
        The regex pattern what is passed and used by the caller.
    separator : `str` or `tuple` (`str`, `str`)
        The executed separator by the ``ContentArgumentSeparator`` instance.
    """
    __slots__ = ('_context_class', '_rp', 'separator', 'assigner')
    def __new__(cls, separator, assigner):
        """
        Creates a new ``ContentArgumentSeparator`` instance. If one already exists with the given parameters, returns
        that instead.
        
        Parameters
        ----------
        separator : `str`, `tuple` (`str`, `str`)
            The executed separator by the ``ContentArgumentSeparator`` instance.
        assigner : `str`
            The assigner for keyword-only arguments.
        
        Raises
        ------
        TypeError
            - If `separator` is not given as `None`, ``ContentArgumentSeparator``, `str`, neither as `tuple` instance.
            - If `separator` was given as `tuple`, but it's element are not `str` instances.
            - If `assigner` was not given as `str` instance.
        ValueError
            - If `separator` is given as `str`, but it's length is not `1`.
            - If `separator` is given as `str`, but it is a space character.
            - If `separator` is given as `tuple`, but one of it's element's length is not `1`.
            - If `separator` is given as `tuple`, but one of it's element's is a space character.
            - If `assigner`'s length is not `1`.
        """
        if separator is None:
            return DEFAULT_SEPARATOR
        
        separator_type = type(separator)
        if separator_type is str:
            processed_separator = separator
        elif separator_type is tuple:
            processed_separator = list(separator)
        elif issubclass(separator_type, str):
            processed_separator = str(separator)
            separator_type = str
        elif issubclass(separator_type, tuple):
            processed_separator = list(separator)
            separator_type = tuple
        else:
            raise TypeError(f'`separator` should have be given as `str` or as `tuple` instance, got '
                f'{separator_type.__name__}.')
        
        if separator_type is str:
            if len(processed_separator) != 1:
                raise ValueError(f'`str` separator length can be only `1`, got {separator!r}.')
            
            if processed_separator.isspace():
                raise ValueError(f'`str` separator cannot be a space character`, meanwhile it is, got {separator!r}.')
            
            separator = processed_separator
        
        else:
            if len(processed_separator) != 2:
                raise ValueError(f'`tuple` separator length can be only `2`, got {separator!r}.')
            
            for index in range(2):
                element = processed_separator[index]
                
                element_type = element.__class__
                if element_type is str:
                    processed_element = element
                elif issubclass(element_type, str):
                    processed_element  = str(element)
                    processed_separator[index] = processed_element
                else:
                    raise TypeError(f'`tuple` separator\'s elements can be only `str` instances, meanwhile it\'s '
                        f'element under index `{index}` is type {element_type.__name__!r}.')
                
                if len(processed_element) != 1:
                    raise ValueError(f'`tuple` separator\'s elements can be only `str` with length of `1`, meanwhile '
                        f'it\'s element under index `{index}` is not, got {element!r}.')
                
                if processed_element.isspace():
                    raise ValueError(f'`tuple` separator\'s elements cannot be space character`, meanwhile it\'s '
                        f'element under index `{index}` is, got {element!r}.')
            
            separator = tuple(processed_separator)
        
        assigner_type = type(assigner)
        if assigner_type is str:
            pass
        elif issubclass(assigner_type, str):
            assigner = str(assigner)
        else:
            raise TypeError(f'`assigner` can be given as `str` instance, got {assigner_type.__name__}.')
        
        if len(assigner) != 1:
            raise ValueError(f'`assigner` length can be `1`, got {len(assigner)}; {assigner!r}.')
        
        try:
            return CONTENT_ARGUMENT_PARSERS[(separator, assigner)]
        except KeyError:
            pass
        
        assigner_escaped = re.escape(assigner)
        if separator_type is str:
            escaped_separator = re.escape(separator)
            rp = re.compile(f'[{escaped_separator}\s]*((?:([^\s{assigner_escaped}]+?)\s*{assigner_escaped}\s*)?(.+?))\s*(?:$|[{escaped_separator})]+)', re.M|re.S)
            
            context_class = ContentArgumentParserContextSeparator
        else:
            start, end = separator
            if start == end:
                escaped_separator = re.escape(start)
                rp = re.compile(f'\s*(?:([^\s{assigner_escaped}]+?)\s*{assigner_escaped}\s*)?(?:(?:{escaped_separator}(.+?)(?:$|{escaped_separator}))|(?:(.+?)(?:$|[{escaped_separator}\s]+)))', re.M|re.S)
            
            else:
                separator_start_escaped = re.escape(start)
                separator_end_escaped = re.escape(end)
                rp = re.compile(f'\s*(?:([^\s{assigner_escaped}]+?)\s*{assigner_escaped}\s*)?(?:(?:{separator_start_escaped}(.+?)(?:$|{separator_end_escaped}))|(?:(.+?)(?:$|[{separator_start_escaped}\s]+)))', re.M|re.S)
            
            context_class = ContentArgumentParserContextEncapsulator
        
        self = object.__new__(cls)
        self.separator = separator
        self._rp = rp
        self._context_class = context_class
        
        CONTENT_ARGUMENT_PARSERS[(separator, assigner)] = self
        return self
    
    def __call__(self, content, index):
        """
        Calls the content argument separator to get the next part of the given content.
        
        Parameters
        ----------
        content : `str`
            The content what's next part we are going to be parsed.
        index : `int`
            The starter index of the content to parse from.
        
        Returns
        -------
        part : `str`
            The parsed out part.
        index : `int`
            The index where the next parsing should start from.
        """
        return self._context_class(self._rp.match(content, index))
    
    def __repr__(self):
        """Returns the content argument separator's representation."""
        return f'{self.__class__.__name__}({self.separator!r}, {self.assigner!r})'
    
    def __hash__(self):
        """Returns the content argument parser's hash."""
        return hash(self.separator) ^ hash(self.assigner)
    
    def __eq__(self, other):
        """Returns whether the two content argument separator are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.separator != other.separator:
            return False
        
        if self.assigner != other.assigner:
            return False
        
        return True


DEFAULT_SEPARATOR = ContentArgumentParser(DEFAULT_ARGUMENT_SEPARATOR, DEFAULT_ARGUMENT_ASSIGNER)


