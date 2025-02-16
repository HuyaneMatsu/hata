import vampytest

from ..fields import put_target_id


def _iter_options():
    target_id = 202310200001
    
    yield 0, False, {}
    yield 0, True, {'target_id': None}
    yield target_id, False, {'target_id': str(target_id)}
    yield target_id, True, {'target_id': str(target_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_id(target_id, defaults):
    """
    Tests whether ``put_target_id`` works as intended.
    
    Parameters
    ----------
    target_id : `int`
        The target's identifier to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_target_id(target_id, {}, defaults)
