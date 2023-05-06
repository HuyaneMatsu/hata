import vampytest

from ...attachment import Attachment

from ..fields import parse_attachments

def test__parse_attachments():
    """
    Tests whether ``parse_attachments`` works as intended.
    """
    attachment_id_0 = 202304290006
    attachment_name_0 = 'Primrose'
    
    attachment_id_1 = 202304290007
    attachment_name_1 = 'Flower'
    
    attachment_0 = Attachment.precreate(
        attachment_id_0,
        name = attachment_name_0,
    )
    
    attachment_1 = Attachment.precreate(
        attachment_id_1,
        name = attachment_name_1,
    )
    
    for input_data, expected_output in (
        ({}, None),
        ({'attachments': None}, None),
        ({'attachments': []}, None),
        (
            {
                'attachments': [
                    attachment_0.to_data(include_internals = True),
                ],
            },
            (attachment_0,),
        ),
        (
            {
                'attachments': [
                    attachment_0.to_data(include_internals = True),
                    attachment_1.to_data(include_internals = True),
                ],
            },
            (attachment_0, attachment_1),
        ),
    ):
        output = parse_attachments(input_data)
        vampytest.assert_eq(output, expected_output)
