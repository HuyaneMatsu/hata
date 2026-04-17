import vampytest

from ..voice_attachment import VoiceAttachment


def test__VoiceAttachment__repr():
    """
    Tests whether ``VoiceAttachment.__repr__`` works as intended.
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
    
    vampytest.assert_instance(repr(voice_attachment), str)


def test__VoiceAttachment__hash():
    """
    Tests whether ``VoiceAttachment.__hash__`` works as intended.
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
    
    vampytest.assert_instance(hash(voice_attachment), int)


def _iter_options__eq():
    description = 'Nue'
    duration = 12.6
    io = b'a'
    name = 'i miss you'
    waveform = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    keyword_parameters = {
        'description': description,
        'duration': duration,
        'io': io,
        'name': name,
        'waveform': waveform,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'description': 'Remilia',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'duration': 56.6,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'io': b'b',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'Slave of Scarlet',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'waveform': b'\x01' * len(waveform),
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__VoiceAttachment__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``VoiceAttachment.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    voice_attachment_0 = VoiceAttachment(**keyword_parameters_0)
    voice_attachment_1 = VoiceAttachment(**keyword_parameters_1)
    
    output = voice_attachment_0 == voice_attachment_1
    vampytest.assert_instance(output, bool)
    return output
