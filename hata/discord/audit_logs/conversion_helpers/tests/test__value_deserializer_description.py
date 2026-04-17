import vampytest

from ..converters import value_deserializer_description


def _iter_options():
    description = 'koishi'
    yield None, None
    yield '', None
    yield description, description


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_deserializer_description(input_value):
    """
    Tests whether ``value_deserializer_description`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | str`
    """
    output = value_deserializer_description(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
