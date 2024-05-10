import vampytest

from ....user import User

from ..fields import validate_failed_user_ids


def _iter_options__passing():
    user_id_0 = 202405010024
    user_id_1 = 202405010025
    
    yield None, None
    yield [], None
    yield [user_id_0], (user_id_0,)
    yield [User.precreate(user_id_0)], (user_id_0,)
    yield [user_id_0, user_id_1], (user_id_0, user_id_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_failed_user_ids(input_value):
    """
    Tests whether `validate_failed_user_ids` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<int>`
    
    Raises
    ------
    TypeError
    """
    output = validate_failed_user_ids(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    if output is not None:
        for element in output:
            vampytest.assert_instance(element, int)
    return output
