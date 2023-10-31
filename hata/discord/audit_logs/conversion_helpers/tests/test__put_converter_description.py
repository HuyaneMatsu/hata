import vampytest

from ..converters import put_converter_description


def _iter_options():
    description = 'koishi'
    yield None, ''
    yield description, description


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_converter_description(input_value):
    """
    Tests whether ``put_converter_description`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return put_converter_description(input_value)
