import vampytest

from ....message import Attachment

from ..fields import parse_attachments


def test__parse_attachments():
    """
    Tests whether ``parse_attachments`` works as intended.
    """
    attachment_id = 202211050008
    attachment_name = 'Faker'
    
    attachment = Attachment.precreate(
        attachment_id,
        name = attachment_name,
    )
    
    for input_value, expected_output in (
        ({}, None),
        ({'attachments': {}}, None),
        (
            {
                'attachments': {
                    str(attachment_id): attachment.to_data(defaults = True, include_internals = True),
                }
            },
            {
                attachment_id: attachment,
            }
        )
    ):
        output = parse_attachments(input_value)
        vampytest.assert_eq(output, expected_output)
