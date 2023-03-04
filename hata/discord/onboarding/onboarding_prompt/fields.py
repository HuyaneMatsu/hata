__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, force_string_parser_factory, nullable_object_array_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    entity_id_putter_factory, force_bool_putter_factory, force_string_putter_factory,
    nullable_entity_array_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_validator_factory, force_string_validator_factory,
    nullable_object_array_validator_factory, preinstanced_validator_factory
)

from ..onboarding_prompt_option import OnboardingPromptOption

from .preinstanced import OnboardingPromptType

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('option_id')

# in_onboarding

parse_in_onboarding = bool_parser_factory('in_onboarding', False)
put_in_onboarding_into = force_bool_putter_factory('in_onboarding')
validate_in_onboarding = bool_validator_factory('in_onboarding', False)

# name

parse_name = force_string_parser_factory('title')
put_name_into = force_string_putter_factory('title')
validate_name = force_string_validator_factory('name', 0, 1024)

# options

parse_options = nullable_object_array_parser_factory('options', OnboardingPromptOption)
put_options_into = nullable_entity_array_putter_factory('options', OnboardingPromptOption)
validate_options = nullable_object_array_validator_factory('options', OnboardingPromptOption)

# required

parse_required = bool_parser_factory('required', False)
put_required_into = force_bool_putter_factory('required')
validate_required = bool_validator_factory('required', False)

# single_select

parse_single_select = bool_parser_factory('single_select', False)
put_single_select_into = force_bool_putter_factory('single_select')
validate_single_select = bool_validator_factory('single_select', False)

# type

parse_type = preinstanced_parser_factory('type', OnboardingPromptType, OnboardingPromptType.multiple_choice)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('prompt_type', OnboardingPromptType)
