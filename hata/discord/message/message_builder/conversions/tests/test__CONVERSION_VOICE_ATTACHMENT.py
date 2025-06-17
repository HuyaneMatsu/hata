from base64 import b64encode as base_64_encode

import vampytest
from scarletio.web_common import FormData

from ....message import MessageFlag
from ....voice_attachment import VoiceAttachment

from ..voice_attachment import CONVERSION_VOICE_ATTACHMENT


def _iter_options__set_validator():
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
    
    # None
    yield None, [None]
    
    # VoiceAttachment
    yield voice_attachment, [voice_attachment]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_VOICE_ATTACHMENT__set_validator(input_value):
    """
    Tests whether ``CONVERSION_VOICE_ATTACHMENT.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : ```list<None | VoiceAttachment>```
    """
    return [*CONVERSION_VOICE_ATTACHMENT.set_validator(input_value)]


def _iter_options__serializer_putter():
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
    
    # None
    yield (
        {},
        False,
        None,
        {},
    )
    
    form = FormData()
    form.add_json(
        'payload_json',
        {
            'attachments': [
                {
                    'id': '0',
                    'description': description,
                    'duration_secs': duration,
                    'waveform': base_64_encode(waveform).decode('ascii'),
                },
            ],
            'flags': MessageFlag().update_by_keys(voice_message = True),
        },
    )
    form.add_field('files[0]', io, file_name = name, content_type = 'application/octet-stream')
    
    # VoiceAttachment
    yield (
        {},
        False,
        voice_attachment,
        form,
    )


@vampytest._(vampytest.call_from(_iter_options__serializer_putter()).returning_last())
def test__CONVERSION_VOICE_ATTACHMENT__serializer_putter(data, required, value):
    """
    Tests whether ``CONVERSION_VOICE_ATTACHMENT.serializer_putter`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to serialize.
    
    required : `bool`
        Whether this field is required.
    
    value : ``None | VoiceAttachment``
        The value to put into data.
    
    Returns
    -------
    output : `dict<str, object> | FormData`
    """
    data = data.copy()
    return CONVERSION_VOICE_ATTACHMENT.serializer_putter(data, required, value)
