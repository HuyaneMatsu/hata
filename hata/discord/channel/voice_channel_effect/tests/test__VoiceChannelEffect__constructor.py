import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..preinstanced import VoiceChannelEffectAnimationType
from ..voice_channel_effect import VoiceChannelEffect


def _assert_fields_set(voice_channel_effect):
    """
    Checks whether every attribute is set of the given voice channel effect.
    
    Parameters
    ----------
    voice_channel_effect : ``VoiceChannelEffect``
        The voice channel effect to check.
    """
    vampytest.assert_instance(voice_channel_effect, VoiceChannelEffect)
    vampytest.assert_instance(voice_channel_effect.animation_id, int)
    vampytest.assert_instance(voice_channel_effect.animation_type, VoiceChannelEffectAnimationType)
    vampytest.assert_instance(voice_channel_effect.channel_id, int)
    vampytest.assert_instance(voice_channel_effect.emoji, Emoji, nullable = True)
    vampytest.assert_instance(voice_channel_effect.guild_id, int)
    vampytest.assert_instance(voice_channel_effect.sound_id, int)
    vampytest.assert_instance(voice_channel_effect.sound_volume, float)
    vampytest.assert_instance(voice_channel_effect.user_id, int)


def test__VoiceChannelEffect__new__no_fields():
    """
    Tests whether ``VoiceChannelEffect.__new__`` works as intended.
    
    Case: No fields given.
    """
    voice_channel_effect = VoiceChannelEffect()
    _assert_fields_set(voice_channel_effect)


def test__VoiceChannelEffect__new__all_fields():
    """
    Tests whether ``VoiceChannelEffect.__new__`` works as intended.
    
    Case: All fields given.
    """
    animation_id = 202304040000
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040001
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040002
    sound_id = 202408180003
    sound_volume = 0.5
    user_id = 202304040003
    
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
    _assert_fields_set(voice_channel_effect)
    
    vampytest.assert_eq(voice_channel_effect.animation_id, animation_id)
    vampytest.assert_is(voice_channel_effect.animation_type, animation_type)
    vampytest.assert_eq(voice_channel_effect.channel_id, channel_id)
    vampytest.assert_is(voice_channel_effect.emoji, emoji)
    vampytest.assert_eq(voice_channel_effect.guild_id, guild_id)
    vampytest.assert_eq(voice_channel_effect.sound_id, sound_id)
    vampytest.assert_eq(voice_channel_effect.sound_volume, sound_volume)
    vampytest.assert_eq(voice_channel_effect.user_id, user_id)
