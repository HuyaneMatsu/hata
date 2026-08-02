import vampytest

from ...attachment import Attachment

from ..fields import parse_attachments


def _iter_options():
    attachment_0 = Attachment.precreate(
        202304290006,
        name = 'Primrose',
    )
    
    attachment_1 = Attachment.precreate(
        202304290007,
        name = 'Flower',
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
            'attachments': [],
        },
        None,
    )
    
    yield (
        {
            'attachments': [
                attachment_0.to_data(include_internals = True),
            ],
        },
        (attachment_0,),
    )
    
    yield (
        {
            'attachments': [
                attachment_0.to_data(include_internals = True),
                attachment_1.to_data(include_internals = True),
            ],
        },
        (
            attachment_0,
            attachment_1,
        ),
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
    output : ``None | tuple<Attachment>``
    """
    output = parse_attachments(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Attachment)
    return output
