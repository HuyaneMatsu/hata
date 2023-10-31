import vampytest

from ....user import User

from ..fields import validate_inviter_id


def _iter_options__passing():
    user_id = 202310310000
    
    yield None, 0
    yield 0, 0
    yield user_id, user_id
    yield User.precreate(user_id), user_id
    yield str(user_id), user_id


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_inviter_id__passing(input_value):
    """
    Tests whether `validate_inviter_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `int`
    """
    return validate_inviter_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_inviter_id__type_error(input_value):
    """
    Tests whether `validate_inviter_id` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Raises
    ------
    TypeError
    """
    validate_inviter_id(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('-1')
@vampytest.call_with('1111111111111111111111')
@vampytest.call_with(-1)
@vampytest.call_with(1111111111111111111111)
def test__validate_inviter_id__value_error(input_value):
    """
    Tests whether `validate_inviter_id` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Raises
    ------
    ValueError
    """
    validate_inviter_id(input_value)
