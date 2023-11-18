import vampytest

from ..converters import value_serializer_description


def _iter_options():
    description = 'koishi'
    yield None, ''
    yield description, description


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_serializer_description(input_value):
    """
    Tests whether ``value_serializer_description`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return value_serializer_description(input_value)
