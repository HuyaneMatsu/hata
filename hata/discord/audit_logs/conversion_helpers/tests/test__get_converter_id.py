import vampytest

from ..converters import get_converter_id


def _iter_options():
    entity_id = 202310220015
    yield None, 0
    yield str(entity_id), entity_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_converter_id(input_value):
    """
    Tests whether ``get_converter_id`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return get_converter_id(input_value)
