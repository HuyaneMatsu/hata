import vampytest

from ..fields import parse_attachment_id


def _iter_options():
    attachment_id = 202509200001
    
    yield (
        {},
        0,
    )
    
    yield (
        {
            'attachment_id': None,
        },
        0,
    )
    
    yield (
        {
            'attachment_id': str(attachment_id),
        },
        attachment_id,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_attachment_id(input_data):
    """
    Tests whether ``parse_attachment_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_attachment_id(input_data)
    vampytest.assert_instance(output, int)
    return output
