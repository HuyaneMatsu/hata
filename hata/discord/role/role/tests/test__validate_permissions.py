import vampytest

from ....permission import Permission

from ..fields import validate_permissions


def _iter_options__passing():
    yield None, Permission(0)
    yield 1, Permission(1)
    yield Permission(1), Permission(1)


def _iter_options__type_error():
    yield 'a'
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_permissions(input_value):
    """
    Tests whether `validate_permissions` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    value : ``Permission``
    
    Raises
    ------
    TypeError
    """
    output = validate_permissions(input_value)
    vampytest.assert_instance(output, Permission)
    return output
