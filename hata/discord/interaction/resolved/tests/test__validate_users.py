import vampytest

from ....user import User

from ..fields import validate_users


def _iter_options():
    user_id = 202211050022
    user_name = 'Faker'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    yield (None, None)
    yield ([], None)
    yield ({}, None)
    yield ([user], {user_id: user})
    yield ({user_id: user}, {user_id: user})


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_users__passing(input_value):
    """
    Tests whether ``validate_users`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | dict<int, ClientUserBase>`
    """
    return validate_users(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with([12.6])
@vampytest.call_with({12.6: 12.6})
def test__validate_users__type_error(input_value):
    """
    Tests whether ``validate_users`` works as intended.
    
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
