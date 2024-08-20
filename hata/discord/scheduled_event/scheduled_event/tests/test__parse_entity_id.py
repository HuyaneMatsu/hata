import vampytest

from ..fields import parse_entity_id


def _iter_options():
    entity_id = 202303140006
    
    yield {}, 0
    yield {'entity_id': None}, 0
    yield {'entity_id': str(entity_id)}, entity_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_entity_id(input_data):
    """
    Tests whether ``parse_entity_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_entity_id(input_data)
    vampytest.assert_instance(output, int)
    return output
