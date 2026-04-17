__all__ = ()

from ..onboarding_prompt.fields import put_id as put_prompt_id

from .fields import (
    put_default_channel_ids, put_enabled, put_mode, put_prompts, validate_default_channel_ids,
    validate_enabled, validate_mode, validate_prompts
)


ONBOARDING_FIELD_CONVERTERS = {
    'default_channel_ids': (validate_default_channel_ids, put_default_channel_ids),
    'enabled': (validate_enabled, put_enabled),
    'mode': (validate_mode, put_mode),
    'prompts': (validate_prompts, put_prompts),
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


def populate_prompt_ids_in_onboarding_screen_prompt_options(data, onboarding_screen_template):
    """
    Populates prompt identifiers in onboarding screen's prompts' options' emojis' datas.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Onboarding prompt data.
    
    onboarding_screen_template : `None | OnboardingScreen`
        Onboarding screen used as a template.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    prompt_datas = data.get('prompts', None)
    if (prompt_datas is not None):
        assign_ids_for = [*prompt_datas]
        
        if onboarding_screen_template is None:
            prompts = None
        else:
            prompts = onboarding_screen_template.prompts
            
        if (prompts is not None):
            for prompt in reversed(prompts):
                if not prompt.id:
                    continue
                
                prompt_data_to_match = prompt.to_data(defaults = True)
                
                for index in reversed(range(len(assign_ids_for))):
                    prompt_data = assign_ids_for[index]
                    if prompt_data != prompt_data_to_match:
                        continue
                    
                    del assign_ids_for[index]
                    put_prompt_id(prompt.id, prompt_data, True)
                    break
        
        for generated_identifier, prompt_data in enumerate(assign_ids_for, 1 << 22):
            put_prompt_id(generated_identifier, prompt_data, True)
    
    return data
