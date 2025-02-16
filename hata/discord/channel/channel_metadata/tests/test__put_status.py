import vampytest

from ..fields import put_status


def _iter_options():
    yield None, False, {}
    yield None, True, {'status': None}
    yield 'a', False, {'status': 'a'}
    yield 'a', True, {'status': 'a'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_status(input_value, defaults):
    """
    Tests whether ``put_status`` is working as intended.
    
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
    return put_status(input_value, {}, defaults)
