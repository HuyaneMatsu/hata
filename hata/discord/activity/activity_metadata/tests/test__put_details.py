import vampytest

from ..fields import put_details


def _iter_options():
    yield None, False, {}
    yield None, True, {'details': ''}
    yield 'a', False, {'details': 'a'}
    yield 'a', True, {'details': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_details(input_value, defaults):
    """
    Tests whether ``put_details`` works as intended.
    
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
    return put_details(input_value, {}, defaults)
