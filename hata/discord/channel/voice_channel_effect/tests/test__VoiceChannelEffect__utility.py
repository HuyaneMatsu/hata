import vampytest

from ....core import BUILTIN_EMOJIS
from ....guild import Guild
from ....soundboard import SoundboardSound
from ....user import ClientUserBase, User

from ...channel import Channel

from ..preinstanced import VoiceChannelEffectAnimationType
from ..voice_channel_effect import VoiceChannelEffect

from .test__VoiceChannelEffect__constructor import _assert_fields_set


def test__VoiceChannelEffect__copy():
    """
    Tests whether ``VoiceChannelEffect.copy`` works as intended.
    """
    animation_id = 202304040028
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040029
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040030
    sound_id = 202408180011
    sound_volume = 0.5
    user_id = 202304040031
    
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
    
    copy = voice_channel_effect.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(voice_channel_effect, copy)

    vampytest.assert_eq(voice_channel_effect, copy)


def test__VoiceChannelEffect__copy_with__0():
    """
    Tests whether ``VoiceChannelEffect.copy_with`` works as intended.
    
    Case: no fields given.
    """
    animation_id = 202304040032
    animation_type = VoiceChannelEffectAnimationType.basic
    channel_id = 202304040033
    emoji = BUILTIN_EMOJIS['x']
    guild_id = 202304040034
    sound_id = 202408180012
    sound_volume = 0.5
    user_id = 202304040035
    
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
    copy = voice_channel_effect.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(voice_channel_effect, copy)

    vampytest.assert_eq(voice_channel_effect, copy)


def test__VoiceChannelEffect__copy_with__1():
    """
    Tests whether ``VoiceChannelEffect.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_animation_id = 202304040036
    old_animation_type = VoiceChannelEffectAnimationType.basic
    old_channel_id = 202304040037
    old_emoji = BUILTIN_EMOJIS['x']
    old_guild_id = 202304040038
    old_sound_id = 202408180013
    old_sound_volume = 0.5
    old_user_id = 202304040039
    
    new_animation_id = 202304040040
    new_animation_type = VoiceChannelEffectAnimationType.premium
    new_channel_id = 202304040041
    new_emoji = BUILTIN_EMOJIS['heart']
    new_guild_id = 202304040042
    new_sound_id = 202408180014
    new_sound_volume = 0.6
    new_user_id = 202304040043
    
    voice_channel_effect = VoiceChannelEffect(
        animation_id = old_animation_id,
        animation_type = old_animation_type,
        channel_id = old_channel_id,
        emoji = old_emoji,
        guild_id = old_guild_id,
        sound_id = old_sound_id,
        sound_volume = old_sound_volume,
        user_id = old_user_id,
    )
    copy = voice_channel_effect.copy_with(
        animation_id = new_animation_id,
        animation_type = new_animation_type,
        channel_id = new_channel_id,
        emoji = new_emoji,
        guild_id = new_guild_id,
        sound_id = new_sound_id,
        sound_volume = new_sound_volume,
        user_id = new_user_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(voice_channel_effect, copy)

    vampytest.assert_eq(copy.animation_id, new_animation_id)
    vampytest.assert_eq(copy.animation_type, new_animation_type)
    vampytest.assert_eq(copy.channel_id, new_channel_id)
    vampytest.assert_eq(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.sound_id, new_sound_id)
    vampytest.assert_eq(copy.sound_volume, new_sound_volume)
    vampytest.assert_eq(copy.user_id, new_user_id)


def test__VoiceChannelEffect__channel__not_cached():
    """
    Tests whether ``VoiceChannelEffect.channel`` works as intended.
    
    Case: Not cached.
    """
    channel_id = 202304040044
    
    voice_channel_effect = VoiceChannelEffect(channel_id = channel_id)
    
    output = voice_channel_effect.channel
    vampytest.assert_instance(output, Channel)
    vampytest.assert_eq(output.id, channel_id)
    vampytest.assert_is(output, voice_channel_effect.channel)


def test__VoiceChannelEffect__channel__cached():
    """
    Tests whether ``VoiceChannelEffect.channel`` works as intended.
    
    Case: Cached.
    """
    channel_id = 202304040045
    
    channel = Channel.precreate(channel_id)
    
    voice_channel_effect = VoiceChannelEffect(channel_id = channel_id)
    
    vampytest.assert_is(voice_channel_effect.channel, channel)


def test__VoiceChannelEffect__guild__not_cached():
    """
    Tests whether ``VoiceChannelEffect.guild`` works as intended.
    
    Case: Not cached.
    """
    guild_id = 202304040046
    
    voice_channel_effect = VoiceChannelEffect(guild_id = guild_id)
    
    output = voice_channel_effect.guild
    vampytest.assert_is(output, None)


def test__VoiceChannelEffect__guild__cached():
    """
    Tests whether ``VoiceChannelEffect.guild`` works as intended.
    
    Case: Cached.
    """
    guild_id = 202304040047
    
    guild = Guild.precreate(guild_id)
    
    voice_channel_effect = VoiceChannelEffect(guild_id = guild_id)
    
    vampytest.assert_is(voice_channel_effect.guild, guild)


def test__VoiceChannelEffect__user__not_cached():
    """
    Tests whether ``VoiceChannelEffect.user`` works as intended.
    
    Case: Not cached.
    """
    user_id = 202304040048
    
    voice_channel_effect = VoiceChannelEffect(user_id = user_id)
    
    output = voice_channel_effect.user
    vampytest.assert_instance(output, ClientUserBase)
    vampytest.assert_eq(output.id, user_id)
    vampytest.assert_is(output, voice_channel_effect.user)


def test__VoiceChannelEffect__user__cached():
    """
    Tests whether ``VoiceChannelEffect.user`` works as intended.
    
    Case: Cached.
    """
    user_id = 202304040049
    
    user = User.precreate(user_id)
    
    voice_channel_effect = VoiceChannelEffect(user_id = user_id)
    
    vampytest.assert_is(voice_channel_effect.user, user)


def test__VoiceChannelEffect__sound__not_cached():
    """
    Tests whether ``VoiceChannelEffect.sound`` works as intended.
    
    Case: Not cached.
    """
    sound_id = 202408180015
    
    voice_channel_effect = VoiceChannelEffect(sound_id = sound_id)
    
    output = voice_channel_effect.sound
    vampytest.assert_instance(output, SoundboardSound)
    vampytest.assert_eq(output.id, sound_id)
    vampytest.assert_is(output, voice_channel_effect.sound)


def test__VoiceChannelEffect__sound__cached():
    """
    Tests whether ``VoiceChannelEffect.sound`` works as intended.
    
    Case: Cached.
    """
    sound_id = 202408180016
    
    sound = SoundboardSound.precreate(sound_id)
    
    voice_channel_effect = VoiceChannelEffect(sound_id = sound_id)
    
    vampytest.assert_is(voice_channel_effect.sound, sound)


def test__VoiceChannelEffect__sound__no_sound():
    """
    Tests whether ``VoiceChannelEffect.sound`` works as intended.
    
    Case: No sound.
    """
    voice_channel_effect = VoiceChannelEffect()
    
    vampytest.assert_is(voice_channel_effect.sound, None)
