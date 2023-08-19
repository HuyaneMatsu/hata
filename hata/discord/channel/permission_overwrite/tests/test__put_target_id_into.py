import vampytest

from ..fields import put_target_id_into


def _iter_options():
    target_id = 202210050005
    
    yield 0, False, {'id': None}
    yield 0, True, {'id': None}
    
    yield target_id, False, {'id': str(target_id)}
    yield target_id, True, {'id': str(target_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_id_into(input_value, defaults):
    """
    Tests whether ``put_target_id_into`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target_id_into(input_value, {}, defaults)
