__all__ = ('GuildBoost',)


from ...bases import DiscordEntity
from ...core import GUILDS, GUILD_BOOSTS
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import create_partial_user_from_id

from .fields import (
    parse_guild_id, parse_user_id, put_guild_id, put_user_id, validate_guild_id, validate_user_id,
    parse_id, put_id, validate_id,
    parse_ended, put_ended, validate_ended,
    parse_ends_at, put_ends_at, validate_ends_at,
    parse_paused_until, validate_paused_until, put_paused_until
)

PRECREATE_FIELDS = {
    'ended': ('ended', validate_ended),
    'ends_at': ('ends_at', validate_ends_at),
    'guild': ('guild_id', validate_guild_id),
    'guild_id': ('guild_id', validate_guild_id),
    'paused_until': ('paused_until', validate_paused_until),
    'user': ('user_id', validate_user_id),
    'user_id': ('user_id', validate_user_id),
}



class GuildBoost(DiscordEntity, immortal = True):
    """
    Represents a guild's boost.
    
    Attributes
    ----------
    ended : `bool`
        Whether the boost already ended.
    
    ends_at : `None | DateTime`
        When the boost ends.
    
    guild_id : `int`
        The guild's identifier the boost is for.
    
    id : `int`
        The guild boost' identifier.
    
    paused_until : `None | Datetime`
        Until when the boost is paused.
    
    user_id : `int`
        The user who owns the boost.
    """
    __slots__ = ('ended', 'ends_at', 'guild_id', 'paused_until', 'user_id', )
    
    def __new__(cls, *, paused_until = ...):
        """
        Creates a new guild boost.
        
        Parameters
        ----------
        paused_until : `None | DateTime`, Optional (Keyword only)
            Until when the boost is paused.
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # paused_until
        if paused_until is ...:
            paused_until = None
        else:
            paused_until = validate_paused_until(paused_until)
        
        # Construct
        self = object.__new__(cls)
        self.ended = False
        self.ends_at = None
        self.guild_id = 0
        self.id = 0
        self.paused_until = paused_until
        self.user_id = 0
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new guild boost from the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Guild boost data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        guild_boost_id = parse_id(data)
        
        try:
            self = GUILD_BOOSTS[guild_boost_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = guild_boost_id
            GUILD_BOOSTS[guild_boost_id] = self
        
        self._set_attributes(data)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Serializes the guild boost.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields of their default value should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_paused_until(self.paused_until, data, defaults)
        
        if include_internals:
            put_ended(self.ended, data, defaults)
            put_ends_at(self.ends_at, data, defaults)
            put_guild_id(self.guild_id, data, defaults)
            put_id(self.id, data, defaults)
            put_user_id(self.user_id, data, defaults)
        
        return data
    
    
    def _set_attributes(self, data):
        """
        Sets the attributes of the guild boost from the given data (except id).
        
        Parameters
        ----------
        data : `dict<str, object>`
            Guild boost data.
        """
        self.guild_id = parse_guild_id(data)
        self.user_id = parse_user_id(data)
        
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the modifiable attributes.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Guild boost data.
        """
        self.ended = parse_ended(data)
        self.ends_at = parse_ends_at(data)
        self.paused_until = parse_paused_until(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the modifiable attributes returns the changed attributes in a dictionary with the changed attributes
        in a `attribute-name`, `old-value` relation.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Guild boost data.
        
        Returns
        -------
        old_attributes : `dict<str, object>`
            All item in the returned dict is optional.
            
            Might contain the following items:
            
            +-----------+-------------------+
            | Keys      | Values            |
            +===========+===================+
            | ended     | `bool`            |
            +-----------+-------------------+
            | ends_at   | `None | DateTime` |
            +-----------+-------------------+
        """
        old_attributes = {}
        
        # ended
        ended = parse_ended(data)
        if self.ended != ended:
            old_attributes['ended'] = self.ended
            self.ended = ended
        
        # ends_at
        ends_at = parse_ends_at(data)
        if self.ends_at != ends_at:
            old_attributes['ends_at'] = self.ends_at
            self.ends_at = ends_at
        
        # paused_until
        paused_until = parse_paused_until(data)
        if self.paused_until != paused_until:
            old_attributes['paused_until'] = self.paused_until
            self.paused_until = paused_until
        
        return old_attributes
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # guild_id
        repr_parts.append(' guild_id = ')
        repr_parts.append(repr(self.guild_id))
        
        # user_id
        repr_parts.append(', user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns hash(self)"""
        guild_boost_id = self.id
        if guild_boost_id:
            return guild_boost_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Calculates the guild boosts's hash based on their fields.
        
        This method is called by ``.__hash__`` if the guild boost has no ``.id`` set.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # ended -> skip, internal
        # ends_at -> skip, internal
        # guild_id -> skip, internal
        
        # paused_until
        paused_until = self.paused_until
        if (paused_until is not None):
            hash_value ^= hash(paused_until)
        
        # user_id -> skip, internal
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns self == other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns self != other."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether self is equal to other. Other must be same type as self.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        is_equal : `bool`
        """
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return (self_id == other_id)
        
        # ended -> skip, internal
        # ends_at -> skip, internal
        # guild_id -> skip, internal
        
        # paused_until
        if self.paused_until != other.paused_until:
            return False
        
        # user_id -> skip, internal
        
        return True
    
    
    @classmethod
    def _create_empty(cls, entity_id):
        """
        Creates a new instance with it's attribute set to their default values.
        
        Parameters
        ----------
        entity_id : `int`
            The entity's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.ended = False
        self.ends_at = None
        self.guild_id = 0
        self.id = entity_id
        self.paused_until = None
        self.user_id = 0
        return self
    

    @classmethod
    def precreate(cls, guild_boost_id, **keyword_parameters):
        """
        Creates a new guild boost instance. When the guild boost is loaded with the same id, it will be picked up.
        
        Parameters
        ----------
        guild_boost_id : `int`
            The guild boost's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters.
        
        Other Parameters
        ----------------
        ended : `None | bool`, Optional (Keyword only)
            Whether the boost already ended.
        
        ends_at : `None | DateTime`, Optional (Keyword only)
            When the boost ends at.
        
        guild : ``None | int | Guild``, Optional (Keyword only)
            Alternative for `guild_id`.
        
        guild_id : ``None | int | Guild``, Optional (Keyword only)
            The guild's identifier the boost is for.
        
        paused_until : `None | DateTime`, Optional (Keyword only)
            Until when the boost is paused.
        
        user : ``None | int | ClientUserBase``, Optional (Keyword only)
            Alternative for `user_id`.
        
        user_id : ``None | int | ClientUserBase``, Optional (Keyword only)
            The user who owns the boost.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        guild_boost_id = validate_id(guild_boost_id)

        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        try:
            self = GUILD_BOOSTS[guild_boost_id]
        except KeyError:
            self = cls._create_empty(guild_boost_id)
            GUILD_BOOSTS[guild_boost_id] = self
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    def copy(self):
        """
        Copies the guild boost.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.ended = False
        new.ends_at = None
        new.guild_id = 0
        new.id = 0
        new.paused_until = self.paused_until
        new.user_id = 0
        return new
    
    
    def copy_with(self, *, paused_until = ...):
        """
        Copies the guild boost with the given fields.
        
        Parameters
        ----------
        paused_until : `None | DateTime`, Optional (Keyword only)
            Until when the boost is paused.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        # paused_until
        if paused_until is ...:
            paused_until = self.paused_until
        else:
            paused_until = validate_paused_until(paused_until)
        
        # Construct
        new = object.__new__(type(self))
        new.ended = False
        new.ends_at = None
        new.guild_id = 0
        new.id = 0
        new.paused_until = paused_until
        new.user_id = 0
        return new
    
    
    @property
    def guild(self):
        """
        Returns the guild boost's guild.
        
        Returns
        -------
        guild : ``None | Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def user(self):
        """
        Returns the guild boost's user.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        return create_partial_user_from_id(self.user_id)
    
    
    @property
    def partial(self):
        """
        Returns whether the guild boost is partial.
        
        Returns
        -------
        partial : `bool`
        """
        return False if self.id else True
