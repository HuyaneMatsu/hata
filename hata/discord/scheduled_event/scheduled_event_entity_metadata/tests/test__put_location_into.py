import vampytest

from ..fields import put_location_into


def _iter_options():
    yield None, False, {'location': ''}
    yield None, True, {'location': ''}
    yield 'a', False, {'location': 'a'}
    yield 'a', True, {'location': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_location_into(input_value, defaults):
    """
    Tests whether ``put_location_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None`, `str`
        Value to serialize.
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_location_into(input_value, {}, defaults)
