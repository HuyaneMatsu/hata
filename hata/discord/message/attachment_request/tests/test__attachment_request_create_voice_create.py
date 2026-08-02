import vampytest

from ..constants import ATTACHMENT_REQUEST_WAVEFORM_OGG_DEFAULT
from ..utils import attachment_request_create_voice_create

from .test__AttachmentRequest import _assert_fields_set


def test__attachment_request_create_voice_create__no_fields_given():
    """
    Tests whether ``attachment_request_create_voice_create`` works as intended.
    
    Case: no fields given.
    """
    name = 'rin.ogg'
    io = b'nyan'
    duration = 2.0
    
    attachment_request = attachment_request_create_voice_create(name, io, duration)
    _assert_fields_set(attachment_request)
    
    vampytest.assert_eq(attachment_request.name, name)
    vampytest.assert_eq(attachment_request.io, io)
    vampytest.assert_eq(attachment_request.duration, duration)
    
    vampytest.assert_is(attachment_request.description, None)
    vampytest.assert_eq(attachment_request.waveform, ATTACHMENT_REQUEST_WAVEFORM_OGG_DEFAULT)


def test__attachment_request_create_voice_create__all_fields_given():
    """
    Tests whether ``attachment_request_create_voice_create`` works as intended.
    
    Case: all fields given.
    """
    name = 'rin.ogg'
    io = b'nyan'
    duration = 2.0
    description = 'hell cat'
    waveform = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    
    attachment_request = attachment_request_create_voice_create(
        name, io, duration, description = description, waveform = waveform
    )
    _assert_fields_set(attachment_request)
    
    vampytest.assert_eq(attachment_request.name, name)
    vampytest.assert_eq(attachment_request.io, io)
    vampytest.assert_eq(attachment_request.description, description)
    vampytest.assert_eq(attachment_request.waveform, waveform)
