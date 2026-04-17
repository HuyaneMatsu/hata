import vampytest

from ..payload_renderer import _get_string_representation


def _iter_options():
    yield 'hey mister', '"hey mister"'
    yield '\U0002ffff', '"\\U0002ffff"'
    yield '\U0001f49a', '"\U0001f49a"'
    yield '\t\t\t', '"\\t\\t\\t"'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_string_representation(input_value):
    """
    Tests whether ``_get_string_representation`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to represent
    
    Returns
    -------
    output : `str`
    """
    output = _get_string_representation(input_value)
    vampytest.assert_instance(output, str)
    return output
