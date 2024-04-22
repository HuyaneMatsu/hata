import vampytest

from ..fields import parse_finalized


def _iter_options():
    yield {}, False
    yield {'results': None}, False
    yield {'results': {}}, False
    yield {'results': {'is_finalized': None}}, False
    yield {'results': {'is_finalized': False}}, False
    yield {'results': {'is_finalized': True}}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_finalized(input_data):
    """
    Tests whether ``parse_finalized`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_finalized(input_data)
    vampytest.assert_instance(output, bool)
    return output
