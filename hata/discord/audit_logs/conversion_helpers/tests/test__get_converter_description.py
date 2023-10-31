import vampytest

from ..converters import get_converter_description


def _iter_options():
    description = 'koishi'
    yield None, None
    yield '', None
    yield description, description


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_converter_description(input_value):
    """
    Tests whether ``get_converter_description`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | str`
    """
    return get_converter_description(input_value)
