import vampytest

from ..fields import parse_entitlement_ids


def _iter_options():
    entitlement_id_0 = 202409220006
    entitlement_id_1 = 202409220007
    
    yield {}, None
    yield {'entitlement_ids': None}, None
    yield {'entitlement_ids': []}, None
    yield {'entitlement_ids': [str(entitlement_id_0), str(entitlement_id_1)]}, (entitlement_id_0, entitlement_id_1)
    yield {'entitlement_ids': [str(entitlement_id_1), str(entitlement_id_0)]}, (entitlement_id_0, entitlement_id_1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_entitlement_ids(input_data):
    """
    Tests whether ``parse_entitlement_ids`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    output = parse_entitlement_ids(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
