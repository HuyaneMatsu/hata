__all__ = ('ReactionAddEvent',)

from scarletio import Task, copy_docs

from ...bases import EventBase
from ...core import KOKORO
from ...permission.permission import PERMISSION_MASK_MANAGE_MESSAGES

from ..reaction import Reaction, ReactionType

from .fields import (
    parse_emoji, parse_message, parse_type, parse_user, put_emoji_into, put_message_into, put_type_into, put_user_into,
    validate_emoji, validate_message, validate_type, validate_user
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
    type : ``ReactionType``
        The reaction's type.
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
    
    __slots__ = ('emoji', 'message', 'type', 'user')
    
    def __new__(cls, message, emoji, user, *, reaction_type = ...):
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
        reaction_type : ``ReactionType``, `int`, Optional (Keyword only)
            The reaction's type.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # emoji
        emoji = validate_emoji(emoji)
        
        # message
        message = validate_message(message)
        
        # reaction_type
        if reaction_type is ...:
            reaction_type = ReactionType.standard
        else:
            reaction_type = validate_type(reaction_type)
        
        # user
        user = validate_user(user)
        
        # Construct
        self = object.__new__(cls)
        self.message = message
        self.emoji = emoji
        self.type = reaction_type
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
        self.type = parse_type(data)
        self.user = parse_user(data, message.guild_id)
        return self
    
    
    @classmethod
    def from_fields(cls, message, emoji, user, reaction_type):
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
        reaction_type : ``ReactionType``
            The reaction's type.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.emoji = emoji
        self.message = message
        self.type = reaction_type
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
        put_type_into(self.type, data, defaults)
        put_user_into(self.user, data, defaults, guild_id = message.guild_id)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' message = ')
        repr_parts.append(repr(self.message))
        
        repr_parts.append(', emoji = ')
        repr_parts.append(repr(self.emoji))
        
        reaction_type = self.type
        if reaction_type is not ReactionType.standard:
            repr_parts.append(', type = ')
            repr_parts.append(reaction_type.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(reaction_type.value))
        
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
        yield self.reaction
        yield self.user
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.emoji is not other.emoji:
            return False
        
        if self.message is not other.message:
            return False
        
        if self.type is not other.type:
            return False
        
        if self.user is not other.user:
            return False
        
        return True
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # emoji
        hash_value ^= hash(self.emoji)
        
        # message
        hash_value ^= hash(self.message)
        
        # typer
        hash_value ^= hash(self.type)
        
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
        new.type = self.type
        new.user = self.user
        return new
    
    
    def copy_with(self, *, emoji = ..., reaction_type = ..., message = ..., user = ...):
        """
        Copies the reaction add (or remove) event with the given fields.
        
        Parameters
        ----------
        emoji : ``Emoji``, Optional (Keyword only)
            The emoji used.
        reaction_type : ``ReactionType``, Optional (Keyword only)
            The reaction's type.
        message : ``Message``, Optional (Keyword only)
            The respective message.
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
        
        # type
        if reaction_type is ...:
            reaction_type = self.type
        else:
            reaction_type = validate_type(reaction_type)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
        
        new = object.__new__(type(self))
        new.emoji = emoji
        new.message = message
        new.type = reaction_type
        new.user = user
        return new
    
    
    @property
    def reaction(self):
        """
        Returns the reaction of the reaction add event.
        
        Returns
        -------
        reaction : ``Reaction``
        """
        return Reaction.from_fields(self.emoji, self.type)
    
    
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
