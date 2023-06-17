__all__ = ('ReactionAddEvent',)

from scarletio import Task, copy_docs

from ...bases import EventBase
from ...core import KOKORO
from ...permission.permission import PERMISSION_MASK_MANAGE_MESSAGES

from .fields import (
    parse_emoji, parse_message, parse_user, put_emoji_into, put_message_into, put_user_into, validate_emoji,
    validate_message, validate_user
)
from .helpers import _delete_reaction_with_task


class ReactionAddEvent(EventBase):
    """
    Represents a processed `MESSAGE_REACTION_ADD` dispatch event.
    
    Attributes
    ----------
    emoji : ``Emoji``
        The emoji used as reaction.
    message : ``Message``
        The message on what the reaction is added.
    user : ``ClientUserBase``
        The user who added the reaction.
    
    Class Attributes
    ----------------
    DELETE_REACTION_OK : `int` = `0`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove.
    DELETE_REACTION_PERM : `int` = `1`
        Returned by ``.delete_reaction_with`` when the client has no permission to execute the reaction remove.
    DELETE_REACTION_NOT_ADDED : `int` = `2`
        Returned by ``.delete_reaction_with`` when the client has permission to execute the reaction remove, but
        it cannot, because the reaction is not added on the respective message. Not applicable for
        ``ReactionAddEvent``.
    """
    DELETE_REACTION_OK = 0
    DELETE_REACTION_PERM = 1
    DELETE_REACTION_NOT_ADDED = 2
    
    __slots__ = ('emoji', 'message', 'user')
    
    def __new__(cls, message, emoji, user):
        """
        Creates a new reaction add (or delete) instance.
        
        Parameters
        ----------
        message : ``Message``
            The respective message.
        emoji : ``Emoji``
            The emoji used.
        user : ``ClientUserBase``
            The user who reacted.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        emoji = validate_emoji(emoji)
        message = validate_message(message)
        user = validate_user(user)
        
        self = object.__new__(cls)
        self.message = message
        self.emoji = emoji
        self.user = user
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new reaction add (or delete) event instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Reaction event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.emoji = parse_emoji(data)
        self.message = message = parse_message(data)
        self.user = parse_user(data, message.guild_id)
        return self
    
    
    @classmethod
    def from_fields(cls, message, emoji, user):
        """
        Creates a new reaction add (or delete) instance.
        
        Parameters
        ----------
        message : ``Message``
            The respective message.
        emoji : ``Emoji``
            The emoji used.
        user : ``ClientUserBase``
            The user who reacted.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.message = message
        self.emoji = emoji
        self.user = user
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the reaction add (or delete) event into a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default field values should be included.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_emoji_into(self.emoji, data, defaults)
        message = self.message
        put_message_into(message, data, defaults)
        put_user_into(self.user, data, defaults, guild_id = message.guild_id)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' message = ')
        repr_parts.append(repr(self.message))
        
        repr_parts.append(', emoji = ')
        repr_parts.append(repr(self.emoji))
        
        repr_parts.append(', user = ')
        repr_parts.append(repr(self.user))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 3
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.message
        yield self.emoji
        yield self.user
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # message type can be different, so check id instead of identity
        if self.message.id != other.message.id:
            return False
        
        if self.emoji is not other.emoji:
            return False
        
        if self.user is not other.user:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # emoji
        hash_value = hash(self.emoji)
        
        # message
        hash_value ^= hash(self.message)
        
        # user
        hash_value ^= self.user.id
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the reaction add (or remove) event.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.emoji = self.emoji
        new.message = self.message
        new.user = self.user
        return new
    
    
    def copy_with(self, *, emoji = ..., message = ..., user = ...):
        """
        Copies the reaction add (or remove) event with the given fields.
        
        Parameters
        ----------
        message : ``Message``, Optional (Keyword only)
            The respective message.
        emoji : ``Emoji``, Optional (Keyword only)
            The emoji used.
        user : ``ClientUserBase``, Optional (Keyword only)
            The user who reacted.
        
        Returns
        -------
        new : `instance<type<self>>`
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # emoji
        if emoji is ...:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # message
        if message is ...:
            message = self.message
        else:
            message = validate_message(message)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        new = object.__new__(type(self))
        new.emoji = emoji
        new.message = message
        new.user = user
        return new
    
    
    def delete_reaction_with(self, client):
        """
        Removes the added reaction.
        
        Parameters
        ----------
        client : ``Client``
            The client, who will execute the action.
        
        Returns
        -------
        result : `int`
            The identifier number of the action what will be executed.
            
            Can be one of the following:
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | DELETE_REACTION_OK    | 0     |
            +-----------------------+-------+
            | DELETE_REACTION_PERM  | 1     |
            +-----------------------+-------+
        """
        if self.message.channel.cached_permissions_for(client) & PERMISSION_MASK_MANAGE_MESSAGES:
            Task(KOKORO, _delete_reaction_with_task(self, client))
            result = self.DELETE_REACTION_OK
        else:
            result = self.DELETE_REACTION_PERM
        
        return result
