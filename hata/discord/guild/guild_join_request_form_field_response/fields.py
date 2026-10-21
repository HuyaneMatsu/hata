__all__ = ()

from ...fields.field_parsers import (
    bool_parser_factory, int_parser_factory, nullable_array_parser_factory, nullable_string_parser_factory,
    preinstanced_parser_factory
)
from ...fields.field_putters import (
    force_bool_putter_factory, int_optional_putter_factory, nullable_string_array_optional_putter_factory,
    nullable_string_optional_putter_factory, preinstanced_putter_factory
)
from ...fields.field_validators import (
    bool_validator_factory, int_conditional_validator_factory, nullable_string_array_validator_factory,
    nullable_string_validator_factory, preinstanced_validator_factory
)
from ...fields.fields_common import (
    parse_description, parse_placeholder, parse_required, parse_title__from_label as parse_title,
    put_description__optional as put_description, put_placeholder__optional as put_placeholder, put_required,
    put_title__to_label as put_title, validate_description__range_0_1024 as validate_description,
    validate_placeholder__range_0_1024 as validate_placeholder, validate_required,
    validate_title__range_0_1024 as validate_title
)

from .preinstanced import GuildJoinRequestFormFieldTextInputStyle, GuildJoinRequestFormFieldType


# accepted

parse_accepted = bool_parser_factory('response', True)
put_accepted = force_bool_putter_factory('response')
validate_accepted = bool_validator_factory('accepted', True)


# choices

parse_choices = nullable_array_parser_factory('choices')
put_choices = nullable_string_array_optional_putter_factory('choices')
validate_choices = nullable_string_array_validator_factory('choices')


# terms

parse_terms = nullable_array_parser_factory('values')
put_terms = nullable_string_array_optional_putter_factory('values')
validate_terms = nullable_string_array_validator_factory('terms')

# text_input_style

validate_text_input_style = preinstanced_validator_factory('text_input_style', GuildJoinRequestFormFieldTextInputStyle)

# type

parse_type = preinstanced_parser_factory('type', GuildJoinRequestFormFieldType, GuildJoinRequestFormFieldType.none)
put_type = preinstanced_putter_factory('type')

# value

parse_value = nullable_string_parser_factory('response')
put_value = nullable_string_optional_putter_factory('response')
validate_value = nullable_string_validator_factory('value', 0, 1024)


# choice_index

parse_choice_index = int_parser_factory('response', -1)
put_choice_index = int_optional_putter_factory('response', -1)
validate_choice_index = int_conditional_validator_factory(
    'choice_index',
    -1,
    (lambda choice_index : choice_index >= -1),
    '>= 0',
)
