__all__ = ()

from scarletio import copy_docs, include

from ....discord.application_command import ApplicationCommandOption, ApplicationCommandOptionChoice

from ..constants import APPLICATION_COMMAND_FUNCTION_DEEPNESS
from ..converter_constants import (
    ANNOTATION_AUTO_COMPLETE_AVAILABILITY, ANNOTATION_TYPE_TO_OPTION_TYPE, ANNOTATION_TYPE_TO_REPRESENTATION,
    ANNOTATION_TYPE_TO_STR_ANNOTATION
)
from ..exceptions import SlashCommandParameterConversionError

from .base import ParameterConverterBase


SlashCommandParameterAutoCompleter = include('SlashCommandParameterAutoCompleter')


class ParameterConverterSlashCommand(ParameterConverterBase):
    """
    Converter class for slash command options.
    
    Attributes
    ----------
    auto_completer : `None | SlashCommandParameterAutoCompleter`
        Auto completer if registered.
    
    channel_types : `None | tuple<ChannelType>``
        The accepted channel types.
    
    choice_enum_type : `None | type<Enum>`
        Enum type of `choices` if applicable.
    
    choices : `None | dict<int | float | str | Enum, str>`
        The choices to choose from if applicable. The keys are choice vales meanwhile the values are choice names.
    
    converter : `CoroutineFunctionType`
        The converter to use to convert a value to it's desired type.
    
    default : `object`
        Default value of the parameter.
    
    description : `None | str
        The parameter's description.
    
    max_length : `int`
        The maximum input length allowed for this option.
    
    max_value : `None | int | float`
        The maximal accepted value by the converter.
    
    min_length : `int`
        The minimum input length allowed for this option.
    
    min_value : `None | int | float`
        The minimal accepted value by the converter.
    
    name : `str`
        The parameter's name.
    
    parameter_name : `str`
        The parameter's internal name.
    
    required : `bool`
        Whether the the parameter is required.
    
    type : `int`
        Internal identifier of the converter.
    """
    __slots__ = (
        'auto_completer', 'channel_types', 'choice_enum_type', 'choices', 'converter', 'default', 'description',
        'max_length', 'max_value', 'min_length', 'min_value', 'name', 'required', 'type'
    )
    
    def __new__(
        cls,
        parameter_name,
        converter_type,
        converter,
        name,
        description,
        default,
        required,
        choice_enum_type,
        choices,
        channel_types,
        max_value,
        min_value,
        auto_completer_function,
        max_length,
        min_length,
    ):
        """
        Creates a new ``ParameterConverterSlashCommand`` from the given parameters.
        
        Parameters
        ----------
        parameter_name : `str`
            The parameter's name.
        
        converter_type : `int`
            Internal identifier of the converter.
        
        converter : `CoroutineFunctionType`
            The converter to use to convert a value to it's desired type.
        
        name : `str`
            The parameter's internal name.
        
        description : `None | str`
            The parameter's description.
        
        default : `bool`
            Default value of the parameter.
        
        required : `bool`
            Whether the the parameter is required.
        
        choice_enum_type : `None | type<Enum>`
            Enum type of `choices` if applicable.
        
        choices : `None | dict<int | float | str | Enum, str>`
            The choices to choose from if applicable. The keys are choice vales meanwhile the values are choice names.
        
        channel_types : `None | tuple<ChannelType>`
            The accepted channel types.
        
        max_value : `None | int | float`
            The maximal accepted value by the converter.
        
        min_value : `None | int | float`
            The minimal accepted value by the converter.
        
        auto_completer_function : `None | async-callable`
            Auto completer if defined.
        
        max_length : `int`
            The maximum input length allowed for this option.
        
        min_length : `int`
            The minimum input length allowed for this option.
        """
        self = object.__new__(cls)
        
        self.parameter_name = parameter_name
        self.auto_completer = None
        self.choice_enum_type = choice_enum_type
        self.choices = choices
        self.converter = converter
        self.default = default
        self.description = description
        self.name = name
        self.required = required
        self.type = converter_type
        self.channel_types = channel_types
        self.max_value = max_value
        self.min_value = min_value
        self.max_length = max_length
        self.min_length = min_length
        
        if (auto_completer_function is not None):
            auto_completer = SlashCommandParameterAutoCompleter(
                auto_completer_function, [parameter_name], APPLICATION_COMMAND_FUNCTION_DEEPNESS, None
            )
            self.register_auto_completer(auto_completer)
        
        return self
    
    
    @copy_docs(ParameterConverterBase.__call__)
    async def __call__(self, client, interaction_event, value):
        choices = self.choices
        
        if (value is None):
            if not self.required:
                return self.default
        
        else:
            converted_value = await self.converter(client, interaction_event, value)
            if (converted_value is not None):
                if (choices is None):
                    return converted_value
                
                choice_enum_type = self.choice_enum_type
                if (choice_enum_type is None):
                    if (converted_value in choices):
                        return converted_value
                
                else:
                    try:
                        converted_value = choice_enum_type(converted_value)
                    except ValueError:
                        pass
                    else:
                        return converted_value
        
        
        raise SlashCommandParameterConversionError(
            self.name,
            value,
            ANNOTATION_TYPE_TO_REPRESENTATION.get(self.type, '???'),
            None if choices is None else [*choices.keys()],
        )
    
    @copy_docs(ParameterConverterBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # name
        name = self.name
        if (self.parameter_name != name):
            repr_parts.append(', name = ')
            repr_parts.append(repr(name))
        
        # type
        repr_parts.append(', type = ')
        repr_parts.append(ANNOTATION_TYPE_TO_STR_ANNOTATION[self.type])
        
        # description
        repr_parts.append(', description = ')
        repr_parts.append(repr(self.description))
        
        # required
        repr_parts.append(', required = ')
        repr_parts.append(repr(self.required))
        
        if not self.required:
            repr_parts.append(', default = ')
            repr_parts.append(repr(self.default))
        
        # choices
        choices = self.choices
        if (choices is not None):
            repr_parts.append(', choices = ')
            repr_parts.append(repr(choices))
        
        # auto_completer
        auto_completer = self.auto_completer
        if (auto_completer is not None):
            repr_parts.append(', auto_completer = ')
            repr_parts.append(repr(auto_completer))
        
        # channel_types
        channel_types = self.channel_types
        if (channel_types is not None):
            repr_parts.append(', channel_types = ')
            repr_parts.append(repr(channel_types))
        
        # min_value
        min_value = self.min_value
        if (min_value is not None):
            repr_parts.append(', min_value = ')
            repr_parts.append(repr(min_value))
        
        # max_value
        max_value = self.max_value
        if (max_value is not None):
            repr_parts.append(', max_value = ')
            repr_parts.append(repr(max_value))
        
        # min_length
        min_length = self.min_length
        if (min_length != 0):
            repr_parts.append(', min_length = ')
            repr_parts.append(repr(min_length))
        
        # max_length
        max_length = self.max_length
        if (max_length != 0):
            repr_parts.append(', max_length = ')
            repr_parts.append(repr(max_length))
    
    
    @copy_docs(ParameterConverterBase.as_option)
    def as_option(self):
        choices = self.choices
        if choices is None:
            option_choices = None
        else:
            is_enum = (self.choice_enum_type is not None)
            
            option_choices = [
                ApplicationCommandOptionChoice(name, str(value.value if is_enum else value))
                for value, name in choices.items()
            ]
        
        option_type = ANNOTATION_TYPE_TO_OPTION_TYPE[self.type]
        
        return ApplicationCommandOption(
            self.name,
            self.description,
            option_type,
            autocomplete = (self.auto_completer is not None),
            channel_types = self.channel_types,
            choices = option_choices,
            required = self.required,
            min_value = self.min_value,
            max_value = self.max_value,
            min_length = self.min_length,
            max_length = self.max_length,
        )
    
    
    def can_be_auto_completed(self):
        """
        Returns whether the parameter can be auto completed.
        
        Returns
        -------
        can_be_auto_completed : `bool`
            Whether the parameter can be auto completed.
        """
        if (self.type not in ANNOTATION_AUTO_COMPLETE_AVAILABILITY):
            return False
        
        if (self.choices is not None):
            return False
        
        return True
    
    
    def is_auto_completed(self):
        """
        Returns whether the parameter is already auto completed.
        
        Returns
        -------
        is_auto_completed : `bool`
        """
        return (self.auto_completer is not None)
    
    
    def register_auto_completer(self, auto_completer):
        """
        Registers an auto completer to the slash command parameter converter.
        
        Parameters
        ----------
        auto_completer : ``SlashCommandParameterAutoCompleter``
            The auto completer to register.
        
        Returns
        -------
        resolved : `int`
            Whether the parameter was resolved.
        
        Raises
        ------
        RuntimeError
            If the parameter cannot be auto completed.
        """
        if (self.type not in ANNOTATION_AUTO_COMPLETE_AVAILABILITY):
            raise RuntimeError(
                f'Parameter `{self.name}` can not be auto completed. Only string base type parameters '
                f'can be (str, int, expression).'
            )
        
        if (self.choices is not None):
            raise RuntimeError(
                f'Parameter `{self.name}` can not be auto completed. `choices` and `autocomplete` are'
                f'mutually exclusive.'
            )
        
        self_auto_completer = self.auto_completer
        if (self_auto_completer is None) or auto_completer._is_deeper_than(self_auto_completer):
            self.auto_completer = auto_completer
            resolved = 1
        else:
            resolved = 0
        
        return resolved
    
    
    @copy_docs(ParameterConverterBase.bind_parent)
    def bind_parent(self, parent):
        auto_completer = self.auto_completer
        if (auto_completer is not None):
            self.auto_completer = auto_completer._bind_parent(parent)
