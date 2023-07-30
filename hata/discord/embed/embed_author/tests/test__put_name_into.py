import vampytest

from ..fields import put_name_into


def _iter_options():
    yield None, False, {'name': ''}
    yield None, True, {'name': ''}
    yield 'a', False, {'name': 'a'}
    yield 'a', True, {'name': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_name_into(input_value, defaults):
    """
    Tests whether ``put_name_into`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_name_into(input_value, {}, defaults)
