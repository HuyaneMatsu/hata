import vampytest

from ..fields import parse_processed


def _iter_options():
    yield (
        {},
        0,
    )
    
    yield (
        {
            'processed_users': None,
        },
        0,
    )
    
    yield (
        {
            'processed_users': 1,
        },
        1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_processed(input_data):
    """
    Tests whether ``parse_processed`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the processed from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_processed(input_data)
    vampytest.assert_instance(output, int)
    return output
