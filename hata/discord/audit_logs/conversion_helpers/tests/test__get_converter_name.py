import vampytest

from ..converters import get_converter_name


def _iter_options():
    name = 'koishi'
    yield None, ''
    yield name, name


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_converter_name(input_value):
    """
    Tests whether ``get_converter_name`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `str`
    """
    return get_converter_name(input_value)
