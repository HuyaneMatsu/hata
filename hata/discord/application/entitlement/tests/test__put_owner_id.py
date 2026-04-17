import vampytest

from ..fields import put_owner_id


def _iter_options():
    owner_id = 202310030001

    yield 0, False, {'owner_id': None}
    yield 0, True, {'owner_id': None}
    yield owner_id, False, {'owner_id': str(owner_id)}
    yield owner_id, True, {'owner_id': str(owner_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_owner_id(input_value, defaults):
    """
    Tests whether ``put_owner_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_owner_id(input_value, {}, defaults)
