import vampytest

from ..payload_renderer import _iter_string_representation_range


def _iter_options():
    yield 'hey mister', 5, ['"hey"', '" mi"', '"ste"', '"r"']
    yield '\U0002ffff a', 5, ['"\\U0002ffff"', '" a"']
    yield 'a \U0002ffff', 5, ['"a "', '"\\U0002ffff"']


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_string_representation_range(input_value, length_limit):
    """
    Tests whether ``_iter_string_representation_range`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to represent
    length_limit : `int`
        Maximal allowed length.
    
    Returns
    -------
    output : `list<str>`
    """
    output = [*_iter_string_representation_range(input_value, length_limit)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
