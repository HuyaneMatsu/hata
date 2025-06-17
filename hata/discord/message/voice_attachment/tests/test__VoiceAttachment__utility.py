import vampytest

from ..voice_attachment import VoiceAttachment

from .test__VoiceAttachment__constructor import _assert_fields_set


def test__VoiceAttachment__copy__default():
    """
    Tests whether ``VoiceAttachment.copy`` works as intended.
    
    Case: default.
    """
    description = 'Nue'
    duration = 12.6
    io = b'a'
    name = 'i miss you'
    waveform = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    voice_attachment = VoiceAttachment(
        name,
        io,
        duration,
        description = description,
        waveform = waveform,
    )
    copy = voice_attachment.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(voice_attachment, copy)
    
    vampytest.assert_eq(voice_attachment, copy)


def test__VoiceAttachment__copy_with__no_fields():
    """
    Tests whether ``VoiceAttachment.copy_with`` works as intended.
    
    Case: no fields given.
    """
    description = 'Nue'
    duration = 12.6
    io = b'a'
    name = 'i miss you'
    waveform = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    voice_attachment = VoiceAttachment(
        name,
        io,
        duration,
        description = description,
        waveform = waveform,
    )
    copy = voice_attachment.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(voice_attachment, copy)
    
    vampytest.assert_eq(voice_attachment, copy)


def test__VoiceAttachment__copy_with__all_fields():
    """
    Tests whether ``VoiceAttachment.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_description = 'Nue'
    old_duration = 12.6
    old_io = b'a'
    old_name = 'i miss you'
    old_waveform = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    new_description = 'Nue'
    new_duration = 12.6
    new_io = b'a'
    new_name = 'i miss you'
    new_waveform = b'\x01' * len(old_waveform)
    
    voice_attachment = VoiceAttachment(
        old_name,
        old_io,
        old_duration,
        description = old_description,
        waveform = old_waveform,
    )
    
    copy = voice_attachment.copy_with(
        description = new_description,
        duration = new_duration,
        io = new_io,
        name = new_name,
        waveform = new_waveform,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(voice_attachment, copy)
    
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.duration, new_duration)
    vampytest.assert_eq(copy.io, new_io)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.waveform, new_waveform)
