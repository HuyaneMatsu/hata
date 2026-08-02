import vampytest

from ..utils import attachment_request_create_keep

from .test__AttachmentRequest import _assert_fields_set


def test__attachment_request_create_keep():
    """
    Tests whether ``attachment_request_create_keep`` works as intended.
    """
    attachment_id = 202607100000
    
    attachment_request = attachment_request_create_keep(attachment_id)
    _assert_fields_set(attachment_request)
    
    vampytest.assert_eq(attachment_request.attachment_id, attachment_id)
