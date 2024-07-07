from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..voice_state import VoiceState


def test__VoiceState__repr():
    """
    Tests whether ``VoiceState.__repr__`` works as intended.
    """
    channel_id = 202301240018
    deaf = True
    guild_id = 202301240019
    speaker = True
    mute = True
    requested_to_speak_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    self_deaf = True
    self_mute = True
    self_stream = True
    self_video = True
    session_id = 'Remilia'
    user_id = 202301240020
    
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
    
    vampytest.assert_instance(repr(voice_state), str)


def test__VoiceState__hash():
    """
    Tests whether ``VoiceState.__hash__`` works as intended.
    """
    channel_id = 202301240021
    deaf = True
    guild_id = 202301240022
    speaker = True
    mute = True
    requested_to_speak_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    self_deaf = True
    self_mute = True
    self_stream = True
    self_video = True
    session_id = 'Remilia'
    user_id = 202301240023
    
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
    
    vampytest.assert_instance(hash(voice_state), int)


def test__VoiceState__eq():
    """
    Tests whether ``VoiceState.__eq__`` works as intended.
    """
    channel_id = 202301240021
    deaf = True
    guild_id = 202301240022
    speaker = True
    mute = True
    requested_to_speak_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    self_deaf = True
    self_mute = True
    self_stream = True
    self_video = True
    session_id = 'Remilia'
    user_id = 202301240023
    
    keyword_parameters = {
        'channel_id': channel_id,
        'deaf': deaf,
        'guild_id': guild_id,
        'speaker': speaker,
        'mute': mute,
        'requested_to_speak_at': requested_to_speak_at,
        'self_deaf': self_deaf,
        'self_mute': self_mute,
        'self_stream': self_stream,
        'self_video': self_video,
        'session_id': session_id,
        'user_id': user_id,
    }
    
    voice_state = VoiceState(**keyword_parameters)
    vampytest.assert_eq(voice_state, voice_state)
    vampytest.assert_ne(voice_state, object())
    
    test_voice_state = VoiceState(**keyword_parameters)
    vampytest.assert_eq(voice_state, test_voice_state)
    
    for field_name, field_value in (
        ('channel_id', 202301240024),
        ('deaf', False),
        ('guild_id', 202301240025),
        ('speaker', False),
        ('mute', False),
        ('requested_to_speak_at', DateTime(2016, 5, 13, tzinfo = TimeZone.utc)),
        ('self_deaf', False),
        ('self_mute', False),
        ('self_stream', False),
        ('self_video', False),
        ('session_id', 'Satori'),
        ('user_id', 202301240026),
    ):
        test_voice_state = VoiceState(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(voice_state, test_voice_state)
