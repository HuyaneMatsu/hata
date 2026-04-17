import vampytest

from ..converters import value_serializer_ids


def _iter_options():
    entity_id_0 = 202310230002
    entity_id_1 = 202310230003
    
    yield None, []
    yield (entity_id_0, entity_id_1), [str(entity_id_0), str(entity_id_1)]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__value_serializer_ids(input_value):
    """
    Tests whether ``value_serializer_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        Raw value.
    
    Returns
    -------
    output : `list<str>`
    """
    output = value_serializer_ids(input_value)
    vampytest.assert_instance(output, list)
    return output
