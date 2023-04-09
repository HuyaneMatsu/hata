__all__ = ('AutoModerationRuleTriggerMetadataMentionSpam',)

from scarletio import copy_docs

from .base import AutoModerationRuleTriggerMetadataBase
from .constants import AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
from .fields import (
    parse_mention_limit, parse_raid_protection, put_mention_limit_into, put_raid_protection_into,
    validate_mention_limit, validate_raid_protection
)


class AutoModerationRuleTriggerMetadataMentionSpam(AutoModerationRuleTriggerMetadataBase):
    """
    Mention spam trigger metadata for an auto moderation rule.
    
    Attributes
    ----------
    mention_limit : `int`
        The amount of mentions in a message after the rule is triggered.
    raid_protection : `bool`
        Whether mention raid protection is enabled.
    """
    __slots__ = ('mention_limit', 'raid_protection')
    
    def __new__(cls, mention_limit = ..., *, raid_protection = ...):
        """
        Creates a new mention spam trigger metadata for ``AutoModerationRule``-s.
        
        Parameters
        ----------
        mention_limit : `int`, Optional
            The amount of mentions in a message after the rule is triggered.
            
            Defaults to the allowed maximal amount.
        raid_protection : `bool`, Optional
            Whether mention raid protection is enabled.
        
        Raises
        ------
        TypeError
            - If `mention_limit` type is incorrect.
        """
        # mention_limit
        if mention_limit is ...:
            mention_limit = AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
        else:
            mention_limit = validate_mention_limit(mention_limit)
        
        # raid_protection
        if raid_protection is ...:
            raid_protection = False
        else:
            raid_protection = validate_raid_protection(raid_protection)
        
        # Construct
        self = object.__new__(cls)
        self.mention_limit = mention_limit
        self.raid_protection = raid_protection
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # mention_limit
        repr_parts.append(' mention_limit = ')
        repr_parts.append(repr(self.mention_limit))
        
        raid_protection = self.raid_protection
        if raid_protection:
            repr_parts.append(', raid_protection = ')
            repr_parts.append(repr(raid_protection))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationRuleTriggerMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.mention_limit = parse_mention_limit(data)
        self.raid_protection = parse_raid_protection(data)
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.to_data)
    def to_data(self, *, defaults = False):
        data = {}
        put_mention_limit_into(self.mention_limit, data, defaults)
        put_raid_protection_into(self.raid_protection, data, defaults)
        return data
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # mention_limit
        if self.mention_limit != other.mention_limit:
            return False
        
        # raid_protection
        if self.raid_protection != other.raid_protection:
            return False
        
        return True
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # mention_limit
        hash_value ^= self.mention_limit
        
        # raid_protection
        hash_value ^= self.raid_protection << 6
        
        return hash_value
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.mention_limit = self.mention_limit
        new.raid_protection = self.raid_protection
        return new
    
    
    def copy_with(self, *, mention_limit = ..., raid_protection = ...):
        """
        Copies the trigger metadata with altering it's attributes based on the given fields.
        
        Parameters
        ----------
        mention_limit : `int`, Optional (Keyword only)
            The amount of mentions in a message after the rule is triggered.
        raid_protection : `bool`, Optional
            Whether mention raid protection is enabled.
        
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
        
        # raid_protection
        if raid_protection is ...:
            raid_protection = self.raid_protection
        else:
            raid_protection = validate_raid_protection(raid_protection)
        
        new = object.__new__(type(self))
        new.mention_limit = mention_limit
        new.raid_protection = raid_protection
        return new
