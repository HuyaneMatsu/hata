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
    user_id = 202304040015
    
    voice_channel_effect = VoiceChannelEffect(
        animation_id = animation_id,
        animation_type = animation_type,
        channel_id = channel_id,
        emoji = emoji,
        guild_id = guild_id,
        user_id = user_id,
    )
    
    vampytest.assert_instance(repr(voice_channel_effect), str)


def test__VoiceChannelEffect__eq():
    """
    Tests whether ``VoiceChannelEffect.__repr__`` works as intended.
    """
    animation_id = 202304040012
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040013
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040014
    user_id = 202304040015
    
    keyword_parameters = {
        'animation_id': animation_id,
        'animation_type': animation_type,
        'channel_id': channel_id,
        'emoji': emoji,
        'guild_id': guild_id,
        'user_id': user_id,
    }
    
    voice_channel_effect_original = VoiceChannelEffect(**keyword_parameters)
    
    vampytest.assert_eq(voice_channel_effect_original, voice_channel_effect_original)
    
    for voice_channel_effect_name, voice_channel_effect_value in (
        ('animation_id', 202304040016),
        ('animation_type', VoiceChannelEffectAnimationType.premium),
        ('channel_id', 202304040017),
        ('emoji', BUILTIN_EMOJIS['heart']),
        ('guild_id', 202304040018),
        ('user_id', 202304040019),
    ):
        voice_channel_effect_altered = VoiceChannelEffect(**{**keyword_parameters, voice_channel_effect_name: voice_channel_effect_value})
        vampytest.assert_ne(voice_channel_effect_original, voice_channel_effect_altered)


def test__VoiceChannelEffect__hash():
    """
    Tests whether ``VoiceChannelEffect.__hash__`` works as intended.
    """
    animation_id = 202304040020
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040021
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040022
    user_id = 202304040023
    
    voice_channel_effect = VoiceChannelEffect(
        animation_id = animation_id,
        animation_type = animation_type,
        channel_id = channel_id,
        emoji = emoji,
        guild_id = guild_id,
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
    user_id = 202304040027
    
    voice_channel_effect = VoiceChannelEffect(
        animation_id = animation_id,
        animation_type = animation_type,
        channel_id = channel_id,
        emoji = emoji,
        guild_id = guild_id,
        user_id = user_id,
    )
    
    vampytest.assert_eq(len([*voice_channel_effect]), len(voice_channel_effect))
