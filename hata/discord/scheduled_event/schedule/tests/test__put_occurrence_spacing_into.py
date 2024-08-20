import vampytest

from ..fields import put_occurrence_spacing_into


def _iter_options():
    yield 1, False, {'interval': 1}
    yield 1, True, {'interval': 1}
    yield 2, False, {'interval': 2}
    yield 2, True, {'interval': 2}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_occurrence_spacing_into(input_value, defaults):
    """
    Tests whether ``put_occurrence_spacing_into`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_occurrence_spacing_into(input_value, {}, defaults)
