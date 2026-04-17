import vampytest

from ..payload_renderer import _get_character_representation_escaped


def _iter_options():
    yield '\U0002ffff', '\\U0002ffff'
    yield '\u01ff', '\\u01ff'
    yield '\x0f', '\\x0f'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_character_representation_escaped(input_value):
    """
    Tests whether ``_get_character_representation_escaped`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to represent.
    
    Returns
    -------
    output : `str`
    """
    output = _get_character_representation_escaped(input_value)
    vampytest.assert_instance(output, str)
    return output
