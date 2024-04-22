import vampytest

from ..preinstanced import PollLayout

from ..fields import parse_layout


def _iter_options():
    yield {}, PollLayout.default
    yield {'layout_type': None}, PollLayout.none
    yield {'layout_type': PollLayout.default.value}, PollLayout.default
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_layout(input_data):
    """
    Tests whether ``parse_layout`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``PollLayout``
    """
    output = parse_layout(input_data)
    vampytest.assert_instance(output, PollLayout)
    return output
