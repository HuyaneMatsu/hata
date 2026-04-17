import vampytest

from ..fields import put_bio


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
            'bio': '',
        },
    )
    
    yield (
        'a',
        False,
        {
            'bio': 'a',
        },
    )
    
    yield (
        'a',
        True,
        {
            'bio': 'a',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_bio(input_value, defaults):
    """
    Tests whether ``put_bio`` works as intended.
    
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
    return put_bio(input_value, {}, defaults)
