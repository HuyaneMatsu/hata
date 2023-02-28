__all__ = (
    'ApplicationCommandParameterConfigurerWrapper', 'ApplicationCommandPermissionOverwriteWrapper', 'CommandWrapper'
)

import reprlib

from scarletio import RichAttributeErrorBaseType, copy_docs, include

from ...discord.application_command import ApplicationCommandPermissionOverwrite, ApplicationCommandOptionType
from ...discord.client import Client
from ...discord.guild import Guild
from ...discord.preconverters import preconvert_snowflake

from .converters import (
    ANNOTATION_TYPE_TO_OPTION_TYPE, ANNOTATION_TYPE_TO_STR_ANNOTATION, parse_annotation_description,
    parse_annotation_name,  parse_annotation_type_and_choice, postprocess_channel_types, preprocess_channel_types,
    process_max_and_min_value, process_max_length, process_min_length
)


Slasher = include('Slasher')


class CommandWrapper(RichAttributeErrorBaseType):
    """
    Wraps a command enabling the wrapper to postprocess the created command.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    """
    __slots__ = ('_wrapped',)
    
    def __new__(cls):
        """
        Creates a partial function to wrap a command.
        
        Subclasses should overwrite this method.
        """
        self = RichAttributeErrorBaseType.__new__(cls)
        
        self._wrapped = None
        
        return self
    
    
    def __call__(self, wrapped):
        """
        Wraps the given command.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        wrapped : `Any`
            The command or other wrapper to wrap.
        
        Raises
        -------
        RuntimeError
            - If `self` is already wrapped.
        
        Returns
        -------
        self : ``CommandWrapper``
        """
        if (self._wrapped is not None):
            raise RuntimeError(
                f'`{self!r}` is already wrapped; got {wrapped!r}.'
            )
        
        self._wrapped = wrapped
        return self
    
    
    def apply(self, command):
        """
        Applies the wrapper's changes on the respective command.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        command : ``CommandBaseApplicationCommand``
        """
        pass
    
    
    def __repr__(self):
        """Returns the command wrapper's representation."""
        return f'<{self.__class__.__name__} wrapped={self._wrapped!r}>'
    
    
    def fetch_function_and_wrappers_back(self):
        """
        Fetches back the source function and all the wrappers, the returns them.
        
        Returns
        -------
        function : `Any`
            The wrapped function.
        wrappers : `list` of ``CommandWrapper``
            The fetched back wrappers.
        """
        wrappers = [self]
        maybe_wrapper = self._wrapped
        while True:
            if isinstance(maybe_wrapper, CommandWrapper):
                wrappers.append(maybe_wrapper)
                maybe_wrapper = maybe_wrapper._wrapped
            else:
                function = maybe_wrapper
                break
        
        wrappers.reverse()
        return function, wrappers


class ApplicationCommandPermissionOverwriteWrapper(CommandWrapper):
    """
    Wraps a command allowing / disallowing it only for the given user or role inside of a guild.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    _guild_id : `int`
        The guild id where the overwrites should be applied to.
    _permission_overwrite : ``ApplicationCommandPermissionOverwrite``
        The permission overwrite to apply.
    """
    __slots__ = ('_guild_id', '_permission_overwrite')
    
    def __new__(cls, guild, target, allow):
        """
        Creates a partial function to wrap a command.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild's identifier where the overwrite is applied.
        target : ``ClientUserBase``, ``Role``, ``Channel``, `tuple` ((``ClientUserBase``, ``Role``, \
                ``Channel``, `str` (`'Role'`, `'role'`, `'User'`, `'user'`, `'Channel'`, `'channel'`, \
                ``ApplicationCommandPermissionOverwriteTargetType``, `int`)), `int`)
            The target entity of the overwrite
            
            The expected type & value might be pretty confusing, but the target was it to allow relaxing creation.
            To avoid confusing, here is a list of the expected structures:
            
            - ``Role``
            - ``ClientUserBase``
            - ``Channel``
            - `tuple` (``Role``, `int`)
            - `tuple` (``ClientUserBase``, `int`)
            - `tuple` (``Channel``, `int`)
            - `tuple` (`'Role'`, `int`)
            - `tuple` (`'role'`, `int`)
            - `tuple` (`'User'`, `int`)
            - `tuple` (`'user'`, `int`)
            - `tuple` (`'Channel'`, `int`)
            - `tuple` (`'channel'`, `int`)
        
        allow : `bool`
            Whether the respective application command should be enabled for the respective entity.
        """
        if isinstance(guild, Guild):
            guild_id = guild.id
        elif isinstance(guild, (int, str)):
            guild_id = preconvert_snowflake(guild, 'guild')
        else:
            raise TypeError(
                f'`guild` can be `{Guild.__class__.__name__}`, `int`, got {guild.__class__.__name__}; {guild!r}.'
            )
        
        permission_overwrite = ApplicationCommandPermissionOverwrite(target, allow)
        
        self = CommandWrapper.__new__(cls)
        
        self._guild_id = guild_id
        self._permission_overwrite = permission_overwrite
        
        return self
    
    
    def apply(self, command):
        """
        Applies the wrapper's changes on the respective command.
        
        Parameters
        ----------
        command : ``CommandBaseApplicationCommand``
        """
        command.add_permission_overwrite(self._guild_id, self._permission_overwrite)
    
    
    def __repr__(self):
        """Returns the command wrapper's representation."""
        return (
            f'<{self.__class__.__name__} wrapped = {self._wrapped!r}, guild_id = {self._guild_id!r}, '
            f'overwrite = {self._permission_overwrite!r}>'
        )
    
    
    def __matmul__(self, other):
        """Calls the wrapper to wrap a client applying self globally. Can also be used to just apply it to `None`"""
        return self._apply_to(other)
    
    
    @copy_docs(__matmul__)
    def __rmatmul__(self, other):
        return self._apply_to(other)
    
    
    def _apply_to(self, other):
        """
        Tries to apply self to to other.
        
        Parameters
        ----------
        other : `None`, ``ApplicationCommandPermissionOverwriteWrapper``, ``Client``, ``Slasher``
            The object to apply self to.
        
        Returns
        -------
        other : `other`, `self`, `NotImplemented`
            Returns `NotImplemented` if `other`'s type is incompatible.
        
        Raises
        ------
        RuntimeError
            - If `other` is a ``Client`` and it has no `slash` extension setupped.
        """
        if (other is None):
            return self
        
        if type(self) is type(other):
            return self(other)
        
        if isinstance(other, (Client, Slasher)):
            return self._apply_globally(other)
        
        return NotImplemented
    
    
    def _apply_globally(self, other):
        """
        Applies the permission globally to all commands to a client.
        
        Here is an example which enables all commands in the guild only for the given role:
        ```py
        client@set_permission(guild_id, ('role', guild_id), False)
        client@set_permission(guild_id, ('role', role_id), True)
        ```
        
        Parameters
        ----------
        other : ``Client``, ``Slasher``
            The object to add the permission overwrite to.
        
        Returns
        -------
        other : `other`
        
        Raises
        ------
        RuntimeError
            - If `other` has no `slash` extension setupped on it.
        """
        if isinstance(other, Client):
            slasher = getattr(other, 'slasher', None)
            if other is None:
                raise RuntimeError(
                    f'Client {other!r} has no slash extension setupped.'
                )
            
        else:
            slasher = other
        
        slasher._add_permission_overwrites_for_guild(self._guild_id, self._permission_overwrite)
        return other


class ApplicationCommandParameterConfigurerWrapper(CommandWrapper):
    """
    Wraps a command enabling you to modify it's parameter's annotations.
    
    Attributes
    ----------
    _wrapped : `Any`
        The command or other wrapper to wrap.
    _autocomplete : `None`, `CoroutineFunction`
        Auto complete function for the parameter.
    _channel_types : `None`, `tuple` of `int`
        The accepted channel types.
    _choice_enum_type : `None`, `type`
        Enum type of `choices` if applicable.
    _choices : `None`, `dict` of (`str`, `int`, `str`) items
        Parameter's choices.
    _description : `None`, `str`
        Parameter's description.
    _max_length : `int`
        The maximum input length allowed for this option.
    _max_value : `None`, `int`, `float`
        The maximal accepted value by the parameter.
    _min_length : `int`
        The minimum input length allowed for this option.
    _min_value : `None`, `int`, `float`
        The minimal accepted value by the parameter.
    _name : `str`
        The parameter's name.
    _parameter_name : `str`
        The parameter's internal name.
    _type : `int`
        The parameter's internal type identifier.
    """
    __slots__ = (
        '_autocomplete', '_channel_types', '_choice_enum_type', '_choices', '_description', '_max_length',
        '_max_value', '_min_length', '_min_value', '_name', '_parameter_name', '_type'
    )
    
    def __new__(
        cls,
        parameter_name,
        type_or_choice,
        description = None,
        name = None,
        *,
        autocomplete = None,
        channel_types = None,
        max_length = None,
        max_value = None,
        min_length = None,
        min_value = None,
    ):
        """
        Creates a partial function to wrap a command.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name to modify.
        type_or_choice : `str`, `type`, `list`, `dict`
            The annotation's value to use.
        description : `None`, `str` = `None`, Optional
            Description for the annotation.
        name : `None`, `str` = `None`, Optional
            Name to use instead of the parameter's.
        autocomplete : `None`, `CoroutineFunction` = `None`, Optional (Keyword only)
            Auto complete function for the parameter.
        channel_types : `None`, `iterable` of `int` = `None`, Optional (Keyword only)
            The accepted channel types.
        max_length : `None`, `int` = `None`, Optional (Keyword only)
            The maximum input length allowed for this option.
        max_value : `None`, `int`, `float` = `None`, Optional (Keyword only)
            The maximal accepted value by the parameter.
        min_length : `None`, `int` = `None`, Optional (Keyword only)
            The minimum input length allowed for this option.
        min_value : `None`, `int`, `float` = `None`, Optional (Keyword only)
            The minimal accepted value by the parameter.
        
        Returns
        -------
        wrapper : `functools.partial` of ``CommandWrapper._decorate``
            Partial function to wrap a command.
        
        Raises
        ------
        TypeError
            - If `description`'s is not `None` nor `str`.
            - If `parameter_type_or_choice` is `list`, but it's elements do not match the `tuple`
                (`str`, `str`, `int`) pattern.
            - If `parameter_type_or_choice` is `dict`, but it's items do not match the (`str`, `str`, `int`)
                pattern.
            - If `parameter_type_or_choice` is unexpected.
            - If `name`'s is neither `None`, `str`.
            - If `channel_types` is neither `None` nor `iterable` of `int`.
        ValueError
            - If `description`'s length is out of the expected range [2:100].
            - If `parameter_type_or_choice` is `str`, but not any of the expected ones.
            - If `parameter_type_or_choice` is `type`, but not any of the expected ones.
            - If `choice` amount is out of the expected range [1:25].
            - If `type_or_choice` is a choice, and a `choice` name is duped.
            - If `type_or_choice` is a choice, and a `choice` values are mixed types.
            - If received `channel_types` from both `type_or_choice` and `channel_types` parameters.
        """
        if type(parameter_name) is str:
            pass
        elif isinstance(parameter_name, str):
            parameter_name = str(parameter_name)
        else:
            raise TypeError(
                f'`parameter_name` can be `str`, got {parameter_name.__class__.__name__}; {parameter_name!r}.'
            )
        
        type_, choice_enum_type, choices, parsed_channel_types = parse_annotation_type_and_choice(
            type_or_choice, parameter_name
        )
        
        max_length = process_max_length(max_length, ANNOTATION_TYPE_TO_OPTION_TYPE[type_])
        min_length = process_min_length(min_length, ANNOTATION_TYPE_TO_OPTION_TYPE[type_])
        
        type_, max_value = process_max_and_min_value(type_, max_value, 'max_value')
        type_, min_value = process_max_and_min_value(type_, min_value, 'min_value')
        
        processed_channel_types = preprocess_channel_types(channel_types)
        channel_types = postprocess_channel_types(processed_channel_types, parsed_channel_types)
        
        if (description is not None):
            description = parse_annotation_description(description, parameter_name)
        
        name = parse_annotation_name(name, parameter_name)
        
        self = CommandWrapper.__new__(cls)
        
        self._autocomplete = autocomplete
        self._choice_enum_type = choice_enum_type
        self._choices = choices
        self._description = description
        self._name = name
        self._parameter_name = parameter_name
        self._type = type_
        self._channel_types = channel_types
        self._max_value = max_value
        self._min_value = min_value
        self._max_length = max_length
        self._min_length = min_length
        
        return self
    
    
    def __repr__(self):
        """Returns the command wrapper's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' wrapped = ', repr(self._wrapped),
            ', parameter_name = ', repr(self.parameter_name),
        ]
        
        type_ = self._type
        type_name = ANNOTATION_TYPE_TO_STR_ANNOTATION[type_]
        repr_parts.append(', type = ')
        repr_parts.append(type_name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_))
        repr_parts.append(')')
        
        autocomplete = self._autocomplete
        if (autocomplete is not None):
            repr_parts.append(', autocomplete = ')
            repr_parts.append(repr(autocomplete))
        
        choice_enum_type = self._choice_enum_type
        if (choice_enum_type is not None):
            repr_parts.append(', choice_enum_type = ')
            repr_parts.append(choice_enum_type.__name__)
        
        choices = self.choices
        if (choices is not None):
            repr_parts.append(', choices = ')
            repr_parts.append(repr(choices))
        
        description = self._description
        if (description is not None):
            repr_parts.append(', description = ')
            repr_parts.append(reprlib.repr(description))
        
        name = self._name
        if (name is not None):
            repr_parts.append(', name = ')
            repr_parts.append(repr(name))
        
        channel_types = self.channel_types
        if (channel_types is not None):
            repr_parts.append(', channel_types = ')
            repr_parts.append(repr(channel_types))
        
        if type_ is ApplicationCommandOptionType.string:
            # min_length
            min_length = self._min_length
            if (min_length != 0):
                repr_parts.append(', min_length = ')
                repr_parts.append(repr(min_length))
            
            # max_length
            max_length = self._max_length
            if (max_length != 0):
                repr_parts.append(', max_length = ')
                repr_parts.append(repr(max_length))
        
        
        if type_ is ApplicationCommandOptionType.integer or type_ is ApplicationCommandOptionType.float:
            min_value = self._min_value
            if (min_value is not None):
                repr_parts.append(', min_value = ')
                repr_parts.append(repr(min_value))
            
            max_value = self._max_value
            if (max_value is not None):
                repr_parts.append(', max_value = ')
                repr_parts.append(repr(max_value))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


def get_parameter_configurers(wrappers):
    """
    Gets the parameter configure wrappers.
    
    Parameters
    ----------
    wrappers : `None`, `list` of ``CommandWrapper``
        The fetched back wrappers if any.
    
    Returns
    -------
    parameter_configurers : `None`, `dict` of (`str`, ``ApplicationCommandParameterConfigurerWrapper``) items
        The collected parameter configurers if any.
    """
    parameter_configurers = None
    
    if (wrappers is not None):
        for wrapper in wrappers:
            if isinstance(wrapper, ApplicationCommandParameterConfigurerWrapper):
                if parameter_configurers is None:
                    parameter_configurers = {}
                
                parameter_configurers[wrapper._parameter_name] = wrapper
                continue
    
    return parameter_configurers
