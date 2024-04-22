import vampytest

from ..fields import validate_old_attributes


def _iter_options__passing():
    yield None, {}
    yield {}, {}
    yield {'yukari': 12.6}, {'yukari': 12.6}


def _iter_options__type_error():
    yield 12.6
    yield {12.6: 'yukari'}


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_old_attributes__passing(input_value):
    """
    Tests whether `validate_old_attributes` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `dict<str, object>`
    
    Raises
    ------
    TypeError
    """
    return validate_old_attributes(input_value)
