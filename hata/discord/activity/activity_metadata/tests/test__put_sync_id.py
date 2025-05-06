import vampytest

from ..fields import put_sync_id


def _iter_options():
    yield None, False, {}
    yield None, True, {'sync_id': ''}
    yield 'a', False, {'sync_id': 'a'}
    yield 'a', True, {'sync_id': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_sync_id(input_value, defaults):
    """
    Tests whether ``put_sync_id`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to serialize.
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_sync_id(input_value, {}, defaults)
