import vampytest

from ..fields import parse_value__bool


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'value': None,
        },
        None,
    )
    
    yield (
        {
            'value': False,
        },
        '\00',
    )
    
    yield (
        {
            'value': True,
        },
        '\01',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_value__bool(input_data):
    """
    Tests whether ``parse_value__bool`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_value__bool(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
