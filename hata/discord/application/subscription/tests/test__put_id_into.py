import vampytest

from ..fields import put_id_into


def _iter_options():
    subscription_id = 202409220001
    
    yield 0, False, {'id': None}
    yield 0, True, {'id': None}
    yield subscription_id, False, {'id': str(subscription_id)}
    yield subscription_id, True, {'id': str(subscription_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_id_into(input_value, defaults):
    """
    Tests whether ``put_id_into`` works as intended.
    
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
    return put_id_into(input_value, {}, defaults)
