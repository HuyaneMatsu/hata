import vampytest

from ....user import User, ZEROUSER

from ..fields import validate_user


def _iter_options():
    user = User.precreate(202308010002, name = 'Ken')
    yield user, user
    yield None, ZEROUSER


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_user__passing(input_value):
    """
    Tests whether `validate_user` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `None`, ``ClientUserBase``
        The value to validate.
    
    Returns
    -------
    output : ``ClientUserBase``
    """
    return validate_user(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with('a')
def test__validate_user__type_error(input_value):
    """
    Tests whether `validate_user` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `None`, ``ClientUserBase``
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_user(input_value)
