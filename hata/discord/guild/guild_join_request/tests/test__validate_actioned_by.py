import vampytest

from ....user import User

from ..fields import validate_actioned_by


def _iter_options__passing():
    user = User.precreate(202305160044, name = 'Ken')
    
    yield None, None
    yield user, user


def _iter_options__type_error():
    yield 12.6
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_actioned_by(input_value):
    """
    Tests whether `validate_actioned_by` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | ClientUserBase`
    
    Raises
    ------
    TypeError
    """
    return validate_actioned_by(input_value)
