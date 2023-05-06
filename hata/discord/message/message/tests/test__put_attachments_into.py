import vampytest

from ...attachment import Attachment

from ..fields import put_attachments_into


def test__put_attachments_into():
    """
    Tests whether ``put_attachments_into`` works as intended.
    """
    attachment_id_0 = 202304290007
    attachment_name_0 = 'Primrose'
    
    attachment_id_1 = 202304290008
    attachment_name_1 = 'Flower'
    
    attachment_0 = Attachment.precreate(
        attachment_id_0,
        name = attachment_name_0,
    )
    
    attachment_1 = Attachment.precreate(
        attachment_id_1,
        name = attachment_name_1,
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {'attachments': []}),
        (None, True, {'attachments': []}),
        (
            (attachment_0, attachment_1),
            False,
            {
                'attachments': [
                    attachment_0.to_data(defaults = False, include_internals = True),
                    attachment_1.to_data(defaults = False, include_internals = True),
                ],
            },
        ),
        (
            (attachment_0, attachment_1),
            True,
            {
                'attachments': [
                    attachment_0.to_data(defaults = True, include_internals = True),
                    attachment_1.to_data(defaults = True, include_internals = True),
                ],
            },
        ),
    ):
        output = put_attachments_into(input_value, {}, defaults, include_internals = True)
        vampytest.assert_eq(output, expected_output)
