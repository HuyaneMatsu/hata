import vampytest

from ..fields import put_tag


def _iter_options():
    yield '', False, {'tag': ''}
    yield '', True, {'tag': ''}
    yield 'a', False, {'tag': 'a'}
    yield 'a', True, {'tag': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_tag(input_value, defaults):
    """
    Tests whether ``put_tag`` works as intended.
    
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
    return put_tag(input_value, {}, defaults)
