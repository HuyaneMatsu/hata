__all__ = ('ActivityMetadataHanging',)

from scarletio import copy_docs

from ...utils import DATETIME_FORMAT_CODE

from .base import ActivityMetadataBase, _pop_empty_name
from .fields import (
    parse_created_at, parse_details, parse_emoji, parse_hang_type, put_created_at, put_details,
    put_emoji, put_hang_type, validate_created_at, validate_details, validate_emoji, validate_hang_type
)
from .preinstanced import HangType


class ActivityMetadataHanging(ActivityMetadataBase):
    """
    Represents a Discord hang activity.
    
    Attributes
    ----------
    created_at : `None | DateTime`
        When the status was created.
    
    details : `None | str`
        The activity's text next to the emoji.
    
    emoji : ``None | Emoji``
        The emoji of the activity.
    
    hang_type : ``HangType``
        How the user is hanging.
    """
    __slots__ = ('created_at', 'details', 'emoji', 'hang_type', )
    
    
    def __new__(cls, *, created_at = ..., details = ..., emoji = ..., hang_type = ...):
        """
        Creates a new hang activity metadata.
        
        Parameters
        ----------
        created_at : `None | DateTime`, Optional (Keyword only)
            When the activity was created.
        
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The emoji of the activity.
        
        details : `None`, `str`, Optional (Keyword only)
            The activity's text under it's emoji.
        
        hang_type : ``HangType``, Optional (Keyword only)
            How the user is hanging.
        
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
        
        # details
        if details is ...:
            details = None
        else:
            details = validate_details(details)
        
        # emoji
        if emoji is ...:
            emoji = None
        else:
            emoji = validate_emoji(emoji)
        
        # hang_type
        if hang_type is ...:
            hang_type = HangType.custom
        else:
            hang_type = validate_hang_type(hang_type)
        
        # Construct
        self = object.__new__(cls)
        self.created_at = created_at
        self.details = details
        self.emoji = emoji
        self.hang_type = hang_type
        return self
        
    
    @classmethod
    @copy_docs(ActivityMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        _pop_empty_name(keyword_parameters)
        return cls(
            created_at = keyword_parameters.pop('created_at', ...),
            details = keyword_parameters.pop('details', ...),
            emoji = keyword_parameters.pop('emoji', ...),
            hang_type = keyword_parameters.pop('hang_type', ...),
        )
    
    
    @copy_docs(ActivityMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        # created_at
        created_at = self.created_at
        if (created_at is not None):
            repr_parts.append(' created_at = ')
            repr_parts.append(format(created_at, DATETIME_FORMAT_CODE))
            
            field_added = True
        else:
            field_added = False
        
        # details
        details = self.details
        if (details is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = False
            
            repr_parts.append(' details = ')
            repr_parts.append(repr(details))
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' emoji = ')
            repr_parts.append(repr(emoji))
        
        # hang_type
        hang_type = self.hang_type
        if (hang_type is not HangType.none):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' hang_type = ')
            repr_parts.append(hang_type.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(hang_type.value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ActivityMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # created_a
        created_at = self.created_at
        if (created_at is not None):
            hash_value ^= hash(created_at)
        
        # details
        details = self.details
        if (details is not None):
            hash_value ^= hash(details)
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= hash(emoji)
        
        # hang_type
        hang_type = self.hang_type
        if (hang_type is not HangType.none):
            hash_value ^= hash(hang_type)
        
        return hash_value
    
    
    @copy_docs(ActivityMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # created_at
        if self.created_at != other.created_at:
            return False
        
        # details
        if self.details != other.details:
            return False
        
        # emoji
        if self.emoji != other.emoji:
            return False
        
        # hang_type
        if self.hang_type is not other.hang_type:
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
        
        put_hang_type(self.hang_type, data, defaults)
        
        if user or include_internals:
            put_details(self.details, data, defaults)
            put_emoji(self.emoji, data, defaults)
        
        if include_internals:
            data['name'] = 'Hang Status'
            put_created_at(self.created_at, data, defaults)
        
        return data
    
    
    @copy_docs(ActivityMetadataBase._update_attributes)
    def _update_attributes(self, data):
        self.created_at = parse_created_at(data)
        self.details = parse_details(data)
        self.emoji = parse_emoji(data)
        self.hang_type = parse_hang_type(data)
    
    
    @copy_docs(ActivityMetadataBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = {}
        
        # created_at
        created_at = parse_created_at(data)
        if self.created_at != created_at:
            old_attributes['created_at'] = self.created_at
            self.created_at = created_at
        
        # details
        details = parse_details(data)
        if self.details != details:
            old_attributes['details'] = self.details
            self.details = details
        
        # emoji
        emoji = parse_emoji(data)
        if self.emoji != emoji:
            old_attributes['emoji'] = self.emoji
            self.emoji = emoji
        
        # hang_type
        hang_type = parse_hang_type(data)
        if self.hang_type is not hang_type:
            old_attributes['hang_type'] = self.hang_type
            self.hang_type = hang_type
        
        return old_attributes
    
    
    @copy_docs(ActivityMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.created_at = self.created_at
        new.emoji = self.emoji
        new.details = self.details
        new.hang_type = self.hang_type
        return new
    
    
    def copy_with(self, *, created_at = ..., details = ..., emoji = ..., hang_type = ...):
        """
        Copies the hang activity metadata with the given fields.
        
        Parameters
        ----------
        created_at : `None | DateTime`, Optional (Keyword only)
            When the status was created.
        
        details : `None`, `str`, Optional (Keyword only)
            The activity's next to its emoji.
        
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The emoji of the activity.
        
        hang_type : ``HangType``, Optional (Keyword only)
            How the user is hanging.
        
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
        
        # details
        if details is ...:
            details = self.details
        else:
            details = validate_details(details)
        
        # emoji
        if emoji is ...:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # hang_type
        if hang_type is ...:
            hang_type = self.hang_type
        else:
            hang_type = validate_hang_type(hang_type)
        
        # Construct
        new = object.__new__(type(self))
        new.created_at = created_at
        new.emoji = emoji
        new.details = details
        new.hang_type = hang_type
        return new
    
    
    @copy_docs(ActivityMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        _pop_empty_name(keyword_parameters)
        return self.copy_with(
            created_at = keyword_parameters.pop('created_at', ...),
            details = keyword_parameters.pop('details', ...),
            emoji = keyword_parameters.pop('emoji', ...),
            hang_type = keyword_parameters.pop('hang_type', ...),
        )
    
    
    @property
    def name(self):
        """
        Returns the activity's display text.
        
        Returns
        -------
        name : `str`
        """
        return self.hang_type.name_getter(self)
