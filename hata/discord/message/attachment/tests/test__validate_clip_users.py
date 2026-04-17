import vampytest

from ....user import ClientUserBase, User

from ..fields import validate_clip_users


def _iter_options__passing():
    user_id_0 = 202502020004
    user_id_1 = 202502020005
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)

    yield None, None
    yield [], None
    yield [user_0], (user_0,)
    yield [user_0, user_0], (user_0,)
    yield [user_1, user_0], (user_0, user_1)
    yield [user_0, user_1], (user_0, user_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_clip_users(input_value):
    """
    Validates whether ``validate_clip_users`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``None | tuple<ClientUserBase>``
    
    Raises
    ------
    TypeError
    """
    output = validate_clip_users(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, ClientUserBase)
    
    return output
