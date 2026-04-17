import vampytest

from ..fields import put_error_message


def _iter_options():
    yield (
        None,
        False,
        {
            'error_message': None,
        },
    )
    
    yield (
        None,
        True,
        {
            'error_message': None,
        },
    )
    
    yield (
        'a',
        False,
        {
            'error_message': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'error_message': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_error_message(input_value, defaults):
    """
    Tests whether ``put_error_message`` works as intended.
    
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
    return put_error_message(input_value, {}, defaults)
