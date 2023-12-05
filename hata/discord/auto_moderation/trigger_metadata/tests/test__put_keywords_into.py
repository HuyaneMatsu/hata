import vampytest

from ..fields import put_keywords_into


def _iter_options():
    yield None, False, {}
    yield None, True, {'keyword_filter': []}
    yield ('a', ), False, {'keyword_filter': ['a']}
    yield ('a', ), True, {'keyword_filter': ['a']}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_keywords_into(input_value, defaults):
    """
    Tests whether ``put_keywords_into`` is working as intended.
    
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
    return put_keywords_into(input_value, {}, defaults)
