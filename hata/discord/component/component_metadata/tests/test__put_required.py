import vampytest

from ..fields import put_required


def _iter_options():
    yield False, False, {'required': False}
    yield False, True, {'required': False}
    yield True, False, {}
    yield True, True, {'required': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_required(input_value, defaults):
    """
    Tests whether ``put_required`` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_required(input_value, {}, defaults)
