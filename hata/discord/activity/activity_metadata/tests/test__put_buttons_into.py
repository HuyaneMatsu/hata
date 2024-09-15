import vampytest

from ..fields import put_buttons_into


def _iter_options():
    yield None, False, {}
    yield None, True, {'buttons': []}
    yield ('a', ), False, {'buttons': ['a']}
    yield ('a', ), True, {'buttons': ['a']}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_buttons_into(input_value, defaults):
    """
    Tests whether ``put_buttons_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<str>`
        Value to serialize.
    defaults : `bool`
        Whether fields with the default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_buttons_into(input_value, {}, defaults)
