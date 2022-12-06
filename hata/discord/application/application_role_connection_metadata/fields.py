__all__ = ()

from functools import partial as partial_func

from ...field_parsers import (
    force_string_parser_factory, nullable_functional_parser_factory, nullable_string_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    force_string_putter_factory, nullable_functional_optional_putter_factory, nullable_string_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    force_string_validator_factory, nullable_string_validator_factory, preinstanced_validator_factory
)
from ...localization.helpers import localized_dictionary_builder
from ...localization.utils import build_locale_dictionary, destroy_locale_dictionary

from .constants import (
    DESCRIPTION_LENGTH_MAX, DESCRIPTION_LENGTH_MIN, KEY_LENGTH_MAX, KEY_LENGTH_MIN, NAME_LENGTH_MAX, NAME_LENGTH_MIN
)
from .preinstanced import ApplicationRoleConnectionMetadataType

# description 

parse_description = nullable_string_parser_factory('description')
put_description_into = nullable_string_putter_factory('description')
validate_description = nullable_string_validator_factory('description', DESCRIPTION_LENGTH_MIN, DESCRIPTION_LENGTH_MAX)

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

# key 

parse_key = force_string_parser_factory('key')
put_key_into = force_string_putter_factory('key')
validate_key = force_string_validator_factory('key', KEY_LENGTH_MIN, KEY_LENGTH_MAX)

# name 

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', NAME_LENGTH_MIN, NAME_LENGTH_MAX)

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

# type

parse_type = preinstanced_parser_factory(
    'type', ApplicationRoleConnectionMetadataType, ApplicationRoleConnectionMetadataType.none
)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('type', ApplicationRoleConnectionMetadataType)
