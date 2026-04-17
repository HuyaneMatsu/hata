import vampytest

from ..fields import put_topic


def _iter_options():
    yield None, False, {'topic': ''}
    yield None, True, {'topic': ''}
    yield 'a', False, {'topic': 'a'}
    yield 'a', True, {'topic': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_topic(input_value, defaults):
    """
    Tests whether ``put_topic`` is working as intended.
    
    Parameters
    ----------
    input_value : `None`, `str`
        Value to serialise.
    defaults : `bool`
        Whether values with their default value should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_topic(input_value, {}, defaults)
