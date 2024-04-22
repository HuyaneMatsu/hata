import vampytest

from ..payload_renderer import _get_character_representation_length


def _iter_options():
    yield 'h', 1
    yield '\U0002ffff', 10
    yield '\U0001f49a', 1
    yield '\t', 2
    yield '\n', 2
    yield '\r', 2
    yield '\\', 2
    yield '"', 2


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_character_representation_length(input_value):
    """
    Tests whether ``_get_character_representation_length`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to represent
    
    Returns
    -------
    output : `int`
    """
    output = _get_character_representation_length(input_value)
    vampytest.assert_instance(output, int)
    return output
