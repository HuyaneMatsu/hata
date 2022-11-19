__all__ = ('AutoModerationRuleTriggerMetadataKeyword',)

from scarletio import copy_docs

from .base import AutoModerationRuleTriggerMetadataBase
from .fields import (
    parse_excluded_keywords, parse_keywords, parse_regex_patterns, put_excluded_keywords_into, put_keywords_into,
    put_regex_patterns_into, validate_excluded_keywords, validate_keywords, validate_regex_patterns
)


class AutoModerationRuleTriggerMetadataKeyword(AutoModerationRuleTriggerMetadataBase):
    """
    Keyword trigger metadata for an auto moderation rule.
    
    Attributes
    ----------
    excluded_keywords : `None`, `tuple` of `str`
        Excluded keywords from under the rule.
    
    keywords : `None`, `tuple` of `str`
        Substrings which will be searched for in content.
    
    regex_patterns : `None`, `tuple` of `str`
        Regular expression patterns which are matched against content.
        
        > Only rust flavored regex is supported.
    
    Matching Strategies
    -------------------
    Use the `*` wildcard symbol at the beginning and end of a keyword to define how the keyword should be matched.
    All keywords are not case sensitive.
    
    - `Prefix` - word must start with the keyword
        +-----------+---------------------------------------+
        | Keyword   | Matches                               |
        +===========+=======================================+
        | cat*      | catch, Catapult, CAttLE               |
        +-----------+---------------------------------------+
        | tra*      | train, trade, TRAditional             |
        +-----------+---------------------------------------+
        | the mat*  | the matrix                            |
        +-----------+---------------------------------------+
    
    
    - `Suffix` - word must end with the keyword
    
        +-----------+---------------------------------------+
        | Keyword   | Matches                               |
        +===========+=======================================+
        | *cat      | wildcat, copyCat                      |
        +-----------+---------------------------------------+
        | *tra      | extra, ultra, orchesTRA               |
        +-----------+---------------------------------------+
        | *the mat  | breathe mat                           |
        +-----------+---------------------------------------+
    
    
    - `Anywhere` - keyword can appear anywhere in the content
    
        +-----------+---------------------------------------+
        | Keyword     | Matches                             |
        +===========+=======================================+
        | *cat*       | location, eduCation                 |
        +-----------+---------------------------------------+
        | *tra*       | abstracted, outrage                 |
        +-----------+---------------------------------------+
        | *the mat*   | breathe matter                      |
        +-----------+---------------------------------------+
    
    
    - `Whole Word` - keyword is a full word or phrase and must be surrounded by whitespace at the beginning and end
    
        +-----------+---------------------------------------+
        | Keyword   | Matches                               |
        +===========+=======================================+
        | cat       | cat                                   |
        +-----------+---------------------------------------+
        | train     | train                                 |
        +-----------+---------------------------------------+
        | the mat   | the mat                               |
        +-----------+---------------------------------------+
    """
    __slots__ = ('excluded_keywords', 'keywords', 'regex_patterns')
    
    def __new__(cls, keywords = None, regex_patterns = None, excluded_keywords = None):
        """
        Creates a new keyword trigger metadata for ``AutoModerationRule``-s.
        
        Parameters
        ----------
        keywords : `None`, `str`, `iterable` of `str` = `None`, Optional
            Substrings which will be searched for in content.
        
        regex_patterns : `None`, `tuple` of `str` = `None`, Optional
            Regular expression patterns which are matched against content.
        
        excluded_keywords : `None`, `str`, `iterable` of `str` = `None`, Optional
            Excluded keywords from the preset.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        """
        excluded_keywords = validate_excluded_keywords(excluded_keywords)
        keywords = validate_keywords(keywords)
        regex_patterns = validate_regex_patterns(regex_patterns)
        
        self = object.__new__(cls)
        self.excluded_keywords = excluded_keywords
        self.keywords = keywords
        self.regex_patterns = regex_patterns
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # keywords
        keywords = self.keywords
        repr_parts.append(' keywords = [')
        if (keywords is not None):
            index = 0
            limit = len(keywords)
            while True:
                keyword = keywords[index]
                repr_parts.append(repr(keyword))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(']')
        
        # regex_patterns
        regex_patterns = self.regex_patterns
        repr_parts.append(', regex_patterns = [')
        if (regex_patterns is not None):
            index = 0
            limit = len(regex_patterns)
            while True:
                keyword = regex_patterns[index]
                repr_parts.append(repr(keyword))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(']')
        
        # excluded_keywords
        excluded_keywords = self.excluded_keywords
        repr_parts.append(', excluded_keywords = [')
        if (excluded_keywords is not None):
            index = 0
            limit = len(excluded_keywords)
            while True:
                excluded_keyword = excluded_keywords[index]
                repr_parts.append(repr(excluded_keyword))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationRuleTriggerMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.excluded_keywords = parse_excluded_keywords(data)
        self.keywords = parse_keywords(data)
        self.regex_patterns = parse_regex_patterns(data)
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.to_data)
    def to_data(self, defaults = False):
        data = {}
        put_excluded_keywords_into(self.excluded_keywords, data, defaults)
        put_keywords_into(self.keywords, data, defaults)
        put_regex_patterns_into(self.regex_patterns, data, defaults)
        return data
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # excluded_keywords
        if self.excluded_keywords != other.excluded_keywords:
            return False
        
        # keywords
        if self.keywords != other.keywords:
            return False
        
        # regex_patterns
        if self.regex_patterns != other.regex_patterns:
            return False
        
        return True
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # excluded_keywords
        excluded_keywords = self.excluded_keywords
        if (excluded_keywords is not None):
            hash_value ^= len(excluded_keywords) << 8
            
            for excluded_keyword in excluded_keywords:
                hash_value ^= hash(excluded_keyword)
        
        # keywords
        keywords = self.keywords
        if (keywords is not None):
            hash_value ^= len(keywords)
            
            for keyword in keywords:
                hash_value ^= hash(keyword)
        
        # regex_patterns
        regex_patterns = self.regex_patterns
        if (regex_patterns is not None):
            hash_value ^= len(regex_patterns) << 4
            
            for regex_pattern in regex_patterns:
                hash_value ^= hash(regex_pattern)
        
        return hash_value
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # excluded_keywords
        excluded_keywords = self.excluded_keywords
        if (excluded_keywords is not None):
            excluded_keywords = (*excluded_keywords, )
        new.excluded_keywords = excluded_keywords
        
        # keywords
        keywords = self.keywords
        if (keywords is not None):
            keywords = (*keywords, )
        new.keywords = keywords
        
        # regex_patterns
        regex_patterns = self.regex_patterns
        if (regex_patterns is not None):
            regex_patterns = (*regex_patterns, )
        new.regex_patterns = regex_patterns
        
        return new

    
    def copy_with(self, *, excluded_keywords = ..., keywords = ..., regex_patterns = ...):
        """
        Copies the trigger metadata with altering it's attributes based on the given fields.
        
        Parameters
        ----------
        excluded_keywords : `None`, `str`, `iterable` of `str, Optional (Keyword only)
            Excluded keywords from the rule.
        
        keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Substrings which will be searched for in content.
        
        regex_patterns : `None`, `tuple` of `str`, Optional (Keyword only)
            Regular expression patterns which are matched against content.
        
        Returns
        -------
        new : `instance<type<self>>`
               
        Raises
        ------
        TypeError
            - If a parameter of incorrect type is given.
        """
        # excluded_keywords
        if excluded_keywords is ...:
            excluded_keywords = self.excluded_keywords
            if (excluded_keywords is not None):
                excluded_keywords = (*excluded_keywords, )
        else:
            excluded_keywords = validate_excluded_keywords(excluded_keywords)
        
        # keywords
        if keywords is ...:
            keywords = self.keywords
            if (keywords is not None):
                keywords = (*keywords, )
        else:
            keywords = validate_keywords(keywords)
        
        # regex_patterns
        if regex_patterns is ...:
            regex_patterns = self.regex_patterns
            if (regex_patterns is not None):
                regex_patterns = (*regex_patterns, )
        else:
            regex_patterns = validate_regex_patterns(regex_patterns)
        
        new = object.__new__(type(self))
        new.excluded_keywords = excluded_keywords
        new.keywords = keywords
        new.regex_patterns = regex_patterns
        return new
