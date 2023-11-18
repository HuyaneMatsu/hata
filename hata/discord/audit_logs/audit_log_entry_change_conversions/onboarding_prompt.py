__all__ = ()

from ...onboarding import OnboardingPromptOption, OnboardingPromptType
from ...onboarding.onboarding_prompt.fields import (
    validate_in_onboarding, validate_name, validate_options, validate_required, validate_single_select, validate_type
)

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import value_deserializer_name, value_serializer_name


# ---- in_onboarding ----

IN_ONBOARDING_CONVERSION = AuditLogEntryChangeConversion(
    ('in_onboarding',),
    'in_onboarding',
    value_validator = validate_in_onboarding,
)


@IN_ONBOARDING_CONVERSION.set_value_deserializer
def in_onboarding_value_deserializer(value):
    if value is None:
        value = False
    return value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    ('title',),
    'name',
    value_deserializer = value_deserializer_name,
    value_serializer = value_serializer_name,
    value_validator = validate_name,
)


# ---- options ----

OPTIONS_CONVERSION = AuditLogEntryChangeConversion(
    ('options',),
    'options',
    value_validator = validate_options,
)


@OPTIONS_CONVERSION.set_value_deserializer
def options_value_deserializer(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*(OnboardingPromptOption.from_data(data) for data in value),)
    
    return value


@OPTIONS_CONVERSION.set_value_serializer
def options_value_serializer(value):
    if value is None:
        value = []
    else:
        value = [option.to_data(defaults = True, include_internals = True) for option in value]
    
    return value


# ---- required ----

REQUIRED_CONVERSION = AuditLogEntryChangeConversion(
    ('required',),
    'required',
    value_validator = validate_required,
)


@REQUIRED_CONVERSION.set_value_deserializer
def required_value_deserializer(value):
    if value is None:
        value = False
    return value


# ---- single_select ----

SINGLE_SELECT_CONVERSION = AuditLogEntryChangeConversion(
    ('single_select',),
    'single_select',
    value_validator = validate_single_select,
)


@SINGLE_SELECT_CONVERSION.set_value_deserializer
def single_select_value_deserializer(value):
    if value is None:
        value = False
    return value


# ---- type ----

TYPE_CONVERSION = AuditLogEntryChangeConversion(
    ('type',),
    'type',
    value_validator = validate_type,
)


@TYPE_CONVERSION.set_value_deserializer
def type_value_deserializer(value):
    return OnboardingPromptType.get(value)


@TYPE_CONVERSION.set_value_serializer
def type_value_serializer(value):
    return value.value


# ---- Construct ----

ONBOARDING_PROMPT_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    IN_ONBOARDING_CONVERSION,
    NAME_CONVERSION,
    OPTIONS_CONVERSION,
    REQUIRED_CONVERSION,
    SINGLE_SELECT_CONVERSION,
    TYPE_CONVERSION,
)
