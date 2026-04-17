import vampytest

from ....user import User, ZEROUSER

from ..fields import validate_inviter


def _iter_options():
    user = User.precreate(202308010001, name = 'Ken')
    yield user, user
    yield None, ZEROUSER


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_inviter__passing(input_value):
    """
    Tests whether `validate_inviter` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``ClientUserBase``
    """
    return validate_inviter(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with('a')
def test__validate_inviter__type_error(input_value):
    """
    Tests whether `validate_inviter` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_inviter(input_value)
