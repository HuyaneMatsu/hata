import vampytest

from ..fields import put_content_type


def _iter_options():
    yield (
        None,
        False,
        {
            'content_type': '',
        },
    )
    
    yield (
        None,
        True,
        {
            'content_type': '',
        },
    )
    
    yield (
        'a',
        False,
        {
            'content_type': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'content_type': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_content_type(input_value, defaults):
    """
    Tests whether ``put_content_type`` works as intended.
    
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
    return put_content_type(input_value, {}, defaults)
