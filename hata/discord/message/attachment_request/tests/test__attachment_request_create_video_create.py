import vampytest

from ..utils import attachment_request_create_video_create

from .test__AttachmentRequest import _assert_fields_set


def test__attachment_request_create_video_create__no_fields_given():
    """
    Tests whether ``attachment_request_create_video_create`` works as intended.
    
    Case: no fields given.
    """
    name = 'rin.mp3'
    io = b'nyan'
    duration = 2.0
    
    attachment_request = attachment_request_create_video_create(name, io, duration)
    _assert_fields_set(attachment_request)
    
    vampytest.assert_eq(attachment_request.name, name)
    vampytest.assert_eq(attachment_request.io, io)
    vampytest.assert_eq(attachment_request.duration, duration)
    
    vampytest.assert_is(attachment_request.description, None)


def test__attachment_request_create_video_create__all_fields_given():
    """
    Tests whether ``attachment_request_create_video_create`` works as intended.
    
    Case: all fields given.
    """
    name = 'rin.mp4'
    io = b'nyan'
    duration = 2.0
    description = 'hell cat'
    
    attachment_request = attachment_request_create_video_create(
        name, io, duration, description = description
    )
    _assert_fields_set(attachment_request)
    
    vampytest.assert_eq(attachment_request.name, name)
    vampytest.assert_eq(attachment_request.io, io)
    
    vampytest.assert_eq(attachment_request.description, description)
