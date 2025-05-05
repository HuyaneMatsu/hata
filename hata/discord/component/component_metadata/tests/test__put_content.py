import vampytest

from ..fields import put_content


def _iter_options():
    yield None, False, {'content': ''}
    yield None, True, {'content': ''}
    yield 'a', False, {'content': 'a'}
    yield 'a', True, {'content': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_content(input_value, defaults):
    """
    Tests whether ``put_content`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_content(input_value, {}, defaults)
