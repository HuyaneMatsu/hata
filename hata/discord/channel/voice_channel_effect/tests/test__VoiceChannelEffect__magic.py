import vampytest

from ....core import BUILTIN_EMOJIS

from ..preinstanced import VoiceChannelEffectAnimationType
from ..voice_channel_effect import VoiceChannelEffect


def test__VoiceChannelEffect__repr():
    """
    Tests whether ``VoiceChannelEffect.__repr__`` works as intended.
    """
    animation_id = 202304040012
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040013
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040014
    sound_id = 202408180006
    sound_volume = 0.5
    user_id = 202304040015
    
    voice_channel_effect = VoiceChannelEffect(
        animation_id = animation_id,
        animation_type = animation_type,
        channel_id = channel_id,
        emoji = emoji,
        guild_id = guild_id,
        sound_id = sound_id,
        sound_volume = sound_volume,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(voice_channel_effect), str)


def _iter_options__eq():
    animation_id = 202304040012
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040013
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040014
    sound_id = 202408180007
    sound_volume = 0.5
    user_id = 202304040015
    
    keyword_parameters = {
        'animation_id': animation_id,
        'animation_type': animation_type,
        'channel_id': channel_id,
        'emoji': emoji,
        'guild_id': guild_id,
        'sound_id': sound_id,
        'sound_volume': sound_volume,
        'user_id': user_id,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'animation_id': 202304040016,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'animation_type': VoiceChannelEffectAnimationType.premium,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'channel_id': 202304040017,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'emoji': BUILTIN_EMOJIS['heart'],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild_id': 202304040018,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sound_id': 202408180008,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sound_volume': 0.6,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user_id': 202304040019,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__GuildProfile__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``VoiceChannelEffect.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<object, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    voice_channel_effect_0 = VoiceChannelEffect(**keyword_parameters_0)
    voice_channel_effect_1 = VoiceChannelEffect(**keyword_parameters_1)
    
    output = voice_channel_effect_0 == voice_channel_effect_1
    vampytest.assert_instance(output, bool)
    return output


def test__VoiceChannelEffect__hash():
    """
    Tests whether ``VoiceChannelEffect.__hash__`` works as intended.
    """
    animation_id = 202304040020
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040021
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040022
    sound_id = 202408180009
    sound_volume = 0.5
    user_id = 202304040023
    
    voice_channel_effect = VoiceChannelEffect(
        animation_id = animation_id,
        animation_type = animation_type,
        channel_id = channel_id,
        emoji = emoji,
        guild_id = guild_id,
        sound_id = sound_id,
        sound_volume = sound_volume,
        user_id = user_id,
    )
    
    vampytest.assert_instance(hash(voice_channel_effect), int)


def test__VoiceChannelEffect__unpack():
    """
    Tests whether ``VoiceChannelEffect`` unpacking works as intended.
    """
    animation_id = 202304040024
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040025
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040026
    sound_id = 202408180010
    sound_volume = 0.5
    user_id = 202304040027
    
    voice_channel_effect = VoiceChannelEffect(
        animation_id = animation_id,
        animation_type = animation_type,
        channel_id = channel_id,
        emoji = emoji,
        guild_id = guild_id,
        sound_id = sound_id,
        sound_volume = sound_volume,
        user_id = user_id,
    )
    
    vampytest.assert_eq(len([*voice_channel_effect]), len(voice_channel_effect))
