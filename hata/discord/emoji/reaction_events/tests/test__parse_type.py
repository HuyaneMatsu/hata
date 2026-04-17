import vampytest

from ...reaction import ReactionType

from ..fields import parse_type


def _iter_options():
    yield {}, ReactionType.standard
    yield {'burst': False}, ReactionType.standard
    yield {'burst': True}, ReactionType.burst


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ReactionType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, ReactionType)
    return output
