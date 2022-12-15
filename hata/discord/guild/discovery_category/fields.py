__all__ = ()

from functools import partial as partial_func

from ...field_parsers import (
    bool_parser_factory, force_string_parser_factory, int_parser_factory, nullable_functional_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, force_string_putter_factory, int_putter_factory,
    nullable_functional_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, force_string_validator_factory, int_conditional_validator_factory
)
from ...localization.helpers import localized_dictionary_builder
from ...localization.utils import build_locale_dictionary, destroy_locale_dictionary

# value

parse_value = int_parser_factory('id', 0)
put_value_into = int_putter_factory('id')
validate_value = int_conditional_validator_factory(
    'value',
    0,
    lambda value : value >= 0,
    '>= 0',
)

# name

parse_name = force_string_parser_factory('name')
put_name_into = force_string_putter_factory('name')
validate_name = force_string_validator_factory('name', 0, 10024)

# name_localizations

parse_name_localizations = nullable_functional_parser_factory(
    'name_localizations', build_locale_dictionary
)
put_name_localizations_into = nullable_functional_optional_putter_factory(
    'name_localizations', destroy_locale_dictionary
)
validate_name_localizations = partial_func(localized_dictionary_builder, parameter_name = 'name_localizations')

# primary

parse_primary = bool_parser_factory('is_primary', False)
put_primary_into = bool_optional_putter_factory('is_primary', False)
validate_primary = bool_validator_factory('primary')

# Ignore additional fields:
# 
# - is_published
# - reasons_to_join
# - social_links
# - about
#
# When looking at guild discovery only `is_published` shows up, but not sure what it does.
# The rest is not even showing up, so they seem to be unused?
