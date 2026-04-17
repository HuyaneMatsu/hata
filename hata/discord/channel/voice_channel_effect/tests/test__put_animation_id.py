import vampytest

from ..fields import put_animation_id


def _iter_options():
    animation_id = 202304030012
    
    yield 0, False, {}
    yield 0, True, {'animation_id': None}
    yield animation_id, False, {'animation_id': str(animation_id)}
    yield animation_id, False, {'animation_id': str(animation_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_animation_id(input_value, defaults):
    """
    Tests whether ``put_animation_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_animation_id(input_value, {}, defaults)
