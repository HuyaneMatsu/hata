import vampytest

from ..payload_renderer import _get_character_representation


def _iter_options():
    yield 'h', 'h'
    yield '\U0002ffff', '\\U0002ffff'
    yield '\U0001f49a', '\U0001f49a'
    yield '\t', '\\t'
    yield '\n', '\\n'
    yield '\r', '\\r'
    yield '\\', '\\\\'
    yield '"', '\\"'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_character_representation(input_value):
    """
    Tests whether ``_get_character_representation`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to represent
    
    Returns
    -------
    output : `str`
    """
    output = _get_character_representation(input_value)
    vampytest.assert_instance(output, str)
    return output
