import vampytest

from ...attachment import Attachment

from ..fields import validate_attachments


def test__validate_attachments__0():
    """
    Validates whether ``validate_attachments`` works as intended.
    
    Case: passing.
    """
    attachment_id_0 = 202304290009
    attachment_id_1 = 202304290010
    
    attachment_0 = Attachment.precreate(attachment_id_0)
    attachment_1 = Attachment.precreate(attachment_id_1)
    
    for input_value, expected_output in (
        ([], None),
        ([attachment_0], (attachment_0,)),
        ([attachment_1, attachment_0], (attachment_0, attachment_1)),
    ):
        output = validate_attachments(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_attachments__1():
    """
    Validates whether ``validate_attachments`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_attachments(input_value)
