import vampytest

from ..fields import put_display_name


def _iter_options():
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'global_name': None,
        },
    )
    
    yield (
        'afraid',
        False,
        {
            'global_name': 'afraid',
        },
    )
    
    yield (
        'afraid',
        True,
        {
            'global_name': 'afraid',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_display_name(input_value, defaults):
    """
    Tests whether ``put_display_name`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to serialize.
    
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_display_name(input_value, {}, defaults)
