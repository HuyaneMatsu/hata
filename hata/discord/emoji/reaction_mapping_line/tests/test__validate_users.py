import vampytest

from ....user import User

from ..fields import validate_users


def _iter_options__passing():
    user_id_0 = 202405110000
    user_id_1 = 202405110001
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)

    yield None, None
    yield [], None
    yield [user_0], {user_0}
    yield [user_0, user_0], {user_0}
    yield [user_1, user_0], {user_1, user_0}
    yield [user_0, user_1], {user_0, user_1}


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_users(input_value):
    """
    Validates whether ``validate_users`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | set<ClientUserBase>``
    
    Raises
    ------
    TypeError
    """
    output = validate_users(input_value)
    vampytest.assert_instance(output, set, nullable = True)
    return output
