import vampytest

from ..fields import put_include_nsfw_channels


def _iter_options():
    yield (
        False,
        False,
        {},
    )
    
    yield (
        False,
        True,
        {
            'include_nsfw': False,
        },
    )
    
    yield (
        True,
        False,
        {
            'include_nsfw': True,
        },
    )
    
    yield (
        True,
        True,
        {
            'include_nsfw': True
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_include_nsfw_channels(input_value, defaults):
    """
    Tests whether ``put_include_nsfw_channels`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_include_nsfw_channels(input_value, {}, defaults)
