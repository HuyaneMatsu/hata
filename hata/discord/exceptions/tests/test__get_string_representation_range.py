import vampytest

from ..payload_renderer import _get_string_representation_range


def _iter_options():
    yield 'hey mister', 0, 5, ('"hey"', 3)
    yield 'hey mister', 3, 5, ('" mi"', 6)
    yield 'hey mister', 6, 5, ('"ste"', 9)
    yield 'hey mister', 9, 5, ('"r"', 10)
    
    yield '\U0002ffff a', 0, 5, ('"\\U0002ffff"', 1)
    yield 'a \U0002ffff', 0, 5, ('"a "', 2)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_string_representation_range(input_value, start, length_limit):
    """
    Tests whether ``_get_string_representation_range`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to represent
    start : `int`
        First character to represent.
    length_limit : `int`
        Maximal allowed length.
    
    Returns
    -------
    output : `(str, int)`
    """
    output = _get_string_representation_range(input_value, start, length_limit)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], str)
    vampytest.assert_instance(output[1], int)
    return output
