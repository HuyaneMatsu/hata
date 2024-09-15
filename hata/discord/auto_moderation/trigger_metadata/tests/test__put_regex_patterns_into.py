import vampytest

from ..fields import put_regex_patterns_into


def _iter_options():
    yield None, False, {}
    yield None, True, {'regex_patterns': []}
    yield ('a', ), False, {'regex_patterns': ['a']}
    yield ('a', ), True, {'regex_patterns': ['a']}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_regex_patterns_into(input_value, defaults):
    """
    Tests whether ``put_regex_patterns_into`` is working as intended.
    
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
    return put_regex_patterns_into(input_value, {}, defaults)
