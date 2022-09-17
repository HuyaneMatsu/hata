__all__ = ('AutoModerationRuleTriggerMetadataKeyword',)

from scarletio import copy_docs

from .base import AutoModerationRuleTriggerMetadataBase


class AutoModerationRuleTriggerMetadataKeyword(AutoModerationRuleTriggerMetadataBase):
    """
    Keyword trigger metadata for an auto moderation rule.
    
    Attributes
    ----------
    keywords : `None`, `tuple` of `str`
        Substrings which will be searched for in content.
    
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
    __slots__ = ('keywords',)
    
    def __new__(cls, keywords):
        """
        Creates a new keyword trigger metadata for ``AutoModerationRule``-s.
        
        Parameters
        ----------
        keywords : `None`, `str`, `iterable` of `str`
            Substrings which will be searched for in content.
               
        Raises
        ------
        TypeError
            - If `keywords` type is incorrect.
            - If a keyword's type is incorrect.
        """
        if keywords is None:
            processed_keywords = None
        
        elif isinstance(keywords, str):
            processed_keywords = (keywords, )
        
        else:
            iterator = getattr(type(keywords), '__iter__', None)
            if iterator is None:
                raise TypeError(
                    f'`keywords` can be `None`, `str`, `iterable` of `str`, '
                    f'got {keywords.__class__.__name__}; {keywords!r}.'
                )
            
            processed_keywords = None
            
            for keyword in iterator(keywords):
                if not isinstance(keyword, str):
                    raise TypeError(
                        f'`keywords` can contain `str` elements, got {keyword.__class__.__name__}; {keyword!r}; '
                        f'keywords={keywords!r}'
                    )
                
                if processed_keywords is None:
                    processed_keywords = set()
                
                processed_keywords.add(keyword)
            
            if (processed_keywords is not None):
                processed_keywords = tuple(sorted(processed_keywords))
        
        self = object.__new__(cls)
        self.keywords = processed_keywords
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # keywords
        keywords = self.keywords
        repr_parts.append(' keywords=[')
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
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationRuleTriggerMetadataBase.from_data)
    def from_data(cls, data):
        keyword_array = data.get('keyword_filter', None)
        if (keyword_array is None) or (not keyword_array):
            keywords = None
        else:
            keywords = tuple(sorted(keyword_array))
        
        self = object.__new__(cls)
        self.keywords = keywords
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.to_data)
    def to_data(self):
        data = {}
        
        data['keyword_filter'] = [*self.iter_keywords()]
        
        return data
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.keywords != other.keywords:
            return False
        
        return True
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        keywords = self.keywords
        if (keywords is not None):
            hash_value ^= len(keywords)
            
            for keyword in keywords:
                hash_value ^= hash(keyword)
        
        return hash_value
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.copy)
    def copy(self):
        new = AutoModerationRuleTriggerMetadataBase.copy(self)
        
        # keywords
        keywords = self.keywords
        if (keywords is not None):
            keywords = tuple(keyword for keyword in keywords)
        new.keywords = keywords
        
        return new
    
    
    def iter_keywords(self):
        """
        Iterates over the keywords of the keyword trigger metadata.
        
        This method is an iterable generator.
        
        Yields
        ------
        keyword : `str`
        """
        keywords = self.keywords
        if (keywords is not None):
            yield from keywords
