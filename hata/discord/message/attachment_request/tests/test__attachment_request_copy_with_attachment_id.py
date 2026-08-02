import vampytest

from ..utils import attachment_request_copy_with_attachment_id, attachment_request_create_regular_edit

from .test__AttachmentRequest import _assert_fields_set


def test__attachment_request_copy_with_attachment_id():
    """
    Tests whether ``attachment_request_copy_with_attachment_id`` works as intended.
    """
    attachment_id_0 = 202607100001
    attachment_id_1 = 202607100002
    description = 'hell cat'
    spoiler = True
    
    attachment_request = attachment_request_create_regular_edit(
        attachment_id_0, description = description, spoiler = spoiler
    )
    copy = attachment_request_copy_with_attachment_id(attachment_request, attachment_id_1)
    
    _assert_fields_set(copy)
    
    vampytest.assert_eq(copy.attachment_id, attachment_id_1)
    vampytest.assert_is(copy.description, description)
    vampytest.assert_eq(copy.spoiler, spoiler)
