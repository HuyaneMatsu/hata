import vampytest

from ....user import User, ZEROUSER

from ..fields import validate_user


def _iter_options__passing():
    user = User.precreate(202308010008, name = 'Yukari')
    yield user, user
    yield None, ZEROUSER


def _iter_options__type_error():
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_user(input_value):
    """
    Tests whether `validate_user` works as intended.
    
    Parameters
    ----------
    input_value : ``None | ClientUserBase``
        The value to validate.
    
    Returns
    -------
    output : ``ClientUserBase``
    
    Raises
    ------
    TypeError
    """
    return validate_user(input_value)
