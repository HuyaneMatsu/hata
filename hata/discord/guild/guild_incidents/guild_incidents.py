__all__ = ('GuildIncidents', )

from scarletio import RichAttributeErrorBaseType

from ...utils import DATETIME_FORMAT_CODE

from .fields import (
    parse_direct_message_spam_detected_at, parse_direct_messages_disabled_until, parse_invites_disabled_until,
    parse_raid_detected_at, put_direct_message_spam_detected_at_into, put_direct_messages_disabled_until_into,
    put_invites_disabled_until_into, put_raid_detected_at_into, validate_direct_message_spam_detected_at,
    validate_direct_messages_disabled_until, validate_invites_disabled_until, validate_raid_detected_at
)


class GuildIncidents(RichAttributeErrorBaseType):
    """
    A guild's incidents.
    
    Attributes
    ----------
    direct_message_spam_detected_at : `None`, `DateTime`
        When direct message spam was detected.
    direct_messages_disabled_until : `None`, `DateTime`
        Until when are the direct messages disabled in the guild.
    invites_disabled_until : `None`, `DateTime`
       Until when are the invites disabled of the guild.
    raid_detected_at : `None`, `DateTime`
        When raid was detected.
    """
    __slots__ = (
        'direct_message_spam_detected_at', 'direct_messages_disabled_until', 'invites_disabled_until',
        'raid_detected_at'
    )
    
    def __new__(
        cls,
        *,
        direct_message_spam_detected_at = ...,
        direct_messages_disabled_until = ...,
        invites_disabled_until = ...,
        raid_detected_at = ...,
    ):
        """
        Creates a new guild incidents with the given fields.
        
        Parameters
        ----------
        direct_message_spam_detected_at : `None`, `DateTime`, Optional (Keyword only)
            When direct message spam was detected.
        direct_messages_disabled_until : `None`, `DateTime`, Optional (Keyword only)
            Until when are the direct messages disabled in the guild.
        invites_disabled_until : `None`, `DateTime`, Optional (Keyword only)
           Until when are the invites disabled of the guild.
        raid_detected_at : `None`, `DateTime`, Optional (Keyword only)
            When raid was detected.
        
        Raises
        ------
        TypeError
            - Parameter with incorrect type given.
        ValueError
            - Parameter with incorrect value given.
        """
        # direct_message_spam_detected_at
        if direct_message_spam_detected_at is ...:
            direct_message_spam_detected_at = None
        else:
            direct_message_spam_detected_at = validate_direct_message_spam_detected_at(direct_message_spam_detected_at)
        
        # direct_messages_disabled_until
        if direct_messages_disabled_until is ...:
            direct_messages_disabled_until = None
        else:
            direct_messages_disabled_until = validate_direct_messages_disabled_until(direct_messages_disabled_until)
        
        # invites_disabled_until
        if invites_disabled_until is ...:
            invites_disabled_until = None
        else:
            invites_disabled_until = validate_invites_disabled_until(invites_disabled_until)
        
        # raid_detected_at
        if raid_detected_at is ...:
            raid_detected_at = None
        else:
            raid_detected_at = validate_raid_detected_at(raid_detected_at)
        
        # Construct
        self = object.__new__(cls)
        self.direct_message_spam_detected_at = direct_message_spam_detected_at
        self.direct_messages_disabled_until = direct_messages_disabled_until
        self.invites_disabled_until = invites_disabled_until
        self.raid_detected_at = raid_detected_at
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a guild incidents from the requested guild incidents data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received guild incidents data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.direct_message_spam_detected_at = parse_direct_message_spam_detected_at(data)
        self.direct_messages_disabled_until = parse_direct_messages_disabled_until(data)
        self.invites_disabled_until = parse_invites_disabled_until(data)
        self.raid_detected_at = parse_raid_detected_at(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the guild incidents to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should also be included as well. 
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_direct_messages_disabled_until_into(self.direct_messages_disabled_until, data, defaults)
        put_invites_disabled_until_into(self.invites_disabled_until, data, defaults)
        
        if include_internals:
            put_direct_message_spam_detected_at_into(self.direct_message_spam_detected_at, data, defaults)
            put_raid_detected_at_into(self.raid_detected_at, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the guild incidents' representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        field_added = False
        
        direct_message_spam_detected_at = self.direct_message_spam_detected_at
        if direct_message_spam_detected_at is not None:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' direct_message_spam_detected_at = ')
            repr_parts.append(format(direct_message_spam_detected_at, DATETIME_FORMAT_CODE))
        
        direct_messages_disabled_until = self.direct_messages_disabled_until
        if direct_messages_disabled_until is not None:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' direct_messages_disabled_until = ')
            repr_parts.append(format(direct_messages_disabled_until, DATETIME_FORMAT_CODE))
        
        invites_disabled_until = self.invites_disabled_until
        if invites_disabled_until is not None:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' invites_disabled_until = ')
            repr_parts.append(format(invites_disabled_until, DATETIME_FORMAT_CODE))
        
        raid_detected_at = self.raid_detected_at
        if raid_detected_at is not None:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' raid_detected_at = ')
            repr_parts.append(format(raid_detected_at, DATETIME_FORMAT_CODE))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two guild incidents are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.direct_message_spam_detected_at != other.direct_message_spam_detected_at:
            return False
        
        if self.direct_messages_disabled_until != other.direct_messages_disabled_until:
            return False
        
        if self.invites_disabled_until != other.invites_disabled_until:
            return False
        
        if self.raid_detected_at != other.raid_detected_at:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the guild incidents."""
        hash_value = 0
        
        # direct_message_spam_detected_at
        direct_message_spam_detected_at = self.direct_message_spam_detected_at
        if direct_message_spam_detected_at is not None:
            hash_value ^= hash(direct_message_spam_detected_at) & (0xffff << 0)
    
        # direct_messages_disabled_until
        direct_messages_disabled_until = self.direct_messages_disabled_until
        if direct_messages_disabled_until is not None:
            hash_value ^= hash(direct_messages_disabled_until) & (0xffff << 4)
        
        # invites_disabled_until
        invites_disabled_until = self.invites_disabled_until
        if invites_disabled_until is not None:
            hash_value ^= hash(invites_disabled_until) & (0xffff << 8)
        
        # raid_detected_at
        raid_detected_at = self.raid_detected_at
        if raid_detected_at is not None:
            hash_value ^= hash(raid_detected_at) & (0xffff << 12)
        
        return hash_value
    
    
    def __bool__(self):
        """Returns whether the guild has any features."""
        if self.direct_message_spam_detected_at is not None:
            return True
        
        if self.direct_messages_disabled_until is not None:
            return True
        
        if self.invites_disabled_until is not None:
            return True
        
        if self.raid_detected_at is not None:
            return True
        
        return False
    
    
    def copy(self):
        """
        Copies the guild incidents.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.direct_message_spam_detected_at = self.direct_message_spam_detected_at
        new.direct_messages_disabled_until = self.direct_messages_disabled_until
        new.invites_disabled_until = self.invites_disabled_until
        new.raid_detected_at = self.raid_detected_at
        return new
    
    
    def copy_with(
        self,
        *,
        direct_message_spam_detected_at = ...,
        direct_messages_disabled_until = ...,
        invites_disabled_until = ...,
        raid_detected_at = ...,
    ):
        """
        Copies the guild incidents with the given fields.
        
        Parameters
        ----------
        direct_message_spam_detected_at : `None`, `DateTime`, Optional (Keyword only)
            When direct message spam was detected.
        direct_messages_disabled_until : `None`, `DateTime`, Optional (Keyword only)
            Until when are the direct messages disabled in the guild.
        invites_disabled_until : `None`, `DateTime`, Optional (Keyword only)
           Until when are the invites disabled of the guild.
        raid_detected_at : `None`, `DateTime`, Optional (Keyword only)
            When raid was detected.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - Parameter with incorrect type given.
        ValueError
            - Parameter with incorrect value given.
        """
        # direct_message_spam_detected_at
        if direct_message_spam_detected_at is ...:
            direct_message_spam_detected_at = self.direct_message_spam_detected_at
        else:
            direct_message_spam_detected_at = validate_direct_message_spam_detected_at(direct_message_spam_detected_at)
        
        # direct_messages_disabled_until
        if direct_messages_disabled_until is ...:
            direct_messages_disabled_until = self.direct_messages_disabled_until
        else:
            direct_messages_disabled_until = validate_direct_messages_disabled_until(direct_messages_disabled_until)
        
        # invites_disabled_until
        if invites_disabled_until is ...:
            invites_disabled_until = self.invites_disabled_until
        else:
            invites_disabled_until = validate_invites_disabled_until(invites_disabled_until)
        
        # raid_detected_at
        if raid_detected_at is ...:
            raid_detected_at = self.raid_detected_at
        else:
            raid_detected_at = validate_invites_disabled_until(raid_detected_at)
        
        # Construct
        new = object.__new__(type(self))
        new.direct_message_spam_detected_at = direct_message_spam_detected_at
        new.direct_messages_disabled_until = direct_messages_disabled_until
        new.invites_disabled_until = invites_disabled_until
        new.raid_detected_at = raid_detected_at
        return new
