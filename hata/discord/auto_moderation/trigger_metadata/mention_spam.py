__all__ = ('AutoModerationRuleTriggerMetadataMentionSpam',)

from scarletio import copy_docs

from ..constants import AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX

from .base import AutoModerationRuleTriggerMetadataBase


class AutoModerationRuleTriggerMetadataMentionSpam(AutoModerationRuleTriggerMetadataBase):
    """
    Mention spam trigger metadata for an auto moderation rule.
    
    Attributes
    ----------
    mention_limit : `int`
        The amount of mentions in a message after the rule is triggered.
    """
    __slots__ = ('mention_limit',)
    
    def __new__(cls, mention_limit):
        """
        Creates a new mention spam trigger metadata for ``AutoModerationRule``-s.
        
        Parameters
        ----------
        mention_limit : `None`, `int`
            The amount of mentions in a message after the rule is triggered.
            
            Defaults to the allowed maximal amount if given as `None`.
            
        Raises
        ------
        TypeError
            - If `mention_limit` type is incorrect.
        """
        if (mention_limit is None):
            mention_limit = AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
        
        elif isinstance(mention_limit, int):
            if mention_limit < 0:
                mention_limit = 0
            
            elif mention_limit > AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX:
                mention_limit = AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
            
        else:
            raise TypeError(
                f'`mention_limit` can be `None`, `int`, got {mention_limit.__class__.__name__}; {mention_limit!r}.'
            )
        
        self = object.__new__(cls)
        self.mention_limit = mention_limit
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # mention_limit
        repr_parts.append(' mention_limit=')
        repr_parts.append(repr(self.mention_limit))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    @copy_docs(AutoModerationRuleTriggerMetadataBase.from_data)
    def from_data(cls, data):
        mention_limit = data.get('mention_total_limit', None)
        if (mention_limit is None):
            mention_limit = AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
        
        self = object.__new__(cls)
        self.mention_limit = mention_limit
        return self
    
    
    @copy_docs(AutoModerationRuleTriggerMetadataBase.to_data)
    def to_data(self):
        data = {}
        
        data['mention_total_limit'] = self.mention_limit
        
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
        new = AutoModerationRuleTriggerMetadataBase.copy(self)
        
        # mention_limit
        new.mention_limit = self.mention_limit
        
        return new
