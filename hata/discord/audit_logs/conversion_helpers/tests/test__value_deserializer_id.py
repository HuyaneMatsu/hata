import vampytest

from ..converters import value_deserializer_id


def _iter_options():
    entity_id = 202310220015
    yield None, 0
    yield str(entity_id), entity_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_deserializer_id(input_value):
    """
    Tests whether ``value_deserializer_id`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return value_deserializer_id(input_value)
