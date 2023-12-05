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


# https://github.com/discord/discord-api-docs/pull/6479
def flatten_emoji_data_in_onboarding_screen_prompt_options(data):
    """
    Flattens an onboarding screen's prompts' options' emojis' datas.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Onboarding prompt data.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    prompt_datas = data.get('prompts', None)
    if (prompt_datas is not None):
        for prompt_data in prompt_datas:
            option_datas = prompt_data.get('options', None)
            if (option_datas is None):
                continue
            
            for option_data in option_datas:
                try:
                    emoji_data = option_data.pop('emoji')
                except KeyError:
                    continue
                
                if emoji_data is None:
                    option_data['emoji_name'] = None
                    continue
                
                for key, value in emoji_data.items():
                    option_data['emoji_' + key] = value

    return data
