__all__ = ('SlasherApplicationCommandParameterConfigurerWrapper',
    'SlasherApplicationCommandPermissionOverwriteWrapper', 'SlasherCommandWrapper')

import reprlib
from functools import partial as partial_func

from ...discord.guild import Guild
from ...discord.preconverters import preconvert_snowflake
from ...discord.interaction import ApplicationCommandPermissionOverwrite

from .converters import parse_annotation_description, parse_annotation_type_and_choice, parse_annotation_name, \
    ANNOTATION_TYPE_TO_STR_ANNOTATION

class SlasherCommandWrapper:
    """
    Wraps a slash command enabling the wrapper to postprocess the created slash command.
    
    Attributes
    ----------
    _wrapped : `Any`
        The wrapped object.
    """
    __slots__ = ('_wrapped',)
    def __new__(cls):
        """
        Creates a partial function to wrap a slash command.
        
        Subclasses should overwrite this method.
        
        Returns
        -------
        wrapper : `functools.partial` of ``SlasherCommandWrapper._decorate``
            Partial function to wrap a slash command.
        """
        return partial_func(cls._decorate, cls)
    
    def _decorate(cls, wrapped):
        """
        Wraps the given command.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        wrapped : `Any`
            The slash command or other wrapper to wrap.
        
        Returns
        -------
        self : ``SlasherCommandWrapper``
            The created instance.
        """
        self = object.__new__(cls)
        self._wrapped = wrapped
        return self
    
    def apply(self, slasher_application_command):
        """
        Applies the wrapper's changes on the respective slash command.
        
        Subclasses should overwrite this method.
        
        Parameters
        ----------
        slasher_application_command : ``SlasherApplicationCommand``
        """
        pass
    
    def __repr__(self):
        """Returns the slash command wrapper's representation."""
        return f'<{self.__class__.__name__} wrapped={self._wrapped!r}>'
    
    def fetch_function_and_wrappers_back(self):
        """
        Fetches back the source function and all the wrappers, the returns them.
        
        Returns
        -------
        function : `Any`
            The wrapped function.
        wrappers : `list` of ``SlasherCommandWrapper`` instances
            The fetched back wrappers.
        """
        wrappers = [self]
        maybe_wrapper = self._wrapped
        while True:
            if isinstance(maybe_wrapper, SlasherCommandWrapper):
                wrappers.append(maybe_wrapper)
                maybe_wrapper = maybe_wrapper._wrapped
            else:
                function = maybe_wrapper
                break
        
        wrappers.reverse()
        return function, wrappers


class SlasherApplicationCommandPermissionOverwriteWrapper(SlasherCommandWrapper):
    """
    Wraps a slash to command allowing / disallowing it only for the given user or role inside of a guild.
    
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
        Creates a partial function to wrap a slash command.
        
        Parameters
        ----------
        guild : ``Guild`` or `int`
            The guild's identifier where the overwrite is applied.
        target : ``ClientUserBase`` or ``Role``, `tuple` ((``ClientUserBase``, ``Role`` type) or \
                `str` (`'Role'`, `'role'`, `'User'`, `'user'`), `int`)
            The target entity of the overwrite
            
            The expected type & value might be pretty confusing, but the target was it to allow relaxing creation.
            To avoid confusing, here is a list of the expected structures:
            
            - ``Role`` instance
            - ``ClientUserBase`` instance
            - `tuple` (``Role`` type, `int`)
            - `tuple` (``ClientUserBase``, `int`)
            - `tuple` (`'Role'`, `int`)
            - `tuple` (`'role'`, `int`)
            - `tuple` (`'User'`, `int`)
            - `tuple` (`'user'`, `int`)
        
        allow : `bool`
            Whether the respective application command should be enabled for the respective entity.
        
        Returns
        -------
        wrapper : `functools.partial` of ``SlasherCommandWrapper._decorate``
            Partial function to wrap a slash command.
        """
        if isinstance(guild, Guild):
            guild_id = guild.id
        elif isinstance(guild, (int, str)):
            guild_id = preconvert_snowflake(guild, 'guild')
        else:
            raise TypeError(f'`guild` can be given neither as `{Guild.__class__.__name__}`, and as `int` instance, '
                f'got {guild.__class__.__name__}.')
        
        overwrite = ApplicationCommandPermissionOverwrite(target, allow)
        
        return partial_func(cls._decorate, cls, guild_id, overwrite)
    
    
    def _decorate(cls, guild_id, permission_overwrite, wrapped):
        """
        Wraps given command.
        
        Parameters
        ----------
        guild_id : `int`
            The guild id where the overwrites should be applied to.
        permission_overwrite : ``ApplicationCommandPermissionOverwrite``
            The permission overwrite to apply.
        wrapped : `Any`
            The slash command or other wrapper to wrap.
        
        Returns
        -------
        self : ``SlasherCommandWrapper``
            The created instance.
        """
        self = object.__new__(cls)
        self._guild_id = guild_id
        self._permission_overwrite = permission_overwrite
        self._wrapped = wrapped
        return self
    
    
    def apply(self, slasher_application_command):
        """
        Applies the wrapper's changes on the respective slash command.
        
        Parameters
        ----------
        slasher_application_command : ``SlasherApplicationCommand``
        """
        slasher_application_command.add_permission_overwrite(self._guild_id, self._permission_overwrite)
    
    
    def __repr__(self):
        """Returns the slash command wrapper's representation."""
        return f'<{self.__class__.__name__} wrapped={self._wrapped!r}, guild_id={self._guild_id!r}, ' \
            f'overwrite={self._permission_overwrite!r}>'


class SlasherApplicationCommandParameterConfigurerWrapper(SlasherCommandWrapper):
    """
    Wraps a slash command enabling you to modify it's parameter's annotations.
    
    Attributes
    ----------
    _wrapped : `Any`
        The slash command or other wrapper to wrap.
    _channel_types : `None` or `tuple` of `int`
        The accepted channel types.
    _choices : `None` or `dict` of (`str` or `int`, `str`) items
        Parameter's choices.
    _description : `None` or `str`
        Parameter's description.
    _name : `str`
        The parameter's name.
    _parameter_name : `str`
        The parameter's internal name.
    _type : `int`
        The parameter's internal type identifier.
    """
    __slots__ = ('_channel_types', '_choices', '_description', '_name', '_parameter_name', '_type')
    
    def __new__(cls, parameter_name, type_or_choice, description=None, name=None, *, channel_types=None):
        """
        Creates a partial function to wrap a slash command.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name to modify.
        type_or_choice : `str`, `type`, `list`, `dict`
            The annotation's value to use.
        description : `None` or `str`, Optional
            Description for the annotation.
        name : `None` or `str`, Optional
            Name to use instead of the parameter's.
        channel_types : `None` or `iterable` of `int`
            The accepted channel types.
        
        Returns
        -------
        wrapper : `functools.partial` of ``SlasherCommandWrapper._decorate``
            Partial function to wrap a slash command.
        
        Raises
        ------
        TypeError
            - If `description`'s is not `None` nor `str` instance.
            - If `parameter_type_or_choice` is `list` instance, but it's elements do not match the `tuple`
                (`str`, `str` or `int`) pattern.
            - If `parameter_type_or_choice` is `dict` instance, but it's items do not match the (`str`, `str` or `int`)
                pattern.
            - If `parameter_type_or_choice` is unexpected.
            - If `name`'s is neither `None` or `str` instance.
            - If `channel_types` is neither `None` nor `iterable` of `int`.
        ValueError
            - If `description`'s length is out of the expected range [2:100].
            - If `parameter_type_or_choice` is `str` instance, but not any of the expected ones.
            - If `parameter_type_or_choice` is `type` instance, but not any of the expected ones.
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
            raise TypeError(f'`parameter_name` can be `str`, got {parameter_name.__class__.__name__}.')
        
        if (channel_types is None):
            channel_types_processed = None
        else:
            channel_types_processed = None
            
            iterator = getattr(type(channel_types), '__iter__', None)
            if (iterator is None):
                raise TypeError(f'`channel_types` is neither `None` nor `iterable`, got '
                    f'{channel_types.__class__.__anme__}.')
            
            for channel_type in iterator(channel_types):
                if type(channel_type) is int:
                    pass
                elif isinstance(channel_type, int):
                    channel_type = int(channel_type)
                else:
                    raise TypeError(f'`channel_types` may include only `int` instances, got '
                        f'{channel_type.__class__.__name__}; {channel_type!r}.')
                
                if channel_types_processed is None:
                    channel_types_processed = set()
                
                channel_types_processed.add(channel_type)
        
            if channel_types_processed:
                channel_types_processed = tuple(sorted(channel_types_processed))
            else:
                channel_types_processed = None
        
        type_, choices, parsed_channel_types = parse_annotation_type_and_choice(type_or_choice, parameter_name)
        
        if (parsed_channel_types is not None):
            if (channel_types_processed is not None):
                raise ValueError(f'`received `channel_types` from both `type_or_choice` and `channel_types` '
                    f'parameters.')
            
            channel_types = parsed_channel_types
        else:
            channel_types = channel_types_processed
            
        if (description is not None):
            description = parse_annotation_description(description, parameter_name)
        name = parse_annotation_name(name, parameter_name)
        
        return partial_func(cls._decorate, cls, choices, description, name, parameter_name, type_, channel_types)
    
    
    def _decorate(cls, choices, description, name, parameter_name, type_, channel_types, wrapped):
        """
        Wraps given command.
        
        Parameters
        ----------
        choices : `None` or `dict` of (`str` or `int`, `str`) items
            Parameter's choices.
        description : `str`
            Parameter's description.
        name : `str`
            The parameter's name.
        parameter_name : `str`
            The parameter's internal name.
        type_ : `int`
            The parameter's internal type identifier.
        channel_types : `None` or `tuple` of `int`
            The accepted channel types.
        wrapped : `Any`
            The slash command or other wrapper to wrap.
        
        Returns
        -------
        self : ``SlasherCommandWrapper``
            The created instance.
        """
        self = object.__new__(cls)
        self._choices = choices
        self._description = description
        self._name = name
        self._parameter_name = parameter_name
        self._type = type_
        self._channel_types = channel_types
        self._wrapped = wrapped
        
        return self
    
    
    def __repr__(self):
        """Returns the slash command wrapper's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' wrapped=', repr(self._wrapped),
            ', parameter_name=', repr(self.parameter_name),
        ]
        
        type_ = self._type
        type_name = ANNOTATION_TYPE_TO_STR_ANNOTATION[type_]
        repr_parts.append(', type=')
        repr_parts.append(type_name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_))
        repr_parts.append(')')
        
        choices = self.choices
        if (choices is not None):
            repr_parts.append(', choices=')
            repr_parts.append(repr(choices))
        
        description = self._description
        if (description is not None):
            repr_parts.append(', description=')
            repr_parts.append(reprlib.repr(description))
        
        name = self._name
        if (name is not None):
            repr_parts.append(', name=')
            repr_parts.append(repr(name))
        
        channel_types = self.channel_types
        if (channel_types is not None):
            repr_parts.append(', channel_types=')
            repr_parts.append(repr(channel_types))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


def get_parameter_configurers(wrappers):
    """
    Gets the parameter configure wrappers.
    
    Parameters
    ----------
    wrappers : `None` or `list` of ``SlasherCommandWrapper``
        The fetched back wrappers if any.
    
    Returns
    -------
    parameter_configurers : `None` or `dict` of (`str`, ``SlasherApplicationCommandParameterConfigurerWrapper``) items
        The collected parameter configurers if any.
    """
    parameter_configurers = None
    
    if (wrappers is not None):
        for wrapper in wrappers:
            if isinstance(wrapper, SlasherApplicationCommandParameterConfigurerWrapper):
                if parameter_configurers is None:
                    parameter_configurers = {}
                
                parameter_configurers[wrapper._parameter_name] = wrapper
                continue
    
    return parameter_configurers
