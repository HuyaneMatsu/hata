__all__ = ('AutoModerationRuleTriggerMetadataKeywordPreset', )

from scarletio import copy_docs

from .base import AutoModerationRuleTriggerMetadataBase
from .fields import (
    parse_excluded_keywords, parse_keyword_presets, put_excluded_keywords_into, put_keyword_presets_into,
    validate_excluded_keywords, validate_keyword_presets
)


class AutoModerationRuleTriggerMetadataKeywordPreset(AutoModerationRuleTriggerMetadataBase):
    """
    Keyword keyword preset trigger metadata for an auto moderation rule.
    
    Attributes
    ----------
    excluded_keywords : `None`, `tuple` of `str`
        Excluded keywords from under the rule.
    
    keyword_presets : `None`, `tuple` of ``AutoModerationKeywordPresetType``
        Keyword preset defined by Discord which will be searched for in content.
    """
    __slots__ = ('excluded_keywords', 'keyword_presets',)
    
    def __new__(cls, keyword_presets = None, excluded_keywords = None):
        """
        Creates a new keyword preset trigger metadata for ``AutoModerationRule``-s.
        
        Parameters
        ----------
        keyword_presets : `None`, `int`, ``AutoModerationKeywordPresetType``, \
                `iterable` of (`int`, ``AutoModerationKeywordPresetType``) = `None`, Optional
            Keyword preset defined by Discord which will be searched for in content.
        
        excluded_keywords : `None`, `str`, `iterable` of `str` = `None`, Optional
            Excluded keywords from the preset.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        """
        excluded_keywords = validate_excluded_keywords(excluded_keywords)
        keyword_presets = validate_keyword_presets(keyword_presets)
        
        self = object.__new__(cls)
        self.excluded_keywords = excluded_keywords
        self.keyword_presets = keyword_presets
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # keyword_presets
        keyword_presets = self.keyword_presets
        repr_parts.append(' keywords = [')
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
        self.keyword_presets = parse_keyword_presets(data)
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_excluded_keywords_into(self.excluded_keywords, data, defaults)
        put_keyword_presets_into(self.keyword_presets, data, defaults)
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
        new = object.__new__(type(self))
        
        # excluded_keywords
        excluded_keywords = self.excluded_keywords
        if (excluded_keywords is not None):
            excluded_keywords = (*excluded_keywords,)
        new.excluded_keywords = excluded_keywords
        
        # keyword_presets
        keyword_presets = self.keyword_presets
        if (keyword_presets is not None):
            keyword_presets = (*keyword_presets,)
        new.keyword_presets = keyword_presets
        
        return new


    
    def copy_with(self, *, excluded_keywords = ..., keyword_presets = ...):
        """
        Copies the trigger metadata with altering it's attributes based on the given fields.
        
        Parameters
        ----------
        excluded_keywords : `None`, `str`, `iterable` of `str, Optional (Keyword only)
            Excluded keywords from the rule.
        
        keyword_presets : `None`, `int`, ``AutoModerationKeywordPresetType``, \
                `iterable` of (`int`, ``AutoModerationKeywordPresetType``), Optional (Keyword only)
            Keyword preset defined by Discord which will be searched for in content.
        
        Returns
        -------
        new : `instance<type<self>>`
               
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        """
        # excluded_keywords
        if excluded_keywords is ...:
            excluded_keywords = self.excluded_keywords
            if (excluded_keywords is not None):
                excluded_keywords = (*excluded_keywords, )
        else:
            excluded_keywords = validate_excluded_keywords(excluded_keywords)
        
        # keyword_presets
        if keyword_presets is ...:
            keyword_presets = self.keyword_presets
            if (keyword_presets is not None):
                keyword_presets = (*keyword_presets, )
        else:
            keyword_presets = validate_keyword_presets(keyword_presets)
        
        new = object.__new__(type(self))
        new.excluded_keywords = excluded_keywords
        new.keyword_presets = keyword_presets
        return new
