from datetime import datetime as DateTime

import vampytest

from ....channel import Channel
from ....guild import Guild

from ...user import ClientUserBase, User

from ..voice_state import VoiceState

from .test__VoiceState__constructor import _assert_fields_set


def test__VoiceState__copy():
    """
    Tests whether ``VoiceState.copy`` works as intended.
    """
    channel_id = 202301240025
    deaf = True
    guild_id = 202301240026
    speaker = True
    mute = True
    requested_to_speak_at = DateTime(2016, 5, 14)
    self_deaf = True
    self_mute = True
    self_stream = True
    self_video = True
    session_id = 'Remilia'
    user_id = 202301240027
    
    
    voice_state = VoiceState(
        channel_id = channel_id,
        deaf = deaf,
        guild_id = guild_id,
        speaker = speaker,
        mute = mute,
        requested_to_speak_at = requested_to_speak_at,
        self_deaf = self_deaf,
        self_mute = self_mute,
        self_stream = self_stream,
        self_video = self_video,
        session_id = session_id,
        user_id = user_id,
    )
    
    copy = voice_state.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, voice_state)
    vampytest.assert_eq(copy, voice_state)


def test__VoiceState__copy_with__0():
    """
    Tests whether ``VoiceState.copy_with`` works as intended.
    
    Case: No fields given.
    """
    channel_id = 202301240028
    deaf = True
    guild_id = 202301240029
    speaker = True
    mute = True
    requested_to_speak_at = DateTime(2016, 5, 14)
    self_deaf = True
    self_mute = True
    self_stream = True
    self_video = True
    session_id = 'Remilia'
    user_id = 202301240030
    
    
    voice_state = VoiceState(
        channel_id = channel_id,
        deaf = deaf,
        guild_id = guild_id,
        speaker = speaker,
        mute = mute,
        requested_to_speak_at = requested_to_speak_at,
        self_deaf = self_deaf,
        self_mute = self_mute,
        self_stream = self_stream,
        self_video = self_video,
        session_id = session_id,
        user_id = user_id,
    )
    
    copy = voice_state.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, voice_state)
    vampytest.assert_eq(copy, voice_state)


def test__VoiceState__copy_with_1():
    """
    Tests whether ``VoiceState.copy_with`` works as intended.
    
    Case: ALl fields given.
    """
    old_channel_id = 202301240031
    old_deaf = True
    old_guild_id = 202301240032
    old_speaker = True
    old_mute = True
    old_requested_to_speak_at = DateTime(2016, 5, 14)
    old_self_deaf = True
    old_self_mute = True
    old_self_stream = True
    old_self_video = True
    old_session_id = 'Remilia'
    old_user_id = 202301240033
    
    new_channel_id = 202301240034
    new_deaf = False
    new_guild_id = 202301240035
    new_speaker = False
    new_mute = False
    new_requested_to_speak_at = DateTime(2016, 5, 13)
    new_self_deaf = False
    new_self_mute = False
    new_self_stream = False
    new_self_video = False
    new_session_id = 'Satori'
    new_user_id = 202301240036
    
    
    voice_state = VoiceState(
        channel_id = old_channel_id,
        deaf = old_deaf,
        guild_id = old_guild_id,
        speaker = old_speaker,
        mute = old_mute,
        requested_to_speak_at = old_requested_to_speak_at,
        self_deaf = old_self_deaf,
        self_mute = old_self_mute,
        self_stream = old_self_stream,
        self_video = old_self_video,
        session_id = old_session_id,
        user_id = old_user_id,
    )
    
    copy = voice_state.copy_with(
        channel_id = new_channel_id,
        deaf = new_deaf,
        guild_id = new_guild_id,
        speaker = new_speaker,
        mute = new_mute,
        requested_to_speak_at = new_requested_to_speak_at,
        self_deaf = new_self_deaf,
        self_mute = new_self_mute,
        self_stream = new_self_stream,
        self_video = new_self_video,
        session_id = new_session_id,
        user_id = new_user_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, voice_state)

    vampytest.assert_eq(copy.channel_id, new_channel_id)
    vampytest.assert_eq(copy.deaf, new_deaf)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.speaker, new_speaker)
    vampytest.assert_eq(copy.mute, new_mute)
    vampytest.assert_eq(copy.requested_to_speak_at, new_requested_to_speak_at)
    vampytest.assert_eq(copy.self_deaf, new_self_deaf)
    vampytest.assert_eq(copy.self_mute, new_self_mute)
    vampytest.assert_eq(copy.self_stream, new_self_stream)
    vampytest.assert_eq(copy.self_video, new_self_video)
    vampytest.assert_eq(copy.session_id, new_session_id)
    vampytest.assert_eq(copy.user_id, new_user_id)


def test__VoiceState__user():
    """
    Tests whether ``VoiceState.user`` works as intended.
    """
    user_id = 202301240037
    voice_state = VoiceState(user_id = user_id)
    user = voice_state.user
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    
    vampytest.assert_eq(voice_state._cache_user, user)


def test__VoiceState__set_cache_user():
    """
    Tests whether ``VoiceState._set_cache_user`` works as intended.
    """
    user_id = 202301240038
    user = User.precreate(user_id)
    
    voice_state = VoiceState()
    voice_state._set_cache_user(user)
    
    vampytest.assert_is(voice_state.user, user)


def test__VoiceState__channel():
    """
    Tests whether ``VoiceState.channel`` works as intended.
    """
    channel_id = 202301240039
    voice_state = VoiceState(channel_id = channel_id)
    channel = voice_state.channel
    vampytest.assert_instance(channel, Channel)
    vampytest.assert_eq(channel.id, channel_id)

def test__VoiceState__guild():
    """
    Tests whether ``VoiceState.guild`` works as intended.
    """
    guild_id = 202301240040
    voice_state = VoiceState(guild_id = guild_id)
    vampytest.assert_is(voice_state.guild, None)
    
    guild = Guild.precreate(guild_id)
    vampytest.assert_is(voice_state.guild, guild)
