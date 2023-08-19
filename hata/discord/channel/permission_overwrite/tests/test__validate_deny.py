import vampytest

from ....permission import Permission

from ..fields import validate_deny


def _iter_options():
    yield Permission(11111), Permission(11111)
    yield 11111, Permission(11111)
    yield 0, Permission()
    yield None, Permission()


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_deny__passing(input_value):
    """
    Tests whether ``validate_deny`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``Permission``
        The validated value.
    """
    output = validate_deny(input_value)
    vampytest.assert_instance(output, Permission)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_deny__type_error(input_value):
    """
    Tests whether ``validate_deny`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_deny(input_value)
