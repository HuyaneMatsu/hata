import vampytest

from ..fields import parse_id


def _iter_options():
    application_entity_id = 202211240041
    
    yield {}, 0
    yield {'id': None}, 0
    yield {'id': str(application_entity_id)}, application_entity_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_id(input_data):
    """
    Tests whether ``parse_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    return parse_id(input_data)
