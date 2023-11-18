__all__ = ()

from ...onboarding import OnboardingMode, OnboardingPrompt
from ...onboarding.onboarding_screen.fields import (
    validate_default_channel_ids, validate_enabled, validate_mode, validate_prompts
)

from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..audit_log_entry_change_conversion.change_deserializers import change_deserializer_deprecation
from ..conversion_helpers.converters import value_deserializer_ids, value_serializer_ids


# ---- below_requirements ---- 

BELOW_REQUIREMENTS_CONVERSION_IGNORED = AuditLogEntryChangeConversion(
    ('below_requirements',),
    '',
    change_deserializer = change_deserializer_deprecation,
)


# ---- default_channel_ids ----

DEFAULT_CHANNEL_IDS_CONVERSION = AuditLogEntryChangeConversion(
    ('default_channel_ids',),
    'default_channel_ids',
    value_deserializer = value_deserializer_ids,
    value_serializer = value_serializer_ids,
    value_validator = validate_default_channel_ids,
)


# ---- enabled ----

ENABLED_CONVERSION = AuditLogEntryChangeConversion(
    ('enabled',),
    'enabled',
    value_validator = validate_enabled,
)


@ENABLED_CONVERSION.set_value_deserializer
def enabled_value_deserializer(value):
    if value is None:
        value = True
    return value


# ---- mode ----

MODE_CONVERSION = AuditLogEntryChangeConversion(
    ('mode',),
    'mode',
    value_validator = validate_mode,
)


@MODE_CONVERSION.set_value_deserializer
def mode_value_deserializer(value):
    return OnboardingMode.get(value)


@MODE_CONVERSION.set_value_serializer
def mode_value_serializer(value):
    return value.value


# ---- prompts ----

PROMPTS_CONVERSION = AuditLogEntryChangeConversion(
    ('prompts',),
    'prompts',
    value_validator = validate_prompts,
)


@PROMPTS_CONVERSION.set_value_deserializer
def prompts_value_deserializer(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*(OnboardingPrompt.from_data(data) for data in value),)
    
    return value


@PROMPTS_CONVERSION.set_value_serializer
def prompts_value_serializer(value):
    if value is None:
        value = []
    else:
        value = [prompt.to_data(defaults = True, include_internals = True) for prompt in value]
    
    return value


# ---- Construct ----

ONBOARDING_SCREEN_CONVERSIONS = AuditLogEntryChangeConversionGroup(
    BELOW_REQUIREMENTS_CONVERSION_IGNORED,
    DEFAULT_CHANNEL_IDS_CONVERSION,
    ENABLED_CONVERSION,
    MODE_CONVERSION,
    PROMPTS_CONVERSION,
)
