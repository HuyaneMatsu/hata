__all__ = ('OnboardingPrompt',)

from ...bases import DiscordEntity
from ...precreate_helpers import process_precreate_parameters_and_raise_extra

from .fields import (
    parse_id, parse_in_onboarding, parse_name, parse_options, parse_required, parse_single_select, parse_type,
    put_id_into, put_in_onboarding_into, put_name_into, put_options_into, put_required_into, put_single_select_into,
    put_type_into, validate_id, validate_in_onboarding, validate_name, validate_options, validate_required,
    validate_single_select, validate_type
)
from .preinstanced import OnboardingPromptType


PRECREATE_FIELDS = {
    'in_onboarding': ('in_onboarding', validate_in_onboarding),
    'name': ('name', validate_name),
    'options': ('options', validate_options),
    'required': ('required', validate_required),
    'single_select': ('single_select', validate_single_select),
}


class OnboardingPrompt(DiscordEntity):
    """
    Option of an onboarding prompt.
    
    Attributes
    ----------
    in_onboarding : `bool`
        Whether this prompt is in the onboarding flow.
    id : `int`
        The prompt's identifier.
    name : `str`
        The prompt's name
    options : `None`, `tuple` of ``OnboardingPromptOption``
        The options of the prompt.
    required : `bool`
        Whether this prompt is required to do in the onboarding flow.
    single_select : `bool`
        Whether only one option can be selected.
    type : ``OnboardingPromptType``
        The prompt's type.
    """
    __slots__ = ('in_onboarding', 'name', 'options', 'required', 'single_select', 'type')
    
    def __new__(
        cls, *, in_onboarding = ..., name = ..., options = ..., prompt_type = ..., required = ..., single_select = ...
    ):
        """
        Creates an onboarding prompt instance from the given parameters.
        
        Parameters
        ----------
        in_onboarding : `bool`, Optional (Keyword only)
            Whether this prompt is in the onboarding flow.
        name : `str`, Optional (Keyword only)
            The prompt's name
        options : `None`, `iterable` of ``OnboardingPromptOption``, Optional (Keyword only)
            The options of the prompt.
        prompt_type : ``OnboardingPromptType``, `int`, Optional (Keyword only)
            The prompt's type.
        required : `bool`, Optional (Keyword only)
            Whether this prompt is required to do in the onboarding flow.
        single_select : `bool`, Optional (Keyword only)
            Whether only one option can be selected.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # in_onboarding
        if in_onboarding is ...:
            in_onboarding = False
        else:
            in_onboarding = validate_in_onboarding(in_onboarding)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # options
        if options is ...:
            options = None
        else:
            options = validate_options(options)
        
        # prompt_type
        if prompt_type is ...:
            prompt_type = OnboardingPromptType.multiple_choice
        else:
            prompt_type = validate_type(prompt_type)
        
        # required
        if required is ...:
            required = False
        else:
            required = validate_required(required)
        
        # single_select
        if single_select is ...:
            single_select = False
        else:
            single_select = validate_single_select(single_select)
        
        self = object.__new__(cls)
        self.in_onboarding = in_onboarding
        self.id = 0
        self.name = name
        self.options = options
        self.required = required
        self.single_select = single_select
        self.type = prompt_type
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new onboarding prompt from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Onboarding prompt option data.
        
        Returns
        -------
        new : `instance<cls>`
        """
        self = object.__new__(cls)
        self.in_onboarding = parse_in_onboarding(data)
        self.id = parse_id(data)
        self.name = parse_name(data)
        self.options = parse_options(data)
        self.required = parse_required(data)
        self.single_select = parse_single_select(data)
        self.type = parse_type(data)
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = True):
        """
        Converts the onboarding prompt to json serializable object.
        
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
        put_in_onboarding_into(self.in_onboarding, data, defaults)
        put_name_into(self.name, data, defaults)
        put_options_into(self.options, data, defaults, include_internals = include_internals)
        put_required_into(self.required, data, defaults)
        put_single_select_into(self.single_select, data, defaults)
        put_type_into(self.type, data, defaults)
        
        if include_internals:
            put_id_into(self.id, data, defaults)
        
        return data
    
    
    def __repr__(self):
        """Returns the onboarding prompt's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
        ]
        
        prompt_id = self.id
        if prompt_id:
            repr_parts.append(' id = ')
            repr_parts.append(repr(prompt_id))
            repr_parts.append(',')
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        prompt_type = self.type
        repr_parts.append(', type = ')
        repr_parts.append(prompt_type.name)
        repr_parts.append(' ~ ')
        repr_parts.append(repr(prompt_type.value))
        
        in_onboarding = self.in_onboarding
        if in_onboarding:
            repr_parts.append(', in_onboarding = ')
            repr_parts.append(repr(in_onboarding))
        
        required = self.required
        if required:
            repr_parts.append(', required = ')
            repr_parts.append(repr(required))
            
        single_select = self.single_select
        if single_select:
            repr_parts.append(', single_select = ')
            repr_parts.append(repr(single_select))
        
        options = self.options
        if (options is not None):
            repr_parts.append(', options = [')
            
            index = 0
            length = len(options)
            
            while True:
                option = options[index]
                index += 1
                
                repr_parts.append(repr(option))
                
                if index == length:
                    break
                
                repr_parts.append(', ')
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two onboarding prompts are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    def __ne__(self, other):
        """Returns whether the two onboarding prompts are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two onboarding prompts are equal.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            The other instance.
        
        Returns
        -------
        are_equal : `bool`
        """
        if self.in_onboarding != other.in_onboarding:
            return False
        
        # id
        # Ignore it
        
        if self.name != other.name:
            return False
        
        if self.options != other.options:
            return False
        
        if self.required != other.required:
            return False
        
        if self.single_select != other.single_select:
            return False
        
        if self.type is not other.type:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the onboarding prompt's hash value."""
        hash_value = 0
        
        hash_value ^= self.in_onboarding
        
        # id
        # ignore it
        
        name = self.name
        if (name is not None):
            hash_value ^= hash(name)
        
        options = self.options
        if (options is not None):
            hash_value ^= len(options) << 2
            
            for option in options:
                hash_value ^= hash(option)
        
        hash_value ^= self.required << 5
        
        hash_value ^= self.single_select << 6
        
        hash_value ^= self.type.value << 7
        
        return hash_value
    
    
    @classmethod
    def precreate(
        cls,
        prompt_id,
        prompt_type = ...,
        **keyword_parameters,
    ):
        """
        Precreates an onboarding prompt. Since they are not cached, this method just a ``.__new__`` alternative.
        
        Parameters
        ----------
        prompt_id : `int`
            The prompt's identifier.
        prompt_type : ``PromptType``, `int`, Optional (Keyword only)
            The prompt's type.
        **keyword_parameters : Keyword parameters
            Additional parameters defining how the option's fields should be set.
        
        Other Parameters
        ----------------
        in_onboarding : `bool`, Optional (Keyword only)
            Whether this prompt is in the onboarding flow.
        name : `str`, Optional (Keyword only)
            The prompt's name
        options : `None`, `iterable` of ``OnboardingPromptOption``, Optional (Keyword only)
            The options of the prompt.
        required : `bool`, Optional (Keyword only)
            Whether this prompt is required to do in the onboarding flow.
        single_select : `bool`, Optional (Keyword only)
            Whether only one option can be selected.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        prompt_id = validate_id(prompt_id)
        
        # prompt_type
        if prompt_type is ...:
            prompt_type = OnboardingPromptType.multiple_choice
        else:
            prompt_type = validate_type(prompt_type)
        
        if keyword_parameters:
            processed = process_precreate_parameters_and_raise_extra(keyword_parameters, PRECREATE_FIELDS)
        else:
            processed = None
        
        # Construct
        
        self = object.__new__(cls)
        self.in_onboarding = False
        self.id = prompt_id
        self.name = ''
        self.options = None
        self.required = False
        self.single_select = False
        self.type = prompt_type
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    def copy(self):
        """
        Copies the onboarding prompt.
        
        Returns
        -------
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.in_onboarding = self.in_onboarding
        new.id = 0
        new.name = self.name
        
        options = self.options
        if (options is not None):
            options = (*(option.copy() for option in options),)
        new.options = options
        
        new.required = self.required
        new.single_select = self.single_select
        new.type = self.type
        return new
    
    
    def copy_with(
        self, *, in_onboarding = ..., name = ..., options = ..., prompt_type = ..., required = ..., single_select = ...
    ):
        """
        Copies the onboarding prompt with the given fields.
        
        Parameters
        ----------
        in_onboarding : `bool`, Optional (Keyword only)
            Whether this prompt is in the onboarding flow.
        name : `str`, Optional (Keyword only)
            The prompt's name
        options : `None`, `iterable` of ``OnboardingPromptOption``, Optional (Keyword only)
            The options of the prompt.
        prompt_type : ``OnboardingPromptType``, `int`, Optional (Keyword only)
            The prompt's type.
        required : `bool`, Optional (Keyword only)
            Whether this prompt is required to do in the onboarding flow.
        single_select : `bool`, Optional (Keyword only)
            Whether only one option can be selected.
        
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
        # in_onboarding
        if in_onboarding is ...:
            in_onboarding = self.in_onboarding
        else:
            in_onboarding = validate_in_onboarding(in_onboarding)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # options
        if options is ...:
            options = self.options
            if (options is not None):
                options = (*(option.copy() for option in options),)
        else:
            options = validate_options(options)
        
        # prompt_type
        if prompt_type is ...:
            prompt_type = self.type
        else:
            prompt_type = validate_type(prompt_type)
        
        # required
        if required is ...:
            required = self.required
        else:
            required = validate_required(required)
        
        # single_select
        if single_select is ...:
            single_select = self.single_select
        else:
            single_select = validate_single_select(single_select)
        
        new = object.__new__(type(self))
        new.in_onboarding = in_onboarding
        new.id = 0
        new.name = name
        new.options = options
        new.required = required
        new.single_select = single_select
        new.type = prompt_type
        return new
    
    
    def iter_options(self):
        """
        Iterates over the options of the prompt.
        
        This method is an iterable generator.
        
        Yields
        ------
        option : ``OnboardingPromptOption``
        """
        options = self.options
        if (options is not None):
            yield from options
