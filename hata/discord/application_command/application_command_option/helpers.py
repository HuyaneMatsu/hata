__all__ = ()

from ..application_command_option_metadata.constants import (
    APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT, APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT
)

from ..application_command_option_metadata.fields import (
    validate_autocomplete, validate_channel_types, validate_choices, validate_default, validate_max_length,
    validate_max_value, validate_min_length, validate_min_value, validate_options, validate_required
)


FIELDS = {
    'autocomplete': (validate_autocomplete, False),
    'channel_types': (validate_channel_types, None),
    'choices': (validate_choices, None),
    'default': (validate_default, False),
    'max_length': (validate_max_length, APPLICATION_COMMAND_OPTION_MAX_LENGTH_DEFAULT),
    'max_value': (validate_max_value, None),
    'min_length': (validate_min_length, APPLICATION_COMMAND_OPTION_MIN_LENGTH_DEFAULT),
    'min_value': (validate_min_value, None),
    'options': (validate_options, None),
    'required': (validate_required, False),
}


def _purge_defaults_and_maybe_raise(keyword_parameters):
    """
    Validates every keyword value. If the output is a default value ignores it.
    
    Raises on extra field and on non-default values.
    
    Parameters
    ----------
    keyword_parameters : `dict` of (`str`, `object)` items
        Keyword parameters passed to an application command option constructor (or copier).
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
        - Extra parameters given.
    ValueError
        - If a parameter's value is incorrect.
        - if a parameter is not applicable for the given option.
    """
    while keyword_parameters:
        key, value = keyword_parameters.popitem()
        
        try:
            validator, default_value = FIELDS[key]
        except KeyError:
            raise TypeError(
                f'Received extra field: field = {key!r}; value = {value!r}.'
            )
        
        validated = validator(value)
        if validated != default_value:
            raise ValueError(
                f'Field not applicable for the option type: field = {key!r}; value = {value!r}.'
            )
