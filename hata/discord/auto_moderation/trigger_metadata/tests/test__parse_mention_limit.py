import vampytest

from ..constants import AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
from ..fields import parse_mention_limit


def _iter_options():
    yield {}, AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
    yield {'mention_total_limit': None}, AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
    yield {'mention_total_limit': 1}, 1


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_mention_limit(input_data):
    """
    Tests whether ``parse_mention_limit`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    output = parse_mention_limit(input_data)
    vampytest.assert_instance(output, int)
    return output
