import vampytest

from ..fields import put_content_into


def _iter_options():
    yield None, False, {}
    yield None, True, {'message': {'content': ''}}
    yield 'a', False, {'message': {'content': 'a'}}
    yield 'a', True, {'message': {'content': 'a'}}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_content_into(input_value, defaults):
    """
    Tests whether ``put_content_into`` works as intended.
    
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
    return put_content_into(input_value, {}, defaults)
