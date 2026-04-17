import vampytest

from ..fields import parse_pinned


def _iter_options():
    yield (
        {},
        False,
    )
    
    yield (
        {
            'pinned': None,
        },
        False,
    )
    
    yield (
        {
            'pinned': False,
        },
        False,
    )
    
    yield (
        {
            'pinned': True,
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_pinned(input_data):
    """
    Tests whether ``parse_pinned`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_pinned(input_data)
    vampytest.assert_instance(output, bool)
    return output
