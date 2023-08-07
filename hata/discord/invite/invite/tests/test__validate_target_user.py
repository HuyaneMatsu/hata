import vampytest

from ....user import User

from ..fields import validate_target_user


def _iter_options():
    user = User.precreate(202308030005, name = 'Ken')
    yield user, user
    yield None, None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_target_user__passing(input_value):
    """
    Tests whether `validate_target_user` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None`, ``ClientUserBase``
    """
    return validate_target_user(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with('a')
def test__validate_target_user__type_error(input_value):
    """
    Tests whether `validate_target_user` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_target_user(input_value)
