import vampytest

from ..fields import put_age_gated


def _iter_options():
    yield False, False, {'requires_age_gate': False}
    yield False, True, {'requires_age_gate': False}
    yield True, False, {'requires_age_gate': True}
    yield True, True, {'requires_age_gate': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_age_gated(input_value, defaults):
    """
    Tests whether ``put_age_gated`` works as intended.
    
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
    return put_age_gated(input_value, {}, defaults)
