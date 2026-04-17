import vampytest

from ..fields import parse_dependent_sku_id


def _iter_options():
    dependent_sku_id = 202506290000

    yield {}, 0
    yield {'dependent_sku_id': None}, 0
    yield {'dependent_sku_id': str(dependent_sku_id)}, dependent_sku_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_dependent_sku_id(input_data):
    """
    Tests whether ``parse_dependent_sku_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_dependent_sku_id(input_data)
    vampytest.assert_instance(output, int)
    return output
