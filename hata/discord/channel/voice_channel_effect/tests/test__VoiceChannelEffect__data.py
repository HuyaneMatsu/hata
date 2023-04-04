import vampytest

from ....core import BUILTIN_EMOJIS

from ..preinstanced import VoiceChannelEffectAnimationType
from ..voice_channel_effect import VoiceChannelEffect

from .test__VoiceChannelEffect__constructor import _assert_fields_set


def test__VoiceChannelEffect__from_data__0():
    """
    Tests whether ``VoiceChannelEffect.from_data`` works as intended.
    
    Case: all voice_channel_effects given.
    """
    animation_id = 202304040004
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040005
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040006
    user_id = 202304040007
    
    data = {
        'animation_id': str(animation_id),
        'animation_type': animation_type.value,
        'channel_id': str(channel_id),
        'emoji': {'name': emoji.unicode},
        'guild_id': str(guild_id),
        'user_id': str(user_id),
    }
    
    voice_channel_effect = VoiceChannelEffect.from_data(data)
    _assert_fields_set(voice_channel_effect)
    
    vampytest.assert_eq(voice_channel_effect.animation_id, animation_id)
    vampytest.assert_is(voice_channel_effect.animation_type, animation_type)
    vampytest.assert_eq(voice_channel_effect.channel_id, channel_id)
    vampytest.assert_is(voice_channel_effect.emoji, emoji)
    vampytest.assert_eq(voice_channel_effect.guild_id, guild_id)
    vampytest.assert_eq(voice_channel_effect.user_id, user_id)


def test__VoiceChannelEffect__to_data__0():
    """
    Tests whether ``VoiceChannelEffect.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    animation_id = 202304040008
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040009
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040010
    user_id = 202304040011
    
    voice_channel_effect = VoiceChannelEffect(
        animation_id = animation_id,
        animation_type = animation_type,
        channel_id = channel_id,
        emoji = emoji,
        guild_id = guild_id,
        user_id = user_id,
    )
    
    expected_output = {
        'animation_id': str(animation_id),
        'animation_type': animation_type.value,
        'channel_id': str(channel_id),
        'emoji': {'name': emoji.unicode},
        'guild_id': str(guild_id),
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        voice_channel_effect.to_data(defaults = True, include_internals = True),
        expected_output,
    )
