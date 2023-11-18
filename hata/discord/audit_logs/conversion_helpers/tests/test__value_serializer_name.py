import vampytest

from ..converters import value_serializer_name


def _iter_options():
    name = 'koishi'
    yield '', ''
    yield name, name


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_serializer_name(input_value):
    """
    Tests whether ``value_serializer_name`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return value_serializer_name(input_value)
