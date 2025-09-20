import vampytest

from ..fields import put_target_id


def _iter_options():
    target_id = 202409010027
    
    yield (
        0,
        False,
        {},
    )
    
    yield (
        0,
        True,
        {
            'data': {
                'target_id': None,
            },
        },
    )
    
    yield (
        target_id,
        False,
        {
            'data': {
                'target_id': str(target_id),
            },
        },
    )
    
    yield (
        target_id,
        True,
        {
            'data': {
                'target_id': str(target_id),
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_id(input_value, defaults):
    """
    Tests whether ``put_target_id`` works as intended.
    
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
    return put_target_id(input_value, {}, defaults)
