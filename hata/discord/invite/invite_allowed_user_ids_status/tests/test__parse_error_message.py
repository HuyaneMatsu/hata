import vampytest

from ..fields import parse_error_message


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'error_message': None,
        },
        None,
    )
    
    yield (
        {
            'error_message': '',
        },
        None,
    )
    
    yield (
        {
            'error_message': 'a',
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_error_message(input_data):
    """
    Tests whether ``parse_error_message`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_error_message(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
