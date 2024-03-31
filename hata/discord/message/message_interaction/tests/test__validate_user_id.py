import vampytest

from ....user import User

from ..fields import validate_user_id


def _iter_options__passing():
    user_id = 202308010003
    user = User.precreate(user_id, name = 'Ken')
    yield user_id, user_id
    yield user, user_id
    yield None, 0


def _iter_options__type_error():
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_user_id__passing(input_value):
    """
    Tests whether `validate_user_id` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    """
    return validate_user_id(input_value)
