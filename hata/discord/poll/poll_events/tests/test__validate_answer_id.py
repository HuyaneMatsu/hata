import vampytest

from ..fields import validate_answer_id


def _iter_options__passing():
    answer_id = 202404030006
    
    # yield None, 0
    yield 0, 0
    yield answer_id, answer_id
    # yield Answer.precreate(answer_id), answer_id
    yield str(answer_id), answer_id


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield '-1'
    yield -1
    yield '1111111111111111111111'
    yield 1111111111111111111111


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_answer_id__passing(input_value):
    """
    Tests whether `validate_answer_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    ValueError
    """
    return validate_answer_id(input_value)
