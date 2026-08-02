import vampytest

from ..utils import attachment_request_create_regular_create

from .test__AttachmentRequest import _assert_fields_set


def test__attachment_request_create_regular_create__no_fields_given():
    """
    Tests whether ``attachment_request_create_regular_create`` works as intended.
    
    Case: no fields given.
    """
    name = 'rin.txt'
    io = b'nyan'
    
    attachment_request = attachment_request_create_regular_create(name, io)
    _assert_fields_set(attachment_request)
    
    vampytest.assert_eq(attachment_request.name, name)
    vampytest.assert_eq(attachment_request.io, io)
    
    vampytest.assert_is(attachment_request.description, None)
    vampytest.assert_eq(attachment_request.spoiler, False)
    vampytest.assert_is(attachment_request.title, None)


def test__attachment_request_create_regular_create__all_fields_given():
    """
    Tests whether ``attachment_request_create_regular_create`` works as intended.
    
    Case: all fields given.
    """
    name = 'rin.txt'
    io = b'nyan'
    description = 'hell cat'
    spoiler = True
    title = 'orin'
    
    attachment_request = attachment_request_create_regular_create(
        name, io, description = description, spoiler = spoiler, title = title
    )
    _assert_fields_set(attachment_request)
    
    vampytest.assert_eq(attachment_request.name, name)
    vampytest.assert_eq(attachment_request.io, io)
    vampytest.assert_eq(attachment_request.description, description)
    vampytest.assert_eq(attachment_request.spoiler, spoiler)
    vampytest.assert_eq(attachment_request.title, title)
