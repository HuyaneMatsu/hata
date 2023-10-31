import vampytest

from ..converters import get_converter_ids


def _iter_options():
    entity_id_0 = 202310230000
    entity_id_1 = 202310230001
    
    yield None, None
    yield [], None
    yield [str(entity_id_0), str(entity_id_1)], (entity_id_0, entity_id_1)
    yield [str(entity_id_1), str(entity_id_0)], (entity_id_0, entity_id_1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_converter_ids(input_value):
    """
    Tests whether ``get_converter_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    return get_converter_ids(input_value)
