__all__ = ('ActivityMetadataCustom',)

from scarletio import copy_docs

from ...utils import DATETIME_FORMAT_CODE

from .base import _pop_empty_name, ActivityMetadataBase
from .fields import (
    parse_created_at, parse_emoji, parse_state, put_created_at_into, put_emoji_into, put_state_into,
    validate_created_at, validate_emoji, validate_state
)


class ActivityMetadataCustom(ActivityMetadataBase):
    """
    Represents a Discord custom activity.
    
    Attributes
    ----------
    created_at : `None`, `datetime`
        When the status was created.
    emoji : `None`, ``Emoji``
        The emoji of the activity. If it has no emoji, then set as `None`.
    state : `None`, `str`
        The activity's text under it's emoji. Defaults to `None`.
    """
    __slots__ = ('created_at', 'emoji', 'state', )
    
    
    def __new__(cls, *, created_at = ..., emoji = ..., state = ...):
        """
        Creates a new custom activity metadata.
        
        Parameters
        ----------
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the status was created.
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The emoji of the activity.
        state : `None`, `str`, Optional (Keyword only)
            The activity's text under it's emoji.
        
        Raises
        ------
        TypeError
            - If a parameter's type is unexpected.
        ValueError
           - If an parameter's value is unexpected.
        """
        # created_at
        if created_at is ...:
            created_at = None
        else:
            created_at = validate_created_at(created_at)
        
        # emoji
        if emoji is ...:
            emoji = None
        else:
            emoji = validate_emoji(emoji)
        
        # state
        if state is ...:
            state = None
        else:
            state = validate_state(state)
        
        # Construct
        self = object.__new__(cls)
        self.created_at = created_at
        self.emoji = emoji
        self.state = state
        return self
        
    
    @classmethod
    @copy_docs(ActivityMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        _pop_empty_name(keyword_parameters)
        return cls(
            created_at = keyword_parameters.pop('created_at', ...),
            emoji = keyword_parameters.pop('emoji', ...),
            state = keyword_parameters.pop('state', ...),
        )
    
    
    @copy_docs(ActivityMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # created_at
        created_at = self.created_at
        if (created_at is not None):
            repr_parts.append(' created_at = ')
            repr_parts.append(format(created_at, DATETIME_FORMAT_CODE))
            
            field_added = True
        else:
            field_added = False
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' emoji = ')
            repr_parts.append(repr(emoji))
        
        # state
        state = self.state
        if (state is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' state = ')
            repr_parts.append(repr(state))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ActivityMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # created_a
        created_at = self.created_at
        if (created_at is not None):
            hash_value ^= hash(created_at)
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= hash(emoji)
        
        # state
        state = self.state
        if (state is not None):
            hash_value ^= hash(state)
        
        return hash_value
    
    
    @copy_docs(ActivityMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # created_at
        if self.created_at != other.created_at:
            return False
        
        # emoji
        if self.emoji != other.emoji:
            return False
        
        # state
        if self.state != other.state:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ActivityMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self._update_attributes(data)
        return self
    
    
    @copy_docs(ActivityMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False, user = False):
        data = {}
        
        if include_internals:
            data['name'] = 'Custom Status'
            put_created_at_into(self.created_at, data, defaults)
            put_emoji_into(self.emoji, data, defaults)
            put_state_into(self.state, data, defaults)
        
        return data
    
    
    @copy_docs(ActivityMetadataBase._update_attributes)
    def _update_attributes(self, data):
        self.created_at = parse_created_at(data)
        self.emoji = parse_emoji(data)
        self.state = parse_state(data)
    
    
    @copy_docs(ActivityMetadataBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = {}
        
        # created_at
        created_at = parse_created_at(data)
        if self.created_at != created_at:
            old_attributes['created_at'] = self.created_at
            self.created_at = created_at
        
        # emoji
        emoji = parse_emoji(data)
        if self.emoji != emoji:
            old_attributes['emoji'] = self.emoji
            self.emoji = emoji
        
        # state
        state = parse_state(data)
        if self.state != state:
            old_attributes['state'] = self.state
            self.state = state
        
        return old_attributes
    
    
    @copy_docs(ActivityMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.created_at = self.created_at
        new.emoji = self.emoji
        new.state = self.state
        return new
    
    
    def copy_with(self, *, created_at = ..., emoji = ..., state = ...):
        """
        Copies the custom activity metadata with the given fields.
        
        Parameters
        ----------
        created_at : `None`, `datetime`, Optional (Keyword only)
            When the status was created.
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The emoji of the activity.
        state : `None`, `str`, Optional (Keyword only)
            The activity's text under it's emoji.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is unexpected.
        ValueError
           - If an parameter's value is unexpected.
        """
        # created_at
        if created_at is ...:
            created_at = self.created_at
        else:
            created_at = validate_created_at(created_at)
        
        # emoji
        if emoji is ...:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # state
        if state is ...:
            state = self.state
        else:
            state = validate_state(state)
        
        # Construct
        new = object.__new__(type(self))
        new.created_at = created_at
        new.emoji = emoji
        new.state = state
        return new
    
    
    @copy_docs(ActivityMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        _pop_empty_name(keyword_parameters)
        return self.copy_with(
            created_at = keyword_parameters.pop('created_at', ...),
            emoji = keyword_parameters.pop('emoji', ...),
            state = keyword_parameters.pop('state', ...),
        )
    
    
    @property
    def name(self):
        """
        Returns the activity's display text.
        
        Returns
        -------
        name : `str`
        """
        state = self.state
        emoji = self.emoji
        if (state is None):
            if (emoji is None):
                name = ''
            else:
                name = emoji.as_emoji
        else:
            if (emoji is None):
                name = state
            else:
                name = f'{emoji.as_emoji} {state}'
        
        return name
