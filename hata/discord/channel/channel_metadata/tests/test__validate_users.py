import vampytest

from ....user import User

from ..fields import validate_users


def _iter_options():
    user_id_1 = 202209150002
    user_id_2 = 202209150003
    
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    yield ([], [])
    yield ([user_id_1], [user_1])
    yield ([user_1], [user_1])
    yield ([user_2, user_1], [user_1, user_2])


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_users__passing(input_value):
    """
    Validates whether ``validate_users`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `list<ClientUserBase>`
    """
    return validate_users(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_users__type_error(input_value):
    """
    Validates whether ``validate_users`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_users(input_value)
