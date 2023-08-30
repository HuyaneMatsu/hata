import vampytest

from ..fields import validate_id


def _iter_options__passing():
    activity_party_id = 'koishi'
    
    yield None, None
    yield '', None
    yield activity_party_id, activity_party_id


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_id__passing(input_value):
    """
    Tests whether `validate_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `int`
    """
    return validate_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_id__type_error(input_value):
    """
    Tests whether `validate_id` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_id(input_value)
