__all__ = ('MessageInteraction',)

from scarletio import include

from ...bases import DiscordEntity
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...user import ZEROUSER

from .fields import (
    parse_id, parse_name_and_sub_command_name_stack, parse_type, parse_user, put_id_into,
    put_name_and_sub_command_name_stack_into, put_type_into, put_user_into, validate_id, validate_name,
    validate_sub_command_name_stack, validate_type, validate_user
)


InteractionType = include('InteractionType')


PRECREATE_FIELDS = {
    'name': ('name', validate_name),
    'sub_command_name_stack': ('sub_command_name_stack', validate_sub_command_name_stack),
    'interaction_type': ('type', validate_type),
    'user': ('user', validate_user),
}

    
class MessageInteraction(DiscordEntity):
    """
    Sent with a ``Message`` when the it is a response to an ``InteractionEvent``.
    
    Attributes
    ----------
    id : `int`
        The interaction's identifier.
    name : `str`
        The invoked interaction's name.
    sub_command_name_stack : `None`, `tuple` of `str`
        The sub-command-group and sub-command names.
    type : ``InteractionType``
        The interaction's type.
    user : ``ClientUserBase``
        Who invoked the interaction.
    """
    __slots__ = ('name', 'sub_command_name_stack', 'type', 'user')
    
    def __new__(cls, *, interaction_type = ..., name = ..., sub_command_name_stack = ..., user = ...):
        """
        Creates a new message interaction with the given fields.
        
        Parameters
        ----------
        name : `str`, Optional (Keyword only)
            The invoked interaction's name.
        
        sub_command_name_stack : `None`, `iterable` of `str`, Optional (Keyword only)
            The sub-command-group and sub-command names.
        
        interaction_type : ``InteractionType``, `int`, Optional (Keyword only)
            The interaction's type.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            Who invoked the interaction.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # interaction_type
        if interaction_type is ...:
            interaction_type = InteractionType.none
        else:
            interaction_type = validate_type(interaction_type)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # sub_command_name_stack
        if sub_command_name_stack is ...:
            sub_command_name_stack = None
        else:
            sub_command_name_stack = validate_sub_command_name_stack(sub_command_name_stack)
        
        # user
        if user is ...:
            user = ZEROUSER
        else:
            user = validate_user(user)
        
        # Construct
        self = object.__new__(cls)
        self.id = 0
        self.name = name
        self.sub_command_name_stack = sub_command_name_stack
        self.type = interaction_type
        self.user = user
        return self
    
    
    @classmethod
    def precreate(cls, message_interaction_id, **keyword_parameters):
        """
        Creates a new message interaction with the given predefined fields.
        
        > Since message interactions are not globally cached, this method is only used for testing.
        
        Parameters
        ----------
        message_interaction_id : `int`
            The message interaction's id.
        
        **keyword_parameters : Keyword parameters
            The attributes to set.
        
        Other Parameters
        ----------------
        name : `str`, Optional (Keyword only)
            The invoked interaction's name.
        
        sub_command_name_stack : `None`, `iterable` of `str`, Optional (Keyword only)
            The sub-command-group and sub-command names.
        
        interaction_type : ``InteractionType``, `int`, Optional (Keyword only)
            The interaction's type.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            Who invoked the interaction.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters.
        ValueError
            - If a parameter's value is incorrect.
        """
        message_interaction_id = validate_id(message_interaction_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        self = cls._create_empty(message_interaction_id)
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    @classmethod
    def _create_empty(cls, message_interaction_id):
        """
        Creates a new message interaction with it's defaults attributes set.
        
        Parameters
        ----------
        message_interaction_id : `int`
            The message interaction's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = message_interaction_id
        self.name = ''
        self.sub_command_name_stack = None
        self.type = InteractionType.none
        self.user = ZEROUSER
        return self
    
    
    @classmethod
    def from_data(cls, data, guild_id = 0):
        """
        Creates a new message interaction from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Message interaction data.
        guild_id : `int` = `0`, Optional (Keyword only)
            The respective message's guild's identifier.
        
        Returns
        -------
        data : `instance<cls>`
        """
        self = object.__new__(cls)
        
        self.id = parse_id(data)
        self.name, self.sub_command_name_stack = parse_name_and_sub_command_name_stack(data)
        self.type = parse_type(data)
        self.user = parse_user(data, guild_id)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False, guild_id = 0):
        """
        Tries to convert the message interaction back to json serializable dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        guild_id : `int` = `0`, Optional (Keyword only)
            The respective message's guild's identifier.
        
        Returns
        -------
        data : `dict` of (`str`, `object`)
        """
        data = {}
        put_name_and_sub_command_name_stack_into((self.name, self.sub_command_name_stack), data, defaults)
        put_type_into(self.type, data, defaults)
        
        if include_internals:
            put_id_into(self.id, data, defaults)
            put_user_into(self.user, data, defaults, guild_id = guild_id)
        
        return data
    
    
    @property
    def partial(self):
        """
        Returns whether the message interaction is partial.
        
        Returns
        -------
        partial : `bool`
        """
        return (self.id == 0)
    
    
    def __repr__(self):
        """Returns the message interaction's representation."""
        repr_parts = ['<', self.__class__.__name__, ' id = ', repr(self.id), ', type = ']
        
        interaction_type = self.type
        repr_parts.append(interaction_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(interaction_type.value))
        
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        sub_command_name_stack = self.sub_command_name_stack
        if (sub_command_name_stack is not None):
            repr_parts.append(', sub_command_name_stack = ')
            repr_parts.append(repr(sub_command_name_stack))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two message interactions are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two message interactions not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # id
        self_id = self.id
        other_id = other.id
        if self_id and other_id and self_id != other_id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # sub_command_name_stack
        if self.sub_command_name_stack != other.sub_command_name_stack:
            return False
        
        # type
        if self.type is not other.type:
            return False
        
        # user
        if self.user != other.user:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the message integration's hash value."""
        hash_value = 0
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        # sub_command_name_stack
        sub_command_name_stack = self.sub_command_name_stack
        if (sub_command_name_stack is not None):
            hash_value ^= len(sub_command_name_stack)
            for sub_command_name in sub_command_name_stack:
                hash_value ^= hash(sub_command_name)
        
        # type
        hash_value ^= self.type.value << 4
        
        # user
        hash_value ^= hash(self.user)
        
        return hash_value
    
    
    
    def copy(self):
        """
        Copies the message application returning a new partial one.
        
        Returns
        -------
        new : `instance<cls>`
        """
        new = object.__new__(type(self))
        
        new.id = 0
        new.name = self.name
        
        sub_command_name_stack = self.sub_command_name_stack
        if (sub_command_name_stack is not None):
            sub_command_name_stack = (*sub_command_name_stack,)
        new.sub_command_name_stack = sub_command_name_stack
        
        new.type = self.type
        new.user = self.user
        
        return new
    
    
    def copy_with(self, *, interaction_type = ..., name = ..., sub_command_name_stack = ..., user = ...):
        """
        Copies the message interaction with the given fields returning a new partial one.
        
        Parameters
        ----------
        name : `str`, Optional (Keyword only)
            The invoked interaction's name.
        
        sub_command_name_stack : `None`, `iterable` of `str`, Optional (Keyword only)
            The sub-command-group and sub-command names.
        
        interaction_type : ``InteractionType``, `int`, Optional (Keyword only)
            The interaction's type.
        
        user : ``ClientUserBase``, Optional (Keyword only)
            Who invoked the interaction.
        
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
        # interaction_type
        if interaction_type is ...:
            interaction_type = self.type
        else:
            interaction_type = validate_type(interaction_type)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # sub_command_name_stack
        if sub_command_name_stack is ...:
            sub_command_name_stack = self.sub_command_name_stack
            if (sub_command_name_stack is not None):
                sub_command_name_stack = (*sub_command_name_stack,)
        else:
            sub_command_name_stack = validate_sub_command_name_stack(sub_command_name_stack)
        
        # user
        if user is ...:
            user = self.user
        else:
            user = validate_user(user)
    
        # Construct
        self = object.__new__(type(self))
        self.id = 0
        self.name = name
        self.sub_command_name_stack = sub_command_name_stack
        self.type = interaction_type
        self.user = user
        return self
    
    
    @property
    def joined_name(self):
        """
        Returns the joined name of the message interaction.
        
        Returns
        -------
        joined_name : `str`
        """
        name = self.name
        sub_command_name_stack = self.sub_command_name_stack
        if (sub_command_name_stack is None):
            return name
        
        return ' '.join([name, *sub_command_name_stack])
    
    
