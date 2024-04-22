import vampytest

from ..fields import put_allow_multiple_choices_into


def _iter_options():
    yield False, False, {}
    yield False, True, {'allow_multiselect': False}
    yield True, False, {'allow_multiselect': True}
    yield True, True, {'allow_multiselect': True}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_allow_multiple_choices_into(input_value, defaults):
    """
    Tests whether ``put_allow_multiple_choices_into`` works as intended.
    
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
    return put_allow_multiple_choices_into(input_value, {}, defaults)
