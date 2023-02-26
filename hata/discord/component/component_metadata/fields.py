__all__ = ()

from scarletio import include

from ...channel import ChannelType
from ...field_parsers import (
    bool_parser_factory, int_parser_factory, negated_bool_parser_factory, nullable_object_array_parser_factory,
    nullable_string_parser_factory, preinstanced_array_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, int_optional_putter_factory, negated_bool_optional_putter_factory,
    nullable_entity_array_putter_factory, nullable_string_optional_putter_factory, preinstanced_array_putter_factory,
    preinstanced_putter_factory, url_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, int_conditional_validator_factory, nullable_object_array_validator_factory,
    nullable_string_validator_factory, preinstanced_array_validator_factory, preinstanced_validator_factory,
    url_optional_validator_factory
)

from ..string_select_option import StringSelectOption

from .constants import (
    BUTTON_STYLE_DEFAULT, LABEL_LENGTH_MAX, MAX_LENGTH_DEFAULT, MAX_LENGTH_MAX, MAX_LENGTH_MIN, MAX_VALUES_DEFAULT,
    MAX_VALUES_MAX, MAX_VALUES_MIN, MIN_LENGTH_DEFAULT, MIN_LENGTH_MAX, MIN_LENGTH_MIN, MIN_VALUES_DEFAULT,
    MIN_VALUES_MAX, MIN_VALUES_MIN, PLACEHOLDER_LENGTH_MAX, TEXT_INPUT_STYLE_DEFAULT, VALUE_LENGTH_MAX
)
from .preinstanced import ButtonStyle, TextInputStyle


Component = include('Component')

# button_style

parse_button_style = preinstanced_parser_factory('style', ButtonStyle, BUTTON_STYLE_DEFAULT)
put_button_style_into = preinstanced_putter_factory('style')
validate_button_style = preinstanced_validator_factory('button_style', ButtonStyle)

# channel_types

parse_channel_types = preinstanced_array_parser_factory('channel_types', ChannelType)
put_channel_types_into = preinstanced_array_putter_factory('channel_types')
validate_channel_types = preinstanced_array_validator_factory('channel_types', ChannelType)

# enabled

parse_enabled = negated_bool_parser_factory('disabled', True)
put_enabled_into = negated_bool_optional_putter_factory('disabled', True)
validate_enabled = bool_validator_factory('enabled', True)

# label

parse_label = nullable_string_parser_factory('label')
put_label_into = nullable_string_optional_putter_factory('label')
validate_label = nullable_string_validator_factory('label', 0, LABEL_LENGTH_MAX)

# max_length

parse_max_length = int_parser_factory('max_length', MAX_LENGTH_DEFAULT)
put_max_length_into = int_optional_putter_factory('max_length', MAX_LENGTH_DEFAULT)
validate_max_length = int_conditional_validator_factory(
    'max_length',
    MAX_LENGTH_MIN,
    (lambda user_limit: user_limit >= MAX_LENGTH_MIN and user_limit <= MAX_LENGTH_MAX),
    f'>= {MAX_LENGTH_MIN} and <= {MAX_LENGTH_MAX},'
)

# max_values

parse_max_values = int_parser_factory('max_values', MAX_VALUES_DEFAULT)
put_max_values_into = int_optional_putter_factory('max_values', MAX_VALUES_DEFAULT)
validate_max_values = int_conditional_validator_factory(
    'max_values',
    MAX_VALUES_MIN,
    (lambda user_limit: user_limit >= MAX_VALUES_MIN and user_limit <= MAX_VALUES_MAX),
    f'>= {MAX_VALUES_MIN} and <= {MAX_VALUES_MAX},'
)

# min_length

parse_min_length = int_parser_factory('min_length', MIN_LENGTH_DEFAULT)
put_min_length_into = int_optional_putter_factory('min_length', MIN_LENGTH_DEFAULT)
validate_min_length = int_conditional_validator_factory(
    'min_length',
    MIN_LENGTH_MIN,
    (lambda user_limit: user_limit >= MIN_LENGTH_MIN and user_limit <= MIN_LENGTH_MAX),
    f'>= {MIN_LENGTH_MIN} and <= {MIN_LENGTH_MAX},'
)

# min_values

parse_min_values = int_parser_factory('min_values', MIN_VALUES_DEFAULT)
put_min_values_into = int_optional_putter_factory('min_values', MIN_VALUES_DEFAULT)
validate_min_values = int_conditional_validator_factory(
    'min_values',
    MIN_VALUES_MIN,
    (lambda user_limit: user_limit >= MIN_VALUES_MIN and user_limit <= MIN_VALUES_MAX),
    f'>= {MIN_VALUES_MIN} and <= {MIN_VALUES_MAX},'
)

# options

parse_options = nullable_object_array_parser_factory('options', StringSelectOption)
put_options_into = nullable_entity_array_putter_factory('options', StringSelectOption)
validate_options = nullable_object_array_validator_factory('options', StringSelectOption)

# placeholder

parse_placeholder = nullable_string_parser_factory('placeholder')
put_placeholder_into = nullable_string_optional_putter_factory('placeholder')
validate_placeholder = nullable_string_validator_factory('placeholder', 0, PLACEHOLDER_LENGTH_MAX)

# required

parse_required = bool_parser_factory('required', True)
put_required_into = bool_optional_putter_factory('required', True)
validate_required = bool_validator_factory('required', True)

# text_input_style

parse_text_input_style = preinstanced_parser_factory('style', TextInputStyle, TEXT_INPUT_STYLE_DEFAULT)
put_text_input_style_into = preinstanced_putter_factory('style')
validate_text_input_style = preinstanced_validator_factory('text_input_style', TextInputStyle)

# url

parse_url = nullable_string_parser_factory('url')
put_url_into = url_optional_putter_factory('url')
validate_url = url_optional_validator_factory('url')

# value

parse_value = nullable_string_parser_factory('value')
put_value_into = nullable_string_optional_putter_factory('value')
validate_value = nullable_string_validator_factory('value', 0, VALUE_LENGTH_MAX)
