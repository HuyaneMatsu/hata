import vampytest

from ....message.attachment import Attachment

from ..fields import parse_attachments


def _iter_options():
    attachment_id_0 = 202405240010
    attachment_name_0 = 'Primrose'
    
    attachment_id_1 = 202405240011
    attachment_name_1 = 'Flower'
    
    attachment_0 = Attachment.precreate(
        attachment_id_0,
        name = attachment_name_0,
    )
    
    attachment_1 = Attachment.precreate(
        attachment_id_1,
        name = attachment_name_1,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'attachments': None,
        },
        None,
    )
    
    yield (
        {
            'attachments': {},
        },
        None,
    )
    
    yield (
        {
            'attachments': {
                str(attachment_id_0): attachment_0.to_data(include_internals = True),
            },
        },
        {
            attachment_id_0: attachment_0,
        }
    )
    
    yield (
        {
            'attachments': {
                str(attachment_id_0): attachment_0.to_data(include_internals = True),
                str(attachment_id_1): attachment_1.to_data(include_internals = True),
            },
        },
        {
            attachment_id_0: attachment_0,
            attachment_id_1: attachment_1,
        }
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_attachments(input_data):
    """
    Tests whether ``parse_attachments`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | dict<int, Attachment>`
    """
    output = parse_attachments(input_data)
    vampytest.assert_instance(output, dict, nullable = True)
    return output
