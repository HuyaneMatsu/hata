import vampytest

from ..helpers import escape_name_to_key


def _iter_options():
    yield 'east_new', 'east_new'
    yield 'East New', 'east_new'
    yield 'Höffman', 'hffman'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__escape_name_to_key(input_value):
    """
    Tests whether ``escape_name_to_key`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to escape.
    
    Returns
    -------
    output : `str`
    """
    output = escape_name_to_key(input_value)
    vampytest.assert_instance(output, str)
    return output
