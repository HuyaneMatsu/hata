import vampytest

from ..fields import put_analytics_id


def _iter_options():
    yield (
        0,
        False,
        {
            'analytics_id': format(0, '0>32x'),
        },
    )
    
    yield (
        0,
        True,
        {
            'analytics_id': format(0, '0>32x'),
        },
    )
    
    yield (
        1,
        False,
        {
            'analytics_id': format(1, '0>32x'),
        },
    )
    
    yield (
        1,
        True,
        {
            'analytics_id': format(1, '0>32x'),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_analytics_id(input_value, defaults):
    """
    Tests whether ``put_analytics_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_analytics_id(input_value, {}, defaults)
