import vampytest

from ..converters import value_serializer_string_array


def _iter_options():
    string_0 = 'koishi'
    string_1 = 'satori'
    
    yield None, []
    yield (string_0, string_1), [string_0, string_1]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_serializer_string_array(input_value):
    """
    Tests whether ``value_serializer_string_array`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        Processed value.
    
    Returns
    -------
    output : `object`
    """
    return value_serializer_string_array(input_value)
