import vampytest

from ..fields import parse_age_gated


def _iter_options():
    yield {}, False
    yield {'requires_age_gate': False}, False
    yield {'requires_age_gate': True}, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_age_gated(input_data):
    """
    Tests whether ``parse_age_gated`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `bool`
    """
    return parse_age_gated(input_data)
