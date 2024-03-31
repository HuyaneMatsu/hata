import vampytest

from ..function import parse_modifier_parameter_name


def _iter_options():
    yield '--hey-mister', ('hey-mister', True)
    yield '--no-hey-mister', ('hey-mister', False)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_modifier_parameter_name(input_value):
    """
    Tests whether ``parse_modifier_parameter_name`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to work with.
    
    Returns
    -------
    output : `(str, bool)`
    """
    output = parse_modifier_parameter_name(input_value)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], str)
    vampytest.assert_instance(output[1], bool)
    return output
