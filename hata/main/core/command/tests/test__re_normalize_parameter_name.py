import vampytest

from ..function import re_normalize_parameter_name


def _iter_options():
    yield 'hey--mister', 'hey-mister'
    yield '--hey-mister', 'hey-mister'
    yield 'hey_mister', 'hey-mister'
    yield 'hey mister', 'hey-mister'
    yield '--', ''


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__re_normalize_parameter_name(input_value):
    """
    Tests whether ``re_normalize_parameter_name`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to work with.
    
    Returns
    -------
    output : `str`
    """
    output = re_normalize_parameter_name(input_value)
    vampytest.assert_instance(output, str)
    return output
