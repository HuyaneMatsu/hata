import vampytest

from ..shared_fields import parse_default


def _iter_options():
    yield (
        {},
        False,
    )
    
    yield (
        {
            'default': None,
        },
        False,
    )
    
    yield (
        {
            'default': False,
        },
        False,
    )
    
    yield (
        {
            'default': True,
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_default(input_data):
    """
    Tests whether ``parse_default`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_default(input_data)
    vampytest.assert_instance(output, bool)
    return output
