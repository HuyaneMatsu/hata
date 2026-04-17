import vampytest

from ..fields import parse_ended


def _iter_options():
    yield (
        {},
        False,
    )
    
    yield (
        {
            'ended': None,
        },
        False,
    )
    
    yield (
        {
            'ended': False,
        },
        False,
    )
    
    yield (
        {
            'ended': True,
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_ended(input_data):
    """
    Tests whether ``parse_ended`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_ended(input_data)
    vampytest.assert_instance(output, bool)
    return output
