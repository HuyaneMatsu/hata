__all__ = ('OnboardingPromptOption',)

from ...bases import DiscordEntity
from ...channel import ChannelType, create_partial_channel_from_id
from ...precreate_helpers import process_precreate_parameters_and_raise_extra
from ...role import create_partial_role_from_id

from .fields import (
    parse_channel_ids, parse_description, parse_emoji, parse_id, parse_name, parse_role_ids, put_channel_ids_into,
    put_description_into, put_emoji_into, put_id_into, put_name_into, put_role_ids_into, validate_channel_ids,
    validate_description, validate_emoji, validate_id, validate_name, validate_role_ids
)


PRECREATE_FIELDS = {
    'channel_ids': ('channel_ids', validate_channel_ids),
    'channels': ('channel_ids', validate_channel_ids),
    'description': ('description', validate_description),
    'emoji': ('emoji', validate_emoji),
    'name': ('name', validate_name),
    'role_ids': ('role_ids', validate_role_ids),
    'roles': ('role_ids', validate_role_ids),
}


class OnboardingPromptOption(DiscordEntity):
    """
    Option of an onboarding prompt.
    
    Attributes
    ----------
    channel_ids : `None`, `tuple` of `int`
        The channels' identifier opted into when this option is selected.
    description : `None`, `str`
        The option's description
    emoji : `None`, ``Emoji``
        The emoji of the option.
    id : `int`
        the option's identifier.
    name : `str`
        The option's name.
    role_ids : `None`, `tuple` of `int`
        The roles' identifiers assigned to the user when this option is selected.
    """
    __slots__ = ('channel_ids', 'description', 'emoji', 'name', 'role_ids')
    
    def __new__(cls, *, channel_ids = ..., description = ..., emoji = ..., name = ..., role_ids = ...):
        """
        Creates an onboarding prompt option instance from the given parameters.
        
        Parameters
        ----------
        channel_ids : `None`, `iterable` of (`int` ``Channel``), Optional (Keyword only)
            The channels' identifier opted into when this option is selected.
        description : `None`, `str`, Optional (Keyword only)
            The option's description
        emoji : `None`, `str`, Optional (Keyword only)
            The emoji of the option.
        name : `str`, Optional (Keyword only)
            The option's name.
        role_ids : `None`, `iterable` of (`int` ``Role``), Optional (Keyword only)
            The roles' identifiers assigned to the user when this option is selected.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # channel_ids
        if channel_ids is ...:
            channel_ids = None
        else:
            channel_ids = validate_channel_ids(channel_ids)
        
        # description
        if description is ...:
            description = None
        else:
            description = validate_description(description)
        
        # emoji
        if emoji is ...:
            emoji = None
        else:
            emoji = validate_emoji(emoji)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # role_ids
        if role_ids is ...:
            role_ids = None
        else:
            role_ids = validate_role_ids(role_ids)
        
        self = object.__new__(cls)
        self.channel_ids = channel_ids
        self.description = description
        self.emoji = emoji
        self.id = 0
        self.name = name
        self.role_ids = role_ids
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new onboarding prompt option from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Onboarding prompt option data.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.channel_ids = parse_channel_ids(data)
        self.description = parse_description(data)
        self.emoji = parse_emoji(data)
        self.id = parse_id(data)
        self.name = parse_name(data)
        self.role_ids = parse_role_ids(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the onboarding prompt option to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        put_channel_ids_into(self.channel_ids, data, defaults)
        put_description_into(self.description, data, defaults)
        put_emoji_into(self.emoji, data, defaults)
        put_name_into(self.name, data, defaults)
        put_role_ids_into(self.role_ids, data, defaults)
        
        if include_internals:
            put_id_into(self.id, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the onboarding prompt option's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        option_id = self.id
        if option_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(option_id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        description = self.description
        if (description is not None):
            repr_parts.append(', description = ')
            repr_parts.append(repr(description))
        
        emoji = self.emoji
        if (emoji is not None):
            repr_parts.append(', emoji = ')
            repr_parts.append(repr(emoji))
        
        channel_ids = self.channel_ids
        if (channel_ids is not None):
            repr_parts.append(', channel_ids = [')
            
            index = 0
            length = len(channel_ids)
            
            while True:
                channel_id = channel_ids[index]
                index += 1
                
                repr_parts.append(repr(channel_id))
                
                if index == length:
                    break
                
                repr_parts.append(', ')
            
            repr_parts.append(']')
        
        role_ids = self.role_ids
        if (role_ids is not None):
            repr_parts.append(', role_ids = [')
            
            index = 0
            length = len(role_ids)
            
            while True:
                role_id = role_ids[index]
                index += 1
                
                repr_parts.append(repr(role_id))
                
                if index == length:
                    break
                
                repr_parts.append(', ')
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two onboarding prompt options are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two onboarding prompt options are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two onboarding prompt options are equal.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        are_equal : `bool`
        """
        if self.channel_ids != other.channel_ids:
            return False
        
        if self.description != other.description:
            return False
        
        if self.emoji != other.emoji:
            return False
        
        # id
        # Ignore it
        
        if self.name != other.name:
            return False
        
        if self.role_ids != other.role_ids:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the onboarding prompt option's hash value."""
        hash_value = 0
        
        channel_ids = self.channel_ids
        if (channel_ids is not None):
            hash_value ^= len(channel_ids)
            
            for channel_id in channel_ids:
                hash_value ^= channel_id
        
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= hash(emoji)
        
        # id
        # ignore it
        
        name = self.name
        if (name is not None):
            if name != description:
                hash_value ^= hash(name)
        
        role_ids = self.role_ids
        if (role_ids is not None):
            hash_value ^= len(role_ids) << 4
            
            for role_id in role_ids:
                hash_value ^= role_id
        
        return hash_value
    
    
    @classmethod
    def precreate(
        cls,
        option_id,
        **keyword_parameters,
    ):
        """
        Precreates an onboarding prompt option. Since they are not cached, this method just a ``.__new__`` alternative.
        
        Parameters
        ----------
        option_id : `int`
            The option's identifier.
        
        **keyword_parameters : Keyword parameters
            Additional parameters defining how the option's fields should be set.
        
        Other Parameters
        ----------------
        channel_ids : `None`, `iterable` of (`int` ``Channel``), Optional (Keyword only)
            The channels' identifier opted into when this option is selected.
        channel_ids : `None`, `iterable` of (`int` ``Channel``), Optional (Keyword only)
            Alternative of `channel_ids`.
        description : `None`, `str`, Optional (Keyword only)
            The option's description
        emoji : `None`, `str`, Optional (Keyword only)
            The emoji of the option.
        name : `str`, Optional (Keyword only)
            The option's name.
        role_ids : `None`, `iterable` of (`int` ``Role``), Optional (Keyword only)
            The roles' identifiers assigned to the user when this option is selected.
        roles : `None`, `iterable` of (`int` ``Role``), Optional (Keyword only)
            Alternative of `role_ids`.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        option_id = validate_id(option_id)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        # Construct
        
        self = object.__new__(cls)
        self.channel_ids = None
        self.description = None
        self.emoji = None
        self.id = option_id
        self.name = ''
        self.role_ids = None
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    def copy(self):
        """
        Copies the onboarding prompt option.
        
        Returns
        -------
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        channel_ids = self.channel_ids
        if (channel_ids is not None):
            channel_ids = (*channel_ids,)
        new.channel_ids = channel_ids
        
        new.description = self.description
        new.emoji = self.emoji
        new.id = 0
        new.name = self.name
        
        role_ids = self.role_ids
        if (role_ids is not None):
            role_ids = (*role_ids,)
        new.role_ids = role_ids
        
        return new
    
    
    def copy_with(self, *, channel_ids = ..., description = ..., emoji = ..., name = ..., role_ids = ...):
        """
        Copies the onboarding prompt option with the given fields.
        
        Parameters
        ----------
        channel_ids : `None`, `iterable` of (`int` ``Channel``), Optional (Keyword only)
            The channels' identifier opted into when this option is selected.
        description : `None`, `str`, Optional (Keyword only)
            The option's description
        emoji : `None`, `str`, Optional (Keyword only)
            The emoji of the option.
        name : `str`, Optional (Keyword only)
            The option's name.
        role_ids : `None`, `iterable` of (`int` ``Role``), Optional (Keyword only)
            The roles' identifiers assigned to the user when this option is selected.
        
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
        # channel_ids
        if channel_ids is ...:
            channel_ids = self.channel_ids
            if (channel_ids is not None):
                channel_ids = (*channel_ids,)
        else:
            channel_ids = validate_channel_ids(channel_ids)
        
        # description
        if description is ...:
            description = self.description
        else:
            description = validate_description(description)
        
        # emoji
        if emoji is ...:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # role_ids
        if role_ids is ...:
            role_ids = self.role_ids
            if (role_ids is not None):
                role_ids = (*role_ids,)
        else:
            role_ids = validate_role_ids(role_ids)
        
        new = object.__new__(type(self))
        new.channel_ids = channel_ids
        new.description = description
        new.emoji = emoji
        new.id = 0
        new.name = name
        new.role_ids = role_ids
        return new
    
    
    @property
    def roles(self):
        """
        Returns the roles that are assigned to the user when this option is selected.
        
        Returns
        -------
        roles : `None`, `tuple` of ``Role``
        """
        role_ids = self.role_ids
        if role_ids is None:
            roles = None
        else:
            roles = (*sorted(
                (create_partial_role_from_id(role_id) for role_id in role_ids),
            ),)
        
        return roles
    
    
    def iter_role_ids(self):
        """
        Iterates over the roles' identifiers assigned to the user when this option is selected.
        
        This method is an iterable generator.
        
        Yields
        ------
        role_id : `int`
        """
        role_ids = self.role_ids
        if (role_ids is not None):
            yield from role_ids
    
    
    def iter_roles(self):
        """
        Iterates over the roles that are assigned to the user when this option is selected.
        Not like ``.roles``, this will not sort the roles of the emoji based on their position, instead uses the
        default ordering (id).
        
        This method is an iterable generator.
        
        Yields
        ------
        role : ``Role``
        """
        for role_id in self.iter_role_ids():
            yield create_partial_role_from_id(role_id)
    
    
    @property
    def channels(self):
        """
        Returns the channels that opted into when this option is selected.
        
        Returns
        -------
        channels : `None`, `tuple` of ``Channel``
        """
        channel_ids = self.channel_ids
        if channel_ids is None:
            channels = None
        else:
            channels = (*(
                create_partial_channel_from_id(channel_id, ChannelType.unknown, 0) for channel_id in channel_ids
            ),)
        
        return channels
    
    
    def iter_channel_ids(self):
        """
        Iterates over the channels' identifiers that opted into when this option is selected.
        
        This method is an iterable generator.
        
        Yields
        ------
        channel_id : `int`
        """
        channel_ids = self.channel_ids
        if (channel_ids is not None):
            yield from channel_ids
    
    
    def iter_channels(self):
        """
        Iterates over the channels that opted into when this option is selected.
        
        This method is an iterable generator.
        
        Yields
        ------
        channel : ``Channel``
        """
        for channel_id in self.iter_channel_ids():
            yield create_partial_channel_from_id(channel_id, ChannelType.unknown, 0)
