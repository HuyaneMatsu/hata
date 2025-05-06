import vampytest

from ..converters import value_deserializer_string_array


def _iter_options():
    string_0 = 'koishi'
    string_1 = 'satori'
    
    yield None, None
    yield [], None
    yield [string_0, string_1], (string_0, string_1)
    yield [string_1, string_0], (string_0, string_1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_deserializer_string_array(input_value):
    """
    Tests whether ``value_deserializer_string_array`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    output = value_deserializer_string_array(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
