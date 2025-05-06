import vampytest

from ..fields import put_id


def _iter_options():
    activity_id = 202306150012
    
    yield 0, False, {}
    yield 0, True, {}
    yield activity_id, False, {'id': format(activity_id, 'x')}
    yield activity_id, True, {'id': format(activity_id, 'x')}


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
