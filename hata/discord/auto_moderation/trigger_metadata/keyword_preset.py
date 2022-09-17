__all__ = ('AutoModerationRuleTriggerMetadataKeywordPreset', )

from scarletio import copy_docs, include

from .base import AutoModerationRuleTriggerMetadataBase


AutoModerationKeywordPresetType = include('AutoModerationKeywordPresetType')


class AutoModerationRuleTriggerMetadataKeywordPreset(AutoModerationRuleTriggerMetadataBase):
    """
    Keyword keyword preset trigger metadata for an auto moderation rule.
    
    Attributes
    ----------
    excluded_keywords : `None`, `tuple` of `str`
        Excluded keywords from under the rule.
    keyword_presets : `None`, `tuple` of `AutoModerationKeywordPresetType`
        Substrings which will be searched for in content.
    """
    __slots__ = ('excluded_keywords', 'keyword_presets',)
    
    def __new__(cls, keyword_presets, excluded_keywords=None):
        """
        Creates a new keyword preset trigger metadata for ``AutoModerationRule``-s.
        
        Parameters
        ----------
        keyword_presets : `None`, `int`, ``AutoModerationKeywordPresetType``, \
                `iterable` of (`int`, ``AutoModerationKeywordPresetType``)
            Keyword preset defined by Discord which will be searched for in content.
        
        excluded_keywords : `None`, `str`, `iterable` of `str` = `None`, Optional (Keyword only)
            Excluded keywords from the preset.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        """
        # excluded_keywords
        if excluded_keywords is None:
            processed_excluded_keywords = None
        
        elif isinstance(excluded_keywords, str):
            processed_excluded_keywords = (excluded_keywords, )
        
        else:
            iterator = getattr(type(excluded_keywords), '__iter__', None)
            if iterator is None:
                raise TypeError(
                    f'`excluded_keywords` can be `None`, `str`, `iterable` of `str`, '
                    f'got {excluded_keywords.__class__.__name__}; {excluded_keywords!r}.'
                )
            
            processed_excluded_keywords = None
            
            for excluded_keyword in iterator(excluded_keywords):
                if not isinstance(excluded_keyword, str):
                    raise TypeError(
                        f'`excluded_keywords` can contain `str` elements, got {excluded_keyword.__class__.__name__}; {excluded_keyword!r}; '
                        f'excluded_keywords={excluded_keywords!r}'
                    )
                
                if processed_excluded_keywords is None:
                    processed_excluded_keywords = set()
                
                processed_excluded_keywords.add(excluded_keyword)
            
            if (processed_excluded_keywords is not None):
                processed_excluded_keywords = tuple(sorted(processed_excluded_keywords))
        
        # keyword_presets
        if keyword_presets is None:
            processed_keyword_presets = None
        
        elif isinstance(keyword_presets, int):
            keyword_preset = AutoModerationKeywordPresetType.get(keyword_presets)
            processed_keyword_presets = (keyword_preset, )
        
        elif isinstance(keyword_presets, AutoModerationKeywordPresetType):
            processed_keyword_presets = (keyword_presets, )
        
        else:
            iterator = getattr(type(keyword_presets), '__iter__', None)
            if iterator is None:
                raise TypeError(
                    f'`keyword_presets` can be `None`, `int`, `{AutoModerationKeywordPresetType.__name__}`, '
                    f'`iterable` of (`int`, `{AutoModerationKeywordPresetType.__name__}`'
                    f'got {keyword_presets.__class__.__name__}; {keyword_presets!r}.'
                )
            
            processed_keyword_presets = None
            
            for keyword_preset in iterator(keyword_presets):
                if isinstance(keyword_preset, int):
                    keyword_preset = AutoModerationKeywordPresetType.get(keyword_preset)
                
                elif isinstance(keyword_preset, AutoModerationKeywordPresetType):
                    pass
                
                else:
                    raise TypeError(
                        f'`keyword_preset` can contain `int`, `{AutoModerationKeywordPresetType.__name__}` elements, '
                        f'got {keyword_preset.__class__.__name__}; {keyword_preset!r}; '
                        f'keyword_presets={keyword_presets!r}'
                    )
                
                if processed_keyword_presets is None:
                    processed_keyword_presets = set()
                
                processed_keyword_presets.add(keyword_preset)
            
            if (processed_keyword_presets is not None):
                processed_keyword_presets = tuple(sorted(processed_keyword_presets))
        
        
        
        
        self = object.__new__(cls)
        self.excluded_keywords = processed_excluded_keywords
        self.keyword_presets = processed_keyword_presets
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # keyword_presets
        keyword_presets = self.keyword_presets
        repr_parts.append(' keywords=[')
        if (keyword_presets is not None):
            index = 0
            limit = len(keyword_presets)
            while True:
                keyword = keyword_presets[index]
                repr_parts.append(repr(keyword.name))
                repr_parts.append('~')
                repr_parts.append(repr(keyword.value))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(']')
        
        # excluded_keywords
        excluded_keywords = self.excluded_keywords
        repr_parts.append(' excluded_keywords=[')
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
        # excluded_keywords
        excluded_keyword_array = data.get('allow_list', None)
        if (excluded_keyword_array is None) or (not excluded_keyword_array):
            excluded_keywords = None
        else:
            excluded_keywords = tuple(sorted(excluded_keyword_array))
        
        # keyword_preset_array
        keyword_preset_array = data.get('presets', None)
        if (keyword_preset_array is None) or (not keyword_preset_array):
            keyword_presets = None
        else:
            keyword_presets = tuple(sorted(
                AutoModerationKeywordPresetType.get(keyword_preset) for keyword_preset in keyword_preset_array
            ))
        
        self = object.__new__(cls)
        self.excluded_keywords = excluded_keywords
        self.keyword_presets = keyword_presets
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.to_data)
    def to_data(self):
        data = {}
        
        # excluded_keywords
        data['allow_list'] = [*self.iter_excluded_keywords()]
        
        # keyword_presets
        data['presets'] = [*self.iter_keyword_presets()]
        
        return data
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # excluded_keywords
        if self.excluded_keywords != other.excluded_keywords:
            return False
        
        # keyword_presets
        if self.keyword_presets != other.keyword_presets:
            return False
        
        return True
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # excluded_keywords
        excluded_keywords = self.excluded_keywords
        if (excluded_keywords is not None):
            hash_value ^= len(excluded_keywords)
            
            for excluded_keyword in excluded_keywords:
                hash_value ^= hash(excluded_keyword)
        
        # keyword_presets
        keyword_presets = self.keyword_presets
        if (keyword_presets is not None):
            hash_value ^= len(keyword_presets)
            
            shift = 0
            
            for keyword_preset in keyword_presets:
                shift += 4
                
                hash_value ^= keyword_preset.value << shift
        
        
        return hash_value
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.copy)
    def copy(self):
        new = AutoModerationRuleTriggerMetadataBase.copy(self)
        
        # keyword_presets
        keyword_presets = self.keyword_presets
        if (keyword_presets is not None):
            keyword_presets = tuple(keyword_preset for keyword_preset in keyword_presets)
        new.keyword_presets = keyword_presets
        
        # excluded_keywords
        excluded_keywords = self.excluded_keywords
        if (excluded_keywords is not None):
            excluded_keywords = tuple(excluded_keyword for excluded_keyword in excluded_keywords)
        new.excluded_keywords = excluded_keywords
        
        return new
    
    
    def iter_excluded_keywords(self):
        """
        Iterates over the excluded keyword of the keyword trigger metadata.
        
        This method is an iterable generator.
        
        Yields
        ------
        excluded_keyword : `str`
        """
        excluded_keywords = self.excluded_keywords
        if (excluded_keywords is not None):
            yield from excluded_keywords
    
    
    def iter_keyword_presets(self):
        """
        Iterates over the keyword presets of the keyword trigger metadata.
        
        This method is an iterable generator.
        
        Yields
        ------
        keyword_preset : `AutoModerationKeywordPresetType`
        """
        keyword_presets = self.keyword_presets
        if (keyword_presets is not None):
            yield from keyword_presets
