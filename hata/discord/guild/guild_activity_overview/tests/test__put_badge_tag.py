import vampytest

from ..fields import put_badge_tag


def _iter_options():
    yield '', False, {'tag': ''}
    yield '', True, {'tag': ''}
    yield 'a', False, {'tag': 'a'}
    yield 'a', True, {'tag': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_badge_tag(input_value, defaults):
    """
    Tests whether ``put_badge_tag`` works as intended.
    
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
    return put_badge_tag(input_value, {}, defaults)
