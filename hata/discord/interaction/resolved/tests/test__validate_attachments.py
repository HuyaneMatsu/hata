import vampytest

from ....message import Attachment

from ..fields import validate_attachments


def test__validate_attachments__0():
    """
    Tests whether ``validate_attachments`` works as intended.
    
    Case: passing.
    """
    attachment_id = 202211050010
    attachment_name = 'Faker'
    
    attachment = Attachment.precreate(
        attachment_id,
        name = attachment_name,
    )
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ({}, None),
        ([attachment], {attachment_id: attachment}),
        ({attachment_id: attachment}, {attachment_id: attachment}),
    ):
        output = validate_attachments(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_attachments__1():
    """
    Tests whether ``validate_attachments`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_attachments(input_value)
