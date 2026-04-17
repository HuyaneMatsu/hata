import vampytest

from ..fields import put_integration_public


def _iter_options():
    yield False, False, {}
    yield False, True, {'integration_public': False}
    yield True, False, {'integration_public': True}
    yield True, True, {'integration_public': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_integration_public(input_value, defaults):
    """
    Tests whether ``put_integration_public`` works as intended.
    
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
    return put_integration_public(input_value, {}, defaults)
