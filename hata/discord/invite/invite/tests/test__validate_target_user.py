import vampytest

from ....user import ClientUserBase, User

from ..fields import validate_target_user


def _iter_options__passing():
    user = User.precreate(202308030005, name = 'Ken')
    
    yield user, user
    yield None, None


def _iter_options__type_error():
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
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
    output : `None | ClientUserBase`
    
    Raises
    ------
    TypeError
    """
    output = validate_target_user(input_value)
    vampytest.assert_instance(output, ClientUserBase, nullable = True)
    return output
