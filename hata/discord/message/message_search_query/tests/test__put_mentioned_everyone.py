import vampytest

from ..fields import put_mentioned_everyone


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
            'mention_everyone': False,
        },
    )
    
    yield (
        True,
        False,
        {
            'mention_everyone': True,
        },
    )
    
    yield (
        True,
        True,
        {
            'mention_everyone': True
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_mentioned_everyone(input_value, defaults):
    """
    Tests whether ``put_mentioned_everyone`` works as intended.
    
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
    return put_mentioned_everyone(input_value, {}, defaults)
