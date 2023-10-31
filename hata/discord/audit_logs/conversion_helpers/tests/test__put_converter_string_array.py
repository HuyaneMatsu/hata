import vampytest

from ..converters import put_converter_string_array


def _iter_options():
    string_0 = 'koishi'
    string_1 = 'satori'
    
    yield None, []
    yield (string_0, string_1), [string_0, string_1]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_converter_string_array(input_value):
    """
    Tests whether ``put_converter_string_array`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        Processed value.
    
    Returns
    -------
    output : `object`
    """
    return put_converter_string_array(input_value)
