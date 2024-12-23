import vampytest

from ..helpers import _validate_delete_on_unload


def _iter_options__passing():
    yield False, False
    yield True, True


def _iter_options__type_error():
    yield 12.6
    yield None


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_delete_on_unload(input_value):
    """
    Tests whether `_validate_delete_on_unload` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `bool`
    
    Raises
    ------
    TypeError
    """
    output = _validate_delete_on_unload(input_value)
    vampytest.assert_instance(output, bool)
    return output