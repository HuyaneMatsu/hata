from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...user import ClientUserBase

from ..voice_state import VoiceState


def _assert_fields_set(voice_state):
    """
    Asserts whether every fields are set of the given voice state.
    
    Parameters
    ----------
    voice_state : ``VoiceState``
        The voice state to check.
    """
    vampytest.assert_instance(voice_state, VoiceState)
    vampytest.assert_instance(voice_state._cache_user, ClientUserBase, nullable = True)
    vampytest.assert_instance(voice_state.channel_id, int)
    vampytest.assert_instance(voice_state.deaf, bool)
    vampytest.assert_instance(voice_state.guild_id, int)
    vampytest.assert_instance(voice_state.speaker, bool)
    vampytest.assert_instance(voice_state.mute, bool)
    vampytest.assert_instance(voice_state.requested_to_speak_at, DateTime, nullable = True)
    vampytest.assert_instance(voice_state.self_deaf, bool)
    vampytest.assert_instance(voice_state.self_mute, bool)
    vampytest.assert_instance(voice_state.self_stream, bool)
    vampytest.assert_instance(voice_state.self_video, bool)
    vampytest.assert_instance(voice_state.session_id, str)
    vampytest.assert_instance(voice_state.user_id, int)



def test__VoiceState__new__0():
    """
    Tests whether ``VoiceState.__new__`` works as intended.
    
    Case: No fields given.
    """
    voice_state = VoiceState()
    _assert_fields_set(voice_state)


def test__VoiceState__new__1():
    """
    Tests whether ``VoiceState.__new__`` works as intended.
    
    Case: All fields given.
    """
    channel_id = 202301240000
    deaf = True
    guild_id = 202301240001
    speaker = True
    mute = True
    requested_to_speak_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    self_deaf = True
    self_mute = True
    self_stream = True
    self_video = True
    session_id = 'Remilia'
    user_id = 202301240002
    
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
    
    _assert_fields_set(voice_state)
    
    vampytest.assert_eq(voice_state.channel_id, channel_id)
    vampytest.assert_eq(voice_state.deaf, deaf)
    vampytest.assert_eq(voice_state.guild_id, guild_id)
    vampytest.assert_eq(voice_state.speaker, speaker)
    vampytest.assert_eq(voice_state.mute, mute)
    vampytest.assert_eq(voice_state.requested_to_speak_at, requested_to_speak_at)
    vampytest.assert_eq(voice_state.self_deaf, self_deaf)
    vampytest.assert_eq(voice_state.self_mute, self_mute)
    vampytest.assert_eq(voice_state.self_stream, self_stream)
    vampytest.assert_eq(voice_state.self_video, self_video)
    vampytest.assert_eq(voice_state.session_id, session_id)
    vampytest.assert_eq(voice_state.user_id, user_id)
