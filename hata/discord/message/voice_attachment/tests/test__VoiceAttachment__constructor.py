import vampytest

from ..voice_attachment import VoiceAttachment


def _assert_fields_set(voice_attachment):
    """
    Tests whether all attributes are set of the given voice attachment.
    
    Parameters
    ----------
    voice_attachment : ``VoiceAttachment``
        The voice attachment to check.
    """
    vampytest.assert_instance(voice_attachment, VoiceAttachment)
    vampytest.assert_instance(voice_attachment.description, str, nullable = True)
    vampytest.assert_instance(voice_attachment.duration, float)
    vampytest.assert_instance(voice_attachment.io, object)
    vampytest.assert_instance(voice_attachment.name, str)
    vampytest.assert_instance(voice_attachment.waveform, bytes)


def test__VoiceAttachment__new__no_fields():
    """
    Tests whether ``VoiceAttachment.__new__`` works as intended.
    
    Case: No fields given.
    """
    duration = 12.6
    io = b'a'
    name = 'i_miss_you.ogg'
    
    voice_attachment = VoiceAttachment(
        name,
        io,
        duration,
    )
    _assert_fields_set(voice_attachment)
    
    vampytest.assert_eq(voice_attachment.duration, duration)
    vampytest.assert_eq(voice_attachment.io, io)
    vampytest.assert_eq(voice_attachment.name, name)


def test__VoiceAttachment__new__all_fields():
    """
    Tests whether ``VoiceAttachment.__new__`` works as intended.
    
    Case: All fields given.
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
    _assert_fields_set(voice_attachment)
    
    vampytest.assert_eq(voice_attachment.description, description)
    vampytest.assert_eq(voice_attachment.duration, duration)
    vampytest.assert_eq(voice_attachment.io, io)
    vampytest.assert_eq(voice_attachment.name, name)
    vampytest.assert_eq(voice_attachment.waveform, waveform)
