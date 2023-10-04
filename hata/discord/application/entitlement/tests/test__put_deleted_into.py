import vampytest

from ..fields import put_deleted_into


def _iter_options():
    yield False, False, {}
    yield False, True, {'deleted': False}
    yield True, False, {'deleted': True}
    yield True, True, {'deleted': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_deleted_into(input_value, defaults):
    """
    Tests whether ``put_deleted_into`` works as intended.
    
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
    return put_deleted_into(input_value, {}, defaults)
