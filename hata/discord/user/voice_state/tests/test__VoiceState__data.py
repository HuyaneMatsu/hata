from datetime import datetime as DateTime

import vampytest

from ....guild import Guild
from ....utils import datetime_to_timestamp

from ..voice_state import VoiceState

from .test__VoiceState__constructor import _assert_fields_set


def test__VoiceState__from_data__0():
    """
    Tests whether ``VoiceState.from_data`` works as intended.
    
    Case: Field setting.
    """
    channel_id = 202301240003
    deaf = True
    guild_id = 202301240004
    speaker = True
    mute = True
    requested_to_speak_at = DateTime(2016, 5, 14)
    self_deaf = True
    self_mute = True
    self_stream = True
    self_video = True
    session_id = 'Remilia'
    user_id = 202301240005
    
    data = {
        'channel_id': str(channel_id),
        'deaf': deaf,
        'suppress': not speaker,
        'mute': mute,
        'request_to_speak_timestamp': datetime_to_timestamp(requested_to_speak_at),
        'self_deaf': self_deaf,
        'self_mute': self_mute,
        'self_stream': self_stream,
        'self_video': self_video,
        'session_id': session_id,
        'user_id': str(user_id),
    }
    
    voice_state = VoiceState.from_data(data, guild_id)
    
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


def test__VoiceState__from_data__1():
    """
    Tests whether ``VoiceState.from_data`` works as intended.
    
    Case: no channel defined.
    """
    voice_state = VoiceState.from_data({}, 0)
    vampytest.assert_is(voice_state, None)


def test__VoiceState__from_data__2():
    """
    Tests whether ``VoiceState.from_data`` works as intended.
    
    Case: caching.
    """
    channel_id = 202301240009
    guild_id = 202301240010
    user_id = 202301240011
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'channel_id': str(channel_id),
        'user_id': str(user_id),
    }
    voice_state = VoiceState.from_data(data, guild_id)
    
    vampytest.assert_eq(guild.voice_states, {user_id: voice_state})


def test__VoiceState__from_data__3():
    """
    Tests whether ``VoiceState.from_data`` works as intended.
    
    Case: caching, `strong_cache` as `False`.
    """
    channel_id = 202306150008
    guild_id = 202306150009
    user_id = 202306150010
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'channel_id': str(channel_id),
        'user_id': str(user_id),
    }
    voice_state = VoiceState.from_data(data, guild_id, strong_cache = False)
    
    vampytest.assert_eq(guild.voice_states, {})


def test__VoiceState__to_data():
    """
    Tests whether ``VoiceState.to_data`` works as intended.
    
    Case: Include defaults.
    """
    channel_id = 202301240006
    deaf = True
    guild_id = 202301240007
    speaker = True
    mute = True
    requested_to_speak_at = DateTime(2016, 5, 14)
    self_deaf = True
    self_mute = True
    self_stream = True
    self_video = True
    session_id = 'Remilia'
    user_id = 202301240008
    
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
    
    expected_output = {
        'channel_id': str(channel_id),
        'deaf': deaf,
        'suppress': not speaker,
        'mute': mute,
        'request_to_speak_timestamp': datetime_to_timestamp(requested_to_speak_at),
        'self_deaf': self_deaf,
        'self_mute': self_mute,
        'self_stream': self_stream,
        'self_video': self_video,
        'session_id': session_id,
        'user_id': str(user_id),
    }
    
    vampytest.assert_eq(
        voice_state.to_data(defaults = True),
        expected_output,
    )

def test__VoiceState__update_attributes():
    """
    Tests whether ``VoiceState._update_attributes`` works as intended.
    """
    old_deaf = True
    old_speaker = True
    old_mute = True
    old_requested_to_speak_at = DateTime(2016, 5, 14)
    old_self_deaf = True
    old_self_mute = True
    old_self_stream = True
    old_self_video = True
    new_deaf = False
    new_speaker = False
    new_mute = False
    new_requested_to_speak_at = DateTime(2016, 5, 13)
    new_self_deaf = False
    new_self_mute = False
    new_self_stream = False
    new_self_video = False

    
    voice_state = VoiceState(
        deaf = old_deaf,
        speaker = old_speaker,
        mute = old_mute,
        requested_to_speak_at = old_requested_to_speak_at,
        self_deaf = old_self_deaf,
        self_mute = old_self_mute,
        self_stream = old_self_stream,
        self_video = old_self_video,
    )
    
    data = {
        'deaf': new_deaf,
        'suppress': not new_speaker,
        'mute': new_mute,
        'request_to_speak_timestamp': datetime_to_timestamp(new_requested_to_speak_at),
        'self_deaf': new_self_deaf,
        'self_mute': new_self_mute,
        'self_stream': new_self_stream,
        'self_video': new_self_video,
    }
    
    voice_state._update_attributes(data)
    
    vampytest.assert_eq(voice_state.deaf, new_deaf)
    vampytest.assert_eq(voice_state.speaker, new_speaker)
    vampytest.assert_eq(voice_state.mute, new_mute)
    vampytest.assert_eq(voice_state.requested_to_speak_at, new_requested_to_speak_at)
    vampytest.assert_eq(voice_state.self_deaf, new_self_deaf)
    vampytest.assert_eq(voice_state.self_mute, new_self_mute)
    vampytest.assert_eq(voice_state.self_stream, new_self_stream)
    vampytest.assert_eq(voice_state.self_video, new_self_video)

def test__VoiceState__difference_update_attributes():
    """
    Tests whether ``VoiceState._difference_update_attributes`` works as intended.
    """
    old_deaf = True
    old_speaker = True
    old_mute = True
    old_requested_to_speak_at = DateTime(2016, 5, 14)
    old_self_deaf = True
    old_self_mute = True
    old_self_stream = True
    old_self_video = True
    new_deaf = False
    new_speaker = False
    new_mute = False
    new_requested_to_speak_at = DateTime(2016, 5, 13)
    new_self_deaf = False
    new_self_mute = False
    new_self_stream = False
    new_self_video = False

    
    voice_state = VoiceState(
        deaf = old_deaf,
        speaker = old_speaker,
        mute = old_mute,
        requested_to_speak_at = old_requested_to_speak_at,
        self_deaf = old_self_deaf,
        self_mute = old_self_mute,
        self_stream = old_self_stream,
        self_video = old_self_video,
    )
    
    data = {
        'deaf': new_deaf,
        'suppress': not new_speaker,
        'mute': new_mute,
        'request_to_speak_timestamp': datetime_to_timestamp(new_requested_to_speak_at),
        'self_deaf': new_self_deaf,
        'self_mute': new_self_mute,
        'self_stream': new_self_stream,
        'self_video': new_self_video,
    }
    
    old_attributes = voice_state._difference_update_attributes(data)
    
    vampytest.assert_eq(voice_state.deaf, new_deaf)
    vampytest.assert_eq(voice_state.speaker, new_speaker)
    vampytest.assert_eq(voice_state.mute, new_mute)
    vampytest.assert_eq(voice_state.requested_to_speak_at, new_requested_to_speak_at)
    vampytest.assert_eq(voice_state.self_deaf, new_self_deaf)
    vampytest.assert_eq(voice_state.self_mute, new_self_mute)
    vampytest.assert_eq(voice_state.self_stream, new_self_stream)
    vampytest.assert_eq(voice_state.self_video, new_self_video)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'deaf': old_deaf,
            'speaker': old_speaker,
            'mute': old_mute,
            'requested_to_speak_at': old_requested_to_speak_at,
            'self_deaf': old_self_deaf,
            'self_mute': old_self_mute,
            'self_stream': old_self_stream,
            'self_video': old_self_video,
        },
    )

def test__VoiceState__update_channel__0():
    """
    Tests whether ``VoiceState._update_channel`` works as intended.
    
    Case: Same channel id-s.
    """
    guild_id = 202301240013
    user_id = 202301240014
    old_channel_id = 202301240012
    new_channel_id = 202301240012
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'channel_id': str(old_channel_id),
        'user_id': str(user_id),
    }
    voice_state = VoiceState.from_data(data, guild_id)
    
    vampytest.assert_eq(guild.voice_states, {user_id: voice_state})
    
    data = {
        'channel_id': str(new_channel_id)
    }
    
    output = voice_state._update_channel(data)
    
    vampytest.assert_eq(
        output,
        (old_channel_id, new_channel_id),
    )
    

def test__VoiceState__update_channel__1():
    """
    Tests whether ``VoiceState._update_channel`` works as intended.
    
    Case: Different channel id-s.
    """
    guild_id = 202301240015
    user_id = 202301240016
    old_channel_id = 202301240017
    new_channel_id = 202301240018
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'channel_id': str(old_channel_id),
        'user_id': str(user_id),
    }
    voice_state = VoiceState.from_data(data, guild_id)
    
    data = {
        'channel_id': str(new_channel_id)
    }
    
    output = voice_state._update_channel(data)
    vampytest.assert_eq(guild.voice_states, {user_id: voice_state})
    
    vampytest.assert_eq(
        output,
        (old_channel_id, new_channel_id),
    )
    

def test__VoiceState__update_channel__2():
    """
    Tests whether ``VoiceState._update_channel`` works as intended.
    
    Case: null channel id.
    """
    guild_id = 202301240015
    user_id = 202301240016
    old_channel_id = 202301240017
    new_channel_id = 0
    
    guild = Guild.precreate(guild_id)
    
    data = {
        'channel_id': str(old_channel_id),
        'user_id': str(user_id),
    }
    voice_state = VoiceState.from_data(data, guild_id)
    
    data = {
        'channel_id': str(new_channel_id)
    }
    
    output = voice_state._update_channel(data)
    vampytest.assert_eq(guild.voice_states, {})
    
    vampytest.assert_eq(
        output,
        (old_channel_id, 0),
    )
