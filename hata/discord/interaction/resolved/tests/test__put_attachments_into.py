import vampytest

from ....message import Attachment

from ..fields import put_attachments_into


def test__put_attachments_into():
    """
    Tests whether ``put_attachments_into`` works as intended.
    """
    attachment_id = 202211050009
    attachment_name = 'Faker'
    
    attachment = Attachment.precreate(
        attachment_id,
        name = attachment_name,
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'attachments': {}}),
        (
            {
                attachment_id: attachment,
            },
                True,
            {
                'attachments': {
                    str(attachment_id): attachment.to_data(defaults = True, include_internals = True),
                }
            },
        )
    ):
        output = put_attachments_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
