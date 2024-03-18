import vampytest

from ..fields import parse_invitable


def _iter_options():
    yield {}, True
    yield {'thread_metadata': {}}, True
    yield {'thread_metadata': {'invitable': False}}, False
    yield {'thread_metadata': {'invitable': True}}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_invitable(input_data):
    """
    Tests whether ``parse_invitable`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    output = parse_invitable(input_data)
    vampytest.assert_instance(output, bool)
    return output
