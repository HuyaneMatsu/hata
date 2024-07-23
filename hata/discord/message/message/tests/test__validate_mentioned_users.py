import vampytest

from ....user import ClientUserBase, User

from ..fields import validate_mentioned_users


def _iter_options__passing():
    user_id_1 = 202305010006
    user_id_2 = 202305010007
    
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    yield None, None
    yield [], None
    yield [user_1], (user_1,)
    yield [user_2, user_1], (user_1, user_2,)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_mentioned_users(input_value):
    """
    Validates whether ``validate_mentioned_users`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<ClientUserBase>`
    
    Raises
    ------
    TypeError
    """
    output = validate_mentioned_users(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, ClientUserBase)
    return output
