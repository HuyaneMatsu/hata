import vampytest

from ..fields import put_entity_id_into


def _iter_options():
    entity_id = 202303140007
    
    yield 0, False, {}
    yield 0, True, {'entity_id': None}
    yield entity_id, False, {'entity_id': str(entity_id)}
    yield entity_id, True, {'entity_id': str(entity_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_entity_id_into(input_value, defaults):
    """
    Tests whether ``put_entity_id_into`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to serialize.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_entity_id_into(input_value, {}, defaults)
