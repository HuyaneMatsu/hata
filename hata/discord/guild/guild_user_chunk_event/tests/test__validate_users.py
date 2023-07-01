import vampytest

from ....user import User

from ..fields import validate_users


def _iter_options__passing():
    user_id = 202306300003
    user_name = 'Koishi'
    
    user = User.precreate(
        user_id,
        name = user_name,
    )
    
    yield None, []
    yield [], []
    yield [user], [user]
    

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_users__passing(input_value):
    """
    Tests whether ``validate_users`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Users to validate.
    
    Returns
    -------
    output : `dict<int, ClientUserBase>`
    
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
        Users to validate.
    
    Raises
    ------
    TypeError
    """
    validate_users(input_value)
