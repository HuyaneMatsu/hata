__all__ = ()

from functools import partial as partial_func

from ...application import Application, ApplicationIntegrationType
from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, flag_parser_factory, force_string_parser_factory,
    nullable_functional_parser_factory, nullable_object_array_parser_factory, nullable_string_parser_factory,
    preinstanced_array_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    force_string_putter_factory, nullable_entity_array_optional_putter_factory,
    nullable_functional_optional_putter_factory, nullable_string_putter_factory, preinstanced_array_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, flag_validator_factory,
    nullable_object_array_validator_factory, nullable_string_validator_factory, preinstanced_array_validator_factory,
    preinstanced_validator_factory
)
from ...guild import Guild
from ...localization.helpers import localized_dictionary_builder
from ...localization.utils import build_locale_dictionary, destroy_locale_dictionary
from ...permission import Permission
from ...utils import is_valid_application_command_name

from ..application_command_option import ApplicationCommandOption

from .constants import (
    DESCRIPTION_LENGTH_MAX, DESCRIPTION_LENGTH_MIN,
    NAME_LENGTH_MAX, NAME_LENGTH_MIN, OPTIONS_MAX
)
from .preinstanced import (
    INTEGRATION_CONTEXT_TYPES_ALL, ApplicationCommandIntegrationContextType,
    ApplicationCommandTargetType
)

# allow_in_dm

validate_allow_in_dm = bool_validator_factory('allow_in_dm', True)

# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id_into = entity_id_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', Application)

# description

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory(
    'description', DESCRIPTION_LENGTH_MIN, DESCRIPTION_LENGTH_MAX
)

# description_localizations

parse_description_localizations = nullable_functional_parser_factory(
    'description_localizations', build_locale_dictionary
)
put_description_localizations_into = nullable_functional_optional_putter_factory(
    'description_localizations', destroy_locale_dictionary
)
validate_description_localizations = partial_func(
    localized_dictionary_builder, parameter_name = 'description_localizations'
)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('id')

# integration_context_types

parse_integration_context_types = preinstanced_array_parser_factory(
    'contexts', ApplicationCommandIntegrationContextType
)


def put_integration_context_types_into(integration_context_types, data, defaults):
    """
    Puts the `integration_context_types`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    integration_context_types : `None | tuple<ApplicationCommandIntegrationContextType>`
        The places where the application command shows up.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if integration_context_types is None:
        raw = None
    else:
        raw = [preinstanced.value for preinstanced in integration_context_types]
    
    data['contexts'] = raw
    return data


validate_integration_context_types = preinstanced_array_validator_factory(
    'integration_context_types', ApplicationCommandIntegrationContextType
)


# integration_types

parse_integration_types = preinstanced_array_parser_factory('integration_types', ApplicationIntegrationType)


def put_integration_types_into(integration_types, data, defaults):
    """
    Puts the `integration_types`'s data into the given `data` json serializable object.
    
    Parameters
    ----------
    integration_types : `None | tuple<ApplicationIntegrationType>`
        The options where the application command can be integrated to.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if integration_types is None:
        raw = None
    else:
        raw = [preinstanced.value for preinstanced in integration_types]
    
    data['integration_types'] = raw
    return data


validate_integration_types = preinstanced_array_validator_factory('integration_types', ApplicationIntegrationType)


# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')


def validate_name(name):
    """
    Validates the given application command's name.
    
    Parameters
    ----------
    name : `None`, `str`
        The application command name to validate.
    
    Returns
    -------
    name : `str`
        The validated name.
    
    Raises
    ------
    TypeError
        - If `name`'s type is incorrect.
    ValueError
        - If `name`'s value is incorrect.
    """
    if name is None:
        return ''
    
    if not isinstance(name, str):
        raise TypeError(
            f'`name` can be `None`, `str`, got {type(name).__name__} ;{name!r}.'
        )
    
    name_length = len(name)
    if (
        name_length and (
            (name_length < NAME_LENGTH_MIN) or
            (name_length > NAME_LENGTH_MAX)
        )
    ):
        raise ValueError(
            f'`name` length can be >= {NAME_LENGTH_MIN} and '
            f'<= {NAME_LENGTH_MAX}, got {name_length}; name = {name!r}'
        )
    
    if not is_valid_application_command_name(name):
        raise ValueError(
            f'`name` contains unexpected character(s) (that are not valid as an application command name); '
            f'got {name!r}.'
        )
    
    return name


# name_localizations

parse_name_localizations = nullable_functional_parser_factory(
    'name_localizations', build_locale_dictionary
)
put_name_localizations_into = nullable_functional_optional_putter_factory(
    'name_localizations', destroy_locale_dictionary
)
validate_name_localizations = partial_func(
    localized_dictionary_builder, parameter_name = 'name_localizations'
)

# nsfw

parse_nsfw = bool_parser_factory('nsfw', False)
put_nsfw_into = bool_optional_putter_factory('nsfw', False)
validate_nsfw = bool_validator_factory('nsfw', False)

# options

parse_options = nullable_object_array_parser_factory('options', ApplicationCommandOption)
put_options_into = nullable_entity_array_optional_putter_factory('options', ApplicationCommandOption)
_pre_validate_options = nullable_object_array_validator_factory('options', ApplicationCommandOption)


def validate_options(options):
    """
    Validates the given application command option `options` field.
    
    Parameters
    ----------
    options : `None`, `iterable` of ``ApplicationCommandOption``
        The parameters or sub-commands of the command option. It's length can be in range [0:25].
    
    Returns
    -------
    options : `None`, `tuple` of ``ApplicationCommandOption``
    
    Returns
    -------
    TypeError
        - If `options`'s type is incorrect.
    ValueError
        - If `options`'s value is incorrect.
        - If `options` is not applicable for the given type.
    """
    options = _pre_validate_options(options)
    if (options is not None):
        options = options[:OPTIONS_MAX]
    
    return options

# required_permissions

parse_required_permissions = flag_parser_factory('default_member_permissions', Permission)


def put_required_permissions_into(required_permissions, data, defaults):
    """
    Puts the given application command's required permissions into the given data.
    
    Parameters
    ----------
    required_permissions : ``Permission``
        The required permissions a user should have to use the command.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if required_permissions:
        required_permissions = format(required_permissions, 'd')
    else:
        required_permissions = None
    data['default_member_permissions'] = required_permissions
    return data


validate_required_permissions = flag_validator_factory('required_permissions', Permission)

# target_type

parse_target_type = preinstanced_parser_factory(
    'type', ApplicationCommandTargetType, ApplicationCommandTargetType.none
)
put_target_type_into = preinstanced_putter_factory('type')
validate_target_type = preinstanced_validator_factory('target_type', ApplicationCommandTargetType)

# version

parse_version = entity_id_parser_factory('version')
put_version_into = entity_id_optional_putter_factory('version')
validate_version = entity_id_validator_factory('version')
