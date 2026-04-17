import vampytest

from ..shared_fields import parse_value


def _iter_options():
    yield (
        {},
        '',
    )
    
    yield (
        {
            'value': '',
        },
        '',
    )
    
    yield (
        {
            'value': '',
        },
        '',
    )
    
    yield (
        {
            'value': 'a',
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_value(input_data):
    """
    Tests whether ``parse_value`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `str`
    """
    output = parse_value(input_data)
    vampytest.assert_instance(output, str)
    return output
