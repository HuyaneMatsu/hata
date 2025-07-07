import vampytest

from ..fields import parse_primary


def _iter_options():
    yield (
        {},
        False,
    )
    
    yield (
        {
            'is_primary': None,
        },
        False,
    )
    
    yield (
        {
            'is_primary': False,
        },
        False,
    )
    
    yield (
        {
            'is_primary': True,
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_primary(input_data):
    """
    Tests whether ``parse_primary`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_primary(input_data)
    vampytest.assert_instance(output, bool)
    return output
