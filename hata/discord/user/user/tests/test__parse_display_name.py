import vampytest

from ..fields import parse_display_name


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'global_name': None,
        },
        None,
    )
    
    yield (
        {
            'global_name': '',
        },
        None,
    )
    
    yield (
        {
            'global_name': 'afraid',
        },
        'afraid',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_display_name(data):
    """
    Tests whether ``parse_display_name`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_display_name(data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
