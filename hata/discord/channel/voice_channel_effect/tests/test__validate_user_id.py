import vampytest

from ....user import User

from ..fields import validate_user_id


def _iter_options__passing():
    user_id = 202304030008
    
    yield None, 0
    yield 0, 0
    yield user_id, user_id
    yield User.precreate(user_id), user_id
    yield str(user_id), user_id


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
def test__validate_user_id__passing(input_value):
    """
    Tests whether `validate_user_id` works as intended.
    
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
    output = validate_user_id(input_value)
    vampytest.assert_instance(output, int)
    return output
