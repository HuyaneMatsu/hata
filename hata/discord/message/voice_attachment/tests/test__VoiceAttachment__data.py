from base64 import b64encode as base_64_encode

import vampytest

from ..voice_attachment import VoiceAttachment



def test__VoiceAttachment__to_data():
    """
    Tests whether ``VoiceAttachment.to_data`` works as intended.
    
    Case: include defaults & internals.
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
    
    vampytest.assert_eq(
        voice_attachment.to_data(),
        {
            'id': '0',
            'description': description,
            'duration_secs': duration,
            'waveform': base_64_encode(waveform).decode('ascii'),
        },
    )
