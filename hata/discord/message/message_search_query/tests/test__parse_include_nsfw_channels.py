import vampytest

from ..fields import parse_include_nsfw_channels


def _iter_options():
    yield (
        {},
        False,
    )
    
    yield (
        {
            'include_nsfw': None,
        },
        False,
    )
    
    yield (
        {
            'include_nsfw': False,
        },
        False,
    )
    
    yield (
        {
            'include_nsfw': True,
        },
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_include_nsfw_channels(input_data):
    """
    Tests whether ``parse_include_nsfw_channels`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_include_nsfw_channels(input_data)
    vampytest.assert_instance(output, bool)
    return output
