import vampytest

from ..converters import value_deserializer_name


def _iter_options():
    name = 'koishi'
    yield None, ''
    yield name, name


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_deserializer_name(input_value):
    """
    Tests whether ``value_deserializer_name`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `str`
    """
    return value_deserializer_name(input_value)
