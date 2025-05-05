import vampytest

from ..shared_fields import put_custom_id


def _iter_options():
    yield None, False, {}
    yield None, True, {'custom_id': None}
    yield 'a', False, {'custom_id': 'a'}
    yield 'a', True, {'custom_id': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_custom_id(input_value, defaults):
    """
    Tests whether ``put_custom_id`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        The value to serialize.
    
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_custom_id(input_value, {}, defaults)
