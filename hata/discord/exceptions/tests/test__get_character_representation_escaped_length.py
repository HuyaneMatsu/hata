import vampytest

from ..payload_renderer import _get_character_representation_escaped_length


def _iter_options():
    yield '\U0002ffff', 10
    yield '\u01ff', 6
    yield '\x0f', 4


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_character_representation_escaped_length(input_value):
    """
    Tests whether ``_get_character_representation_escaped_length`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to represent.
    
    Returns
    -------
    output : `int`
    """
    output = _get_character_representation_escaped_length(input_value)
    vampytest.assert_instance(output, int)
    return output
