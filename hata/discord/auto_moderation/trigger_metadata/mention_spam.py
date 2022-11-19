__all__ = ('AutoModerationRuleTriggerMetadataMentionSpam',)

from scarletio import copy_docs

from .base import AutoModerationRuleTriggerMetadataBase
from .fields import parse_mention_limit, put_mention_limit_into, validate_mention_limit


class AutoModerationRuleTriggerMetadataMentionSpam(AutoModerationRuleTriggerMetadataBase):
    """
    Mention spam trigger metadata for an auto moderation rule.
    
    Attributes
    ----------
    mention_limit : `int`
        The amount of mentions in a message after the rule is triggered.
    """
    __slots__ = ('mention_limit',)
    
    def __new__(cls, mention_limit = None):
        """
        Creates a new mention spam trigger metadata for ``AutoModerationRule``-s.
        
        Parameters
        ----------
        mention_limit : `None`, `int`, = `None`, Optional
            The amount of mentions in a message after the rule is triggered.
            
            Defaults to the allowed maximal amount if given as `None`.
            
        Raises
        ------
        TypeError
            - If `mention_limit` type is incorrect.
        """
        mention_limit = validate_mention_limit(mention_limit)
        
        self = object.__new__(cls)
        self.mention_limit = mention_limit
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # mention_limit
        repr_parts.append(' mention_limit = ')
        repr_parts.append(repr(self.mention_limit))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationRuleTriggerMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.mention_limit = parse_mention_limit(data)
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_mention_limit_into(self.mention_limit, data, defaults)
        return data
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.mention_limit != other.mention_limit:
            return False
        
        return True
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # mention_limit
        hash_value ^= self.mention_limit
        
        return hash_value
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        # mention_limit
        new.mention_limit = self.mention_limit
        
        return new
    
    
    def copy_with(self, *, mention_limit = ..., keyword_presets = ...):
        """
        Copies the trigger metadata with altering it's attributes based on the given fields.
        
        Parameters
        ----------
        mention_limit : `None`, `int`, Optional (Keyword only)
            The amount of mentions in a message after the rule is triggered.
        
        Returns
        -------
        new : `instance<type<self>>`
               
        Raises
        ------
        TypeError
            - If a parameter of incorrect type given.
        """
        # mention_limit
        if mention_limit is ...:
            mention_limit = self.mention_limit
        else:
            mention_limit = validate_mention_limit(mention_limit)
        
        new = object.__new__(type(self))
        new.mention_limit = mention_limit
        return new
