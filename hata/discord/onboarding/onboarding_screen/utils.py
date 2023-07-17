__all__ = ()


from .fields import (
    put_default_channel_ids_into, put_enabled_into, put_mode_into, put_prompts_into, validate_default_channel_ids,
    validate_enabled, validate_mode, validate_prompts
)


ONBOARDING_FIELD_CONVERTERS = {
    'default_channel_ids': (validate_default_channel_ids, put_default_channel_ids_into),
    'enabled': (validate_enabled, put_enabled_into),
    'mode': (validate_mode, put_mode_into),
    'prompts': (validate_prompts, put_prompts_into),
}
