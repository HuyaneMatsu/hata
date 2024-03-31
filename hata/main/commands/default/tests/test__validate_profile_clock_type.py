import vampytest

from ..run import _validate_profile_clock_type


def _iter_options():
    yield '', ('wall', False)
    yield 'wall', ('wall', False)
    yield 'cpu', ('cpu', False)
    yield 'wAlL', ('wall', False)
    yield 'pudding', ('', True)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_profile_clock_type(input_value):
    """
    Tests whether ``_validate_profile_clock_type`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to validate.
    
    Returns
    -------
    clock_type : `str`
    message_returned : `bool`
    """
    output = _validate_profile_clock_type(input_value)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    clock_type, message = output
    vampytest.assert_instance(clock_type, str)
    vampytest.assert_instance(message, str, nullable = True)
    return clock_type, message is not None
