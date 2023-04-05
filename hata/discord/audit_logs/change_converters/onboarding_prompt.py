__all__ = ()

from ...onboarding import OnboardingPromptOption, OnboardingPromptType

from ..audit_log_change import AuditLogChange

from .shared import _convert_preinstanced, convert_nothing, convert_snowflake


def convert_str__name(name, data):
    return convert_nothing('name', data)


def convert_options(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        if before:
            before = (*(OnboardingPromptOption.from_data(data) for data in before),)
        else:
            before = None
    
    after = data.get('new_value', None)
    if (after is not None):
        if after:
            after = (*(OnboardingPromptOption.from_data(data) for data in after),)
        else:
            after = None
    
    return AuditLogChange('actions', before, after)


def convert_channel_type(name, data):
    return _convert_preinstanced('type', data, OnboardingPromptType)


ONBOARDING_PROMPT_CONVERTERS = {
    'id': convert_snowflake,
    'in_onboarding': convert_nothing,
    'title': convert_str__name,
    'options': convert_options,
    'required': convert_nothing,
    'single_select': convert_nothing,
    'type': convert_channel_type,
}
