import vampytest

from ..utils import attachment_request_create_voice_edit

from .test__AttachmentRequest import _assert_fields_set


def test__attachment_request_create_voice_edit__no_fields_given():
    """
    Tests whether ``attachment_request_create_voice_edit`` works as intended.
    
    Case: no fields given.
    """
    attachment_id = 2026070014
    
    attachment_request = attachment_request_create_voice_edit(attachment_id)
    _assert_fields_set(attachment_request)
    
    vampytest.assert_eq(attachment_request.attachment_id, attachment_id)
    
    vampytest.assert_is(attachment_request.description, None)


def test__attachment_request_create_voice_edit__all_fields_given():
    """
    Tests whether ``attachment_request_create_voice_edit`` works as intended.
    
    Case: all fields given.
    """
    attachment_id = 2026070015
    description = 'hell cat'
    
    attachment_request = attachment_request_create_voice_edit(
        attachment_id, description = description
    )
    _assert_fields_set(attachment_request)
    
    vampytest.assert_eq(attachment_request.attachment_id, attachment_id)
    vampytest.assert_eq(attachment_request.description, description)
