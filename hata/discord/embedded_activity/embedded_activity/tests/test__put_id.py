import vampytest

from ..fields import put_id


def _iter_options():
    embedded_activity_id = 202409010071
    
    yield 0, False, {'instance_id': None}
    yield 0, True, {'instance_id': None}
    yield embedded_activity_id, False, {'instance_id': str(embedded_activity_id)}
    yield embedded_activity_id, True, {'instance_id': str(embedded_activity_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_id(input_value, defaults):
    """
    Tests whether ``put_id`` works as intended.
    
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
    return put_id(input_value, {}, defaults)
