import vampytest

from ..converters import put_converter_ids


def _iter_options():
    entity_id_0 = 202310230002
    entity_id_1 = 202310230003
    
    yield None, []
    yield (entity_id_0, entity_id_1), [str(entity_id_0), str(entity_id_1)]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_converter_ids(input_value):
    """
    Tests whether ``put_converter_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        Raw value.
    
    Returns
    -------
    output : `list<str>`
    """
    return put_converter_ids(input_value)
