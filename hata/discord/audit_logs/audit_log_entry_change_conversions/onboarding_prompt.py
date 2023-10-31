__all__ = ()

from ...onboarding import OnboardingPromptOption, OnboardingPromptType
from ...onboarding.onboarding_prompt.fields import (
    validate_in_onboarding, validate_name, validate_options, validate_required, validate_single_select, validate_type
)

from ..audit_log_change.flags import FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import get_converter_name, put_converter_name


# ---- in_onboarding ----

IN_ONBOARDING_CONVERSION = AuditLogEntryChangeConversion(
    'in_onboarding',
    'in_onboarding',
    FLAG_IS_MODIFICATION,
    validator = validate_in_onboarding,
)


@IN_ONBOARDING_CONVERSION.set_get_converter
def in_onboarding_get_converter(value):
    if value is None:
        value = False
    return value


# ---- name ----

NAME_CONVERSION = AuditLogEntryChangeConversion(
    'title',
    'name',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_name,
    put_converter = put_converter_name,
    validator = validate_name,
)


# ---- options ----

OPTIONS_CONVERSION = AuditLogEntryChangeConversion(
    'options',
    'options',
    FLAG_IS_MODIFICATION,
    validator = validate_options,
)


@OPTIONS_CONVERSION.set_get_converter
def options_get_converter(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*(OnboardingPromptOption.from_data(data) for data in value),)
    
    return value


@OPTIONS_CONVERSION.set_put_converter
def options_put_converter(value):
    if value is None:
        value = []
    else:
        value = [option.to_data(defaults = True, include_internals = True) for option in value]
    
    return value


# ---- required ----

REQUIRED_CONVERSION = AuditLogEntryChangeConversion(
    'required',
    'required',
    FLAG_IS_MODIFICATION,
    validator = validate_required,
)


@REQUIRED_CONVERSION.set_get_converter
def required_get_converter(value):
    if value is None:
        value = False
    return value


# ---- single_select ----

SINGLE_SELECT_CONVERSION = AuditLogEntryChangeConversion(
    'single_select',
    'single_select',
    FLAG_IS_MODIFICATION,
    validator = validate_single_select,
)


@SINGLE_SELECT_CONVERSION.set_get_converter
def single_select_get_converter(value):
    if value is None:
        value = False
    return value


# ---- type ----

TYPE_CONVERSION = AuditLogEntryChangeConversion(
    'type',
    'type',
    FLAG_IS_MODIFICATION,
    validator = validate_type,
)


@TYPE_CONVERSION.set_get_converter
def type_get_converter(value):
    return OnboardingPromptType.get(value)


@TYPE_CONVERSION.set_put_converter
def type_put_converter(value):
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
