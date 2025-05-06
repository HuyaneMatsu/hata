import vampytest

from ..fields import put_excluded_keywords


def _iter_options():
    yield None, False, {}
    yield None, True, {'allow_list': []}
    yield ('a', ), False, {'allow_list': ['a']}
    yield ('a', ), True, {'allow_list': ['a']}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_excluded_keywords(input_value, defaults):
    """
    Tests whether ``put_excluded_keywords`` is working as intended.
    
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
    return put_excluded_keywords(input_value, {}, defaults)
