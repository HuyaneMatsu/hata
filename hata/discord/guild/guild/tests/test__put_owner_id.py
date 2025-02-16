import vampytest

from ..fields import put_owner_id


def _iter_options():
    owner_id = 202306100001
    
    yield 0, False, {'owner_id': None}
    yield 0, True, {'owner_id': None}
    yield owner_id, False, {'owner_id': str(owner_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_owner_id(input_value, defaults):
    """
    Tests whether ``put_owner_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Owner id.
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_owner_id(input_value, {}, defaults)
