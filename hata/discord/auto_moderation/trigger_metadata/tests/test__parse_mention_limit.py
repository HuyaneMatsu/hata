import vampytest

from ..constants import AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX
from ..fields import parse_mention_limit

def test__parse_mention_limit():
    """
    Tests whether ``parse_mention_limit`` works as intended.
    """
    for input_data, expected_output in (
        ({}, AUTO_MODERATION_TRIGGER_MENTION_LIMIT_MAX),
        ({'mention_total_limit': 1}, 1),
    ):
        output = parse_mention_limit(input_data)
        vampytest.assert_eq(output, expected_output)
