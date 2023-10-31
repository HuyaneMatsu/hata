__all__ = ()

from ...onboarding import OnboardingMode, OnboardingPrompt
from ...onboarding.onboarding_screen.fields import (
    validate_default_channel_ids, validate_enabled, validate_mode, validate_prompts
)

from ..audit_log_change.flags import FLAG_IS_IGNORED, FLAG_IS_MODIFICATION
from ..audit_log_entry_change_conversion import AuditLogEntryChangeConversion, AuditLogEntryChangeConversionGroup
from ..conversion_helpers.converters import get_converter_ids, put_converter_ids


# ---- below_requirements ---- 

BELOW_REQUIREMENTS_CONVERSION_IGNORED = AuditLogEntryChangeConversion(
    'below_requirements',
    '',
    FLAG_IS_IGNORED,
)


# ---- default_channel_ids ----

DEFAULT_CHANNEL_IDS_CONVERSION = AuditLogEntryChangeConversion(
    'default_channel_ids',
    'default_channel_ids',
    FLAG_IS_MODIFICATION,
    get_converter = get_converter_ids,
    put_converter = put_converter_ids,
    validator = validate_default_channel_ids,
)


# ---- enabled ----

ENABLED_CONVERSION = AuditLogEntryChangeConversion(
    'enabled',
    'enabled',
    FLAG_IS_MODIFICATION,
    validator = validate_enabled,
)


@ENABLED_CONVERSION.set_get_converter
def enabled_get_converter(value):
    if value is None:
        value = True
    return value


# ---- mode ----

MODE_CONVERSION = AuditLogEntryChangeConversion(
    'mode',
    'mode',
    FLAG_IS_MODIFICATION,
    validator = validate_mode,
)


@MODE_CONVERSION.set_get_converter
def mode_get_converter(value):
    return OnboardingMode.get(value)


@MODE_CONVERSION.set_put_converter
def mode_put_converter(value):
    return value.value



# ---- prompts ----

PROMPTS_CONVERSION = AuditLogEntryChangeConversion(
    'prompts',
    'prompts',
    FLAG_IS_MODIFICATION,
    validator = validate_prompts,
)


@PROMPTS_CONVERSION.set_get_converter
def prompts_get_converter(value):
    if value is None:
        pass
    elif (not value):
        value = None
    else:
        value = (*(OnboardingPrompt.from_data(data) for data in value),)
    
    return value


@PROMPTS_CONVERSION.set_put_converter
def prompts_put_converter(value):
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
