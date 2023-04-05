__all__ = ()

from ...onboarding import OnboardingPrompt

from ..audit_log_change import AuditLogChange

from .shared import convert_nothing, convert_snowflake_array


def convert_prompts(name, data):
    before = data.get('old_value', None)
    if (before is not None):
        if before:
            before = (*(OnboardingPrompt.from_data(data) for data in before),)
        else:
            before = None
    
    after = data.get('new_value', None)
    if (after is not None):
        if after:
            after = (*(OnboardingPrompt.from_data(data) for data in after),)
        else:
            after = None
    
    return AuditLogChange('actions', before, after)


ONBOARDING_SCREEN_CONVERTERS = {
    'default_channel_ids': convert_snowflake_array,
    'enabled': convert_nothing,
    'prompts': convert_prompts,
}
