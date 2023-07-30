import vampytest

from ..fields import put_name_into


def _iter_options():
    yield '', False, {'filename': ''}
    yield '', True, {'filename': ''}
    yield 'a', False, {'filename': 'a'}
    yield 'a', True, {'filename': 'a'}


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
