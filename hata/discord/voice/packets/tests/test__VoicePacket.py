import vampytest

from ...reader import EMPTY_VOICE_FRAME_DECODED, EMPTY_VOICE_FRAME_ENCODED

from ..voice_packet import VoicePacket


def _assert_fields_set(voice_packet):
    """
    Asserts whether every fields are set of the given voice packet.
    
    Parameters
    ----------
    voice_packet : ``VoicePacket``
        Voice packet.
    """
    vampytest.assert_instance(voice_packet, VoicePacket)
    vampytest.assert_instance(voice_packet._cache_decoded, bytes, nullable = True)
    vampytest.assert_instance(voice_packet.encoded, bytes)


def test__VoicePacket__new():
    """
    Tests whether ``VoicePacket.__new__`` works as intended.
    """
    encoded = EMPTY_VOICE_FRAME_ENCODED
    
    voice_packet = VoicePacket(encoded)
    _assert_fields_set(voice_packet)
    
    vampytest.assert_eq(voice_packet.encoded, encoded)


def test__VoicePacket__repr():
    """
    Tests whether ``VoicePacket.__repr__`` works as intended.
    """
    encoded = EMPTY_VOICE_FRAME_ENCODED
    
    voice_packet = VoicePacket(encoded)
    
    output = repr(voice_packet)
    vampytest.assert_instance(output, str)


def test__VoicePacket__hash():
    """
    Tests whether ``VoicePacket._hash__`` works as intended.
    """
    encoded = EMPTY_VOICE_FRAME_ENCODED
    
    voice_packet = VoicePacket(encoded)
    
    output = hash(voice_packet)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    encoded = EMPTY_VOICE_FRAME_ENCODED
    
    keyword_parameters = {
        'encoded': encoded,
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
            'encoded': b'4566',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__VoicePacket__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``VoicePacket.__eq__`` works as intended.
    
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
    voice_packet_0 = VoicePacket(**keyword_parameters_0)
    voice_packet_1 = VoicePacket(**keyword_parameters_1)
    
    output = voice_packet_0 == voice_packet_1
    vampytest.assert_instance(output, bool)
    return output


def test__VoicePacket__decoded():
    """
    Tests whether ``VoicePacket.__repr__`` works as intended.
    """
    encoded = EMPTY_VOICE_FRAME_ENCODED
    decoded = EMPTY_VOICE_FRAME_DECODED
    
    voice_packet = VoicePacket(encoded)
    
    output = voice_packet.decoded
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(output, decoded)
    
    # check caching.
    vampytest.assert_is(output, voice_packet.decoded)
